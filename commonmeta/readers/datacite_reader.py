"""datacite reader for Commonmeta"""
from collections import defaultdict
import requests
from pydash import py_

from ..utils import normalize_url, normalize_doi, normalize_cc_url, dict_to_spdx
from ..base_utils import compact, wrap, presence
from ..author_utils import get_authors
from ..date_utils import strip_milliseconds, normalize_date_dict
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
    try:
        response = requests.get(url, kwargs, timeout=10)
        if response.status_code != 200:
            return {"state": "not_found"}
        return py_.get(response.json(), "data.attributes", {})
    except requests.exceptions.ReadTimeout:
        return {"state": "timeout"}

def read_datacite(data: dict, **kwargs) -> Commonmeta:
    """read_datacite"""
    meta = data
    if data is None:
        return {"state": "not_found"}

    read_options = kwargs or {}

    id_ = doi_as_url(meta.get("doi", None))
    resource_type_general = py_.get(meta, "types.resourceTypeGeneral")
    resource_type = py_.get(meta, "types.resourceType")
    type_ = DC_TO_CM_TRANSLATIONS.get(resource_type_general, "Other")
    additional_type = DC_TO_CM_TRANSLATIONS.get(resource_type, None)
    # if resource_type is one of the new resource_type_general types introduced in schema 4.3, use it
    if additional_type:
        type_ = additional_type
        additional_type = None
    else:
        additional_type = resource_type

    contributors = get_authors(wrap(meta.get("creators", None)))
    contrib = get_authors(wrap(meta.get("contributors", None)))
    if contrib:
        contributors = contributors + contrib

    publisher = meta.get("publisher", None)
    if isinstance(publisher, str):
        publisher = {"name": publisher}
    date = get_dates(wrap(meta.get("dates", None)), meta.get("publicationYear", None))
    container = meta.get("container", None)
    license_ = meta.get("rightsList", [])
    if len(license_) > 0:
        license_ = normalize_cc_url(license_[0].get("rightsUri", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    files = [get_file(i) for i in wrap(meta.get("content_url"))]
    references = get_references(
        wrap(meta.get("relatedItems", None) or meta.get("relatedIdentifiers", None))
    )
    descriptions = get_descriptions(wrap(meta.get("descriptions", None)))

    return {
        # required properties
        "id": id_,
        "type": type_,
        "doi": doi_from_url(id_) if id_ else None,
        "url": normalize_url(meta.get("url", None)),
        "contributors": contributors,
        "titles": compact(meta.get("titles", None)),
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional properties
        "additional_type": additional_type,
        "subjects": presence(meta.get("subjects", None)),
        "language": meta.get("language", None),
        "alternate_identifiers": presence(meta.get("alternateIdentifiers", None)),
        "sizes": presence(meta.get("sizes", None)),
        "formats": presence(meta.get("formats", None)),
        "version": meta.get("version", None),
        "license": presence(license_),
        "descriptions": descriptions,
        "geo_locations": wrap(meta.get("geoLocations", None)),
        "funding_references": presence(meta.get("fundingReferences", None)),
        "references": presence(references),
        # other properties
        "files": presence(files),
        "container": presence(container),
        "provider": "DataCite",
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
                "relatedMetadataScheme",
            ],
        )
        return reference

    return [map_reference(i) for i in references if is_reference(i)]


def get_file(file: str) -> dict:
    """get_file"""
    return compact({"url": file})


def get_dates(dates: list, publication_year) -> dict:
    """convert date list to dict, rename and/or remove some keys"""
    date: dict = defaultdict(list)
    for sub in dates:
        date[sub.get("dateType", None)] = sub.get("date", None)
    if date.get("Issued", None) is None and publication_year is not None:
        date["Issued"] = str(publication_year)
    return normalize_date_dict(date)


def get_descriptions(descriptions: list) -> list:
    """get_descriptions"""

    def is_description(description):
        """is_description"""
        return description.get("descriptionType", None) in [
            "Abstract",
            "Methods",
            "SeriesInformation",
            "TableOfContents",
            "TechnicalInfo",
            "Other",
        ]

    def map_description(description):
        """map_description"""
        return {
            "description": description.get("description", None),
            "descriptionType": description.get("descriptionType", None),
        }

    return [
        map_description(i)
        for i in descriptions
        if is_description(i) and i.get("description", None) is not None
    ]
