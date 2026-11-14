"""crossref reader for commonmeta-py"""

from __future__ import annotations

from xml.parsers.expat import ExpatError

import requests
from requests.exceptions import ConnectionError, ReadTimeout

from ..api_utils import COMMONMETA_USER_AGENT
from ..author_utils import get_authors
from ..base_utils import (
    compact,
    dig,
    first,
    flatten,
    parse_attributes,
    parse_xml,
    pascal_case,
    presence,
    sanitize,
    unique,
    wrap,
)
from ..constants import (
    CM_NOTICE_TYPES,
    CR_TO_CM_CONTAINER_TRANSLATIONS,
    CR_TO_CM_TRANSLATIONS,
    CR_UPDATE_SOURCE_TO_CM,
    CR_UPDATE_TO_CM_RELATION_TYPES,
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


def get_crossref_list(query: dict, **kwargs) -> list[dict]:
    """get_crossref list from Crossref API."""
    url = crossref_api_query_url(query, **kwargs)
    headers = {"User-Agent": COMMONMETA_USER_AGENT}
    response = requests.get(url, timeout=30, headers=headers, **kwargs)
    if response.status_code != 200:
        return []
    return response.json().get("message", {}).get("items", [])


def get_crossref(pid: str | None, **kwargs) -> dict:
    """get_crossref"""
    doi = validate_doi(pid)
    if doi is None:
        return {"state": "not_found"}
    url = crossref_api_url(doi)
    headers = {"User-Agent": COMMONMETA_USER_AGENT}
    response = requests.get(url, timeout=10, headers=headers, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return {**response.json().get("message", {}), "via": "crossref"}


def read_crossref(data: dict | None, **kwargs) -> Commonmeta:
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
    title, additional_titles = get_titles(meta)
    publisher = compact({"name": meta.get("publisher", None)})
    # Front Matter blog content is registered as posted-content (Preprint) or a
    # journal (Journal) but maps to BlogPost / Blog. Front Matter may be the
    # publisher (Rogue Scholar) or the institution (Crossref-registered blogs).
    institution_names = [
        i.get("name", None)
        for i in wrap(meta.get("institution", None))
        if isinstance(i, dict)
    ]
    if "Front Matter" in institution_names or dig(publisher, "name") == "Front Matter":
        if _type == "Preprint":
            _type = "BlogPost"
        elif _type == "Journal":
            _type = "Blog"
    # A notice that retracts or corrects another work is a Retraction or an
    # Erratum, though Crossref types it as the article it is published as.
    notice_type = get_notice_type(meta.get("update-to", None))
    if notice_type and _type not in CONTAINER_WORK_TYPES:
        _type = notice_type
    date_published = (
        dig(meta, "issued.date-time")
        or get_date_from_date_parts(meta.get("issued", None))
        or dig(meta, "created.date-time")
    )
    # The DOI is the primary id; it is not duplicated into identifiers.
    identifiers: list = []
    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_[0].get("URL", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None
    issn = get_issn(meta)
    container = get_container(meta, issn=issn)
    if _type == "BlogPost":
        # a blog post has no additional_type and its container is a Blog
        additional_type = None
        if container:
            container = {**container, "type": "Blog"}
    relations = get_relations(meta.get("relation", None))
    if issn is not None:
        relations.append(
            {
                "id": issn_as_url(issn),
                "type": "IsPartOf",
            }
        )
        relations = unique(relations)
    for relation in get_update_relations(meta, _id):
        if relation not in relations:
            relations.append(relation)
    references = unique([get_reference(i) for i in wrap(meta.get("reference", None))])
    funding_references = from_crossref_funding(wrap(meta.get("funder", None)))
    description, additional_descriptions = get_abstract(meta)
    subjects = unique([{"subject": i} for i in wrap(meta.get("subject", None))])
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
            "additional_descriptions": presence(additional_descriptions),
            "additional_titles": presence(additional_titles),
            "additional_type": additional_type,
            "archive_locations": presence(archive_locations),
            "container": presence(container),
            "contributors": presence(contributors),
            "date_published": presence(date_published),
            "description": description,
            "files": presence(files),
            "funding_references": presence(funding_references),
            "geo_locations": None,
            "identifiers": presence(identifiers),
            "language": meta.get("language", None),
            "license": license_,
            "number": presence((meta.get("article-number", None) or "").strip()),
            "provider": "Crossref",
            "publisher": presence(publisher),
            "references": presence(references),
            "relations": presence(relations),
            "state": state,
            "subjects": presence(subjects),
            "title": title,
            "url": url,
            "version": dig(meta, "version.version"),
        },
        **read_options,
    }


def get_titles(meta) -> tuple[str | None, list]:
    """Title information from Crossref metadata.

    Returns a tuple of (title, additional_titles) per the commonmeta v1.0
    schema, where title is a single scalar string and additional_titles
    holds subtitles/translated titles.
    """
    titles = wrap(parse_attributes(meta.get("title", None)))
    subtitles = wrap(parse_attributes(meta.get("subtitle", None)))
    original_language_titles = wrap(
        parse_attributes(meta.get("original_language_title", None))
    )
    language = None

    title = sanitize(titles[0]) if titles else None
    if title is None and original_language_titles:
        # no separate translated title: the original_language_title is the
        # only title present, so it's the primary title, not a translation.
        title = sanitize(original_language_titles[0])
        original_language_titles = original_language_titles[1:]
    additional_titles = (
        [{"title": sanitize(i)} for i in titles[1:]]
        + [
            compact(
                {
                    "title": sanitize(i),
                    "type": "Subtitle",
                }
            )
            for i in subtitles
        ]
        + [
            compact(
                {
                    "title": sanitize(i),
                    "type": "TranslatedTitle",
                    "language": language,
                }
            )
            for i in original_language_titles
        ]
    )
    return title, additional_titles


def get_abstract(meta: dict) -> tuple[str | None, list]:
    """Get abstract from Crossref metadata.

    Returns a tuple of (description, additional_descriptions) per the
    commonmeta v1.0 schema, where description is a single scalar string.
    Crossref only ever provides a single abstract, so
    additional_descriptions is always empty, but is returned for symmetry
    with other readers and future extension.
    """
    abstract = meta.get("abstract", None)
    if abstract is None:
        return None, []

    try:
        # Parse the abstract XML if it is JATS formatted
        description_dct = parse_xml(abstract, xml_attribs=True)
        description = dig(description_dct, "jats:p")
        if description is None:
            description = abstract
        return sanitize(description), []
    except (TypeError, ExpatError):
        return sanitize(abstract), []


def get_reference(reference: dict | None) -> dict | None:
    """Get reference from Crossref reference"""
    if reference is None or not isinstance(reference, dict):
        return None
    doi = reference.get("DOI", None)
    asserted_by_raw = reference.get("doi-asserted-by", None)
    metadata = {
        "key": reference.get("key", None),
        "id": normalize_doi(doi) if doi else None,
        # the formatted reference string prefers the unstructured citation,
        # then falls back to the structured article title.
        "reference": reference.get("unstructured", None)
        or reference.get("article-title", None),
        "publisher": reference.get("publisher", None),
        "publication_year": reference.get("year", None),
        "volume": reference.get("volume", None),
        "issue": reference.get("issue", None),
        "first_page": reference.get("first-page", None),
        "last_page": reference.get("last-page", None),
        "asserted_by": asserted_by_raw.capitalize() if asserted_by_raw else None,
    }
    return compact(metadata)


# Crossref types that name a container rather than a work; a notice registered
# as one keeps its type.
CONTAINER_WORK_TYPES = ("Journal", "Blog", "BookSeries", "ProceedingsSeries")


def _update_relation_types(update: dict) -> tuple[str, str] | None:
    """The (on the updated work, on the notice) relation types of an update."""
    update_type = str(update.get("type", None) or "").lower()
    update_type = update_type.replace("-", "_").replace(" ", "_")
    return CR_UPDATE_TO_CM_RELATION_TYPES.get(update_type, None)


def get_notice_type(updates: list | None) -> str | None:
    """The commonmeta type of a notice that retracts or corrects another work."""
    for update in wrap(updates):
        types = _update_relation_types(update) if isinstance(update, dict) else None
        if types and types[1] in CM_NOTICE_TYPES:
            return CM_NOTICE_TYPES[types[1]]
    return None


def get_update_relations(meta: dict, _id: str | None) -> list:
    """Relations for the notices that retract or correct this work (`updated-by`)
    and the works this notice retracts or corrects (`update-to`).

    Crossref lists an update once per asserting party - the publisher, and
    Retraction Watch for a retraction in its database - and each is kept, with
    `asserted_by`.
    """
    updates = [(u, True) for u in wrap(meta.get("updated-by", None))] + [
        (u, False) for u in wrap(meta.get("update-to", None))
    ]
    relations: list = []
    for update, on_updated_work in updates:
        if not isinstance(update, dict):
            continue
        types = _update_relation_types(update)
        target = doi_as_url(update.get("DOI", None))
        # DOIs are case-insensitive; an update naming the record itself adds nothing
        if types is None or not target or target.lower() == (_id or "").lower():
            continue
        relation = compact(
            {
                "id": target,
                "type": types[0] if on_updated_work else types[1],
                "asserted_by": CR_UPDATE_SOURCE_TO_CM.get(update.get("source", None)),
            }
        )
        if relation not in relations:
            relations.append(relation)
    return relations


def get_relations(relations: dict | None) -> list:
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
        "IsPreprintOf",
        "HasPreprint",
        "IsSupplementTo",
        "IsSupplementedBy",
    ]

    if not relations:
        return []

    def format_relation(key: str, values: list) -> list[dict] | None:
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

    # Format all relations and filter out None values
    formatted = [format_relation(k, v) for k, v in relations.items()]
    valid = [r for r in formatted if r is not None]
    return unique(flatten(valid))


