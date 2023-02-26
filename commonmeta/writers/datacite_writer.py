"""DataCite writer for commonmeta-py"""
import json
from typing import Optional

from ..base_utils import wrap, compact
from ..constants import (CM_TO_BIB_TRANSLATIONS, CM_TO_CP_TRANSLATIONS, CM_TO_CR_TRANSLATIONS, CM_TO_DC_TRANSLATIONS, CM_TO_RIS_TRANSLATIONS, CM_TO_SO_TRANSLATIONS, Commonmeta)


def write_datacite(metadata: Commonmeta) -> Optional[str]:
    """Write datacite"""
    creators = [to_datacite_creator(i) for i in wrap(metadata.creators)]
    related_items = [to_datacite_related_item(i) for i in wrap(metadata.references)]

    resource_type_general = CM_TO_DC_TRANSLATIONS.get(metadata.type, 'Other')
    resource_type = CM_TO_CR_TRANSLATIONS.get(metadata.type, 'Other')
    if resource_type_general == resource_type or resource_type_general in ['Dataset', 'JournalArticle', 'Other', 'Preprint', 'Software']:
        resource_type = None
    types = compact({
        "resourceTypeGeneral": resource_type_general,
        "resourceType": resource_type,
        "schemaOrg": CM_TO_SO_TRANSLATIONS.get(metadata.type, 'CreativeWork'),
        "citeproc": CM_TO_CP_TRANSLATIONS.get(metadata.type, 'article'),
        "bibtex": CM_TO_BIB_TRANSLATIONS.get(metadata.type, 'misc'),
        "ris": CM_TO_RIS_TRANSLATIONS.get(metadata.type, 'GEN'),
    })

    data = compact(
        {
            "id": metadata.id,
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
            "types": types,
            "relatedItems": related_items,
            "sizes": metadata.sizes,
            "formats": metadata.formats,
            "version": metadata.version,
            "rightsList": metadata.rights,
            "descriptions": metadata.descriptions,
            "geoLocations": metadata.geo_locations,
            "fundingReferences": metadata.funding_references,
        }
    )
    return json.dumps(data, indent=4)


def to_datacite_creator(creator: dict) -> dict:
    """Convert creators to datacite creators"""
    if creator.get("familyName", None):
        name = ", ".join([creator.get("familyName", ""), creator.get("givenName", "")])
    elif creator.get("name", None):
        name = creator.get("name", None)
    return compact(
        {
            "name": name,
            "givenName": creator.get("givenName", None),
            "familyName": creator.get("familyName", None),
            "nameType": creator.get("nameType", None),
            "nameIdentifiers": creator.get("nameIdentifiers", None),
            "affiliation": creator.get("affiliation", None),
        }
    )


def to_datacite_related_item(reference: dict) -> dict:
    """Convert reference to datacite related_item"""
    doi = reference.get("doi", None)
    url = reference.get("url", None)
    return compact(
        {
            "relatedIdentifier": doi if doi else url,
            "relatedIdentifierType": "DOI" if doi else "URL",
            "relationType": "References",
        }
    )
