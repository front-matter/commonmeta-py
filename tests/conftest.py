"""Shared pytest fixtures for commonmeta-py tests."""

import os
import sys

import pytest

# Make sibling helper modules (e.g. conformance_common) importable from the
# test-*.py files regardless of pytest's import mode.
sys.path.insert(0, os.path.dirname(__file__))


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
