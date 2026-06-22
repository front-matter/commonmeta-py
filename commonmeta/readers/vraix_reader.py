"""VRAIX reader for commonmeta-py, backed by the commonmeta_rs PyO3 bindings.

Disabled: commonmeta_rs hasn't been migrated to the commonmeta v1.0 schema
yet. Re-enable once commonmeta-rs is refactored to use v1.0.
"""

from __future__ import annotations

# import commonmeta_rs


def get_vraix_list(source: str, date: str, **kwargs) -> list[dict]:
    """get_vraix_list. Fetches a VRAIX daily dump for `source` ("crossref" or
    "datacite") and `date` (YYYY-MM-DD), already parsed into commonmeta-shaped
    dicts. With `input_path`, reads a local SQLite file directly instead of
    downloading from metadata.vraix.org."""
    raise NotImplementedError(
        "vraix reading is temporarily disabled: commonmeta_rs has not yet "
        "been migrated to the commonmeta v1.0 schema."
    )
    # return commonmeta_rs.fetch_vraix(
    #     source,
    #     date,
    #     input_path=kwargs.get("input_path"),
    #     limit=kwargs.get("limit"),
    #     offset=kwargs.get("offset", 0),
    #     cache_ttl_days=kwargs.get("cache_ttl_days", 30),
    # )
