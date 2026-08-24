"""InvenioRDM writer for commonmeta-py"""

from __future__ import annotations

import atexit
import logging
from base64 import b64encode
from contextlib import contextmanager
from datetime import date as date_type
from datetime import datetime
from functools import lru_cache
from html import escape
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

import orjson as json
from babel.core import UnknownLocaleError
from babel.dates import format_date
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from commonmeta.readers.inveniordm_reader import search_by_doi, search_by_guid

from ..api_utils import http
from ..base_utils import (
    compact,
    dig,
    first,
    presence,
    scrub,
    unique,
    wrap,
)
from ..constants import (
    CM_TO_INVENIORDM_CONTRIBUTOR_ROLES,
    CM_TO_INVENIORDM_TRANSLATIONS,
    COMMUNITY_TRANSLATIONS,
    INVENIORDM_IDENTIFIER_TYPES,
    OPENALEX_TOPIC_SUBFIELD_MAPPINGS,
)
from ..date_utils import get_iso8601_date
from ..doi_utils import doi_from_url, is_rogue_scholar_doi, normalize_doi
from ..inveniordm_service import active_backend, system_process
from ..utils import (
    FOS_MAPPINGS,
    OPENALEX_TO_FOS_MAPPINGS,
    get_identifier,
    get_language,
    id_from_url,
    normalize_url,
    pages_as_string,
    string_to_slug,
    validate_orcid,
    validate_ror,
)

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList

log = logging.getLogger(__name__)

# The fields `write_inveniordm` owns. A record may carry further fields written by
# another pipeline; those are left alone and ignored when comparing records.
INVENIORDM_METADATA_FIELDS = frozenset(
    {
        "resource_type",
        "creators",
        "contributors",
        "title",
        "publisher",
        "publication_date",
        "dates",
        "subjects",
        "description",
        "rights",
        "languages",
        "identifiers",
        "references",
        "related_identifiers",
        "funding",
        "version",
    }
)
INVENIORDM_CUSTOM_FIELDS = frozenset(
    {
        "journal:journal",
        "rs:doi",
        "rs:content_html",
        "rs:image",
        "rs:generator",
        "pidbox:citations",
    }
)

# Stylesheet and fonts for the pdf rendition, shipped with the package.
PDF_RESOURCES = Path(__file__).parent.parent / "resources" / "pdf"

# The variant rogue-scholar-api deposited: archival, and tagged, so the pdf
# carries the structure tree a screen reader and a reflowing viewer need.
# WeasyPrint only knows the accessible ("a") conformance levels since 67, hence
# the >=69 floor in pyproject.toml.
PDF_VARIANT = "pdf/a-3a"

# Front matter headings, in the languages rogue-scholar-api translated them to.
PDF_TITLES = {
    "published": {
        "en": "Published",
        "de": "Veröffentlicht",
        "es": "Publicado",
        "fr": "Publié",
        "it": "Pubblicato",
        "pt": "Publicados",
    },
    "abstract": {
        "en": "Abstract",
        "de": "Zusammenfassung",
        "es": "Resumen",
        "fr": "Résumé",
        "it": "Riassunto",
        "pt": "Resumo",
    },
    "copyright": {
        "en": "Copyright",
        "de": "Urheberrecht",
        "es": "Copyright",
        "fr": "Droit d'auteur",
        "it": "Copyright",
        "pt": "Direitos de autor",
    },
    # the alt description an image gets when the post gives it none
    "image": {
        "en": "Image",
        "de": "Bild",
        "es": "Imagen",
        "fr": "Image",
        "it": "Immagine",
        "pt": "Imagem",
    },
}


def write_inveniordm(metadata: Metadata, write_pdf: bool = False, **kwargs) -> dict:
    """Write inveniordm.

    ``write_pdf`` deposits a pdf rendition of the post as a record file, which
    means the record is created with files enabled. It is ignored for records
    with no content: ``rs:content_html`` is what the pdf is rendered from, and
    InvenioRDM refuses to publish a record that has files enabled but none
    uploaded ("Missing uploaded files"), so enabling files for a record that
    cannot produce one would fail the publish.
    """
    if metadata is None or metadata.write_errors is not None:
        return {}
    if is_rogue_scholar_doi(metadata.id, ra="crossref"):
        pids = {
            "doi": {
                "identifier": doi_from_url(metadata.id),
                "provider": "crossref",
            },
        }
    # elif is_rogue_scholar_doi(metadata.id, ra="datacite"):
    #     # DataCite DOIs should not be provided in the InvenioRDM writer
    #     pids = None
    else:
        pids = {
            "doi": {"identifier": doi_from_url(metadata.id), "provider": "external"},
        }
    _type = CM_TO_INVENIORDM_TRANSLATIONS.get(metadata.type, "Other")
    creators = [
        to_inveniordm_creator(i)
        for i in wrap(metadata.contributors)
        if "Author" in wrap(i.get("roles", None))
    ]
    contributors = scrub(
        [
            to_inveniordm_contributor(i)
            for i in wrap(metadata.contributors)
            if "Author" not in wrap(i.get("roles", None))
        ]
    )
    identifiers = [
        {
            "identifier": i.get("identifier", None),
            "scheme": INVENIORDM_IDENTIFIER_TYPES.get(
                i.get("identifier_type", None), "other"
            ),
        }
        for i in wrap(metadata.identifiers)
        if i.get("identifier_type", None) != "DOI"
    ]
    identifiers.append(
        {
            "identifier": metadata.url,
            "scheme": "url",
        }
    )
    references = [to_inveniordm_reference(i) for i in wrap(metadata.references)]
    # IsReferencedBy relations are citing works: their home is
    # custom_fields.pidbox:citations, not related_identifiers (mirrors the
    # reader, which also still accepts the legacy rs:citations name).
    related_identifiers = [
        to_inveniordm_related_identifier(i)
        for i in wrap(metadata.relations)
        if i.get("id", None)
        and i.get("type", None) not in ("IsPartOf", "IsReferencedBy")
    ]
    citations = [
        c
        for c in (
            to_inveniordm_citation(i)
            for i in wrap(metadata.relations)
            if i.get("type", None) == "IsReferencedBy"
        )
        if c is not None
    ]
    funding = unique(
        [
            to_inveniordm_funding(i)
            for i in wrap(metadata.funding_references)
            if i.get("funder_name", None)
        ]
    )
    container = metadata.container if metadata.container else {}
    journal_title = (
        container.get("title", None)
        if _type not in ["inbook", "inproceedings"]
        and container.get("type") in ["Journal", "Periodical", "Blog"]
        else None
    )
    issn = get_identifier(container, "ISSN")
    # A journal identified by a DOI (rather than an ISSN)
    journal_doi = get_identifier(container, "DOI")
    volume = container.get("volume", None)
    issue = container.get("issue", None)
    pages = pages_as_string(container)

    date_fields = compact(
        {
            "published": metadata.date_published,
            "updated": metadata.date_updated,
            **(metadata.dates or {}),
        }
    )
    dates = []
    for d, v in date_fields.items():
        t = d.lower()
        if t == "published":
            t = "issued"
        elif t == "accessed":
            t = "other"
        dates.append({"date": v, "type": {"id": t}})

    # Flatten subjects list since to_inveniordm_subject can return multiple subjects
    # Deduplicate by ID to handle multiple subfields mapping to same FOS
    all_subjects = [
        s for i in wrap(metadata.subjects) for s in (to_inveniordm_subject(i) or [])
    ]
    seen_ids = set()
    subjects = []
    for subject in all_subjects:
        subject_id = subject.get("id")
        if subject_id is None or subject_id not in seen_ids:
            subjects.append(subject)
            if subject_id is not None:
                seen_ids.add(subject_id)

    # files = to_files(metadata)

    # Only enable files when a pdf will actually be produced. metadata.content
    # is what becomes rs:content_html below, and the pdf is rendered from it;
    # enabling files for a record that cannot produce one fails the publish.
    files_enabled = bool(write_pdf and presence(metadata.content))

    return compact(
        {
            "pids": pids,
            "access": {"record": "public", "files": "public"},
            "files": {"enabled": files_enabled},
            "metadata": compact(
                {
                    "resource_type": {"id": _type},
                    "creators": creators,
                    "contributors": presence(contributors),
                    "title": metadata.title,
                    "publisher": (
                        metadata.publisher.get("name", None)
                        if metadata.publisher
                        else None
                    ),
                    "publication_date": (
                        get_iso8601_date(metadata.date_published)
                        if metadata.date_published
                        else None
                    ),
                    "dates": presence(dates),
                    "subjects": presence(subjects),
                    "description": metadata.description,
                    "rights": (
                        [{"id": metadata.license.get("id").lower()}]
                        if metadata.license and metadata.license.get("id", None)
                        else None
                    ),
                    "languages": (
                        [{"id": get_language(metadata.language, format="alpha_3")}]
                        if metadata.language
                        else None
                    ),
                    "identifiers": identifiers,
                    "references": presence(references),
                    "related_identifiers": presence(related_identifiers),
                    "funding": presence(funding),
                    "version": metadata.version,
                }
            ),
            "custom_fields": compact(
                {
                    "journal:journal": compact(
                        {
                            "title": journal_title,
                            "issn": issn,
                            "volume": volume,
                            "issue": issue,
                            "pages": pages,
                        }
                    ),
                    "rs:doi": journal_doi,
                    "rs:content_html": presence(metadata.content),
                    "rs:image": presence(metadata.image),
                    # rs:generator is a record VocabularyCF ({"id": <platform>});
                    # feed:generator is a *community* field and invalid on a record.
                    "rs:generator": (
                        {"id": container.get("platform")}
                        if container.get("platform")
                        else None
                    ),
                    "pidbox:citations": presence(citations),
                }
            ),
        }
    )


