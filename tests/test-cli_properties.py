"""Property-based tests for the encode and decode commands"""

import re

import pytest
from click.testing import CliRunner

# hypothesis is a dev dependency on Python 3.11+ only.
pytest.importorskip("hypothesis")

from hypothesis import given  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from commonmeta.cli import decode, encode  # noqa: E402

ENCODING_CHARS = "0123456789abcdefghjkmnpqrstvwxyz"

# A suffix is the base32 number plus a two digit checksum, padded with zeros to
# ten characters and split every five.
SUFFIX = re.compile(r"\A[0-9a-hjkmnp-tv-z]{5}(?:-[0-9a-hjkmnp-tv-z]{1,5})+\Z")

prefixes = st.from_regex(r"\A10\.[0-9]{4,5}\Z")
numbers = st.integers(min_value=1, max_value=2**64)


def invoke(command, args: list[str]) -> str:
    result = CliRunner().invoke(command, args)
    assert result.exit_code == 0, result.output
    return result.output.removesuffix("\n")


@given(prefixes, numbers)
def test_decode_reverses_encode(prefix, number):
    doi = invoke(encode, [prefix, "--number", str(number)])
    assert invoke(decode, [doi]) == str(number)


@given(prefixes, numbers)
def test_encode_a_number_gives_a_padded_suffix(prefix, number):
    doi = invoke(encode, [prefix, "--number", str(number)])
    head, suffix = doi.rsplit("/", maxsplit=1)
    assert head == f"https://doi.org/{prefix}"
    assert SUFFIX.match(suffix)
    assert len(suffix.replace("-", "")) >= 10


@given(prefixes, numbers)
def test_encode_a_number_is_deterministic(prefix, number):
    args = [prefix, "--number", str(number)]
    assert invoke(encode, args) == invoke(encode, args)


@given(prefixes)
def test_decode_reads_a_random_doi(prefix):
    doi = invoke(encode, [prefix])
    head, suffix = doi.rsplit("/", maxsplit=1)
    assert head == f"https://doi.org/{prefix}"
    assert len(suffix) == 11
    assert int(invoke(decode, [doi])) >= 0


@given(prefixes, numbers)
def test_decode_ignores_case_and_hyphens(prefix, number):
    doi = invoke(encode, [prefix, "--number", str(number)])
    head, suffix = doi.rsplit("/", maxsplit=1)
    assert invoke(decode, [f"{head}/{suffix.upper().replace('-', '')}"]) == str(number)


@given(prefixes, numbers, st.data())
def test_decode_rejects_a_mistyped_character(prefix, number, data):
    """The checksum catches every single substituted character, which then
    decodes as 0."""
    doi = invoke(encode, [prefix, "--number", str(number)])
    head, suffix = doi.rsplit("/", maxsplit=1)
    position = data.draw(st.sampled_from([i for i, c in enumerate(suffix) if c != "-"]))
    char = data.draw(st.sampled_from(ENCODING_CHARS.replace(suffix[position], "")))
    mistyped = suffix[:position] + char + suffix[position + 1 :]
    assert invoke(decode, [f"{head}/{mistyped}"]) == "0"


@given(st.text(min_size=1).filter(lambda s: not s.startswith("-")))
def test_decode_answers_a_number_for_any_text(text):
    assert int(invoke(decode, [text])) >= 0


@given(prefixes, st.integers(max_value=0))
def test_encode_refuses_a_number_below_one(prefix, number):
    result = CliRunner().invoke(encode, [prefix, "--number", str(number)])
    assert result.exit_code == 2
    assert "--number" in result.output
