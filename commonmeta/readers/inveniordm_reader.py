"""InvenioRDM reader for Commonmeta"""

import httpx
from pydash import py_
from furl import furl

from ..utils import (
    normalize_url,
    normalize_doi,
    dict_to_spdx,
    name_to_fos,
    from_inveniordm,
    get_language,
)
from ..base_utils import compact, wrap, presence, sanitize
from ..author_utils import get_authors
from ..date_utils import strip_milliseconds
from ..doi_utils import doi_as_url, doi_from_url
from ..constants import (
    INVENIORDM_TO_CM_TRANSLATIONS,
    COMMONMETA_RELATION_TYPES,
    Commonmeta,
)


def get_inveniordm(pid: str, **kwargs) -> dict:
    """get_inveniordm"""
    if pid is None:
        return {"state": "not_found"}
    url = normalize_url(pid)
    response = httpx.get(url, timeout=10, follow_redirects=True, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json()


def read_inveniordm(data: dict, **kwargs) -> Commonmeta:
    """read_inveniordm"""
    meta = data
    read_options = kwargs or {}

    url = normalize_url(py_.get(meta, "links.self_html"))
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
    title = py_.get(meta, "metadata.title")
    titles = [{"title": sanitize(title)}] if title else None
    additional_titles = py_.get(meta, "metadata.additional_titles")
    # if additional_titles:
    #     titles += [{"title": sanitize("bla")} for i in wrap(additional_titles)]

    date: dict = {}
    date["published"] = py_.get(meta, ("metadata.publication_date"))
    if date["published"]:
        date["published"] = date["published"].split("/")[0]
    date["updated"] = strip_milliseconds(meta.get("updated", None))
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
    else:
        container = py_.get(meta, "custom_fields.journal:journal")
        if container:
            issn = py_.get(meta, "custom_fields.journal:journal.issn")
            container = compact(
                {
                    "type": "Periodical",
                    "title": container.get("title", None),
                    "identifier": issn,
                    "identifierType": "ISSN" if issn else None,
                }
            )
    license_ = py_.get(meta, "metadata.rights[0].id") or py_.get(
        meta, "metadata.license.id"
    )
    if license_:
        license_ = dict_to_spdx({"id": license_})
    descriptions = format_descriptions(
        [
            py_.get(meta, "metadata.description"),
            py_.get(meta, "metadata.notes"),
        ]
    )
    language = py_.get(meta, "metadata.language") or py_.get(
        meta, "metadata.languages[0].id"
    )
    subjects = [name_to_fos(i) for i in wrap(py_.get(meta, "metadata.keywords"))]

    references = get_references(wrap(py_.get(meta, "metadata.related_identifiers")))
    relations = get_relations(wrap(py_.get(meta, "metadata.related_identifiers")))
    if meta.get("conceptdoi", None):
        relations.append(
            {
                "id": doi_as_url(meta.get("conceptdoi")),
                "type": "IsVersionOf",
            }
        )
    files = [get_file(i) for i in wrap(meta.get("files"))]

    return {
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
        "language": get_language(language),
        "version": py_.get(meta, "metadata.version"),
        "license": presence(license_),
        "descriptions": descriptions,
        "geoLocations": None,
        # "funding_references": presence(meta.get("fundingReferences", None)),
        "references": presence(references),
        "relations": presence(relations),
        # other properties
        "files": files,
        "container": container,
        "provider": "DataCite",
    } | read_options


def get_references(references: list) -> list:
    """get_references"""

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
