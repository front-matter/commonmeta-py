"""ORCID writer for commonmeta-py.

Writes a commonmeta *person* entity as `ORCID 3.0 person JSON
<https://info.orcid.org/documentation/>`_ - the shape the ORCID API's
``/person`` endpoint serves, and the inverse of
:mod:`commonmeta.readers.orcid_reader`.

Only what commonmeta models is written. An ORCID person carries per-field
`visibility`, `source`, `put-code` and created/modified dates that commonmeta has
no home for, so reading is lossy and writing back cannot invent what was dropped.
Affiliations are not written: they live in an ORCID *record*, not a person, and
have no place in this shape.
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from ..base_utils import compact, presence, wrap
from ..constants import CM_TO_ORCID_IDENTIFIER_TYPES
from ..utils import validate_orcid

if TYPE_CHECKING:
    from ..metadata import Metadata


def write_orcid(metadata: Metadata | None) -> dict | None:
    """Write a commonmeta person as ORCID person JSON."""
    if metadata is None:
        return None
    if getattr(metadata, "entity_type", None) != "person":
        raise ValueError("Only person entities can be written as ORCID")

    orcid = validate_orcid(metadata.id)
    return compact(
        {
            "last-modified-date": presence(format_last_modified(metadata)),
            "name": presence(format_name(metadata, orcid)),
            "other-names": presence(format_other_names(metadata)),
            "biography": presence(format_biography(metadata)),
            "researcher-urls": presence(format_researcher_urls(metadata)),
            "external-identifiers": presence(format_external_identifiers(metadata)),
            "addresses": presence(format_addresses(metadata)),
            "path": f"/{orcid}/person" if orcid else None,
        }
    )


def format_last_modified(metadata: Metadata) -> dict:
    """ORCID reports dates as milliseconds since the epoch in person JSON."""
    date_updated = metadata.date_updated
    if not date_updated:
        return {}
    try:
        parsed = datetime.datetime.fromisoformat(date_updated.replace("Z", "+00:00"))
    except ValueError:
        return {}
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return {"value": int(parsed.timestamp() * 1000)}


def format_name(metadata: Metadata, orcid: str | None) -> dict:
    """The name block. `name` is only written as a credit name when it differs
    from "given family", which is what the reader derives when absent."""
    given_name = metadata.given_name
    family_name = metadata.family_name
    derived = " ".join([i for i in (given_name, family_name) if i]) or None
    credit_name = metadata.name if metadata.name != derived else None
    return compact(
        {
            "given-names": {"value": given_name} if given_name else None,
            "family-name": {"value": family_name} if family_name else None,
            "credit-name": {"value": credit_name} if credit_name else None,
            "path": orcid,
        }
    )


def format_other_names(metadata: Metadata) -> dict:
    """additional_names become other-names."""
    names = [{"content": i} for i in wrap(metadata.additional_names) if i]
    return {"other-name": names} if names else {}


def format_biography(metadata: Metadata) -> dict:
    """description is the person's biography."""
    return {"content": metadata.description} if metadata.description else {}


def format_researcher_urls(metadata: Metadata) -> dict:
    """urls become researcher-urls, whose url is a {"value": ...} wrapper."""
    urls = [
        compact({"url-name": url.get("name"), "url": {"value": url["url"]}})
        for url in wrap(metadata.urls)
        if url.get("url")
    ]
    return {"researcher-url": urls} if urls else {}


def format_external_identifiers(metadata: Metadata) -> dict:
    """identifiers become external-identifiers.

    An identifier written as "Other" kept its original ORCID type name in
    `scheme`, so that is restored here rather than emitting "Other".
    """
    identifiers = []
    for identifier in wrap(metadata.identifiers):
        value = identifier.get("identifier")
        if not value:
            continue
        id_type = CM_TO_ORCID_IDENTIFIER_TYPES.get(
            identifier.get("identifier_type")
        ) or identifier.get("scheme")
        if not id_type:
            continue
        identifiers.append({"external-id-type": id_type, "external-id-value": value})
    return {"external-identifier": identifiers} if identifiers else {}


def format_addresses(metadata: Metadata) -> dict:
    """country becomes the sole address; ORCID models a list."""
    if not metadata.country:
        return {}
    return {"address": [{"country": {"value": metadata.country}}]}
