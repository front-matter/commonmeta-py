"""Commonmeta writer for commonmeta-py"""
import json
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
    return json.dumps(data, indent=4)


def write_commonmeta_list(metalist):
    """Write commonmeta list"""
    if metalist is None:
        return None

    # def format_commonmeta(item):
    #     item = py_.omit(item, ["via", "style", "locale", "doi", "depositor", "email", "registrant"])
    #     return vars(item)

    items = [vars(item) for item in metalist.items]
    return json.dumps(compact(items), indent=4)
