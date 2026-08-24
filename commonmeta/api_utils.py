"""API Utils module for commonmeta-py"""

from __future__ import annotations

from datetime import datetime as date

import jwt
import requests
from furl import furl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .base_utils import dig
from .doi_utils import doi_as_url, doi_from_url

# User-Agent for API requests
COMMONMETA_USER_AGENT = (
    "commonmeta-py (https://commonmeta.org/; mailto:info@front-matter.de)"
)

# Shared HTTP session with retry strategy for API calls
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 502, 503, 504],
    allowed_methods=["GET", "POST", "PUT"],
    backoff_factor=2,
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
# Say who we are on every request, not only on the ones that remember to.
# Servers behind a filter answer the default "python-requests/x.y" with 406
# Not Acceptable, which is what a blog's feature image came back as. A header
# passed to a single request still overrides this.
http.headers["User-Agent"] = COMMONMETA_USER_AGENT


def get_session_with_retry(
    *,
    total: int = 3,
    status_forcelist: list[int] | None = None,
    allowed_methods: list[str] | None = None,
    backoff_factor: float = 2.0,
) -> requests.Session:
    """Return a new requests.Session configured with a custom Retry.

    Use this when a specific API call needs different retry behavior
    (e.g., a different `status_forcelist`). It does not alter the shared
    global session `http`.
    """
    retry = Retry(
        total=total,
        status_forcelist=status_forcelist or [429, 502, 503, 504],
        allowed_methods=allowed_methods or ["GET", "POST", "PUT"],
        backoff_factor=backoff_factor,
    )
    _adapter = HTTPAdapter(max_retries=retry)
    _session = requests.Session()
    _session.mount("https://", _adapter)
    _session.mount("http://", _adapter)
    return _session


def generate_ghost_token(key: str) -> str:
    """Generate a short-lived JWT for the Ghost Admin API.
    From https://ghost.org/docs/admin-api/#token-authentication"""

    # Split the key into ID and SECRET
    try:
        _id, secret = key.split(":")
    except ValueError:
        raise ValueError("Invalid API key format. Expected format: 'id:secret'")

    # Prepare header and payload
    iat = int(date.now().timestamp())

    header = {"alg": "HS256", "typ": "JWT", "kid": _id}
    payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/admin/"}

    # Create and return the token (including decoding secret)
    return jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers=header)


def get_post_url(doi: str | None, host: str = "rogue-scholar.org") -> str | None:
    """Look a post's url up in InvenioRDM by DOI.

    Replaces the lookup against api.rogue-scholar.org that the JSON Feed
    reader used to provide. The records search is public, so no token is
    needed; the post url is the ``url`` identifier on the record.
    """
    doi = doi_from_url(doi)
    if not doi:
        return None
    try:
        response = http.get(
            f"https://{host}/api/records",
            params={"q": f'doi:"{doi}"', "size": 1},
            headers={"User-Agent": COMMONMETA_USER_AGENT},
            timeout=10,
        )
        response.raise_for_status()
        record = dig(response.json(), "hits.hits.0")
    except (requests.exceptions.RequestException, ValueError):
        return None
    if not record:
        return None
    return next(
        (
            i.get("identifier")
            for i in dig(record, "metadata.identifiers") or []
            if i.get("scheme") == "url"
        ),
        None,
    )


def update_ghost_post_via_api(
    doi: str,
    api_key: str | None = None,
    api_url: str | None = None,
    host: str = "rogue-scholar.org",
) -> dict[str, str]:
    """Update Ghost post via API"""
    # Check required parameters
    if not api_key or not api_url:
        return {"error": "api_key and api_url are required"}

    # get post url from InvenioRDM, needed to find the post via the Ghost API
    url = get_post_url(doi, host=host)
    doi = doi_as_url(doi)
    if not doi or not url:
        return {"error": "DOI or URL not found"}

    # get post_id and updated_at from ghost api
    token = generate_ghost_token(api_key)
    headers = {
        "Authorization": f"Ghost {token}",
        "Content-Type": "application/json",
        "Accept-Version": "v5",
    }
    f = furl(url)
    if not f.path.segments:
        return {"error": "Invalid URL: no path segments found"}
    slug = f.path.segments[-1]
    ghost_url = f"{api_url}/ghost/api/admin/posts/slug/{slug}/"

    try:
        response = requests.get(ghost_url, headers=headers, timeout=10)
    except requests.RequestException as e:
        return {"error": f"Network error fetching post: {str(e)}"}

    if response.status_code != 200:
        return {"error": "Error fetching post"}

    try:
        posts = response.json().get("posts")
    except requests.JSONDecodeError:
        return {"error": "Invalid JSON response from Ghost API"}

    if not posts or not isinstance(posts, list) or len(posts) == 0:
        return {"error": "No posts found in response"}

    ghost_post = posts[0]
    guid = ghost_post.get("id")
    updated_at = ghost_post.get("updated_at")
    if not guid or not updated_at:
        return {"error": "guid or updated_at not found"}

    # update post canonical_url using doi. This requires sending
    # the updated_at timestamp to avoid conflicts, and must use guid
    # rather than url for put requests
    ghost_url = f"{api_url}/ghost/api/admin/posts/{guid}/"

    request_data = {"posts": [{"canonical_url": doi, "updated_at": updated_at}]}
    try:
        response = requests.put(
            ghost_url,
            headers=headers,
            json=request_data,
            timeout=10,
        )
    except requests.RequestException as e:
        return {"error": f"Network error updating post: {str(e)}"}

    if response.status_code != 200:
        return {"error": "Error updating post"}
    return {"message": f"DOI {doi} added", "guid": guid, "updated_at": updated_at}
