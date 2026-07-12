"""datacite reader for Commonmeta"""

from __future__ import annotations

from collections import defaultdict

import requests
from requests.exceptions import ReadTimeout

from ..author_utils import get_authors
from ..base_utils import compact, dig, presence, unique, wrap
from ..constants import (
    CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS,
    DC_TO_CM_CONTAINER_TRANSLATIONS,
    DC_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..date_utils import normalize_date_dict
from ..doi_utils import (
    datacite_api_sample_url,
    datacite_api_url,
    doi_as_url,
    doi_from_url,
)
from ..utils import (
    dict_to_spdx,
    format_name_identifier,
    normalize_cc_url,
    normalize_doi,
    normalize_url,
)


def get_datacite(pid: str | None, **kwargs) -> dict:
    """get_datacite"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = datacite_api_url(doi)
    try:
        response = requests.get(url, timeout=10, **kwargs)
        if response.status_code != 200:
            return {"state": "not_found"}
        return {**dig(response.json(), "data.attributes", {}), "via": "datacite"}
    except ReadTimeout:
        return {"state": "timeout"}


def read_datacite(data: dict, **kwargs) -> Commonmeta:
    """read_datacite"""
    meta = data
    if data is None:
        return {"state": "not_found"}

    read_options = kwargs or {}

    _id = doi_as_url(meta.get("doi", None))
    resource__typegeneral = dig(meta, "types.resourceTypeGeneral")
    resource_type = dig(meta, "types.resourceType")
    _type = DC_TO_CM_TRANSLATIONS.get(resource__typegeneral, "Other")
    additional_type = DC_TO_CM_TRANSLATIONS.get(resource_type, None)
    # if resource_type is one of the new resource__typegeneral types introduced in schema 4.3, use it
    if additional_type:
        _type = additional_type
        additional_type = None
    else:
        additional_type = resource_type
    title, additional_titles = get_titles(wrap(meta.get("titles", None)))

    contributors = get_authors(wrap(meta.get("creators", None)))
    contrib = get_authors(wrap(meta.get("contributors", None)))
    if contrib:
        contributors = contributors + contrib

    publisher = meta.get("publisher", None)
    if isinstance(publisher, str):
        publisher = {"name": publisher}
    elif isinstance(publisher, dict):
        publisher = get_publisher(publisher)
    date_published, date_updated, dates = get_dates(
        wrap(meta.get("dates", None)), meta.get("publicationYear", None)
    )
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
                "identifier_type": "DOI",
            }
        )
    )

    references = get_references(
        wrap(meta.get("relatedItems", None) or meta.get("relatedIdentifiers", None))
    )
    relations = get_relations(wrap(meta.get("relatedIdentifiers", None)))
    description, additional_descriptions = get_descriptions(
        wrap(meta.get("descriptions", None))
    )
    geo_locations = get_geolocation(wrap(meta.get("geoLocations", None)))
    funding_references = get_funding_references(
        wrap(meta.get("fundingReferences", None))
    )

    def format_subject(subject) -> dict:
        """format_subject"""
        return compact(
            {
                "id": subject.get("valueURI", None),
                "subject": subject.get("subject", None),
                "language": subject.get("lang", None),
            }
        )

    subjects = unique([format_subject(i) for i in wrap(meta.get("subjects", None))])
    state = "findable"

    return {
        **{
            # required properties
            "id": _id,
            "type": _type,
            # recommended and optional properties
            "additional_descriptions": presence(additional_descriptions),
            "additional_titles": presence(additional_titles),
            "additional_type": additional_type,
            "container": presence(container),
            "contributors": presence(contributors),
            "date_published": presence(date_published),
            "date_updated": presence(date_updated),
            "dates": dates,
            "description": description,
            "files": presence(files),
            "funding_references": presence(funding_references),
            "geo_locations": presence(geo_locations),
            "identifiers": presence(identifiers),
            "language": meta.get("language", None),
            "license": presence(license_),
            "provider": "DataCite",
            "publisher": publisher,
            "references": presence(references),
            "relations": presence(relations),
            "state": state,
            "subjects": presence(subjects),
            "title": title,
            "url": normalize_url(meta.get("url", None)),
            "version": meta.get("version", None),
        },
        **read_options,
    }


def get_identifiers(identifiers: list) -> list:
    """get_identifiers"""

    def is_identifier(identifier) -> bool:
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

    def format_identifier(identifier) -> dict:
        """format_identifier"""
        if is_identifier(identifier):
            type_ = identifier.get("identifierType")
        else:
            type_ = "Other"

        return compact(
            {
                "identifier": identifier.get("alternateIdentifier", None),
                "identifier_type": type_,
            }
        )

    return [format_identifier(i) for i in wrap(identifiers)]


def get_references(references: list) -> list:
    """get_references"""

    def is_reference(reference) -> bool:
        """is_reference"""
        return reference.get("relationType", None) in ["Cites", "References"]

    def map_reference(reference, index) -> dict:
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


# DataCite relationType → commonmeta relation type. Types not listed pass
# through unchanged.
DC_TO_CM_RELATION_TYPES = {
    "IsCitedBy": "IsReferencedBy",
    "Reviews": "IsReviewOf",
    "IsReviewedBy": "HasReview",
}


def get_relations(relations: list) -> list:
    """get_relations"""

    def is_relation(relation) -> bool:
        """relation"""
        return relation.get("relationType", None) in [
            "IsCitedBy",
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

    def map_relation(relation) -> dict:
        """map_relation"""

        identifier = normalize_doi(
            relation.get("relatedIdentifier", None)
        ) or relation.get("relatedIdentifier", None)
        relation_type = relation.get("relationType", None)
        relation_type = DC_TO_CM_RELATION_TYPES.get(relation_type, relation_type)
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


def get_dates(
    dates: list, publication_year
) -> tuple[str | None, str | None, dict | None]:
    """convert date list to (date_published, date_updated, dates) per v1.0"""
    date: dict = defaultdict(list)
    for sub in dates:
        date[sub.get("dateType", None)] = sub.get("date", None)
    if date.get("Issued", None) is None and publication_year is not None:
        date["Issued"] = str(publication_year)
    normalized = normalize_date_dict(date)
    date_published = normalized.pop("published", None)
    date_updated = normalized.pop("updated", None)
    return date_published, date_updated, presence(normalized)


def get_descriptions(descriptions: list) -> tuple[str | None, list]:
    """get_descriptions

    Returns a tuple of (description, additional_descriptions) per the
    commonmeta v1.0 schema, where description is a single scalar string.
    """

    def map_description(description) -> dict:
        """map_description"""
        type = description.get("descriptionType", None)
        if type is None:
            type = "Abstract"
        elif type not in ["Abstract", "Methods", "TechnicalInfo", "Other"]:
            type = "Other"
        return compact(
            {
                "description": description.get("description", None),
                "type": type,
                "language": description.get("lang", None),
            }
        )

    items = [
        map_description(i)
        for i in descriptions
        if i.get("description", None) is not None
    ]
    if not items:
        return None, []
    description = items[0].get("description", None)
    return description, items[1:]


def get_titles(titles: list) -> tuple[str | None, list]:
    """get_titles

    Returns a tuple of (title, additional_titles) per the commonmeta v1.0
    schema, where title is a single scalar string.
    """

    def map_title(title) -> dict:
        """map_title"""
        return compact(
            {
                "title": title.get("title", None),
                "type": (
                    title.get("titleType")
                    if title.get("titleType", None)
                    in ["AlternativeTitle", "Subtitle", "TranslatedTitle"]
                    else None
                ),
                "language": title.get("lang", None),
            }
        )

    items = [map_title(i) for i in titles if i.get("title", None) is not None]
    if not items:
        return None, []
    title = items[0].get("title", None)
    return title, items[1:]


def get_funding_references(funding_references: list) -> list:
    """get_funding_references

    DataCite funding references use funderIdentifier/funderIdentifierType,
    which may be ROR, Crossref Funder ID, GRID, ISNI, Ringgold, or Other.
    Commonmeta's funder_id is ROR-only, so Crossref Funder ID is translated to ROR
    where possible.
    """

    def map_funding_reference(funding: dict) -> dict:
        funder_identifier = funding.get("funderIdentifier", None)
        funder_identifier_type = funding.get("funderIdentifierType", None)
        funder_id = None
        if funder_identifier_type == "ROR":
            funder_id = funder_identifier
        elif funder_identifier_type == "Crossref Funder ID":
            funder_id = CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS.get(
                funder_identifier, None
            )
        # GRID/ISNI/Ringgold/Other/None have no ROR equivalent: funder_id
        # stays None rather than leaking a non-ROR identifier.

        return compact(
            {
                "funder_id": funder_id,
                "funder_name": funding.get("funderName", None),
                "award_id": funding.get("awardUri", None),
                "award_title": funding.get("awardTitle", None),
                "award_number": funding.get("awardNumber", None),
            }
        )

    return [map_funding_reference(i) for i in funding_references]


def get_publisher(publisher: dict) -> dict:
    """get_publisher"""
    return compact(
        {"id": format_name_identifier(publisher), "name": publisher.get("name", None)}
    )


def get_geolocation(geolocations: list) -> list:
    """get_geolocation

    Returns flat v1.0-shaped geo_locations (place,
    point_longitude/point_latitude, box_*_longitude/box_*_latitude,
    polygon as WKT) instead of the nested geoLocationPoint/Box/Polygon shape.
    """

    def point_value(point: dict, key: str) -> float | None:
        value = point.get(key, None)
        return float(value) if value else None

    def box_value(box: dict, key: str) -> float | None:
        value = box.get(key, None)
        return float(value) if value else None

    def polygon_to_wkt(polygon) -> str | None:
        points = wrap(polygon)
        coords = [
            f"{p.get('pointLongitude')} {p.get('pointLatitude')}"
            for p in points
            if p.get("pointLongitude", None) is not None
            and p.get("pointLatitude", None) is not None
        ]
        if not coords:
            return None
        return f"POLYGON(({', '.join(coords)}))"

    def map_geolocation(location: dict) -> dict:
        point = location.get("geoLocationPoint", None) or {}
        box = location.get("geoLocationBox", None) or {}
        return compact(
            {
                "place": location.get("geoLocationPlace", None),
                "point_longitude": point_value(point, "pointLongitude"),
                "point_latitude": point_value(point, "pointLatitude"),
                "box_west_longitude": box_value(box, "westBoundLongitude"),
                "box_east_longitude": box_value(box, "eastBoundLongitude"),
                "box_south_latitude": box_value(box, "southBoundLatitude"),
                "box_north_latitude": box_value(box, "northBoundLatitude"),
                "polygon": polygon_to_wkt(location.get("geoLocationPolygon", None)),
            }
        )

    return [map_geolocation(location) for location in geolocations]


def get_container(container: dict | None) -> dict | None:
    """get_container"""
    if container is None:
        return None
    _type = (
        DC_TO_CM_CONTAINER_TRANSLATIONS.get(container.get("type"), None)
        if container.get("type", None)
        else None
    )

    container_identifier = container.get("identifier", None)
    return compact(
        {
            "type": _type,
            "title": container.get("title", None),
            "identifier": container_identifier,
            "identifier_type": "URL" if container_identifier else None,
        }
    )


def get_random_datacite_id(number: int = 1) -> list:
    """Get random DOI from DataCite"""
    number = 20 if number > 20 else number
    url = datacite_api_sample_url(number)
    try:
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            return []

        items = dig(response.json(), "data")
        return [i.get("id") for i in items]
    except ReadTimeout:
        return []
