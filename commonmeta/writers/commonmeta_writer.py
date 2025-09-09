"""Commonmeta writer for commonmeta-py"""

from ..base_utils import compact, omit


def write_commonmeta(metadata):
    """Write commonmeta"""
    if metadata is None:
        return None

    data = omit(
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

    # Rename keys to camelCase
    key_mappings = {
        "additional_type": "additionalType",
        "archive_locations": "archiveLocations",
        "geo_locations": "geoLocations",
        "funding_references": "fundingReferences",
    }

    for old_key, new_key in key_mappings.items():
        if old_key in data:
            data[new_key] = data.pop(old_key)

    return compact(data)


def write_commonmeta_list(metalist):
    """Write commonmeta list. If file is provided,
    write to file. Supports JSON, JSON Lines and YAML format."""
    if metalist is None:
        return None

    def format_item(item):
        """Format item for commonmeta list"""
        item = omit(vars(item), ["via", "is_valid"])
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