def to_inveniordm_identifiers(_id: str | None) -> list | None:
    """Format a v1.0 person.id (ORCID) as InvenioRDM identifiers"""
    identifier = validate_orcid(_id)
    if identifier:
        return [
            {
                "identifier": identifier,
                "scheme": "orcid",
            }
        ]
    return None


def to_inveniordm_creator(creator: dict) -> dict:
    """Convert a v1.0 {type, person|organization, roles} contributor to an
    InvenioRDM creator"""
    _type = creator.get("type", None)
    organization = creator.get("organization", None)
    person = creator.get("person", None) or {}
    given_name = person.get("given_name", None)
    family_name = person.get("family_name", None)
    if family_name:
        name = ", ".join([family_name, given_name or ""])
    elif organization:
        name = organization.get("name", None)
    else:
        name = None
    _id = organization.get("id", None) if organization else person.get("id", None)

    return compact(
        {
            "person_or_org": compact(
                {
                    "name": name,
                    "given_name": given_name,
                    "family_name": family_name,
                    "type": _type.lower() + "al" if _type else None,
                    "identifiers": to_inveniordm_identifiers(_id),
                }
            ),
            "affiliations": to_inveniordm_affiliations(person),
        }
    )


def to_inveniordm_contributor(contributor: dict) -> dict:
    """Convert a v1.0 {type, person|organization, roles} contributor to an
    InvenioRDM contributor"""
    _type = contributor.get("type", None)
    organization = contributor.get("organization", None)
    person = contributor.get("person", None) or {}
    given_name = person.get("given_name", None)
    family_name = person.get("family_name", None)
    if family_name:
        name = ", ".join([family_name, given_name or ""])
    elif organization:
        name = organization.get("name", None)
    else:
        name = None
    _id = organization.get("id", None) if organization else person.get("id", None)

    role = first(wrap(contributor.get("roles", None)))
    _role = (
        {"id": CM_TO_INVENIORDM_CONTRIBUTOR_ROLES.get(role)}
        if CM_TO_INVENIORDM_CONTRIBUTOR_ROLES.get(role)
        else None
    )
    if _role is None:
        return None
    return compact(
        {
            "person_or_org": compact(
                {
                    "name": name,
                    "given_name": given_name,
                    "family_name": family_name,
                    "type": _type.lower() + "al" if _type else None,
                    "identifiers": to_inveniordm_identifiers(_id),
                }
            ),
            "role": _role,
            "affiliations": to_inveniordm_affiliations(person),
        }
    )


def to_inveniordm_subject(sub: dict) -> list | None:
    """Convert subject to inveniordm subject. Adds scheme based on id pattern.
    For subfields, also returns a FOS subject if a mapping exists."""
    if sub.get("subject", None) is None:
        return None

    if sub.get("id", "").startswith("https://openalex.org/domains/"):
        scheme = "Domains"
    elif sub.get("id", "").startswith("https://openalex.org/fields/"):
        scheme = "Fields"
    elif sub.get("id", "").startswith("https://openalex.org/subfields/"):
        scheme = "Subfields"
    elif sub.get("id", "").startswith("https://openalex.org/T"):
        scheme = "Topics"
    elif sub.get("id", "").startswith("http://www.oecd.org/science/inno/38235147.pdf"):
        scheme = "FOS"
    else:
        scheme = None

    result = [
        compact(
            {
                "id": sub.get("id", None),
                "subject": sub.get("subject"),
                "scheme": scheme,
            }
        )
    ]

    # If this is a subfield, also add a FOS subject if mapping exists
    if sub.get("id", "").startswith("https://openalex.org/subfields/"):
        # Extract subfield ID (last part of URL)
        subfield_id = sub.get("id", "").split("/")[-1]
        fos_name = OPENALEX_TO_FOS_MAPPINGS.get(subfield_id, None)
        if fos_name:
            fos_id = FOS_MAPPINGS.get(fos_name, None)
            existing_ids = {
                s.get("id")
                for s in result
                if isinstance(s, dict) and s.get("id") is not None
            }
            if fos_id and fos_id not in existing_ids:
                result.append(
                    compact(
                        {
                            "id": fos_id,
                            "subject": f"FOS: {fos_name}",
                            "scheme": "FOS",
                        }
                    )
                )

    return result


