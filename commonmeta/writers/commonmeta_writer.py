"""Commonmeta writer for commonmeta-py"""
import json

from ..utils import pages_as_string, to_citeproc
from ..base_utils import wrap, presence, parse_attributes, compact
from ..date_utils import get_date_by_type, get_date_parts
from ..doi_utils import doi_from_url


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
            # recommended and optional properties
            "subjects": metadata.subjects,
            "contributors": metadata.contributors,
            "dates": metadata.dates,
            "language": metadata.language,
            "types": metadata.types,
            "references": metadata.references,
            # other properties
            "sizes": metadata.sizes,
            "formats": metadata.formats,
            "version": metadata.version,
            "rightsList": metadata.rights,
            "descriptions": metadata.descriptions,
            "geoLocations": metadata.geo_locations,
            "fundingReferences": metadata.funding_references
        }
    )
    return json.dumps(data, indent=4)
