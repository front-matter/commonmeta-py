"""crossref reader for commonmeta-py"""
from typing import Optional
import requests
from pydash import py_

from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    from_csl,
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
    get_crossref_member,
    crossref_api_url,
)
from ..constants import (
    CR_TO_CM_TRANSLATIONS,
    CR_TO_CM_CONTAINER_TRANSLATIONS,
    CROSSREF_CONTAINER_TYPES,
    Commonmeta,
)


def get_crossref(pid: str, **kwargs) -> dict:
    """get_crossref"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = crossref_api_url(doi)
    response = requests.get(url, kwargs, timeout=10)
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
    id_ = doi_as_url(doi)
    resource_type = meta.get("type", {}).title().replace("-", "")
    type_ = CR_TO_CM_TRANSLATIONS.get(resource_type, "Other")

    if meta.get("author", None):
        contributors = get_authors(from_csl(wrap(meta.get("author"))))
    else:
        contributors = None

    def editor_type(item):
        item["contributorType"] = "Editor"
        return item

    editors = [editor_type(i) for i in wrap(meta.get("editor", None))]
    if editors:
        contributors += get_authors(from_csl(editors))

    url = normalize_url(py_.get(meta, "resource.primary.URL"))
    titles = get_titles(meta)

    member_id = meta.get("member", None)
    # TODO: get publisher from member_id almost always return publisher name, but sometimes does not
    if member_id is not None:
        publisher = get_crossref_member(member_id)
    else:
        publisher = meta.get("publisher", None)

    date: dict = {}
    date["submitted"] = None
    date["accepted"] = py_.get(meta, "accepted.date-time")
    date["published"] = (
        py_.get(meta, "issued.date-time")
        or get_date_from_date_parts(meta.get("issued", None))
        or py_.get(meta, "created.date-time")
    )
    date["updated"] = py_.get(meta, "updated.date-time") or py_.get(
        meta, "deposited.date-time"
    )

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_[0].get("URL", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    container = get_container(meta, resource_type=resource_type)

    references = [get_reference(i) for i in wrap(meta.get("reference", None))]
    funding_references = from_crossref_funding(wrap(meta.get("funder", None)))

    description = meta.get("abstract", None)
    if description is not None:
        descriptions = [
            {"description": sanitize(description), "descriptionType": "Abstract"}
        ]
    else:
        descriptions = None

    subjects = [{"subject": i} for i in wrap(meta.get("subject", []))]
    files = [
        get_file(i)
        for i in wrap(meta.get("link", None))
        if i["content-type"] != "unspecified"
    ]

    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "id": id_,
        "type": type_,
        "url": url,
        "contributors": contributors,
        "titles": presence(titles),
        "publisher": publisher,
        "date": compact(date),
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
        "references": references,
        # other properties
        "files": presence(files),
        "container": presence(container),
        "provider": get_doi_ra(id_),
        "state": state,
        "schema_version": None,
    } | read_options


def get_titles(meta):
    """Title information from Crossref metadata."""
    title = parse_attributes(meta.get("title", None))
    subtitle = parse_attributes(meta.get("subtitle", None))
    original_language_title = meta.get("original_language_title", None)
    language = None
    if title is None and original_language_title is None and subtitle is None:
        return None
    if title is not None and subtitle is None:
        return [{"title": sanitize(title)}]
    if original_language_title:
        return [
            compact(
                {
                    "title": sanitize(original_language_title),
                    "lang": language,
                }
            )
        ]
    if subtitle:
        return [
            compact({"title": sanitize(title)}),
            {
                "title": sanitize(subtitle),
                "titleType": "Subtitle",
            },
        ]


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


def get_container(meta: dict, resource_type: str = "JournalArticle") -> dict:
    """Get container from Crossref"""
    container_type = CROSSREF_CONTAINER_TYPES.get(resource_type, None)
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