def to_inveniordm_affiliations(person: dict) -> list | None:
    """Convert a v1.0 person's affiliations to inveniordm affiliations."""

    def format_affiliation(affiliation):
        # affiliation identifiers are ROR-only in v1.0; emit the InvenioRDM
        # affiliation id only for ROR-typed identifiers.
        ror = (
            affiliation.get("identifier", None)
            if affiliation.get("identifier_type", None) == "ROR"
            else None
        )
        return compact(
            {
                "id": id_from_url(ror),
                "name": affiliation.get("name", None),
            }
        )

    return scrub(
        [format_affiliation(i) for i in wrap(person.get("affiliations", None))]
    )


def to_inveniordm_related_identifier(relation: dict) -> dict | None:
    """Convert relation to inveniordm related_identifier"""
    if normalize_doi(relation.get("id", None)):
        identifier = doi_from_url(relation.get("id", None))
        scheme = "doi"
    elif normalize_url(relation.get("id", None)):
        identifier = relation.get("id", None)
        scheme = "url"
    else:
        return None

    # normalize relation types
    if relation.get("type", None) == "HasReview":
        relation_type = "isreviewedby"
    elif relation.get("type", None) == "IsPreprintOf":
        relation_type = "ispreviousversionof"
    elif relation.get("type", None) is not None:
        relation_type = str(relation.get("type")).lower()
    else:
        return None

    return compact(
        {
            "identifier": identifier,
            "scheme": scheme,
            "relation_type": {"id": relation_type},
        }
    )


def to_inveniordm_citation(relation: dict) -> dict | None:
    """Convert an IsReferencedBy relation to a custom_fields.pidbox:citations
    entry (the inverse of the reader's ``get_citations``)."""
    if normalize_doi(relation.get("id", None)):
        return {"identifier": doi_from_url(relation.get("id", None)), "scheme": "doi"}
    if normalize_url(relation.get("id", None)):
        return {"identifier": relation.get("id", None), "scheme": "url"}
    return None


def to_inveniordm_reference(reference: dict) -> dict | None:
    """Convert reference to inveniordm reference"""
    if normalize_doi(reference.get("id", None)):
        identifier = doi_from_url(reference.get("id", None))
        scheme = "doi"
    elif normalize_url(reference.get("id", None)):
        identifier = reference.get("id", None)
        scheme = "url"
    else:
        identifier = None
        scheme = None

    # the commonmeta `reference` field holds the formatted reference string
    # (falling back to the legacy unstructured/title fields).
    unstructured = reference.get("reference", None) or reference.get(
        "unstructured", None
    )
    if unstructured:
        if reference.get("id", None):
            # remove duplicate ID from unstructured reference
            unstructured = unstructured.replace(reference.get("id"), "")
        # remove optional trailing whitespace
        unstructured = unstructured.rstrip()
    else:
        title = reference.get("title", None)
        unstructured = str(title) if title else "Unknown title"
        if reference.get("publication_year", None):
            unstructured += f" ({reference.get('publication_year')})."

    return compact(
        {
            "reference": unstructured,
            "scheme": scheme,
            "identifier": identifier,
        }
    )


def to_inveniordm_funding(funding: dict) -> dict | None:
    """Convert a v1.0 flat funding reference (ROR-only funder_id) to
    inveniordm funding"""
    funder_identifier = validate_ror(funding.get("funder_id", None))
    award_number = funding.get("award_number", None)
    award_title = funding.get("award_title", None)
    if award_title:
        award_title = {"en": award_title}
    if funding.get("award_id", None):
        award_identifier = funding.get("award_id", None)
        scheme = "doi" if normalize_doi(award_identifier) else "url"
        if scheme == "doi":
            award_identifier = doi_from_url(award_identifier)
        award_identifiers = [
            {
                "scheme": scheme,
                "identifier": award_identifier,
            },
        ]
    else:
        award_identifiers = None

    if award_number or award_title or award_identifiers:
        return compact(
            {
                "funder": compact(
                    {
                        "name": funding.get("funder_name"),
                        "id": funder_identifier,
                    }
                ),
                "award": compact(
                    {
                        "number": award_number,
                        "title": award_title,
                        "identifiers": award_identifiers,
                    }
                ),
            }
        )

    return compact(
        {
            "funder": compact(
                {
                    "name": funding.get("funder_name"),
                    "id": funder_identifier,
                }
            ),
        }
    )


def to_files(metadata: Metadata) -> list:
    """Convert metadata files to inveniordm files"""

    def format_file(file):
        return compact(
            {
                "key": file.get("key", None),
                "bucket": file.get("bucket", None),
                "size": file.get("size", None),
                "checksum": file.get("checksum", None),
                "checksum_algorithm": file.get("checksumAlgorithm", None),
                "filename": file.get("filename", None),
                "description": file.get("description", None),
            }
        )

    return [format_file(i) for i in wrap(metadata.files)]


def write_inveniordm_list(
    metalist: MetadataList, write_pdf: bool = False, **kwargs
) -> list | None:
    """Write InvenioRDM list"""

    if metalist is None:
        return None

    def write_item(item) -> dict | None:
        """write inveniordm item for inveniordm list"""

        return write_inveniordm(item, write_pdf=write_pdf)

    return [write_item(item) for item in metalist.items]


def to_pdf_author(contributor: dict) -> str | None:
    """Format a contributor for the pdf byline, given name first"""
    person = contributor.get("person", None) or {}
    name = " ".join(
        n
        for n in (person.get("given_name", None), person.get("family_name", None))
        if n
    )
    return name or (contributor.get("organization", None) or {}).get("name", None)


def to_pdf_date(date: str | None, language: str) -> str | None:
    """Format a publication date the way a reader writes it, in its language.

    Falls back to the iso date for anything babel cannot make a long date of,
    a partial date such as "2024-10" among them.
    """
    if not date:
        return None
    iso = get_iso8601_date(date)
    try:
        return format_date(date_type.fromisoformat(iso), format="long", locale=language)
    except (ValueError, TypeError, UnknownLocaleError) as error:
        log.warning(f"Cannot format date {date} for the pdf: {error}")
        return iso


