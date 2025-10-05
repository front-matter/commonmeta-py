"""RIS writer for commonmeta-py"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base_utils import compact, first, parse_attributes, wrap
from ..constants import CM_TO_RIS_TRANSLATIONS
from ..doi_utils import doi_from_url
from ..utils import to_ris

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


def write_ris(metadata: Metadata) -> bytes | None:
    """Write ris"""
    if metadata is None:
        return None
    container = metadata.container or {}
    publisher = metadata.publisher or {}
    _type = CM_TO_RIS_TRANSLATIONS.get(metadata.type, "GEN")
    ris = compact(
        {
            "TY": _type,
            "T1": first(parse_attributes(metadata.titles, content="title", first=True)),
            "T2": container.get("title", None),
            "AU": to_ris(metadata.contributors),
            "DO": doi_from_url(metadata.id),
            "UR": metadata.url,
            "AB": first(
                parse_attributes(
                    metadata.descriptions, content="description", first=True
                )
            ),
            "KW": parse_attributes(
                wrap(metadata.subjects), content="subject", first=False
            ),
            "PY": metadata.date.get("published")[:4]
            if metadata.date.get("published", None)
            else None,
            "PB": publisher.get("name", None),
            "LA": metadata.language,
            "VL": container.get("volume", None),
            "IS": container.get("issue", None),
            "SP": container.get("firstPage", None),
            "EP": container.get("lastPage", None),
            # 'SN'= > Array.wrap(related_identifiers).find do | ri |
            # ri['relationType'] == 'IsPartOf'
            # end.to_h.fetch('relatedIdentifier', nil),
            "ER": "",
        }
    )
    string = []
    for key, val in ris.items():
        if isinstance(val, list) and val not in [[], [None]]:
            for vai in val:
                string.append(f"{key}  - {vai}")
        elif val not in [[], [None]]:
            string.append(f"{key}  - {val}")
    return "\r\n".join(string).encode("utf-8")


def write_ris_list(metalist: MetadataList | None) -> bytes | None:
    """Write RIS list"""
    if metalist is None:
        return None
    items = [write_ris(item) for item in metalist.items]
    # Filter None values and decode bytes to str for joining
    items_str = [item.decode("utf-8") for item in items if item is not None]
    return "\r\n\r\n".join(items_str).encode("utf-8")
