"""schema_org reader for commonmeta-py"""
from ..utils import dict_to_spdx, from_citeproc, normalize_id, name_to_fos
from ..base_utils import wrap, compact, sanitize
from ..author_utils import get_authors
from ..date_utils import get_date_from_date_parts
from ..doi_utils import doi_from_url
from ..constants import (
    CP_TO_SO_TRANSLATIONS,
    CP_TO_DC_TRANSLATIONS,
    SO_TO_BIB_TRANSLATIONS,
    CP_TO_RIS_TRANSLATIONS,
    Commonmeta,
)


def read_citeproc(data: dict, **kwargs) -> Commonmeta:
    """read_citeproc"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    read_options = kwargs or {}

    pid = normalize_id(meta.get("id", None) or meta.get("DOI", None))
    citeproc_type = meta.get("type", None)
    schema_org = CP_TO_SO_TRANSLATIONS.get(citeproc_type, None) or "CreativeWork"
    types = compact(
        {
            "resourceTypeGeneral": CP_TO_DC_TRANSLATIONS.get(citeproc_type, None),
            "reourceType": meta.get("additionalType", None),
            "schemaOrg": schema_org,
            "citeproc": citeproc_type,
            "bibtex": SO_TO_BIB_TRANSLATIONS.get(schema_org, None) or "misc",
            "ris": CP_TO_RIS_TRANSLATIONS.get(schema_org, None) or "GEN",
        }
    )

    if meta.get("author", None):
        creators = get_authors(from_citeproc(wrap(meta.get("author", None))))
    else:
        creators = [{"nameType": "Organizational", "name": ":(unav)"}]
    contributors = get_authors(from_citeproc(wrap(meta.get("editor", None))))

    date_issued = get_date_from_date_parts(meta.get("issued", None))
    if date_issued:
        dates = [{"date": date_issued, "dateType": "Issued"}]
        publication_year = int(date_issued[0:4])
        # Date.edtf(date).present?
    else:
        dates = None
        publication_year = None

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

    state = "findable" if pid or read_options else "not_found"
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
        "pid": pid,
        "doi": doi_from_url(pid) if pid else None,
        "url": normalize_id(meta.get("URL", None)),
        "titles": [{"title": meta.get("title", None)}],
        "creators": creators,
        "publisher": meta.get("publisher", None),
        "publication_year": publication_year,
        "types": types,
        "contributors": contributors,
        "container": container,
        "references": None,
        "dates": dates,
        "descriptions": descriptions,
        "rights": rights,
        "version": meta.get("version", None),
        "subjects": subjects,
        "state": state,
    } | read_options