def to_pdf_rights(metadata: Metadata, authors: list, language: str) -> str | None:
    """Format the copyright line and the terms the post is available under.

    Mirrors the rogue-scholar-api pdf template: a copyright holder and year for
    everything except CC0, which waives copyright rather than asserting it,
    followed by what the licence permits.
    """
    url = (metadata.license or {}).get("url", None)
    identifier = (metadata.license or {}).get("id", None)
    if not url and not identifier:
        return None

    link = f'<a href="{escape(url)}">' if url else "<span>"
    close = "</a>" if url else "</span>"
    if (identifier or "").lower().startswith("cc0"):
        return (
            "This is an open access article, free of all copyright, and may be "
            "freely reproduced, distributed, transmitted, modified, built upon, "
            "or otherwise used by anyone for any lawful purpose. The work is "
            f"made available under the {link}Creative Commons CC0 public domain "
            f"dedication{close}."
        )

    year = (get_iso8601_date(metadata.date_published) or "")[:4]
    holder = authors[0] if authors else ""
    if len(authors) > 1:
        holder += " et al."
    copyright_line = (
        f'Copyright <span class="copyright">&copy;</span> '
        f"{escape(holder)} {year}.".replace("  ", " ")
    )
    if (identifier or "").lower().startswith("cc-by-4.0"):
        return (
            f"{copyright_line} Distributed under the terms of the {link}Creative "
            f"Commons Attribution 4.0 International License{close}, which permits "
            "unrestricted use, distribution, and reproduction in any medium, "
            "provided the original author and source are credited."
        )
    return (
        f"{copyright_line} Distributed under the terms of the "
        f"{link}{escape(identifier or url)}{close} license."
    )


def to_pdf_meta_tags(metadata: Metadata, authors: list) -> list:
    """The meta tags WeasyPrint turns into the pdf's own metadata.

    Each one lands in both the info dictionary and the XMP packet that PDF/A
    requires: author as /Author and dc:creator, description as /Subject and
    dc:description, keywords as /Keywords and pdf:Keywords, the dcterms dates
    as /CreationDate and /ModDate and their xmp counterparts. `read_pdf_metadata`
    reads them back out. The doi has no slot of its own in either, so it stays
    on the title page rather than becoming a custom info key, which would put
    the pdf outside PDF/A.
    """
    tags = [f'<meta name="author" content="{escape(name)}">' for name in authors]
    if presence(metadata.description):
        tags.append(
            f'<meta name="description" content="{escape(metadata.description)}">'
        )
    keywords = unique(
        [
            subject.get("subject")
            for subject in wrap(metadata.subjects)
            if subject.get("subject", None)
        ]
    )
    if keywords:
        tags.append(f'<meta name="keywords" content="{escape(", ".join(keywords))}">')
    platform = (metadata.container or {}).get("platform", None)
    if platform:
        tags.append(f'<meta name="generator" content="{escape(platform)}">')
    for name, date in (
        ("dcterms.created", metadata.date_published),
        ("dcterms.modified", metadata.date_updated),
    ):
        # W3C-DTF, which is what WeasyPrint parses these as; the iso date is
        # the part of it every record has
        if date:
            tags.append(f'<meta name="{name}" content="{get_iso8601_date(date)}">')
    return tags


def to_pdf_image(metadata: Metadata) -> str | None:
    """The feature image as a data uri, None when there is none to be had.

    Fetched here rather than left to WeasyPrint so the image travels inside
    the pdf instead of the pdf depending on the blog still serving it, and so
    an image that cannot be fetched is left out altogether: WeasyPrint draws
    the alt text wherever an image fails, and "Feature image" printed across
    the title page reads as a mistake rather than as a missing picture.
    """
    url = presence(metadata.image)
    if url is None:
        return None
    try:
        response = http.get(url, timeout=30)
        response.raise_for_status()
    except Exception as error:
        # the image is decoration: no fetch of it is worth failing the render,
        # and in tests the request is the cassette's to refuse
        log.warning(f"Cannot embed the feature image {url}: {error}")
        return None

    mime_type = response.headers.get("Content-Type", "").split(";")[0].strip()
    if not mime_type.startswith("image/"):
        log.warning(f"Feature image {url} is {mime_type or 'of unknown type'}")
        return None
    return f"data:{mime_type};base64,{b64encode(response.content).decode('ascii')}"


def finish_pdf(pdf: bytes, metadata: Metadata) -> bytes:
    """Everything the rendition still needs after WeasyPrint has written it.

    The doi and the licence have no slot among the meta tags WeasyPrint
    reads, but each has a standard XMP property - dc:identifier, and dc:rights
    with the licence url as its xmpRights:WebStatement - so pikepdf writes
    them into the packet WeasyPrint produced, rather than them becoming custom
    info keys, which would put the pdf outside PDF/A. Writing them into that
    same packet, as opposed to appending a second rdf:RDF block, is what makes
    them visible to a reader that looks up properties by name.

    The images then lose their /Interpolate key, which WeasyPrint sets on
    every image it draws and PDF/A forbids (ISO 19005-3 6.2.8: present means
    false). It only ever hinted that a viewer may smooth the image when it is
    scaled up, so dropping it costs the rendition nothing and is what makes
    veraPDF pass the file.
    """
    import pikepdf

    identifier = presence(metadata.id)
    license_id = (metadata.license or {}).get("id", None)
    license_url = (metadata.license or {}).get("url", None)

    output = BytesIO()
    with pikepdf.open(BytesIO(pdf)) as document:
        # update_docinfo would copy these into the info dictionary, where a
        # pdf has no entry for either, and PDF/A wants the two kept in step.
        # set_pikepdf_as_editor would overwrite pdf:Producer, leaving it at
        # odds with the /Producer WeasyPrint wrote, and stamp the current
        # time as xmp:MetadataDate, which would make renditions of the same
        # post differ from each other.
        with document.open_metadata(
            update_docinfo=False, set_pikepdf_as_editor=False
        ) as xmp:
            if identifier:
                xmp["dc:identifier"] = identifier
            if license_id:
                xmp["dc:rights"] = license_id
            if license_url:
                xmp["xmpRights:WebStatement"] = license_url

        for obj in document.objects:
            # every object, rather than every page's images: an image can also
            # sit inside a form xobject
            if (
                isinstance(obj, pikepdf.Stream)
                and obj.get("/Subtype", None) == pikepdf.Name.Image
                and "/Interpolate" in obj
            ):
                del obj["/Interpolate"]

        document.save(output)
    return output.getvalue()


def to_pdf_attachment(metadata: Metadata, weasyprint):
    """The post content, embedded in the pdf as the source it was rendered from.

    PDF/A-3 is the variant that allows an arbitrary embedded file, and
    WeasyPrint gives it the /AFRelationship the standard asks for. The dates
    come from the record so that rendering the same post twice gives the same
    file, rather than the current time WeasyPrint would default to.
    """
    created = to_pdf_datetime(metadata.date_published)
    modified = to_pdf_datetime(metadata.date_updated) or created
    return weasyprint.Attachment(
        string=metadata.content,
        name=f"{Path(pdf_filename(metadata)).stem}.html",
        description="Post content as html (rs:content_html)",
        relationship="Source",
        created=created,
        modified=modified,
    )


