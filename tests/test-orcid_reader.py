# pylint: disable=invalid-name
"""Test orcid reader"""

# The ORCID fixtures ship with the commonmeta-schema package (shared with
# commonmeta-rs); the golden commonmeta output for each is asserted by the
# conformance harness in test-conformance.py. These tests cover the reader's own
# mapping rules and edge cases.
from conformance_common import fixture_path, read_text

from commonmeta import Metadata
from commonmeta.readers.orcid_reader import read_orcid


def test_person_json():
    """ORCID person JSON (the /person endpoint)"""
    subject = Metadata(
        read_text(fixture_path("orcid", "person_0000-0003-1419-2405.json")),
        via="orcid",
    )
    assert subject.is_valid
    assert subject.entity_type == "person"
    assert subject.id == "https://orcid.org/0000-0003-1419-2405"
    assert subject.given_name == "Martin"
    assert subject.family_name == "Fenner"
    assert subject.name == "Martin Fenner"
    assert subject.additional_names == ["Martin Hellmut Fenner"]
    assert subject.country == "DE"
    assert subject.asserted_by == "ORCID"
    # last-modified-date is milliseconds since the epoch in the person JSON
    assert subject.date_updated == "2026-06-16T19:54:19Z"
    assert subject.identifiers == [
        {"identifier": "000000035060549X", "identifier_type": "ISNI"}
    ]
    assert subject.urls == [
        {"name": "Mastodon", "url": "https://hachyderm.io/@mfenner"},
        {"name": "GitHub", "url": "https://github.com/mfenner"},
        {"name": "Blog", "url": "https://blog.front-matter.de"},
    ]
    # a biography's line breaks are content, and survive the writer
    assert subject.description.startswith("Martin Fenner is the Founder")
    assert "\n" in subject.description
    # the /person endpoint carries no employments
    assert getattr(subject, "affiliations", None) is None


def test_unmapped_external_id_keeps_scheme():
    """An external id type with no commonmeta equivalent becomes Other + scheme"""
    meta = read_orcid(
        {
            "path": "/0000-0003-1419-2405/person",
            "external-identifiers": {
                "external-identifier": [
                    {
                        "external-id-type": "Loop profile",
                        "external-id-value": "12345",
                    },
                    {
                        "external-id-type": "ISNI",
                        "external-id-value": "000000035060549X",
                    },
                ]
            },
        }
    )
    assert meta["identifiers"] == [
        {
            "identifier": "12345",
            "identifier_type": "Other",
            "scheme": "Loop profile",
        },
        {"identifier": "000000035060549X", "identifier_type": "ISNI"},
    ]


def test_display_name_without_credit_name():
    """Without a credit name the display name is given + family"""
    meta = read_orcid(
        {
            "path": "0000-0003-1419-2405",
            "name": {
                "given-names": {"value": "Josiah"},
                "family-name": {"value": "Carberry"},
            },
        }
    )
    assert meta["name"] == "Josiah Carberry"


def test_not_found():
    """no record"""
    assert read_orcid(None) == {"state": "not_found"}
