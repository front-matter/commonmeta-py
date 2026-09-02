# pylint: disable=invalid-name
"""pdf reader tests"""

import io

import pikepdf
import pytest

from commonmeta import Metadata
from commonmeta.readers.inveniordm_reader import search_by_doi
from commonmeta.readers.pdf_reader import pdf_authors, read_pdf


@pytest.fixture
def rendition(render_pdf):
    """A rendition of a post, and the record it was written from."""
    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )
    return subject, render_pdf(subject)


def without(pdf: bytes, *keys: str) -> bytes:
    """The same pdf with entries removed from its catalog.

    `/Names` is where the embedded files are listed and `/Metadata` is the XMP
    packet, so dropping them makes a rendition into the two kinds of pdf the
    reader falls back for.
    """
    output = io.BytesIO()
    with pikepdf.open(io.BytesIO(pdf)) as document:
        for key in keys:
            del document.Root[key]
        document.save(output)
    return output.getvalue()


@pytest.mark.vcr
def test_a_rendition_gives_back_the_record_it_was_written_from(rendition):
    """The attachment carries the record, so nothing is read off the page."""
    subject, pdf = rendition

    back = Metadata(pdf)

    assert back.via == "pdf"
    assert back.is_valid
    assert back.id == subject.id
    assert back.type == "BlogPost"
    assert back.title == subject.title
    assert back.contributors == subject.contributors
    assert back.container == subject.container
    assert back.subjects == subject.subjects
    # each relation type is a property of its own in schema.org, so they come
    # back as a set rather than in the order the record listed them
    assert sorted(back.relations, key=lambda r: r["id"]) == sorted(
        subject.relations, key=lambda r: r["id"]
    )
    assert back.content == subject.content
    assert len(back.references) == len(subject.references)


@pytest.mark.vcr("test_a_rendition_gives_back_the_record_it_was_written_from.yaml")
def test_a_pdf_is_read_from_the_path_it_is_written_to(tmp_path, rendition):
    """A pdf on disk is bytes; every other input a path names is text."""
    subject, pdf = rendition
    file = tmp_path / "rendition.pdf"
    file.write_bytes(pdf)

    back = Metadata(str(file))

    assert back.via == "pdf"
    assert back.id == subject.id


@pytest.mark.vcr("test_a_rendition_gives_back_the_record_it_was_written_from.yaml")
def test_a_pdf_without_a_source_is_read_for_its_xmp_packet(rendition):
    """What any pdf says about itself, where it carries no record."""
    subject, pdf = rendition

    back = Metadata(without(pdf, "/Names"))

    assert back.is_valid
    assert back.id == subject.id
    # a pdf says it is a document; only the record it carries says more
    assert back.type == "Document"
    assert back.title == subject.title
    assert [c["person"]["family_name"] for c in back.contributors] == [
        "Ochsner",
        "Pampel",
        "Fenner",
    ]
    assert back.date_published == "2026-07-28"
    assert back.language == "en"
    assert back.license["id"] == "CC-BY-4.0"
    # the keywords the pdf carries, which say their scheme in the string
    assert back.subjects[0] == {
        "subject": "Information Systems and Management (Subfield)"
    }
    # what the packet has no room for
    assert back.container is None
    assert back.references is None
    assert back.content is None


@pytest.mark.vcr("test_a_rendition_gives_back_the_record_it_was_written_from.yaml")
def test_a_pdf_with_no_xmp_packet_is_read_for_its_info_dictionary(rendition):
    """The older of the two places a pdf keeps its own metadata."""
    subject, pdf = rendition

    back = Metadata(without(pdf, "/Names", "/Metadata"))

    assert back.is_valid
    # /DOI is what `finish_pdf` writes there and what a viewer shows
    assert back.id == subject.id
    assert back.title == subject.title
    assert [c["person"]["family_name"] for c in back.contributors] == [
        "Ochsner",
        "Pampel",
        "Fenner",
    ]
    assert back.date_published == "2026-07-28"
    assert back.description.startswith("The fragmentation of social media")


@pytest.mark.parametrize(
    "author, expected",
    [
        # the info dictionary joins authors with a comma, which is also what
        # separates a family name from a given one
        (
            "Catharina Ochsner, Heinz Pampel, Martin Fenner",
            ["Catharina Ochsner", "Heinz Pampel", "Martin Fenner"],
        ),
        ("Ochsner, Catharina", ["Ochsner, Catharina"]),
        ("Smith, J.; Doe, A.", ["Smith, J.", "Doe, A."]),
        ("Jane Doe", ["Jane Doe"]),
        # the xmp packet has no such problem: it holds a list
        (["Jane Doe", "John Smith"], ["Jane Doe", "John Smith"]),
        (None, []),
        ("", []),
    ],
)
def test_the_authors_a_pdf_names(author, expected):
    """A semicolon always separates authors; a comma only sometimes does."""
    assert pdf_authors(author) == expected


def test_what_is_not_a_pdf_is_not_found():
    """The reader reads pdfs, and says so about anything else."""
    assert read_pdf(b"<html></html>") == {"state": "not_found"}
    assert read_pdf(None) == {"state": "not_found"}
