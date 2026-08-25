# pylint: disable=invalid-name
"""Test io_utils"""

import logging
from base64 import b64encode
from os import path, remove
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest  # noqa: F401
import zstandard
from requests.exceptions import RequestException

from commonmeta import Metadata
from commonmeta.io_utils import (
    download_file,
    embed_image,
    get_extension,
    pdf_filename,
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
    assert metadata["attachments"] == {"10.54900-xn57k-gyw73.html": "text/html"}
    assert read_pdf_attachment(pdf).decode("utf-8") == subject.content


@pytest.mark.vcr("test_pdf_rendition_of_a_post_read_from_inveniordm.yaml")
def test_write_pdf_rendition_to_a_file(tmp_path, feature_image):
    """A rendition is written the way every other output format is.

    `write_output` takes the compression suffixes with it, so a rendition can
    be written compressed by naming it that way.
    """
    from conftest import offline_url_fetcher, require_weasyprint

    from commonmeta.io_utils import write_pdf_rendition

    require_weasyprint()
    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )

    plain = tmp_path / "post.pdf"
    pdf = write_pdf_rendition(subject, url_fetcher=offline_url_fetcher, file=str(plain))

    assert plain.read_bytes() == pdf
    assert read_pdf_metadata(plain.read_bytes())["title"] == subject.title

    # the same rendition, compressed, and refused when it would overwrite
    compressed = tmp_path / "post.pdf.zst"
    write_pdf_rendition(subject, url_fetcher=offline_url_fetcher, file=str(compressed))
    assert zstandard.ZstdDecompressor().decompress(compressed.read_bytes()) == pdf
    with pytest.raises(FileExistsError):
        write_pdf_rendition(subject, url_fetcher=offline_url_fetcher, file=str(plain))

    # and a name it does not write
    with pytest.raises(ValueError):
        write_pdf_rendition(subject, url_fetcher=offline_url_fetcher, file="post.json")


def test_pdf_filename_names_the_file_after_the_doi():
    """The whole doi, with its slash made safe for a filename."""

    class Meta:
        id = "https://doi.org/10.59350/j63pf-38v68"

    assert pdf_filename(Meta()) == "10.59350-j63pf-38v68.pdf"


def test_pdf_filename_replaces_every_slash():
    """A name with a slash in it is a path rather than a file."""

    class Meta:
        id = "https://doi.org/10.5555/foo/bar"

    assert pdf_filename(Meta()) == "10.5555-foo-bar.pdf"


def test_pdf_filename_prefers_the_record_to_the_run():
    """Two dois are in play, and only one of them lasts.

    Rogue Scholar mints a random suffix for a post that has none, on every read
    of the feed, while the record is matched by guid - so metadata.id is a
    different doi each run for the same post. Naming the file from it left one
    record holding three entries, each named after a doi that existed only for
    the length of the run that made it.
    """

    class Meta:
        id = "https://doi.org/10.59350/j63pf-38v68"  # minted this run

    # The record's own doi, which upsert_record adopts and the update leaves
    # alone, names the file.
    assert (
        pdf_filename(Meta(), {"doi": "https://doi.org/10.59350/rqawv-7g546"})
        == "10.59350-rqawv-7g546.pdf"
    )
    # A bare doi is accepted as readily as a url.
    assert (
        pdf_filename(Meta(), {"doi": "10.59350/rqawv-7g546"})
        == "10.59350-rqawv-7g546.pdf"
    )
    # A genuinely new post has no record to take a doi from, so the one in hand
    # is the one it will keep.
    assert pdf_filename(Meta(), None) == "10.59350-j63pf-38v68.pdf"
    assert pdf_filename(Meta(), {}) == "10.59350-j63pf-38v68.pdf"
    assert pdf_filename(Meta(), {"doi": None}) == "10.59350-j63pf-38v68.pdf"


def test_pdf_filename_without_a_doi():
    """Nothing to name it after, and a pdf still has to be called something."""

    class Meta:
        id = "https://rogue-scholar.org/records/e1ndf-19s62"

    assert pdf_filename(Meta()) == "content.pdf"
    assert pdf_filename(Meta(), {"doi": None}) == "content.pdf"


