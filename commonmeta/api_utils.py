"""API Utils module for commonmeta-py"""

from typing import Optional
from datetime import datetime as date
import httpx
from furl import furl
import jwt

from .doi_utils import validate_doi, doi_as_url
from .readers.json_feed_reader import get_json_feed_item_uuid


def generate_ghost_token(key: str) -> str:
    """Generate a short-lived JWT for the Ghost Admin API.
    From https://ghost.org/docs/admin-api/#token-authentication"""

    # Split the key into ID and SECRET
    _id, secret = key.split(":")

    # Prepare header and payload
    iat = int(date.now().timestamp())

    header = {"alg": "HS256", "typ": "JWT", "kid": _id}
    payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/admin/"}

    # Create and return the token (including decoding secret)
    return jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers=header)


def update_ghost_post_via_api(
    _id: str, api_key: Optional[str] = None, api_url: Optional[str] = None
) -> dict[str, str]:
    """Update Ghost post via API"""
    # get post doi and url from Rogue Scholar API
    # post url is needed to find post via Ghost API
    post = get_json_feed_item_uuid(_id)
    if post.get("error", None):
        return post
    doi = validate_doi(post.get("doi", None))
    doi = doi_as_url(doi)
    url = post.get("url", None)
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
    slug = f.path.segments[-1]
    ghost_url = f"{api_url}/ghost/api/admin/posts/slug/{slug}/"
    response = httpx.get(ghost_url, headers=headers, timeout=10)
    if response.status_code != 200:
        return {"error": "Error fetching post"}
    ghost_post = response.json().get("posts")[0]
    guid = ghost_post.get("id")
    updated_at = ghost_post.get("updated_at")
    if not guid or not updated_at:
        return {"error": "guid or updated_at not found"}

    # update post canonical_url using doi. This requires sending
    # the updated_at timestamp to avoid conflicts, and must use guid
    # rather than url for put requests
    ghost_url = f"{api_url}/ghost/api/admin/posts/{guid}/"

    json = {"posts": [{"canonical_url": doi, "updated_at": updated_at}]}
    response = httpx.put(
        ghost_url,
        headers=headers,
        json=json,
    )
    if response.status_code != 200:
        return {"error": "Error updating post"}
    return {"message": f"DOI {doi} added", "guid": guid, "updated_at": updated_at}
