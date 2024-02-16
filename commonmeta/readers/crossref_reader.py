"""crossref reader for commonmeta-py"""
from typing import Optional
import httpx
from pydash import py_
import time

from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    normalize_url,
    normalize_doi,
    normalize_issn,
)
from ..base_utils import wrap, compact, presence, sanitize, parse_attributes
from ..author_utils import get_authors
from ..date_utils import get_date_from_date_parts
from ..doi_utils import (
    doi_as_url,
    doi_from_url,
    get_doi_ra,
    # get_crossref_member,
    crossref_api_url,
    crossref_api_query_url,
    crossref_api_sample_url,
)
from ..constants import (
    CR_TO_CM_TRANSLATIONS,
    CR_TO_CM_CONTAINER_TRANSLATIONS,
    CROSSREF_CONTAINER_TYPES,
    Commonmeta,
)


def timer_func(func):
    def function_timer(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "{func} took {time} seconds to complete its execution."
        print(msg.format(func=func.__name__, time=runtime))
        return value

    return function_timer


def get_crossref_list(query: dict, **kwargs) -> list[dict]:
    """get_crossref list from Crossref API."""
    url = crossref_api_query_url(query, **kwargs)
    response = httpx.get(url, timeout=30, **kwargs)
    if response.status_code != 200:
        return []
    return response.json().get("message", {}).get("items", [])


def get_crossref(pid: str, **kwargs) -> dict:
    """get_crossref"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = crossref_api_url(doi)
    response = httpx.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json().get("message", {})


def read_crossref(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_crossref"""
    if data is None:
        return {"state": "not_found"}
    meta = data
    # read_options = ActiveSupport::HashWithIndifferentAccess.
    # new(options.except(:doi, :id, :url,
    # :sandbox, :validate, :ra))
    read_options = kwargs or {}

    doi = meta.get("DOI", None)
    _id = doi_as_url(doi)
    _type = CR_TO_CM_TRANSLATIONS.get(meta.get("type", None))

    if meta.get("author", None):
        contributors = get_authors(wrap(meta.get("author")))
    else:
        contributors = []

    def editor_type(item):
        item["contributorType"] = "Editor"
        return item

    editors = [editor_type(i) for i in wrap(meta.get("editor", None))]
    if editors:
        contributors += get_authors(editors)

    url = normalize_url(py_.get(meta, "resource.primary.URL"))
    titles = get_titles(meta)
    publisher = compact({"name": meta.get("publisher", None)})

    date = compact(
        {
            "published": py_.get(meta, "issued.date-time")
            or get_date_from_date_parts(meta.get("issued", None))
            or py_.get(meta, "created.date-time")
        }
    )

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_[0].get("URL", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    container = get_container(meta)
    references = [get_reference(i) for i in wrap(meta.get("reference", None))]
    funding_references = from_crossref_funding(wrap(meta.get("funder", None)))

    description = meta.get("abstract", None)
    if description is not None:
        descriptions = [
            {"description": sanitize(description), "descriptionType": "Abstract"}
        ]
    else:
        descriptions = None

    subjects = py_.uniq([{"subject": i} for i in wrap(meta.get("subject", []))])
    files = [
        get_file(i)
        for i in wrap(meta.get("link", None))
        if i["content-type"] != "unspecified"
    ]

    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "id": _id,
        "type": _type,
        "url": url,
        "contributors": presence(contributors),
        "titles": presence(titles),
        "publisher": presence(publisher),
        "date": presence(date),
        # recommended and optional properties
        "subjects": presence(subjects),
        "language": meta.get("language", None),
        "alternate_identifiers": None,
        "sizes": None,
        "formats": None,
        "version": meta.get("version", None),
        "license": license_,
        "descriptions": descriptions,
        "geo_locations": None,
        "funding_references": presence(funding_references),
        "references": presence(references),
        # other properties
        "files": presence(files),
        "container": presence(container),
        "provider": get_doi_ra(_id),
        "state": state,
        "schema_version": None,
    } | read_options


def get_titles(meta):
    """Title information from Crossref metadata."""
    titles = wrap(parse_attributes(meta.get("title", None)))
    subtitles = wrap(parse_attributes(meta.get("subtitle", None)))
    original_language_titles = wrap(
        parse_attributes(meta.get("original_language_title", None))
    )
    language = None
    return (
        [{"title": sanitize(i)} for i in titles]
        + [
            compact(
                {
                    "title": sanitize(i),
                    "titleType": "Subtitle",
                }
            )
            for i in subtitles
        ]
        + [
            compact(
                {
                    "title": sanitize(i),
                    "titleType": "TranslatedTitle",
                    "lang": language,
                }
            )
            for i in original_language_titles
        ]
    )


def get_reference(reference: Optional[dict]) -> Optional[dict]:
    """Get reference from Crossref reference"""
    if reference is None or not isinstance(reference, dict):
        return None
    doi = reference.get("DOI", None)
    metadata = {
        "key": reference.get("key", None),
        "doi": normalize_doi(doi) if doi else None,
        "contributor": reference.get("author", None),
        "title": reference.get("article-title", None),
        "publisher": reference.get("publisher", None),
        "publicationYear": reference.get("year", None),
        "volume": reference.get("volume", None),
        "issue": reference.get("issue", None),
        "firstPage": reference.get("first-page", None),
        "lastPage": reference.get("last-page", None),
        "containerTitle": reference.get("journal-title", None),
        "edition": None,
        "unstructured": reference.get("unstructured", None) if doi is None else None,
    }
    return compact(metadata)


def get_file(file: dict) -> dict:
    """Get file from Crossref"""
    return compact(
        {
            "url": file.get("URL", None),
            "mimeType": file.get("content-type", None),
        }
    )


def get_container(meta: dict) -> dict:
    """Get container from Crossref"""
    container_type = CROSSREF_CONTAINER_TYPES.get(meta.get("type", None))
    container_type = CR_TO_CM_CONTAINER_TRANSLATIONS.get(container_type, None)
    issn = (
        next(
            (
                item
                for item in wrap(meta.get("issn-type", None))
                if item["type"] == "electronic"
            ),
            None,
        )
        or next(
            (
                item
                for item in wrap(meta.get("issn-type", None))
                if item["type"] == "print"
            ),
            None,
        )
        or {}
    )
    issn = normalize_issn(issn["value"]) if issn else None
    isbn = (
        next(
            (
                item
                for item in wrap(meta.get("isbn-type", None))
                if item["type"] == "electronic"
            ),
            None,
        )
        or next(
            (
                item
                for item in wrap(meta.get("isbn-type", None))
                if item["type"] == "print"
            ),
            None,
        )
        or {}
    )
    isbn = isbn["value"] if isbn else None
    container_title = parse_attributes(meta.get("container-title", None), first=True)
    volume = meta.get("volume", None)
    issue = py_.get(meta, "journal-issue.issue")
    if meta.get("page", None):
        pages = meta.get("page", None).split("-")
        first_page = pages[0]
        last_page = pages[1] if len(pages) > 1 else None
    else:
        first_page = None
        last_page = None

    # TODO: add support for series, location, missing in Crossref JSON

    return compact(
        {
            "type": container_type,
            "identifier": issn or isbn,
            "identifierType": "ISSN" if issn else "ISBN" if isbn else None,
            "title": container_title,
            "volume": volume,
            "issue": issue,
            "firstPage": first_page,
            "lastPage": last_page,
        }
    )


def from_crossref_funding(funding_references: list) -> list:
    """Get funding references from Crossref"""
    formatted_funding_references = []
    for funding in funding_references:
        funding_reference = compact(
            {
                "funderName": funding.get("name", None),
                "funderIdentifier": doi_as_url(funding["DOI"])
                if funding.get("DOI", None) is not None
                else None,
                "funderIdentifierType": "Crossref Funder ID"
                if funding.get("DOI", "").startswith("10.13039")
                else None,
            }
        )
        funding_reference = py_.omit(funding_reference, "DOI", "doi-asserted-by")
        if (
            funding.get("name", None) is not None
            and funding.get("award", None) is not None
        ):
            for award in wrap(funding["award"]):
                fund_ref = funding_reference.copy()
                fund_ref["awardNumber"] = award
                formatted_funding_references.append(fund_ref)
        elif funding_reference != {}:
            formatted_funding_references.append(funding_reference)
    return formatted_funding_references


def get_random_crossref_id(number: int = 1, **kwargs) -> list:
    """Get random DOI from Crossref"""
    number = 20 if number > 20 else number
    url = crossref_api_sample_url(number, **kwargs)
    try:
        response = httpx.get(url, timeout=10)
        if response.status_code != 200:
            return []

        items = py_.get(response.json(), "message.items")
        return [i.get("DOI") for i in items]
    except (httpx.exceptions.ReadTimeout, httpx.exceptions.ConnectionError):
        return []
