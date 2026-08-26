# pylint: disable=invalid-name
"""Test io_utils"""

import io
import logging
import os
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
    to_pdf_content,
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
    assert '<div class="date">Blog post published July 28, 2026</div>' in html
    assert (
        '<div class="keywords"><h4>Keywords</h4>Information Systems and '
        "Management (Subfield), Academic Publishing and Open Access (Topic), "
        "Original Research</div>" in html
    )

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
        type = None
        contributors = date_published = date_updated = None
        description = image = language = license = container = subjects = None
        references = None

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
        type = None
        contributors = date_published = date_updated = None
        description = image = language = license = container = subjects = None
        references = None

    with pytest.raises(ValueError, match="File format not supported"):
        write_pdf(Meta(), str(tmp_path / "record.json"))


def test_find_pango_points_dyld_at_homebrew(monkeypatch):
    """A mac finds pango where brew put it, without the shell saying so.

    dyld looks for the libraries WeasyPrint dlopens by leaf name only in
    DYLD_FALLBACK_LIBRARY_PATH, which lists neither homebrew directory - and
    SIP strips the variable from a protected binary, so a shell profile cannot
    be relied on to carry it either.
    """
    from commonmeta.io_utils import DYLD_DEFAULT_LIB_PATHS, find_pango

    monkeypatch.setattr("sys.platform", "darwin")
    monkeypatch.setattr("os.path.isdir", lambda p: p == "/opt/homebrew/lib")
    monkeypatch.setenv("DYLD_FALLBACK_LIBRARY_PATH", "/opt/mine/lib")

    find_pango()

    paths = os.environ["DYLD_FALLBACK_LIBRARY_PATH"].split(os.pathsep)
    assert paths[0] == "/opt/mine/lib"  # what was already there stays, and first
    assert "/opt/homebrew/lib" in paths
    # the defaults setting the variable would otherwise have dropped
    assert set(DYLD_DEFAULT_LIB_PATHS) <= set(paths)


def test_find_pango_leaves_other_platforms_alone(monkeypatch):
    """Everywhere else the loader finds the libraries on its own."""
    from commonmeta.io_utils import find_pango

    monkeypatch.setattr("sys.platform", "linux")
    monkeypatch.delenv("DYLD_FALLBACK_LIBRARY_PATH", raising=False)

    find_pango()

    assert "DYLD_FALLBACK_LIBRARY_PATH" not in os.environ


@pytest.mark.vcr("test_pdf_rendition_of_a_post_read_from_inveniordm.yaml")
def test_the_pdf_says_one_thing_about_its_keywords(write_pdf_file):
    """What the title page prints is what the pdf carries as its own metadata."""
    from commonmeta.io_utils import to_pdf_keywords

    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )

    metadata = read_pdf_metadata(write_pdf_file(subject))

    assert metadata["keywords"] == to_pdf_keywords(subject)
    assert metadata["keywords"] == [
        "Information Systems and Management (Subfield)",
        "Academic Publishing and Open Access (Topic)",
        "Original Research",
    ]


@pytest.mark.parametrize(
    "text, expected",
    [
        # the emoji was the separator, and the gap it left goes with it
        ("AIMOS 🔸 Mindless 🔸 Top 10", "AIMOS Mindless Top 10"),
        ("Hello🎉world", "Helloworld"),
        # a run goes as one, and the space it stood in stays a single space,
        # which html collapses wherever it lands
        ("Launch day 🚀🚀", "Launch day "),
        # a flag is a pair of regional indicators, a keycap a digit and a mark
        ("Reading in 🇩🇪 today", "Reading in today"),
        # what a title says with punctuation is not an emoji
        ("Café — naïve “quotes”, 50% ± 2, α→β", "Café — naïve “quotes”, 50% ± 2, α→β"),
    ],
)
def test_strip_emoji(text, expected):
    """A page drops what it would have to draw from a colour font."""
    from commonmeta.io_utils import strip_emoji

    assert strip_emoji(text) == expected


