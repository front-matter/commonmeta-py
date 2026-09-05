# pylint: disable=invalid-name
"""Test io_utils"""

import io
import logging
import os
from base64 import b64encode
from os import path, remove
from types import SimpleNamespace
from unittest.mock import Mock, patch

import orjson
import pytest  # noqa: F401
import zstandard
from requests.exceptions import RequestException

from commonmeta import Metadata
from commonmeta.io_utils import (
    download_file,
    embed_image,
    former_pdf_filenames,
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
def test_pdf_rendition_of_a_post_read_from_inveniordm(render_pdf):
    """Generate a PDF from InvenioRDM record."""
    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )
    assert subject.id == "https://doi.org/10.54900/xn57k-gyw73"
    assert subject.title == "Ten simple rules for scholarly blogging"
    assert len(subject.content) > 30000

    html = to_pdf_html(subject)
    pdf = render_pdf(subject)
    metadata = read_pdf_metadata(pdf)

    # the front matter the record was read for
    assert "<h1>Ten simple rules for scholarly blogging</h1>" in html
    assert '<a href="https://orcid.org/0009-0005-3885-3951">' in html
    assert '<img class="orcid" alt="ORCID iD" src="orcid.svg" />' in html
    assert (
        '<div class="date">Blog post published July 28, 2026 in '
        "<i>Upstream</i></div>" in html
    )
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
    # the post travels inside the pdf as the source it was rendered from,
    # as a page that carries the record in its head
    assert metadata["attachments"] == {"10.54900_xn57k-gyw73.html": "text/html"}
    attachment = read_pdf_attachment(pdf).decode("utf-8")
    assert f"<body>\n{subject.content}\n</body>" in attachment
    assert (
        '<meta name="citation_title" content="Ten simple rules for scholarly '
        'blogging">' in attachment
    )


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

    assert pdf_filename(Meta()) == "10.59350_j63pf-38v68.pdf"


def test_former_pdf_filenames_offers_the_old_name():
    """The slash used to be a dash, and the old file is still on the record."""
    assert "10.53731-9r3yj-zwy78.pdf" in former_pdf_filenames(
        "10.53731_9r3yj-zwy78.pdf"
    )


def test_former_pdf_filenames_keeps_an_underscore_in_the_suffix():
    """Only the slash became an underscore; the suffix's own were always there.

    `10.59350/zotero_fr.5552` was written as `10.59350-zotero_fr.5552.pdf`.
    Putting every underscore back as a dash asked for a file that was never
    written, and the real predecessor stayed on the record beside the new one.
    """
    assert "10.59350-zotero_fr.5552.pdf" in former_pdf_filenames(
        "10.59350_zotero_fr.5552.pdf"
    )


def test_former_pdf_filenames_covers_a_doi_with_two_slashes():
    """Where the underscores were all slashes, they all go back to dashes."""
    assert "10.5555-foo-bar.pdf" in former_pdf_filenames("10.5555_foo_bar.pdf")


def test_former_pdf_filenames_has_nothing_to_offer_without_a_slash():
    """A fallback name was never written under another one."""
    assert former_pdf_filenames("content.pdf") == []


def test_pdf_filename_replaces_every_slash():
    """A name with a slash in it is a path rather than a file."""

    class Meta:
        id = "https://doi.org/10.5555/foo/bar"

    assert pdf_filename(Meta()) == "10.5555_foo_bar.pdf"


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
        == "10.59350_rqawv-7g546.pdf"
    )
    # A bare doi is accepted as readily as a url.
    assert (
        pdf_filename(Meta(), {"doi": "10.59350/rqawv-7g546"})
        == "10.59350_rqawv-7g546.pdf"
    )
    # A genuinely new post has no record to take a doi from, so the one in hand
    # is the one it will keep.
    assert pdf_filename(Meta(), None) == "10.59350_j63pf-38v68.pdf"
    assert pdf_filename(Meta(), {}) == "10.59350_j63pf-38v68.pdf"
    assert pdf_filename(Meta(), {"doi": None}) == "10.59350_j63pf-38v68.pdf"


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
def test_the_pdf_says_one_thing_about_its_keywords(render_pdf):
    """What the title page prints is what the pdf carries as its own metadata."""
    from commonmeta.io_utils import to_pdf_keywords

    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )

    metadata = read_pdf_metadata(render_pdf(subject))

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


