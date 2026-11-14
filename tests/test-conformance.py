# pylint: disable=invalid-name
"""Conformance harness ported from commonmeta-rs (tests/conformance.rs).

`commonmeta_roundtrip` reads every fixture in tests/fixtures/commonmeta/,
parses and re-serializes it, and asserts equivalence under commonmeta
semantics (strict — guards against commonmeta-py regressions).

The cross-format golden tests follow the convention
  tests/fixtures/<format>/<name>.<ext>       -> input in that format
  tests/fixtures/commonmeta/<name>.json      -> expected commonmeta output
(or a format-specific *_out directory for writer goldens). Each fixture pair
is a separate parametrized case: it passes when commonmeta-py matches the
commonmeta-rs golden output and xfails (documenting the diff) when it diverges.
"""

import json
import re

import pytest
from conformance_common import (
    assert_golden_or_xfail,
    canonical_commonmeta_value,
    case_id,
    collect_json,
    convert,
    convert_or_xfail,
    diff,
    fixture_path,
    pair_id,
    read_text,
    reader_pairs,
    utils_cases,
    writer_pairs,
)

from commonmeta import Metadata
from commonmeta.doi_utils import decode_doi, encode_doi
from commonmeta.schema_utils import COMMONMETA_SCHEMA_URI, json_schema_errors
from commonmeta.utils import find_entity_type
from commonmeta.writers.commonmeta_writer import collapse_whitespace

# --- commonmeta round-trip (strict) ---


@pytest.mark.parametrize(
    "path", collect_json(fixture_path("commonmeta")), ids=lambda p: p.split("/")[-1]
)
def test_commonmeta_roundtrip(path):
    """Every commonmeta fixture re-serializes to an equivalent document.

    Compares against the fixture as authored, not against a second convert()
    of the same input: running both sides through the reader+writer makes the
    assertion tautological, so any field the pipeline drops disappears from
    expected and actual alike and the diff is empty by construction.
    """
    raw = read_text(path)
    expected = json.loads(raw)
    if isinstance(expected, list):
        expected = expected[0]
    # A work's description is whitespace-normalized on write by design (see
    # collapse_whitespace), so a hard-wrapped fixture description re-serializes
    # to a single line. Apply the same transform to the expectation rather than
    # asserting on formatting the writer deliberately discards. Person and
    # organization entities are exempt: a biography's line breaks are content.
    if find_entity_type(expected) == "work":
        # The writer stamps schema_version onto every work by design (as
        # commonmeta-rs does); a fixture authored without it still round-trips.
        expected.setdefault("schema_version", COMMONMETA_SCHEMA_URI)
        if expected.get("description"):
            expected["description"] = collapse_whitespace(expected["description"])
        for d in expected.get("additional_descriptions") or []:
            if isinstance(d, dict) and d.get("description"):
                d["description"] = collapse_whitespace(d["description"])
    actual = convert("commonmeta", "commonmeta", raw)
    diffs = diff(expected, actual)
    assert not diffs, "\n".join(str(d) for d in diffs)


def test_commonmeta_fixtures_present():
    """The commonmeta fixture corpus is non-empty."""
    assert collect_json(fixture_path("commonmeta")), "no commonmeta fixtures found"


# --- list output (commonmeta array: an entity followed by its works) ---


@pytest.mark.parametrize(
    "path",
    collect_json(fixture_path("commonmeta_list")),
    ids=lambda p: p.split("/")[-1],
)
def test_commonmeta_list_is_schema_valid_array(path):
    """A `list` result is a commonmeta JSON array [entity, work, …].

    It is the shape `list --from orcid|ror … --to commonmeta` returns (person or
    organization first, then works), the counterpart to `convert`'s single object.
    The whole array validates against the v1.0 schema (whose top level is an
    array), and every element round-trips through the reader+writer.
    """
    from commonmeta.schema_utils import json_schema_errors

    records = json.loads(read_text(path))
    assert isinstance(records, list) and len(records) >= 2
    assert json_schema_errors(records) is None, "list array fails schema validation"
    assert find_entity_type(records[0]) in ("person", "organization")
    assert all(find_entity_type(r) == "work" for r in records[1:])
    for record in records:
        convert("commonmeta", "commonmeta", json.dumps(record))