def test_the_page_drops_an_emoji_the_metadata_keeps(write_pdf_file):
    """A colour font fails PDF/A, and a pdf's own metadata is text, not glyphs.

    https://rogue-scholar.org/records/ywetc-na038 is a post whose title uses
    emoji as separators; embedding Apple Color Emoji for them cost the
    rendition its conformance (ISO 19005-3 6.2.11.5, glyph widths).
    """
    import pikepdf
    from conftest import sample_metadata

    sample = sample_metadata(
        "<p>Body 🎉</p>", title="AIMOS Presentation 🔸 Mindless Transparency"
    )

    pdf = write_pdf_file(sample)

    with pikepdf.open(io.BytesIO(pdf)) as document:
        fonts = {
            str(obj.BaseFont)
            for obj in document.objects
            if isinstance(obj, pikepdf.Dictionary)
            and obj.get("/Type") == pikepdf.Name.Font
            and "/BaseFont" in obj
        }
    assert fonts and all("Emoji" not in font for font in fonts)
    # the page reads without them, the metadata reads with them
    assert read_pdf_metadata(pdf)["title"] == (
        "AIMOS Presentation 🔸 Mindless Transparency"
    )


@pytest.mark.parametrize(
    "src, page, poster",
    [
        (
            "https://www.youtube-nocookie.com/embed/okjTV1oX4RU?rel=0&autoplay=0",
            "https://youtu.be/okjTV1oX4RU",
            "https://img.youtube.com/vi/okjTV1oX4RU/hqdefault.jpg",
        ),
        (
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
        ),
        # vimeo publishes no thumbnail at a known address, so the link stands alone
        ("https://player.vimeo.com/video/76979871", "https://vimeo.com/76979871", ""),
        # anything else an iframe carries is not a video
        ("https://example.org/subscribe", None, None),
    ],
)
def test_to_pdf_video(src, page, poster):
    """Where an embed points, and the frame to show for it."""
    from commonmeta.io_utils import to_pdf_video

    assert to_pdf_video(src) == (None if page is None else (page, poster))


def test_to_pdf_content_shows_a_video_as_its_poster_frame():
    """A pdf has no browsing context: an iframe draws nothing at all.

    https://rogue-scholar.org/records/ywetc-na038 embeds a talk this way, and
    the rendition lost it without trace.
    """
    from conftest import PNG_PIXEL, image_response

    from commonmeta import io_utils

    content = (
        '<p>Before</p><div class="youtube-wrap"><iframe '
        'src="https://www.youtube-nocookie.com/embed/okjTV1oX4RU?rel=0"'
        "></iframe></div><p>After</p>"
    )
    get = Mock(return_value=image_response(PNG_PIXEL, "image/jpeg"))

    with patch.object(io_utils, "http", SimpleNamespace(get=get)):
        html = to_pdf_content(content, "en")

    assert (
        get.call_args.args[0] == "https://img.youtube.com/vi/okjTV1oX4RU/hqdefault.jpg"
    )
    assert '<figure class="video">' in html
    assert '<a href="https://youtu.be/okjTV1oX4RU">' in html
    assert '<img alt="Video" src="data:image/jpeg;base64,' in html
    # and the link is readable on paper, where a link cannot be followed
    assert (
        "<figcaption>"
        '<a href="https://youtu.be/okjTV1oX4RU">https://youtu.be/okjTV1oX4RU</a>'
        "</figcaption>" in html
    )
    assert "<iframe" not in html
    assert "<p>Before</p>" in html and "<p>After</p>" in html


def test_to_pdf_content_keeps_the_link_when_the_poster_cannot_be_had():
    """A thumbnail is worth a request, not a render: the link is the point."""
    from commonmeta import io_utils

    content = '<iframe src="https://player.vimeo.com/video/76979871"></iframe>'
    get = Mock(side_effect=AssertionError("vimeo has no thumbnail to fetch"))

    with patch.object(io_utils, "http", SimpleNamespace(get=get)):
        html = to_pdf_content(content, "en")

    assert '<figure class="video"><figcaption>' in html
    assert '<a href="https://vimeo.com/76979871">https://vimeo.com/76979871</a>' in html
    assert "<img" not in html


