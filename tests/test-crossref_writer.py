"""Crossref JSON writer tests"""

import pytest
import json as stdlib_json

from commonmeta import Metadata
from commonmeta.writers.crossref_writer import write_crossref


def test_write_journal_article():
    """Round-trip a Crossref journal article through the writer."""
    subject = Metadata("https://doi.org/10.7554/elife.01567", via="crossref")
    output = stdlib_json.loads(subject.write(to="crossref"))

    assert output["status"] == "ok"
    assert output["message-type"] == "work"
    assert output["message-version"] == "1.0.0"

    msg = output["message"]
    assert msg["DOI"] == "10.7554/elife.01567"
    assert msg["type"] == "journal-article"
    assert msg["title"] == [
        "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    ]
    assert msg["publisher"] == "eLife Sciences Publications, Ltd"
    assert msg["volume"] == "3"
    assert msg["ISSN"] == ["2050-084X"]
    assert msg["language"] == "en"
    assert msg["issued"] == {"date-parts": [[2014, 2, 11]]}
    assert msg["URL"] == "https://doi.org/10.7554/elife.01567"
    assert msg["resource"] == {
        "primary": {"URL": "https://elifesciences.org/articles/01567"}
    }

    author = msg["author"][0]
    assert author["given"] == "Martial"
    assert author["family"] == "Sankar"
    assert author["sequence"] == "first"
    assert author["affiliation"][0]["name"] == (
        "Department of Plant Molecular Biology, University of Lausanne, "
        "Lausanne, Switzerland"
    )

    assert msg["license"][0] == {
        "URL": "https://creativecommons.org/licenses/by/3.0/legalcode",
        "content-version": "vor",
    }
    assert msg["license"][1]["content-version"] == "tdm"

    assert len(msg["reference"]) == 27
    ref = msg["reference"][0]
    assert ref["key"] == "bib1"
    assert ref["DOI"] == "10.1038/nature02100"
    assert ref["unstructured"] == "APL regulates vascular tissue identity in Arabidopsis"


def test_write_posted_content():
    """Preprint (posted-content) uses group-title, not container-title,
    and has a `posted` date field in addition to `issued`."""
    subject = Metadata("https://doi.org/10.1101/097196", via="crossref")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]

    assert msg["type"] == "posted-content"
    assert "container-title" not in msg
    assert msg["group-title"] == "Scientific Communication and Education"
    assert "posted" in msg
    assert msg["posted"]["date-parts"] == [[2016, 12, 28]]
    assert msg["issued"]["date-parts"] == [[2016, 12, 28]]
    assert msg["abstract"].startswith("<jats:p>")


def test_write_dissertation():
    """Dissertation type mapping and ORCID round-trip."""
    subject = Metadata("https://doi.org/10.14264/uql.2020.791", via="crossref")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]

    assert msg["type"] == "dissertation"
    assert msg["issued"] == {"date-parts": [[2020, 6, 8]]}
    author = msg["author"][0]
    assert author["ORCID"] == "https://orcid.org/0000-0003-3086-4443"
    assert author["authenticated-orcid"] is False
    assert author["given"] == "Patricia Maree"
    assert author["family"] == "Collingwood"


def test_license_always_emits_vor_and_tdm():
    """The writer must always produce both 'vor' and 'tdm' content-version entries."""
    subject = Metadata("https://doi.org/10.7554/elife.01567", via="crossref")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]

    assert len(msg["license"]) == 2
    versions = {lic["content-version"] for lic in msg["license"]}
    assert versions == {"vor", "tdm"}
    # Both entries point at the same URL
    urls = {lic["URL"] for lic in msg["license"]}
    assert len(urls) == 1


def test_write_without_doi():
    """Records without a DOI omit the DOI field but still write correctly."""
    data = stdlib_json.dumps({
        "id": "https://example.org/article",
        "type": "JournalArticle",
        "title": "No DOI Here",
        "date_published": "2023-05",
        "provider": "Crossref",
    })
    subject = Metadata(data, via="commonmeta")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]

    assert "DOI" not in msg
    assert msg["type"] == "journal-article"
    assert msg["title"] == ["No DOI Here"]
    assert msg["issued"] == {"date-parts": [[2023, 5]]}
    assert "URL" not in msg


def test_write_year_only_date():
    """Year-only dates produce single-element date-parts."""
    data = stdlib_json.dumps({
        "id": "https://doi.org/10.1000/test",
        "type": "JournalArticle",
        "title": "Year Only",
        "date_published": "2021",
        "provider": "Crossref",
    })
    subject = Metadata(data, via="commonmeta")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]
    assert msg["issued"] == {"date-parts": [[2021]]}


