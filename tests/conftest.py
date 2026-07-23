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


def _drop_encoding_headers(response):
    """Remove ``Content-Encoding`` / ``Content-Length`` from recorded responses.

    Runs after vcrpy's ``decode_compressed_response`` (see below). That built-in
    only understands gzip and deflate; when a server negotiates Brotli (``br``)
    or Zstandard (``zstd``) — which urllib3 2.x advertises whenever the ``brotli``
    / ``zstandard`` packages are installed — vcrpy leaves the ``Content-Encoding``
    header in place. Replaying such a cassette makes requests/urllib3 try to
    decode the body a second time and raise
    ``requests.exceptions.ContentDecodingError`` on Python 3.9.

    urllib3 has already decompressed the body in-flight by the time it is
    recorded, so the stored body is plain text; dropping the encoding header (and
    the now-stale ``Content-Length``) is exactly the manual cassette cleanup this
    automates, and makes replay codec- and Python-version-agnostic.
    """
    headers = response.get("headers") or {}
    for key in [
        k for k in headers if k.lower() in ("content-encoding", "content-length")
    ]:
        del headers[key]
    return response


@pytest.fixture(scope="module")
def vcr_config():
    """VCR configuration for pytest-recording.

    ``decode_compressed_response`` decodes gzip/deflate response bodies at record
    time and drops their Content-Encoding header. ``before_record_response`` then
    strips any remaining encoding headers (Brotli/Zstandard, which the built-in
    does not handle) so no cassette stores a body alongside a stale
    ``Content-Encoding`` header — which would double-decompress on replay and
    raise ``requests.exceptions.ContentDecodingError`` on Python 3.9's urllib3.
    """
    return {
        "decode_compressed_response": True,
        "before_record_response": _drop_encoding_headers,
    }
