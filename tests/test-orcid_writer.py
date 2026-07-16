# pylint: disable=invalid-name
"""Test orcid writer"""

import json

import pytest
from conformance_common import diff, fixture_path, read_text

from commonmeta import Metadata
from commonmeta.readers.orcid_reader import read_orcid


def test_roundtrip_is_identity():
    """ORCID person -> commonmeta -> ORCID person -> commonmeta is the same.

    Reading ORCID into commonmeta is lossy by design (visibility, source,
    put-codes; see the writer's docstring), so the writer is checked against what
    commonmeta models rather than against the input verbatim.
    """
    raw = read_text(fixture_path("orcid", "person_0000-0003-1419-2405.json"))
    before = json.loads(Metadata(raw, via="orcid").write(to="commonmeta"))
    orcid = Metadata(raw, via="orcid").write(to="orcid")
    after = json.loads(Metadata(orcid.decode(), via="orcid").write(to="commonmeta"))
    assert not diff(before, after)


def test_person():
    """A person is rebuilt in the ORCID API's shape."""
    raw = read_text(fixture_path("orcid", "person_0000-0003-1419-2405.json"))
    out = json.loads(Metadata(raw, via="orcid").write(to="orcid"))

    assert out["path"] == "/0000-0003-1419-2405/person"
    assert out["name"]["given-names"] == {"value": "Martin"}
    assert out["name"]["family-name"] == {"value": "Fenner"}
    assert out["other-names"] == {"other-name": [{"content": "Martin Hellmut Fenner"}]}
    assert out["addresses"] == {"address": [{"country": {"value": "DE"}}]}
    assert out["biography"]["content"].startswith("Martin Fenner is the Founder")
    assert out["external-identifiers"] == {
        "external-identifier": [
            {"external-id-type": "ISNI", "external-id-value": "000000035060549X"}
        ]
    }
    assert out["researcher-urls"]["researcher-url"][0] == {
        "url-name": "Mastodon",
        "url": {"value": "https://hachyderm.io/@mfenner"},
    }


def test_last_modified_is_milliseconds():
    """ORCID reports person dates as milliseconds since the epoch."""
    raw = read_text(fixture_path("orcid", "person_0000-0003-1419-2405.json"))
    out = json.loads(Metadata(raw, via="orcid").write(to="orcid"))
    # the reader turned 1781639659032 into 2026-06-16T19:54:19Z; it goes back
    # whole-second, so the sub-second part of the original is not restored
    assert out["last-modified-date"] == {"value": 1781639659000}


def test_credit_name_only_when_it_differs():
    """`name` is only a credit name when it isn't just "given family", which is
    what the reader derives when the credit name is absent."""
    derived = read_orcid(
        {
            "path": "0000-0003-1419-2405",
            "name": {
                "given-names": {"value": "Josiah"},
                "family-name": {"value": "Carberry"},
            },
        }
    )
    out = json.loads(Metadata(json.dumps(derived), via="commonmeta").write(to="orcid"))
    assert "credit-name" not in out["name"]

    explicit = dict(derived, name="J. Carberry")
    out = json.loads(Metadata(json.dumps(explicit), via="commonmeta").write(to="orcid"))
    assert out["name"]["credit-name"] == {"value": "J. Carberry"}


def test_other_identifier_restores_its_scheme():
    """An identifier read as Other kept its ORCID type in `scheme`; the writer
    restores it rather than emitting "Other"."""
    person = {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "identifiers": [
            {
                "identifier": "12345",
                "identifier_type": "Other",
                "scheme": "Loop profile",
            }
        ],
    }
    out = json.loads(Metadata(json.dumps(person), via="commonmeta").write(to="orcid"))
    assert out["external-identifiers"] == {
        "external-identifier": [
            {"external-id-type": "Loop profile", "external-id-value": "12345"}
        ]
    }


def test_rejects_non_person():
    """Only persons are representable as ORCID."""
    subject = Metadata(
        read_text(fixture_path("commonmeta", "organization.json")), via="commonmeta"
    )
    with pytest.raises(ValueError, match="Only person entities"):
        subject.write(to="orcid")
