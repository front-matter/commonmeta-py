"""OpenAlex writer for commonmeta-py

A commonmeta work as an OpenAlex work, in the shape the OpenAlex API gives it,
as commonmeta-rs writes it (formats/openalex_work.rs).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..base_utils import wrap
from ..constants import (
    CM_TO_OA_CONTAINER_TRANSLATIONS,
    CM_TO_OA_TRANSLATIONS,
    SPDX_TO_OA_LICENSES,
)
from ..doi_utils import normalize_doi
from ..utils import validate_openalex

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


def _text(value: Any) -> str | None:
    """A string, or None (null) where it is empty."""
    return value if isinstance(value, str) and value else None


def _identifier(metadata: Metadata, kind: str) -> str | None:
    """The work's identifier of `kind` (OpenAlex, PMID, ...), if it has one."""
    for i in wrap(metadata.identifiers):
        if (
            isinstance(i, dict)
            and str(i.get("identifier_type", "")).lower() == kind.lower()
            and i.get("identifier")
        ):
            return i["identifier"]
    return None


def _last_segment(value: str) -> str:
    return value.rstrip("/").rsplit("/", 1)[-1]


def inverted_index(text: str) -> dict[str, list[int]]:
    """An abstract as OpenAlex keeps it: each word with the positions it has."""
    index: dict[str, list[int]] = {}
    for position, word in enumerate(text.split()):
        index.setdefault(word, []).append(position)
    return index


def _contributor_name(contributor: dict) -> str:
    person = contributor.get("person")
    if isinstance(person, dict):
        given = person.get("given_name") or ""
        family = person.get("family_name") or ""
        if not given and not family:
            return person.get("name") or ""
        return f"{given} {family}".strip()
    organization = contributor.get("organization")
    if isinstance(organization, dict):
        return organization.get("name") or ""
    return ""


def _affiliations(contributor: dict) -> list[dict]:
    person = contributor.get("person")
    if not isinstance(person, dict):
        return []
    return [a for a in wrap(person.get("affiliations")) if isinstance(a, dict)]


def _authorships(metadata: Metadata) -> list[dict]:
    contributors = [c for c in wrap(metadata.contributors) if isinstance(c, dict)]
    last = max(len(contributors) - 1, 0)
    authorships = []
    for i, contributor in enumerate(contributors):
        name = _contributor_name(contributor)
        person = contributor.get("person")
        orcid = person.get("id") if isinstance(person, dict) else None
        affiliations = _affiliations(contributor)
        institutions = []
        for a in affiliations:
            identifier = a.get("identifier") or ""
            is_ror = str(a.get("identifier_type", "")).upper() == "ROR" or (
                identifier.startswith("https://ror.org/")
            )
            institutions.append(
                {
                    "display_name": _text(a.get("name")),
                    "ror": _text(identifier) if is_ror else None,
                }
            )
        if i == 0:
            position = "first"
        elif i == last:
            position = "last"
        else:
            position = "middle"
        authorships.append(
            {
                "author_position": position,
                "author": {"display_name": _text(name), "orcid": _text(orcid)},
                "institutions": institutions,
                "raw_author_name": _text(name),
                "raw_affiliation_strings": [
                    a["name"] for a in affiliations if a.get("name")
                ],
            }
        )
    return authorships


def _funding(metadata: Metadata) -> tuple[list[dict], list[dict]]:
    """Funders by ROR where one is known, each once; awards with a number."""
    references = [f for f in wrap(metadata.funding_references) if isinstance(f, dict)]
    funders: list[dict] = []
    seen: set[str] = set()
    for f in references:
        name = f.get("funder_name") or ""
        if not name or name in seen:
            continue
        seen.add(name)
        funder_id = f.get("funder_id") or ""
        funders.append(
            {
                "display_name": name,
                "ror": funder_id if funder_id.startswith("https://ror.org/") else None,
            }
        )
    awards = [
        {
            "funder_award_id": f["award_number"],
            "display_name": _text(f.get("award_title")),
            "funder_display_name": _text(f.get("funder_name")),
        }
        for f in references
        if f.get("award_number")
    ]
    return funders, awards


def _topics(metadata: Metadata) -> tuple[list[dict], dict | None]:
    """Topics, and the first with the subfield, from the subjects the reader
    made of them."""
    subjects = [s for s in wrap(metadata.subjects) if isinstance(s, dict)]
    topics = [
        {"id": s["id"], "display_name": s.get("subject")}
        for s in subjects
        if (s.get("id") or "").startswith("https://openalex.org/T")
    ]
    subfield = next(
        (
            {"id": s["id"], "display_name": s.get("subject")}
            for s in subjects
            if (s.get("id") or "").startswith("https://openalex.org/subfields/")
        ),
        None,
    )
    primary_topic = None
    if topics:
        primary_topic = dict(topics[0])
        if subfield is not None:
            primary_topic["subfield"] = subfield
    return topics, primary_topic


