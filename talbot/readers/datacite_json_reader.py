import requests
from pydash import py_
from datacite.errors import DataCiteForbiddenError, DataCiteGoneError, \
    DataCiteNoContentError, DataCiteNotFoundError, DataCiteServerError, \
    DataCiteUnauthorizedError
from datacite.rest_client import DataCiteRESTClient
from ..utils import (datacite_api_url, compact, presence, 
    parse_attributes, wrap, camel_case, sanitize, camel_case,
    normalize_url,
    CR_TO_BIB_TRANSLATIONS,
    CR_TO_SO_TRANSLATIONS,
    CR_TO_CP_TRANSLATIONS,
    CR_TO_RIS_TRANSLATIONS,
    DC_TO_SO_TRANSLATIONS,
    DC_TO_RIS_TRANSLATIONS,
    SO_TO_CP_TRANSLATIONS,
    SO_TO_BIB_TRANSLATIONS)
from ..author_utils import get_authors
from ..doi_utils import doi_as_url, get_doi_ra

def get_datacite_json(id=None, **kwargs):
    """get_datacite json"""
    if id is None:
        return { 'string': None, 'state': 'not_found' } 

    url = datacite_api_url(id)
    response = requests.get(url, kwargs)
    if response.status_code != 200:
        return { 'string': None, 'state': 'not_found' }
    return response.json().get('data', {}).get('attributes', {})

def read_datacite_json(string=None, **kwargs):
    """read_datacite json"""
    if string is None:
        return { 'meta': None, 'state': 'not_found' }
    meta = string

    id = doi_as_url(meta.get('doi', None))
    resource_type_general = py_.get(meta, 'types.resourceTypeGeneral', None)
    resource_type = py_.get(meta, 'types.resourceType', None)
    schema_org = CR_TO_SO_TRANSLATIONS.get(camel_case(resource_type), None) or DC_TO_SO_TRANSLATIONS.get(resource_type_general, None) or 'CreativeWork'
    types = compact({
        'resourceTypeGeneral': resource_type_general,
        'resourceType': resource_type,
        'schemaOrg': schema_org,
        'citeproc': CR_TO_CP_TRANSLATIONS.get(camel_case(resource_type), None) or SO_TO_CP_TRANSLATIONS.get(schema_org, None) or 'article',
        'bibtex': CR_TO_BIB_TRANSLATIONS.get(camel_case(resource_type), None) or SO_TO_BIB_TRANSLATIONS.get(schema_org, None) or 'misc',
        'ris': CR_TO_RIS_TRANSLATIONS.get(camel_case(resource_type), None) or DC_TO_RIS_TRANSLATIONS.get(resource_type_general, None) or 'GEN'
    })

    creators = get_authors(wrap(meta.get('creators', None)))
    contributors = get_authors(wrap(meta.get('contributors', None)))
    date_registered = None
 
    return {
        'id': id,
        'url': normalize_url(meta.get('url', None)),
        'types': types,
        'creators': creators,
        'contributors': contributors,
        'titles': compact(meta.get('titles', None)),
        'dates': presence(meta.get('dates', None)) or [{'date': meta.get('publicationYear', None), 'dateType': 'Issued'}],
        'publication_year': meta.get('publicationYear', None),
        'date_registered': date_registered,
        'publisher': meta.get('publisher', None),
        'rights_list': presence(meta.get('rightsList', None)),
        'issn': meta.get('issn', None),
        'container': meta.get('container', None),
        'related_identifiers': presence(meta.get('relatedIdentifiers', None)),
        'funding_references': meta.get('fundingReferences', None),
        'descriptions': meta.get('descriptions', None),
        'subjects': presence(meta.get('subjects', None)),
        'language': meta.get('language', None),
        'version_info': meta.get('version', None),
        'agency': 'DataCite' # get_doi_ra(id)
    }
  