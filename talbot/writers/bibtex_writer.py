"""Bibtex writer for Talbot"""
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from ..utils import pages_as_string
from ..base_utils import compact
from ..author_utils import authors_as_string
from ..date_utils import get_month_from_date, get_date_by_type


def write_bibtex(metadata):
    """Write bibtex"""
    container = metadata.container or {}
    db = BibDatabase()
    db.entries = [
        compact(
            {
                "ID": metadata.pid,
                "ENTRYTYPE": metadata.types.get("bibtex", "misc"),
                "abstract": metadata.descriptions[0].get("description", None)
                if metadata.descriptions
                else None,
                "author": authors_as_string(metadata.creators),
                "copyright": str(metadata.rights[0].get("rightsUri", None))
                if metadata.rights
                else None,
                "doi": metadata.doi,
                "issn": container.get("identifier", None) if container.get('identifierType', None) == 'ISSN' else None,
                "issue": container.get("issue", None),
                "journal": container.get("title", None) if metadata.types.get("bibtex", None) != "inproceedings" else None,
                "booktitle": container.get("title", None) if metadata.types.get("bibtex", None) == "inproceedings" else None,
                "language": metadata.language,
                "month": get_month_from_date(metadata.dates[0].get("date", None)),
                "pages": pages_as_string(container),
                "publisher": container.get("publisher", None) if metadata.types.get("bibtex", None) in ["phdthesis"] else None,
                "institution": container.get("publisher", None) if metadata.types.get("bibtex", None) == "phdthesis" else None,
                "title": metadata.titles[0].get("title", None),
                "url": metadata.url,
                "urldate": get_date_by_type(metadata.dates, date_only=True),
                "year": str(metadata.publication_year),
            }
        )
    ]
    writer = BibTexWriter()
    writer.indent = "    "
    bibtex_str = writer.write(db)
    return bibtex_str
