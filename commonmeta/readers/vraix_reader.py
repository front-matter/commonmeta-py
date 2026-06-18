"""VRAIX reader for commonmeta-py, backed by the commonmeta_rs PyO3 bindings"""

from __future__ import annotations

import commonmeta_rs


def get_vraix_list(source: str, date: str, **kwargs) -> list[dict]:
    """get_vraix_list. Fetches a VRAIX daily dump for `source` ("crossref" or
    "datacite") and `date` (YYYY-MM-DD), already parsed into commonmeta-shaped
    dicts. With `input_path`, reads a local SQLite file directly instead of
    downloading from metadata.vraix.org."""
    return commonmeta_rs.fetch_vraix(
        source,
        date,
        input_path=kwargs.get("input_path"),
        limit=kwargs.get("limit"),
        offset=kwargs.get("offset", 0),
        cache_ttl_days=kwargs.get("cache_ttl_days", 30),
    )