def test_the_page_drops_an_emoji_the_metadata_keeps(render_pdf):
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

    pdf = render_pdf(sample)

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


@pytest.mark.vcr("test_pdf_rendition_of_a_post_read_from_inveniordm.yaml")
def test_an_embedded_file_is_associated_with_the_document_once(render_pdf):
    """One entry in /AF per file, which is what the association means.

    WeasyPrint 69 collects the attachments twice, from the EmbeddedFiles name
    tree and from its own scan for /Filespec objects, and lists each of them
    twice in the array PDF/A-3 asks for.
    """
    import pikepdf

    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )

    pdf = render_pdf(subject)

    with pikepdf.open(io.BytesIO(pdf)) as document:
        associated = document.Root.AF
        names = document.Root.Names.EmbeddedFiles.Names
        assert [str(name) for name in names[0::2]] == ["10.54900_xn57k-gyw73.html"]
        assert len(associated) == 1
        # the one association is the file itself, rather than a copy of it
        assert associated[0].objgen == names[1].objgen
        assert str(associated[0].AFRelationship) == "/Source"


@pytest.mark.vcr("test_pdf_rendition_of_a_post_read_from_inveniordm.yaml")
def test_the_attachment_says_what_the_post_is():
    """The html a rendition carries is a page, not a fragment.

    It says what the post is twice: as schema.org json-ld, which is what this
    library reads back, and as the Highwire meta tags Google Scholar reads.
    """
    from commonmeta.io_utils import to_attachment_html

    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )

    html = to_attachment_html(subject)

    assert html.startswith('<!doctype html>\n<html lang="en">')
    assert (
        '<link rel="canonical" href="https://upstream.force11.org/'
        'ten-simple-rules-for-scholarly-blogging/">' in html
    )
    # the three tags Scholar requires, and the venue it cites the post by
    assert '<meta name="citation_author" content="Ochsner, Catharina">' in html
    assert '<meta name="citation_publication_date" content="2026/7/28">' in html
    assert '<meta name="citation_journal_title" content="Upstream">' in html
    assert '<meta name="citation_doi" content="10.54900/xn57k-gyw73">' in html

    json_ld = orjson.loads(
        html.split('<script type="application/ld+json">')[1].split("</script>")[0]
    )
    assert json_ld["@id"] == subject.id
    assert json_ld["@type"] == "BlogPosting"
    # the body of the page is the body of the post, so the json-ld does not
    # carry a second copy of it
    assert "articleBody" not in json_ld
    assert f"<body>\n{subject.content}\n</body>" in html


@pytest.mark.vcr
def test_the_record_is_read_back_out_of_the_attachment(render_pdf):
    """A rendition taken apart gives back the record it was written from."""
    from commonmeta.readers.schema_org_reader import parse_schema_org_html

    record_id = search_by_doi("10.54900/xn57k-gyw73", "rogue-scholar.org", None)
    subject = Metadata(
        f"https://rogue-scholar.org/api/records/{record_id}", via="inveniordm"
    )

    attachment = read_pdf_attachment(render_pdf(subject)).decode("utf-8")
    back = Metadata(
        orjson.dumps(
            parse_schema_org_html(attachment, subject.url, content=True)
        ).decode("utf-8"),
        via="schema_org",
    )

    assert back.is_valid
    assert back.id == subject.id
    assert back.title == subject.title
    assert back.contributors == subject.contributors
    assert back.container == subject.container
    assert back.subjects == subject.subjects
    assert back.content == subject.content
    assert len(back.references) == len(subject.references)


