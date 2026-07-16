# pylint: disable=invalid-name
"""Test ror reader"""

# The ROR fixtures ship with the commonmeta-schema package (shared with
# commonmeta-rs); the golden commonmeta output for each is asserted by the
# conformance harness in test-conformance.py. These tests cover the reader's
# own mapping rules and edge cases.
from conformance_common import fixture_path, read_text

from commonmeta import Metadata
from commonmeta.readers.ror_reader import read_ror


def test_nsf():
    """ROR record for the U.S. National Science Foundation"""
    subject = Metadata(read_text(fixture_path("ror", "ror_nsf.json")), via="ror")
    assert subject.is_valid
    assert subject.entity_type == "organization"
    assert subject.id == "https://ror.org/021nxhr62"
    assert subject.name == "U.S. National Science Foundation"
    assert subject.acronym == "NSF"
    assert subject.additional_names == [
        "National Science Foundation",
        "United States National Science Foundation",
    ]
    assert subject.types == ["funder", "government"]
    assert subject.status == "active"
    assert subject.established == 1950
    assert subject.country == "US"
    assert subject.date_updated == "2026-06-02"
    assert subject.asserted_by == "ROR"


def test_cambridge_university():
    """ROR record for the University of Cambridge"""
    subject = Metadata(
        read_text(fixture_path("ror", "ror_cambridge_university.json")), via="ror"
    )
    assert subject.is_valid
    assert subject.entity_type == "organization"
    assert subject.id == "https://ror.org/013meh722"
    assert subject.name == "University of Cambridge"
    assert subject.types == ["education", "funder"]
    assert subject.country == "GB"


def test_identifiers():
    """external_ids map to commonmeta identifiers, preferring `preferred`"""
    subject = Metadata(read_text(fixture_path("ror", "ror_nsf.json")), via="ror")
    assert subject.identifiers == [
        # `preferred` wins over the three ids in `all`
        {"identifier": "100000001", "identifier_type": "FundRef"},
        {"identifier": "grid.431093.c", "identifier_type": "GRID"},
        # `preferred` is null here, so the first of `all` is used
        {"identifier": "0000 0001 1958 7073", "identifier_type": "ISNI"},
        {"identifier": "Q304878", "identifier_type": "Wikidata"},
    ]


def test_relations():
    """ROR relationships map from the perspective of the related organization"""
    subject = Metadata(read_text(fixture_path("ror", "ror_nsf.json")), via="ror")
    by_type = {}
    for relation in subject.relations:
        by_type.setdefault(relation["type"], []).append(relation)

    # a ROR "child" names an organization this one contains
    assert by_type["HasPart"][0] == {
        "id": "https://ror.org/02a0fwv66",
        "type": "HasPart",
        "name": "American Institute of Mathematics",
    }
    assert by_type["IsPartOf"] == [
        {
            "id": "https://ror.org/02rcrvv70",
            "type": "IsPartOf",
            "name": "Government of the United States of America",
        }
    ]
    assert by_type["IsRelatedTo"] == [
        {
            "id": "https://ror.org/043trmd87",
            "type": "IsRelatedTo",
            "name": "Center for Hierarchical Manufacturing",
        }
    ]


def test_geo_locations():
    """locations map to geo_locations with a GeoNames id and a composed place"""
    subject = Metadata(read_text(fixture_path("ror", "ror_nsf.json")), via="ror")
    assert subject.geo_locations == [
        {
            "id": "https://www.geonames.org/4744091",
            "place": "Alexandria, Virginia, United States",
            "point_latitude": 38.80484,
            "point_longitude": -77.04692,
        }
    ]


def test_place_omits_repeated_subdivision():
    """A city named after its subdivision isn't repeated in `place`"""
    meta = read_ror(
        {
            "id": "https://ror.org/013meh722",
            "locations": [
                {
                    "geonames_id": 1,
                    "geonames_details": {
                        "name": "Singapore",
                        "country_subdivision_name": "Singapore",
                        "country_name": "Singapore",
                        "country_code": "SG",
                        "lat": 1.28967,
                        "lng": 103.85007,
                    },
                }
            ],
        }
    )
    assert meta["geo_locations"][0]["place"] == "Singapore, Singapore"


def test_location_without_coordinates_dropped():
    """ROR sends 0/0 for unresolved coordinates; that isn't a real location"""
    meta = read_ror(
        {
            "id": "https://ror.org/013meh722",
            "locations": [
                {
                    "geonames_id": 1,
                    "geonames_details": {
                        "name": "Nowhere",
                        "country_name": "Nowhereland",
                        "country_code": "NL",
                        "lat": 0,
                        "lng": 0,
                    },
                }
            ],
        }
    )
    assert "geo_locations" not in meta
    # the country still comes from the first location
    assert meta["country"] == "NL"


def test_unmapped_external_id_dropped():
    """An external id type with no commonmeta equivalent is dropped"""
    meta = read_ror(
        {
            "id": "https://ror.org/013meh722",
            "external_ids": [
                {"type": "orgref", "all": ["12345"], "preferred": "12345"},
                {"type": "wikidata", "all": ["Q35794"], "preferred": None},
            ],
        }
    )
    assert meta["identifiers"] == [
        {"identifier": "Q35794", "identifier_type": "Wikidata"}
    ]


def test_not_found():
    """a record without a ROR id"""
    assert read_ror(None) == {"state": "not_found"}
