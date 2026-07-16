"""Commonmeta writer for commonmeta-py"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ..base_utils import compact, omit, presence, wrap
from ..schema_utils import COMMONMETA_SCHEMA_URI

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


def collapse_whitespace(text):
    """Collapse runs of internal whitespace (newlines, indentation) to a
    single space, matching sanitize() applied by the format readers. Keeps
    descriptions normalized regardless of source formatting (e.g. indented
    multi-line XML elements)."""
    if not isinstance(text, str):
        return text
    return " ".join(re.split(r"\s+", text, flags=re.UNICODE)).strip()


def write_commonmeta(metadata: Metadata | None) -> dict | None:
    """Write commonmeta."""
    if metadata is None:
        return None

    # date_created/date_registered are vestigial registration-timestamp
    # attributes, distinct from the public date_published/date_updated/
    # dates. The rest are internal bookkeeping (registration credentials,
    # validation state) that aren't part of the commonmeta schema -
    # commonmeta.additionalProperties is false, so any of these leaking
    # through fails validation.
    data = omit(
        vars(metadata),
        [
            "via",
            "entity_type",
            "_validate",
            "_no_network",
            "is_valid",
            "errors",
            "write_errors",
            "date_created",
            "date_registered",
            "state",
            "depositor",
            "email",
            "registrant",
            "login_id",
            "login_passwd",
            "test_mode",
            "host",
            "token",
            "legacy_conn",
        ],
    )

    # Declare the schema the record is encoded against. The schema pins this to
    # a const, so it's stamped from COMMONMETA_SCHEMA_URI rather than carried
    # through from the input - a record read from an older commonmeta document
    # is re-serialized against the version we write. Works only: person and
    # organization don't define the property.
    if getattr(metadata, "entity_type", "work") == "work":
        data["schema_version"] = COMMONMETA_SCHEMA_URI

    # The top-level id already carries the canonical DOI, so an identifiers entry
    # repeating it as a DOI is redundant. Only the DOI-typed duplicate is
    # dropped: a non-DOI identifier that happens to equal the id (e.g. a jsonfeed
    # GUID) is kept, because its type carries meaning the id doesn't.
    if data.get("identifiers"):
        data["identifiers"] = presence(
            [
                i
                for i in wrap(data["identifiers"])
                if not (
                    i.get("identifier") == data.get("id")
                    and i.get("identifier_type") == "DOI"
                )
            ]
        )

    # contributors/relations have minItems: 1 - an empty list must be
    # omitted entirely rather than included, since compact() only drops
    # None.
    if "contributors" in data:
        data["contributors"] = presence(data["contributors"])
    if "relations" in data:
        data["relations"] = presence(data["relations"])

    # The v1.0 schema reference allows only: key, id, type, reference,
    # asserted_by. Strip internal fields (publication_year, volume,
    # issue, first_page, last_page, publisher, title, unstructured, etc.) and
    # map unstructured → reference when the reference field is absent.
    _REFERENCE_SCHEMA_KEYS = {"key", "id", "type", "reference", "asserted_by"}
    if data.get("references"):
        cleaned = []
        for r in wrap(data["references"]):
            ref = {k: v for k, v in r.items() if k in _REFERENCE_SCHEMA_KEYS}
            if "reference" not in ref:
                fallback = r.get("unstructured") or r.get("reference")
                if fallback:
                    ref["reference"] = fallback
            cleaned.append(compact(ref))
        data["references"] = presence(cleaned)

    # Normalize whitespace in descriptions so output is independent of the
    # source's formatting (e.g. indented multi-line XML descriptions). Works
    # only: a person's description is their biography, where the line breaks are
    # authored content rather than an artifact of the source markup.
    if getattr(metadata, "entity_type", "work") == "work":
        if data.get("description"):
            data["description"] = collapse_whitespace(data["description"])
        if data.get("additional_descriptions"):
            for d in wrap(data["additional_descriptions"]):
                if isinstance(d, dict) and d.get("description"):
                    d["description"] = collapse_whitespace(d["description"])

    return compact(data)


def write_commonmeta_list(metalist: MetadataList | None) -> dict | None:
    """Write commonmeta list. If file is provided,
    write to file. Supports JSON, JSON Lines and YAML format."""
    if metalist is None:
        return None

    items = [write_commonmeta(item) for item in metalist.items]
    return compact(
        {
            "id": metalist.id,
            "title": metalist.title,
            "description": metalist.description,
            "items": items,
        }
    )
