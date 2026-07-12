"""Shared pytest fixtures for commonmeta-py tests."""

import pytest


@pytest.fixture(scope="module")
def vcr_config():
    """VCR configuration for pytest-recording.

    decode_compressed_response decodes gzip/deflate response bodies at record
    time and drops the Content-Encoding header. Without it, cassettes store a
    decoded body alongside a stale ``Content-Encoding: gzip`` header, and
    replaying them double-decompresses the body — which raises
    requests.exceptions.ContentDecodingError on Python 3.9's urllib3.
    """
    return {"decode_compressed_response": True}