def test_write_funding():
    """Funding references are grouped by funder and awards collected."""
    data = stdlib_json.dumps({
        "id": "https://doi.org/10.1000/funded",
        "type": "JournalArticle",
        "title": "Funded Study",
        "date_published": "2022",
        "funding_references": [
            {
                "funder_id": "https://doi.org/10.13039/501100000780",
                "funder_name": "European Commission",
                "award_number": "EC-123",
            },
            {
                "funder_id": "https://doi.org/10.13039/501100000780",
                "funder_name": "European Commission",
                "award_number": "EC-456",
            },
            {
                "funder_id": "",
                "funder_name": "Anonymous Donor",
                "award_number": "",
            },
        ],
        "provider": "Crossref",
    })
    subject = Metadata(data, via="commonmeta")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]
    funders = msg["funder"]

    assert len(funders) == 2
    ec = funders[0]
    assert ec["DOI"] == "10.13039/501100000780"
    assert ec["name"] == "European Commission"
    assert ec["award"] == ["EC-123", "EC-456"]
    anon = funders[1]
    assert anon["name"] == "Anonymous Donor"
    assert "DOI" not in anon
    assert "award" not in anon


def test_write_editor_separate_from_author():
    """Editors are emitted in `editor`, not `author`."""
    data = stdlib_json.dumps({
        "id": "https://doi.org/10.1000/edited",
        "type": "Book",
        "title": "Edited Volume",
        "date_published": "2020",
        "contributors": [
            {
                "type": "Person",
                "person": {"given_name": "Alice", "family_name": "Author"},
                "roles": ["Author"],
            },
            {
                "type": "Person",
                "person": {"given_name": "Bob", "family_name": "Editor"},
                "roles": ["Editor"],
            },
        ],
        "provider": "Crossref",
    })
    subject = Metadata(data, via="commonmeta")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]

    assert len(msg["author"]) == 1
    assert msg["author"][0]["family"] == "Author"
    assert len(msg["editor"]) == 1
    assert msg["editor"][0]["family"] == "Editor"
    assert msg["author"][0]["sequence"] == "first"
    assert msg["editor"][0]["sequence"] == "first"


def test_write_organization_author():
    """Organization contributors use the `name` field, not given/family."""
    data = stdlib_json.dumps({
        "id": "https://doi.org/10.1000/org",
        "type": "Report",
        "title": "Org Report",
        "date_published": "2021",
        "contributors": [
            {
                "type": "Organization",
                "organization": {"name": "WHO Collaboration"},
                "roles": ["Author"],
            }
        ],
        "provider": "Crossref",
    })
    subject = Metadata(data, via="commonmeta")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]

    assert msg["author"][0]["name"] == "WHO Collaboration"
    assert "given" not in msg["author"][0]
    assert "family" not in msg["author"][0]


def test_write_none_returns_none():
    """write_crossref(None) returns None."""
    assert write_crossref(None) is None


def test_write_subjects():
    """Subjects are emitted as a flat string list under `subject`."""
    data = stdlib_json.dumps({
        "id": "https://doi.org/10.1000/subj",
        "type": "JournalArticle",
        "title": "Subjectful",
        "date_published": "2020",
        "subjects": [
            {"subject": "Ecology"},
            {"subject": "Evolution"},
        ],
        "provider": "Crossref",
    })
    subject = Metadata(data, via="commonmeta")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]
    assert msg["subject"] == ["Ecology", "Evolution"]


def test_write_affiliation_with_ror():
    """Affiliations with ROR IDs are serialized with id-type=ROR."""
    data = stdlib_json.dumps({
        "id": "https://doi.org/10.1000/ror",
        "type": "JournalArticle",
        "title": "ROR Test",
        "date_published": "2021",
        "contributors": [
            {
                "type": "Person",
                "person": {
                    "given_name": "Jane",
                    "family_name": "Doe",
                    "affiliations": [
                        {
                            "identifier": "https://ror.org/04fa4r544",
                            "identifier_type": "ROR",
                            "name": "CERN",
                            "asserted_by": "Publisher",
                        }
                    ],
                },
                "roles": ["Author"],
            }
        ],
        "provider": "Crossref",
    })
    subject = Metadata(data, via="commonmeta")
    msg = stdlib_json.loads(subject.write(to="crossref"))["message"]
    aff = msg["author"][0]["affiliation"][0]
    assert aff["name"] == "CERN"
    assert aff["id"][0]["id"] == "https://ror.org/04fa4r544"
    assert aff["id"][0]["id-type"] == "ROR"
    assert aff["id"][0]["asserted-by"] == "publisher"
