"""Commonmeta reader for commonmeta-py."""

from __future__ import annotations

from ..constants import Commonmeta

# The grant fields of a funding reference were named award_* before
# commonmeta-schema 1.0.12.
_LEGACY_FUNDING_KEYS = {
    "award_id": "grant_id",
    "award_title": "grant_title",
    "award_number": "grant_number",
}


def _upgrade_funding_reference(funding: dict) -> dict:
    """Return a funding reference with award_* keys renamed to grant_*.

    A grant_* key already present wins over its award_* counterpart.
    """
    if not isinstance(funding, dict):
        return funding
    upgraded = {}
    for key, value in funding.items():
        new_key = _LEGACY_FUNDING_KEYS.get(key)
        if new_key is None:
            upgraded[key] = value
        elif new_key not in funding:
            upgraded[new_key] = value
    return upgraded


def read_commonmeta(data: dict | None, **kwargs) -> Commonmeta:
    """read_commonmeta"""
    if data is None:
        return {"state": "not_found"}
    meta = data
    funding_references = meta.get("funding_references")
    if isinstance(funding_references, list):
        meta = meta | {
            "funding_references": [
                _upgrade_funding_reference(f) for f in funding_references
            ]
        }

    read_options = kwargs or {}

    return meta | read_options
