"""Test OpenAlex writer"""

import json

import pytest
from click.testing import CliRunner
from conformance_common import collect_json, fixture_path

from commonmeta import Metadata
from commonmeta.cli import convert
from commonmeta.utils import find_entity_type
from commonmeta.writers.openalex_writer import inverted_index

# The commonmeta-rs writer test (formats/openalex_work.rs), ported.
WORK = {
    "id": "https://doi.org/10.5555/abc",
    "type": "JournalArticle",
    "title": "Molecular structure of nucleic acids",
    "date_published": "1953-04-25",
    "language": "en",
    "url": "https://example.org/abc",
    "description": "We wish to suggest a structure",
    "contributors": [
        {
            "type": "Person",
            "roles": ["Author"],
            "person": {
                "id": "https://orcid.org/0000-0002-1825-0097",
                "given_name": "J. D.",
                "family_name": "Watson",
                "affiliations": [
                    {
                        "identifier": "https://ror.org/03x94j517",
                        "identifier_type": "ROR",
                        "name": "Medical Research Council",
                    }
                ],
            },
        },
        {
            "type": "Person",
            "roles": ["Author"],
            "person": {"given_name": "F. H. C.", "family_name": "Crick"},
        },
    ],
    "container": {
        "type": "Journal",
        "title": "Nature",
        "volume": "171",
        "issue": "4356",
        "first_page": "737",
        "last_page": "738",
        "identifiers": [{"identifier": "0028-0836", "identifier_type": "ISSN"}],
    },
    "license": {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
    },
    "identifiers": [
        {
            "identifier": "https://openalex.org/W2126466006",
            "identifier_type": "OpenAlex",
        },
        {"identifier": "13054692", "identifier_type": "PMID"},
    ],
    "funding_references": [
        {
            "funder_id": "https://ror.org/00yjd3n13",
            "funder_name": "SNSF",
            "grant_number": "123",
            "grant_title": "A grant",
        }
    ],
    "subjects": [
        {"id": "https://openalex.org/T10432", "subject": "DNA"},
        {"id": "https://openalex.org/subfields/1312", "subject": "Molecular Biology"},
    ],
    "references": [
        {"id": "https://openalex.org/W1984602737"},
        {"id": "https://doi.org/10.5555/x"},
    ],
}


def test_a_work_written_as_openalex():
    subject = Metadata(WORK, via="commonmeta")
    record = json.loads(subject.write(to="openalex"))
    assert subject.write_errors is None
    assert record["id"] == "https://openalex.org/W2126466006"
    assert record["doi"] == "https://doi.org/10.5555/abc"
    assert record["type"] == "article"
    assert record["publication_year"] == 1953
    assert record["ids"] == {
        "openalex": "https://openalex.org/W2126466006",
        "doi": "https://doi.org/10.5555/abc",
        "pmid": "https://pubmed.ncbi.nlm.nih.gov/13054692",
    }
    assert [a["author_position"] for a in record["authorships"]] == ["first", "last"]
    assert record["authorships"][0]["author"] == {
        "display_name": "J. D. Watson",
        "orcid": "https://orcid.org/0000-0002-1825-0097",
    }
    assert record["authorships"][0]["institutions"] == [
        {"display_name": "Medical Research Council", "ror": "https://ror.org/03x94j517"}
    ]
    assert record["primary_location"]["source"] == {
        "display_name": "Nature",
        "issn_l": "0028-0836",
        "issn": ["0028-0836"],
        "type": "journal",
        "host_organization_name": None,
    }
    assert record["best_oa_location"]["license"] == "cc-by"
    assert record["primary_topic"] == {
        "id": "https://openalex.org/T10432",
        "display_name": "DNA",
        "subfield": {
            "id": "https://openalex.org/subfields/1312",
            "display_name": "Molecular Biology",
        },
    }
    assert record["funders"] == [
        {"display_name": "SNSF", "ror": "https://ror.org/00yjd3n13"}
    ]
    assert record["awards"] == [
        {
            "funder_award_id": "123",
            "display_name": "A grant",
            "funder_display_name": "SNSF",
        }
    ]
    assert record["referenced_works"] == ["https://openalex.org/W1984602737"]
    assert record["abstract_inverted_index"]["structure"] == [5]