# --- reader golden tests (xfail on divergence) ---


@pytest.mark.parametrize("pair", reader_pairs("crossref"), ids=pair_id)
def test_crossref_to_commonmeta_golden(pair):
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("crossref", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize("pair", reader_pairs("schemaorg"), ids=pair_id)
def test_schemaorg_to_commonmeta_golden(pair):
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("schemaorg", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize("pair", reader_pairs("csl"), ids=pair_id)
def test_csl_to_commonmeta_golden(pair):
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("csl", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize(
    "pair", reader_pairs("bibtex", "bib", "bibtex_commonmeta"), ids=pair_id
)
def test_bibtex_to_commonmeta_golden(pair):
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("bibtex", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize(
    "pair", reader_pairs("crossref_xml", "xml", "crossref_xml_commonmeta"), ids=pair_id
)
def test_crossref_xml_to_commonmeta_golden(pair):
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("crossref_xml", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize(
    "pair", reader_pairs("cff", "cff", "cff_commonmeta"), ids=pair_id
)
def test_cff_to_commonmeta_golden(pair):
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("cff", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize(
    "pair", reader_pairs("ris", "ris", "ris_commonmeta"), ids=pair_id
)
def test_ris_to_commonmeta_golden(pair):
    input_path, expected_path = pair
    # pure.ris produces a record without a DOI-based id which fails schema validation
    if pair_id(pair) == "pure.ris":
        pytest.skip("pure.ris has no DOI-based id (matches commonmeta-rs skip)")
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("ris", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize(
    "pair", reader_pairs("datacite_xml", "xml", "datacite_xml_commonmeta"), ids=pair_id
)
def test_datacite_xml_to_commonmeta_golden(pair):
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("datacite_xml", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize("pair", reader_pairs("ror"), ids=pair_id)
def test_ror_to_commonmeta_golden(pair):
    """ROR API records convert to commonmeta organization entities."""
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("ror", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize("pair", reader_pairs("orcid"), ids=pair_id)
def test_orcid_to_commonmeta_golden(pair):
    """ORCID person JSON converts to commonmeta person entities."""
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("orcid", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize(
    "pair", reader_pairs("orcid", "xml", "orcid_commonmeta"), ids=pair_id
)
def test_orcid_xml_to_commonmeta_golden(pair):
    """ORCID record XML converts to commonmeta person entities."""
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail("orcid_xml", "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


# --- writer golden tests (xfail on divergence) ---


@pytest.mark.parametrize("pair", writer_pairs("crossref_out"), ids=pair_id)
def test_commonmeta_to_crossref_golden(pair):
    input_path, expected_path = pair
    expected = json.loads(read_text(expected_path))
    actual = convert_or_xfail("commonmeta", "crossref", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize("pair", writer_pairs("datacite"), ids=pair_id)
def test_commonmeta_to_datacite_golden(pair):
    input_path, expected_path = pair
    expected = json.loads(read_text(expected_path))
    actual = convert_or_xfail("commonmeta", "datacite", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize("pair", writer_pairs("schemaorg_out"), ids=pair_id)
def test_commonmeta_to_schemaorg_golden(pair):
    input_path, expected_path = pair
    expected = json.loads(read_text(expected_path))
    actual = convert_or_xfail("commonmeta", "schemaorg", read_text(input_path))
    assert_golden_or_xfail(expected, actual)


@pytest.mark.parametrize("pair", writer_pairs("bibtex_out", "bib"), ids=pair_id)
def test_commonmeta_to_bibtex_golden(pair):
    input_path, expected_path = pair
    expected = read_text(expected_path)
    actual = convert_or_xfail("commonmeta", "bibtex", read_text(input_path))
    if actual != expected:
        pytest.xfail("BibTeX output diverges from commonmeta-rs golden")


# --- shared helper fixtures (strict) ---
#
# fixtures/utils describes encode_doi/decode_doi behaviour rather than record
# conversion, so unlike the golden matrices these assert outright: the helpers
# are shared with commonmeta-rs and a divergence is a bug, not a known gap.


@pytest.mark.parametrize("case", utils_cases("decode_doi_cases.json"), ids=case_id)
def test_decode_doi_cases(case):
    assert decode_doi(case["doi"], checksum=case["checksum"]) == case["expected_number"]


@pytest.mark.parametrize("case", utils_cases("encode_doi_cases.json"), ids=case_id)
def test_encode_doi_cases(case):
    doi = encode_doi(case["prefix"], case.get("number"), checksum=case["checksum"])

    if "expected_doi" in case:
        assert doi == case["expected_doi"]
    if "expected_doi_prefix" in case:
        assert doi.startswith(case["expected_doi_prefix"])
    if "expected_suffix_pattern" in case:
        suffix = doi.rsplit("/", maxsplit=1)[-1]
        assert re.match(case["expected_suffix_pattern"], suffix), suffix

    # the encoded DOI has to decode back; a random suffix only has to be nonzero
    expected = case.get("expected_decoded_number")
    decoded = decode_doi(doi, checksum=case["checksum"])
    if expected == "nonzero":
        assert decoded != 0
    else:
        assert decoded == expected


# --- self-tests for the diff engine (strict) ---


def test_diff_detects_lost_field():
    assert len(diff({"a": "x", "b": "y"}, {"a": "x"})) == 1


def test_diff_ignores_emptyish_absences():
    e = {"a": "x", "empty": "", "arr": [], "obj": {}, "zero": 0}
    assert diff(e, {"a": "x"}) == []


def test_diff_treats_int_and_float_as_equal():
    assert diff({"lat": 52}, {"lat": 52.0}) == []


def test_diff_flags_changed_scalar():
    assert len(diff({"title": "A"}, {"title": "B"})) == 1


def test_diff_flags_array_length():
    diffs = diff({"xs": [1, 2, 3]}, {"xs": [1, 2]})
    assert any(m.kind == "LENGTH" for m in diffs)


# --- reader gaps closed for commonmeta-schema 1.0.11 (strict) ---
#
# The golden tests above xfail on any divergence, so a regression in a pair
# that once passed would go unnoticed. These pairs exercise the 1.0.11 fields
# (number, edition, container.event, update relations, Retraction) and must
# match the commonmeta-rs golden exactly.

STRICT_GOLDENS = [
    ("crossref", "json", "commonmeta", "crossref_retracted_article.json"),
    ("crossref", "json", "commonmeta", "crossref_retraction_notice.json"),
    ("crossref_xml", "xml", "crossref_xml_commonmeta", "crossref_elife_01567.xml"),
    ("csl", "json", "commonmeta", "csl_book.json"),
    ("csl", "json", "commonmeta", "csl_conference_paper.json"),
    ("csl", "json", "commonmeta", "csl_report.json"),
]


@pytest.mark.parametrize(
    "from_format,ext,expected_subdir,name",
    STRICT_GOLDENS,
    ids=[g[3] for g in STRICT_GOLDENS],
)
def test_schema_1_0_11_reader_golden(from_format, ext, expected_subdir, name):
    pairs = {pair_id(p): p for p in reader_pairs(from_format, ext, expected_subdir)}
    assert name in pairs, f"{from_format} golden {name} not found"
    input_path, expected_path = pairs[name]
    # canonicalized as the golden tests above are: the writer drops an
    # identifier repeating the DOI id, which some goldens list
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert(from_format, "commonmeta", read_text(input_path))
    diffs = diff(expected, actual)
    assert not diffs, "\n".join(str(d) for d in diffs)
    assert json_schema_errors(actual) is None


def _crossref(message: dict) -> dict:
    return convert("crossref", "commonmeta", json.dumps({"message": message}))


def test_crossref_correction_notice_is_an_erratum():
    """A correction notice Corrects the work it updates; an update type with no
    commonmeta relation and an update naming the record itself add nothing."""
    actual = _crossref(
        {
            "DOI": "10.5555/ERRATUM",
            "type": "journal-article",
            "title": ["Erratum: A Study"],
            "update-to": [
                {
                    "DOI": "10.5555/original",
                    "type": "correction",
                    "source": "publisher",
                },
                {"DOI": "10.5555/older", "type": "new_version", "source": "publisher"},
                {"DOI": "10.5555/erratum", "type": "correction", "source": "publisher"},
            ],
        }
    )
    assert actual["type"] == "Erratum"
    assert actual["relations"] == [
        {
            "id": "https://doi.org/10.5555/original",
            "type": "Corrects",
            "asserted_by": "Publisher",
        }
    ]
    assert json_schema_errors(actual) is None


@pytest.mark.parametrize(
    "update_type,relation_type",
    [
        ("retraction", "IsRetractedBy"),
        ("partial_retraction", "IsRetractedBy"),
        ("corrigendum", "IsCorrectedBy"),
        ("expression_of_concern", "HasExpressionOfConcern"),
        ("Expression of Concern", "HasExpressionOfConcern"),
        ("withdrawal", "IsWithdrawnBy"),
        ("reinstatement", "IsReinstatedBy"),
        ("addendum", "IsSupplementedBy"),
    ],
)
def test_crossref_updated_by(update_type, relation_type):
    """The updated work keeps a relation to its notice, and its own type; a
    source commonmeta has no provider for leaves asserted_by out."""
    actual = _crossref(
        {
            "DOI": "10.5555/original",
            "type": "journal-article",
            "title": ["A Study"],
            "article-number": " e123 ",
            "updated-by": [
                {"DOI": "10.5555/notice", "type": update_type, "source": "elsewhere"}
            ],
        }
    )
    assert actual["type"] == "JournalArticle"
    assert actual["number"] == "e123"
    assert actual["relations"] == [
        {"id": "https://doi.org/10.5555/notice", "type": relation_type}
    ]
    assert json_schema_errors(actual) is None


def test_crossref_container_notice_keeps_its_type():
    """Only a work becomes a Retraction; a journal registered with an update
    stays a journal."""
    actual = _crossref(
        {
            "DOI": "10.5555/journal",
            "type": "journal",
            "title": ["A Journal"],
            "update-to": [{"DOI": "10.5555/original", "type": "retraction"}],
        }
    )
    assert actual["type"] == "Journal"


def _csl(item: dict) -> dict:
    return convert("csl", "commonmeta", json.dumps(item))


@pytest.mark.parametrize(
    "csl_type,series_type",
    [
        ("book", "BookSeries"),
        ("chapter", "BookSeries"),
        ("paper-conference", "ProceedingsSeries"),
        ("report", "ReportSeries"),
    ],
)
def test_csl_collection_title_without_container_is_the_series(csl_type, series_type):
    actual = _csl(
        {
            "id": "10.5555/series",
            "type": csl_type,
            "title": "A Work",
            "collection-title": "A Series",
        }
    )
    assert actual["container"]["type"] == series_type
    assert actual["container"]["title"] == "A Series"


def test_csl_collection_title_beside_a_container_title_is_not_the_container():
    actual = _csl(
        {
            "id": "10.5555/chapter",
            "type": "chapter",
            "title": "A Chapter",
            "container-title": "A Book",
            "collection-title": "A Series",
        }
    )
    assert actual["container"] == {"type": "Book", "title": "A Book"}


def test_csl_number_variables_and_event():
    """CSL number variables may be numbers; `event` is the CSL 1.0.1 name of
    `event-title`."""
    actual = _csl(
        {
            "id": "10.5555/conf",
            "type": "paper-conference",
            "title": "A Paper",
            "container-title": "Proceedings",
            "event": "A Conference",
            "edition": 3,
            "number": 17,
        }
    )
    assert actual["edition"] == "3"
    assert actual["number"] == "17"
    assert actual["container"]["event"] == "A Conference"
    assert json_schema_errors(actual) is None


CROSSMARK_RETRACTION_XML = """<?xml version="1.0" encoding="UTF-8"?>
<crossref_result xmlns="http://www.crossref.org/qrschema/3.0" version="3.0">
  <query_result><body><query status="resolved">
    <doi type="journal_article">10.1177/17588359211061903</doi>
    <doi_record><crossref xmlns="http://www.crossref.org/xschema/1.1">
      <journal>
        <journal_metadata language="en">
          <full_title>Therapeutic Advances in Medical Oncology</full_title>
          <issn media_type="electronic">1758-8359</issn>
        </journal_metadata>
        <journal_issue><journal_volume><volume>13</volume></journal_volume></journal_issue>
        <journal_article publication_type="full_text">
          <titles><title>Retraction notice: Downregulation of long noncoding RNA LINC01419</title></titles>
          <publication_date media_type="online"><month>12</month><day>15</day><year>2021</year></publication_date>
          <crossmark>
            <crossmark_version>2</crossmark_version>
            <updates>
              <update type="retraction" date="2021-12-15">10.1177/1758835919874651</update>
              <update type="correction" date="2022-01-10">10.5555/also-corrected</update>
              <update type="new_version" date="2022-01-10">10.5555/newer</update>
              <update type="retraction" date="2021-12-15">10.1177/17588359211061903</update>
            </updates>
          </crossmark>
          <doi_data>
            <doi>10.1177/17588359211061903</doi>
            <resource>https://journals.sagepub.com/doi/10.1177/17588359211061903</resource>
          </doi_data>
        </journal_article>
      </journal>
    </crossref></doi_record>
  </query></body></query_result>
</crossref_result>"""


def test_crossref_xml_crossmark_updates_make_a_retraction():
    """Crossmark updates relate a notice to the works it retracts or corrects,
    asserted by the publisher; the first decides the notice type (as in
    commonmeta-rs' crossmark_updates_make_a_retraction)."""
    actual = convert("crossref_xml", "commonmeta", CROSSMARK_RETRACTION_XML)
    assert actual["type"] == "Retraction"
    updates = [r for r in actual["relations"] if r["type"] != "IsPartOf"]
    assert updates == [
        {
            "id": "https://doi.org/10.1177/1758835919874651",
            "type": "Retracts",
            "asserted_by": "Publisher",
        },
        {
            "id": "https://doi.org/10.5555/also-corrected",
            "type": "Corrects",
            "asserted_by": "Publisher",
        },
    ]
    assert json_schema_errors(actual) is None


def _retraction_notice() -> Metadata:
    expected_path = fixture_path("commonmeta", "crossref_retraction_notice.json")
    record = json.loads(read_text(expected_path))
    record["contributors"] = [
        {
            "type": "Person",
            "person": {"given_name": "Jo", "family_name": "Example"},
            "roles": ["Author"],
        }
    ]
    return Metadata(record, via="commonmeta")


def test_crossref_xml_writes_a_notice_as_a_journal_article():
    """Crossref deposits a retraction notice as a journal article."""
    subject = _retraction_notice()
    xml = subject.write(to="crossref_xml")
    assert "<journal_article" in xml
    assert subject.write_errors is None


def test_inveniordm_leaves_out_update_relations():
    """InvenioRDM's relation types are DataCite's, which have none for a
    retraction or correction."""
    subject = _retraction_notice()
    record = json.loads(subject.write(to="inveniordm"))
    relation_types = [
        r["relation_type"]["id"]
        for r in record["metadata"].get("related_identifiers", [])
    ]
    assert "retracts" not in relation_types
    assert subject.write_errors is None


def test_csl_writes_a_proceedings_article_as_a_conference_paper():
    expected_path = fixture_path("commonmeta", "csl_conference_paper.json")
    subject = Metadata(json.loads(read_text(expected_path)), via="commonmeta")
    record = json.loads(subject.write(to="csl"))
    assert record["type"] == "paper-conference"


@pytest.mark.parametrize(
    "name",
    ["csl_book.json", "csl_conference_paper.json", "crossref_retracted_article.json"],
)
def test_csl_and_datacite_writers_validate(name):
    """The CSL writer writes no license (CSL-JSON has no variable for one), and
    the DataCite writer writes publicationYear as the four-digit string its
    schema requires."""
    record = json.loads(read_text(fixture_path("commonmeta", name)))
    subject = Metadata(record, via="commonmeta")
    csl = json.loads(subject.write(to="csl"))
    assert subject.write_errors is None
    assert "copyright" not in csl and "license" not in csl
    datacite = json.loads(subject.write(to="datacite"))
    assert subject.write_errors is None
    assert datacite["publicationYear"] == record["date_published"][:4]
