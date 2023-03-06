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
            "creators": metadata.creators,
            "titles": metadata.titles,
            "publisher": metadata.publisher,
            "date": metadata.date,
            # recommended and optional properties
            "subjects": metadata.subjects,
            "contributors": metadata.contributors,
            "language": metadata.language,
            "references": metadata.references,
            "sizes": metadata.sizes,
            "formats": metadata.formats,
            "version": metadata.version,
            "license": metadata.license,
            "descriptions": metadata.descriptions,
            "geoLocations": metadata.geo_locations,
            "fundingReferences": metadata.funding_references,
            # other properties
            "provider": metadata.provider,
        }
    )
    return json.dumps(data, indent=4)
