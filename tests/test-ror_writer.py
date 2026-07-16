# pylint: disable=invalid-name
"""Test ror writer"""

import json

import pytest
from conformance_common import diff, fixture_path, read_text

from commonmeta import Metadata


def test_roundtrip_is_identity():
    """ROR -> commonmeta -> ROR -> commonmeta returns the same record.

    The writer can't be checked against the input verbatim: reading ROR into
    commonmeta is lossy by design (see the writer's docstring). What must hold is
    that nothing commonmeta *does* model is lost on the way out.
    """
    for name in ("ror_nsf.json", "ror_cambridge_university.json"):
        raw = read_text(fixture_path("ror", name))
        before = json.loads(Metadata(raw, via="ror").write(to="commonmeta"))
        ror = Metadata(raw, via="ror").write(to="ror")
        after = json.loads(Metadata(ror.decode(), via="ror").write(to="commonmeta"))
        assert not diff(before, after), name


def test_nsf():
    """A ROR record is rebuilt in the API's shape."""
    raw = read_text(fixture_path("ror", "ror_nsf.json"))
    out = json.loads(Metadata(raw, via="ror").write(to="ror"))

    assert out["id"] == "https://ror.org/021nxhr62"
    assert out["status"] == "active"
    assert out["established"] == 1950
    assert out["types"] == ["funder", "government"]
    assert out["admin"] == {
        "last_modified": {"date": "2026-06-02", "schema_version": "2.1"}
    }


def test_names_are_typed():
    """The display name carries ror_display; the acronym and aliases are their
    own entries."""
    raw = read_text(fixture_path("ror", "ror_nsf.json"))
    names = json.loads(Metadata(raw, via="ror").write(to="ror"))["names"]

    display = [n for n in names if "ror_display" in n["types"]]
    assert display == [
        {
            "lang": None,
            "types": ["label", "ror_display"],
            "value": "U.S. National Science Foundation",
        }
    ]
    assert [n["value"] for n in names if n["types"] == ["acronym"]] == ["NSF"]
    assert [n["value"] for n in names if n["types"] == ["alias"]] == [
        "National Science Foundation",
        "United States National Science Foundation",
    ]


def test_external_ids():
    """commonmeta keeps one value per identifier, so `all` has a single entry."""
    raw = read_text(fixture_path("ror", "ror_nsf.json"))
    out = json.loads(Metadata(raw, via="ror").write(to="ror"))
    assert out["external_ids"] == [
        {"all": ["100000001"], "preferred": "100000001", "type": "fundref"},
        {"all": ["grid.431093.c"], "preferred": "grid.431093.c", "type": "grid"},
        {
            "all": ["0000 0001 1958 7073"],
            "preferred": "0000 0001 1958 7073",
            "type": "isni",
        },
        {"all": ["Q304878"], "preferred": "Q304878", "type": "wikidata"},
    ]


def test_relationships():
    """Relations map back to ROR's parent/child/related, keeping the label."""
    raw = read_text(fixture_path("ror", "ror_nsf.json"))
    out = json.loads(Metadata(raw, via="ror").write(to="ror"))
    by_type = {}
    for relationship in out["relationships"]:
        by_type.setdefault(relationship["type"], []).append(relationship)

    assert by_type["parent"] == [
        {
            "id": "https://ror.org/02rcrvv70",
            "label": "Government of the United States of America",
            "type": "parent",
        }
    ]
    assert by_type["child"][0]["label"] == "American Institute of Mathematics"
    assert by_type["related"][0]["label"] == "Center for Hierarchical Manufacturing"


def test_locations():
    """geo_locations plus the country code rebuild ROR's locations."""
    raw = read_text(fixture_path("ror", "ror_nsf.json"))
    out = json.loads(Metadata(raw, via="ror").write(to="ror"))
    assert out["locations"] == [
        {
            "geonames_id": 4744091,
            "geonames_details": {
                "country_code": "US",
                "country_name": "United States",
                "country_subdivision_name": "Virginia",
                "lat": 38.80484,
                "lng": -77.04692,
                "name": "Alexandria",
            },
        }
    ]


def test_rejects_non_organization():
    """Only organizations are representable as ROR."""
    subject = Metadata(
        read_text(fixture_path("commonmeta", "journal_article.json")), via="commonmeta"
    )
    with pytest.raises(ValueError, match="Only organization entities"):
        subject.write(to="ror")