# a table whose caption lands near the foot of the page, which is where the
# rendition used to fail: the spacer puts it there without depending on how a
# paragraph of text happens to break
TABLE_WITH_CAPTION = (
    "<table><caption>Changes in publication types</caption>"
    "<thead><tr><th>Type</th><th>Count</th></tr></thead><tbody>"
    + "".join(f"<tr><td>row {i}</td><td>{i}</td></tr>" for i in range(12))
    + "</tbody></table>"
)


@pytest.mark.parametrize("spacer", range(18, 27))
def test_a_table_caption_is_not_left_at_a_page_break(render_pdf, spacer):
    """A caption keeps its table, whatever height the page break falls at.

    WeasyPrint 69 cannot build a structure tree for a table whose caption was
    left on the page before it - it raises `Table wrapper without a table` -
    and the failure took the whole record push with it, so the stylesheet
    keeps a caption with the first row it describes. 10.59350/4r6jj-90k30 is a
    post it failed on: a Quarto analysis whose first table is captioned.
    """
    from conftest import sample_metadata

    sample = sample_metadata(
        f'<div style="height: {spacer}cm"></div>{TABLE_WITH_CAPTION}'
    )

    # the pdf is still tagged: the rendition did not fall back to writing one
    # without a structure tree
    assert read_pdf_metadata(render_pdf(sample))["tagged"] is True


def test_a_page_weasyprint_cannot_tag_is_written_untagged(caplog):
    """A rendition that cannot be tagged is written anyway, and says so.

    The stylesheet keeps captions off page breaks, but `break-after: avoid` is
    a hint rather than a guarantee, and a rendition that raises would take the
    record push with it.
    """
    from commonmeta.io_utils import write_pdf_bytes

    def write_pdf(**options):
        if options["pdf_variant"].endswith("a"):
            raise ValueError("Table wrapper without a table")
        return b"%PDF-untagged"

    renders = []

    def render():
        renders.append(1)
        return SimpleNamespace(write_pdf=write_pdf)

    metadata = SimpleNamespace(id="https://doi.org/10.59350/4r6jj-90k30")

    with caplog.at_level(logging.WARNING):
        pdf = write_pdf_bytes(render, metadata, {"pdf_variant": "pdf/a-3a"})

    # the pages are laid out again rather than written twice: a document that
    # raised part way through tagging carries what it had already built
    assert len(renders) == 2

    assert pdf == b"%PDF-untagged"
    assert "pdf/a-3b" in caplog.text