def to_pdf_datetime(date: str | None) -> datetime | None:
    """An iso date as the datetime WeasyPrint stamps an attachment with"""
    if not date:
        return None
    try:
        return datetime.fromisoformat(get_iso8601_date(date))
    except (ValueError, TypeError):
        return None


def to_pdf_content(content: str | None, language: str) -> str:
    """The post content, with an alt description on every image.

    A tagged pdf needs one for each image, and WeasyPrint logs an error per
    image that has none - which for a post whose images carry no alt text, as
    blog posts routinely do, is an error per image on every render. An image
    without alt borrows the caption of the figure it sits in, or its own title
    attribute, or takes a generic label in the language of the post. An empty
    alt would not do: WeasyPrint reads it as no description at all.
    """
    if not content or "<img" not in content:
        return content or ""

    soup = BeautifulSoup(content, "html.parser")
    label = PDF_TITLES["image"].get(language, PDF_TITLES["image"]["en"])
    described = False
    for image in soup.find_all("img"):
        if (image.get("alt") or "").strip():
            continue
        figure = image.find_parent("figure")
        caption = figure.find("figcaption") if figure else None
        image["alt"] = (
            (caption.get_text(" ", strip=True) if caption else "")
            or (image.get("title") or "").strip()
            or label
        )
        described = True
    return str(soup) if described else content


def to_pdf_html(metadata: Metadata) -> str:
    """Build the html document the pdf is rendered from.

    The post content is the body, preceded by the front matter that the
    stylesheet styles by class, in the order the rogue-scholar-api pdf template
    used: the title, the blog name (hidden, it only feeds the running header),
    the byline, the publication date, the doi, the description, the feature
    image and the licence. The licence carries `break-after: always`, so the
    front matter is a title page.
    """
    language = get_language(metadata.language, format="alpha_2") or "en"
    authors = [
        name
        for name in (
            to_pdf_author(i)
            for i in wrap(metadata.contributors)
            if "Author" in wrap(i.get("roles", None))
        )
        if name
    ]
    container = metadata.container or {}
    title = escape(metadata.title or "")

    front_matter = [
        f"<h1>{title}</h1>",
        f'<span class="header">{escape(container.get("title", "") or "")}</span>',
    ]
    if authors:
        names = ", ".join(f"<span>{escape(name)}</span>" for name in authors)
        front_matter.append(f'<p class="author">{names}</p>')
    date_published = to_pdf_date(metadata.date_published, language)
    if date_published:
        label = PDF_TITLES["published"].get(language, PDF_TITLES["published"]["en"])
        front_matter.append(f'<div class="date">{label} {escape(date_published)}</div>')
    if metadata.id:
        front_matter.append(
            f'<p class="identifier"><a href="{escape(metadata.id)}">'
            f"{escape(metadata.id)}</a></p>"
        )
    if presence(metadata.description):
        label = PDF_TITLES["abstract"].get(language, PDF_TITLES["abstract"]["en"])
        # the text follows the heading directly, as in the rights block: a <p>
        # would add its own margin on top of the heading's padding
        front_matter.append(
            f'<div class="abstract"><h4>{label}</h4>'
            f"{escape(metadata.description)}</div>"
        )
    image = to_pdf_image(metadata)
    if image:
        front_matter.append(
            f'<img class="feature-image" alt="Feature image" src="{image}" />'
        )
    rights = to_pdf_rights(metadata, authors, language)
    if rights:
        label = PDF_TITLES["copyright"].get(language, PDF_TITLES["copyright"]["en"])
        front_matter.append(f'<div class="rights"><h4>{label}</h4>{rights}</div>')

    head = [
        "<meta charset='utf-8'>",
        f"<title>{title}</title>",
        *to_pdf_meta_tags(metadata, authors),
    ]
    return (
        f"<html lang='{escape(language)}'><head>{''.join(head)}</head>"
        f'<body><section class="front-matter">{"".join(front_matter)}</section>'
        f"{to_pdf_content(metadata.content, language)}</body></html>"
    )


def load_weasyprint():
    """Import WeasyPrint, None when its native stack is missing.

    Imported here rather than at module level because WeasyPrint binds pango,
    cairo and glib through cffi at import time: on a machine without those
    system libraries the import raises OSError rather than ImportError, and
    only the pdf path should pay for that.
    """
    try:
        import weasyprint

        return weasyprint
    except (ImportError, OSError) as error:
        log.error(f"Cannot render pdf, weasyprint needs the pango libraries: {error}")
        return None


@lru_cache(maxsize=1)
def pdf_stylesheet() -> tuple:
    """The shipped stylesheet and the font configuration it registers into.

    Parsed once per process: it reads and registers the six bundled font
    faces, which is the expensive part of rendering a post. The same font
    configuration has to reach `write_pdf`, otherwise the @font-face rules are
    dropped and the text falls back to WeasyPrint's default font.
    """
    import weasyprint
    from weasyprint.text.fonts import FontConfiguration

    font_config = FontConfiguration()
    css = weasyprint.CSS(
        filename=str(PDF_RESOURCES / "style.css"), font_config=font_config
    )
    # WeasyPrint's font configuration calls back into its own module when it is
    # finalized, which fails once the interpreter has torn those modules down.
    # Dropping the cache at exit finalizes it while that is still safe.
    atexit.register(pdf_stylesheet.cache_clear)
    return css, font_config


class DemoteToDebug(logging.Filter):
    """Send a logger's warnings to debug for as long as it is installed."""

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelno == logging.WARNING:
            record.levelno, record.levelname = logging.DEBUG, "DEBUG"
        return True


@contextmanager
def quiet_render_warnings() -> Iterator[None]:
    """Keep what a post is made of out of our logs while it is rendered.

    WeasyPrint reports every declaration it cannot parse and every id it sees
    twice, and post content carries whatever css and markup the blog's editor
    wrote: `background-color: null` from Ghost, or the duplicate anchors a
    Quarto document has. fontTools reports what it finds in the fonts it
    subsets, down to which version of a table they use. None of it says
    anything about the rendition, and nobody here can act on any of it, so it
    is demoted to debug rather than dropped, and only for the render.

    Errors keep their level: a post whose image would not load says something
    worth hearing. So does our own stylesheet, which is parsed before this
    takes effect.
    """
    demote = DemoteToDebug()
    weasyprint_log = logging.getLogger("weasyprint")
    weasyprint_log.addFilter(demote)
    # fontTools reports through a logger per table, and a filter on a logger
    # sees only what is logged to it, not what its children pass up. So its
    # warnings are held back by level instead of being demoted.
    fonttools_log = logging.getLogger("fontTools")
    level = fonttools_log.level
    fonttools_log.setLevel(max(level, logging.ERROR))
    try:
        yield
    finally:
        weasyprint_log.removeFilter(demote)
        fonttools_log.setLevel(level)