@pytest.mark.parametrize(
    "reference, expected",
    [
        # the citation text, with the identifier after it as a link
        (
            {
                "id": "https://doi.org/10.1177/0741088313493610",
                "unstructured": "Luzón, M. J. (2013). Public Communication of "
                "Science in Blogs. <i>Written Communication</i>, <i>30</i>(4).",
            },
            "<li>Luzón, M. J. (2013). Public Communication of Science in Blogs. "
            "<i>Written Communication</i>, <i>30</i>(4). "
            '<a href="https://doi.org/10.1177/0741088313493610">'
            "https://doi.org/10.1177/0741088313493610</a></li>",
        ),
        # the current schema calls the citation text `reference`
        (
            {"reference": "Rettberg, J. W. (2008). Blogging. Polity."},
            "<li>Rettberg, J. W. (2008). Blogging. Polity.</li>",
        ),
        # a citation that spells the identifier out does not get it twice
        (
            {
                "id": "https://doi.org/10.5555/12345678",
                "reference": "A work. https://doi.org/10.5555/12345678",
            },
            "<li>A work. https://doi.org/10.5555/12345678</li>",
        ),
        # an identifier is a reference on its own; nothing is not
        (
            {"id": "https://doi.org/10.5555/12345678"},
            '<li><a href="https://doi.org/10.5555/12345678">'
            "https://doi.org/10.5555/12345678</a></li>",
        ),
        ({"id": None, "unstructured": None}, None),
        ("not a reference", None),
    ],
)
def test_to_pdf_reference(reference, expected):
    """One entry of the reference list, from either shape of the field."""
    from commonmeta.io_utils import to_pdf_reference

    assert to_pdf_reference(reference) == expected


def test_to_pdf_references_closes_the_rendition():
    """The works a record cites are printed after the post that cites them."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_html

    sample = sample_metadata("<p>Body</p>")
    sample.references = [
        {"unstructured": "Burton, M. (2015). Blogs as infrastructure. [Phd]."},
        {
            "id": "https://doi.org/10.1371/journal.pbio.0060240",
            "unstructured": "Batts, S. A. (2008). Advancing Science.",
        },
    ]

    html = to_pdf_html(sample)

    assert html.index("<p>Body</p>") < html.index('<section class="references">')
    assert (
        '<section class="references"><h2>References</h2><ol>'
        "<li>Burton, M. (2015). Blogs as infrastructure. [Phd].</li>"
        "<li>Batts, S. A. (2008). Advancing Science. "
        '<a href="https://doi.org/10.1371/journal.pbio.0060240">'
        "https://doi.org/10.1371/journal.pbio.0060240</a></li></ol></section>" in html
    )


def test_to_pdf_references_are_written_in_the_language_of_the_post():
    """The heading over them reads as the rest of the front matter does."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_references

    sample = sample_metadata("<p>Text</p>")
    sample.references = [{"reference": "Ein Werk."}]

    assert "<h2>Literatur</h2>" in to_pdf_references(sample, "de")


def test_to_pdf_references_are_not_printed_twice():
    """Rogue Scholar reads a record's references out of the post that lists
    them, so a post with its own list would otherwise carry it twice."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_html

    sample = sample_metadata(
        "<p>Body</p><h2>References</h2><ol><li>Rettberg, J. W. (2008).</li></ol>"
    )
    sample.references = [{"reference": "Rettberg, J. W. (2008). Blogging. Polity."}]

    assert '<section class="references">' not in to_pdf_html(sample)


def test_to_pdf_references_of_a_record_that_cites_nothing():
    """Nothing is printed, rather than an empty page with a heading."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_references

    sample = sample_metadata("<p>Body</p>")
    sample.references = []

    assert to_pdf_references(sample, "en") == ""


