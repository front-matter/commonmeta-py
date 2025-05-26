"""Commonmeta writer for commonmeta-py"""

import pydash as py_

from ..base_utils import compact


def write_commonmeta(metadata):
    """Write commonmeta"""
    if metadata is None:
        return None

    data = py_.omit(
        vars(metadata),
        [
            "via",
            "is_valid",
            "date_created",
            "date_published",
            "date_registered",
            "date_updated",
            "state",
        ],
    )
    data = py_.rename_keys(
        data,
        {
            "additional_type": "additionalType",
            "archive_locations": "archiveLocations",
            "geo_locations": "geoLocations",
            "funding_references": "fundingReferences",
        },
    )
    return compact(data)


def write_commonmeta_list(metalist):
    """Write commonmeta list. If file is provided,
    write to file. Supports JSON, JSON Lines and YAML format."""
    if metalist is None:
        return None

    def format_item(item):
        """Format item for commonmeta list"""
        item = py_.omit(vars(item), ["via", "is_valid"])
        return compact(item)

    items = [format_item(item) for item in metalist.items]
    return compact(
        {
            "id": metalist.id,
            "title": metalist.title,
            "description": metalist.description,
            "items": items,
        }
    )
