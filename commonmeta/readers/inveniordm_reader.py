"""InvenioRDM reader for Commonmeta"""

from __future__ import annotations

import logging

from furl import furl
from requests.exceptions import RequestException

from ..api_utils import http
from ..author_utils import get_authors
from ..base_utils import (
    compact,
    dig,
    omit,
    presence,
    sanitize,
    scrub,
    wrap,
)
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
    issn_as_url,
    normalize_doi,
    normalize_ror,
    normalize_url,
)

log = logging.getLogger(__name__)


def get_journal_pages(meta) -> dict:
    """Read volume/issue/pages from ``custom_fields.journal:journal``, splitting
    the ``pages`` string back into first_page/last_page (the inverse of the
    writer's ``pages_as_string``)."""
    journal = dig(meta, "custom_fields.journal:journal") or {}
    pages = journal.get("pages", None)
    first_page = last_page = None
    if pages:
        parts = str(pages).split("-", 1)
        first_page = parts[0].strip() or None
        if len(parts) > 1 and parts[1].strip():
            last_page = parts[1].strip()
    return compact(
        {
            "volume": journal.get("volume", None),
            "issue": journal.get("issue", None),
            "first_page": first_page,
            "last_page": last_page,
        }
    )


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


def read_inveniordm_parent(record) -> dict:
    """Read optional parent metadata from an InvenioRDM ``record``.

    ``record`` may be a plain dict, a Record model, or a ``ChainObject``
    (record + parent); ``dig`` handles all three. This is called by the caller
    of :func:`read_inveniordm` (e.g. ``Metadata`` for a chain object) and the
    result is passed through as kwargs — ``read_inveniordm`` itself never reads
    the ``parent`` object, only the caller does.

    - ``community_issn`` / ``community_doi``: the blog ISSN/DOI registered on the
      community via the communities UI (preferred over the record-level fields).
    - ``concept_doi`` / ``concept_id``: the parent/concept record used to build
      version relationships.
    """
    parent = dig(record, "parent") or {}
    community_fields = dig(parent, "communities.entries.0.custom_fields") or {}
    return {
        "community_issn": community_fields.get("rs:issn"),
        "community_doi": community_fields.get("rs:doi"),
        "concept_doi": dig(parent, "pids.doi.identifier"),
        "concept_id": parent.get("id"),
    }


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
    if _type == "Preprint" and dig(publisher, "name") == "Front Matter":
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

    # optional container metadata. The community DOI/ISSN is resolved by the
    # caller with read_inveniordm_parent() and passed through kwargs (preferred);
    # it is not always available, so fall back to the record-level custom_fields
    # written by the inveniordm writer.
    issn = kwargs.get("community_issn") or dig(
        meta, "custom_fields.journal:journal.issn"
    )
    journal_doi = kwargs.get("community_doi") or dig(meta, "custom_fields.rs:doi")
    identifier = issn or journal_doi or None
    identifier_type = (
        ("ISSN" if issn else "DOI" if journal_doi else None) if identifier else None
    )

    if furl(url).host == "zenodo.org":
        container = compact(
            {
                "identifiers": [
                    {"identifier": "cern.zenodo", "identifier_type": "DataCite"},
                ],
                "type": "Repository",
                "title": "Zenodo",
            }
        )
        publisher = {"name": "Zenodo"}
    elif is_rogue_scholar_doi(_id):
        container = compact(
            {
                "type": "Blog",
                "title": dig(meta, "custom_fields.journal:journal.title"),
                "identifiers": (
                    [{"identifier": identifier, "identifier_type": identifier_type}]
                    if identifier
                    else None
                ),
                "platform": get_generator_platform(
                    dig(meta, "custom_fields.rs:generator", None)
                ),
                **get_journal_pages(meta),
            }
        )
        publisher = {"name": "Front Matter"}
    elif dig(meta, "custom_fields.journal:journal"):
        container = compact(
            {
                "type": "Journal",
                "title": dig(meta, "custom_fields.journal:journal.title"),
                "identifiers": (
                    [{"identifier": identifier, "identifier_type": identifier_type}]
                    if identifier
                    else None
                ),
                **get_journal_pages(meta),
            }
        )
    else:
        container = compact(
            {
                "type": "Repository",
                "identifiers": (
                    [{"identifier": identifier, "identifier_type": identifier_type}]
                    if identifier
                    else None
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
    # Preserve the InvenioRDM record id (rid) as an identifier. It is always a
    # string; numeric ids (e.g. Zenodo) are not record ids and are skipped.
    rid = meta.get("id", None)
    if isinstance(rid, str) and rid:
        identifiers.append(
            {"identifier": rid, "identifier_type": "Other", "scheme": "RID"}
        )
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
    relations = get_relations(wrap(dig(meta, "metadata.related_identifiers")))
    # citing works are represented as IsReferencedBy relations
    relations += get_citations(wrap(dig(meta, "custom_fields.rs:citations")))

    explicit_parent_doi = kwargs.get("parent_doi", None)
    nested_parent_doi = kwargs.get("concept_doi")
    own_doi = doi_as_url(meta.get("doi", None)) or doi_as_url(
        dig(meta, "pids.doi.identifier")
    )

    # Version relationships. The parent/concept DOI deposit (``parent_doi``
    # kwarg, ``_id`` == concept DOI) links to its version via ``HasVersion``; a
    # version record links to its concept DOI via ``IsVersionOf``. Crossref
    # accepts both as ``rel:intra_work_relation``. Both are guarded against
    # self-referential links (relation id == the record's own DOI).
    if explicit_parent_doi:
        parent_url = doi_as_url(explicit_parent_doi)
        if own_doi and own_doi != parent_url:
            relations.append(
                {
                    "id": own_doi,
                    "type": "HasVersion",
                }
            )
    elif nested_parent_doi:
        parent_url = doi_as_url(nested_parent_doi)
        if parent_url and parent_url != own_doi:
            relations.append(
                {
                    "id": parent_url,
                    "type": "IsVersionOf",
                }
            )
    elif meta.get("conceptdoi", None):
        relations.append(
            {
                "id": doi_as_url(meta.get("conceptdoi")),
                "type": "IsVersionOf",
            }
        )
    elif validate_prefix(_id) == "10.59350" and kwargs.get("concept_id"):
        relations.append(
            {
                "id": doi_as_url(f"10.59350/{kwargs.get('concept_id')}"),
                "type": "IsVersionOf",
            }
        )

    # Bibliographic IsPartOf: the blog's ISSN, else its registered DOI.
    if is_rogue_scholar_doi(_id):
        if issn is not None:
            relations.append({"id": issn_as_url(issn), "type": "IsPartOf"})
        elif journal_doi is not None:
            relations.append({"id": journal_doi, "type": "IsPartOf"})

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
    """Convert citing works (custom_fields.rs:citations) to IsReferencedBy
    relations, unifying citations into relations."""

    def get_citation(citation: dict) -> dict | None:
        if not isinstance(citation, dict):
            return None

        if citation.get("scheme", None) == "doi":
            id_ = normalize_doi(citation.get("identifier"))
        elif citation.get("scheme", None) == "url":
            id_ = normalize_url(citation.get("identifier"))
        else:
            id_ = citation.get("identifier")
        if not id_:
            return None
        return {
            "id": id_,
            "type": "IsReferencedBy",
        }

    return [c for c in (get_citation(i) for i in citations) if c is not None]


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
