import re
import requests

def validate_doi(doi):
    """Validate a DOI"""
    m = re.search(r"\A(?:(http|https):/(/)?(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}/.+)\Z", doi)
    if m is None:
        return None
    return m.group(6)

def validate_prefix(doi):
    """Validate a DOI prefix for a given DOI"""
    m = re.search(r"\A(?:(http|https):/(/)?(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}).*\Z", doi)
    if m is None:
        return None
    return m.group(6)

def doi_as_url(doi):
    """Return a DOI as a URL"""
    if doi is None:
        return None
    return "https://doi.org/" + doi.lower()

def normalize_doi(doi, **kwargs):
    """Normalize a DOI"""
    doi_str = validate_doi(doi)
    if not doi_str:
        return None
    return doi_resolver(doi, **kwargs) + doi

def doi_resolver(doi, **kwargs):
    """Return a DOI resolver for a given DOI"""
    if doi is None:
        return None
    m = re.match(r"\A(?:(http|https):/(/)?(handle\.stage\.datacite\.org))", doi, re.IGNORECASE)
    if m is not None or kwargs.get('sandbox', False):
        return 'https://handle.stage.datacite.org/'
    else:
        return 'https://doi.org/'

def get_doi_ra(doi):
    """Return the DOI registration agency for a given DOI"""
    prefix = validate_prefix(doi)
    if prefix is None:
        return None
    response = requests.get("https://doi.org/ra/" + prefix)
    if response.status_code != 200:
        return None
    return response.json()[0].get('RA', None)
   