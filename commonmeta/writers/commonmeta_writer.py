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
            "pid": metadata.pid,
            "doi": metadata.doi,
            "url": metadata.url,
            "creators": metadata.creators,
            "titles": metadata.titles,
            "publisher": metadata.publisher,
            "publicationYear": metadata.publication_year,
            "types": metadata.types,
            # recommended and optional properties
            "subjects": metadata.subjects,
            "contributors": metadata.contributors,
            "dates": metadata.dates,
            "language": metadata.language,
            "references": metadata.references,
            "sizes": metadata.sizes,
            "formats": metadata.formats,
            "version": metadata.version,
            "rights": metadata.rights,
            "descriptions": metadata.descriptions,
            "geoLocations": metadata.geo_locations,
            "fundingReferences": metadata.funding_references,
            # other properties
            "agency": metadata.agency,
        }
    )
    return json.dumps(data, indent=4)