def write_pdf_rendition(
    metadata: Metadata, url_fetcher=None, **options
) -> bytes | None:
    """Render the post content as a tagged pdf, None when there is nothing to render.

    ``url_fetcher`` is handed to WeasyPrint for the images the post links, and
    any further ``options`` go to ``write_pdf`` - among them ``pdf_variant``,
    which defaults to PDF/A-3a.
    """
    if presence(metadata.content) is None:
        return None
    weasyprint = load_weasyprint()
    if weasyprint is None:
        return None

    # before the block below, so that a problem with the shipped stylesheet is
    # still reported as one
    css, font_config = pdf_stylesheet()
    # WeasyPrint picks its own fetcher when none is given; naming its default
    # explicitly would go through an api it deprecated in 69.
    fetcher = {"url_fetcher": url_fetcher} if url_fetcher is not None else {}
    options.setdefault("pdf_variant", PDF_VARIANT)
    options.setdefault("attachments", [to_pdf_attachment(metadata, weasyprint)])
    with quiet_render_warnings():
        document = weasyprint.HTML(
            string=to_pdf_html(metadata), base_url=str(PDF_RESOURCES), **fetcher
        ).render(stylesheets=[css], font_config=font_config)
        pdf = document.write_pdf(**options)
    return finish_pdf(pdf, metadata)


def pdf_filename(metadata: Metadata) -> str:
    """Name the pdf after the doi suffix, which is unique and stable"""
    doi = doi_from_url(metadata.id)
    return f"{doi.split('/')[-1]}.pdf" if doi else "content.pdf"


def push_inveniordm(metadata: Metadata, host: str, token: str, **kwargs) -> dict:
    """Push record to InvenioRDM.

    Options:
        previous_doi: the doi this record supersedes.
        skip_unchanged: do not republish a record whose metadata is unchanged.
            Defaults to True.
        write_pdf: deposit a pdf rendition of the post as a record file.
            Ignored for records whose rs:content_html is empty, since that is
            what the pdf is rendered from. Defaults to False, which keeps
            records metadata-only. The file is uploaded while the record is a
            draft. An already published record takes one where the instance
            allows its files to be modified (InvenioRDM 14 and newer, with
            RDM_IMMEDIATE_FILE_MODIFICATION_ENABLED); where it does not, the
            refusal is logged and the record is published without the file.
        system_process: write through InvenioRDM's service layer as
            system_identity rather than over HTTP, for code running inside the
            instance it is writing to. `token` is then unused and may be None.
            Requires an application context and an InvenioRDM installation;
            without either, this falls back to HTTP. Defaults to False.
    """
    if kwargs.get("system_process", False):
        with system_process():
            return push_inveniordm(
                metadata, host, token, **{**kwargs, "system_process": False}
            )

    try:
        doi = normalize_doi(metadata.id)
        if doi is None:
            raise ValueError("no doi provided")

        record = {
            "doi": doi,
            "previous_doi": kwargs.get("previous_doi", None),
        }

        # extract optional information needed
        # community_id is the id of the primary community of the record,
        # in the case of Rogue Scholar the blog community

        if metadata.relations:
            community_index = None
            for i, relation in enumerate(metadata.relations):
                if relation.get("type") == "IsPartOf" and relation.get(
                    "id", ""
                ).startswith(f"https://{host}/api/communities/"):
                    slug = relation.get("id").split("/")[5]
                    community_id = search_by_slug(slug, "blog", host, token)
                    if community_id:
                        record["community"] = slug
                        record["community_id"] = community_id
                        community_index = i
                        continue

            if community_index is not None:
                metadata.relations.pop(community_index)

        # upsert record via the InvenioRDM API
        record = upsert_record(
            metadata,
            host,
            token,
            record,
            skip_unchanged=kwargs.get("skip_unchanged", True),
            write_pdf=kwargs.get("write_pdf", False),
        )

        # optionally add record to InvenioRDM communities
        record = add_record_to_communities(metadata, host, token, record)

        # optionally update external services
        record = update_external_services(metadata, host, token, record, **kwargs)
        return record
    except ValueError as ve:
        log.error(
            f"Value error in push_inveniordm: {str(ve)}",
            exc_info=True,
            extra={"host": host, "record_id": metadata.id},
        )
        record = {
            "doi": doi if "doi" in locals() else None,
            "status": "error",
        }
    except Exception as e:
        log.error(
            f"Unexpected error in push_inveniordm: {str(e)}",
            exc_info=True,
            extra={"host": host, "record_id": record.get("id")},
        )
        record["status"] = "error"

    return record


def push_inveniordm_list(
    metalist: MetadataList, host: str, token: str, **kwargs
) -> bytes | None:
    """Push inveniordm list to InvenioRDM, returns list of push results."""

    if metalist is None:
        return None
    items = [push_inveniordm(item, host, token, **kwargs) for item in metalist.items]
    return json.dumps(items, option=json.OPT_INDENT_2)


def upsert_record(
    metadata: Metadata,
    host: str,
    token: str,
    record: dict,
    skip_unchanged: bool = True,
    write_pdf: bool = False,
) -> dict:
    """Upsert InvenioRDM record, based on DOI"""

    output = write_inveniordm(metadata, write_pdf=write_pdf)

    # Check if record already exists in InvenioRDM
    record["id"] = search_by_doi(doi_from_url(record.get("doi")), host, token)

    # Also check by record guid
    if record["id"] is None:
        guid = next(
            (
                i.get("identifier")
                for i in wrap(metadata.identifiers)
                if i.get("identifier_type") == "GUID" and i.get("identifier")
            ),
            None,
        )
        if guid is not None:
            record["id"] = search_by_guid(guid, host, token)

    if record["previous_doi"] is not None:
        record["previous_id"] = search_by_doi(
            doi_from_url(record["previous_doi"]), host, token
        )

    if record.get("previous_id", None) is not None:
        # Create a new version from the previous record
        record["id"] = record["previous_id"]
        record = create_new_version(record, host, token)

        # Update new version
        record = update_draft_record(record, host, token, output)
    elif record.get("id", None) is not None:
        # Update draft record with new metadata (except PIDs which should not be updated)
        update_output = {k: v for k, v in output.items() if k != "pids"}

        # Publishing an unchanged record still writes a new revision and moves its
        # updated timestamp, so leave the record alone when it already matches.
        # A record still missing its pdf is not left alone, even when the
        # metadata matches: the file is the reason to write it again.
        if skip_unchanged:
            published = get_published_record(record["id"], host, token)
            if (
                published is not None
                and record_matches(update_output, published)
                and (not write_pdf or dig(published, "files.entries"))
            ):
                record["created"] = published.get("created", None)
                record["updated"] = published.get("updated", None)
                record["status"] = "unchanged"
                return record

        # Create draft record from published record
        record = edit_published_record(record, host, token)

        record = update_draft_record(record, host, token, update_output)
    else:
        # Create draft record for DOI that is external or needs to be registered
        # (currently only supported for Crossref PID provider)
        record = create_draft_record(record, host, token, output)

    # Attach the pdf rendition while the record is still a draft: publishing
    # locks its files. dig() rather than write_pdf, so that the upload follows
    # the same content check the writer made when it enabled files.
    if dig(output, "files.enabled") and record.get("id", None):
        record = upload_pdf(metadata, host, token, record)
        # The draft carried a file that could neither be published nor removed,
        # so it was thrown away; there is nothing left to publish, and the
        # record stands as it was published before.
        if record.get("status", None) == "draft_discarded":
            return record

    # Publish draft record
    record = publish_draft_record(record, host, token)

    return record


