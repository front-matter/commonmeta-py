"""OpenAlex reader for commonmeta-py"""

from typing import Optional

import requests
from requests.exceptions import ConnectionError, ReadTimeout

from ..author_utils import get_authors
from ..base_utils import compact, dig, presence, sanitize, unique, wrap
from ..constants import (
    CR_TO_CM_TRANSLATIONS,
    OA_TO_CM_CONTAINER_TRANLATIONS,
    OA_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..doi_utils import (
    normalize_doi,
)
from ..utils import (
    dict_to_spdx,
    normalize_url,
    openalex_api_query_url,
    openalex_api_sample_url,
    openalex_api_url,
    validate_id,
    validate_openalex,
)

# Map OpenAlex license strings to SPDX licenceId. May not be the correct license version.
OA_LICENSES = {"cc-by": "CC-BY-4.0", "cc0": "CC0-1.0"}
OA_IDENTIFIER_TYPES = {
    "openalex": "OpenAlex",
    "doi": "DOI",
    "mag": "MAG",
    "pmid": "PMID",
    "pmcid": "PMCID",
}


def get_openalex_list(query: dict, **kwargs) -> list[dict]:
    """get_openalex list from OpenAlex API."""
    url = openalex_api_query_url(query, **kwargs)
    response = requests.get(url, timeout=30, **kwargs)
    if response.status_code != 200:
        return []
    return response.json().get("results", [])


def get_openalex(pid: str, **kwargs) -> dict:
    """get_openalex"""
    id, identifier_type = validate_id(pid)
    if identifier_type not in ["DOI", "MAG", "OpenAlex", "PMID", "PMCID"]:
        return {"state": "not_found"}
    url = openalex_api_url(id, identifier_type, **kwargs)
    response = requests.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    # OpenAlex returns record as list
    if identifier_type in ["MAG", "PMID", "PMCID"]:
        return dig(response.json(), "results[0]") | {"via": "openalex"}
    return response.json() | {"via": "openalex"}


def read_openalex(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_openalex"""
    if data is None:
        return {"state": "not_found"}
    meta = data
    read_options = kwargs or {}

    _id = meta.get("doi", None) or meta.get("id", None)
    _type = CR_TO_CM_TRANSLATIONS.get(meta.get("type_crossref", None)) or "Other"
    additional_type = OA_TO_CM_TRANSLATIONS.get(meta.get("type", None))
    if additional_type == _type:
        additional_type = None

    archive_locations = []
    contributors = get_contributors(wrap(meta.get("authorships")))
    contributors = get_authors(contributors)

    url = normalize_url(
        dig(meta, "primary_location.landing_page_url") or dig(meta, "id")
    )
    title = meta.get("title", None)
    if title is not None:
        titles = [{"title": sanitize(title)}]
    else:
        titles = None
    publisher = compact(
        {"name": dig(meta, "primary_location.source.host_organization_name")}
    )
    date = compact(
        {"published": dig(meta, "publication_date") or dig(meta, "created_date")}
    )
    identifiers = [
        {
            "identifier": uid,
            "identifierType": OA_IDENTIFIER_TYPES[uidType],
        }
        for uidType, uid in (meta.get("ids", {})).items()
    ]

    license_ = dig(meta, "best_oa_location.license")
    if license_ is not None:
        license_ = OA_LICENSES.get(license_, license_)
        license_ = dict_to_spdx({"id": license_})
    container = get_container(meta)
    relations = []
    references = [
        get_related(i) for i in get_references(meta.get("referenced_works", []))
    ]
    funding_references = from_openalex_funding(wrap(meta.get("grants", None)))

    description = get_abstract(meta)
    if description is not None:
        descriptions = [{"description": sanitize(description), "type": "Abstract"}]
    else:
        descriptions = None

    subjects = unique(
        [
            {"subject": dig(i, "subfield.display_name")}
            for i in wrap(meta.get("topics", None))
        ]
    )
    files = get_files(meta)

    return {
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
        "provider": "OpenAlex",
        "publisher": presence(publisher),
        "references": presence(references),
        "relations": presence(relations),
        "subjects": presence(subjects),
        "titles": presence(titles),
        "url": url,
        "version": meta.get("version", None),
    } | read_options


def get_abstract(meta):
    """Parse abstract from OpenAlex abstract_inverted_index"""
    abstract_inverted_index = dig(meta, "abstract_inverted_index")

    if abstract_inverted_index:
        # Determine the length of the abstract
        max_pos = max(
            p for positions in abstract_inverted_index.values() for p in positions
        )
        abstract_words = [""] * (max_pos + 1)

        for word, positions in abstract_inverted_index.items():
            for p in positions:
                abstract_words[p] = word

        abstract = " ".join(abstract_words)
    else:
        abstract = None
    return abstract


def get_contributors(contributors: list) -> list:
    """Parse contributor"""

    def parse_contributor(c):
        affiliations = []
        for affiliation in c.get("institutions", []):
            affiliations.append(
                compact(
                    {
                        "id": affiliation.get("ror", None),
                        "name": affiliation.get("display_name", None),
                    }
                )
            )

        return compact(
            {
                "id": dig(c, "author.orcid"),
                "name": dig(c, "author.display_name"),
                "affiliations": affiliations,
            }
        )

    return [parse_contributor(i) for i in contributors]


def get_references(pids: list, **kwargs) -> list:
    """Get related articles from OpenAlex using their pid
    Used for retrieving metadata for citations and references which are not included in the OpenAlex record
    """
    references = get_openalex_works(pids)
    return references


def get_citations(citation_url: str, **kwargs) -> list:
    response = requests.get(citation_url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    response = response.json()
    return response.json().get("results", [])


def get_related(related: Optional[dict]) -> Optional[dict]:
    """Get reference from OpenAlex reference"""
    if related is None or not isinstance(related, dict):
        return None
    doi = related.get("doi", None)
    metadata = {
        "id": normalize_doi(doi) if doi else None,
        "contributor": related.get("author", None),
        "title": related.get("display_name", None),
        "publisher": related.get(
            "primary_location.source.host_organization_name", None
        ),
        "publicationYear": related.get("publication_year", None),
        "volume": dig(related, "biblio.volume"),
        "issue": dig(related, "biblio.issue"),
        "firstPage": dig(related, "biblio.first_page"),
        "lastPage": dig(related, "biblio.last_page"),
        "containerTitle": related.get("primary_location.source.display_name", None),
    }
    return compact(metadata)


def get_openalex_works(pids: list, **kwargs) -> list:
    """Get OpenAlex works, use batches of 49 to honor API limit."""
    pid_batches = [pids[i : i + 49] for i in range(0, len(pids), 49)]
    works = []
    for pid_batch in pid_batches:
        ids = "|".join(pid_batch)
        url = f"https://api.openalex.org/works?filter=ids.openalex:{ids}"
        response = requests.get(url, timeout=10, **kwargs)
        if response.status_code != 200:
            return {"state": "not_found"}
        response = response.json()
        if dig(response, "count") == 0:
            return {"state": "not_found"}

        works.extend(response.get("results"))

    return works


def get_openalex_funders(pids: list, **kwargs) -> list:
    """Get ROR id and name from OpenAlex funders.
    use batches of 49 to honor API limit."""
    pid_batches = [pids[i : i + 49] for i in range(0, len(pids), 49)]
    funders = []
    for pid_batch in pid_batches:
        ids = "|".join(pid_batch)
        url = f"https://api.openalex.org/funders?filter=ids.openalex:{ids}"
        response = requests.get(url, timeout=10, **kwargs)
        if response.status_code != 200:
            return {"state": "not_found"}
        response = response.json()
        if dig(response, "count") == 0:
            return {"state": "not_found"}

        def format_funder(funder):
            return compact(
                {
                    "id": dig(funder, "id"),
                    "ror": dig(funder, "ids.ror"),
                    "name": dig(funder, "display_name"),
                }
            )

        f = [format_funder(i) for i in response.get("results")]
        funders.extend(f)

    return funders


def get_openalex_source(str: Optional[str], **kwargs) -> Optional[dict]:
    """Get issn, name, homepage_url and type from OpenAlex source."""
    id = validate_openalex(str)
    if not id:
        return None

    url = f"https://api.openalex.org/sources/{id}"
    response = requests.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    response = response.json()
    if dig(response, "count") == 0:
        return {"state": "not_found"}

    return compact(
        {
            "id": dig(response, "id"),
            "url": dig(response, "homepage_url"),
            "issn": dig(response, "issn_l"),
            "title": dig(response, "display_name"),
            "type": dig(response, "type"),
        }
    )


def get_files(meta) -> Optional[list]:
    """get file links"""
    pdf_url = dig(meta, "best_oa_location.pdf_url")
    if pdf_url is None:
        return None
    return [
        {"mimeType": "application/pdf", "url": pdf_url},
    ]


def get_container(meta: dict) -> dict:
    """Get container from OpenAlex"""
    source = get_openalex_source(dig(meta, "primary_location.source.id"))
    container_type = dig(source, "type")
    if container_type:
        container_type = OA_TO_CM_CONTAINER_TRANLATIONS.get(
            container_type, container_type
        )
    issn = dig(source, "issn")
    container_title = dig(source, "title")
    url_ = dig(source, "url")

    return compact(
        {
            "type": container_type,
            "identifier": issn or url_,
            "identifierType": "ISSN" if issn else "URL" if url_ else None,
            "title": container_title,
            "volume": dig(meta, "biblio.volume"),
            "issue": dig(meta, "biblio.issue"),
            "firstPage": dig(meta, "biblio.first_page"),
            "lastPage": dig(meta, "biblio.last_page"),
        }
    )


def from_openalex_funding(funding_references: list) -> list:
    """Get funding references from OpenAlex"""
    funder_ids = [
        validate_openalex(funding.get("funder"))
        for funding in funding_references
        if "funder" in funding
    ]
    funders = get_openalex_funders(funder_ids)
    formatted_funding_references = []
    for funding in funding_references:
        funder = next(
            item for item in funders if item["id"] == funding.get("funder", None)
        )
        f = compact(
            {
                "funderName": funder.get("name", None),
                "funderIdentifier": funder.get("ror", None),
                "funderIdentifierType": "ROR" if funder.get("ror", None) else None,
                "awardNumber": funding.get("award_id", None),
            }
        )
        formatted_funding_references.append(f)
    return unique(formatted_funding_references)


def get_random_openalex_id(number: int = 1, **kwargs) -> list:
    """Get random ID from OpenAlex"""
    number = min(number, 20)
    url = openalex_api_sample_url(number, **kwargs)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []

        items = dig(response.json(), "results")
        return items
    except (ReadTimeout, ConnectionError):
        return []
