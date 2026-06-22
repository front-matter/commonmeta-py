"""InvenioRDM reader for Commonmeta"""

from __future__ import annotations

import logging

from furl import furl
from requests.exceptions import RequestException

from ..api_utils import http
from ..author_utils import get_authors
from ..base_utils import compact, dig, omit, presence, sanitize, scrub, wrap
from ..constants import (
    COMMONMETA_RELATION_TYPES,
    INVENIORDM_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..date_utils import strip_milliseconds
from ..doi_utils import doi_as_url, is_rogue_scholar_doi, validate_prefix
from ..utils import (
    dict_to_spdx,
    from_inveniordm,
    get_language,
    normalize_doi,
    normalize_ror,
    normalize_url,
)

log = logging.getLogger(__name__)


def get_generator_platform(generator) -> str | None:
    """container.platform is a string per the v1.0 schema, but
    custom_fields.rs:generator can be a dict ({id, title: {en: ...}})
    rather than a plain string."""
    if isinstance(generator, dict):
        return generator.get("id", None) or dig(generator, "title.en", None)
    return generator


def get_inveniordm(pid: str, **kwargs) -> dict:
    """get_inveniordm"""
    if pid is None:
        return {"state": "not_found"}
    url = normalize_url(pid)
    response = http.get(url, timeout=10, allow_redirects=True, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json()


def read_inveniordm(data: dict, **kwargs) -> Commonmeta:
    """read_inveniordm"""
    meta = data
    read_options = kwargs or {}

    url = normalize_url(kwargs.get("url", None) or dig(meta, "links.self_html"))

    # if data is for a parent record
    if kwargs.get("parent_doi", None):
        _id = doi_as_url(kwargs.get("parent_doi", None))
    else:
        _id = (
            doi_as_url(meta.get("doi", None))
            or doi_as_url(dig(meta, "pids.doi.identifier"))
            or url
        )

    # Rogue Scholar records use an external URL
    # TODO: enable use of Rogue Scholar repository URL
    if is_rogue_scholar_doi(_id):
        url = next(
            (
                normalize_url(identifier.get("identifier"))
                for identifier in wrap(dig(meta, "metadata.identifiers"))
                if identifier.get("scheme") == "url"
                and identifier.get("identifier", None) is not None
            ),
            None,
        )

    resource_type = dig(meta, "metadata.resource_type.type") or dig(
        meta, "metadata.resource_type.id"
    )
    _type = INVENIORDM_TO_CM_TRANSLATIONS.get(resource_type, "Other")

    contrib = wrap(dig(meta, "metadata.creators")) + wrap(
        dig(meta, "metadata.contributors")
    )
    contributors = get_authors(
        from_inveniordm(contrib),
    )
    publisher = meta.get("publisher", None) or dig(meta, "metadata.publisher")
    if publisher:
        publisher = {"name": publisher}
    if _type == "Article" and dig(publisher, "name") == "Front Matter":
        _type = "BlogPost"

    title = dig(meta, "metadata.title")
    title = sanitize(title) if title else None
    # if additional_titles:
    #     additional_titles += [{"title": sanitize("bla")} for i in wrap(additional_titles)]
    additional_titles: list = []

    date_published = next(
        (
            i.get("date")
            for i in wrap(dig(meta, "metadata.dates"))
            if dig(i, "type.id") == "issued" and i.get("date", None) is not None
        ),
        None,
    ) or dig(meta, ("metadata.publication_date"))
    date_updated = next(
        (
            i.get("date")
            for i in wrap(dig(meta, "metadata.dates", []))
            if dig(i, "type.id") == "updated" and i.get("date", None) is not None
        ),
        None,
    ) or strip_milliseconds(meta.get("updated", None))
    if furl(url).host == "zenodo.org":
        container = compact(
            {
                "id": "https://www.re3data.org/repository/r3d100010468",
                "type": "DataRepository" if _type == "Dataset" else "Repository",
                "title": "Zenodo",
            }
        )
        publisher = {"name": "Zenodo"}
    elif is_rogue_scholar_doi(_id):
        issn = dig(meta, "custom_fields.journal:journal.issn")
        slug = dig(meta, "parent.communities.entries.0.slug")
        community_url = (
            f"https://rogue-scholar.org/communities/{slug}" if slug else None
        )
        container = compact(
            {
                "type": "Blog",
                "title": dig(meta, "custom_fields.journal:journal.title"),
                "identifier": issn if issn else community_url,
                "identifier_type": "ISSN" if issn else "URL",
                "platform": get_generator_platform(
                    dig(meta, "custom_fields.rs:generator", None)
                ),
            }
        )
        publisher = {"name": "Front Matter"}
    else:
        container = dig(meta, "custom_fields.journal:journal")
        if container:
            issn = dig(meta, "custom_fields.journal:journal.issn")
            container = compact(
                {
                    "type": "Periodical",
                    "title": container.get("title", None),
                    "identifier": issn if issn else None,
                    "identifier_type": "ISSN" if issn else None,
                    "platform": get_generator_platform(
                        dig(meta, "custom_fields.rs:generator", None)
                    ),
                }
            )
    description, additional_descriptions = get_descriptions(
        [
            dig(meta, "metadata.description"),
            dig(meta, "metadata.notes"),
        ]
    )
    identifiers = [
        result
        for i in wrap(dig(meta, "metadata.identifiers"))
        if (result := format_identifier(i)) is not None
    ]
    language = dig(meta, "metadata.language") or dig(meta, "metadata.languages.0.id")
    license_ = dig(meta, "metadata.rights.0.id") or dig(meta, "metadata.license.id")
    if license_:
        license_ = dict_to_spdx({"id": license_})
    subjects = get_subjects(
        wrap(dig(meta, "metadata.subjects")) + wrap(dig(meta, "metadata.keywords"))
    )
    references = get_references(wrap(dig(meta, "metadata.references")))
    # fallback to related_identifiers
    if len(references) == 0:
        references = get_references_from_relations(
            wrap(dig(meta, "metadata.related_identifiers"))
        )
    citations = get_citations(wrap(dig(meta, "custom_fields.rs:citations")))
    relations = get_relations(wrap(dig(meta, "metadata.related_identifiers")))

    # if data is for a parent record
    if kwargs.get("parent_doi", None):
        related_id = doi_as_url(meta.get("doi", None)) or doi_as_url(
            dig(meta, "pids.doi.identifier")
        )
        relations.append(
            {
                "id": related_id,
                "type": "HasVersion",
            }
        )
    elif meta.get("conceptdoi", None):
        relations.append(
            {
                "id": doi_as_url(meta.get("conceptdoi")),
                "type": "IsVersionOf",
            }
        )
    elif validate_prefix(_id) == "10.59350" and dig(meta, "parent.id"):
        relations.append(
            {
                "id": doi_as_url(f"10.59350/{dig(meta, 'parent.id')}"),
                "type": "IsVersionOf",
            }
        )

    funding_references = get_funding_references(wrap(dig(meta, "metadata.funding")))
    version = dig(meta, "metadata.version")
    content = dig(meta, "custom_fields.rs:content_html")
    image = dig(meta, "custom_fields.rs:image")
    state = "findable"
    files = [get_file(i) for i in wrap(meta.get("files"))]

    return {
        **{
            # required properties
            "id": _id,
            "type": _type,
            # recommended and optional properties
            "additional_descriptions": presence(additional_descriptions),
            "additional_titles": presence(additional_titles),
            # "additional_type": additional_type,
            "citations": presence(citations),
            "container": container,
            "content": presence(content),
            "contributors": contributors,
            "date_published": date_published,
            "date_updated": date_updated,
            "description": description,
            "files": presence(files),
            "funding_references": presence(funding_references),
            "geo_locations": None,
            "identifiers": presence(identifiers),
            "image": presence(image),
            "language": get_language(language),
            "license": presence(license_),
            "provider": "Crossref" if is_rogue_scholar_doi(_id) else "DataCite",
            "publisher": publisher,
            "references": presence(references),
            "relations": presence(relations),
            "state": state,
            "subjects": presence(subjects),
            "title": title,
            "url": url,
            "version": version,
        },
        **read_options,
    }


def get_references(references: list) -> list:
    """get_references"""

    def get_reference(reference: dict) -> dict | None:
        if not isinstance(reference, dict):
            return None

        if reference.get("scheme", None) == "doi":
            id_ = normalize_doi(reference.get("identifier"))
        elif reference.get("scheme", None) == "url":
            id_ = normalize_url(reference.get("identifier"))
        else:
            id_ = reference.get("identifier")
        return {
            "id": id_,
            "unstructured": reference.get("reference", None),
        }

    return [get_reference(i) for i in references]


def get_citations(citations: list) -> list:
    """get citations."""

    def get_citation(citation: dict) -> dict | None:
        if not isinstance(citation, dict):
            return None

        if citation.get("scheme", None) == "doi":
            id_ = normalize_doi(citation.get("identifier"))
        elif citation.get("scheme", None) == "url":
            id_ = normalize_url(citation.get("identifier"))
        else:
            id_ = citation.get("identifier")
        return {
            "id": id_,
            "unstructured": citation.get("reference", None),
        }

    return [get_citation(i) for i in citations]


def get_references_from_relations(references: list) -> list:
    """get_references_from_relations"""

    def is_reference(reference) -> bool:
        """is_reference"""
        return reference.get("relationType", None) in ["Cites", "References"]

    def map_reference(reference) -> dict:
        """map_reference"""
        identifier = reference.get("relatedIdentifier", None)
        identifier_type = reference.get("relatedIdentifierType", None)
        if identifier and identifier_type == "DOI":
            reference["id"] = normalize_doi(identifier)
        elif identifier and identifier_type == "URL":
            reference["id"] = normalize_url(identifier)
        reference = omit(
            reference,
            [
                "relationType",
                "relatedIdentifier",
                "relatedIdentifierType",
                "resourceTypeGeneral",
                "schemeType",
                "schemeUri",
                "relatedMetadataScheme",
            ],
        )
        return reference

    return [map_reference(i) for i in references if is_reference(i)]


def get_funding_references(funding_references: list) -> list:
    """get_funding_references

    InvenioRDM funder identifiers come from a controlled vocabulary entry
    (funder.id) that is always a ROR ID, so normalize_ror already enforces
    the v1.0 ROR-only constraint on funder_id: it returns None for anything
    that isn't a valid ROR ID rather than leaking another identifier scheme.
    """

    def map_funding(funding: dict) -> dict:
        """map_funding"""

        funder_id = normalize_ror(dig(funding, "funder.id"))
        award_id = dig(funding, "award.identifiers.0.identifier")
        if normalize_doi(award_id) is not None:
            award_id = normalize_doi(award_id)

        return compact(
            {
                "funder_id": funder_id,
                "funder_name": dig(funding, "funder.name"),
                "award_id": award_id,
                "award_title": dig(funding, "award.title.en"),
                "award_number": dig(funding, "award.number"),
            }
        )

    return [map_funding(i) for i in funding_references]


def get_subjects(subjects: list) -> list:
    """get_subjects/keywords. Can be list of dicts (Subjects: InvenioRDM) or list of strings (Keywords: Zenodo)."""

    def get_subject(subject: dict) -> dict | None:
        if isinstance(subject, str):
            return {"subject": subject}
        if not isinstance(subject, dict) or subject.get("subject", None) is None:
            return None

        if subject.get("id", None) is not None:
            return {"id": subject.get("id"), "subject": subject.get("subject")}

        if subject.get("scheme", None) == "FOS":
            subj_str = f"FOS: {subject.get('subject')}"
        elif subject.get("scheme", None) == "Domains":
            subj_str = f"Domain: {subject.get('subject')}"
        elif subject.get("scheme", None) == "Fields":
            subj_str = f"Field: {subject.get('subject')}"
        elif subject.get("scheme", None) == "Subfields":
            subj_str = f"Subfield: {subject.get('subject')}"
        elif subject.get("scheme", None) == "Topics":
            subj_str = f"Topic: {subject.get('subject')}"
        else:
            subj_str = subject.get("subject")
        return {"subject": subj_str}

    return scrub([get_subject(i) for i in subjects])


def get_file(file: dict) -> dict | None:
    """get_file"""
    _type = file.get("type", None)
    return compact(
        {
            "bucket": file.get("bucket", None),
            "key": file.get("key", None),
            "checksum": file.get("checksum", None),
            "url": dig(file, "links.self"),
            "size": file.get("size", None),
            "mime_type": "application/" + _type if _type else None,
        }
    )


def get_relations(relations: list) -> list:
    """get_relations"""

    def map_relation(relation: dict) -> dict | None:
        """map_relation"""
        identifier = dig(relation, "identifier")
        scheme = dig(relation, "scheme")
        relation_type = dig(relation, "relation_type.id") or dig(relation, "relation")

        # Return None if essential data is missing
        if not identifier or not relation_type:
            return None

        if scheme == "doi":
            identifier = doi_as_url(identifier)
        else:
            identifier = normalize_url(identifier)
        return {
            "id": identifier,
            "type": (relation_type[0].upper() + relation_type[1:]),
        }

    identifiers = [result for i in relations if (result := map_relation(i)) is not None]
    return [i for i in identifiers if i.get("type") in COMMONMETA_RELATION_TYPES]


def get_descriptions(descriptions: list) -> tuple[str | None, list]:
    """get_descriptions

    Returns a tuple of (description, additional_descriptions) per the
    commonmeta v1.0 schema, where description is a single scalar string.
    """
    items = [
        {
            "description": sanitize(i),
            "type": "Abstract" if index == 0 else "Other",
        }
        for index, i in enumerate(descriptions)
        if i
    ]
    if not items:
        return None, []
    description = items[0].get("description", None)
    return description, items[1:]


def format_identifier(identifier: dict) -> dict | None:
    """format_identifier. scheme url is stored as url metadata."""
    if (
        identifier.get("identifier", None) is None
        or identifier.get("scheme", None) is None
        or identifier.get("scheme") == "url"
    ):
        return None

    scheme = identifier.get("scheme")
    if scheme == "doi":
        identifier_type = "DOI"
    elif scheme == "uuid":
        identifier_type = "UUID"
    elif scheme == "guid":
        identifier_type = "GUID"
    else:
        identifier_type = None
    return {
        "identifier": identifier.get("identifier"),
        "identifier_type": identifier_type,
    }


def search_by_doi(doi, host, token) -> str | None:
    """Search for a record by DOI in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = {"q": f"doi:{doi}", "size": 1}
    try:
        response = http.get(
            f"https://{host}/api/records", headers=headers, params=params
        )
        if response.status_code == 429:
            log.warning("Rate limit exceeded while searching by DOI")
            return None
        response.raise_for_status()
        data = response.json()
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits.0.id")
        return None
    except RequestException as e:
        log.error(f"Error searching for DOI {doi}: {str(e)}", exc_info=True)
        return None


def search_by_guid(guid, host, token) -> str | None:
    """Search for a record by GUID in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = {"q": f'metadata.identifiers.identifier:"{guid}"', "size": 1}
    try:
        response = http.get(
            f"https://{host}/api/records", headers=headers, params=params
        )
        if response.status_code == 429:
            log.warning("Rate limit exceeded while searching by GUID")
            return None
        response.raise_for_status()
        data = response.json()
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits.0.id")
        return None
    except RequestException as e:
        log.error(f"Error searching for GUID {guid}: {str(e)}", exc_info=True)
        return None