def add_record_to_communities(
    metadata: Metadata, host: str, token: str, record: dict
) -> dict:
    """Add record to one or more InvenioRDM communities"""

    communities = get_record_communities(record, host, token)
    community_ids = [c.get("id") for c in communities] if communities else []

    # Add record to primary community if primary community is specified
    if (
        record.get("community_id", None) is not None
        and record.get("community_id") not in community_ids
    ):
        record = add_record_to_community(record, host, token, record["community_id"])

    # Add record to subject area community if subject area community is specified
    # Subject area communities should exist for all OpenAlex subfields

    if metadata.subjects:
        for subject in metadata.subjects:
            # OpenAlex subfield
            if subject.get("id", "").startswith("https://openalex.org/subfields/"):
                slug = subject.get("id").split("/")[-1]
                community_id = search_by_slug(slug, "topic", host, token)
                if community_id and community_id not in community_ids:
                    record = add_record_to_community(record, host, token, community_id)
            # OpenAlex subfield of topic
            if subject.get("id", "").startswith("https://openalex.org/T"):
                topic = subject.get("id").split("/")[-1]
                slug = OPENALEX_TOPIC_SUBFIELD_MAPPINGS.get(topic[1:], None)
                if slug is not None:
                    community_id = search_by_slug(slug, "topic", host, token)
                    if community_id and community_id not in community_ids:
                        record = add_record_to_community(
                            record, host, token, community_id
                        )
            subject_name = subject.get("subject", "")
            slug = string_to_slug(subject_name)
            if slug in COMMUNITY_TRANSLATIONS:
                slug = COMMUNITY_TRANSLATIONS[slug]
            community_id = search_by_slug(slug, "topic", host, token)
            if community_id and community_id not in community_ids:
                record = add_record_to_community(record, host, token, community_id)

    # Add record to communities defined as IsPartOf relation in InvenioRDM RelatedIdentifiers
    if metadata.relations:
        for relation in metadata.relations:
            if relation.get("type", None) == "IsPartOf" and relation.get(
                "id", ""
            ).startswith(f"https://{host}/api/communities/"):
                slug = relation.get("id").split("/")[5]
                community_id = search_by_slug(slug, "topic", host, token)
                if community_id and community_id not in community_ids:
                    record = add_record_to_community(record, host, token, community_id)

    return record


def update_external_services(
    metadata: Metadata, host: str, token: str, record: dict, **kwargs
) -> dict:
    """Update external services with changes in InvenioRDM"""

    return record


