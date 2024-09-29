"""Bibtex writer for commonmeta-py"""
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import page_double_hyphen

from ..utils import pages_as_string, get_language
from ..base_utils import compact
from ..author_utils import authors_as_string
from ..date_utils import get_month_from_date, get_iso8601_date, MONTH_SHORT_NAMES
from ..doi_utils import doi_from_url
from ..constants import CM_TO_BIB_TRANSLATIONS, Commonmeta


def write_bibtex(metadata: Commonmeta) -> str:
    """Write bibtex"""
    if metadata.write_errors is not None:
        return None
    item = write_bibtex_item(metadata)
    bibtex_str = """
    @comment{
        BibTeX entry created by commonmeta-py
    }
    """
    bib_database = BibDatabase()
    bib_database.entries = [item]
    bib_database.entries[0] = page_double_hyphen(bib_database.entries[0])
    writer = BibTexWriter()
    writer.common_strings = True
    writer.indent = "    "
    bibtex_str = writer.write(bib_database)

    # Hack to remove curly braces around month names
    for month_name in MONTH_SHORT_NAMES:
        bibtex_str = bibtex_str.replace(f"{{{month_name}}}", month_name)
    return bibtex_str


def write_bibtex_item(metadata: Commonmeta) -> dict:
    """Write bibtex item"""
    container = metadata.container if metadata.container else {}
    date_published = get_iso8601_date(metadata.date.get("published", None))
    authors = authors_as_string(metadata.contributors)
    if metadata.titles and len(metadata.titles) > 1:
        title = ": ".join(
            [
                metadata.titles[0].get("title", None),
                metadata.titles[1].get("title", None),
            ]
        )
    elif metadata.titles and len(metadata.titles) == 1:
        title = metadata.titles[0].get("title", None)
    else:
        title = None
    doi = doi_from_url(metadata.id)
    _id = doi if doi else metadata.id
    _type = CM_TO_BIB_TRANSLATIONS.get(metadata.type, "misc")
    abstract = (
        metadata.descriptions[0].get("description", None)
        if metadata.descriptions
        else None
    )
    author = authors if authors and len(authors) > 0 else None
    license_ = str(metadata.license.get("url")) if metadata.license else None
    institution = metadata.publisher.get("name", None) if _type == "phdthesis" else None
    issn = (
        container.get("identifier", None)
        if container.get("identifierType", None) == "ISSN"
        else None
    )
    isbn = (
        container.get("identifier", None)
        if container.get("identifierType", None) == "ISBN"
        else None
    )
    issue = container.get("issue", None)
    journal = (
        container.get("title", None)
        if _type not in ["inbook", "inproceedings"]
        and container.get("type") in ["Journal", "Periodical"]
        else None
    )
    booktitle = (
        container.get("title", None) if _type in ["inbook", "inproceedings"] else None
    )
    language = get_language(metadata.language)
    location = (
        container.get("location", None)
        if _type not in ["article", "phdthesis"]
        else None
    )
    month = get_month_from_date(date_published)
    pages = pages_as_string(container)
    publisher = (
        metadata.publisher.get("name", None)
        if _type not in ["article", "phdthesis"]
        else None
    )
    series = container.get("series", None)
    url = metadata.url
    year = date_published[:4] if date_published else None

    return compact(
        {
            "ID": _id,
            "ENTRYTYPE": _type,
            "abstract": abstract,
            "author": author,
            "copyright": license_,
            "doi": doi,
            "institution": institution,
            "isbn": isbn,
            "issn": issn,
            "issue": issue,
            "journal": journal,
            "booktitle": booktitle,
            "language": language,
            "location": location,
            "month": month,
            "pages": pages,
            "publisher": publisher,
            "series": series,
            "title": title,
            "url": url,
            "urldate": date_published,
            "year": year,
        }
    )


def write_bibtex_list(metalist):
    """Write bibtex list"""
    if metalist is None:
        return None

    bib_database = BibDatabase()
    bib_database.entries = [write_bibtex_item(item) for item in metalist.items]

    # TODO: Fix page_double_hyphen in write_bibtex_item
    bib_database.entries = [page_double_hyphen(entry) for entry in bib_database.entries]
    writer = BibTexWriter()
    writer.common_strings = True
    writer.indent = "    "
    bibtex_str = writer.write(bib_database)

    # Hack to remove curly braces around month names
    # TODO: Fix this in write_bibtex_item
    for month_name in MONTH_SHORT_NAMES:
        bibtex_str = bibtex_str.replace(f"{{{month_name}}}", month_name)
    return bibtex_str
