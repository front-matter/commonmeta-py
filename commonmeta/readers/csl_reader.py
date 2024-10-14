"""CSL-JSON reader for commonmeta-py"""
from ..utils import dict_to_spdx, from_csl, normalize_id, name_to_fos, encode_doi
from ..base_utils import wrap, compact, sanitize, presence
from ..author_utils import get_authors
from ..date_utils import get_date_from_date_parts
from ..doi_utils import get_doi_ra, doi_from_url
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

    # optionally generate a DOI if missing but a DOI prefix is provided
    prefix = read_options.get("prefix", None)
    if doi_from_url(_id) is None and prefix is not None:
        _id = encode_doi(prefix)

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
    relations = []
    issn = meta.get("ISSN", None)
    if issn is not None:
        relations.append(
            {
                "id": issn_as_url(issn),
                "type": "IsPartOf",
            }
        )
    container = compact(
        {
            "type": "Periodical",
            "title": meta.get("container-title", None),
            "identifier": issn,
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
                "type": "Abstract",
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
        "contributors": presence(contributors),
        "publisher": presence(publisher),
        "date": compact(date),
        "container": container,
        "references": None,
        "relations": presence(relations),
        "descriptions": descriptions,
        "license": license_,
        "version": meta.get("version", None),
        "subjects": subjects,
        "provider": provider,
        "state": state,
    } | read_options
