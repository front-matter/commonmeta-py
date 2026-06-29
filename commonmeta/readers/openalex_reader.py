"""OpenAlex reader for commonmeta-py"""

from __future__ import annotations

from requests.exceptions import ConnectionError, ReadTimeout

from ..api_utils import COMMONMETA_USER_AGENT, http
from ..author_utils import get_authors
from ..base_utils import compact, dig, presence, sanitize, unique, wrap
from ..constants import (
    CR_TO_CM_TRANSLATIONS,
    OA_TO_CM_CONTAINER_TRANLATIONS,
    OA_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..doi_utils import normalize_doi
from ..utils import (
    dict_to_spdx,
    normalize_orcid,
    normalize_ror,
    normalize_url,
    openalex_api_query_url,
    openalex_api_sample_url,
    openalex_api_url,
    validate_id,
    validate_openalex,
)

# Map OpenAlex license strings to SPDX licenseId.
OA_LICENSES = {
    "cc-by": "CC-BY-4.0",
    "cc0": "CC0-1.0",
    "cc-by-sa": "CC-BY-SA-4.0",
    "cc-by-nc": "CC-BY-NC-4.0",
    "cc-by-nd": "CC-BY-ND-4.0",
    "cc-by-nc-sa": "CC-BY-NC-SA-4.0",
    "cc-by-nc-nd": "CC-BY-NC-ND-4.0",
}
OA_IDENTIFIER_TYPES = {
    "openalex": "OpenAlex",
    "doi": "DOI",
    "pmid": "PMID",
    "pmcid": "PMCID",
}


def get_openalex_list(query: dict, **kwargs) -> list[dict]:
    """get_openalex list from OpenAlex API."""
    url = openalex_api_query_url(query, **kwargs)
    response = http.get(url, timeout=30, **kwargs)
    if response.status_code != 200:
        return []
    return response.json().get("results", [])


def get_openalex(pid: str, **kwargs) -> dict:
    """get_openalex"""
    id, identifier_type = validate_id(pid)
    if identifier_type not in ["DOI", "MAG", "OpenAlex", "PMID", "PMCID"]:
        return {"state": "not_found"}
    url = openalex_api_url(id, identifier_type, **kwargs)
    headers = {"User-Agent": COMMONMETA_USER_AGENT}
    response = http.get(url, timeout=10, headers=headers, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    # OpenAlex returns record as list
    if identifier_type in ["MAG", "PMID", "PMCID"]:
        return dig(response.json(), "results[0]") | {"via": "openalex"}
    return response.json() | {"via": "openalex"}


def read_openalex(data: dict | None, **kwargs) -> Commonmeta:
    """read_openalex"""
    if data is None:
        return {"state": "not_found"}
    meta = data
    read_options = kwargs or {}

    _id = meta.get("doi", None) or meta.get("id", None)

    # type_crossref was removed from top-level; the equivalent
    # Crossref-style classification now lives at primary_location.raw_type.
    _type = (
        CR_TO_CM_TRANSLATIONS.get(meta.get("type_crossref"))
        or CR_TO_CM_TRANSLATIONS.get(dig(meta, "primary_location.raw_type"))
        or "Other"
    )
    additional_type = OA_TO_CM_TRANSLATIONS.get(meta.get("type", None))
    if additional_type == _type:
        additional_type = None

    contributors = get_contributors(wrap(meta.get("authorships")))
    contributors = get_authors(contributors)

    url = normalize_url(
        dig(meta, "primary_location.landing_page_url") or dig(meta, "id")
    )
    raw_title = meta.get("display_name") or meta.get("title")
    title = sanitize(raw_title) if raw_title else None

    publisher = compact(
        {"name": dig(meta, "primary_location.source.host_organization_name")}
    )
    date_published = dig(meta, "publication_date") or dig(meta, "created_date")

    identifiers = build_identifiers(meta, _id)

    license_ = dig(meta, "best_oa_location.license")
    # "other-oa" is OpenAlex's sentinel for an unspecified open license; drop it.
    if license_ == "other-oa":
        license_ = None
    if license_ is not None:
        license_ = OA_LICENSES.get(license_, license_)
        license_ = dict_to_spdx({"id": license_})

    container = get_container(meta)

    references = []
    for oa_url in meta.get("referenced_works", []):
        oa_id = validate_openalex(oa_url)
        if oa_id:
            references.append({"id": f"https://openalex.org/{oa_id}"})

    funding_references = []
    for grant in wrap(meta.get("grants")):
        funder = grant.get("funder", "")
        funder_name = grant.get("funder_display_name", "")
        if not funder_name:
            continue
        funder_id = normalize_ror(funder) if funder else None
        f = compact({
            "funder_id": funder_id,
            "funder_name": funder_name,
            "award_number": grant.get("award_id") or None,
        })
        funding_references.append(f)
    funding_references = unique(funding_references) or None

    description = get_abstract(meta)
    description = sanitize(description) if description else None

    subjects = []
    primary_topic = meta.get("primary_topic")
    if primary_topic:
        subfield = primary_topic.get("subfield", {})
        subfield_id = subfield.get("id")
        subfield_name = subfield.get("display_name")
        topic_id = primary_topic.get("id")
        topic_name = primary_topic.get("display_name")
        if subfield_id and subfield_name:
            subjects.append({"id": subfield_id, "subject": subfield_name})
        if topic_id and topic_name:
            subjects.append({"id": topic_id, "subject": topic_name})

    files = get_files(meta)

    return {
        # required properties
        "id": _id,
        "type": _type,
        # recommended and optional properties
        "additional_type": additional_type,
        "container": presence(container),
        "contributors": presence(contributors),
        "date_published": date_published,
        "description": description,
        "files": presence(files),
        "funding_references": presence(funding_references),
        "geo_locations": None,
        "identifiers": identifiers or None,
        "language": meta.get("language", None),
        "license": license_,
        "provider": "OpenAlex",
        "publisher": presence(publisher),
        "references": presence(references),
        "subjects": presence(subjects),
        "title": title,
        "url": url,
        "version": meta.get("version", None),
    } | read_options


def build_identifiers(meta: dict, _id: str | None) -> list[dict]:
    """Build identifiers list with canonical DOI + OpenAlex first, then
    deduplicated additional identifiers from the ids map."""
    identifiers: list[dict] = []

    # Canonical DOI from the top-level record id
    if _id and _id.startswith("https://doi.org/"):
        identifiers.append({"identifier": _id, "identifier_type": "DOI"})

    # Canonical OpenAlex ID from the top-level work id
    oa_id = validate_openalex(meta.get("id"))
    if oa_id:
        identifiers.append(
            {"identifier": f"https://openalex.org/{oa_id}", "identifier_type": "OpenAlex"}
        )

    # Additional identifiers from the ids map, in a defined order
    for key in ["openalex", "doi", "pmid", "pmcid"]:
        value = (meta.get("ids") or {}).get(key)
        if not value:
            continue
        id_type = OA_IDENTIFIER_TYPES.get(key)
        if not id_type:
            continue
        normalized = normalize_doi(value) if id_type == "DOI" else value
        if not normalized:
            continue
        if any(
            i["identifier_type"] == id_type and i["identifier"] == normalized
            for i in identifiers
        ):
            continue
        identifiers.append({"identifier": normalized, "identifier_type": id_type})

    return identifiers


def get_abstract(meta: dict) -> str | None:
    """Parse abstract from OpenAlex abstract_inverted_index."""
    abstract_inverted_index = dig(meta, "abstract_inverted_index")
    if not abstract_inverted_index:
        return None

    max_pos = max(
        p for positions in abstract_inverted_index.values() for p in positions
    )
    abstract_words = [""] * (max_pos + 1)
    for word, positions in abstract_inverted_index.items():
        for p in positions:
            abstract_words[p] = word

    return " ".join(w for w in abstract_words if w) or None


def get_contributors(contributors: list) -> list:
    """Parse contributor from OpenAlex authorship dicts."""

    def parse_contributor(c: dict) -> dict:
        affiliations = [
            compact({
                "id": normalize_ror(affiliation.get("ror")),
                "name": affiliation.get("display_name"),
            })
            for affiliation in c.get("institutions", [])
            if affiliation.get("display_name") or affiliation.get("ror")
        ]
        return compact({
            "id": normalize_orcid(dig(c, "author.orcid")),
            "name": dig(c, "author.display_name"),
            "affiliations": affiliations or None,
        })

    return [parse_contributor(i) for i in contributors]


def get_files(meta: dict) -> list | None:
    """get file links"""
    pdf_url = dig(meta, "best_oa_location.pdf_url")
    if pdf_url is None:
        return None
    return [{"mime_type": "application/pdf", "url": pdf_url}]


def get_container(meta: dict) -> dict | None:
    """Get container from OpenAlex"""
    container_type = dig(meta, "primary_location.source.type")
    if container_type:
        container_type = OA_TO_CM_CONTAINER_TRANLATIONS.get(
            container_type, container_type
        )
    issn = dig(meta, "primary_location.source.issn_l")
    container_title = dig(meta, "primary_location.source.display_name")

    return compact(
        {
            "type": container_type,
            "identifier": issn,
            "identifier_type": "ISSN" if issn else None,
            "title": container_title,
            "volume": dig(meta, "biblio.volume"),
            "issue": dig(meta, "biblio.issue"),
            "first_page": dig(meta, "biblio.first_page"),
            "last_page": dig(meta, "biblio.last_page"),
        }
    )


def get_random_openalex_id(number: int = 1, **kwargs) -> list:
    """Get random ID from OpenAlex"""
    number = min(number, 20)
    url = openalex_api_sample_url(number, **kwargs)
    try:
        response = http.get(url, timeout=10)
        if response.status_code != 200:
            return []
        items = dig(response.json(), "results")
        return items
    except (ReadTimeout, ConnectionError):
        return []
