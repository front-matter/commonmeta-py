"""Date utils for Talbot"""
import datetime
from typing import Optional, Union
import dateparser
import pydash as py_
from .utils import wrap

MONTH_NAMES = {
    "01": "jan",
    "02": "feb",
    "03": "mar",
    "04": "apr",
    "05": "may",
    "06": "jun",
    "07": "jul",
    "08": "aug",
    "09": "sep",
    "10": "oct",
    "11": "nov",
    "12": "dec",
}


ISO8601_DATE_FORMAT = "%Y-%m-%d"


def get_iso8601_date(date: Union[datetime.datetime, datetime.date, str, int]) -> str:
    """Get ISO 8601 date without time"""
    if isinstance(date, (datetime.datetime, datetime.date)):
        return date.strftime(ISO8601_DATE_FORMAT)
    if isinstance(date, str):
        return dateparser.parse(date).strftime(ISO8601_DATE_FORMAT)
    if isinstance(date, int):
        return datetime.datetime.fromtimestamp(date).strftime(ISO8601_DATE_FORMAT)
    return ''


def get_date_by_type(dates: list, date_type="Issued", date_only=False) -> Optional[str]:
    """Get date by date type"""
    date = next((i for i in dates if i.get("dateType", None) == date_type), None)
    if not isinstance(date, dict):
        return None
    if date_only:
        return date.get("date", "")[0:10]
    return date.get("date", None)


def get_date_parts(iso8601_time: Optional[str]) -> dict:
    """Get date parts"""
    if iso8601_time is None:
        return {"date-parts": [[]]}

    # add 0s to the end of the date if it is incomplete
    if len(iso8601_time) < 10:
        iso8601_time = iso8601_time.ljust(10, "0")

    year = int(iso8601_time[0:4])
    month = int(iso8601_time[5:7])
    day = int(iso8601_time[8:10])

    date_parts = py_.reject([year, month, day], lambda x: x == 0)
    return {"date-parts": [date_parts]}


def get_date_from_date_parts(date_as_parts: Optional[dict]) -> Optional[str]:
    """Get date from date parts"""
    if date_as_parts is None:
        return None
    date_parts = date_as_parts.get("date-parts", [])
    if len(date_parts) == 0:
        return None
    date_parts = date_parts[0]
    if date_parts[0] is None:
        return None
    year = date_parts[0] if len(date_parts) > 0 else 0
    month = date_parts[1] if len(date_parts) > 1 else 0
    day = date_parts[2] if len(date_parts) > 2 else 0
    return get_date_from_parts(year, month, day)


def get_date_from_parts(year=0, month=0, day=0) -> Optional[str]:
    """Get date from parts"""
    arr = [str(year).rjust(4, "0"), str(
        month).rjust(2, "0"), str(day).rjust(2, "0")]
    arr = [e for i, e in enumerate(arr) if (e not in ["00", "0000"])]
    return None if len(arr) == 0 else "-".join(arr)


def get_month_from_date(date: Optional[Union[str, int, datetime.datetime, datetime.date]]) -> Optional[str]:
    """Get month from date"""
    if date is None:
        return None
    # if date type is not recognized
    if not isinstance(date, (str, int, datetime.datetime, datetime.date)):
        return None
    if isinstance(date, str):
        date = dateparser.parse(date).strftime(ISO8601_DATE_FORMAT)
    if isinstance(date, int):
        date = datetime.datetime.fromtimestamp(
            date).strftime(ISO8601_DATE_FORMAT)
    if isinstance(date, (datetime.datetime, datetime.date)):
        date = date.strftime(ISO8601_DATE_FORMAT)
    date = date.split("-")
    return MONTH_NAMES.get(date[1], None) if len(date) > 1 else None


def strip_milliseconds(iso8601_time: Optional[str]) -> Optional[str]:
    """strip milliseconds if there is a time, as it interferes with edtc parsing"""
    if iso8601_time is None or len(iso8601_time) == 0:
        return None
    if "T00:00:00" in iso8601_time:
        return iso8601_time.split("T")[0]
    if "+00:00" in iso8601_time:
        return iso8601_time.split("+")[0] + "Z"
    if "." in iso8601_time:
        return iso8601_time.split(".")[0] + "Z"

    return iso8601_time
