"""OpenAlex reader for commonmeta-py"""

from typing import Optional

import httpx
from pydash import py_

from ..author_utils import get_authors
from ..base_utils import compact, presence, sanitize, wrap
from ..constants import (
    OA_TO_CM_CONTAINER_TRANLATIONS,
    OA_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..doi_utils import (
    doi_as_url,
    openalex_api_sample_url,
    openalex_api_url,
)
from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    normalize_doi,
    normalize_url,
)


def get_openalex(pid: str, **kwargs) -> dict:
    """get_openalex"""
    if pid is None:
        return {"state": "not_found"}
    url = openalex_api_url(pid)
    response = httpx.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json() | {"via": "openalex"}


def read_openalex(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_openalex"""
    if data is None:
        return {"state": "not_found"}
    meta = data
    read_options = kwargs or {}

    doi = meta.get("doi", None)
    _id = doi_as_url(doi)
    _type = OA_TO_CM_TRANSLATIONS.get(meta.get("type", None)) or "Other"

    archive_locations = []
    contributors = get_contributors(wrap(meta.get("authorships")))
    contributors = get_authors(contributors)
    editors = []

    url = normalize_url(
        py_.get(meta, "primary_location.landing_page_url") or py_.get(meta, "id")
    )
    titles = [{"title": sanitize(py_.get(meta, "title"))}]
    publisher = compact(
        {"name": meta.get("primary_location.source.display_name", None)}
    )
    if _type == "Article" and py_.get(publisher, "name") == "Front Matter":
        _type = "BlogPost"
    date = compact(
        {
            "published": py_.get(meta, "publication_date")
            or py_.get(meta, "created_date")
        }
    )
    identifiers = [
        {
            "identifier": pidurl_as_pid(str(uid)),
            "identifierType": uidType.upper(),
        }
        for uidType, uid in (meta.get("ids", {})).items()
    ]

    license_ = meta.get("license", None)  # Returns string E.g. "cc-by"
    if license_ is not None:
        license_ = normalize_cc_url(license_[0].get("URL", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None
        # Need clarification on how the final license should look
    issn = None
    container = get_container(meta)  # Todo
    relations = []
    references = [
        get_related(i) for i in get_references(meta.get("referenced_works", []))[:2]
    ]  # FTODO
    funding_references = from_openalex_funding(wrap(meta.get("grants", None)))

    description = get_abstract(meta)
    if description is not None:
        descriptions = [{"description": sanitize(description), "type": "Abstract"}]
    else:
        descriptions = None

    subjects = py_.uniq(
        [
            {"subject": py_.get(i, "subfield.display_name")}
            for i in wrap(meta.get("topics", None))
        ]
    )

    files = py_.uniq(
        []
    )  # Openalex has urls for openacess article pdfs where available but not any more that I can see
    # Would files be used just for these urls?

    return {
        # required properties
        "id": _id,
        "type": _type,
        # recommended and optional properties
        "additionalType": None,
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


def pidurl_as_pid(pid):
    """Strip url parts from OpenAlex pid"""
    pid = str(pid)
    parts = pid.split("/")
    pid = "/".join(parts[3:]) if len(parts) > 3 else pid
    return pid


def get_abstract(meta):
    """Parse abstract from OpenAlex abstract_inverted_index"""
    abstract_inverted_index = py_.get(meta, "abstract_inverted_index")

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
        abstract = ""


def get_contributors(contributors: list) -> list:
    """Parse contributor"""

    def parse_contributor(c):
        return compact(
            {
                "id": py_.get(c, "author.orcid"),
                "name": py_.get(c, "author.display_name"),
                "affiliations": [
                    {"name": py_.get(c, "affiliations[0].raw_affiliation_string")}
                ],
            }
        )

    return [parse_contributor(i) for i in contributors]


def get_references(pids: list, **kwargs) -> list:
    """Get related articles from OpenAlex using their pid
    \n Used for retrieving metadata for citations and references which are not included in the OpenAlex record
    \n Uses batches of 49 to meet their API limit of 50 pids per request"""
    pid_batches = [pids[i : i + 49] for i in range(0, len(pids), 49)]

    references = []
    for pid_batch in pid_batches:
        ids = "|".join(pid_batch)
        url = f"https://api.openalex.org/works?filter=ids.openalex:{ids}"
        response = httpx.get(url, timeout=10, **kwargs)
        if response.status_code != 200:
            return {"state": "not_found"}
        response = response.json()
        if py_.get(response, "count") == 0:
            return {"state": "not_found"}

        references.extend(response.get("results"))

    return references


def get_citations(citation_url: str, **kwargs) -> list:
    response = httpx.get(citation_url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    response = response.json()
    return response.json().get("results", [])


def get_related(related: Optional[dict]) -> Optional[dict]:
    """Get reference from OpenAlex reference"""
    if related is None or not isinstance(related, dict):
        return None
    doi = related.get("doi", None)
    print(doi)
    metadata = {
        "id": normalize_doi(doi) if doi else None,
        "contributor": related.get("author", None),
        "title": related.get("display_name", None),
        "publisher": related.get(
            "primary_location.source.host_organization_name", None
        ),
        "publicationYear": related.get("publication_year", None),
        "volume": py_.get(related, "biblio.volume"),
        "issue": py_.get(related, "biblio.issue"),
        "firstPage": py_.get(related, "biblio.first_page"),
        "lastPage": py_.get(related, "biblio.last_page"),
        "containerTitle": related.get("primary_location.source.display_name", None),
    }
    return compact(metadata)


def get_file(file: dict) -> dict:
    """Get file from OpenAlex"""
    return compact(
        {
            "url": file.get("URL", None),
            "mimeType": file.get("content-type", None),
        }
    )


def get_container(meta: dict) -> dict:
    """Get container from OpenAlex"""
    container = meta.get("primary_location", {})
    container_source = container.get("source", None)
    container_source = py_.get(meta, "primary_location.source") or {}
    container_type = container_source.get("type", None)
    container_type = OA_TO_CM_CONTAINER_TRANLATIONS.get(container_type, None)
    issn = container_source.get("issn_l", None)
    id = container.get("id", None)
    container_title = container_source.get("display_name", None)
    volume = py_.get(meta, "biblio.volume")
    issue = py_.get(meta, "biblio.issue")
    first_page = py_.get(meta, "biblio.first_page")
    last_page = py_.get(meta, "biblio.last_page")

    # TODO: add support for series, location, missing in Crossref JSON

    return compact(
        {
            "type": container_type,
            "identifier": issn or id,
            "identifierType": "ISSN" if issn else "OpenAlexID",
            "title": container_title,
            "volume": volume,
            "issue": issue,
            "firstPage": first_page,
            "lastPage": last_page,
        }
    )


def from_openalex_funding(funding_references: list) -> list:
    """Get funding references from OpenAlex"""
    formatted_funding_references = []
    for funding in funding_references:
        f = compact(
            {
                "funderName": funding.get("funder_display_name", None),
                "funderIdentifier": pidurl_as_pid(funding["funder"]),
                "funderIdentifierType": "OpenAlex Funder ID",
                "awardNumber": funding.get("award_id", None),
            }
        )
        formatted_funding_references.append(f)
    return py_.uniq(formatted_funding_references)


def get_random_openalex_id(number: int = 1, **kwargs) -> list:
    """Get random DOI from OpenAlex"""
    number = 20 if number > 20 else number
    url = openalex_api_sample_url(number, **kwargs)
    try:
        response = httpx.get(url, timeout=10)
        if response.status_code != 200:
            return []

        items = py_.get(response.json(), "results")
        return [i.get("doi") for i in items]
    except (httpx.ReadTimeout, httpx.ConnectError):
        return []
