"""RIS writer for commonmeta-py"""
from ..utils import to_ris
from ..base_utils import compact, wrap, presence, parse_attributes
from ..doi_utils import doi_from_url
from ..constants import CM_TO_RIS_TRANSLATIONS


def write_ris(metadata):
    """Write ris"""
    container = metadata.container or {}
    type_ = CM_TO_RIS_TRANSLATIONS.get(metadata.type, "GEN")
    ris = compact(
        {
            "TY": type_,
            "T1": parse_attributes(metadata.titles, content="title", first=True),
            "T2": container.get("title", None),
            "AU": to_ris(metadata.contributors),
            "DO": doi_from_url(metadata.id) if metadata.id else None,
            "UR": metadata.url,
            "AB": parse_attributes(
                metadata.descriptions, content="description", first=True
            ),
            "KW": presence(
                parse_attributes(
                    wrap(metadata.subjects), content="subject", first=False
                )
            ),
            "PY": metadata.date.get('published')[:4] if metadata.date.get('published', None) else None,
            "PB": metadata.publisher.get("name", None),
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
        if isinstance(val, list):
            for vai in val:
                string.append(f"{key}  - {vai}")
        else:
            string.append(f"{key}  - {val}")
    return "\r\n".join(string)
