"""Commonmeta writer for commonmeta-py"""
import orjson as json
import orjsonl
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
            "related_identifiers": metadata.related_identifiers,
            "funding_references": metadata.funding_references,
            # other properties
            "files": metadata.files,
            "provider": metadata.provider,
        }
    )
    return json.dumps(data)


def write_commonmeta_list(metalist):
    """Write commonmeta list. If filename is provided,
    write to file. Optionally, use JSON Lines format."""
    if metalist is None:
        return None

    items = [vars(item) for item in metalist.items]

    if metalist.filename and metalist.filename.endswith(".json"):
        if metalist.jsonlines:
            orjsonl.save(metalist.filename, items)
        else:
            json_items = json.dumps(items).decode("utf-8")
            with open(metalist.filename, "w") as file:
                file.write(json_items)
        return metalist.filename
    else:
        return json.dumps(items)
