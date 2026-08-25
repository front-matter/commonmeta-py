"""Shared pytest fixtures for commonmeta-py tests."""

import base64
import os
import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch
from urllib.parse import unquote_to_bytes, urlparse
from urllib.request import url2pathname

import pytest

from commonmeta.io_utils import write_pdf_rendition

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
    # The cache store is read on a miss and written after a fetch, so it needs
    # the same isolation: a developer machine has a populated cache.sqlite3.
    monkeypatch.setenv("CACHE_DB", str(tmp_path / "absent-cache.sqlite3"))


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


def require_weasyprint():
    """Import WeasyPrint, skipping the caller when its native stack is missing.

    WeasyPrint binds pango, cairo and glib through cffi at import time, so a
    machine without those system libraries raises OSError rather than
    ImportError. On macOS they come from `brew install pango`, which puts them
    somewhere dyld searches only through DYLD_FALLBACK_LIBRARY_PATH - and SIP
    drops that variable when a protected binary is launched, so exporting it in
    a shell profile does not reliably survive. Setting it here does, because
    ctypes reads it when the library is actually dlopened. The writer imports
    WeasyPrint the same way, and this runs first.
    """
    if sys.platform == "darwin":
        paths = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "").split(os.pathsep)
        paths += [
            p for p in ("/opt/homebrew/lib", "/usr/local/lib") if os.path.isdir(p)
        ]
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = os.pathsep.join(
            dict.fromkeys(p for p in paths if p)
        )
    try:
        import weasyprint
    except (ImportError, OSError) as error:
        pytest.skip(f"weasyprint needs the pango libraries: {error}")
    return weasyprint


def offline_url_fetcher(url, **kwargs):
    """Serve the bundled fonts and embedded data, refuse everything remote.

    Post content links images, iframes and video from the blog it came from,
    and a test must not go to the network for them. WeasyPrint logs a failed
    resource and lays the page out without it, which is what a reader with a
    dead image link would get anyway. Fonts and data uris are read here rather
    than through WeasyPrint's own default fetcher, which it deprecated in 69.
    """
    from weasyprint.urls import URLFetcherResponse

    if url.startswith("file:"):
        path = url2pathname(urlparse(url).path)
        return URLFetcherResponse(url, body=open(path, "rb"))  # noqa: SIM115
    if url.startswith("data:"):
        # the feature image, which the writer embeds rather than links
        header, _, payload = url.partition(",")
        mime_type = header[len("data:") :].split(";")[0]
        body = (
            base64.b64decode(payload)
            if header.endswith(";base64")
            else unquote_to_bytes(payload)
        )
        return URLFetcherResponse(url, body=body, headers={"Content-Type": mime_type})
    raise ValueError(f"external resource not fetched in tests: {url}")


# a 1x1 red png, the stand-in for whatever a blog serves as its feature image
PNG_PIXEL = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmM"
    "IQAAAABJRU5ErkJggg=="
)


def image_response(content: bytes = PNG_PIXEL, mime_type: str = "image/png"):
    """What `http.get` returns for a feature image, without the network."""
    return SimpleNamespace(
        content=content,
        headers={"Content-Type": mime_type},
        raise_for_status=lambda: None,
    )


@pytest.fixture
def feature_image():
    """Serve every feature image request the writer makes from memory.

    The writer fetches the image itself, to embed it rather than link it, and
    a test must not go to the blog for it. Patched at the http boundary, so
    the fetch, the content type check and the data uri are all still covered.
    The writer's own name for the session is replaced rather than the session
    itself, which the readers share and use to replay their cassettes.
    """
    from commonmeta import io_utils

    get = Mock(return_value=image_response())
    with patch.object(io_utils, "http", SimpleNamespace(get=get)):
        yield get


@pytest.fixture
def write_pdf(tmp_path, feature_image):
    """Write a record's pdf rendition, and keep the file.

    Renders offline: the feature image comes from the `feature_image` fixture
    and the images the post itself links are refused. Returns the pdf bytes,
    for `read_pdf_metadata` and the font check to read back, and writes them
    to a file the way `upload_pdf` deposits them.
    """
    require_weasyprint()

    def render(metadata, name: str = "content.pdf", **options) -> bytes:
        pdf = write_pdf_rendition(metadata, url_fetcher=offline_url_fetcher, **options)
        assert pdf is not None and pdf.startswith(b"%PDF-")
        path = tmp_path / name
        path.write_bytes(pdf)
        return pdf

    return render
