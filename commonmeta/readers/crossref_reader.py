"""crossref reader for commonmeta-py"""

from typing import List, Optional
from xml.parsers.expat import ExpatError

import requests
from requests.exceptions import ConnectionError, ReadTimeout

from ..author_utils import get_authors
from ..base_utils import (
    compact,
    dig,
    flatten,
    omit,
    parse_attributes,
    parse_xml,
    pascal_case,
    presence,
    sanitize,
    unique,
    wrap,
)
from ..constants import (
    CR_TO_CM_CONTAINER_TRANSLATIONS,
    CR_TO_CM_TRANSLATIONS,
    CROSSREF_CONTAINER_TYPES,
    CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS,
    Commonmeta,
)
from ..date_utils import get_date_from_date_parts
from ..doi_utils import (
    crossref_api_query_url,
    crossref_api_sample_url,
    crossref_api_url,
    doi_as_url,
    validate_doi,
)
from ..utils import (
    dict_to_spdx,
    issn_as_url,
    normalize_cc_url,
    normalize_doi,
    normalize_issn,
    normalize_url,
    validate_isbn,
)


def get_crossref_list(query: dict, **kwargs) -> List[dict]:
    """get_crossref list from Crossref API."""
    url = crossref_api_query_url(query, **kwargs)
    response = requests.get(url, timeout=30, **kwargs)
    if response.status_code != 200:
        return []
    return response.json().get("message", {}).get("items", [])


def get_crossref(pid: str, **kwargs) -> dict:
    """get_crossref"""
    doi = validate_doi(pid)
    if doi is None:
        return {"state": "not_found"}
    url = crossref_api_url(doi)
    response = requests.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return {**response.json().get("message", {}), "via": "crossref"}


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
    _type = CR_TO_CM_TRANSLATIONS.get(meta.get("type", None)) or "Other"
    additional_type = meta.get("subtype", None)

    archive_locations = wrap(meta.get("archive", None))

    if meta.get("author", None):
        contributors = get_authors(wrap(meta.get("author")), via="crossref")
    else:
        contributors = []

    def editor_type(item):
        item["contributorType"] = "Editor"
        return item

    editors = [editor_type(i) for i in wrap(meta.get("editor", None))]
    if editors:
        contributors += get_authors(editors)

    url = normalize_url(dig(meta, "resource.primary.URL"))
    titles = get_titles(meta)
    publisher = compact({"name": meta.get("publisher", None)})
    if _type == "Article" and dig(publisher, "name") == "Front Matter":
        _type = "BlogPost"
    date = compact(
        {
            "published": dig(meta, "issued.date-time")
            or get_date_from_date_parts(meta.get("issued", None))
            or dig(meta, "created.date-time")
        }
    )
    identifiers = []
    identifiers.append(
        compact(
            {
                "identifier": _id,
                "identifierType": "DOI",
            }
        )
    )
    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_[0].get("URL", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None
    issn = get_issn(meta)
    container = get_container(meta, issn=issn)
    relations = get_relations(meta.get("relation", None))
    if issn is not None:
        relations.append(
            {
                "id": issn_as_url(issn),
                "type": "IsPartOf",
            }
        )
        relations = unique(relations)
    references = unique([get_reference(i) for i in wrap(meta.get("reference", None))])
    funding_references = from_crossref_funding(wrap(meta.get("funder", None)))
    descriptions = get_abstract(meta)
    subjects = unique(
        [
            {"subject": i}
            for i in wrap(meta.get("subject", None) or meta.get("group-title", None))
        ]
    )
    files = unique(
        [
            get_file(i)
            for i in wrap(meta.get("link", None))
            if i["content-type"] != "unspecified"
        ]
    )
    state = "findable" if meta or read_options else "not_found"

    return {
        **{
            # required properties
            "id": _id,
            "type": _type,
            # recommended and optional properties
            "additionalType": additional_type,
            "archiveLocations": presence(archive_locations),
            "container": presence(container),
            "contributors": presence(contributors),
            "date": presence(date),
            "descriptions": presence(descriptions),
            "files": presence(files),
            "fundingReferences": presence(funding_references),
            "geoLocations": None,
            "identifiers": identifiers,
            "language": meta.get("language", None),
            "license": license_,
            "publisher": presence(publisher),
            "references": presence(references),
            "relations": presence(relations),
            "subjects": presence(subjects),
            "titles": presence(titles),
            "url": url,
            "version": meta.get("version", None),
            # other properties
            "provider": "Crossref",
            "state": state,
        },
        **read_options,
    }


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


def get_abstract(meta: dict) -> Optional[str]:
    """Get abstract from Crossref metadata."""
    abstract = meta.get("abstract", None)
    if abstract is None:
        return None

    try:
        # Parse the abstract XML if it is JATS formatted
        description_dct = parse_xml(abstract, xml_attribs=True)
        description = dig(description_dct, "jats:p")
        if description is None:
            description = abstract
        return [{"description": sanitize(description), "type": "Abstract"}]
    except (TypeError, ExpatError):
        return [{"description": sanitize(abstract), "type": "Abstract"}]


def get_reference(reference: Optional[dict]) -> Optional[dict]:
    """Get reference from Crossref reference"""
    if reference is None or not isinstance(reference, dict):
        return None
    doi = reference.get("DOI", None)
    metadata = {
        "key": reference.get("key", None),
        "id": normalize_doi(doi) if doi else None,
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
        "unstructured": reference.get("unstructured", None),
    }
    return compact(metadata)


def get_relations(relations: list) -> list:
    """Get relations from Crossref"""
    supported_types = [
        "IsNewVersionOf",
        "IsPreviousVersionOf",
        "IsVersionOf",
        "HasVersion",
        "IsPartOf",
        "HasPart",
        "IsVariantFormOf",
        "IsOriginalFormOf",
        "IsIdenticalTo",
        "IsTranslationOf",
        "IsReviewOf",
        "HasReview",
        "IsPreprintOf",
        "HasPreprint",
        "IsSupplementTo",
        "IsSupplementedBy",
    ]

    if not relations:
        return []

    def format_relation(key, values):
        _type = pascal_case(key)
        if _type not in supported_types:
            return None
        rs = []
        for value in values:
            if value.get("id-type", None) == "doi":
                _id = doi_as_url(value.get("id", None))
            elif value.get("id-type", None) == "issn":
                _id = issn_as_url(value.get("id", None))
            else:
                _id = value.get("id", None)

            rs.append({"type": _type, "id": _id})

        return rs

    return unique(
        compact(flatten([format_relation(k, v) for k, v in relations.items()]))
    )


def get_file(file: dict) -> dict:
    """Get file from Crossref"""
    return compact(
        {
            "url": file.get("URL", None),
            "mimeType": file.get("content-type", None),
        }
    )


def get_issn(meta: dict) -> Optional[str]:
    """Get ISSN from Crossref"""
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
        or next(
            (
                item
                for item in dig(meta, "relation.is-part-of", [])
                if item["id-type"] == "issn"
            ),
            None,
        )
        or {}
    )
    return (
        normalize_issn(issn.get("value", None) or issn.get("id", None))
        if issn
        else None
    )


