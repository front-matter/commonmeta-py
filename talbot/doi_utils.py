"""Doi utils for Talbot"""
import re
import requests


def validate_doi(doi):
    """Validate a DOI"""
    match = re.search(
        r"\A(?:(http|https):/(/)?(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}/.+)\Z",
        doi,
    )
    if match is None:
        return None
    return match.group(6)


def validate_prefix(doi):
    """Validate a DOI prefix for a given DOI"""
    match = re.search(
        r"\A(?:(http|https):/(/)?(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}).*\Z",
        doi,
    )
    if match is None:
        return None
    return match.group(6)


def doi_from_url(url):
    """Return a DOI from a URL"""
    match = re.search(
        r"\A(?:(http|https)://(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}/.+)\Z",
        url,
    )
    if match is None:
        return None
    return match.group(5).lower()


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
    return doi_resolver(doi, **kwargs) + doi_str.lower()


def doi_resolver(doi, **kwargs):
    """Return a DOI resolver for a given DOI"""
    if doi is None:
        return None
    match = re.match(
        r"\A(http|https):/(/)?handle\.stage\.datacite\.org", doi, re.IGNORECASE
    )
    if match is not None or kwargs.get("sandbox", False):
        return "https://handle.stage.datacite.org/"
    return "https://doi.org/"


def get_doi_ra(doi):
    """Return the DOI registration agency for a given DOI"""
    prefix = validate_prefix(doi)
    if prefix is None:
        return None
    response = requests.get("https://doi.org/ra/" + prefix)
    if response.status_code != 200:
        return None
    return response.json()[0].get("RA", None)
