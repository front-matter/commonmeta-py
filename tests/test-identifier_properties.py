"""Property-based tests for the DOI, ORCID, ISSN, ROR and URL helpers"""

import re

import pytest

# hypothesis is a dev dependency on Python 3.11+ only.
pytest.importorskip("hypothesis")

from hypothesis import given  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from commonmeta.doi_utils import (  # noqa: E402
    doi_as_url,
    doi_from_url,
    normalize_doi,
    validate_doi,
)
from commonmeta.utils import (  # noqa: E402
    from_curie,
    issn_as_url,
    issn_from_url,
    normalize_id,
    normalize_issn,
    normalize_orcid,
    normalize_ror,
    normalize_url,
    validate_orcid,
    validate_ror,
)

dois = st.builds(
    lambda prefix, suffix: f"10.{prefix}/{suffix}",
    st.integers(1000, 99999),
    st.from_regex(r"\A[a-z0-9][a-z0-9._;()/:-]{0,30}\Z"),
)


@given(dois)
def test_normalize_doi_is_idempotent(doi):
    normalized = normalize_doi(doi)
    assert normalized == f"https://doi.org/{doi}"
    assert normalize_doi(normalized) == normalized


@given(dois)
def test_doi_from_url_reverses_doi_as_url(doi):
    assert doi_from_url(doi_as_url(doi)) == doi


@given(dois)
def test_normalize_doi_ignores_case(doi):
    assert normalize_doi(doi.upper()) == normalize_doi(doi)


def orcid_check_character(digits: str) -> str:
    """ISO 7064 11,2 over the first fifteen digits."""
    total = 0
    for digit in digits:
        total = (total + int(digit)) * 2
    check = (12 - total % 11) % 11
    return "X" if check == 10 else str(check)


# The fifteen digits before the check character, in the ranges ORCID assigns
# from (0000-0001-5000-000 to 0000-0003-5000-000, 0009-0000-0000-000 to
# 0009-0010-0000-000), which is what idutils accepts.
orcids = st.one_of(
    st.integers(15000000, 35000000).map(lambda n: f"0000{n:011d}"),
    st.integers(0, 100000000).map(lambda n: f"0009{n:011d}"),
).map(
    lambda d: "-".join(
        (d + orcid_check_character(d))[i : i + 4] for i in range(0, 16, 4)
    )
)


@given(orcids)
def test_normalize_orcid_accepts_a_valid_orcid(orcid):
    normalized = normalize_orcid(orcid)
    assert normalized == f"https://orcid.org/{orcid}"
    assert normalize_orcid(normalized) == normalized
    assert normalize_orcid(orcid.replace("-", " ")) == normalized


@given(orcids, st.integers(0, 14), st.integers(1, 9))
def test_validate_orcid_rejects_a_mistyped_digit(orcid, position, change):
    """ISO 7064 11,2 catches every single changed digit."""
    digits = orcid.replace("-", "")
    digits = (
        digits[:position]
        + str((int(digits[position]) + change) % 10)
        + digits[position + 1 :]
    )
    mistyped = "-".join(digits[i : i + 4] for i in range(0, 16, 4))
    assert validate_orcid(mistyped) is None


issns = st.from_regex(r"\A\d{4}-\d{3}[\dX]\Z")


@given(issns)
def test_normalize_issn_keeps_an_issn(issn):
    assert normalize_issn(issn) == issn
    assert normalize_issn(issn.replace("-", "")) == issn
    assert normalize_issn(issn.lower()) == issn


@given(st.text(max_size=12))
def test_normalize_issn_answers_an_issn_or_none(string):
    normalized = normalize_issn(string)
    if normalized is not None:
        assert re.fullmatch(r"\d{4}-\d{3}[\dX]", normalized)
        assert normalize_issn(normalized) == normalized


@given(issns)
def test_issn_from_url_reverses_issn_as_url(issn):
    assert issn_from_url(issn_as_url(issn)) == issn


@given(st.text())
def test_helpers_never_raise_on_any_text(string):
    for helper in (
        validate_doi,
        normalize_doi,
        doi_from_url,
        validate_orcid,
        normalize_orcid,
        normalize_issn,
        validate_ror,
        normalize_ror,
        normalize_id,
        normalize_url,
        from_curie,
    ):
        helper(string)
