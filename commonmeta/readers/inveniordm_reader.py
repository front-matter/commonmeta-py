"""InvenioRDM reader for Commonmeta"""

from typing import Optional

import requests
from furl import furl

from ..author_utils import get_authors
from ..base_utils import compact, dig, omit, presence, sanitize, wrap
from ..constants import (
    COMMONMETA_RELATION_TYPES,
    INVENIORDM_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..date_utils import strip_milliseconds
from ..doi_utils import doi_as_url, doi_from_url, is_rogue_scholar_doi
from ..utils import (
    dict_to_fos,
    dict_to_spdx,
    from_inveniordm,
    get_language,
    name_to_fos,
    normalize_doi,
    normalize_ror,
    normalize_url,
)


def get_inveniordm(pid: str, **kwargs) -> dict:
    """get_inveniordm"""
    if pid is None:
        return {"state": "not_found"}
    url = normalize_url(pid)
    response = requests.get(url, timeout=10, allow_redirects=True, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json()


def read_inveniordm(data: dict, **kwargs) -> Commonmeta:
    """read_inveniordm"""
    meta = data
    read_options = kwargs or {}

    url = normalize_url(dig(meta, "links.self_html"))
    _id = (
        doi_as_url(meta.get("doi", None))
        or doi_as_url(dig(meta, "pids.doi.identifier"))
        or url
    )
    # Rogue Scholar records use an external URL
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

    contributors = dig(meta, "metadata.creators")
    contributors = get_authors(
        from_inveniordm(wrap(contributors)),
    )
    publisher = meta.get("publisher", None) or dig(meta, "metadata.publisher")
    if publisher:
        publisher = {"name": publisher}
    if _type == "Article" and dig(publisher, "name") == "Front Matter":
        _type = "BlogPost"

    title = dig(meta, "metadata.title")
    titles = [{"title": sanitize(title)}] if title else None
    # if additional_titles:
    #     titles += [{"title": sanitize("bla")} for i in wrap(additional_titles)]

    date: dict = {}
    date["published"] = next(
        (
            i.get("date")
            for i in wrap(dig(meta, "metadata.dates"))
            if dig(i, "type.id") == "issued" and i.get("date", None) is not None
        ),
        None,
    ) or dig(meta, ("metadata.publication_date"))
    date["updated"] = next(
        (
            i.get("date")
            for i in wrap(dig(meta, "metadata.dates", []))
            if dig(i, "type.id") == "updated" and i.get("date", None) is not None
        ),
        None,
    ) or strip_milliseconds(meta.get("updated", None))
    f = furl(url)
    if f.host == "zenodo.org":
        container = compact(
            {
                "id": "https://www.re3data.org/repository/r3d100010468",
                "type": "DataRepository" if _type == "Dataset" else "Repository",
                "title": "Zenodo",
            }
        )
        publisher = {"name": "Zenodo"}
    elif f.host == "rogue-scholar.org":
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
                "identifierType": "ISSN" if issn else "URL",
                "platform": dig(meta, "custom_fields.rs:generator", None),
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
                    "identifierType": "ISSN" if issn else None,
                    "platform": dig(meta, "custom_fields.rs:generator", None),
                }
            )
    descriptions = format_descriptions(
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
    subjects = [dict_to_fos(i) for i in wrap(dig(meta, "metadata.subjects"))] or [
        name_to_fos(i) for i in wrap(dig(meta, "metadata.keywords"))
    ]
    references = get_references(wrap(dig(meta, "metadata.references")))
    # fallback to related_identifiers
    if len(references) == 0:
        references = get_references_from_relations(
            wrap(dig(meta, "metadata.related_identifiers"))
        )
    citations = get_citations(wrap(dig(meta, "custom_fields.rs:citations")))
    relations = get_relations(wrap(dig(meta, "metadata.related_identifiers")))
    funding_references = get_funding_references(wrap(dig(meta, "metadata.funding")))
    if meta.get("conceptdoi", None):
        relations.append(
            {
                "id": doi_as_url(meta.get("conceptdoi")),
                "type": "IsVersionOf",
            }
        )

    content = dig(meta, "custom_fields.rs:content_html")
    image = dig(meta, "custom_fields.rs:image")
    state = "findable"
    files = [get_file(i) for i in wrap(meta.get("files"))]

    return {
        **{
            # required properties
            "id": _id,
            "type": _type,
            "doi": doi_from_url(_id),
            "url": url,
            "contributors": presence(contributors),
            "titles": titles,
            "publisher": publisher,
            "date": compact(date),
            # recommended and optional properties
            # "additional_type": additional_type,
            "subjects": presence(subjects),
            "identifiers": presence(identifiers),
            "language": get_language(language),
            "version": dig(meta, "metadata.version"),
            "license": presence(license_),
            "descriptions": descriptions,
            "geoLocations": None,
            "fundingReferences": presence(funding_references),
            "references": presence(references),
            "citations": presence(citations),
            "relations": presence(relations),
            "content": presence(content),
            "image": presence(image),
            "files": presence(files),
            # other properties
            "container": container,
            "provider": "Crossref" if is_rogue_scholar_doi(_id) else "Datacite",
            "state": state,
        },
        **read_options,
    }


def get_references(references: list) -> list:
    """get_references"""

    def get_reference(reference: dict) -> Optional[dict]:
        if not isinstance(reference, dict):
            return None

        if reference.get("scheme", None) == "doi":
            id_ = normalize_doi(reference.get("identifier"))
        elif reference.get("scheme", None) == "url":
            id_ = normalize_url(reference.get("identifier"))
        else:
            id_ = reference.get("identifier")
        return compact(
            {
                "id": id_,
                "unstructured": reference.get("reference", None),
            }
        )

    return [get_reference(i) for i in references]


def get_citations(citations: list) -> list:
    """get citations."""

    def get_citation(citation: dict) -> Optional[dict]:
        if not isinstance(citation, dict):
            return None

        if citation.get("scheme", None) == "doi":
            id_ = normalize_doi(citation.get("identifier"))
        elif citation.get("scheme", None) == "url":
            id_ = normalize_url(citation.get("identifier"))
        else:
            id_ = citation.get("identifier")
        return compact(
            {
                "id": id_,
                "unstructured": citation.get("reference", None),
            }
        )

    return [get_citation(i) for i in citations]


def get_references_from_relations(references: list) -> list:
    """get_references_from_relations"""

    def is_reference(reference):
        """is_reference"""
        return reference.get("relationType", None) in ["Cites", "References"]

    def map_reference(reference):
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
    """get_funding_references"""

    def map_funding(funding: dict) -> dict:
        """map_funding"""

        funder_identifier = normalize_ror(dig(funding, "funder.id"))
        award_uri = dig(funding, "award.identifiers.0.identifier")
        if normalize_doi(award_uri) is not None:
            award_uri = normalize_doi(award_uri)

        return compact(
            {
                "funderName": dig(funding, "funder.name"),
                "funderIdentifier": funder_identifier,
                "funderIdentifierType": "ROR" if funder_identifier else None,
                "awardTitle": dig(funding, "award.title.en"),
                "awardNumber": dig(funding, "award.number"),
                "awardUri": award_uri,
            }
        )

    return [map_funding(i) for i in funding_references]


def get_file(file: dict) -> str:
    """get_file"""
    _type = file.get("type", None)
    return compact(
        {
            "bucket": file.get("bucket", None),
            "key": file.get("key", None),
            "checksum": file.get("checksum", None),
            "url": dig(file, "links.self"),
            "size": file.get("size", None),
            "mimeType": "application/" + _type if _type else None,
        }
    )


def get_relations(relations: list) -> list:
    """get_relations"""

    def map_relation(relation: dict) -> Optional[dict]:
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


def format_descriptions(descriptions: list) -> list:
    """format_descriptions"""
    return [
        {
            "description": sanitize(i),
            "type": "Abstract" if index == 0 else "Other",
        }
        for index, i in enumerate(descriptions)
        if i
    ]


def format_identifier(identifier: dict) -> Optional[dict]:
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
        "identifierType": identifier_type,
    }
