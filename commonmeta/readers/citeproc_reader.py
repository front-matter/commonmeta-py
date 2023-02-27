"""schema_org reader for commonmeta-py"""
from ..utils import dict_to_spdx, from_citeproc, normalize_id, name_to_fos
from ..base_utils import wrap, compact, sanitize
from ..author_utils import get_authors
from ..date_utils import get_date_from_date_parts
from ..doi_utils import doi_from_url
from ..constants import (
    CP_TO_CM_TRANSLATIONS,
    Commonmeta,
)


def read_citeproc(data: dict, **kwargs) -> Commonmeta:
    """read_citeproc"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    read_options = kwargs or {}

    id_ = normalize_id(meta.get("id", None) or meta.get("DOI", None))
    type_ = CP_TO_CM_TRANSLATIONS.get(meta.get("type", None), 'Other')

    creators = get_authors(from_citeproc(wrap(meta.get("author", None))))
    contributors = get_authors(from_citeproc(wrap(meta.get("editor", None))))

    date = {'published': get_date_from_date_parts(meta.get("issued", None))}

    if meta.get("copyright", None):
        rights = [dict_to_spdx({"rightsURI": meta.get("copyright")})]
    else:
        rights = None

    pages = meta.get("page", "").split("-")
    container = compact(
        {
            "type": "Periodical",
            "title": meta.get("container-title", None),
            "identifier": meta.get("ISSN", None),
            "identifierType": "ISSN" if meta.get("ISSN", None) else None,
            "volume": meta.get("volume", None),
            "issue": meta.get("issue", None),
            "firstPage": pages[0],
            "lastPage": pages[1] if len(pages) > 1 else None,
        }
    )

    state = "findable" if id_ or read_options else "not_found"
    subjects = [name_to_fos(i) for i in wrap(meta.get("keywords", None))]

    if meta.get("abstract", None):
        descriptions = [
            {
                "description": sanitize(str(meta.get("abstract"))),
                "descriptionType": "Abstract",
            }
        ]
    else:
        descriptions = None

    return {
        "id": id_,
        "type": type_,
        "doi": doi_from_url(id_) if id_ else None,
        "url": normalize_id(meta.get("URL", None)),
        "titles": [{"title": meta.get("title", None)}],
        "creators": creators,
        "publisher": meta.get("publisher", None),
        "date": compact(date),
        "contributors": contributors,
        "container": container,
        "references": None,
        "descriptions": descriptions,
        "rights": rights,
        "version": meta.get("version", None),
        "subjects": subjects,
        "state": state,
    } | read_options
