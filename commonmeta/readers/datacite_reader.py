"""datacite reader for Commonmeta"""

from collections import defaultdict
from typing import Optional
import httpx
from pydash import py_

from ..utils import (
    normalize_url,
    normalize_doi,
    normalize_cc_url,
    dict_to_spdx,
    format_name_identifier,
)
from ..base_utils import compact, wrap, presence
from ..author_utils import get_authors
from ..date_utils import normalize_date_dict
from ..doi_utils import (
    doi_as_url,
    doi_from_url,
    datacite_api_url,
    datacite_api_sample_url,
)
from ..constants import (
    DC_TO_CM_TRANSLATIONS,
    DC_TO_CM_CONTAINER_TRANSLATIONS,
    Commonmeta,
)


def get_datacite(pid: str, **kwargs) -> dict:
    """get_datacite"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = datacite_api_url(doi)
    try:
        response = httpx.get(url, timeout=10, **kwargs)
        if response.status_code != 200:
            return {"state": "not_found"}
        return py_.get(response.json(), "data.attributes", {}) | {"via": "datacite"}
    except httpx.ReadTimeout:
        return {"state": "timeout"}


def read_datacite(data: dict, **kwargs) -> Commonmeta:
    """read_datacite"""
    meta = data
    if data is None:
        return {"state": "not_found"}

    read_options = kwargs or {}

    _id = doi_as_url(meta.get("doi", None))
    resource__typegeneral = py_.get(meta, "types.resourceTypeGeneral")
    resource_type = py_.get(meta, "types.resourceType")
    _type = DC_TO_CM_TRANSLATIONS.get(resource__typegeneral, "Other")
    additional_type = DC_TO_CM_TRANSLATIONS.get(resource_type, None)
    # if resource_type is one of the new resource__typegeneral types introduced in schema 4.3, use it
    if additional_type:
        _type = additional_type
        additional_type = None
    else:
        additional_type = resource_type
    titles = get_titles(wrap(meta.get("titles", None)))

    contributors = get_authors(wrap(meta.get("creators", None)))
    contrib = get_authors(wrap(meta.get("contributors", None)))
    if contrib:
        contributors = contributors + contrib

    publisher = meta.get("publisher", None)
    if isinstance(publisher, str):
        publisher = {"name": publisher}
    elif isinstance(publisher, dict):
        publisher = get_publisher(publisher)
    date = get_dates(wrap(meta.get("dates", None)), meta.get("publicationYear", None))
    container = get_container(meta.get("container", None))
    license_ = meta.get("rightsList", [])
    if len(license_) > 0:
        license_ = normalize_cc_url(license_[0].get("rightsUri", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    files = [get_file(i) for i in wrap(meta.get("content_url"))]

    identifiers = get_identifiers(wrap(meta.get("alternateIdentifiers", None)))
    identifiers.append(
        compact(
            {
                "identifier": normalize_doi(_id),
                "identifierType": "DOI",
            }
        )
    )

    references = get_references(
        wrap(meta.get("relatedItems", None) or meta.get("relatedIdentifiers", None))
    )
    relations = get_relations(wrap(meta.get("relatedIdentifiers", None)))
    descriptions = get_descriptions(wrap(meta.get("descriptions", None)))
    geo_locations = get_geolocation(wrap(meta.get("geoLocations", None)))

    def format_subject(subject):
        """format_subject"""
        return compact(
            {
                "subject": subject.get("subject", None),
                "language": subject.get("lang", None),
            }
        )

    subjects = py_.uniq([format_subject(i) for i in wrap(meta.get("subjects", None))])

    return {
        # required properties
        "id": _id,
        "type": _type,
        # recommended and optional properties
        "additionalType": additional_type,
        "container": presence(container),
        "contributors": presence(contributors),
        "date": compact(date),
        "descriptions": presence(descriptions),
        "files": presence(files),
        "fundingReferences": presence(meta.get("fundingReferences", None)),
        "geoLocations": presence(geo_locations),
        "identifiers": presence(identifiers),
        "language": meta.get("language", None),
        "license": presence(license_),
        "provider": "DataCite",
        "publisher": publisher,
        "references": presence(references),
        "relations": presence(relations),
        "subjects": presence(subjects),
        "titles": presence(titles),
        "url": normalize_url(meta.get("url", None)),
        "version": meta.get("version", None),
    } | read_options


def get_identifiers(identifiers: list) -> list:
    """get_identifiers"""

    def is_identifier(identifier):
        """supported identifier types"""
        return identifier.get("identifierType", None) in [
            "ARK",
            "arXiv",
            "Bibcode",
            "DOI",
            "Handle",
            "ISBN",
            "ISSN",
            "PMID",
            "PMCID",
            "PURL",
            "URL",
            "URN",
            "Other",
        ]

    def format_identifier(identifier):
        """format_identifier"""
        if is_identifier(identifier):
            type_ = identifier.get("identifierType")
        else:
            type_ = "Other"

        return compact(
            {
                "identifier": identifier.get("alternateIdentifier", None),
                "identifierType": type_,
            }
        )

    return [format_identifier(i) for i in wrap(identifiers)]


def get_references(references: list) -> list:
    """get_references"""

    def is_reference(reference):
        """is_reference"""
        return reference.get("relationType", None) in ["Cites", "References"]

    def map_reference(reference, index):
        """map_reference"""
        identifier = reference.get("relatedIdentifier", None)
        identifier_type = reference.get("relatedIdentifierType", None)
        if identifier_type == "DOI":
            id_ = normalize_doi(identifier)
        elif identifier_type == "URL":
            id_ = normalize_url(identifier)
        else:
            id_ = identifier
        return compact(
            {
                "key": f"ref{index + 1}",
                "id": id_,
            }
        )

    return [
        map_reference(i, index) for index, i in enumerate(references) if is_reference(i)
    ]


def get_relations(relations: list) -> list:
    """get_relations"""

    def is_relation(relation):
        """relation"""
        return relation.get("relationType", None) in [
            "IsNewVersionOf",
            "IsPreviousVersionOf",
            "IsVersionOf",
            "HasVersion",
            "IsPartOf",
            "HasPart",
            "IsVariantFormOf",
            "IsOriginalFormOf",
            "IsIdenticalTo",
            "IsTranslationOf",
            "IsReviewedBy",
            "Reviews",
            "IsPreprintOf",
            "HasPreprint",
            "IsSupplementTo",
        ]

    def map_relation(relation):
        """map_relation"""

        identifier = normalize_doi(
            relation.get("relatedIdentifier", None)
        ) or relation.get("relatedIdentifier", None)
        relation_type = relation.get("relationType", None)
        return compact(
            {
                "id": identifier,
                "type": relation_type,
            }
        )

    return [map_relation(i) for i in relations if is_relation(i)]


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

    def map_description(description):
        """map_description"""
        return compact(
            {
                "description": description.get("description", None),
                "type": description.get("descriptionType")
                if description.get("descriptionType", None)
                in ["Abstract", "Methods", "TechnicalInfo", "Other"]
                else "Other",
                "language": description.get("lang", None),
            }
        )

    return [
        map_description(i)
        for i in descriptions
        if i.get("description", None) is not None
    ]


def get_titles(titles: list) -> list:
    """get_titles"""

    def map_title(title):
        """map_title"""
        return compact(
            {
                "title": title.get("title", None),
                "type": title.get("titleType")
                if title.get("titleType", None)
                in ["AlternativeTitle", "Subtitle", "TranslatedTitle"]
                else None,
                "language": title.get("lang", None),
            }
        )

    return [map_title(i) for i in titles if i.get("title", None) is not None]


def get_publisher(publisher: dict) -> dict:
    """get_publisher"""
    return compact(
        {"id": format_name_identifier(publisher), "name": publisher.get("name", None)}
    )


def get_geolocation(geolocations: list) -> list:
    """get_geolocation"""

    def geo_location_point(point: dict):
        """geo_location_point, convert lat and long to int"""
        return {
            "pointLatitude": float(point.get("pointLatitude"))
            if point.get("pointLatitude", None)
            else None,
            "pointLongitude": float(point.get("pointLongitude"))
            if point.get("pointLongitude", None)
            else None,
        }

    def geo_location_box(box: dict):
        """geo_location_box, convert lat and long to int"""
        return {
            "eastBoundLongitude": float(box.get("eastBoundLongitude"))
            if box.get("eastBoundLongitude", None)
            else None,
            "northBoundLatitude": float(box.get("northBoundLatitude"))
            if box.get("northBoundLatitude", None)
            else None,
            "southBoundLatitude": float(box.get("southBoundLatitude"))
            if box.get("southBoundLatitude", None)
            else None,
            "westBoundLongitude": float(box.get("westBoundLongitude"))
            if box.get("westBoundLongitude", None)
            else None,
        }

    return [
        compact(
            {
                "geoLocationPoint": geo_location_point(location.get("geoLocationPoint"))
                if location.get("geoLocationPoint", None)
                else None,
                "geoLocationBox": geo_location_box(location.get("geoLocationBox"))
                if location.get("geoLocationBox", None)
                else None,
                "geoLocationPlace": location.get("geoLocationPlace", None),
            }
        )
        for location in geolocations
    ]


def get_container(container: Optional[dict]) -> dict or None:
    """get_container"""
    if container is None:
        return None
    _type = (
        DC_TO_CM_CONTAINER_TRANSLATIONS.get(container.get("type"), None)
        if container.get("type", None)
        else None
    )

    return compact(
        {
            "id": container.get("identifier", None),
            "type": _type,
            "title": container.get("title", None),
        }
    )


def get_random_datacite_id(number: int = 1) -> list:
    """Get random DOI from DataCite"""
    number = 20 if number > 20 else number
    url = datacite_api_sample_url(number)
    try:
        response = httpx.get(url, timeout=60)
        if response.status_code != 200:
            return []

        items = py_.get(response.json(), "data")
        return [i.get("id") for i in items]
    except httpx.ReadTimeout:
        return []
