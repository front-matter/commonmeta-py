"""ORCID reader for Commonmeta.

Reads ORCID 3.0 JSON and returns a commonmeta *person* entity. Accepts both the
full ``/record`` response - identity under ``person`` plus employments and
educations under ``activities-summary``, which become affiliations - and the
leaner ``/person`` response (identity only, no activities), which is also the
shape held by the local SQLite store. :func:`get_orcid` fetches ``/record``.

The equivalent for the ORCID XML data-file dumps is
:mod:`commonmeta.readers.orcid_xml_reader`.
"""

from __future__ import annotations

import requests

from ..base_utils import compact, dig, presence, wrap
from ..constants import ORCID_TO_CM_IDENTIFIER_TYPES, Commonmeta
from ..date_utils import get_date_from_unix_timestamp
from ..utils import normalize_orcid, validate_orcid


def get_orcid(pid: str | None, **kwargs) -> dict:
    """Fetch an ORCID record by ORCID ID or URL.

    Uses the ``/record`` endpoint (identity plus employments/educations) rather
    than ``/person``, so affiliations are carried; read_orcid accepts both shapes.
    """
    orcid = validate_orcid(pid)
    if orcid is None:
        return {"state": "not_found"}
    url = f"https://pub.orcid.org/v3.0/{orcid}/record"
    response = requests.get(
        url, headers={"Accept": "application/json"}, timeout=10, **kwargs
    )
    if response.status_code != 200:
        return {"state": "not_found"}
    return {**response.json(), "via": "orcid"}


def format_identifier(external_id: dict) -> dict | None:
    """Convert an ORCID external identifier to a commonmeta identifier.

    Shared with the XML reader: both shapes use external-id-type/-value.
    """
    id_type = external_id.get("external-id-type", None)
    identifier = external_id.get("external-id-value", None)
    if not id_type or not identifier:
        return None
    identifier_type = ORCID_TO_CM_IDENTIFIER_TYPES.get(id_type)
    return compact(
        {
            "identifier": identifier,
            "identifier_type": identifier_type or "Other",
            # An unmapped type keeps its ORCID name, which "Other" would lose.
            "scheme": None if identifier_type else id_type,
        }
    )


def display_name(given_name: str | None, family_name: str | None, credit: str | None):
    """The person's display name: the ORCID credit name, else given + family.

    Shared with the XML reader.
    """
    if credit:
        return credit
    return " ".join([i for i in (given_name, family_name) if i]) or None


def read_orcid(data: dict | None, **kwargs) -> Commonmeta:
    """read_orcid: ORCID 3.0 JSON -> commonmeta person entity.

    Handles both shapes ORCID serves: the full ``/record`` response (identity
    nested under ``person``, employments/educations under ``activities-summary``)
    and the leaner ``/person`` response (identity at the top level, no
    activities) - the latter is also what the local SQLite store holds.
    """
    if data is None:
        return {"state": "not_found"}
    read_options = kwargs or {}

    # A /record response wraps identity in "person" and adds "activities-summary";
    # a /person response (and the local store) is the person subtree on its own.
    is_record = "person" in data or "orcid-identifier" in data
    person = (data.get("person", None) if is_record else None) or data
    activities = data.get("activities-summary", None) if is_record else None

    # id: the record-level iD, else the person path's first segment. "path" is
    # "/0000-0003-1419-2405/person" from the API or the bare ORCID from the store.
    path = (
        (dig(data, "orcid-identifier.path") if is_record else None)
        or person.get("path", None)
        or ""
    )
    orcid = path.strip("/").split("/")[0]
    _id = normalize_orcid(orcid) if orcid else None

    name = person.get("name", None) or {}
    given_name = dig(name, "given-names.value")
    family_name = dig(name, "family-name.value")

    additional_names = [
        value
        for i in wrap(dig(person, "other-names.other-name"))
        if (value := i.get("content", None))
    ]

    identifiers = [
        identifier
        for i in wrap(dig(person, "external-identifiers.external-identifier"))
        if (identifier := format_identifier(i)) is not None
    ]

    urls = [
        compact({"name": i.get("url-name", None), "url": url})
        for i in wrap(dig(person, "researcher-urls.researcher-url"))
        if (url := dig(i, "url.value"))
    ]

    addresses = wrap(dig(person, "addresses.address"))
    country = dig(addresses[0], "country.value") if addresses else None

    # ORCID reports the last-modified date as milliseconds since the epoch here,
    # unlike the XML record, which carries an ISO 8601 string.
    last_modified = dig(person, "last-modified-date.value")
    date_updated = (
        get_date_from_unix_timestamp(last_modified // 1000)
        if isinstance(last_modified, int)
        else None
    )

    return {
        **compact(
            {
                "id": _id,
                "given_name": given_name,
                "family_name": family_name,
                "name": display_name(
                    given_name, family_name, dig(name, "credit-name.value")
                ),
                "additional_names": presence(additional_names),
                "description": dig(person, "biography.content"),
                "identifiers": presence(identifiers),
                "urls": presence(urls),
                "country": country,
                "affiliations": presence(read_record_affiliations(activities)),
                "date_updated": date_updated,
                "asserted_by": "ORCID",
            }
        ),
        **read_options,
    }


def read_record_affiliations(activities: dict | None) -> list:
    """Employments then educations from a /record JSON ``activities-summary``.

    The affiliation mapping (department folding, disambiguation ids, role, dates)
    is shared with the XML reader via ``format_affiliation``; only the /record
    JSON nesting differs - summaries sit one level deeper, under an
    ``affiliation-group[].summaries[]`` wrapper, and dates are ``{value}``-wrapped.
    """
    if not activities:
        return []
    # Lazy import: orcid_xml_reader imports display_name/format_identifier from
    # this module, so a top-level import would be circular.
    from .orcid_xml_reader import format_affiliation

    def flatten_date(date: dict | None) -> dict | None:
        if not date:
            return None
        return (
            compact(
                {part: dig(date, f"{part}.value") for part in ("year", "month", "day")}
            )
            or None
        )

    result = []
    for kind, role_prefix in (("employments", None), ("educations", "Education")):
        for group in wrap(dig(activities, f"{kind}.affiliation-group")):
            for entry in wrap(group.get("summaries", None)):
                summary = entry.get("employment-summary", None) or entry.get(
                    "education-summary", None
                )
                if not summary:
                    continue
                summary = {
                    **summary,
                    "start-date": flatten_date(summary.get("start-date", None)),
                    "end-date": flatten_date(summary.get("end-date", None)),
                }
                if (
                    affiliation := format_affiliation(summary, role_prefix)
                ) is not None:
                    result.append(affiliation)
    return result
