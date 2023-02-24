"""DataCite writer for commonmeta-py"""
import json
from typing import Optional
from pydash import py_

from ..utils import pages_as_string, to_citeproc
from ..base_utils import wrap, presence, parse_attributes, compact
from ..date_utils import get_date_by_type, get_date_parts
from ..doi_utils import doi_from_url
from ..constants import Commonmeta

def write_datacite(metadata: Optional[Commonmeta]) -> Optional[str]:
    """Write datacite"""
    if metadata is None:
        return None
    creators = [to_datacite_creator(i) for i in wrap(metadata.creators)]
    related_items = [to_datacite_related_item(i) for i in wrap(metadata.references)]

    data = compact(
        {
            "id": metadata.pid,
            "doi": metadata.doi,
            "url": metadata.url,
            "creators": creators,
            "titles": metadata.titles,
            "publisher": metadata.publisher,
            "publicationYear": metadata.publication_year,
            "subjects": metadata.subjects,
            "contributors": metadata.contributors,
            "dates": metadata.dates,
            "language": metadata.language,
            "types": metadata.types,
            "relatedItems": related_items,
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


def to_datacite_creator(creator: dict) -> dict:
    """Convert creators to datacite creators"""
    if creator.get('familyName', None):
        name = ', '.join([creator.get("familyName", ''), creator.get("givenName", '')])
    elif creator.get('name', None):
        name = creator.get("name", None)
    return compact({
        "name": name,
        "givenName": creator.get("givenName", None),
        "familyName": creator.get("familyName", None),
        "nameType": creator.get("nameType", None),
        "nameIdentifiers": creator.get("nameIdentifiers", None),
        "affiliation": creator.get("affiliation", None),
    })

def to_datacite_related_item(reference: dict) -> dict:
    """Convert reference to datacite related_item"""
    doi = reference.get('doi', None)
    url = reference.get('url', None)
    return compact({
        "relatedIdentifier": doi if doi else url,
        "relatedIdentifierType": "DOI" if doi else "URL",
        "relationType": "References",
    })
