"""Doi utils for commonmeta-py"""

import re
from typing import Optional

import base32_lib as base32
import requests
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
            uri = f.args.get("uri")
            if uri is not None:
                f.path.segments.clear()
                f.path.segments.append(uri)

    path = str(f.path).replace("%2F", "/")
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
    doi_url = doi_as_url(doi)
    if doi_url is None:
        return None
    response = requests.head(doi_url, timeout=10)
    if response.status_code != 301:
        return doi_url
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
    resolver = doi_resolver(doi, **kwargs)
    if resolver is None:
        return None
    return resolver + doi_str.lower()


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


def encode_doi(prefix, number: Optional[int] = None, checksum: bool = True) -> str:
    """Generate a DOI using the DOI prefix and a random base32 suffix"""
    if isinstance(number, int):
        suffix = base32.encode(number, split_every=5, checksum=checksum)
    else:
        suffix = base32.generate(length=10, split_every=5, checksum=True)
    return f"https://doi.org/{prefix}/{suffix}"


def decode_doi(doi: str, checksum: bool = True) -> int:
    """Decode a DOI to a number"""
    try:
        validated_doi = validate_doi(doi)
        if validated_doi is None:
            return 0
        suffix = validated_doi.split("/", maxsplit=1)[1]
        if checksum:
            number = base32.decode(suffix, checksum=True)
        else:
            number = base32.decode(suffix)
        return number
    except ValueError:
        return 0


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


def crossref_api_query_url(query: dict) -> str:
    """Return the Crossref API query URL"""
    url = "https://api.crossref.org/works"
    f = furl(url)
    rows = min(int(query.get("rows", 20)), 1000)
    queries = []
    filters = []
    _query = None
    _filter = None

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
    if queries:
        _query = ",".join(queries)

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
    if filters:
        _filter = ",".join(filters)

    f.args.update(compact({"rows": rows, "query": _query, "filter": _filter}))

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


def is_rogue_scholar_doi(doi: str, ra: str = "crossref") -> bool:
    """Check if a DOI is from Rogue Scholar with specific registration agency"""
    rogue_scholar_crossref_prefixes = [
        "10.13003",
        "10.53731",
        "10.54900",
        "10.59347",
        "10.59348",
        "10.59349",
        "10.59350",
        "10.63485",
        "10.64000",
        "10.64395",
    ]
    rogue_scholar_datacite_prefixes = [
        "10.5438",
        "10.34732",  # not managed by Front Matter
        "10.57689",  # not managed by Front Matter
        "10.58079",  # not managed by Front Matter
        "10.60804",
        "10.71938",  # not managed by Front Matter
        # "10.83132",
    ]

    prefix = validate_prefix(doi)
    if not prefix:
        return False

    is_crossref = prefix in rogue_scholar_crossref_prefixes
    is_datacite = prefix in rogue_scholar_datacite_prefixes

    if ra == "crossref":
        return is_crossref
    elif ra == "datacite":
        return is_datacite
    return is_crossref or is_datacite


def generate_wordpress_doi(prefix: str, slug: str, guid: str) -> str:
    """Generate a DOI from a WordPress GUID and slug"""

    if not prefix or not guid:
        return ""

    pattern = re.compile(r"p=(\d+)$")
    matched = pattern.search(guid)

    if matched:
        suffix = f"{slug}.{matched.group(1)}"
    else:
        # post_id not found, use random base32 encoding
        suffix = base32.generate(length=10, split_every=5, checksum=True)

    doi = f"https://doi.org/{prefix}/{suffix}"
    return doi


def validate_doi_from_guid(prefix: str, guid: str, checksum=True) -> bool:
    """Validates a GUID that is a DOI"""
    if not prefix:
        return False

    doi = normalize_doi(guid)
    if not doi:
        return False

    p = validate_prefix(doi)
    if not p or p != prefix:
        return False

    suffix = doi.split("/")[-1]

    try:
        number = base32.decode(suffix, checksum)
        return number != 0
    except (ValueError, IndexError):
        return False


def generate_substack_doi(prefix: str, slug: str, guid: str) -> str:
    """Generate a DOI from a Substack GUID and slug"""
    if not prefix or not slug or not guid:
        return ""

    # make sure guid is an integer
    try:
        _ = int(guid)
    except ValueError:
        return ""
    suffix = f"{slug}.{guid}"

    doi = f"https://doi.org/{prefix}/{suffix}"
    return doi
