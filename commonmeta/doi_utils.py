"""Doi utils for commonmeta-py"""

import re
from typing import Optional
import httpx
from furl import furl

from .base_utils import compact


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


def validate_suffix(doi: Optional[str]) -> Optional[str]:
    """Validate a DOI suffix for a given DOI"""
    if doi is None:
        return None
    match = re.search(
        r"\A(?:(http|https):/(/)?(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5})/(.+)\Z",  # noqa: E501
        doi,
    )
    if match is None:
        return None
    return match.group(7)


def doi_from_url(url: Optional[str]) -> Optional[str]:
    """Return a DOI from a URL"""
    if url is None:
        return None

    f = furl(url)
    # check for allowed scheme if string is a URL
    if f.host is not None and f.scheme not in ["http", "https", "ftp"]:
        return None

    # url is for a short DOI
    if f.host == "doi.org" and not f.path.segments[0].startswith("10."):
        return short_doi_as_doi(url)

    # special rules for specific hosts
    if f.host == "onlinelibrary.wiley.com":
        if f.path.segments[-1] in ["epdf"]:
            f.path.segments.pop()
    elif f.host == "www.plosone.org":
        if (
            f.path.segments[-1] in ["fetchobject.action"]
            and f.args.get("uri", None) is not None
        ):
            f.path = f.args.get("uri")
    path = str(f.path)
    match = re.search(
        r"(10\.\d{4,5}/.+)\Z",
        path,
    )
    if match is None:
        return None
    return match.group(0).lower()


def short_doi_as_doi(doi: Optional[str]) -> Optional[str]:
    """Resolve a short DOI"""
    if doi is None:
        return None
    response = httpx.head(doi_as_url(doi), timeout=10)
    if response.status_code != 301:
        return doi_as_url(doi)
    return response.headers.get("Location")


def doi_as_url(doi: Optional[str]) -> Optional[str]:
    """Return a DOI as a URL"""
    if doi is None:
        return None
    if furl(doi).host == "doi.org":
        return doi.lower()
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
    response = httpx.get("https://doi.org/ra/" + prefix, timeout=10)
    if response.status_code != 200:
        return None
    return response.json()[0].get("RA", None)


def get_crossref_member(member_id) -> Optional[dict]:
    """Return the Crossref member for a given member_id"""
    response = httpx.get("https://api.crossref.org/members/" + member_id, timeout=10)
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


def crossref_api_query_url(query: dict) -> str:
    """Return the Crossref API query URL"""
    url = "https://api.crossref.org/works"
    f = furl(url)
    rows = min(int(query.get("rows", 20)), 1000)
    queries = []
    filters = []
    if query.get("query", None) is not None:
        queries += [query.get("query")]
    for key, value in query.items():
        if key in [
            "query.bibliographic",
            "query.author",
            "query.title",
            "query.container-title",
        ]:
            queries += [f"{key}:{value}"]
        _query = ",".join(queries) if len(queries) > 0 else None

    for key, value in query.items():
        if key in [
            "prefix",
            "member",
            "type",
            "has-full-text",
            "has-references",
            "has-orcid",
            "has-funder",
            "has-license",
        ]:
            filters += [f"{key}:{value}"]
        _filter = ",".join(filters) if len(filters) > 0 else None
    f.args = compact({"rows": rows, "query": _query, "filter": _filter})

    return f.url


def crossref_api_sample_url(number: int = 1, **kwargs) -> str:
    """Return the Crossref API URL for a sample of works"""
    types = [
        "book-section",
        "monograph",
        "report-component",
        "report",
        "peer-review",
        "book-track",
        "journal-article",
        "book-part",
        "other",
        "book",
        "journal-volume",
        "book-set",
        "reference-entry",
        "proceedings-article",
        "journal",
        "component",
        "book-chapter",
        "proceedings-series",
        "report-series",
        "proceedings",
        "database",
        "standard",
        "reference-book",
        "posted-content",
        "journal-issue",
        "dissertation",
        "grant",
        "dataset",
        "book-series",
        "edited-book",
        "journal-section",
        "monograph-series",
        "journal-meta",
        "book-series-meta",
        "component-list",
        "journal-issue-meta",
        "journal-meta",
        "book-part-meta",
        "book-meta",
        "proceedings-meta",
        "book-series-meta",
        "book-set",
    ]
    url = f"https://api.crossref.org/works?sample={number}"
    if kwargs.get("prefix", None) and validate_prefix(kwargs.get("prefix")):
        url += f"&filter=prefix:{kwargs.get('prefix')}"
    if kwargs.get("_type", None) and kwargs.get("_type") in types:
        url += f"&filter=type:{kwargs.get('_type')}"
    return url


def datacite_api_url(doi: str, **kwargs) -> str:
    """Return the DataCite API URL for a given DOI"""
    match = re.match(
        r"\A(http|https):/(/)?handle\.stage\.datacite\.org", doi, re.IGNORECASE
    )
    if match is not None or kwargs.get("sandbox", False):
        return f"https://api.stage.datacite.org/dois/{doi_from_url(doi)}?include=media,client"
    return f"https://api.datacite.org/dois/{doi_from_url(doi)}?include=media,client"


def datacite_api_sample_url(number: int = 1, **kwargs) -> str:
    """Return the DataCite API URL for a sample of dois"""
    if kwargs.get("sandbox", False):
        return f"https://api.stage.datacite.org/dois?random=true&page[size]={number}"
    return f"https://api.datacite.org/dois?random=true&page[size]={number}"


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