def create_draft_record(record: dict, host: str, token: str, output: dict) -> dict:
    """Create a new draft record in InvenioRDM"""
    backend = active_backend()
    if backend is not None:
        return backend.create_draft_record(record, output)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.post(
            f"https://{host}/api/records", headers=headers, json=output
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        if response.status_code != 201:
            log.error(
                f"Failed to create draft record: {response.status_code} - {response.json()}"
            )
            record["status"] = "failed_create_draft"
            return record
        data = response.json()
        record["id"] = data.get("id", None)
        record["created"] = data.get("created", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "draft"
        return record
    except RequestException as e:
        log.error(f"Error creating draft record: {str(e)}", exc_info=True)
        record["status"] = "error_draft"
        return record


def upload_pdf(metadata: Metadata, host: str, token: str, record: dict) -> dict:
    """Attach the pdf rendition to a draft record as a record file.

    InvenioRDM takes a file in three calls: register the key, put the bytes,
    commit. They go to the draft, which for an already published record has its
    files locked unless the instance runs InvenioRDM 14 or newer with
    RDM_IMMEDIATE_FILE_MODIFICATION_ENABLED and a policy that admits this
    caller. Where it is locked, the refusal is logged and the record is
    published without the file rather than not published at all.
    """
    pdf = write_pdf_rendition(metadata)
    if pdf is None:
        log.warning(f"No content to render a pdf from for record {record.get('id')}")
        return record

    key = pdf_filename(metadata)

    # Dispatched after rendering, not before: the pdf is built the same way for
    # either transport, and only the three upload calls differ.
    backend = active_backend()
    if backend is not None:
        return backend.upload_file(record, key, pdf)

    url = f"https://{host}/api/records/{record['id']}/draft/files"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = http.post(
            url,
            headers={**headers, "Content-Type": "application/json"},
            json=[{"key": key}],
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        if response.status_code != 201:
            log.warning(
                f"Failed to add pdf {key} to record {record['id']}: "
                f"{response.status_code} - {response.text}"
            )
            return record

        response = http.put(
            f"{url}/{key}/content",
            headers={**headers, "Content-Type": "application/octet-stream"},
            data=pdf,
        )
        response.raise_for_status()

        response = http.post(f"{url}/{key}/commit", headers=headers)
        response.raise_for_status()

        record["files"] = [key]
        return record
    except RequestException as e:
        log.error(
            f"Error uploading pdf {key} for record {record['id']}: {str(e)}",
            exc_info=True,
        )
        return record


def reserve_doi(record: dict, host: str, token: str) -> dict:
    """Reserve a DOI for a draft record."""
    backend = active_backend()
    if backend is not None:
        return backend.reserve_doi(record)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.post(
            f"https://{host}/api/records/{record.get('id')}/draft/pids/doi",
            headers=headers,
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        response.raise_for_status()
        data = response.json()
        record["doi"] = data.get("doi", None)
        record["status"] = "doi_reserved"
        return record
    except RequestException as e:
        log.error(
            f"Error reserving DOI for record {record['id']}: {str(e)}", exc_info=True
        )
        record["status"] = "error_reserve_doi"
        return record


def get_published_record(record_id: str, host: str, token: str) -> dict | None:
    """Read a published record from InvenioRDM"""
    backend = active_backend()
    if backend is not None:
        return backend.read_record(record_id)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.get(f"https://{host}/api/records/{record_id}", headers=headers)
        if response.status_code == 429:
            log.warning(f"Rate limit exceeded while reading record {record_id}")
            return None
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        log.error(f"Error reading record {record_id}: {str(e)}", exc_info=True)
        return None


def _first_difference(sent, stored, path: str = "") -> str | None:
    """Return the path of the first value not already stored, None if all of them are.

    InvenioRDM expands vocabulary entries on read, e.g. `{"id": "eng"}` comes back
    as `{"id": "eng", "title": {"en": "English"}}`, so a stored dict is allowed to
    hold more keys than were sent.
    """
    if isinstance(sent, dict):
        if not isinstance(stored, dict):
            return path
        for key, value in sent.items():
            child = f"{path}.{key}" if path else key
            if key not in stored:
                return child
            difference = _first_difference(value, stored[key], child)
            if difference is not None:
                return difference
        return None
    if isinstance(sent, list):
        if not isinstance(stored, list) or len(sent) != len(stored):
            return path
        for index, (a, b) in enumerate(zip(sent, stored)):
            difference = _first_difference(a, b, f"{path}[{index}]")
            if difference is not None:
                return difference
        return None
    return None if sent == stored else path


def record_matches(output: dict, published: dict) -> bool:
    """Check whether a published record already holds the metadata to be written.

    Republishing writes a new revision even when nothing changed, so this decides
    whether the edit/update/publish cycle can be skipped. Uncertainty resolves to
    False: writing an unchanged record is wasteful, skipping a changed one is a bug.
    The field that ruled out a match is logged, since a value normalised server-side
    would otherwise quietly rule out every record.
    """
    record_id = published.get("id", None)
    for section, owned in (
        ("metadata", INVENIORDM_METADATA_FIELDS),
        ("custom_fields", INVENIORDM_CUSTOM_FIELDS),
    ):
        sent = output.get(section) or {}
        stored = published.get(section) or {}
        # a field that is no longer written but still stored has to be cleared
        for field in owned:
            if field not in sent and presence(stored.get(field)) is not None:
                log.debug(f"Record {record_id} clears {section}.{field}")
                return False

    difference = _first_difference(output, published)
    if difference is not None:
        log.debug(f"Record {record_id} differs at {difference}")
        return False
    return True


def edit_published_record(record: dict, host: str, token: str) -> dict:
    """Create a draft from a published record in InvenioRDM"""
    backend = active_backend()
    if backend is not None:
        return backend.edit_published_record(record)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.post(
            f"https://{host}/api/records/{record['id']}/draft", headers=headers
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        response.raise_for_status()
        data = response.json()
        record["updated"] = data.get("updated", None)
        record["status"] = "edited"
        return record
    except RequestException as e:
        log.error(
            f"Error creating draft from published record: {str(e)}", exc_info=True
        )
        record["status"] = "error_edit_published_record"
        return record


def create_new_version(record: dict, host: str, token: str) -> dict:
    """Create a new version of a published record in InvenioRDM"""
    backend = active_backend()
    if backend is not None:
        return backend.create_new_version(record)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.post(
            f"https://{host}/api/records/{record['id']}/versions", headers=headers
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        response.raise_for_status()
        data = response.json()
        record["id"] = data.get("id", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "new_version"
        return record
    except RequestException as e:
        log.error(
            f"Error creating new version from published record: {str(e)}", exc_info=True
        )
        record["status"] = "error_create_new_version"
        return record


def update_draft_record(
    record: dict, host: str, token: str, inveniordm_data: dict
) -> dict:
    """Update a draft record in InvenioRDM"""
    backend = active_backend()
    if backend is not None:
        return backend.update_draft_record(record, inveniordm_data)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.put(
            f"https://{host}/api/records/{record['id']}/draft",
            headers=headers,
            json=inveniordm_data,
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        response.raise_for_status()
        data = response.json()
        record["updated"] = data.get("updated", None)
        record["status"] = "updated"
        return record
    except RequestException as e:
        log.error(f"Error updating draft record: {str(e)}", exc_info=True)
        record["status"] = "error_update_draft_record"
        return record


def publish_draft_record(record: dict, host: str, token: str) -> dict:
    """Publish a draft record in InvenioRDM"""
    backend = active_backend()
    if backend is not None:
        return backend.publish_draft_record(record)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        if not record.get("id", None):
            raise InvenioRDMError("Missing record id")

        response = http.post(
            f"https://{host}/api/records/{record['id']}/draft/actions/publish",
            headers=headers,
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        if response.status_code != 202:
            log.error(
                f"Failed to publish draft record: {response.status_code} - {response.json()}"
            )
            record["status"] = "error_publish_draft_record"
            return record
        data = response.json()
        record["created"] = data.get("created", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "published"
        return record
    except RequestException as e:
        log.error(f"Error publishing draft record: {str(e)}", exc_info=True)
        record["status"] = "error_publish_draft_record"
        return record


def get_record_communities(record: dict, host: str, token: str) -> list | None:
    """Get record communities by id"""
    backend = active_backend()
    if backend is not None:
        return backend.get_record_communities(record)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.get(
            f"https://{host}/api/records/{record['id']}/communities",
            headers=headers,
        )
        if response.status_code == 429:
            log.warning("Rate limit exceeded while getting communities")
            return None
        response.raise_for_status()
        data = response.json()
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits")
        return None
    except RequestException as e:
        log.error(f"Error getting communities: {str(e)}", exc_info=True)
        return None


def add_record_to_community(
    record: dict, host: str, token: str, community_id: str
) -> dict:
    """Add a record to a community"""
    backend = active_backend()
    if backend is not None:
        return backend.add_record_to_community(record, community_id)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    json = {"communities": [{"id": community_id}]}
    try:
        response = http.post(
            f"https://{host}/api/records/{record['id']}/communities",
            headers=headers,
            json=json,
        )
        if response.status_code == 400:
            # InvenioRDM returns 400 when the community has no logo set or the
            # record is already linked to the community.
            data = response.json()
            log.warning(
                "Failed to add record to community: %s",
                data.get("errors", response.text),
                extra={"record_id": record["id"], "community_id": community_id},
            )
        elif response.status_code == 429:
            log.warning(
                "Rate limit exceeded while adding record to community",
                extra={"record_id": record["id"], "community_id": community_id},
            )
        else:
            response.raise_for_status()
        return record
    except RequestException as e:
        log.error("Error adding record to community: %s", str(e), exc_info=True)
        return record


def search_by_slug(slug: str, type: str, host: str, token: str) -> str | None:
    """Search for a community by slug in InvenioRDM"""
    backend = active_backend()
    if backend is not None:
        return backend.search_community_by_slug(slug)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = [("q", f"slug:{slug}"), ("type", type), ("type", "subject"), ("size", 1)]
    try:
        response = http.get(
            f"https://{host}/api/communities", headers=headers, params=params
        )
        if response.status_code == 429:
            log.warning("Rate limit exceeded while searching for community by slug")
            return None
        response.raise_for_status()
        data = response.json()
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits.0.id")
        return None
    except RequestException as e:
        log.error(f"Error searching for community: {str(e)}", exc_info=True)
        return None


class InvenioRDMError(Exception):
    """Custom exception for InvenioRDM API errors"""
