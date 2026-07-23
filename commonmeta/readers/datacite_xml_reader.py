"""datacite_xml reader for Commonmeta"""

from __future__ import annotations

from collections import defaultdict

import requests

from ..author_utils import get_authors
from ..base_utils import (
    compact,
    dig,
    first,
    omit,
    parse_attributes,
    presence,
    sanitize,
    wrap,
)
from ..constants import (
    DC_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..date_utils import normalize_date_dict, strip_milliseconds
from ..doi_utils import datacite_api_url, doi_as_url, doi_from_url, normalize_doi
from ..readers.datacite_reader import DC_TO_CM_RELATION_TYPES
from ..utils import (
    dedupe_subjects,
    dict_to_spdx,
    normalize_arxiv,
    normalize_cc_url,
    normalize_url,
)


def get_datacite_xml(pid: str, **kwargs) -> dict:
    """get_datacite_xml"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = datacite_api_url(doi)
    response = requests.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return {**dig(response.json(), "data.attributes", {}), "via": "datacite_xml"}


def read_datacite_xml(data: dict, **kwargs) -> Commonmeta:
    """read_datacite_xml"""
    if data is None:
        return {"state": "not_found"}

    read_options = kwargs or {}

    meta = data.get("resource", {})

    doi = first(parse_attributes(meta.get("identifier", None)))
    _id = doi_as_url(doi) if doi else None

    resource__typegeneral = dig(meta, "resourceType.resourceTypeGeneral")
    _type = DC_TO_CM_TRANSLATIONS.get(resource__typegeneral, "Other")
    additional_type = dig(meta, "resourceType.#text")
    # Drop additional_type when it is redundant with the resolved type: it
    # maps to a known CM type or just repeats the type (e.g. resourceType
    # "dataset" under a Dataset).
    if additional_type and (
        DC_TO_CM_TRANSLATIONS.get(additional_type, None)
        or additional_type.lower() == _type.lower()
        or additional_type.startswith("info:")
    ):
        additional_type = None

    identifiers = wrap(dig(meta, "alternateIdentifiers.alternateIdentifier"))
    identifiers = get_xml_identifiers(identifiers)
    # DataCite stores the DOI as the primary <identifier>; include it as a
    # DOI identifier unless already present.
    if _id and not any(i.get("identifier", None) == _id for i in identifiers):
        identifiers = identifiers + [{"identifier": _id, "identifier_type": "DOI"}]

    title, additional_titles = get_titles(wrap(dig(meta, "titles.title")))

    contributors = get_authors(wrap(dig(meta, "creators.creator")))
    contrib = get_authors(wrap(dig(meta, "contributors.contributor")))
    if contrib:
        contributors = contributors + contrib

    publisher = {"name": first(parse_attributes(meta.get("publisher", None)))}
    date_published, date_updated, dates = get_dates(
        wrap(dig(meta, "dates.date")), meta.get("publicationYear", None)
    )
    # "created"/"registered" are DataCite admin timestamps for the DOI
    # record itself, found alongside "resource" in the API response, not
    # inside it.
    dates = dates or {}
    dates.setdefault("created", strip_milliseconds(data.get("created", None)))
    dates["registered"] = strip_milliseconds(data.get("registered", None))
    dates = presence(compact(dates))

    description, additional_descriptions = get_descriptions(
        wrap(dig(meta, "descriptions.description"))
    )

    def format_subject(subject):
        """format_subject"""
        if isinstance(subject, str):
            return {"subject": subject}
        if isinstance(subject, dict):
            return compact(
                {
                    "subject": subject.get("#text", None),
                    "scheme": subject.get("subjectScheme", None),
                    # DataCite XML spells this schemeURI; the JSON API uses schemeUri.
                    "scheme_uri": subject.get("schemeURI", None),
                    "language": subject.get("xml:lang", None),
                }
            )
        return None

    subjects = dedupe_subjects(
        [format_subject(i) for i in wrap(dig(meta, "subjects.subject")) if i]
    )

    geo_locations = get_geolocation(wrap(dig(meta, "geoLocations.geoLocation")))

    def map_rights(rights):
        """map_rights"""
        return compact(
            {
                "rights": rights.get("#text", None),
                "url": rights.get("rightsURI", None),
                "lang": rights.get("xml:lang", None),
            }
        )

    license_ = wrap(dig(meta, "rightsList.rights"))
    if len(license_) > 0:
        license_ = normalize_cc_url(license_[0].get("rightsURI", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    references = get_xml_references(
        wrap(dig(meta, "relatedIdentifiers.relatedIdentifier"))
    )
    relations = get_xml_relations(
        wrap(dig(meta, "relatedIdentifiers.relatedIdentifier"))
    )

    funding_references = get_funding_references(
        wrap(dig(meta, "fundingReferences.fundingReference"))
    )

    container = get_container(dig(meta, "relatedItems.relatedItem"))
    if _type == "BlogPost":
        # a blog post has no additional_type and its container is a Blog
        additional_type = None
        if container:
            container = {**container, "type": "Blog"}

    files = meta.get("contentUrl", None)
    state = "findable" if _id or read_options else "not_found"

    return {
        **{
            # required properties
            "id": _id,
            "type": _type,
            # recommended and optional properties
            "additional_descriptions": presence(additional_descriptions),
            "additional_titles": presence(additional_titles),
            "additional_type": presence(additional_type),
            "container": presence(container),
            "contributors": presence(contributors),
            "date_published": presence(date_published),
            "date_updated": presence(date_updated),
            "dates": dates,
            "description": description,
            "files": presence(files),
            "funding_references": presence(funding_references),
            "geo_locations": presence(geo_locations),
            "identifiers": identifiers,
            "language": meta.get("language", None),
            "license": presence(license_),
            "provider": "DataCite",
            "publisher": publisher,
            "references": presence(references),
            "relations": presence(relations),
            "schema_version": meta.get("xmlns", None),
            "state": state,
            "subjects": presence(subjects),
            "title": title,
            "url": normalize_url(meta.get("url", None)),
            "version": meta.get("version", None),
        },
        **read_options,
    }


def get_xml_identifiers(identifiers: list) -> list:
    """get_identifiers"""

    def is_identifier(identifier):
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

    def format_identifier(identifier):
        """format_identifier"""

        if is_identifier(identifier):
            type_ = identifier.get("alternateIdentifierType")
        else:
            type_ = "Other"

        return compact(
            {
                "identifier": identifier.get("#text", None),
                "identifier_type": type_,
            }
        )

    return [format_identifier(i) for i in identifiers]


def get_xml_references(references: list) -> list:
    """get_xml_references"""

    def is_reference(reference):
        """is_reference"""
        return reference.get("relationType", None) in [
            "Cites",
            "References",
        ] and reference.get("relatedIdentifierType", None) in ["DOI", "URL"]

    def map_reference(reference):
        """map_reference"""
        identifier = reference.get("relatedIdentifier", None)
        identifier_type = reference.get("relatedIdentifierType", None)
        if identifier and identifier_type == "DOI":
            reference["doi"] = normalize_doi(identifier)
        elif identifier and identifier_type == "URL":
            reference["url"] = normalize_url(identifier)
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


def get_container(related_items: list) -> dict | None:
    """Build a container from a DataCite relatedItem (relationType
    ``IsPublishedIn``), e.g. the journal a work was published in."""
    item = next(
        (
            i
            for i in wrap(related_items)
            if isinstance(i, dict) and i.get("relationType", None) == "IsPublishedIn"
        ),
        None,
    )
    if item is None:
        return None
    rii = item.get("relatedItemIdentifier", None)
    if isinstance(rii, dict):
        identifier = rii.get("#text", None)
        identifier_type = rii.get("relatedItemIdentifierType", None)
    else:
        identifier = rii
        identifier_type = None
    return compact(
        {
            "type": item.get("relatedItemType", None),
            "identifiers": (
                [
                    compact(
                        {"identifier": identifier, "identifier_type": identifier_type}
                    )
                ]
                if identifier
                else None
            ),
            "title": dig(item, "titles.title"),
            "volume": item.get("volume", None),
            "issue": item.get("issue", None),
            "first_page": item.get("firstPage", None),
            "last_page": item.get("lastPage", None),
        }
    )


def get_xml_relations(relations: list) -> list:
    """get_xml_relations"""

    def is_relation(relation):
        """is_relation"""
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

    def map_relation(relation):
        """map_relation"""
        # the identifier value is the element text (#text) when the element
        # carries attributes (relatedIdentifierType, relationType, ...).
        identifier = relation.get("relatedIdentifier", None) or relation.get(
            "#text", None
        )
        identifier_type = relation.get("relatedIdentifierType", None)
        if identifier and identifier_type == "DOI":
            _id = normalize_doi(identifier)
        elif identifier and identifier_type == "arXiv":
            _id = normalize_arxiv(identifier)
        elif identifier and identifier_type == "URL":
            _id = normalize_url(identifier)
        else:
            _id = identifier
        relation_type = relation.get("relationType", None)
        relation_type = DC_TO_CM_RELATION_TYPES.get(relation_type, relation_type)
        return compact(
            {
                "id": _id,
                "type": relation_type,
            }
        )

    return [map_relation(i) for i in relations if is_relation(i)]


def get_dates(
    dates: list, publication_year
) -> tuple[str | None, str | None, dict | None]:
    """convert date list to (date_published, date_updated, dates) per v1.0"""
    date: dict = defaultdict(list)
    for sub in dates:
        date[sub.get("dateType", None)] = sub.get("#text", None)
    if date.get("Issued", None) is None and publication_year is not None:
        date["Issued"] = str(publication_year)
    normalized = normalize_date_dict(date)
    date_published = normalized.pop("published", None)
    date_updated = normalized.pop("updated", None)
    return date_published, date_updated, presence(normalized)


def get_titles(titles: list) -> tuple[str | None, list]:
    """get_titles

    Returns a tuple of (title, additional_titles) per the commonmeta v1.0
    schema, where title is a single scalar string.
    """

    def map_title(title) -> dict | None:
        """map_title"""
        if isinstance(title, str):
            return {"title": title}
        if isinstance(title, dict):
            return compact(
                {
                    "title": title.get("#text", None),
                    "type": (
                        title.get("titleType")
                        if title.get("titleType", None)
                        in ["AlternativeTitle", "Subtitle", "TranslatedTitle"]
                        else None
                    ),
                    "language": title.get("xml:lang", None),
                }
            )
        return None

    items = [map_title(i) for i in titles]
    items = [i for i in items if i and i.get("title", None) is not None]
    if not items:
        return None, []
    title = items[0].get("title", None)
    return title, items[1:]


def get_descriptions(descriptions: list) -> tuple[str | None, list]:
    """get_descriptions

    Returns a tuple of (description, additional_descriptions) per the
    commonmeta v1.0 schema, where description is a single scalar string.
    """

    def map_description(description) -> dict | None:
        """map_description"""
        if isinstance(description, str):
            return {"description": description, "type": "Abstract"}
        if isinstance(description, dict):
            type_ = description.get("descriptionType", "Abstract")
            if type_ not in [
                "Abstract",
                "Summary",
                "Methods",
                "TechnicalInfo",
                "Other",
            ]:
                type_ = "Other"
            return compact(
                {
                    "description": sanitize(description.get("#text", None)),
                    "type": type_,
                    "language": description.get("xml:lang", None),
                }
            )
        return None

    items = [map_description(i) for i in descriptions]
    items = [i for i in items if i and i.get("description", None) is not None]
    if not items:
        return None, []
    description = items[0].get("description", None)
    return description, items[1:]


def get_funding_references(funding_references: list) -> list:
    """get_funding_references

    DataCite funding references use funderIdentifier/funderIdentifierType,
    which may be ROR, Crossref Funder ID, GRID, ISNI, Ringgold, or Other.
    ROR ids are kept as-is and Crossref Funder IDs as DOIs; other schemes have
    no resolvable id and are dropped.
    """

    def map_funding_reference(funding: dict) -> dict:
        funder_identifier_node = funding.get("funderIdentifier", None)
        if isinstance(funder_identifier_node, dict):
            funder_identifier = funder_identifier_node.get("#text", None)
            funder_identifier_type = funder_identifier_node.get(
                "funderIdentifierType", None
            )
        elif isinstance(funder_identifier_node, str):
            funder_identifier = funder_identifier_node
            funder_identifier_type = None
        else:
            funder_identifier = None
            funder_identifier_type = None

        funder_id = None
        if funder_identifier_type == "ROR":
            funder_id = funder_identifier
        elif funder_identifier_type == "Crossref Funder ID":
            funder_id = normalize_doi(funder_identifier)
        # GRID/ISNI/Ringgold/Other/None have no resolvable id: funder_id
        # stays None rather than leaking a non-DOI/ROR identifier.

        award_number_node = funding.get("awardNumber", None)
        if isinstance(award_number_node, dict):
            award_number = award_number_node.get("#text", None)
            award_id = award_number_node.get("awardURI", None)
        elif isinstance(award_number_node, str):
            award_number = award_number_node
            award_id = None
        else:
            award_number = None
            award_id = None

        return compact(
            {
                "funder_id": funder_id,
                "funder_name": funding.get("funderName", None),
                "award_id": award_id,
                "award_title": funding.get("awardTitle", None),
                "award_number": award_number,
            }
        )

    return [map_funding_reference(i) for i in funding_references]


def get_geolocation(geolocations: list) -> list:
    """get_geolocation

    Returns flat v1.0-shaped geo_locations (place,
    point_longitude/point_latitude, box_*_longitude/box_*_latitude,
    polygon as WKT) instead of the nested geoLocationPoint/Box/Polygon shape.
    """

    def point_value(point, key: str) -> float | None:
        if not isinstance(point, dict):
            return None
        value = point.get(key, None)
        return float(value) if value else None

    def box_value(box, key: str) -> float | None:
        if not isinstance(box, dict):
            return None
        value = box.get(key, None)
        return float(value) if value else None

    def polygon_to_wkt(polygon) -> str | None:
        points = wrap(dig(polygon, "polygonPoint"))
        coords = [
            f"{p.get('pointLongitude')} {p.get('pointLatitude')}"
            for p in points
            if p.get("pointLongitude", None) is not None
            and p.get("pointLatitude", None) is not None
        ]
        if not coords:
            return None
        return f"POLYGON(({', '.join(coords)}))"

    def map_geolocation(location) -> dict | None:
        if isinstance(location, str):
            return {"place": location}
        if not isinstance(location, dict):
            return None
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

    items = [map_geolocation(location) for location in geolocations]
    return [i for i in items if i]


def get_random_datacite_id(number: int = 1) -> list:
    """Get random DOI from DataCite. Kept for backwards compatibility,
    re-exported from datacite_reader."""
    from .datacite_reader import get_random_datacite_id as _get_random_datacite_id

    return _get_random_datacite_id(number)
