"""Commonmeta writer for commonmeta-py"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base_utils import compact, omit, presence, wrap
from ..v1_compat import (
    v1_to_container,
    v1_to_contributor,
    v1_to_date,
    v1_to_descriptions,
    v1_to_files,
    v1_to_funding_reference,
    v1_to_geo_locations,
    v1_to_identifiers,
    v1_to_titles,
)

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


def write_commonmeta_records_for_rust(metalist: MetadataList | None) -> list:
    """Records for the commonmeta_rs FFI boundary (Parquet/archive writers).

    commonmeta_rs's Data struct deserializes JSON with `rename_all =
    "camelCase"` and hasn't been migrated to the v1.0 schema - it still
    expects the v0.18 shape (titles[]/descriptions[] arrays, a nested date
    object, camelCase keys). Metadata's attributes are v1.0-shaped, so
    unlike write_commonmeta_list(), this converts back to v0.18 shape for
    this one FFI boundary, on top of stripping the non-schema bookkeeping
    attributes.

    Currently unused: Metadata.write(to="parquet"/"zip"/"tgz") - the only
    callers - are disabled pending commonmeta-rs's own v1.0 migration. Once
    that's done, this function (and the v1.0->v0.18 conversion it does)
    becomes unnecessary, since commonmeta_rs will accept v1.0-shaped
    records directly.
    """
    if metalist is None:
        return []

    def to_v018(item) -> dict:
        data = omit(
            vars(item),
            [
                "via",
                "is_valid",
                "errors",
                "write_errors",
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

        if "additional_type" in data:
            data["additionalType"] = data.pop("additional_type")
        if "archive_locations" in data:
            data["archiveLocations"] = data.pop("archive_locations")

        data["titles"] = v1_to_titles(
            data.pop("title", None), data.pop("additional_titles", None)
        )
        data["descriptions"] = v1_to_descriptions(
            data.pop("description", None), data.pop("additional_descriptions", None)
        )
        data["date"] = v1_to_date(
            data.pop("date_published", None),
            data.pop("date_updated", None),
            data.pop("dates", None),
        )

        if "contributors" in data:
            data["contributors"] = presence(
                [v1_to_contributor(c) for c in wrap(data["contributors"])]
            )
        if "funding_references" in data:
            data["fundingReferences"] = [
                v1_to_funding_reference(f) for f in wrap(data.pop("funding_references"))
            ]
        if "container" in data:
            data["container"] = v1_to_container(data["container"])
        if "identifiers" in data:
            data["identifiers"] = v1_to_identifiers(data["identifiers"])
        if "files" in data:
            data["files"] = v1_to_files(data["files"])
        if "geo_locations" in data:
            data["geoLocations"] = v1_to_geo_locations(data.pop("geo_locations"))

        return compact(data)

    return [to_v018(item) for item in metalist.items]
