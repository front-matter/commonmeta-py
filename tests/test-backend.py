"""Test the optional Rust backend seam.

These cover the guard and the schema handshake, not commonmeta-rs itself. The
tests that need the extra skip when it isn't installed, so the suite stays green
on a plain `pip install commonmeta-py` and on Python 3.9.
"""

import json
import os

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
    assert json.loads(metalist.write(to="commonmeta"))[0]["id"] == records[0]["id"]


@needs_backend
def test_convert_reads_from_local_store_offline(monkeypatch, tmp_path):
    """A pid in the local SQLite store is served offline, no network."""
    from commonmeta import Metadata

    db = str(tmp_path / "store.sqlite3")
    doi = "https://doi.org/10.5555/offline-hit"
    record = {
        "id": doi,
        "type": "JournalArticle",
        "schema_version": COMMONMETA_SCHEMA_URI,
    }
    require_backend().write_sqlite([record], db)
    monkeypatch.setenv("COMMONMETA_DB", db)

    subject = Metadata(doi, no_network=True)
    assert subject.is_valid
    # served straight from the store as commonmeta, bypassing any reader
    assert subject.via == "commonmeta"
    assert subject.id == doi
    assert subject.type == "JournalArticle"


@needs_backend
def test_convert_offline_miss_raises(monkeypatch, tmp_path):
    """--no-network with a pid absent from the store raises, never fetches."""
    from commonmeta import Metadata
    from commonmeta.backend import BackendError

    db = str(tmp_path / "store.sqlite3")
    require_backend().write_sqlite(
        [{"id": "https://doi.org/10.5555/present", "type": "JournalArticle"}], db
    )
    monkeypatch.setenv("COMMONMETA_DB", db)

    with pytest.raises(BackendError, match="requires network access"):
        Metadata("https://doi.org/10.5555/absent", no_network=True)


@needs_backend
def test_convert_offline_miss_no_database_raises(monkeypatch, tmp_path):
    """--no-network with no database at all names the missing file."""
    from commonmeta import Metadata
    from commonmeta.backend import BackendError

    monkeypatch.setenv("COMMONMETA_DB", str(tmp_path / "does-not-exist.sqlite3"))
    with pytest.raises(BackendError, match="no local database"):
        Metadata("https://doi.org/10.5555/absent", no_network=True)


@needs_backend
def test_get_doi_ra_uses_prefix_cache(monkeypatch, tmp_path):
    """get_doi_ra reads the SQLite prefixes cache before any network call."""
    from commonmeta import doi_utils

    db = str(tmp_path / "store.sqlite3")
    # write_sqlite creates the database file so use_cache is enabled
    require_backend().write_sqlite(
        [{"id": "https://doi.org/10.5555/seed", "type": "JournalArticle"}], db
    )
    require_backend().store_doi_ra_sqlite("10.7554/elife.01567", "Crossref", db)
    monkeypatch.setenv("COMMONMETA_DB", db)

    def _no_http(*args, **kwargs):
        raise AssertionError("network call despite a prefix-cache hit")

    monkeypatch.setattr(doi_utils.requests, "get", _no_http)
    assert doi_utils.get_doi_ra("10.7554/elife.01567") == "Crossref"


@needs_backend
def test_get_doi_ra_no_network_miss_returns_none(monkeypatch, tmp_path):
    """Under no_network a prefix-cache miss returns None, no network."""
    from commonmeta import doi_utils

    db = str(tmp_path / "store.sqlite3")
    require_backend().write_sqlite(
        [{"id": "https://doi.org/10.5555/seed", "type": "JournalArticle"}], db
    )
    monkeypatch.setenv("COMMONMETA_DB", db)

    def _no_http(*args, **kwargs):
        raise AssertionError("network call under no_network")

    monkeypatch.setattr(doi_utils.requests, "get", _no_http)
    assert doi_utils.get_doi_ra("10.99999/uncached", no_network=True) is None


@needs_backend
def test_get_doi_ra_caches_after_fetch(monkeypatch, tmp_path):
    """A network resolve is written back to the prefixes cache."""
    from commonmeta import doi_utils

    db = str(tmp_path / "store.sqlite3")
    require_backend().write_sqlite(
        [{"id": "https://doi.org/10.5555/seed", "type": "JournalArticle"}], db
    )
    monkeypatch.setenv("COMMONMETA_DB", db)

    calls = []

    class _Resp:
        status_code = 200

        @staticmethod
        def json():
            return [{"RA": "DataCite"}]

    def _fake_get(url, *args, **kwargs):
        calls.append(url)
        return _Resp()

    monkeypatch.setattr(doi_utils.requests, "get", _fake_get)
    assert doi_utils.get_doi_ra("10.1234/example") == "DataCite"
    assert len(calls) == 1
    # now cached: a second call hits the store, not the network
    assert require_backend().lookup_doi_ra_sqlite("10.1234/example", db) == "DataCite"
    assert doi_utils.get_doi_ra("10.1234/example") == "DataCite"
    assert len(calls) == 1


