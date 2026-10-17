"""Property-based tests for the date helpers"""

import datetime

import pytest

# hypothesis is a dev dependency on Python 3.11+ only.
pytest.importorskip("hypothesis")

from hypothesis import given  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from commonmeta.date_utils import (  # noqa: E402
    get_date_from_date_parts,
    get_date_from_parts,
    get_date_from_unix_timestamp,
    get_date_parts,
    get_iso8601_date,
    strip_milliseconds,
)

dates = st.dates(min_value=datetime.date(1, 1, 1))


@given(dates)
def test_get_date_from_date_parts_reverses_get_date_parts(date):
    iso = date.isoformat()
    assert get_date_from_date_parts(get_date_parts(iso)) == iso


@given(dates)
def test_get_date_parts_reads_year_and_month(date):
    """A date with a month and no day, or with neither, keeps what it has."""
    iso = date.isoformat()
    for partial in (iso[:7], iso[:4]):
        assert get_date_from_date_parts(get_date_parts(partial)) == partial


@given(st.integers(1, 9999), st.integers(1, 12), st.integers(1, 28))
def test_get_date_from_parts_pads(year, month, day):
    assert get_date_from_parts(year, month, day) == f"{year:04d}-{month:02d}-{day:02d}"
    assert get_date_from_parts(year, month) == f"{year:04d}-{month:02d}"
    assert get_date_from_parts(year) == f"{year:04d}"


@given(st.integers(-(2**34), 2**34))
def test_get_date_from_unix_timestamp_is_utc(timestamp):
    expected = datetime.datetime(
        1970, 1, 1, tzinfo=datetime.timezone.utc
    ) + datetime.timedelta(seconds=timestamp)
    assert get_date_from_unix_timestamp(timestamp) == expected.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


@given(st.datetimes(min_value=datetime.datetime(1000, 1, 1)))
def test_get_iso8601_date_starts_with_the_date(value):
    assert get_iso8601_date(value).startswith(value.date().isoformat())


@given(
    st.datetimes(min_value=datetime.datetime(1000, 1, 1)),
    st.integers(1, 999999),
)
def test_strip_milliseconds_drops_the_fraction(value, microseconds):
    """A time at midnight is taken for no time at all, and dropped with it."""
    stamp = value.replace(microsecond=microseconds).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if value.replace(microsecond=0).time() == datetime.time(0, 0):
        assert strip_milliseconds(stamp) == value.date().isoformat()
    else:
        assert strip_milliseconds(stamp) == value.strftime("%Y-%m-%dT%H:%M:%SZ")


@given(st.text(max_size=40))
def test_date_helpers_never_raise_on_any_text(string):
    """Feeds carry dates as they please; one that will not read is no date."""
    get_iso8601_date(string)
    get_date_parts(string)
    strip_milliseconds(string)
