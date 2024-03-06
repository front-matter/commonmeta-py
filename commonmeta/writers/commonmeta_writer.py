"""Commonmeta writer for commonmeta-py"""
import orjson as json
import orjsonl
import pydash as py_
from ..base_utils import compact


def write_commonmeta(metadata):
    """Write commonmeta"""
    if metadata is None:
        return None

    data = compact(
        {
            # required properties
            "id": metadata.id,
            "type": metadata.type,
            "url": metadata.url,
            "contributors": metadata.contributors,
            "titles": metadata.titles,
            "publisher": metadata.publisher,
            "date": metadata.date,
            # recommended and optional properties
            "container": metadata.container,
            "subjects": metadata.subjects,
            "language": metadata.language,
            "references": metadata.references,
            "sizes": metadata.sizes,
            "formats": metadata.formats,
            "version": metadata.version,
            "license": metadata.license,
            "descriptions": metadata.descriptions,
            "geo_locations": metadata.geo_locations,
            "alternate_identifiers": metadata.alternate_identifiers,
            "relations": metadata.relations,
            "funding_references": metadata.funding_references,
            # other properties
            "files": metadata.files,
            "provider": metadata.provider,
            "schema_version": "https://commonmeta.org/commonmeta_v0.12",
        }
    )
    return json.dumps(data)


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
            "schema_version": "https://commonmeta.org/commonmeta_v0.12",
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
