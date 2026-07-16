"""VRAIX reader for commonmeta-py.

Fetches VRAIX daily dumps, which are corpus-scale SQLite files. That work lives
in the optional Rust backend (``pip install 'commonmeta-py[backend]'``); without
it, :func:`get_vraix_list` explains how to install it.
"""

from __future__ import annotations

from ..backend import require_backend


def get_vraix_list(source: str, date: str, **kwargs) -> list[dict]:
    """get_vraix_list. Fetches a VRAIX daily dump for `source` ("crossref" or
    "datacite") and `date` (YYYY-MM-DD), already parsed into commonmeta-shaped
    dicts. With `input_path`, reads a local SQLite file directly instead of
    downloading from metadata.vraix.org."""
    backend = require_backend()
    return backend.fetch_vraix(
        source,
        date,
        input_path=kwargs.get("input_path"),
        limit=kwargs.get("limit"),
        offset=kwargs.get("offset", 0),
        cache_ttl_days=kwargs.get("cache_ttl_days", 30),
    )
