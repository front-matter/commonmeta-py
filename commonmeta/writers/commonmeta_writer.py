"""Commonmeta writer for commonmeta-py"""

import orjson as json
import orjsonl
import pydash as py_
import yaml

from ..base_utils import compact
from ..file_utils import get_extension, write_gz_file, write_zip_file


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
    return json.dumps(compact(data), option=json.OPT_INDENT_2)


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
    output = compact(
        {
            "id": metalist.id,
            "title": metalist.title,
            "description": metalist.description,
            "items": items,
        }
    )

    if metalist.file:
        filename, extension, compress = get_extension(metalist.file)
        if not extension:
            extension = "json"
        if extension == "jsonl":
            orjsonl.save(metalist.file, items)
        elif extension == "json":
            json_output = json.dumps(output).decode("utf-8")
            with open(metalist.file, "w") as file:
                file.write(json_output)
        elif extension == "yaml":
            yaml_output = yaml.dump(output).decode("utf-8")
            if compress == "gz":
                write_gz_file(filename, yaml_output)
            elif compress == "zip":
                write_zip_file(filename, yaml_output)
            else:
                with open(metalist.file, "w") as file:
                    file.write(yaml_output)
        return metalist.file
    else:
        return json.dumps(output).decode("utf-8")
