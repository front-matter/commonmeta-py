"""Shared pytest fixtures for commonmeta-py tests."""

import os
import sys

import pytest

# Make sibling helper modules (e.g. conformance_common) importable from the
# test-*.py files regardless of pytest's import mode.
sys.path.insert(0, os.path.dirname(__file__))


@pytest.fixture(autouse=True)
def _isolate_backend_db(monkeypatch, tmp_path):
    """Point the backend's SQLite store at a nonexistent path for every test.

    Metadata now reads pid inputs from the local commonmeta database first (Rust
    backend) before any network fetch. Without this, tests on a developer machine
    with a populated ~/…/commonmeta.sqlite3 would be served from that store and
    bypass the VCR cassettes, making results non-deterministic across machines.
    A path under tmp_path never exists, so backend reads always miss and tests
    fall through to their recorded network behavior.
    """
    monkeypatch.setenv("COMMONMETA_DB", str(tmp_path / "absent.sqlite3"))


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
