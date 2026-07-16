# pylint: disable=invalid-name
"""Test orcid reader"""

# The ORCID fixtures ship with the commonmeta-schema package (shared with
# commonmeta-rs); the golden commonmeta output for each is asserted by the
# conformance harness in test-conformance.py. These tests cover the reader's own
# mapping rules and edge cases.
from conformance_common import fixture_path, read_text

from commonmeta import Metadata
from commonmeta.readers.orcid_reader import read_orcid


def test_record_json():
    """ORCID record JSON (the /record endpoint), with affiliations"""
    subject = Metadata(
        read_text(fixture_path("orcid", "0000-0002-0068-716X.json")),
        via="orcid",
    )
    assert subject.is_valid
    assert subject.entity_type == "person"
    assert subject.id == "https://orcid.org/0000-0002-0068-716X"
    assert subject.given_name == "Cameron"
    assert subject.family_name == "Neylon"
    assert subject.name == "Cameron Neylon"
    assert subject.country == "SE"
    assert subject.asserted_by == "ORCID"
    # last-modified-date is milliseconds since the epoch in the record JSON
    assert subject.date_updated == "2026-07-16T09:46:15Z"
    assert subject.identifiers == [
        {"identifier": "9738760800", "identifier_type": "ScopusID"},
        {"identifier": "0000000138376191", "identifier_type": "ISNI"},
    ]
    assert subject.urls == [
        {"name": "Personal website", "url": "http://cameronneylon.net"},
        {"name": "Mastodon", "url": "https://hcommons.social/@cameronneylon"},
    ]
    assert subject.description.startswith("Cameron Neylon is an independent researcher")
    # the /record endpoint carries employments and educations as affiliations;
    # educations keep an "Education" role prefix so they stay distinguishable
    assert len(subject.affiliations) == 6
    assert (
        subject.affiliations[0]["name"]
        == "Curtin University, Centre for Culture & Technology"
    )
    assert subject.affiliations[-1]["role"] == "Education: BSc (Hons)"


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
