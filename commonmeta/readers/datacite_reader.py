"""datacite reader for Commonmeta"""
import requests
from pydash import py_

from ..utils import normalize_url, normalize_doi
from ..base_utils import compact, wrap, presence
from ..author_utils import get_authors
from ..date_utils import strip_milliseconds
from ..doi_utils import doi_as_url, doi_from_url, datacite_api_url
from ..constants import (
    DC_TO_CM_TRANSLATIONS,
    Commonmeta,
)


def get_datacite(pid: str, **kwargs) -> dict:
    """get_datacite"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = datacite_api_url(doi)
    response = requests.get(url, kwargs, timeout=5)
    if response.status_code != 200:
        return {"state": "not_found"}
    return py_.get(response.json(), "data.attributes", {})


def read_datacite(data: dict, **kwargs) -> Commonmeta:
    """read_datacite"""
    meta = data

    read_options = kwargs or {}

    id_ = doi_as_url(meta.get("doi", None))
    resource_type_general = py_.get(meta, "types.resourceTypeGeneral")
    resource_type = py_.get(meta, "types.resourceType")
    type_ = DC_TO_CM_TRANSLATIONS.get(resource_type_general, 'Other')
    additional_type = DC_TO_CM_TRANSLATIONS.get(resource_type, None)
    # if resource_type is one of the new resource_type_general types introduced in schema 4.3, use it
    if additional_type:
        type_ = additional_type
        additional_type = None

    container = meta.get("container", None)
    print(container)
    rights = meta.get("rightsList", None)
    references = get_references(wrap(meta.get("relatedItems", None) or meta.get("relatedIdentifiers", None)))

    return {
        # required properties
        "id": id_,
        "type": type_,
        "doi": doi_from_url(id_) if id_ else None,
        "url": normalize_url(meta.get("url", None)),
        "creators": get_authors(wrap(meta.get("creators", None))),
        "titles": compact(meta.get("titles", None)),
        "publisher": meta.get("publisher", None),
        "publication_year": int(meta.get("publicationYear", None)),
        # recommended and optional properties
        "additional_type": additional_type,
        "subjects": presence(meta.get("subjects", None)),
        "contributors": get_authors(wrap(meta.get("contributors", None))),
        "dates": presence(meta.get("dates", None))
        or [{"date": meta.get("publicationYear", None), "dateType": "Issued"}],
        "language": meta.get("language", None),
        "alternate_identifiers": presence(meta.get("alternateIdentifiers", None)),
        "sizes": presence(meta.get("sizes", None)),
        "formats": presence(meta.get("formats", None)),
        "version": meta.get("version", None),
        "rights": presence(rights),
        "descriptions": meta.get("descriptions", None),
        "geo_locations": wrap(meta.get("geoLocations", None)),
        "funding_references": presence(meta.get("fundingReferences", None)),
        "references": presence(references),
        # other properties
        "date_created": strip_milliseconds(meta.get("created", None)),
        "date_registered": strip_milliseconds(meta.get("registered", None)),
        "date_published": strip_milliseconds(meta.get("published", None)),
        "date_updated": strip_milliseconds(meta.get("updated", None)),
        "content_url": presence(meta.get("contentUrl", None)),
        "container": presence(container),
        "agency": "DataCite",
        "state": "findable",
        "schema_version": meta.get("schemaVersion", None),
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
                "relatedMetadataScheme"
            ])
        return reference
    return [map_reference(i) for i in references if is_reference(i)]