def get_file(file: dict) -> dict:
    """Get file from Crossref"""
    return compact(
        {
            "url": file.get("URL", None),
            "mime_type": file.get("content-type", None),
        }
    )


def get_issn(meta: dict) -> str | None:
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
    normalized = (
        normalize_issn(issn.get("value", None) or issn.get("id", None))
        if issn
        else None
    )
    # fall back to the plain ISSN array when no typed ISSN is present
    if normalized is None:
        normalized = normalize_issn(first(wrap(meta.get("ISSN", None))))
    return normalized


def get_container(meta: dict, issn: str | None) -> dict:
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
    container_title = (
        first(parse_attributes(meta.get("container-title", None), first=True))
        or dig(meta, "group-title")
        or dig(meta, "institution.0.name")
    )
    volume = meta.get("volume", None)
    issue = dig(meta, "journal-issue.issue") or meta.get("issue", None)
    page = meta.get("page", None)
    if page is not None:
        pages = page.split("-")
        first_page = pages[0]
        last_page = pages[1] if len(pages) > 1 else None
    else:
        first_page = None
        last_page = None

    # TODO: add support for series, location, missing in Crossref JSON

    return compact(
        {
            "type": container_type,
            "identifiers": (
                [
                    {
                        "identifier": issn or isbn,
                        "identifier_type": "ISSN" if issn else "ISBN",
                    }
                ]
                if issn or isbn
                else None
            ),
            "title": container_title,
            "volume": volume,
            "issue": issue,
            "first_page": first_page,
            "last_page": last_page,
        }
    )