def test_embed_image_returns_a_data_uri():
    """The feature image travels inside the pdf rather than being linked."""
    from conftest import PNG_PIXEL, image_response

    from commonmeta import io_utils

    class Meta:
        image = "https://example.org/feature.png"

    get = Mock(return_value=image_response(PNG_PIXEL, "image/png"))
    with patch.object(io_utils, "http", SimpleNamespace(get=get)):
        uri = embed_image(Meta())

    assert uri == f"data:image/png;base64,{b64encode(PNG_PIXEL).decode()}"
    assert get.call_args.args[0] == "https://example.org/feature.png"
    # asked for as an image: a blog behind a filter answers a bare request with
    # 406 Not Acceptable
    assert get.call_args.kwargs["headers"]["Accept"].startswith("image/")


def test_embed_image_takes_the_type_the_server_serves():
    """A jpeg is a jpeg, whatever the url ends in."""
    from conftest import image_response

    from commonmeta import io_utils

    class Meta:
        image = "https://example.org/feature.png"

    get = Mock(
        return_value=image_response(b"\xff\xd8\xff", "image/jpeg; charset=binary")
    )
    with patch.object(io_utils, "http", SimpleNamespace(get=get)):
        uri = embed_image(Meta())

    assert uri.startswith("data:image/jpeg;base64,")


def test_embed_image_without_an_image():
    """Most records have none, and nothing is fetched for them."""
    from commonmeta import io_utils

    class Meta:
        image = None

    get = Mock()
    with patch.object(io_utils, "http", SimpleNamespace(get=get)):
        assert embed_image(Meta()) is None

    get.assert_not_called()


@pytest.mark.parametrize(
    "response",
    [
        # the blog no longer serves it
        SimpleNamespace(raise_for_status=Mock(side_effect=RequestException("404"))),
        # or serves an error page where the image used to be
        SimpleNamespace(
            content=b"<html>Not found</html>",
            headers={"Content-Type": "text/html"},
            raise_for_status=lambda: None,
        ),
        # or nothing that says what it is
        SimpleNamespace(content=b"", headers={}, raise_for_status=lambda: None),
    ],
)
def test_embed_image_that_cannot_be_used(response, caplog):
    """An image the render cannot use is left out, and said so once.

    WeasyPrint draws the alt text where an image fails, which would print
    "Feature image" across the title page.
    """
    from commonmeta import io_utils

    class Meta:
        image = "https://example.org/feature.png"

    with caplog.at_level(logging.WARNING, logger="commonmeta.io_utils"):
        with patch.object(
            io_utils, "http", SimpleNamespace(get=Mock(return_value=response))
        ):
            assert embed_image(Meta()) is None

    assert "https://example.org/feature.png" in caplog.records[0].getMessage()


def test_write_pdf_names_a_file_and_returns_the_bytes(
    tmp_path, weasyprint, feature_image
):
    """What a caller that names a file gets: the file, and what went in it."""
    from commonmeta.io_utils import write_pdf

    class Meta:
        id = "https://doi.org/10.5555/a-record"
        title = "A record with no post behind it"
        content = None
        contributors = date_published = date_updated = None
        description = image = language = license = container = subjects = None

    output = tmp_path / "record.pdf"
    pdf = write_pdf(Meta(), str(output))

    assert output.read_bytes() == pdf
    assert read_pdf_metadata(pdf)["title"] == "A record with no post behind it"


def test_write_pdf_without_a_renderer(tmp_path, monkeypatch):
    """A caller that named a file is told why there is none, rather than None.

    WeasyPrint is absent on Python 3.9, and on any machine without pango.
    """
    from commonmeta import io_utils
    from commonmeta.io_utils import write_pdf

    class Meta:
        id = "https://doi.org/10.5555/a-record"
        content = None

    monkeypatch.setattr(io_utils, "load_weasyprint", lambda: None)

    with pytest.raises(ValueError, match="pango"):
        write_pdf(Meta(), str(tmp_path / "record.pdf"))
    assert not (tmp_path / "record.pdf").exists()


def test_write_pdf_refuses_a_name_it_does_not_write(
    tmp_path, weasyprint, feature_image
):
    """The extension says what a file is; a pdf is not written to post.json."""
    from commonmeta.io_utils import write_pdf

    class Meta:
        id = "https://doi.org/10.5555/a-record"
        title = "A record"
        content = None
        contributors = date_published = date_updated = None
        description = image = language = license = container = subjects = None

    with pytest.raises(ValueError, match="File format not supported"):
        write_pdf(Meta(), str(tmp_path / "record.json"))