def write_openalex(metadata: Metadata | None, **kwargs) -> dict | None:
    """Write a commonmeta work as an OpenAlex work.

    A person or organization has no OpenAlex work to be written as.
    """
    if metadata is None or getattr(metadata, "entity_type", "work") != "work":
        return None

    openalex_id = validate_openalex(_identifier(metadata, "OpenAlex"))
    openalex = f"https://openalex.org/{openalex_id}" if openalex_id else None
    work_id = metadata.id or ""
    if work_id.startswith("https://doi.org/"):
        doi = work_id
    else:
        doi_identifier = _identifier(metadata, "DOI")
        doi = normalize_doi(doi_identifier) if doi_identifier else None
    pmid = _identifier(metadata, "PMID")
    pmcid = _identifier(metadata, "PMCID")
    ids = {
        key: value
        for key, value in (
            ("openalex", openalex),
            ("doi", doi),
            (
                "pmid",
                f"https://pubmed.ncbi.nlm.nih.gov/{_last_segment(pmid)}"
                if pmid
                else None,
            ),
            (
                "pmcid",
                f"https://www.ncbi.nlm.nih.gov/pmc/articles/{_last_segment(pmcid)}"
                if pmcid
                else None,
            ),
        )
        if value
    }

    pdf_url = next(
        (
            f["url"]
            for f in wrap(metadata.files)
            if isinstance(f, dict)
            and f.get("mime_type") == "application/pdf"
            and f.get("url")
        ),
        None,
    )
    license_id = (metadata.license or {}).get("id") or ""
    license_ = SPDX_TO_OA_LICENSES.get(license_id.upper())
    container = metadata.container or {}
    publisher = metadata.publisher or {}
    issns = [
        i["identifier"]
        for i in wrap(container.get("identifiers"))
        if isinstance(i, dict)
        and str(i.get("identifier_type", "")).upper() == "ISSN"
        and i.get("identifier")
    ]
    source = None
    if container.get("title"):
        source = {
            "display_name": container["title"],
            "issn_l": issns[0] if issns else None,
            "issn": issns or None,
            "type": CM_TO_OA_CONTAINER_TRANSLATIONS.get(container.get("type"), "other"),
            "host_organization_name": _text(publisher.get("name")),
        }
    primary_location = {
        "landing_page_url": _text(metadata.url),
        "pdf_url": pdf_url,
        "source": source,
        "license": license_,
    }
    best_oa_location = None
    if pdf_url or license_:
        best_oa_location = {
            "landing_page_url": _text(metadata.url),
            "pdf_url": pdf_url,
            "license": license_,
        }

    topics, primary_topic = _topics(metadata)
    funders, awards = _funding(metadata)
    date_published = metadata.date_published or ""
    year = int(date_published[:4]) if date_published[:4].isdigit() else None
    referenced_works = [
        f"https://openalex.org/{oa_id}"
        for r in wrap(metadata.references)
        if isinstance(r, dict) and (oa_id := validate_openalex(r.get("id")))
    ]

    return {
        "id": openalex,
        "doi": doi,
        "title": _text(metadata.title),
        "display_name": _text(metadata.title),
        "publication_year": year,
        "publication_date": _text(date_published),
        "ids": ids,
        "language": _text(metadata.language),
        "type": CM_TO_OA_TRANSLATIONS.get(metadata.type, "other"),
        "primary_location": primary_location,
        "best_oa_location": best_oa_location,
        "authorships": _authorships(metadata),
        "biblio": {
            "volume": _text(container.get("volume")),
            "issue": _text(container.get("issue")),
            "first_page": _text(container.get("first_page")),
            "last_page": _text(container.get("last_page")),
        },
        "primary_topic": primary_topic,
        "topics": topics,
        "awards": awards,
        "funders": funders,
        "referenced_works": referenced_works,
        "abstract_inverted_index": (
            inverted_index(metadata.description) if metadata.description else None
        ),
    }


def write_openalex_list(metalist: MetadataList | None) -> list | None:
    """Write commonmeta works as a JSON array of OpenAlex works. A person or
    organization in the list (an ORCID record before its works) is left out."""
    if metalist is None:
        return None
    works = (write_openalex(item) for item in metalist.items)
    return [work for work in works if work is not None]