def from_crossref_funding(funding_references: list) -> list:
    """Get funding references from Crossref"""
    formatted_funding_references = []
    for funding in funding_references:
        # funder_id is ROR-only in v1.0. Crossref Funder ID DOIs (10.13039/...)
        # are translated to ROR; any other DOI has no ROR equivalent, so it's
        # dropped rather than leaking a non-ROR doi.org URL into funder_id.
        funder_id = None
        if funding.get("DOI", "").startswith("10.13039"):
            funder_id = CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS.get(
                doi_as_url(funding["DOI"]), None
            )
        f = compact(
            {
                "funder_name": funding.get("name", None),
                "funder_id": funder_id,
            }
        )
        if (
            funding.get("name", None) is not None
            and funding.get("award", None) is not None
        ):
            for award in wrap(funding["award"]):
                fund_ref = f.copy()
                fund_ref["award_number"] = award
                formatted_funding_references.append(fund_ref)
        elif f != {}:
            formatted_funding_references.append(f)
    return unique(formatted_funding_references)


def get_random_crossref_id(number: int = 1, **kwargs) -> list:
    """Get random DOI from Crossref"""
    number = 20 if number > 20 else number
    url = crossref_api_sample_url(number, **kwargs)
    headers = {"User-Agent": COMMONMETA_USER_AGENT}
    try:
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code != 200:
            return []

        items = dig(response.json(), "message.items")
        return [i.get("DOI") for i in items]
    except (ReadTimeout, ConnectionError):
        return []
