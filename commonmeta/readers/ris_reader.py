"""RIS reader for commonmeta-py"""
from typing import Optional

from ..utils import compact, normalize_url, wrap
from ..base_utils import presence
from ..author_utils import get_authors
from ..date_utils import get_date_from_parts
from ..doi_utils import normalize_doi, doi_from_url
from ..constants import RIS_TO_CM_TRANSLATIONS, Commonmeta


def read_ris(data: Optional[str], **kwargs) -> Commonmeta:
    """read_ris"""

    meta = ris_meta(data=data)
    read_options = kwargs or {}

    if not isinstance(meta, dict):
        return {"state": "not_found"}

    _id = read_options.get("doi", None) or normalize_doi(meta.get("DO", None))
    _type = RIS_TO_CM_TRANSLATIONS.get(meta.get("TY", None), "Other")
    container_type = "Journal" if _type == "JournalArticle" else None

    def get_author(author):
        """get_author"""
        return {"creatorName": author}

    authors = [get_author(i) for i in wrap(meta.get("AU", None))]
    contributors = get_authors(authors)
    date = {}
    if meta.get("PY", None) is not None:
        date["published"] = get_date_from_parts(*str(meta.get("PY", None)).split("/"))
    if meta.get("Y1", None) is not None:
        date["created"] = get_date_from_parts(*str(meta.get("Y1", None)).split("/"))
    # related_identifiers = if meta.fetch('T2', nil).present? & & meta.fetch('SN', nil).present?
    #                             [{'type' = > 'Periodical',
    #                                'id'= > meta.fetch('SN', nil),
    #                                'relatedIdentifierType'= > 'ISSN',
    #                                'relationType'= > 'IsPartOf',
    #                                'title' = > meta.fetch('T2', nil)}.compact]
    #                           else
    #                             []
    #                           end
    descriptions = None
    if meta.get("AB", None) is not None:
        descriptions = [{"description": meta.get("AB"), "type": "Abstract"}]
    if meta.get("T2", None) is not None:
        container = compact(
            {
                "type": container_type,
                "title": meta.get("T2", None),
                "volume": meta.get("VL", None),
                "issue": meta.get("IS", None),
                "firstPage": meta.get("SP", None),
                "lastPage": meta.get("EP", None),
            }
        )
    else:
        container = None
    if meta.get("PB", None) is not None:
        publisher = {"name": meta.get("PB")}
    else:
        publisher = None
    subjects = wrap(meta.get("KW", None))
    state = "findable" if meta.get("DO", None) or read_options else "not_found"

    return {
        "id": _id,
        "type": _type,
        "doi": doi_from_url(_id),
        "url": normalize_url(meta.get("UR", None)),
        "titles": [{"title": meta.get("T1", None)}],
        "descriptions": descriptions,
        "contributors": presence(contributors),
        "publisher": presence(publisher),
        "container": container,
        # 'related_identifiers': related_identifiers,
        "date": date,
        "subjects": subjects,
        "language": meta.get("LA", None),
        "state": state,
    } | read_options


def ris_meta(data):
    """ris_meta"""
    meta = {}
    if data is None:
        return meta
    for line in data.split("\n"):
        values = line.split("-", 2)
        key = values[0].strip()
        if len(values) == 1:
            continue
        if meta.get(key, None) is None:
            meta[key] = values[1].strip()
        elif isinstance(meta[key], str):
            meta[key] = [meta[key]]
        elif isinstance(meta[key], list):
            meta[key].append(values[1].strip())

    return meta