def test_a_page_that_fails_for_another_reason_is_not_written(caplog):
    """Only the tagging failure falls back; everything else is a failure."""
    from commonmeta.io_utils import write_pdf_bytes

    def write_pdf(**options):
        raise ValueError("Font is not embeddable")

    metadata = SimpleNamespace(id="https://doi.org/10.59350/4r6jj-90k30")

    with pytest.raises(ValueError, match="Font is not embeddable"):
        write_pdf_bytes(
            lambda: SimpleNamespace(write_pdf=write_pdf),
            metadata,
            {"pdf_variant": "pdf/a-3a"},
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


def test_to_pdf_content_marks_the_reference_list_the_post_prints():
    """The works cited begin a page, wherever they are written.

    A post that lists them itself had them run on from the text - the
    stylesheet can only break before something it can select, so the heading
    is marked here.
    """
    content = (
        "<h2>Funding</h2><p>Funded by nobody.</p>"
        '<h2 class="wp-block-heading">References</h2>'
        "<ol><li>Rettberg, J. W. (2008). Blogging. Polity.</li></ol>"
    )

    html = to_pdf_content(content, "en")

    assert '<h2 class="wp-block-heading references">References</h2>' in html
    # the heading over anything else is left alone
    assert "<h2>Funding</h2>" in html


def test_to_pdf_content_leaves_a_post_without_a_reference_list_alone():
    """Nothing is marked in a post that cites nothing, and nothing is parsed."""
    content = "<h2>Reference rot</h2><p>Links die.</p>"

    assert to_pdf_content(content, "en") == content


def test_to_pdf_content_drops_a_style_nothing_here_defines():
    """A post's inline styles reach for its site's custom properties.

    WeasyPrint resolves an empty expression for `calc()` around a `var()` no
    stylesheet here sets, and fails that on an assertion -- which took the pdf,
    and the post with it. The declaration has no value to compute either way.
    """
    content = (
        '<p style="color: red; font-size: calc(var(--font-size-14) + '
        'var(--offset, 0px))">Hello</p>'
    )

    html = to_pdf_content(content, "en")

    assert 'style="color: red"' in html
    assert "calc(" not in html


def test_to_pdf_content_keeps_a_property_the_same_style_defines():
    """Most of them resolve: tailwind sets --tw-shadow beside the rule reading it."""
    content = '<p style="--tw-shadow: 0 0 #0000; box-shadow: var(--tw-shadow)">Hi</p>'

    assert to_pdf_content(content, "en") == content


def test_to_pdf_content_keeps_a_data_uri_whole():
    """A declaration is not split on the semicolon inside a value.

    `url(data:image/svg+xml;base64,...)` names its encoding with one, and
    cutting there would leave two halves of a rule that draws nothing.
    """
    style = "background: url(data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=); top: var(--x)"
    content = f'<p style="{style}">Hi</p>'

    html = to_pdf_content(content, "en")

    assert "data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=" in html
    assert "var(--x)" not in html


def test_to_pdf_reference_keeps_the_markup_a_citation_carries():
    """A citation says things in markup: a journal name is set in italics, a
    formula and an ordinal in <sub> and <sup>, and a link points somewhere."""
    from commonmeta.io_utils import to_pdf_reference

    entry = to_pdf_reference(
        {
            "reference": "Smith, A. (2020). Effects of CO<sub>2</sub> and the "
            "2<sup>nd</sup> law. <b>Nature</b>, <i>12</i>(4). "
            '<a href="https://example.org/paper">Full text</a>'
        }
    )

    assert entry == (
        "<li>Smith, A. (2020). Effects of CO<sub>2</sub> and the 2<sup>nd</sup> "
        'law. <b>Nature</b>, <i>12</i>(4). <a href="https://example.org/paper">'
        "Full text</a></li>"
    )


def test_to_pdf_reference_drops_markup_that_is_not_inline():
    """What a citation cannot carry into the pdf: layout, scripts, and an
    address that would run one."""
    from commonmeta.io_utils import to_pdf_reference

    entry = to_pdf_reference(
        {
            "reference": "<div>Smith, A. (2020).</div><script>alert(1)</script>"
            '<a href="javascript:alert(1)">Nature</a>'
        }
    )

    assert entry == "<li>Smith, A. (2020).<a>Nature</a></li>"
    assert "alert(1)" not in entry


@pytest.mark.parametrize(
    "container, expected",
    [
        # named rather than linked, whatever the container says it is: the one
        # address a title page points at is the record's own
        (
            {
                "title": "Journal of Medicinal Chemistry",
                "identifiers": [{"identifier": "0022-2623", "identifier_type": "ISSN"}],
            },
            "<i>Journal of Medicinal Chemistry</i>",
        ),
        ({"title": "The Ideophone", "platform": "WordPress"}, "<i>The Ideophone</i>"),
        # and the markup a name carries is its own
        (
            {"title": "Journal of <i>Drosophila</i> Research"},
            "<i>Journal of <i>Drosophila</i> Research</i>",
        ),
        ({}, None),
        (None, None),
    ],
)
def test_to_pdf_container(container, expected):
    """The journal or blog the work came out in, as the title page names it."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_container

    sample = sample_metadata(None)
    sample.container = container

    assert to_pdf_container(sample) == expected


@pytest.mark.parametrize(
    "language, expected",
    [
        (
            "en",
            "Journal article published May 27, 2026 in "
            "<i>Journal of Medicinal Chemistry</i>",
        ),
        (
            "de",
            "Zeitschriftenartikel veröffentlicht am 27. Mai 2026 in "
            "<i>Journal of Medicinal Chemistry</i>",
        ),
        # the romance languages name what the work came out in next to the
        # type, which is where their sentence has room for it
        (
            "es",
            "Artículo de revista en <i>Journal of Medicinal Chemistry</i>, "
            "fecha de publicación: 27 de mayo de 2026",
        ),
        (
            "fr",
            "Article de revue dans <i>Journal of Medicinal Chemistry</i>, "
            "date de publication : 27 mai 2026",
        ),
    ],
)
def test_to_pdf_published_in_a_container(language, expected):
    """What the record is, when it came out, and what it came out in.

    https://doi.org/10.1021/acs.jmedchem.6c00463, as each language writes it.
    """
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_published

    sample = sample_metadata(None)
    sample.type = "JournalArticle"
    sample.date_published = "2026-05-27"
    sample.container = {
        "title": "Journal of Medicinal Chemistry",
        "identifiers": [{"identifier": "0022-2623", "identifier_type": "ISSN"}],
    }

    assert to_pdf_published(sample, language) == expected


def test_to_pdf_byline_holds_a_name_together():
    """A byline breaks between names, never inside one.

    https://rogue-scholar.org/records/xvy4r-fzn40 has six authors and a byline
    that runs to a second line; it broke "Nees Jan van Eck" across it.
    """
    from commonmeta.io_utils import to_pdf_byline

    byline = to_pdf_byline(
        [
            {"name": "Najko Jahn", "orcid": None},
            {"name": "Nees Jan van Eck", "orcid": "0000-0001-8448-4521"},
        ]
    )

    assert "<span>Najko Jahn</span>" in byline
    assert "<span>Nees Jan van Eck</span>" in byline
    # the comma between two names is where it breaks instead
    assert "</a>" not in byline.split("</span>, ")[0]


def test_to_pdf_metadata_keeps_the_ordinary_spaces_in_a_name():
    """The no-break spaces are how a name is set, not how it is written: what
    a reader's viewer shows as the author is the name itself."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_authors, to_pdf_metadata

    sample = sample_metadata(None)
    sample.contributors = [
        {
            "roles": ["Author"],
            "person": {"given_name": "Nees Jan", "family_name": "van Eck"},
        }
    ]

    head = "".join(to_pdf_metadata(sample, to_pdf_authors(sample)))

    assert '<meta name="author" content="Nees Jan van Eck">' in head


def test_to_pdf_running_matter():
    """What every page after the title page carries: what the work came out
    in and what it is called, and its address as a link in the foot."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_running_matter

    sample = sample_metadata(None, title="Ten simple rules for scholarly blogging")
    sample.container = {"title": "Upstream"}

    assert to_pdf_running_matter(sample) == (
        '<div class="running-head"><b>Upstream</b> • Ten simple rules for '
        'scholarly blogging</div><div class="running-foot">'
        '<a href="https://doi.org/10.53731/kdqkf-nf052">'
        "https://doi.org/10.53731/kdqkf-nf052</a></div>"
    )


def test_to_pdf_running_matter_of_a_work_that_came_out_in_nothing():
    """The head is the title alone, without a separator in front of it."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_running_matter

    sample = sample_metadata(None, title="A record with no container")

    assert (
        '<div class="running-head">A record with no container</div>'
        in to_pdf_running_matter(sample)
    )


@pytest.mark.vcr("test_pdf_rendition_of_a_post_read_from_inveniordm.yaml")
def test_to_pdf_citation():
    """How to cite the work, in apa and in the language of the rendition."""
    from commonmeta import Metadata
    from commonmeta.io_utils import to_pdf_citation

    subject = Metadata(
        "https://rogue-scholar.org/api/records/e1ndf-19s62", via="inveniordm"
    )

    assert to_pdf_citation(subject, "en") == (
        "Ochsner, C., Pampel, H., &amp; Fenner, M. (2026, July 28). Ten simple "
        "rules for scholarly blogging. <i>Upstream</i>. "
        "https://doi.org/10.54900/xn57k-gyw73"
    )
    # the same record cited in another language, in that language's locale
    # (citeproc-py orders the date parts the way the style says, so what the
    # locale changes here is the name of the month)
    assert "(2026, Juli 28)" in to_pdf_citation(subject, "de")


def test_to_pdf_citation_of_a_record_that_cannot_be_cited():
    """A record the citation processor cannot cite gets no such section."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_citation, to_pdf_html

    sample = sample_metadata("<p>Body</p>")
    sample.write = lambda **kwargs: b"Error: citation not available for style apa."

    assert to_pdf_citation(sample, "en") is None
    assert "recommended-citation" not in to_pdf_html(sample)


def test_the_pdf_carries_its_doi_where_a_viewer_shows_it(render_pdf):
    """The doi is in the info dictionary as well as in the xmp packet.

    A viewer's document properties, and `pdfinfo`, read the first and never
    look at the second; PDF/A asks the entries it defines to agree with their
    xmp counterparts, and /doi is not one of those.
    """
    import pikepdf
    from conftest import sample_metadata

    pdf = render_pdf(sample_metadata("<p>Body</p>"))

    with pikepdf.open(io.BytesIO(pdf)) as document:
        assert str(document.docinfo["/DOI"]) == "https://doi.org/10.53731/kdqkf-nf052"
        # and in the xmp packet twice over: as the url dc:identifier holds,
        # and as the bare doi the tools that read a pdf for one look for
        xmp = document.open_metadata()
        assert xmp["prism:doi"] == "10.53731/kdqkf-nf052"
        # which a pdf may only carry once it says what a prism property is
        assert "<pdfaSchema:prefix>prism</pdfaSchema:prefix>" in str(xmp)
    assert read_pdf_metadata(pdf)["id"] == "https://doi.org/10.53731/kdqkf-nf052"


def test_the_pdf_of_a_record_without_a_doi_says_nothing_about_one(render_pdf):
    """A record with no id gets no such entry, rather than an empty one."""
    import pikepdf
    from conftest import sample_metadata

    sample = sample_metadata("<p>Body</p>")
    sample.id = None

    pdf = render_pdf(sample)

    with pikepdf.open(io.BytesIO(pdf)) as document:
        assert "/DOI" not in document.docinfo
        xmp = document.open_metadata()
        assert "prism:doi" not in xmp
        # and no schema description for a property it does not carry
        assert "pdfaSchema" not in str(xmp)


def test_to_pdf_feature_alt_reads_the_post_for_a_caption():
    """The record carries the feature image as a url and nothing else.

    Half the posts show the same image again in the text, and a fair few of
    those show it over a caption - which describes the image on the title page
    as well as it describes the one in the post.
    """
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_feature_alt

    sample = sample_metadata(
        '<p>Body</p><figure><img src="https://example.org/cover.png">'
        "<figcaption>Scrabble tiles spelling BLOG POST</figcaption></figure>"
    )
    sample.image = "https://example.org/cover.png"

    assert to_pdf_feature_alt(sample, "en") == "Scrabble tiles spelling BLOG POST"


def test_to_pdf_feature_alt_says_what_the_image_is_when_the_post_says_nothing(
    feature_image,
):
    """A reader is told what the image is rather than nothing at all."""
    from conftest import sample_metadata

    from commonmeta.io_utils import to_pdf_feature_alt, to_pdf_html

    sample = sample_metadata("<p>Body with no images at all</p>")
    sample.image = "https://example.org/cover.png"

    assert to_pdf_feature_alt(sample, "en") == "Feature image"
    # in the language of the post, as every other label on the page is
    assert to_pdf_feature_alt(sample, "de") == "Beitragsbild"
    # a post that shows the image without describing it says nothing either
    sample.content = '<p><img src="https://example.org/cover.png"></p>'
    assert to_pdf_feature_alt(sample, "en") == "Feature image"

    sample.language = "de"
    assert 'alt="Beitragsbild"' in to_pdf_html(sample)
