"""CSL-JSON reader for commonmeta-py"""

from __future__ import annotations

from ..author_utils import get_authors
from ..base_utils import compact, presence, sanitize, wrap
from ..constants import (
    CSL_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..date_utils import get_date_from_date_parts
from ..doi_utils import doi_from_url, encode_doi
from ..utils import (
    dict_to_spdx,
    from_csl,
    get_language,
    issn_as_url,
    name_to_fos,
    normalize_id,
)

# commonmeta type → container type for CSL records
_CSL_CONTAINER_TYPES = {
    "JournalArticle": "Periodical",
    "JournalIssue": "Periodical",
    "JournalVolume": "Periodical",
    "Journal": "Periodical",
    "ProceedingsArticle": "Proceedings",
    "Proceedings": "Proceedings",
    "BookChapter": "Book",
    "Book": "Book",
    "BlogPost": "Blog",
    "Dataset": "DataRepository",
}


def csl_number(value) -> str | None:
    """A CSL number variable (`edition`, `number`), a string or a number."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def csl_series_type(_type: str) -> str:
    """The container type of a series named by CSL `collection-title`."""
    if _type in ("Proceedings", "ProceedingsArticle"):
        return "ProceedingsSeries"
    if _type == "Report":
        return "ReportSeries"
    return "BookSeries"


def read_csl(data: dict | None, **kwargs) -> Commonmeta:
    """read_csl"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    read_options = kwargs or {}

    _id = normalize_id(meta.get("id", None) or meta.get("DOI", None)) or meta.get(
        "id", None
    )
    _type = CSL_TO_CM_TRANSLATIONS.get(meta.get("type", None), "Other")

    # optionally generate a DOI if missing but a DOI prefix is provided
    prefix = read_options.get("prefix", None)
    if doi_from_url(_id) is None and prefix is not None:
        _id = encode_doi(prefix)

    contributors = get_authors(from_csl(wrap(meta.get("author", None))))
    contrib = get_authors(from_csl(wrap(meta.get("editor", None))))
    if contrib:
        contributors += contrib

    date_published = get_date_from_date_parts(meta.get("issued", None))

    license_url = meta.get("license", None) or meta.get("copyright", None)
    license_ = dict_to_spdx({"url": license_url}) if license_url else None

    pages = (meta.get("page") or "").split("-")
    publisher = meta.get("publisher", None)
    if isinstance(publisher, str):
        publisher = {"name": publisher}
    publisher_place = meta.get("publisher-place", None)
    if isinstance(publisher_place, str) and publisher_place.strip():
        publisher = {
            **(publisher or {}),
            "geo_locations": [{"place": publisher_place.strip()}],
        }
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
            "type": _CSL_CONTAINER_TYPES.get(_type, None),
            "title": meta.get("container-title", None),
            "identifiers": (
                [{"identifier": issn, "identifier_type": "ISSN"}] if issn else None
            ),
            "volume": meta.get("volume", None),
            "issue": meta.get("issue", None),
            "first_page": pages[0] or None,
            "last_page": pages[1] if len(pages) > 1 else None,
            "additional_titles": presence(
                [
                    t.strip()
                    for t in wrap(meta.get("container-title-short", None))
                    if isinstance(t, str) and t.strip()
                ]
            ),
            # the conference or event (CSL 1.0.2); `event` is its CSL 1.0.1 name
            "event": meta.get("event-title", None) or meta.get("event", None),
            "location": meta.get("event-place", None),
        }
    )
    # A series title without a container title: the item's container is the
    # series (the CSL writer writes a series container as `collection-title`).
    collection_title = meta.get("collection-title", None)
    if not container.get("title", None) and collection_title:
        container = {
            **container,
            "type": csl_series_type(_type),
            "title": collection_title,
        }
    dates = compact(
        {"available": get_date_from_date_parts(meta.get("available-date", None))}
    )
    genre = meta.get("genre", None)
    additional_type = genre.strip() if isinstance(genre, str) else None

    state = "findable" if _id or read_options else "not_found"
    # CSL-JSON uses `categories`; fall back to the singular/plural keyword fields.
    # A comma-separated keyword string is split into individual subjects.
    raw_subjects = (
        meta.get("categories", None)
        or meta.get("keyword", None)
        or meta.get("keywords", None)
    )
    if isinstance(raw_subjects, str):
        raw_subjects = [k.strip() for k in raw_subjects.split(",") if k.strip()]
    subjects = [name_to_fos(i) for i in wrap(raw_subjects)]

    description = sanitize(str(meta.get("abstract"))) if meta.get("abstract") else None

    return {
        "id": _id,
        "type": _type,
        "additional_type": presence(additional_type),
        "container": container,
        "contributors": presence(contributors),
        "date_published": date_published,
        "dates": presence(dates),
        "description": description,
        "edition": csl_number(meta.get("edition", None)),
        "language": get_language(meta.get("language", None)),
        "license": license_,
        "number": csl_number(meta.get("number", None)),
        "publisher": presence(publisher),
        "references": None,
        "relations": presence(relations),
        "state": state,
        "subjects": subjects,
        "title": meta.get("title", None),
        "url": normalize_id(meta.get("URL", None)),
        "version": meta.get("version", None),
    } | read_options
