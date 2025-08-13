"""InvenioRDM reader for Commonmeta"""

from typing import Optional

import requests
from furl import furl
from pydash import py_

from ..author_utils import get_authors
from ..base_utils import compact, presence, sanitize, wrap
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
    normalize_url,
    validate_ror,
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

    url = normalize_url(py_.get(meta, "links.self_html")) or next(
        (
            normalize_url(identifier.get("identifier"))
            for identifier in wrap(py_.get(meta, "metadata.identifiers", []))
            if identifier.get("scheme") == "url"
            and identifier.get("identifier", None) is not None
        ),
        None,
    )
    _id = (
        doi_as_url(meta.get("doi", None))
        or doi_as_url(py_.get(meta, "pids.doi.identifier"))
        or url
    )
    resource_type = py_.get(meta, "metadata.resource_type.type") or py_.get(
        meta, "metadata.resource_type.id"
    )
    _type = INVENIORDM_TO_CM_TRANSLATIONS.get(resource_type, "Other")

    contributors = py_.get(meta, "metadata.creators")
    contributors = get_authors(
        from_inveniordm(wrap(contributors)),
    )
    publisher = meta.get("publisher", None) or py_.get(meta, "metadata.publisher")
    if publisher:
        publisher = {"name": publisher}
    if _type == "Article" and py_.get(publisher, "name") == "Front Matter":
        _type = "BlogPost"

    title = py_.get(meta, "metadata.title")
    titles = [{"title": sanitize(title)}] if title else None
    # if additional_titles:
    #     titles += [{"title": sanitize("bla")} for i in wrap(additional_titles)]

    date: dict = {}
    date["published"] = next(
        (
            i.get("date")
            for i in wrap(py_.get(meta, "metadata.dates", []))
            if py_.get(i, "type.id") == "issued" and i.get("date", None) is not None
        ),
        None,
    ) or py_.get(meta, ("metadata.publication_date"))
    date["updated"] = next(
        (
            i.get("date")
            for i in wrap(py_.get(meta, "metadata.dates", []))
            if py_.get(i, "type.id") == "updated" and i.get("date", None) is not None
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
        issn = py_.get(meta, "custom_fields.journal:journal.issn")
        slug = py_.get(meta, "parent.communities.entries.0.slug")
        community_url = (
            f"https://rogue-scholar.org/communities/{slug}" if slug else None
        )
        container = compact(
            {
                "type": "Blog",
                "title": py_.get(meta, "custom_fields.journal:journal.title"),
                "identifier": issn if issn else community_url,
                "identifierType": "ISSN" if issn else "URL",
                "platform": py_.get(meta, "custom_fields.rs:generator", None),
            }
        )
        publisher = {"name": "Front Matter"}
    else:
        container = py_.get(meta, "custom_fields.journal:journal")
        if container:
            issn = py_.get(meta, "custom_fields.journal:journal.issn")
            container = compact(
                {
                    "type": "Periodical",
                    "title": container.get("title", None),
                    "identifier": issn if issn else None,
                    "identifierType": "ISSN" if issn else None,
                    "platform": py_.get(meta, "custom_fields.rs:generator", None),
                }
            )
    descriptions = format_descriptions(
        [
            py_.get(meta, "metadata.description"),
            py_.get(meta, "metadata.notes"),
        ]
    )
    identifiers = py_.compact(
        [format_identifier(i) for i in wrap(py_.get(meta, "metadata.identifiers"))]
    )
    language = py_.get(meta, "metadata.language") or py_.get(
        meta, "metadata.languages[0].id"
    )
    license_ = py_.get(meta, "metadata.rights[0].id") or py_.get(
        meta, "metadata.license.id"
    )
    if license_:
        license_ = dict_to_spdx({"id": license_})
    subjects = [dict_to_fos(i) for i in wrap(py_.get(meta, "metadata.subjects"))] or [
        name_to_fos(i) for i in wrap(py_.get(meta, "metadata.keywords"))
    ]
    references = get_references(wrap(py_.get(meta, "metadata.references")))
    # fallback to related_identifiers
    if len(references) == 0:
        references = get_references_from_relations(
            wrap(py_.get(meta, "metadata.related_identifiers"))
        )
    relations = get_relations(wrap(py_.get(meta, "metadata.related_identifiers")))
    funding_references = get_funding_references(wrap(py_.get(meta, "metadata.funding")))
    if meta.get("conceptdoi", None):
        relations.append(
            {
                "id": doi_as_url(meta.get("conceptdoi")),
                "type": "IsVersionOf",
            }
        )

    content = py_.get(meta, "custom_fields.rs:content_html")
    image = py_.get(meta, "custom_fields.rs:image")
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
            "version": py_.get(meta, "metadata.version"),
            "license": presence(license_),
            "descriptions": descriptions,
            "geoLocations": None,
            "fundingReferences": presence(funding_references),
            "references": presence(references),
            "relations": presence(relations),
            "content": presence(content),
            "image": presence(image),
            "files": presence(files),
            # other properties
            "container": container,
            "provider": "Crossref" if is_rogue_scholar_doi(_id) else "Datacite",
        },
        **read_options,
    }


def get_references(references: list) -> list:
    """get_references"""

    def get_reference(reference: dict) -> Optional[dict]:
        if reference is None or not isinstance(reference, dict):
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
        reference = py_.omit(
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

        return compact(
            {
                "funderName": py_.get(funding, "funder.name"),
                "funderIdentifier": py_.get(funding, "funder.id"),
                "funderIdentifierType": "ROR"
                if validate_ror(py_.get(funding, "funder.id"))
                else None,
                "awardTitle": py_.get(funding, "award.title.en"),
                "awardNumber": py_.get(funding, "award.number"),
                "awardUri": py_.get(funding, "award.identifiers[0].identifier"),
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
            "url": py_.get(file, "links.self"),
            "size": file.get("size", None),
            "mimeType": "application/" + _type if _type else None,
        }
    )


def get_relations(relations: list) -> list:
    """get_relations"""

    def map_relation(relation: dict) -> dict:
        """map_relation"""
        identifier = relation.get("identifier", None)
        scheme = relation.get("scheme", None)
        relation_type = relation.get("relation", None) or relation.get(
            "relation_type", None
        )
        if scheme == "doi":
            identifier = doi_as_url(identifier)
        else:
            identifier = normalize_url(identifier)
        return {
            "id": identifier,
            "type": py_.capitalize(relation_type, False) if relation_type else None,
        }

    identifiers = [map_relation(i) for i in relations]
    return [
        i
        for i in identifiers
        if py_.upper_first(i["type"]) in COMMONMETA_RELATION_TYPES
    ]


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