@needs_backend
def test_orcid_reads_from_people_table_offline(monkeypatch, tmp_path):
    """An ORCID in the local people table is served offline via the backend.

    convert <orcid> checks the SQLite people table first and only falls back to
    the ORCID API when the record is absent (and --no-network isn't set).
    """
    import json
    import sqlite3

    import zstandard

    from commonmeta import Metadata

    db = str(tmp_path / "store.sqlite3")
    orcid_url = "https://orcid.org/0000-0002-0068-716X"
    person = {
        "path": "/0000-0002-0068-716X/person",
        "name": {
            "given-names": {"value": "Cameron"},
            "family-name": {"value": "Neylon"},
        },
    }
    blob = zstandard.ZstdCompressor().compress(json.dumps(person).encode())
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE people (id TEXT PRIMARY KEY, metadata BLOB)")
    con.execute("INSERT INTO people (id, metadata) VALUES (?, ?)", (orcid_url, blob))
    con.commit()
    con.close()
    monkeypatch.setenv("COMMONMETA_DB", db)

    subject = Metadata("0000-0002-0068-716X", via="orcid", no_network=True)
    assert subject.is_valid
    assert subject.entity_type == "person"
    assert subject.id == orcid_url
    assert subject.name == "Cameron Neylon"


# ── The cache store: read after the main store, written after a fetch ─────────


def test_resolve_cache_db_path_precedence(monkeypatch, tmp_path):
    """Explicit path, then CACHE_DB, then the per-user data directory."""
    from commonmeta.backend import resolve_cache_db_path

    monkeypatch.setenv("CACHE_DB", str(tmp_path / "from-env.sqlite3"))
    assert resolve_cache_db_path(str(tmp_path / "explicit.sqlite3")).endswith(
        "explicit.sqlite3"
    )
    assert resolve_cache_db_path().endswith("from-env.sqlite3")

    monkeypatch.delenv("CACHE_DB")
    assert resolve_cache_db_path().endswith("commonmeta/cache.sqlite3")


_CROSSREF_MESSAGE = {
    "DOI": "10.5555/cached",
    "type": "journal-article",
    "title": ["A Cached Article"],
    "author": [{"given": "Josiah", "family": "Carberry"}],
    "via": "crossref",
}


@needs_backend
def test_read_falls_back_to_the_cache_store(monkeypatch, tmp_path):
    """A pid missing from the main store is served from the cache."""
    from commonmeta import Metadata

    cache = str(tmp_path / "cache.sqlite3")
    require_backend().upsert_pid_records(
        [("10.5555/cached", 1, json.dumps(_CROSSREF_MESSAGE))], cache
    )
    monkeypatch.setenv("COMMONMETA_DB", str(tmp_path / "absent.sqlite3"))
    monkeypatch.setenv("CACHE_DB", cache)

    subject = Metadata("https://doi.org/10.5555/cached", no_network=True)

    assert subject.via == "commonmeta"
    assert subject.title == "A Cached Article"


@needs_backend
def test_fetch_is_written_to_the_cache_store(monkeypatch, tmp_path):
    """What had to be fetched is cached, so the next read is local."""
    import commonmeta.metadata as metadata_module
    from commonmeta import Metadata

    cache = str(tmp_path / "cache.sqlite3")
    monkeypatch.setenv("COMMONMETA_DB", str(tmp_path / "absent.sqlite3"))
    monkeypatch.setenv("CACHE_DB", cache)
    monkeypatch.setattr(
        metadata_module, "get_crossref", lambda pid, **kwargs: dict(_CROSSREF_MESSAGE)
    )

    fetched = Metadata("https://doi.org/10.5555/cached")
    assert fetched.title == "A Cached Article"

    # the second read needs neither the network nor the patched fetcher
    monkeypatch.setattr(
        metadata_module,
        "get_crossref",
        lambda pid, **kwargs: pytest.fail("fetched again instead of reading the cache"),
    )
    assert Metadata("https://doi.org/10.5555/cached", no_network=True).via == "commonmeta"


@needs_backend
def test_orcid_fetch_is_cached_as_xml(monkeypatch, tmp_path):
    """ORCID is fetched and cached as the record XML the store keeps."""
    from conformance_common import fixture_path, read_text

    import commonmeta.metadata as metadata_module
    from commonmeta import Metadata

    orcid = "0000-0002-0068-716X"
    xml = read_text(fixture_path("orcid_xml", f"{orcid}.xml"))
    cache = str(tmp_path / "cache.sqlite3")
    monkeypatch.setenv("COMMONMETA_DB", str(tmp_path / "absent.sqlite3"))
    monkeypatch.setenv("CACHE_DB", cache)
    monkeypatch.setattr(metadata_module, "get_orcid_xml", lambda pid, **kwargs: xml)

    subject = Metadata(f"https://orcid.org/{orcid}")
    assert subject.entity_type == "person"
    assert subject.family_name == "Neylon"
    # affiliations are why the XML reader is used rather than the person JSON
    assert subject.affiliations

    # cached as XML under the ORCID source id, so the store reads it back
    stored = require_backend().read_person_commonmeta_sqlite(orcid, cache)
    assert json.loads(stored)[0]["family_name"] == "Neylon"

    monkeypatch.setattr(
        metadata_module,
        "get_orcid_xml",
        lambda pid, **kwargs: pytest.fail("fetched again instead of reading the cache"),
    )
    assert Metadata(f"https://orcid.org/{orcid}", no_network=True).family_name == "Neylon"


@needs_backend
def test_an_unwritable_cache_does_not_fail_the_read(monkeypatch, tmp_path):
    """The cache is an accelerator: a write it cannot do is not an error."""
    import commonmeta.metadata as metadata_module
    from commonmeta import Metadata

    monkeypatch.setenv("COMMONMETA_DB", str(tmp_path / "absent.sqlite3"))
    monkeypatch.setenv("CACHE_DB", str(tmp_path / "no-such-directory" / "cache.sqlite3"))
    monkeypatch.setattr(
        metadata_module, "get_crossref", lambda pid, **kwargs: dict(_CROSSREF_MESSAGE)
    )

    subject = Metadata("https://doi.org/10.5555/cached")

    assert subject.title == "A Cached Article"
