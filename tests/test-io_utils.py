# pylint: disable=invalid-name
"""Test io_utils"""

from os import path, remove

import pytest  # noqa: F401

from commonmeta import Metadata
from commonmeta.io_utils import (
    download_file,
    get_extension,
    read_file,
    read_gz_file,
    read_pdf_attachment,
    read_pdf_metadata,
    read_zip_file,
    to_pdf_html,
    uncompress_content,
    unzip_content,
    write_file,
    write_gz_file,
    write_output,
    write_zip_file,
)
from commonmeta.readers.inveniordm_reader import search_by_doi


def test_read_file():
    "read_file"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json")
    assert len(read_file(filename)) == 150146


def test_read_gz_file():
    "read_gz_file"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json.gz")
    assert len(read_gz_file(filename)) == 150146


def test_read_zip_file():
    "read_zip_file"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json.zip")
    assert len(read_zip_file(filename)) == 150146


def test_uncompress_content():
    "uncompress_content"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json.gz")
    input = read_file(filename)
    output = uncompress_content(input)
    assert len(output) > len(input)


def test_unzip_content():
    "unzip_content"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json.zip")
    input = read_file(filename)
    output = unzip_content(input)
    assert len(output) > len(input)


def test_download_file():
    "download_file"
    url = "https://zenodo.org/records/15461402/files/front-matter/commonmeta-v0.25.0.zip?download=1"
    assert len(download_file(url)) == 18820287


def test_write_file():
    "write_file"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json")
    output = read_file(filename)
    new_filename = path.join(path.dirname(__file__), "fixtures", "posts1.json")
    assert write_file(new_filename, output) is None
    remove(new_filename)


def test_write_file_error():
    "write_file FileExistsError"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json")
    output = read_file(filename)
    with pytest.raises(FileExistsError):
        write_file(filename, output)


def test_write_gz_file():
    "write_gz_file"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json")
    output = read_file(filename)
    new_filename = path.join(path.dirname(__file__), "fixtures", "posts1.json.gz")
    assert write_gz_file(new_filename, output) is None
    remove(new_filename)


def test_write_zip_file():
    "write_zip_file"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json")
    output = read_file(filename)
    new_filename = path.join(path.dirname(__file__), "fixtures", "posts1.json.zip")
    assert write_zip_file(new_filename, output) is None
    remove(new_filename)


def test_get_extension():
    "get_extension"
    assert get_extension("test.json.gz") == ("test.json", ".json", ".gz")
    assert get_extension("test.yaml") == ("test.yaml", ".yaml", None)
    assert get_extension("test") == ("test.json", ".json", None)


def test_write_output():
    "write_output"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json")
    output = read_file(filename)
    new_filename = path.join(path.dirname(__file__), "fixtures", "posts1.json.zip")
    assert write_output(new_filename, output, [".json"]) is None
    remove(new_filename)


def test_write_output_wrong_extension():
    "write_output wrong extension"
    filename = path.join(path.dirname(__file__), "fixtures", "posts.json")
    output = read_file(filename)
    new_filename = path.join(path.dirname(__file__), "fixtures", "posts1.json.zip")
    with pytest.raises(ValueError):
        write_output(new_filename, output, [".yaml"])


@pytest.mark.vcr
def test_pdf_rendition_of_a_post_read_from_inveniordm(write_pdf_file):
    """Generate a PDF from InvenioRDM record."""
    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )
    assert subject.id == "https://doi.org/10.54900/xn57k-gyw73"
    assert subject.title == "Ten simple rules for scholarly blogging"
    assert len(subject.content) > 30000

    html = to_pdf_html(subject)
    pdf = write_pdf_file(subject)
    metadata = read_pdf_metadata(pdf)

    # the front matter the record was read for
    assert "<h1>Ten simple rules for scholarly blogging</h1>" in html
    assert '<span class="header">Upstream</span>' in html
    assert '<a href="https://orcid.org/0009-0005-3885-3951">' in html
    assert '<img class="orcid" alt="ORCID iD" src="orcid.svg" />' in html
    assert '<div class="date">Published July 28, 2026</div>' in html
    assert '<div class="keywords"><h4>Keywords</h4>Original Research</div>' in html

    # and what the pdf itself says it is
    assert metadata["id"] == subject.id
    assert metadata["title"] == subject.title
    assert metadata["authors"] == ["Catharina Ochsner", "Heinz Pampel", "Martin Fenner"]
    assert metadata["license"] == "CC-BY-4.0"
    assert metadata["language"] == "en"
    assert metadata["variant"] == "PDF/A-3a"
    assert metadata["tagged"] is True
    # the post travels inside the pdf as the source it was rendered from
    assert metadata["attachments"] == {"xn57k-gyw73.html": "text/html"}
    assert read_pdf_attachment(pdf).decode("utf-8") == subject.content
