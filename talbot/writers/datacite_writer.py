"""DataCite writer for Talbot"""
import json
from typing import Optional

from ..utils import pages_as_string, to_citeproc
from ..base_utils import wrap, presence, parse_attributes, compact
from ..date_utils import get_date_by_type, get_date_parts
from ..doi_utils import doi_from_url
from ..constants import TalbotMeta

def write_datacite(metadata: Optional[TalbotMeta]) -> Optional[dict]:
    """Write datacite"""
    if metadata is None:
        return None

    dictionary = compact(
        {
            "id": metadata.pid,
            "doi": metadata.doi,
            "url": metadata.url,
            "creators": to_datacite_creators(metadata.creators),
            "titles": metadata.titles,
            "publisher": metadata.publisher,
            "publicationYear": metadata.publication_year,
            "subjects": metadata.subjects,
            "contributors": metadata.contributors,
            "dates": metadata.dates,
            "language": metadata.language,
            "types": metadata.types,
            "relatedItems": metadata.related_items,
            "sizes": metadata.sizes,
            "formats": metadata.formats,
            "version": metadata.version,
            "rightsList": metadata.rights,
            "descriptions": metadata.descriptions,
            "geoLocations": metadata.geo_locations,
            "fundingReferences": metadata.funding_references
        }
    )
    return json.dumps(dictionary, indent=4)


def to_datacite_creators(creators: list) -> list:
    """Convert creators to datacite creators"""
    formatted_creators = []
    for creator in wrap(creators):
        if creator.get('familyName', None):
            name = ', '.join([creator.get("familyName", ''), creator.get("givenName", '')])
        elif creator.get('name', None):
            name = creator.get("name", None)
        cre = {
            "name": name,
            "givenName": creator.get("givenName", None),
            "familyName": creator.get("familyName", None),
            "nameType": creator.get("nameType", None),
            "nameIdentifiers": creator.get("nameIdentifiers", None),
            "affiliation": creator.get("affiliation", None),
        }
        formatted_creators.append(compact(cre))
    return formatted_creators