def get_container(meta: dict, issn: str) -> dict:
    """Get container from Crossref"""
    container_type = CROSSREF_CONTAINER_TYPES.get(meta.get("type", None))
    container_type = CR_TO_CM_CONTAINER_TRANSLATIONS.get(container_type, None)
    # TODO: ISBN not included in ProceedingsArticle metadata
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
    isbn = validate_isbn(isbn["value"]) if isbn else None
    container_title = parse_attributes(meta.get("container-title", None), first=True)
    if not container_title:
        container_title = dig(meta, "institution.0.name")
    volume = meta.get("volume", None)
    issue = dig(meta, "journal-issue.issue")
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
        f = compact(
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
        if f.get("funderIdentifierType", None) == "Crossref Funder ID":
            # convert to ROR
            funderIdentifier = CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS.get(
                f.get("funderIdentifier", None)
            )
            if funderIdentifier:
                f["funderIdentifier"] = funderIdentifier
                f["funderIdentifierType"] = "ROR"
        f = omit(f, "DOI", "doi-asserted-by")
        if (
            funding.get("name", None) is not None
            and funding.get("award", None) is not None
        ):
            for award in wrap(funding["award"]):
                fund_ref = f.copy()
                fund_ref["awardNumber"] = award
                formatted_funding_references.append(fund_ref)
        elif f != {}:
            formatted_funding_references.append(f)
    return unique(formatted_funding_references)


def get_random_crossref_id(number: int = 1, **kwargs) -> list:
    """Get random DOI from Crossref"""
    number = 20 if number > 20 else number
    url = crossref_api_sample_url(number, **kwargs)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []

        items = dig(response.json(), "message.items")
        return [i.get("DOI") for i in items]
    except (ReadTimeout, ConnectionError):
        return []
