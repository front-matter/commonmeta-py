"""BibTeX reader for commonmeta-py"""

from __future__ import annotations

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

from ..author_utils import get_authors
from ..base_utils import compact, container_identifiers, presence
from ..constants import BIB_TO_CM_TRANSLATIONS, Commonmeta
from ..doi_utils import normalize_doi
from ..utils import dict_to_spdx, get_language, normalize_url

# Month abbreviations and full names → month number
_MONTH_MAP: dict[str, int] = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}

# Map BibTeX entry type to the container type
_CONTAINER_TYPE: dict[str, str] = {
    "article": "Journal",
    "inbook": "Book",
    "incollection": "Book",
    "inproceedings": "Book",
}


def read_bibtex(data: str | None, **kwargs) -> Commonmeta:
    """Read a BibTeX string and return a commonmeta dict."""
    if not data or not isinstance(data, str):
        return {"state": "not_found"}

    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    bib = bibtexparser.loads(data, parser=parser)

    if not bib.entries:
        return {"state": "not_found"}

    return _entry_to_commonmeta(bib.entries[0], **kwargs)


def _parse_names(raw: str, role: str = "Author") -> list[dict]:
    """Split a BibTeX author/editor string into contributor dicts.

    Splits on ' and ' without prior bibtexparser name-swapping so that
    org names (no comma) reach get_authors intact for is_personal_name
    detection, and 'Last, First' names are split explicitly.
    """
    names: list[str] = [n.strip() for n in raw.split(" and ") if n.strip()]
    result = []
    for raw_name in names:
        name = raw_name.strip("{}")
        if not name:
            continue
        if "," not in name:
            result.append({"name": name, "contributor_roles": [role]})
        else:
            family, given = name.split(",", 1)
            result.append(
                {
                    "familyName": family.strip(),
                    "givenName": given.strip(),
                    "contributor_roles": [role],
                }
            )
    return result


def _parse_date(year: str | None, month: str | None, day: str | None) -> str | None:
    """Build an ISO 8601 partial date from separate year/month/day fields."""
    if not year:
        return None
    result = year.strip()
    if month:
        m_str = str(month).strip().lower()
        m = _MONTH_MAP.get(m_str)
        if m is None:
            try:
                m = int(m_str)
            except (ValueError, TypeError):
                m = None
        if m:
            result += f"-{m:02d}"
            if day:
                try:
                    result += f"-{int(day):02d}"
                except (ValueError, TypeError):
                    pass
    return result


def _entry_to_commonmeta(entry: dict, **kwargs) -> Commonmeta:
    """Convert a bibtexparser entry dict into a commonmeta dict."""
    read_options = kwargs or {}
    entry_type = entry.get("ENTRYTYPE", "misc").lower()
    _type = BIB_TO_CM_TRANSLATIONS.get(entry_type, "Other")

    # ID: DOI → URL → cite key
    doi_raw = entry.get("doi")
    identifiers: list[dict] = []
    if doi_raw:
        _id = normalize_doi(doi_raw)
        if _id:
            identifiers = [{"identifier": _id, "identifier_type": "DOI"}]
    else:
        _id = None

    if not _id:
        url_raw = entry.get("url")
        _id = normalize_url(url_raw) if url_raw else entry.get("ID")

    url = normalize_url(entry.get("url")) if entry.get("url") else None

    # Title
    title = entry.get("title") or None

    # Contributors: authors then editors
    contributor_dicts: list[dict] = []
    author_raw = entry.get("author", "")
    if author_raw:
        contributor_dicts.extend(_parse_names(author_raw, role="Author"))
    editor_raw = entry.get("editor")
    if editor_raw:
        contributor_dicts.extend(_parse_names(editor_raw, role="Editor"))
    contributors = get_authors(contributor_dicts) if contributor_dicts else None

    # Date: prefer the biblatex `date` field, else assemble year/month/day
    date_published = entry.get("date") or _parse_date(
        entry.get("year"), entry.get("month"), entry.get("day")
    )

    # Abstract
    description = entry.get("abstract") or None

    # License from copyright field
    license_ = None
    copyright_raw = entry.get("copyright")
    if copyright_raw:
        license_ = dict_to_spdx({"url": copyright_raw})

    # Publisher / institution
    publisher = None
    pub_name = (
        entry.get("publisher")
        or (entry.get("school") if entry_type == "phdthesis" else None)
        or entry.get("institution")
    )
    if pub_name:
        publisher = {"name": pub_name}

    # Language
    language = None
    lang_raw = entry.get("language")
    if lang_raw:
        language = get_language(lang_raw) or lang_raw

    # Version
    version = entry.get("version") or None

    # Container
    container_title = entry.get("journal") or entry.get("booktitle") or None
    issn = entry.get("issn") or None
    isbn = entry.get("isbn") or None
    identifier = issn or isbn
    identifier_type = "ISSN" if issn else ("ISBN" if isbn else None)
    volume = entry.get("volume") or None
    issue = entry.get("issue") or entry.get("number") or None

    # Pages: split on "--" or "-"
    first_page = last_page = None
    pages_raw = entry.get("pages")
    if pages_raw:
        if "--" in pages_raw:
            parts = pages_raw.split("--", 1)
            first_page, last_page = parts[0].strip(), parts[1].strip()
        elif "–" in pages_raw:
            parts = pages_raw.split("–", 1)
            first_page, last_page = parts[0].strip(), parts[1].strip()
        else:
            first_page = pages_raw.strip()

    container = None
    if any([container_title, identifier, volume, issue, first_page]):
        container = compact(
            {
                "type": _CONTAINER_TYPE.get(entry_type, "Periodical"),
                "title": container_title,
                "identifiers": container_identifiers(identifier, identifier_type),
                "volume": volume,
                "issue": issue,
                "first_page": first_page,
                "last_page": last_page,
            }
        )

    return {
        "id": _id,
        "type": _type,
        "url": url,
        "title": title,
        "contributors": presence(contributors),
        "date_published": date_published,
        "description": description,
        "license": license_,
        "publisher": presence(publisher),
        "container": presence(container),
        "identifiers": identifiers or None,
        "language": language,
        "version": version,
    } | read_options
