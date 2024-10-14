"""Test api utils"""
import pytest  # noqa: F401
import jwt
from datetime import datetime as date

from commonmeta.api_utils import (
    generate_ghost_token,
    update_ghost_post_via_api,
)


def test_generate_ghost_token():
    "generate_ghost_token"
    _id = "abc"
    key = b"secret"
    token = generate_ghost_token(f"{_id}:{key.hex()}")
    decoded_token = jwt.decode(token, key, algorithms="HS256", audience="/admin/")
    assert decoded_token["iat"] == int(date.now().timestamp())


def test_generate_ghost_token_broken_key():
    "generate_ghost_token broken key"
    _id = "abc"
    key = "secret"
    with pytest.raises(ValueError):
        generate_ghost_token(f"{_id}:{key}")


# def test_update_ghost_post_via_api():
#     "update_ghost_post_via_api"
#     _id = "d0ca6fa3-3a93-46d3-b820-446938d78f70"
#     api_key = "abc"
#     api_url = "https://front-matter.ghost.io"

#     assert {
#         "guid": "62d42bbd41e317003df48d61",
#         "message": "DOI https://doi.org/10.53731/r294649-6f79289-8cw06 added",
#         "updated_at": "2023-09-01T22:07:56.000Z",
#     } == update_ghost_post_via_api(_id, api_key, api_url)


def test_update_ghost_post_via_api__idnot_found():
    "update_ghost_post_via_api id not found"
    _id = "abc"
    api_key = "def"
    api_url = "https://example.com"

    assert {"error": "An error occured."} == update_ghost_post_via_api(
        _id, api_key, api_url
    )
