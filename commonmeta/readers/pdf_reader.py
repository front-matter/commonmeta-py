"""pdf reader for commonmeta-py"""

from __future__ import annotations

from ..author_utils import get_authors
from ..base_utils import presence, wrap
from ..constants import Commonmeta
from ..date_utils import get_iso8601_date
from ..doi_utils import doi_from_url, get_doi_ra
from ..io_utils import read_pdf_attachment, read_pdf_docinfo, read_pdf_metadata
from ..utils import dict_to_spdx, normalize_id
from .schema_org_reader import parse_schema_org_html, read_schema_org


def read_pdf(data: bytes | dict | None, **kwargs) -> Commonmeta:
    """Read a pdf and return a commonmeta dict.

    A rendition this library wrote carries the record it was written from: the
    post travels inside it as an html attachment whose head holds the record
    as schema.org json-ld, and reading that back gives every field the record
    had. Every other pdf is read for what any pdf can say about itself - its
    XMP packet and its info dictionary - which is a title, an author list, a
    description and the dates, and is what a viewer shows under document
    properties.
    """
    pdf = data.get("data", None) if isinstance(data, dict) else data
    if not isinstance(pdf, bytes) or not pdf.startswith(b"%PDF-"):
        return {"state": "not_found"}

    record = read_pdf_source(pdf, **kwargs)
    if record is not None:
        return record
    return read_pdf_document_properties(pdf, **kwargs)


def read_pdf_source(pdf: bytes, **kwargs) -> Commonmeta | None:
    """The record an attached html source carries, None where there is none.

    The attachment is the page the pdf was rendered from, with the record in
    its head; `content=True` reads its body back as the content of the work,
    since the json-ld leaves the body out rather than carry it twice.
    """
    for name in read_pdf_attachment_names(pdf):
        if not name.lower().endswith((".html", ".htm")):
            continue
        attachment = read_pdf_attachment(pdf, name)
        if attachment is None:
            continue
        html = attachment.decode("utf-8", errors="replace")
        if "application/ld+json" not in html:
            continue
        meta = parse_schema_org_html(html, content=True)
        if meta.get("@id", None) or meta.get("name", None):
            return read_schema_org(meta, **kwargs)
    return None


def read_pdf_attachment_names(pdf: bytes) -> list:
    """The names of the files a pdf carries, in the order it carries them."""
    return list(read_pdf_metadata(pdf).get("attachments", {}))


def read_pdf_document_properties(pdf: bytes, **kwargs) -> Commonmeta:
    """What a pdf says about itself, from its XMP packet and info dictionary.

    The two say the same things under different names, and PDF/A asks them to
    agree; where they differ the XMP packet wins, since it is the one with
    structure - an author list rather than a single string, and a language.
    """
    docinfo = read_pdf_docinfo(pdf)
    xmp = read_pdf_metadata(pdf)

    _id = normalize_id(xmp.get("id", None) or docinfo.get("id", None))
    doi = doi_from_url(_id) if _id else None
    title = xmp.get("title", None) or docinfo.get("title", None)
    description = xmp.get("description", None) or docinfo.get("description", None)
    keywords = xmp.get("keywords", None) or docinfo.get("keywords", None)
    license_ = xmp.get("license_url", None) or xmp.get("license", None)

    return {
        # required properties
        "id": _id,
        # a pdf says it is a document and no more; a rendition that knows what
        # it renders says so in the record it carries as its attachment
        "type": "Document",
        # recommended and optional properties
        "additional_type": None,
        "archive_locations": None,
        "container": None,
        "contributors": presence(
            get_authors(
                [
                    {"name": name}
                    for name in pdf_authors(xmp.get("authors", None))
                    or pdf_authors(docinfo.get("authors", None))
                ]
            )
        ),
        "date_published": pdf_date(
            xmp.get("created", None) or docinfo.get("created", None)
        ),
        "date_updated": pdf_date(
            xmp.get("modified", None) or docinfo.get("modified", None)
        ),
        "dates": None,
        "descriptions": None,
        "description": description,
        "files": None,
        "funding_references": None,
        "geo_locations": None,
        "identifiers": (
            [{"identifier": doi, "identifier_type": "DOI"}] if doi else None
        ),
        "language": xmp.get("language", None),
        "license": dict_to_spdx({"url": license_}) if license_ else None,
        "provider": get_doi_ra(doi) if doi else None,
        "publisher": None,
        "references": None,
        "relations": None,
        "state": "findable" if _id or title else "not_found",
        "subjects": presence([{"subject": keyword} for keyword in wrap(keywords)]),
        "title": title,
        "url": None,
        "version": None,
    } | kwargs


def pdf_authors(authors) -> list:
    """The authors a pdf names, one per entry.

    The XMP packet holds them as a list, which is the whole of it. The info
    dictionary holds a single string, and a comma in it is ambiguous: it
    separates two authors in "Catharina Ochsner, Heinz Pampel" and a family
    name from a given one in "Ochsner, Catharina". A semicolon never is, so it
    is taken first; a comma is read as a separator only where every part it
    makes is a name of its own - two words or more - which is what tells the
    two apart.
    """
    if isinstance(authors, list):
        return [author for author in authors if author]
    if not isinstance(authors, str) or not authors.strip():
        return []
    if ";" in authors:
        return [author.strip() for author in authors.split(";") if author.strip()]
    parts = [part.strip() for part in authors.split(",") if part.strip()]
    if len(parts) > 1 and all(len(part.split()) > 1 for part in parts):
        return parts
    return [authors.strip()]


def pdf_date(date: str | None) -> str | None:
    """A pdf date as an iso8601 one.

    The info dictionary writes `D:20260728120000Z`, the XMP packet writes the
    iso8601 date itself, and `get_iso8601_date` reads what either gives once
    the `D:` prefix is off it.
    """
    if not date:
        return None
    if date.startswith("D:"):
        digits = date[2:]
        date = f"{digits[0:4]}-{digits[4:6]}-{digits[6:8]}".rstrip("-")
    return get_iso8601_date(date)
