"""ORCID reader for Commonmeta.

Reads ORCID 3.0 *person* JSON - the shape the ORCID API's ``/person`` endpoint
serves - and returns a commonmeta *person* entity.

A person carries names, biography, external ids, URLs and addresses, but no
employments, so it yields no affiliations. For those, read a full record XML with
:mod:`commonmeta.readers.orcid_xml_reader`.
"""

from __future__ import annotations

import requests

from ..base_utils import compact, dig, presence, wrap
from ..constants import ORCID_TO_CM_IDENTIFIER_TYPES, Commonmeta
from ..date_utils import get_date_from_unix_timestamp
from ..utils import normalize_orcid, validate_orcid


def get_orcid(pid: str | None, **kwargs) -> dict:
    """Fetch an ORCID person record by ORCID ID or URL."""
    orcid = validate_orcid(pid)
    if orcid is None:
        return {"state": "not_found"}
    url = f"https://pub.orcid.org/v3.0/{orcid}/person"
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
    """read_orcid: ORCID 3.0 person JSON -> commonmeta person entity"""
    if data is None:
        return {"state": "not_found"}
    meta = data
    read_options = kwargs or {}

    # "path" is "/0000-0003-1419-2405/person" from the API, or the bare ORCID
    # when the record came from a local store.
    path = meta.get("path", None) or ""
    orcid = path.strip("/").split("/")[0]
    _id = normalize_orcid(orcid) if orcid else None

    name = meta.get("name", None) or {}
    given_name = dig(name, "given-names.value")
    family_name = dig(name, "family-name.value")

    additional_names = [
        value
        for i in wrap(dig(meta, "other-names.other-name"))
        if (value := i.get("content", None))
    ]

    identifiers = [
        identifier
        for i in wrap(dig(meta, "external-identifiers.external-identifier"))
        if (identifier := format_identifier(i)) is not None
    ]

    urls = [
        compact({"name": i.get("url-name", None), "url": url})
        for i in wrap(dig(meta, "researcher-urls.researcher-url"))
        if (url := dig(i, "url.value"))
    ]

    addresses = wrap(dig(meta, "addresses.address"))
    country = dig(addresses[0], "country.value") if addresses else None

    # ORCID reports the last-modified date as milliseconds since the epoch here,
    # unlike the XML record, which carries an ISO 8601 string.
    last_modified = dig(meta, "last-modified-date.value")
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
                "description": dig(meta, "biography.content"),
                "identifiers": presence(identifiers),
                "urls": presence(urls),
                "country": country,
                "date_updated": date_updated,
                "asserted_by": "ORCID",
            }
        ),
        **read_options,
    }
