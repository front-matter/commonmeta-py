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

import pytest
from conformance_common import (
    assert_golden_or_xfail,
    canonical_commonmeta_value,
    collect_json,
    convert,
    convert_or_xfail,
    diff,
    fixture_path,
    pair_id,
    read_text,
    reader_pairs,
    writer_pairs,
)

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
