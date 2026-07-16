# pylint: disable=invalid-name
"""Test orcid writer"""

import json

import pytest
from conformance_common import diff, fixture_path, read_text

from commonmeta import Metadata
from commonmeta.readers.orcid_reader import read_orcid


def test_roundtrip_is_identity():
    """ORCID -> commonmeta -> ORCID -> commonmeta is the same.

    Reading ORCID into commonmeta is lossy by design (visibility, source,
    put-codes; see the writer's docstring), so the writer is checked against what
    commonmeta models rather than against the input verbatim. Affiliations are
    part of the /record the writer emits, so they round-trip too.
    """
    raw = read_text(fixture_path("orcid", "0000-0002-0068-716X.json"))
    before = json.loads(Metadata(raw, via="orcid").write(to="commonmeta"))
    orcid = Metadata(raw, via="orcid").write(to="orcid")
    after = json.loads(Metadata(orcid.decode(), via="orcid").write(to="commonmeta"))
    assert not diff(before, after)


def test_record():
    """A person is rebuilt in the ORCID /record shape, affiliations included."""
    raw = read_text(fixture_path("orcid", "0000-0002-0068-716X.json"))
    out = json.loads(Metadata(raw, via="orcid").write(to="orcid"))

    assert out["orcid-identifier"] == {
        "uri": "https://orcid.org/0000-0002-0068-716X",
        "path": "0000-0002-0068-716X",
    }
    person = out["person"]
    assert person["path"] == "/0000-0002-0068-716X/person"
    assert person["name"]["given-names"] == {"value": "Cameron"}
    assert person["name"]["family-name"] == {"value": "Neylon"}
    assert person["addresses"] == {"address": [{"country": {"value": "SE"}}]}
    assert person["biography"]["content"].startswith("Cameron Neylon is an independent")
    assert person["external-identifiers"] == {
        "external-identifier": [
            {"external-id-type": "Scopus Author ID", "external-id-value": "9738760800"},
            {"external-id-type": "ISNI", "external-id-value": "0000000138376191"},
        ]
    }
    assert person["researcher-urls"]["researcher-url"][0] == {
        "url-name": "Personal website",
        "url": {"value": "http://cameronneylon.net"},
    }


def test_activities_summary():
    """Affiliations become employments and educations under activities-summary."""
    raw = read_text(fixture_path("orcid", "0000-0002-0068-716X.json"))
    activities = json.loads(Metadata(raw, via="orcid").write(to="orcid"))[
        "activities-summary"
    ]

    employments = activities["employments"]["affiliation-group"]
    educations = activities["educations"]["affiliation-group"]
    assert len(employments) == 4
    assert len(educations) == 2

    summary = employments[0]["summaries"][0]["employment-summary"]
    assert summary["organization"] == {
        "name": "Curtin University, Centre for Culture & Technology",
        "disambiguated-organization": {
            "disambiguated-organization-identifier": "1649",
            "disambiguation-source": "RINGGOLD",
        },
    }
    assert summary["role-title"] == "Professor of Research Communications"
    # ISO date parts come back {value}-wrapped
    assert summary["start-date"] == {
        "year": {"value": "2015"},
        "month": {"value": "07"},
        "day": {"value": "21"},
    }
    # the "Education" role prefix is stripped back off the education title
    education = educations[-1]["summaries"][0]["education-summary"]
    assert education["role-title"] == "BSc (Hons)"


def test_last_modified_is_milliseconds():
    """ORCID reports person dates as milliseconds since the epoch."""
    raw = read_text(fixture_path("orcid", "0000-0002-0068-716X.json"))
    person = json.loads(Metadata(raw, via="orcid").write(to="orcid"))["person"]
    # the reader turned 1784195175480 into 2026-07-16T09:46:15Z; it goes back
    # whole-second, so the sub-second part of the original is not restored
    assert person["last-modified-date"] == {"value": 1784195175000}


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
    assert "credit-name" not in out["person"]["name"]

    explicit = dict(derived, name="J. Carberry")
    out = json.loads(Metadata(json.dumps(explicit), via="commonmeta").write(to="orcid"))
    assert out["person"]["name"]["credit-name"] == {"value": "J. Carberry"}


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
    assert out["person"]["external-identifiers"] == {
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
