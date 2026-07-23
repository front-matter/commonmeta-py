"""datacite reader for Commonmeta"""

from __future__ import annotations

from collections import defaultdict

import requests
from requests.exceptions import ReadTimeout

from ..author_utils import get_authors
from ..base_utils import compact, dig, presence, wrap
from ..constants import (
    CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS,
    CSL_TO_CM_TRANSLATIONS,
    DC_RESOURCE_TYPE_TO_CM,
    DC_TO_CM_CONTAINER_TRANSLATIONS,
    DC_TO_CM_TRANSLATIONS,
    SO_TO_CM_TRANSLATIONS,
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
    dedupe_subjects,
    dict_to_spdx,
    format_name_identifier,
    normalize_cc_url,
    normalize_doi,
    normalize_url,
)

# DataCite client id → OpenAlex source id, for the container a work inherits from
# its registering client (rc25). Mirrors commonmeta-rs' DATACITE_OPENALEX_SOURCES.
DATACITE_CLIENT_TO_OPENALEX_SOURCES = {
    "cern.zenodo": "https://openalex.org/S4306400562",
}


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
        body = response.json()
        # Carry the registering DataCite client id (from relationships, outside
        # attributes) alongside the attributes: rc25 uses it as the container.
        return {
            **dig(body, "data.attributes", {}),
            "client": dig(body, "data.relationships.client.data.id", None),
            "via": "datacite",
        }
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
    # resourceType refines/overrides resourceTypeGeneral when it maps to a
    # commonmeta type: first the standard DataCite map (schema 4.3+ subtypes),
    # then the free-text subtype map (e.g. "blogpost" -> "BlogPost"). When it
    # resolves, additional_type is left unset.
    additional_type = DC_TO_CM_TRANSLATIONS.get(resource_type, None)
    rt_additional = DC_RESOURCE_TYPE_TO_CM.get(
        resource_type.lower() if isinstance(resource_type, str) else ""
    )
    if additional_type:
        _type = additional_type
        additional_type = None
    elif rt_additional:
        _type = rt_additional
        additional_type = None
    else:
        # resourceTypeGeneral "Text" is a coarse catch-all; when resourceType
        # did not resolve, refine the type via the citeproc or schema.org hints.
        refined = None
        if resource__typegeneral == "Text":
            refined = CSL_TO_CM_TRANSLATIONS.get(
                dig(meta, "types.citeproc"), None
            ) or SO_TO_CM_TRANSLATIONS.get(dig(meta, "types.schemaOrg"), None)
        if refined:
            _type = refined
            additional_type = None
        elif (
            isinstance(resource_type, str)
            and resource_type
            and resource_type.lower() != _type.lower()
            and not resource_type.startswith("info:")
        ):
            # keep resourceType as additional_type only when it adds information
            additional_type = resource_type
        else:
            additional_type = None
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
    # rc25: the container identifier is an IsPartOf DOI (e.g. a proceedings or
    # book the work is part of), else the registering DataCite client (a
    # repository) — mapped to an OpenAlex source when known, else kept as a
    # DataCite identifier. The attributes.container identifier itself is never
    # used; only its title/type/volume/pages carry over.
    part_of_doi = next(
        (
            doi
            for r in wrap(meta.get("relatedIdentifiers", None))
            if r.get("relationType") == "IsPartOf"
            and (r.get("relatedIdentifierType") or "").upper() == "DOI"
            and (doi := normalize_doi(r.get("relatedIdentifier")))
        ),
        None,
    )
    if part_of_doi:
        container_id, container_id_type = part_of_doi, "DOI"
    else:
        client_id = meta.get("client", None)
        openalex = (
            DATACITE_CLIENT_TO_OPENALEX_SOURCES.get(client_id) if client_id else None
        )
        if openalex:
            container_id, container_id_type = openalex, "OpenAlex"
        elif client_id:
            container_id, container_id_type = client_id, "DataCite"
        else:
            container_id, container_id_type = None, None
    if container_id:
        container = {
            **(container or {}),
            "identifiers": (
                [{"identifier": container_id, "identifier_type": container_id_type}]
                if container_id
                else None
            ),
        }
    if _type == "BlogPost":
        # a blog post has no additional_type; a *named* container (with a title)
        # is a Blog. A bare identifier-only container (an IsPartOf DOI or the
        # registering client) carries no type.
        additional_type = None
        if container and container.get("title"):
            container = {**container, "type": "Blog"}
    license_ = meta.get("rightsList", [])
    if len(license_) > 0:
        license_ = normalize_cc_url(license_[0].get("rightsUri", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    files = [get_file(i) for i in wrap(meta.get("content_url"))]

    # The DOI is the primary id; it is not duplicated into identifiers.
    identifiers = get_identifiers(wrap(meta.get("alternateIdentifiers", None)))

    references = get_references(
        wrap(meta.get("relatedItems", None) or meta.get("relatedIdentifiers", None))
    )
    relations = get_relations(wrap(meta.get("relatedIdentifiers", None)))
    # the IsPartOf DOI promoted to the container is not duplicated as a relation.
    if part_of_doi:
        relations = [r for r in relations if r.get("id") != part_of_doi]
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
                "scheme": subject.get("subjectScheme", None),
                "scheme_uri": subject.get("schemeUri", None),
            }
        )

    subjects = dedupe_subjects(
        [format_subject(i) for i in wrap(meta.get("subjects", None))]
    )
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
        return identifier.get("alternateIdentifierType", None) in [
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
            type_ = identifier.get("alternateIdentifierType")
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

    def map_reference(reference) -> dict:
        """map_reference"""
        identifier = reference.get("relatedIdentifier", None)
        identifier_type = reference.get("relatedIdentifierType", None)
        if identifier_type == "DOI":
            id_ = normalize_doi(identifier)
        elif identifier_type == "URL":
            id_ = normalize_url(identifier)
        else:
            id_ = identifier
        ref_type = DC_TO_CM_TRANSLATIONS.get(
            reference.get("resourceTypeGeneral", None), None
        )
        return compact({"id": id_, "type": ref_type})

    return [map_reference(i) for i in references if is_reference(i)]


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

    def map_relation(relation) -> dict | None:
        """map_relation"""
        related = relation.get("relatedIdentifier", None)
        id_type = (relation.get("relatedIdentifierType") or "").upper()
        # ISBNs are expanded to a urn:isbn: URN so they aren't dropped; ISSNs
        # (the periodical, already captured by the container) and anything else
        # that doesn't normalize to a resolvable id are dropped.
        if id_type == "ISBN":
            isbn = "".join(c for c in (related or "") if c.isalnum())
            identifier = f"urn:isbn:{isbn}" if isbn else None
        else:
            identifier = normalize_doi(related) or normalize_url(related)
        if identifier is None:
            return None
        relation_type = relation.get("relationType", None)
        relation_type = DC_TO_CM_RELATION_TYPES.get(relation_type, relation_type)
        return compact(
            {
                "id": identifier,
                "type": relation_type,
            }
        )

    return [
        r
        for r in (map_relation(i) for i in relations if is_relation(i))
        if r is not None
    ]


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

    # rc25: the attributes.container identifier is never used; the container
    # identifier is set from an IsPartOf DOI or the DataCite client in the
    # caller. Only the title/type/volume/pages carry over here.
    return compact(
        {
            "type": _type,
            "title": container.get("title", None),
            "volume": container.get("volume", None),
            "issue": container.get("issue", None),
            "first_page": container.get("firstPage", None),
            "last_page": container.get("lastPage", None),
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
