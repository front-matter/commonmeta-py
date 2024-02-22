"""InvenioRDM reader for Commonmeta"""
import httpx
from pydash import py_

from ..utils import (
    normalize_url,
    normalize_doi,
    dict_to_spdx,
    name_to_fos,
    from_inveniordm,
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

    _id = doi_as_url(meta.get("doi", None))
    resource_type = py_.get(meta, "metadata.resource_type.type")
    _type = INVENIORDM_TO_CM_TRANSLATIONS.get(resource_type, "Other")
    contributors = get_authors(
        from_inveniordm(wrap(py_.get(meta, "metadata.creators")))
    )
    # contrib = get_authors(wrap(meta.get("metadata.contributors", None)))
    # if contrib:
    #     contributors = contributors + contrib

    publisher = {"name": meta.get("publisher", None) or "Zenodo"}

    title = py_.get(meta, "metadata.title")
    titles = [{"title": sanitize(title)}] if title else None

    date: dict = {}
    date["published"] = py_.get(meta, ("metadata.publication_date"))
    date["updated"] = strip_milliseconds(meta.get("updated", None))
    container = compact(
        {
            "id": "https://www.re3data.org/repository/r3d100010468",
            "type": "DataRepository" if _type == "Dataset" else "Repository",
            "title": "Zenodo",
        }
    )
    license_ = py_.get(meta, "metadata.license.id")
    if license_:
        license_ = dict_to_spdx({"id": license_})

    descriptions = format_descriptions(
        [
            py_.get(meta, "metadata.description"),
            py_.get(meta, "metadata.notes"),
        ]
    )
    language = py_.get(meta, "metadata.language")
    subjects = [name_to_fos(i) for i in wrap(py_.get(meta, "metadata.keywords"))]

    references = get_references(wrap(py_.get(meta, "metadata.related_identifiers")))
    related_identifiers = get_related_identifiers(
        wrap(py_.get(meta, "metadata.related_identifiers"))
    )
    if meta.get("conceptdoi", None):
        related_identifiers.append(
            {
                "id": doi_as_url(meta.get("conceptdoi")),
                "type": "IsVersionOf",
            }
        )
    files = [get_file(i) for i in wrap(meta.get("files"))]

    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "id": _id,
        "type": _type,
        "doi": doi_from_url(_id),
        "url": normalize_url(py_.get(meta, "links.self_html")),
        "contributors": contributors,
        "titles": titles,
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional properties
        # "additional_type": additional_type,
        "subjects": presence(subjects),
        "language": language,
        # "alternate_identifiers": presence(meta.get("alternateIdentifiers", None)),
        "sizes": None,
        "formats": None,
        "version": py_.get(meta, "metadata.version"),
        "license": presence(license_),
        "descriptions": descriptions,
        "geo_locations": None,
        # "funding_references": presence(meta.get("fundingReferences", None)),
        # "references": presence(references),
        "related_identifiers": presence(related_identifiers),
        # other properties
        "files": files,
        "container": container,
        "provider": "InvenioRDM",
        "state": state,
        # "schema_version": meta.get("schemaVersion", None),
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
            reference["doi"] = normalize_doi(identifier)
        elif identifier and identifier_type == "URL":
            reference["url"] = normalize_url(identifier)
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


def get_related_identifiers(related_identifiers: list) -> list:
    """get_related_identifiers"""

    def map_related_identifier(related_identifier: dict) -> dict:
        """get_related_identifier"""
        identifier = related_identifier.get("identifier", None)
        scheme = related_identifier.get("scheme", None)
        relation_type = related_identifier.get("relation", None)
        if scheme == "doi":
            identifier = doi_as_url(identifier)
        else:
            identifier = normalize_url(identifier)
        return {
            "id": identifier,
            "type": py_.capitalize(relation_type, False) if relation_type else None,
        }

    identifiers = [map_related_identifier(i) for i in related_identifiers]
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
            "descriptionType": "Abstract" if index == 0 else "Other",
        }
        for index, i in enumerate(descriptions)
        if i
    ]
