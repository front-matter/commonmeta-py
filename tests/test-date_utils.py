# pylint: disable=invalid-name
"""Test date utils"""
from datetime import date
import pytest  # noqa: F401

from commonmeta.date_utils import (
    get_iso8601_date,
    get_date_from_date_parts,
    get_date_from_parts,
    get_date_parts,
    get_month_from_date,
    get_date_from_crossref_parts,
    get_datetime_from_time,
    get_datetime_from_pdf_time,
)


def test_get_iso8601_date():
    """get_iso8601_date"""
    assert "2012-01-01" == get_iso8601_date("2012-01-01")
    assert "2012-01-01" == get_iso8601_date("2012-01-01T00:00:00Z")
    assert "2012-01-01" == get_iso8601_date("2012-01-01T00:00:00+00:00")
    assert "2012-01-01" == get_iso8601_date("2012-01-01T09:12:45+06:00")
    assert "2012-05-12" == get_iso8601_date("May 12, 2012")
    assert "2012-01-03" == get_iso8601_date("3. Januar 2012")
    assert "1972-09-09" == get_iso8601_date(84914841)
    assert "2020-05-17" == get_iso8601_date(date(2020, 5, 17))


def test_get_date_from_date_parts():
    "get_date_from_date_parts"
    assert "2012-01-01" == get_date_from_date_parts({"date-parts": [[2012, 1, 1]]})
    assert "2012-01" == get_date_from_date_parts({"date-parts": [[2012, 1]]})
    assert "2012" == get_date_from_date_parts({"date-parts": [[2012]]})
    assert None is get_date_from_date_parts({"date-parts": []})
    assert None is get_date_from_date_parts({"date-parts": [[None]]})
    assert None is get_date_from_date_parts({})
    assert None is get_date_from_date_parts(None)


def test_get_date_from_parts():
    "get_date_from_parts"
    assert "2012-01-01" == get_date_from_parts(2012, 1, 1)
    assert "2012-01" == get_date_from_parts(2012, 1)
    assert "2012" == get_date_from_parts(2012)
    assert None is get_date_from_parts()


def test_get_date_from_crossref_parts():
    """get_date_from_crossref_parts"""
    assert "2012-01-01" == get_date_from_crossref_parts(
        {"year": "2012", "month": "01", "day": "01"}
    )
    assert "2012-01" == get_date_from_crossref_parts({"year": "2012", "month": "01"})
    assert "2012" == get_date_from_crossref_parts({"year": "2012"})
    assert None is get_date_from_crossref_parts({})


def test_get_date_parts():
    "get_date_parts"
    assert {"date-parts": [[2012, 1, 1]]} == get_date_parts("2012-01-01")
    assert {"date-parts": [[2012, 1]]} == get_date_parts("2012-01")
    assert {"date-parts": [[2012]]} == get_date_parts("2012")
    assert {"date-parts": [[]]} == get_date_parts(None)


def test_get_month_from_date():
    """get month from date"""
    assert "jan" == get_month_from_date("2012-01-01")
    assert "jan" == get_month_from_date("2012-01-01T00:00:00Z")
    assert "jan" == get_month_from_date("2012-01-01T00:00:00+00:00")
    assert "jan" == get_month_from_date("2012-01-01T09:12:45+06:00")
    assert "may" == get_month_from_date("May 12, 2012")
    assert "jan" == get_month_from_date("3. Januar 2012")
    assert "sep" == get_month_from_date(84914841)
    assert "may" == get_month_from_date(date(2020, 5, 17))
    assert None is get_month_from_date(None)
    assert None is get_month_from_date([8])


def test_get_datetime_from_time():
    """get datetime from time"""
    # present
    time = "20200226071709"
    response = get_datetime_from_time(time)
    assert "2020-02-26T07:17:09Z" == response

    # past
    time = "18770312071709"
    response = get_datetime_from_time(time)
    assert "1877-03-12T07:17:09Z" == response

    # future
    time = "20970114071709"
    response = get_datetime_from_time(time)
    assert "2097-01-14T07:17:09Z" == response

    # invalid
    time = "20201587168864794"
    response = get_datetime_from_time(time)
    assert None is response


def test_get_datetime_from_pdf_time():
    """get datetime from pdf time"""
    # present
    time = "D:20180427082257+02'00'"
    response = get_datetime_from_pdf_time(time)
    assert "2018-04-27T08:22:57Z" == response
