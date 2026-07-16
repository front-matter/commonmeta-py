# pylint: disable=invalid-name
"""Test orcid_xml reader"""

# The ORCID fixtures ship with the commonmeta-schema package (shared with
# commonmeta-rs); the golden commonmeta output is asserted by the conformance
# harness in test-conformance.py. These tests cover the reader's own mapping
# rules and edge cases.
from conformance_common import fixture_path, read_text

from commonmeta import Metadata
from commonmeta.readers.orcid_xml_reader import (
    format_affiliation,
    format_affiliation_date,
    normalize_ror_identifier,
    read_orcid_xml,
)


def test_record_xml():
    """ORCID record XML (as found in the bulk summaries dumps)"""
    subject = Metadata(
        read_text(fixture_path("orcid_xml", "0000-0002-0068-716X.xml")), via="orcid_xml"
    )
    assert subject.is_valid
    assert subject.entity_type == "person"
    assert subject.id == "https://orcid.org/0000-0002-0068-716X"
    assert subject.given_name == "Cameron"
    assert subject.family_name == "Neylon"
    assert subject.name == "Cameron Neylon"
    assert subject.country == "SE"
    # the XML carries an ISO 8601 string rather than a unix timestamp
    assert subject.date_updated == "2026-07-16T09:46:15.485Z"
    assert subject.identifiers == [
        {"identifier": "9738760800", "identifier_type": "ScopusID"},
        {"identifier": "0000000138376191", "identifier_type": "ISNI"},
    ]


def test_affiliations():
    """employments and educations both become affiliations"""
    subject = Metadata(
        read_text(fixture_path("orcid_xml", "0000-0002-0068-716X.xml")), via="orcid_xml"
    )
    assert len(subject.affiliations) == 6
    # department-name is folded into the organization name
    assert subject.affiliations[0] == {
        "identifier": "1649",
        "identifier_type": "Ringgold",
        "name": "Curtin University, Centre for Culture & Technology",
        "role": "Professor of Research Communications",
        "start_date": "2015-07-21",
        "end_date": "2024-12-31",
    }
    # an organization without a disambiguated id carries no identifier
    assert "identifier" not in subject.affiliations[1]
    assert subject.affiliations[1]["name"] == "PLOS, Advocacy"
    # educations are role-prefixed so they stay distinguishable in a flat list
    assert subject.affiliations[-1]["role"] == "Education: BSc (Hons)"


def test_affiliation_date_parts():
    """ORCID affiliation dates are year/month/day parts, zero-padded"""
    assert (
        format_affiliation_date({"year": "2015", "month": "7", "day": "21"})
        == "2015-07-21"
    )
    assert format_affiliation_date({"year": "2001", "month": "03"}) == "2001-03"
    assert format_affiliation_date({"year": "1995"}) == "1995"
    assert format_affiliation_date({"month": "07"}) is None
    assert format_affiliation_date(None) is None


def test_ror_affiliation_identifier_normalized():
    """A ROR disambiguation source yields a ROR URL, bare or already a URL"""
    assert normalize_ror_identifier("00k4h2615") == "https://ror.org/00k4h2615"
    assert (
        normalize_ror_identifier("https://ror.org/00k4h2615")
        == "https://ror.org/00k4h2615"
    )
    assert normalize_ror_identifier(None) is None


def test_unmapped_disambiguation_source_drops_identifier():
    """An organization id from a source with no commonmeta type is dropped,
    but the affiliation itself is kept."""
    affiliation = format_affiliation(
        {
            "role-title": "Researcher",
            "organization": {
                "name": "Example University",
                "disambiguated-organization": {
                    "disambiguated-organization-identifier": "12345",
                    "disambiguation-source": "LEI",
                },
            },
        }
    )
    assert affiliation == {"name": "Example University", "role": "Researcher"}


def test_affiliation_without_organization_name_dropped():
    """An affiliation with no organization name isn't representable"""
    assert format_affiliation({"role-title": "Researcher"}) is None


def test_not_found():
    """no record"""
    assert read_orcid_xml(None) == {"state": "not_found"}
