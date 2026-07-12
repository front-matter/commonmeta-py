"""Commonmeta writer for commonmeta-py"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base_utils import compact, omit, presence, wrap

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


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

    # contributors/relations have minItems: 1 - an empty list must be
    # omitted entirely rather than included, since compact() only drops
    # None.
    if "contributors" in data:
        data["contributors"] = presence(data["contributors"])
    if "relations" in data:
        data["relations"] = presence(data["relations"])

    # The v1.0 schema reference allows only: key, id, type, reference,
    # title, asserted_by. Strip internal fields (publication_year, volume,
    # issue, first_page, last_page, publisher, unstructured, etc.) and
    # map unstructured → reference when the reference field is absent.
    _REFERENCE_SCHEMA_KEYS = {"key", "id", "type", "reference", "title", "asserted_by"}
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
