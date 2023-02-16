"""crossref reader for Talbot"""
from typing import Optional, TypedDict
from functools import reduce
import requests
from pydash import py_

from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    from_citeproc,
    normalize_url
)
from ..base_utils import wrap, compact, presence, sanitize
from ..author_utils import get_authors
from ..date_utils import get_date_from_date_parts
from ..doi_utils import doi_as_url, doi_from_url, get_doi_ra, crossref_api_url
from ..constants import (
    CR_TO_BIB_TRANSLATIONS,
    CR_TO_CP_TRANSLATIONS,
    CR_TO_DC_TRANSLATIONS,
    CR_TO_RIS_TRANSLATIONS,
    CR_TO_SO_TRANSLATIONS,
    TalbotMeta
)


def get_crossref(pid: str, **kwargs) -> dict:
    """get_crossref"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = crossref_api_url(doi)
    response = requests.get(url, kwargs, timeout=5)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json().get("message", {})


def read_crossref(data: Optional[dict], **kwargs) -> TalbotMeta:
    """read_crossref"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    # read_options = ActiveSupport::HashWithIndifferentAccess.
    # new(options.except(:doi, :id, :url,
    # :sandbox, :validate, :ra))
    read_options = kwargs or {}

    doi = meta.get("DOI", None)
    pid = doi_as_url(doi)
    resource_type = meta.get("type", {}).title().replace("-", "")
    types = {
        "resourceTypeGeneral": CR_TO_DC_TRANSLATIONS[resource_type] or "Text",
        "resourceType": resource_type,
        "schemaOrg": CR_TO_SO_TRANSLATIONS.get(resource_type, None) or "CreativeWork",
        "citeproc": CR_TO_CP_TRANSLATIONS.get(resource_type, None) or "article-journal",
        "bibtex": CR_TO_BIB_TRANSLATIONS.get(resource_type, None) or "misc",
        "ris": CR_TO_RIS_TRANSLATIONS.get(resource_type, None) or "GEN",
    }
    if meta.get("author", None):
        creators = get_authors(from_citeproc(wrap(meta.get("author"))))
    else:
        creators = [{"nameType": "Organizational", "name": ":(unav)"}]
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
    publisher = meta.get("publisher", None)

    date_created = py_.get(meta, 'created.date-time')
    date_issued = py_.get(meta, 'issued.date-time') or get_date_from_date_parts(meta.get('issued', None))
    date_deposited = py_.get(meta, 'deposited.date-time')
    date_indexed = py_.get(meta, 'indexed.date-time')
    date_registered = py_.get(meta, 'registered.date-time') or date_created
    date_published = date_issued or date_created or ':unav'
    date_updated = date_deposited or date_indexed
    dates = [{"date": date_published, "dateType": "Issued"}]
    if date_updated is not None:
        dates.append({"date": date_updated, "dateType": "Updated"})
    publication_year = int(date_published[0:4]) if date_published else None

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_[0].get("URL", None))
        rights = [dict_to_spdx(
            {"rightsUri": license_})] if license_ else None
    else:
        rights = None

    issns = meta.get("issn-type", None)
    if issns is not None:
        issn = (
            next(
                (item for item in issns if item["type"] == "electronic"), None)
            or next((item for item in issns if item["type"] == "print"), None)
            or {}
        )
        issn = issn["value"] if issn else None
    else:
        issn = None
    if issn is not None:
        related_items = [
            compact(
                {
                    "relationType": "IsPartOf",
                    "relatedItemIdentifierType": "ISSN",
                    "resourceTypeGeneral": "Collection",
                    "relatedItemIdentifier": issn,
                }
            )
        ]
    else:
        related_items = []
    related_items += [get_related_item(i) for i in wrap(meta.get("reference", []))]

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
    container_title = container_titles[0] if len(
        container_titles) > 0 else None
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

    if issn:
        related_items = [
            {
                "relationType": "IsPartOf",
                "relatedItemIdentifierType": "ISSN",
                "resourceTypeGeneral": "Collection",
                "relatedItemIdentifier": issn,
            }
        ]
    else:
        related_items = []
    references = meta.get("reference", [])
    for ref in references:
        related_items.append(get_related_item(ref))

    funding_references = from_crossref_funding(wrap(meta.get("funder", None)))

    description = meta.get("abstract", None)
    if description is not None:
        descriptions = [
            {"description": sanitize(description),
             "descriptionType": "Abstract"}
        ]
    else:
        descriptions = None

    state = "findable" if meta or read_options else "not_found"
    subjects = [{'subject': i} for i in wrap(meta.get("subject", []))]

    return {
        # required properties
        "pid": pid,
        "doi": doi,
        "url": url,
        "creators": creators,
        "titles": presence(titles),
        "types": types,
        "publisher": publisher,
        "publication_year": publication_year,
        # recommended and optional properties
        "subjects": presence(subjects),
        "contributors": contributors,
        "dates": dates,
        "language": meta.get("language", None),
        "alternate_identifiers": None,
        "sizes": None,
        "formats": None,
        "version": meta.get("version", None),
        "rights": rights,
        "descriptions": descriptions,
        "geo_locations": None,
        "funding_references": presence(funding_references),
        "related_items": related_items,
        # other properties
        "date_created": date_created,
        "date_registered": date_registered,
        "date_published": date_published,
        "date_updated": date_updated,
        "content_url": presence(meta.get("contentUrl", None)),
        "container": container,
        "agency": get_doi_ra(pid),
        "state": state,
        "schema_version": None
    } | read_options


def get_related_item(reference: Optional[dict]) -> Optional[dict]:
    """Get related_item from Crossref reference"""
    if reference is None or not isinstance(reference, dict):
        return None
    doi = reference.get("DOI", None)
    metadata = {
        "key": reference.get("key", None),
        "relationType": "References",
        "relatedItemType": None,
    }
    if doi is not None:
        metadata = metadata | {
            "relatedItemIdentifier": doi.lower(),
            "relatedItemIdentifierType": "DOI",
        }
    else:
        metadata = metadata | {
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
            "unstructured": reference.get("unstructured", None)
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
