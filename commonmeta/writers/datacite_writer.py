"""DataCite writer for commonmeta-py"""
import json
from typing import Optional

from ..base_utils import wrap, compact
from ..doi_utils import doi_from_url
from ..constants import (CM_TO_BIB_TRANSLATIONS, CM_TO_CSL_TRANSLATIONS, CM_TO_CR_TRANSLATIONS, CM_TO_DC_TRANSLATIONS, CM_TO_RIS_TRANSLATIONS, CM_TO_SO_TRANSLATIONS, Commonmeta)


def write_datacite(metadata: Commonmeta) -> Optional[str]:
    """Write datacite"""
    creators = [to_datacite_creator(i) for i in wrap(metadata.contributors) if i.get('contributorRoles', None) == ['Author']]
    contributors = [to_datacite_creator(i) for i in wrap(metadata.contributors) if i.get('contributorRoles', None) == ['Author']]
    related_items = [to_datacite_related_item(i) for i in wrap(metadata.references)]

    resource_type_general = CM_TO_DC_TRANSLATIONS.get(metadata.type, 'Other')
    resource_type = CM_TO_CR_TRANSLATIONS.get(metadata.type, 'Other')
    if resource_type_general == resource_type or resource_type_general in ['Dataset', 'JournalArticle', 'Other', 'Preprint', 'Software']:
        resource_type = None
    types = compact({
        "resourceTypeGeneral": resource_type_general,
        "resourceType": resource_type,
        "schemaOrg": CM_TO_SO_TRANSLATIONS.get(metadata.type, 'CreativeWork'),
        "citeproc": CM_TO_CSL_TRANSLATIONS.get(metadata.type, 'article'),
        "bibtex": CM_TO_BIB_TRANSLATIONS.get(metadata.type, 'misc'),
        "ris": CM_TO_RIS_TRANSLATIONS.get(metadata.type, 'GEN'),
    })
    publication_year = metadata.date.get('published')[:4] if metadata.date.get('published', None) else None
    
    def to_datacite_date(date: dict) -> dict:
        """Convert dates to datacite dates"""
        for k, v in date.items():
            return {
                "date": v,
                "dateType": k.title(),
            }
    dates = [to_datacite_date(i) for i in wrap(metadata.date)]

    license_ = [compact({
        "rightsIdentifier": metadata.license.get('id').lower() if metadata.license.get('id', None) else None,
        'rightsIdentifierScheme': 'SPDX',
        "rightsUri": metadata.license.get('url', None),
        'schemeUri': 'https://spdx.org/licenses/',
    })] if metadata.license else None

    data = compact(
        {
            "id": metadata.id,
            "doi": doi_from_url(metadata.id) if metadata.id else None,
            "url": metadata.url,
            "creators": creators,
            "titles": metadata.titles,
            "publisher": metadata.publisher,
            "publicationYear": publication_year,
            "subjects": metadata.subjects,
            "contributors": contributors,
            "dates": dates,
            "language": metadata.language,
            "types": types,
            "relatedItems": related_items,
            "sizes": metadata.sizes,
            "formats": metadata.formats,
            "version": metadata.version,
            "rightsList": license_,
            "descriptions": metadata.descriptions,
            "geoLocations": metadata.geo_locations,
            "fundingReferences": metadata.funding_references,
        }
    )
    return json.dumps(data, indent=4)


def to_datacite_creator(creator: dict) -> dict:
    """Convert creators to datacite creators"""
    type_ = creator.get("type", None)
    if creator.get("familyName", None):
        name = ", ".join([creator.get("familyName", ""), creator.get("givenName", "")])
    elif creator.get("name", None):
        name = creator.get("name", None)
    name_identifiers = creator.get("id", None)
    if name_identifiers:
        def format_name_identifier(name_identifier):
            return {
                "nameIdentifier": name_identifier,
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        name_identifiers = [
            format_name_identifier(i) for i in wrap(name_identifiers)
        ]
    return compact(
        {
            "name": name,
            "givenName": creator.get("givenName", None),
            "familyName": creator.get("familyName", None),
            "nameType": type_ + "al" if type_ else None,
            "nameIdentifiers": name_identifiers,
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
