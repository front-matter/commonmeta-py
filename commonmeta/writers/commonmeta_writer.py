"""Commonmeta writer for commonmeta-py"""

import orjson as json
import orjsonl
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
    return json.dumps(compact(data))


def write_commonmeta_list(metalist):
    """Write commonmeta list. If filename is provided,
    write to file. Optionally, use JSON Lines format."""
    if metalist is None:
        return None

    def format_item(item):
        """Format item for commonmeta list"""
        item = py_.omit(vars(item), ["via", "is_valid"])
        return compact(item)

    items = [format_item(item) for item in metalist.items]
    output = compact(
        {
            "id": metalist.id,
            "title": metalist.title,
            "description": metalist.description,
            "items": items,
        }
    )

    if metalist.filename and metalist.filename.rsplit(".", 1)[1] in ["jsonl", "json"]:
        if metalist.jsonlines:
            orjsonl.save(metalist.filename, items)
        else:
            json_output = json.dumps(output).decode("utf-8")
            with open(metalist.filename, "w") as file:
                file.write(json_output)
        return metalist.filename
    else:
        return json.dumps(output).decode("utf-8")
