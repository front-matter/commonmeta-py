"""crossref reader for commonmeta-py"""
from typing import Optional
import requests
from pydash import py_

from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    from_citeproc,
    normalize_url,
    normalize_doi,
)
from ..base_utils import wrap, compact, presence, sanitize
from ..author_utils import get_authors
from ..date_utils import get_date_from_date_parts
from ..doi_utils import doi_as_url, doi_from_url, get_doi_ra, get_crossref_member, crossref_api_url
from ..constants import (
    CR_TO_CM_TRANSLATIONS,
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
    type_ = CR_TO_CM_TRANSLATIONS.get(resource_type, 'Other')

    if meta.get("author", None):
        creators = get_authors(from_citeproc(wrap(meta.get("author"))))
    else:
        creators = None

    def editor_type(item):
        item["ContributorType"] = "Editor"
        return item

    editors = [editor_type(i) for i in wrap(meta.get("editor", None))]
    contributors = presence(get_authors(from_citeproc(editors)))

    url = normalize_url(py_.get(meta, "resource.primary.URL"))
    title = meta.get("title", None) or meta.get("original-title")
    if isinstance(title, list) and len(title) > 0:
        title = title[0]
    if isinstance(title, str):
        titles = [{"title": sanitize(title)}]
    else:
        titles = []

    member_id = meta.get("member", None)
    # TODO: get publisher from member_id almost always return publisher name, but sometimes does not
    if member_id is not None:
        publisher = get_crossref_member(member_id)
    else:
        publisher = meta.get("publisher", None)

    date: dict = {}
    date['submitted'] = None
    date['accepted'] = py_.get(meta, "accepted.date-time")
    date['published'] = py_.get(meta, "issued.date-time") or get_date_from_date_parts(
        meta.get("issued", None)) or py_.get(meta, "created.date-time")
    date['updated'] = py_.get(meta, "updated.date-time") or py_.get(meta, "deposited.date-time")

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_[0].get("URL", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    issns = meta.get("issn-type", None)
    if issns is not None:
        issn = (
            next((item for item in issns if item["type"] == "electronic"), None)
            or next((item for item in issns if item["type"] == "print"), None)
            or {}
        )
        issn = issn["value"] if issn else None
    else:
        issn = None

    if resource_type == "JournalArticle":
        container_type = "Journal"
    elif resource_type == "JournalIssue":
        container_type = "Journal"
    elif resource_type == "BookChapter":
        container_type = "Book"
    elif resource_type == "Monograph":
        container_type = "BookSeries"
    else:
        container_type = "Periodical"

    if meta.get("page", None):
        pages = meta.get("page", None).split("-")
        first_page = pages[0]
        last_page = pages[1] if len(pages) > 1 else None
    else:
        first_page = None
        last_page = None

    container_titles = meta.get("container-title", [])
    container_title = container_titles[0] if len(container_titles) > 0 else None
    if container_title is not None:
        container = compact(
            {
                "type": container_type,
                "title": container_title,
                "identifier": issn,
                "identifierType": "ISSN" if issn else None,
                "volume": meta.get("volume", None),
                "issue": meta.get("issue", None),
                "firstPage": first_page,
                "lastPage": last_page,
            }
        )
    else:
        container = None

    references = references = [
        get_reference(i) for i in wrap(meta.get("reference", None))
    ]
    funding_references = from_crossref_funding(wrap(meta.get("funder", None)))

    description = meta.get("abstract", None)
    if description is not None:
        descriptions = [
            {"description": sanitize(description), "descriptionType": "Abstract"}
        ]
    else:
        descriptions = None

    state = "findable" if meta or read_options else "not_found"
    subjects = [{"subject": i} for i in wrap(meta.get("subject", []))]

    return {
        # required properties
        "id": id_,
        "type": type_,
        "doi": doi,
        "url": url,
        "creators": creators,
        "titles": presence(titles),
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional properties
        "subjects": presence(subjects),
        "contributors": contributors,
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
        "content_url": presence(meta.get("contentUrl", None)),
        "container": container,
        "provider": get_doi_ra(id_),
        "state": state,
        "schema_version": None,
    } | read_options


def get_reference(reference: Optional[dict]) -> Optional[dict]:
    """Get reference from Crossref reference"""
    if reference is None or not isinstance(reference, dict):
        return None
    doi = reference.get("DOI", None)
    metadata = {
        "key": reference.get("key", None),
        "doi": normalize_doi(doi) if doi else None,
        "creator": reference.get("author", None),
        "title": reference.get("article-title", None),
        "publisher": reference.get("publisher", None),
        "publicationYear": reference.get("year", None),
        "volume": reference.get("volume", None),
        "issue": reference.get("issue", None),
        "firstPage": reference.get("first-page", None),
        "lastPage": reference.get("last-page", None),
        "containerTitle": reference.get("journal-title", None),
        "edition": None,
        "contributor": None,
        "unstructured": reference.get("unstructured", None) if doi is None else None,
    }
    return compact(metadata)


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
