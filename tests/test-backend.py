"""Test the optional Rust backend seam.

These cover the guard and the schema handshake, not commonmeta-rs itself. The
tests that need the extra skip when it isn't installed, so the suite stays green
on a plain `pip install commonmeta-py` and on Python 3.9.
"""

import pytest

from commonmeta.backend import (
    BACKEND_PYTHON_SUPPORTED,
    BackendError,
    _load,
    backend_available,
    require_backend,
)
from commonmeta.schema_utils import COMMONMETA_SCHEMA_URI

needs_backend = pytest.mark.skipif(
    not backend_available(), reason="commonmeta-py[backend] not installed"
)


def test_backend_available_is_a_bool():
    """backend_available() answers rather than raising, either way."""
    assert isinstance(backend_available(), bool)


@pytest.mark.skipif(
    not BACKEND_PYTHON_SUPPORTED, reason="the version gate fires first below 3.14"
)
def test_require_backend_without_extra(monkeypatch):
    """Without commonmeta_rs importable, the error says how to install it."""
    import builtins

    real_import = builtins.__import__

    def missing(name, *args, **kwargs):
        if name == "commonmeta_rs":
            raise ImportError("No module named 'commonmeta_rs'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", missing)
    _load.cache_clear()
    with pytest.raises(BackendError, match=r"commonmeta-py\[backend\]"):
        require_backend()
    _load.cache_clear()


@pytest.mark.skipif(
    BACKEND_PYTHON_SUPPORTED, reason="only applies below the backend's Python floor"
)
def test_require_backend_below_python_floor():
    """Below 3.14 the backend can't exist, and the error says so rather than
    suggesting an install that would fail."""
    _load.cache_clear()
    with pytest.raises(BackendError, match="requires Python 3.14"):
        require_backend()
    _load.cache_clear()


def test_backend_commands_registered_only_when_supported():
    """The CLI lists the backend commands only where they could run."""
    from commonmeta.cli import cli

    backend_commands = {"import", "match", "migrate", "settings", "validate", "package"}
    listed = set(cli.commands)
    if BACKEND_PYTHON_SUPPORTED:
        assert backend_commands <= listed
    else:
        assert not (backend_commands & listed)
    # the native commands are there either way
    assert {"convert", "decode", "encode", "list"} <= listed


@needs_backend
def test_schema_versions_agree():
    """py and rs must encode the same commonmeta schema: they share a persistent
    store, where a mismatch persists rather than being recomputed."""
    backend = require_backend()
    assert backend.__commonmeta_schema__ == COMMONMETA_SCHEMA_URI


@needs_backend
def test_mismatched_schema_is_rejected(monkeypatch):
    """A backend targeting a different schema fails loudly at load."""
    import commonmeta_rs

    monkeypatch.setattr(
        commonmeta_rs,
        "__commonmeta_schema__",
        "https://commonmeta.org/commonmeta_v0.18.json",
        raising=False,
    )
    _load.cache_clear()
    with pytest.raises(BackendError, match="different commonmeta schema"):
        require_backend()
    _load.cache_clear()


@needs_backend
def test_parquet_roundtrip():
    """MetadataList.write(to="parquet") round-trips through the backend."""
    import json

    from commonmeta import MetadataList

    records = [
        {
            "id": f"https://doi.org/10.5555/{i}",
            "type": "JournalArticle",
            "title": f"Test {i}",
        }
        for i in range(5)
    ]
    metalist = MetadataList({"items": records}, via="commonmeta")
    data = metalist.write(to="parquet")
    assert isinstance(data, bytes) and len(data) > 0

    backend = require_backend()
    back = backend.read_parquet(data)
    assert len(back) == 5
    assert [i["id"] for i in back] == [r["id"] for r in records]
    # the round-trip is lossless: each row carries the full record as JSON
    assert back[0]["title"] == "Test 0"
    assert (
        json.loads(metalist.write(to="commonmeta"))["items"][0]["id"]
        == records[0]["id"]
    )
