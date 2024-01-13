"""Commonmeta reader for commonmeta-py"""
from ..constants import Commonmeta


def read_commonmeta(data: dict, **kwargs) -> Commonmeta:
    """read_commonmeta"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    read_options = kwargs or {}

    return meta | read_options
