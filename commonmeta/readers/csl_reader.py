"""CSL-JSON reader for commonmeta-py"""
from ..utils import dict_to_spdx, from_csl, normalize_id, name_to_fos
from ..base_utils import wrap, compact, sanitize, presence
from ..author_utils import get_authors
from ..date_utils import get_date_from_date_parts
from ..doi_utils import get_doi_ra
from ..constants import (
    CSL_TO_CM_TRANSLATIONS,
    Commonmeta,
)


def read_csl(data: dict, **kwargs) -> Commonmeta:
    """read_csl"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    read_options = kwargs or {}

    _id = normalize_id(meta.get("id", None) or meta.get("DOI", None))
    _type = CSL_TO_CM_TRANSLATIONS.get(meta.get("type", None), "Other")

    contributors = get_authors(from_csl(wrap(meta.get("author", None))))
    contrib = get_authors(from_csl(wrap(meta.get("editor", None))))
    if contrib:
        contributors += contrib

    date = {"published": get_date_from_date_parts(meta.get("issued", None))}

    license_ = meta.get("copyright", None)
    if license_ is not None:
        license_ = dict_to_spdx({"url": meta.get("copyright")})

    pages = meta.get("page", "").split("-")
    publisher = meta.get("publisher", None)
    if isinstance(publisher, str):
        publisher = {"name": publisher}
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

    state = "findable" if _id or read_options else "not_found"
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

    provider = get_doi_ra(_id)

    return {
        "id": _id,
        "type": _type,
        "url": normalize_id(meta.get("URL", None)),
        "titles": [{"title": meta.get("title", None)}],
        "contributors": contributors,
        "publisher": presence(publisher),
        "date": compact(date),
        "container": container,
        "references": None,
        "descriptions": descriptions,
        "license": license_,
        "version": meta.get("version", None),
        "subjects": subjects,
        "provider": provider,
        "state": state,
    } | read_options