@pytest.mark.parametrize(
    "content, expected",
    [
        ("<h2>References</h2><ol><li>A work.</li></ol>", True),
        ("<h3>Literaturverzeichnis</h3>", True),
        ("<h2>Bibliography:</h2>", True),
        ("<h2>Referências</h2>", True),
        ("<p>References</p>", False),
        ("<h2>Reference rot</h2>", False),
        (None, False),
    ],
)
def test_has_reference_list(content, expected):
    """What marks a post that prints the works it cites: the heading over them."""
    from commonmeta.io_utils import has_reference_list

    assert has_reference_list(content) is expected


@pytest.mark.parametrize(
    "type, language, expected",
    [
        ("JournalArticle", "en", "Journal article"),
        ("JournalArticle", "de", "Zeitschriftenartikel"),
        ("BlogPost", "de", "Blogbeitrag"),
        ("BlogPost", "fr", "Billet de blog"),
        ("Software", "pt", "Software"),
        # a type no language has a name for is called what its camel case says
        ("StudyRegistration", "en", "Study registration"),
        ("StudyRegistration", "nl", "Study registration"),
        # and one that says nothing a reader can use is left off the page
        ("Other", "en", None),
        (None, "en", None),
    ],
)
def test_to_pdf_type(type, language, expected):
    """What the record is, in the language the rendition is written in."""
    from commonmeta.io_utils import to_pdf_type

    assert to_pdf_type(type, language) == expected


@pytest.mark.parametrize(
    "language, expected",
    [
        ("en", "Journal article published May 27, 2026"),
        ("de", "Zeitschriftenartikel veröffentlicht am 27. Mai 2026"),
        # the romance languages name the date rather than follow the type with
        # a participle, which would have to agree with the noun before it
        ("es", "Artículo de revista, fecha de publicación: 27 de mayo de 2026"),
        ("fr", "Article de revue, date de publication : 27 mai 2026"),
        ("it", "Articolo di rivista, data di pubblicazione: 27 maggio 2026"),
        ("pt", "Artigo de revista, data de publicação: 27 de maio de 2026"),
    ],
)
def test_to_pdf_published(language, expected):
    """The line under the byline says what the record is and when it came out.

    https://doi.org/10.1021/acs.jmedchem.6c00463, as each language writes it.
    """
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_published

    sample = sample_metadata(None)
    sample.type = "JournalArticle"
    sample.date_published = "2026-05-27"

    assert to_pdf_published(sample, language) == expected


def test_to_pdf_published_without_a_type():
    """A record whose type says nothing keeps the date on its own."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_published

    sample = sample_metadata(None)
    sample.date_published = "2026-05-27"

    assert to_pdf_published(sample, "en") == "Published May 27, 2026"
    sample.type = "Other"
    assert to_pdf_published(sample, "en") == "Published May 27, 2026"
    sample.language = "de"
    assert to_pdf_published(sample, "de") == "Veröffentlicht 27. Mai 2026"


def test_to_pdf_published_without_a_date():
    """A record with no publication date gets no line at all."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_published

    sample = sample_metadata(None)
    sample.type = "JournalArticle"

    assert to_pdf_published(sample, "en") is None
    assert '<div class="date">' not in to_pdf_html(sample)


def test_pdf_type_names_cover_the_vocabulary():
    """Every type a record can have has a name in each language.

    A missing one would put an English word in the middle of a German line,
    so the table is held against the schema the types come from.
    """
    import json

    import commonmeta
    from commonmeta.io_utils import PDF_TYPE_NAMES

    schema = json.loads(
        read_file(
            path.join(
                path.dirname(commonmeta.__file__), "resources", "commonmeta_v1.0.json"
            )
        )
    )
    # "Other" names nothing a reader can use, and is left off the page
    types = set(schema["$defs"]["type"]["enum"]) - {"Other"}
    for language, names in PDF_TYPE_NAMES.items():
        assert set(names) == types, language
