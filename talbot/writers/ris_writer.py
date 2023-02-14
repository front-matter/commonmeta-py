"""RIS writer for Talbot"""
from ..utils import to_ris
from ..base_utils import compact, wrap, presence, parse_attributes
from ..doi_utils import doi_from_url


def write_ris(metadata):
    """Write ris"""
    container = metadata.container or {}
    ris = compact(
        {
            "TY": metadata.types.get("ris", "GEN"),
            "T1": parse_attributes(metadata.titles, content="title", first=True),
            "T2": container.get("title", None),
            "AU": to_ris(metadata.creators),
            "DO": doi_from_url(metadata.pid),
            "UR": metadata.url,
            "AB": parse_attributes(
                metadata.descriptions, content="description", first=True
            ),
            "KW": presence(
                parse_attributes(
                    wrap(metadata.subjects), content="subject", first=False
                )
            ),
            "PY": metadata.publication_year,
            "PB": metadata.publisher,
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