def test_a_work_written_as_openalex_reads_back():
    """The OpenAlex reader reads back what the writer writes (as in
    commonmeta-rs' a_work_written_as_openalex_reads_back)."""
    record = json.loads(Metadata(WORK, via="commonmeta").write(to="openalex"))
    back = Metadata(record, via="openalex")
    assert back.id == WORK["id"]
    assert back.type == "JournalArticle"
    assert back.funding_references == [
        {
            "funder_id": "https://ror.org/00yjd3n13",
            "funder_name": "SNSF",
            "grant_number": "123",
            "grant_title": "A grant",
        }
    ]
    assert back.title == WORK["title"]
    assert back.date_published == WORK["date_published"]
    assert back.description == WORK["description"]
    assert back.license["id"] == "CC-BY-4.0"
    assert back.container["title"] == "Nature"
    assert back.container["volume"] == "171"
    assert len(back.contributors) == 2
    assert (
        back.contributors[0]["person"]["id"] == WORK["contributors"][0]["person"]["id"]
    )
    assert (
        back.contributors[0]["person"]["affiliations"][0]["identifier"]
        == "https://ror.org/03x94j517"
    )
    assert len(back.subjects) == 2


def test_a_sparse_work_keeps_its_nulls():
    """As commonmeta-rs writes it, a field the work lacks is null."""
    subject = Metadata(
        {"id": "https://example.org/a", "type": "Dataset", "title": "A dataset"},
        via="commonmeta",
    )
    record = json.loads(subject.write(to="openalex"))
    assert record["id"] is None
    assert record["doi"] is None
    assert record["ids"] == {}
    assert record["type"] == "dataset"
    assert record["publication_year"] is None
    assert record["best_oa_location"] is None
    assert record["primary_location"]["source"] is None
    assert record["authorships"] == []
    assert record["abstract_inverted_index"] is None


@pytest.mark.parametrize(
    "text,expected",
    [
        ("a b a", {"a": [0, 2], "b": [1]}),
        ("  spaced\nout  ", {"spaced": [0], "out": [1]}),
        ("", {}),
    ],
)
def test_inverted_index(text, expected):
    assert inverted_index(text) == expected


def test_an_organization_has_no_openalex_work():
    subject = Metadata(
        json.loads(open(fixture_path("commonmeta", "organization.json")).read()),
        via="commonmeta",
    )
    assert subject.write(to="openalex") == b"{}"


def test_convert_to_openalex():
    result = CliRunner().invoke(
        convert,
        [fixture_path("commonmeta", "journal_article.json"), "--to", "openalex"],
    )
    assert result.exit_code == 0
    assert json.loads(result.output)["type"] == "article"


def _works() -> list[str]:
    works = []
    for path in collect_json(fixture_path("commonmeta")):
        record = json.loads(open(path).read())
        if isinstance(record, dict) and find_entity_type(record) == "work":
            works.append(path)
    return works


@pytest.mark.parametrize("path", _works(), ids=lambda p: p.split("/")[-1])
def test_openalex_writer_matches_commonmeta_rs(path):
    """Each commonmeta work fixture is written exactly as commonmeta-rs writes
    it, key order included. Needs the Rust backend."""
    commonmeta_rs = pytest.importorskip("commonmeta_rs")
    text = open(path).read()
    expected = json.loads(commonmeta_rs.convert("commonmeta", "openalex", text))
    actual = json.loads(Metadata(path, via="commonmeta").write(to="openalex"))
    assert actual == expected
    assert list(actual) == list(expected)


def test_a_list_is_written_as_its_works():
    """A person before its works (an ORCID record) is left out."""
    from commonmeta import MetadataList

    subject = MetadataList(
        fixture_path("commonmeta_list", "orcid_person_with_works.json"),
        via="commonmeta",
    )
    records = json.loads(subject.write(to="openalex"))
    assert len(subject.items) == 2
    assert [r["type"] for r in records] == ["article"]


@pytest.mark.parametrize("path", _works(), ids=lambda p: p.split("/")[-1])
def test_openalex_reader_matches_commonmeta_rs(path):
    """What the writer writes, the OpenAlex reader reads as commonmeta-rs does:
    type, container, license, funding, identifiers, subjects, references and
    files. Contributors are left out: commonmeta-py splits names and tells
    people from organizations differently. Needs the Rust backend."""
    commonmeta_rs = pytest.importorskip("commonmeta_rs")
    record = Metadata(path, via="commonmeta").write(to="openalex").decode("utf-8")
    expected = json.loads(commonmeta_rs.convert("openalex", "commonmeta", record))
    actual = json.loads(Metadata(json.loads(record), via="openalex").write())
    for key in (
        "id",
        "type",
        "container",
        "license",
        "funding_references",
        "identifiers",
        "subjects",
        "references",
        "files",
        "publisher",
        "date_published",
        "description",
    ):
        # An empty value and an absent one are the same, as in the conformance
        # tests: commonmeta-rs writes a work OpenAlex has no DOI for with an
        # empty id, commonmeta-py without one.
        assert (actual.get(key) or None) == (expected.get(key) or None), key
