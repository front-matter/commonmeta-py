"""Doi utils for commonmeta-py"""
import re
from typing import Optional
import requests


def validate_doi(doi: Optional[str]) -> Optional[str]:
    """Validate a DOI"""
    if doi is None:
        return None
    match = re.search(
        r"\A(?:(http|https):/(/)?(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}/.+)\Z",  # noqa: E501
        doi,
    )
    if match is None:
        return None
    return match.group(6)


def validate_prefix(doi: Optional[str]) -> Optional[str]:
    """Validate a DOI prefix for a given DOI"""
    if doi is None:
        return None
    match = re.search(
        r"\A(?:(http|https):/(/)?(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}).*\Z",  # noqa: E501
        doi,
    )
    if match is None:
        return None
    return match.group(6)


def doi_from_url(url: str) -> Optional[str]:
    """Return a DOI from a URL"""
    match = re.search(
        r"\A(?:(http|https)://(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}/.+)\Z",
        url,
    )
    if match is None:
        return None
    return match.group(5).lower()


def doi_as_url(doi: Optional[str]) -> Optional[str]:
    """Return a DOI as a URL"""
    if doi is None:
        return None
    return "https://doi.org/" + doi.lower()


def normalize_doi(doi: Optional[str], **kwargs) -> Optional[str]:
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


def get_doi_ra(doi) -> Optional[str]:
    """Return the DOI registration agency for a given DOI"""
    prefix = validate_prefix(doi)
    if prefix is None:
        return None
    response = requests.get("https://doi.org/ra/" + prefix, timeout=10)
    if response.status_code != 200:
        return None
    return response.json()[0].get("RA", None)


def get_crossref_member(member_id) -> Optional[dict]:
    """Return the Crossref member for a given member_id"""
    response = requests.get("https://api.crossref.org/members/" + member_id, timeout=10)
    if response.status_code != 200:
        return None
    data = response.json().get("message", None)
    name = data.get("primary-name", None)
    return {"id": "https://api.crossref.org/members/" + member_id, "name": name}


def crossref_api_url(doi: str) -> str:
    """Return the Crossref API URL for a given DOI"""
    return "https://api.crossref.org/works/" + doi


def crossref_xml_api_url(doi: str) -> str:
    """Return the Crossref XML API URL for a given DOI"""
    return f"https://api.crossref.org/works/{doi}/transform/application/vnd.crossref.unixsd+xml"


def datacite_api_url(doi: str, **kwargs) -> str:
    """Return the DataCite API URL for a given DOI"""
    match = re.match(
        r"\A(http|https):/(/)?handle\.stage\.datacite\.org", doi, re.IGNORECASE
    )
    if match is not None or kwargs.get("sandbox", False):
        return f"https://api.stage.datacite.org/dois/{doi_from_url(doi)}?include=media,client"
    return f"https://api.datacite.org/dois/{doi_from_url(doi)}?include=media,client"


def is_rogue_scholar_doi(doi: str) -> bool:
    """Return True if DOI is from Rogue Scholar"""
    prefix = validate_prefix(doi)
    return prefix in [
        "10.34732",
        "10.53731",
        "10.54900",
        "10.57689",
        "10.59348",
        "10.59349",
        "10.59350",
    ]
