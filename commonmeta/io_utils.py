"""File utils module for commonmeta-py.

Reading and writing files, including compression and PDF.
"""

from __future__ import annotations

import atexit
import gzip
import io
import logging
import zipfile
from base64 import b64encode
from datetime import date as date_type
from datetime import datetime
from functools import lru_cache
from html import escape, unescape
from pathlib import Path
from typing import TYPE_CHECKING

import nh3
import requests
import zstandard
from babel.core import UnknownLocaleError
from babel.dates import format_date
from bs4 import BeautifulSoup

from .api_utils import http
from .base_utils import dig, presence, unique, wrap
from .date_utils import get_iso8601_date
from .doi_utils import doi_from_url
from .utils import get_language, validate_orcid

if TYPE_CHECKING:
    from .metadata import Metadata

log = logging.getLogger(__name__)


def read_file(filename: str) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


def uncompress_content(input: bytes) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(input)) as gz:
        return gz.read()


def unzip_content(input: bytes, filename: str | None = None) -> bytes:
    output = b""
    with zipfile.ZipFile(io.BytesIO(input)) as zf:
        for info in zf.infolist():
            if filename and info.filename != filename:
                continue
            with zf.open(info) as file:
                output += file.read()
    return output


def read_gz_file(filename: str) -> bytes:
    input_bytes = read_file(filename)
    return uncompress_content(input_bytes)


def read_zip_file(filename: str, name: str | None = None) -> bytes:
    input_bytes = read_file(filename)
    return unzip_content(input_bytes, name)


def download_file(url: str) -> bytes:
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    return resp.content


def write_file(filename: str, output: bytes) -> None:
    with open(filename, "xb") as f:
        f.write(output)


def write_gz_file(filename: str, output: bytes) -> None:
    with gzip.open(filename, "xb") as gzfile:
        gzfile.write(output)


def write_zip_file(filename: str, output: bytes) -> None:
    path = Path(filename)
    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(path.name, output)


def write_zst_file(filename: str, output: bytes) -> None:
    compressor = zstandard.ZstdCompressor()
    with open(filename, "xb") as f:
        f.write(compressor.compress(output))


def get_extension(filename: str) -> tuple[str, str, str | None]:
    """Extract extension and compression from filename"""
    extension = Path(filename).suffix
    if extension == ".gz":
        compress = ".gz"
        filename = filename[:-3]
        extension = Path(filename).suffix
    elif extension == ".zip":
        compress = ".zip"
        filename = filename[:-4]
        extension = Path(filename).suffix
    elif extension == ".zst":
        compress = ".zst"
        filename = filename[:-4]
        extension = Path(filename).suffix
    elif extension == "":
        compress = None
        filename = filename + ".json"
        extension = ".json"
    else:
        compress = None
    return filename, extension, compress


def write_output(filename: str, input: bytes | str, ext: list[str]) -> None:
    """Write output to file with supported extension.

    Text formats arrive as a string and binary ones - a pdf rendition, a
    parquet file - as bytes; both are written as they are, so `ext` is what
    says which extensions a caller means to produce.
    """

    # Convert string to bytes if necessary
    if isinstance(input, str):
        input = input.encode("utf-8")

    filename, extension, compress = get_extension(filename)
    if extension not in ext:
        raise ValueError(
            f"File format not supported. Please provide a filename with {ext} extension."
        )
    if compress == ".gz":
        write_gz_file(filename + compress, input)
    elif compress == ".zip":
        write_zip_file(filename + compress, input)
    elif compress == ".zst":
        write_zst_file(filename + compress, input)
    else:
        write_file(filename, input)


# Stylesheet and fonts for the pdf rendition, shipped with the package.
PDF_RESOURCES = Path(__file__).parent / "resources" / "pdf"

# The PDF variant used for writing PDF files. # WeasyPrint only knows the accessible ("a") conformance levels since 67, hence
# the >=69 floor in pyproject.toml.
PDF_VARIANT = "pdf/a-3a"

# The markup a title or a description is allowed to carry into the pdf. Post
# titles are html, and an italicised species name says something an escaped
# <i> does not; anything that lays out, loads or runs is dropped.
PDF_INLINE_TAGS = {
    "a",
    "abbr",
    "b",
    "br",
    "cite",
    "code",
    "em",
    "i",
    "mark",
    "q",
    "s",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "u",
}

# Front matter headings, in the languages rogue-scholar-api translated them to.
PDF_TITLES = {
    "published": {
        "en": "Published",
        "de": "Veröffentlicht",
        "es": "Publicado",
        "fr": "Publié",
        "it": "Pubblicato",
        "pt": "Publicados",
    },
    "abstract": {
        "en": "Abstract",
        "de": "Zusammenfassung",
        "es": "Resumen",
        "fr": "Résumé",
        "it": "Riassunto",
        "pt": "Resumo",
    },
    "copyright": {
        "en": "Copyright",
        "de": "Urheberrecht",
        "es": "Copyright",
        "fr": "Droit d'auteur",
        "it": "Copyright",
        "pt": "Direitos de autor",
    },
    "keywords": {
        "en": "Keywords",
        "de": "Schlüsselwörter",
        "es": "Palabras clave",
        "fr": "Mots clés",
        "it": "Parole chiave",
        "pt": "Palavras-chave",
    },
    # the alt description an image gets when the post gives it none
    "image": {
        "en": "Image",
        "de": "Bild",
        "es": "Imagen",
        "fr": "Image",
        "it": "Immagine",
        "pt": "Imagem",
    },
}


def to_pdf_author(contributor: dict) -> str | None:
    """Format a contributor for the pdf byline, given name first"""
    person = contributor.get("person", None) or {}
    name = " ".join(
        n
        for n in (person.get("given_name", None), person.get("family_name", None))
        if n
    )
    return name or (contributor.get("organization", None) or {}).get("name", None)


def to_pdf_authors(metadata: Metadata) -> list:
    """The authors of the post, each with the orcid it has, if it has one."""
    authors = []
    for contributor in wrap(metadata.contributors):
        if "Author" not in wrap(contributor.get("roles", None)):
            continue
        name = to_pdf_author(contributor)
        if not name:
            continue
        person = contributor.get("person", None) or {}
        authors.append({"name": name, "orcid": validate_orcid(person.get("id", None))})
    return authors


def to_pdf_byline(authors: list) -> str:
    """The byline, with each name that has an orcid linking to it.

    The name carries the link and the orcid icon marks it, which is how ORCID
    asks for an iD to be shown next to a name and what the rogue-scholar-api
    template did. The icon is a file next to the stylesheet, so it resolves
    against the same base url the fonts do.
    """
    names = []
    for author in authors:
        name = f"<span>{escape(author['name'])}</span>"
        orcid = author.get("orcid", None)
        if orcid:
            url = f"https://orcid.org/{orcid}"
            name = (
                f'<a href="{url}">{name}'
                f'<img class="orcid" alt="ORCID iD" src="orcid.svg" /></a>'
            )
        names.append(name)
    return f'<p class="author">{", ".join(names)}</p>' if names else ""


def to_pdf_keywords(metadata: Metadata) -> list:
    """The tags the post gave itself, rather than every subject it was given.

    A Rogue Scholar record carries the OpenAlex subfield and the field of
    science it was classified into alongside the blog's own tags, which are
    the ones the tags of the post: the classifications are identified by a
    url, the post's own tags are not.
    """
    tags = unique(
        [
            subject.get("subject")
            for subject in wrap(metadata.subjects)
            if subject.get("subject", None) and not subject.get("id", None)
        ]
    )
    return tags or unique(
        [
            subject.get("subject")
            for subject in wrap(metadata.subjects)
            if subject.get("subject", None)
        ]
    )


def to_pdf_markup(text: str | None) -> str:
    """A title or description with the inline markup it carries.

    Post titles are html: "The atlas/axis complex of <i>Apatosaurus louisae</i>
    CM 3018" says something the same string with its tags escaped does not.
    Only inline markup survives - anything that would lay out, load or run is
    dropped rather than shown as text.
    """
    if not text:
        return ""
    return nh3.clean(text, tags=PDF_INLINE_TAGS, attributes={})


def to_pdf_text(text: str | None) -> str:
    """The same title or description as plain text, for the pdf's metadata.

    An info dictionary and an XMP packet hold text, not markup, so the tags
    come out and the entities they leave behind are resolved: what a reader's
    viewer shows as the document's title.
    """
    if not text:
        return ""
    return unescape(nh3.clean(text, tags=set()))


def to_pdf_date(date: str | None, language: str) -> str | None:
    """Format a publication date the way a reader writes it, in its language.

    Falls back to the iso date for anything babel cannot make a long date of,
    a partial date such as "2024-10" among them.
    """
    if not date:
        return None
    iso = get_iso8601_date(date)
    try:
        return format_date(date_type.fromisoformat(iso), format="long", locale=language)
    except (ValueError, TypeError, UnknownLocaleError) as error:
        log.warning(f"Cannot format date {date} for the pdf: {error}")
        return iso


def to_pdf_rights(metadata: Metadata, authors: list, language: str) -> str | None:
    """Format the copyright line and the terms the post is available under.

    Mirrors the rogue-scholar-api pdf template: a copyright holder and year for
    everything except CC0, which waives copyright rather than asserting it,
    followed by what the licence permits.
    """
    url = (metadata.license or {}).get("url", None)
    identifier = (metadata.license or {}).get("id", None)
    if not url and not identifier:
        return None

    link = f'<a href="{escape(url)}">' if url else "<span>"
    close = "</a>" if url else "</span>"
    if (identifier or "").lower().startswith("cc0"):
        return (
            "This is an open access article, free of all copyright, and may be "
            "freely reproduced, distributed, transmitted, modified, built upon, "
            "or otherwise used by anyone for any lawful purpose. The work is "
            f"made available under the {link}Creative Commons CC0 public domain "
            f"dedication{close}."
        )

    year = (get_iso8601_date(metadata.date_published) or "")[:4]
    holder = authors[0] if authors else ""
    if len(authors) > 1:
        holder += " et al."
    copyright_line = (
        f'Copyright <span class="copyright">&copy;</span> '
        f"{escape(holder)} {year}.".replace("  ", " ")
    )
    if (identifier or "").lower().startswith("cc-by-4.0"):
        return (
            f"{copyright_line} Distributed under the terms of the {link}Creative "
            f"Commons Attribution 4.0 International License{close}, which permits "
            "unrestricted use, distribution, and reproduction in any medium, "
            "provided the original author and source are credited."
        )
    return (
        f"{copyright_line} Distributed under the terms of the "
        f"{link}{escape(identifier or url)}{close} license."
    )


def to_pdf_meta_tags(metadata: Metadata, authors: list) -> list:
    """The meta tags WeasyPrint turns into the pdf's own metadata.

    Each one lands in both the info dictionary and the XMP packet that PDF/A
    requires: author as /Author and dc:creator, description as /Subject and
    dc:description, keywords as /Keywords and pdf:Keywords, the dcterms dates
    as /CreationDate and /ModDate and their xmp counterparts. `read_pdf_metadata`
    reads them back out. The doi has no slot of its own in either, so it stays
    on the title page rather than becoming a custom info key, which would put
    the pdf outside PDF/A.
    """
    tags = [
        f'<meta name="author" content="{escape(author["name"])}">' for author in authors
    ]
    description = to_pdf_text(metadata.description)
    if description:
        tags.append(f'<meta name="description" content="{escape(description)}">')
    keywords = unique(
        [
            subject.get("subject")
            for subject in wrap(metadata.subjects)
            if subject.get("subject", None)
        ]
    )
    if keywords:
        tags.append(f'<meta name="keywords" content="{escape(", ".join(keywords))}">')
    platform = (metadata.container or {}).get("platform", None)
    if platform:
        tags.append(f'<meta name="generator" content="{escape(platform)}">')
    for name, date in (
        ("dcterms.created", metadata.date_published),
        ("dcterms.modified", metadata.date_updated),
    ):
        # W3C-DTF, which is what WeasyPrint parses these as; the iso date is
        # the part of it every record has
        if date:
            tags.append(f'<meta name="{name}" content="{get_iso8601_date(date)}">')
    return tags


def to_pdf_image(metadata: Metadata) -> str | None:
    """The feature image as a data uri, None when there is none to be had.

    Fetched here rather than left to WeasyPrint so the image travels inside
    the pdf instead of an external link.
    """
    url = presence(metadata.image)
    if url is None:
        return None
    try:
        response = http.get(
            str(url), timeout=30, headers={"Accept": "image/*,*/*;q=0.8"}
        )
        response.raise_for_status()
    except Exception as error:
        # the image is decoration: no fetch of it is worth failing the render,
        # and in tests the request is the cassette's to refuse
        log.warning(f"Cannot embed the feature image {url}: {error}")
        return None

    mime_type = response.headers.get("Content-Type", "").split(";")[0].strip()
    if not mime_type.startswith("image/"):
        log.warning(f"Feature image {url} is {mime_type or 'of unknown type'}")
        return None
    return f"data:{mime_type};base64,{b64encode(response.content).decode('ascii')}"


def finish_pdf(pdf: bytes, metadata: Metadata) -> bytes:
    """Everything the rendition still needs after WeasyPrint has written it.

    The doi and the licence have no slot among the meta tags WeasyPrint
    reads, but each has a standard XMP property - dc:identifier, and dc:rights
    with the licence url as its xmpRights:WebStatement - so pikepdf writes
    them into the packet WeasyPrint produced, rather than them becoming custom
    info keys, which would put the pdf outside PDF/A. Writing them into that
    same packet, as opposed to appending a second rdf:RDF block, is what makes
    them visible to a reader that looks up properties by name.

    The images then lose their /Interpolate key, which WeasyPrint sets on
    every image it draws and PDF/A forbids (ISO 19005-3 6.2.8: present means
    false). It only ever hinted that a viewer may smooth the image when it is
    scaled up, so dropping it costs the rendition nothing and is what makes
    veraPDF pass the file.
    """
    import pikepdf

    identifier = presence(metadata.id)
    license_id = (metadata.license or {}).get("id", None)
    license_url = (metadata.license or {}).get("url", None)

    output = io.BytesIO()
    with pikepdf.open(io.BytesIO(pdf)) as document:
        # update_docinfo would copy these into the info dictionary, where a
        # pdf has no entry for either, and PDF/A wants the two kept in step.
        # set_pikepdf_as_editor would overwrite pdf:Producer, leaving it at
        # odds with the /Producer WeasyPrint wrote, and stamp the current
        # time as xmp:MetadataDate, which would make renditions of the same
        # post differ from each other.
        with document.open_metadata(
            update_docinfo=False, set_pikepdf_as_editor=False
        ) as xmp:
            if identifier:
                xmp["dc:identifier"] = identifier
            if license_id:
                xmp["dc:rights"] = license_id
            if license_url:
                xmp["xmpRights:WebStatement"] = license_url

        for obj in document.objects:
            # every object, rather than every page's images: an image can also
            # sit inside a form xobject
            if (
                isinstance(obj, pikepdf.Stream)
                and obj.get("/Subtype", None) == pikepdf.Name.Image
                and "/Interpolate" in obj
            ):
                del obj["/Interpolate"]

        # deterministic_id computes the trailer's /ID from the contents rather
        # than from the clock, which is the last thing that made two renditions
        # of the same post differ from each other
        document.save(output, deterministic_id=True)
    return output.getvalue()


def to_pdf_attachment(metadata: Metadata, weasyprint):
    """The post content, embedded in the pdf as the source it was rendered from.

    PDF/A-3 is the variant that allows an arbitrary embedded file, and
    WeasyPrint gives it the /AFRelationship the standard asks for.
    """
    created = to_pdf_datetime(metadata.date_published)
    modified = to_pdf_datetime(metadata.date_updated) or created
    return weasyprint.Attachment(
        string=metadata.content,
        name=f"{Path(pdf_filename(metadata)).stem}.html",
        description="Post content as html (rs:content_html)",
        relationship="Source",
        created=created,
        modified=modified,
    )


def to_pdf_datetime(date: str | None) -> datetime | None:
    """An iso date as the datetime WeasyPrint stamps an attachment with"""
    if not date:
        return None
    try:
        return datetime.fromisoformat(get_iso8601_date(date))
    except (ValueError, TypeError):
        return None


def to_pdf_content(content: str | None, language: str) -> str:
    """The post content, with an alt description on every image.

    A tagged pdf needs one for each image, and WeasyPrint logs an error per
    image that has none - which for a post whose images carry no alt text, as
    blog posts routinely do, is an error per image on every render. An image
    without alt borrows the caption of the figure it sits in, or its own title
    attribute, or takes a generic label in the language of the post. An empty
    alt would not do: WeasyPrint reads it as no description at all.
    """
    if not content or "<img" not in content:
        return content or ""

    soup = BeautifulSoup(content, "html.parser")
    label = PDF_TITLES["image"].get(language, PDF_TITLES["image"]["en"])
    described = False
    for image in soup.find_all("img"):
        if (image.get("alt") or "").strip():
            continue
        figure = image.find_parent("figure")
        caption = figure.find("figcaption") if figure else None
        image["alt"] = (
            (caption.get_text(" ", strip=True) if caption else "")
            or (image.get("title") or "").strip()
            or label
        )
        described = True
    return str(soup) if described else content


def to_pdf_html(metadata: Metadata) -> str:
    """Build the html document the pdf is rendered from.

    The post content is the body, preceded by the front matter that the
    stylesheet styles by class, in the order the rogue-scholar-api pdf template
    used: the title, the blog name (hidden, it only feeds the running header),
    the byline, the publication date, the doi, the description, the feature
    image and the licence. The licence carries `break-after: always`, so the
    front matter is a title page.
    """
    language = get_language(metadata.language, format="alpha_2") or "en"
    authors = to_pdf_authors(metadata)
    container = metadata.container or {}

    front_matter = [
        f"<h1>{to_pdf_markup(metadata.title)}</h1>",
        f'<span class="header">{escape(container.get("title", "") or "")}</span>',
        to_pdf_byline(authors),
    ]
    date_published = to_pdf_date(metadata.date_published, language)
    if date_published:
        label = PDF_TITLES["published"].get(language, PDF_TITLES["published"]["en"])
        front_matter.append(f'<div class="date">{label} {escape(date_published)}</div>')
    if metadata.id:
        front_matter.append(
            f'<p class="identifier"><a href="{escape(metadata.id)}">'
            f"{escape(metadata.id)}</a></p>"
        )
    if presence(metadata.description):
        label = PDF_TITLES["abstract"].get(language, PDF_TITLES["abstract"]["en"])
        # the text follows the heading directly, as in the rights block: a <p>
        # would add its own margin on top of the heading's padding
        front_matter.append(
            f'<div class="abstract"><h4>{label}</h4>'
            f"{to_pdf_markup(metadata.description)}</div>"
        )
    keywords = to_pdf_keywords(metadata)
    if keywords:
        label = PDF_TITLES["keywords"].get(language, PDF_TITLES["keywords"]["en"])
        front_matter.append(
            f'<div class="keywords"><h4>{label}</h4>{escape(", ".join(keywords))}</div>'
        )
    image = to_pdf_image(metadata)
    if image:
        front_matter.append(
            f'<img class="feature-image" alt="Feature image" src="{image}" />'
        )
    rights = to_pdf_rights(metadata, [a["name"] for a in authors], language)
    if rights:
        label = PDF_TITLES["copyright"].get(language, PDF_TITLES["copyright"]["en"])
        front_matter.append(f'<div class="rights"><h4>{label}</h4>{rights}</div>')

    head = [
        "<meta charset='utf-8'>",
        f"<title>{escape(to_pdf_text(metadata.title))}</title>",
        *to_pdf_meta_tags(metadata, authors),
    ]
    return (
        f"<html lang='{escape(language)}'><head>{''.join(head)}</head>"
        f'<body><section class="front-matter">{"".join(front_matter)}</section>'
        f"{to_pdf_content(metadata.content, language)}</body></html>"
    )


def load_weasyprint():
    """Import WeasyPrint, None when its native stack is missing.

    Imported here rather than at module level because WeasyPrint binds pango,
    cairo and glib through cffi at import time: on a machine without those
    system libraries the import raises OSError rather than ImportError, and
    only the pdf path should pay for that.
    """
    try:
        import weasyprint

        return weasyprint
    except (ImportError, OSError) as error:
        log.error(f"Cannot render pdf, weasyprint needs the pango libraries: {error}")
        return None


def pdf_filename(metadata: Metadata, record: dict | None = None) -> str:
    """Name the pdf after the doi of the record or metadata it is attached to.

    Replaces the slash in the doi with a dash, so the filename is valid on every
    filesystem. Falls back to "content.pdf" when there is no doi.
    """
    doi = doi_from_url(dig(record, "doi")) or doi_from_url(metadata.id)
    return f"{doi.replace('/', '-')}.pdf" if doi else "content.pdf"


@lru_cache(maxsize=1)
def pdf_stylesheet() -> tuple:
    """The shipped stylesheet and the font configuration it registers into.

    Parsed once per process: it reads and registers the six bundled font
    faces, which is the expensive part of rendering a post. The same font
    configuration has to reach `write_pdf`, otherwise the @font-face rules are
    dropped and the text falls back to WeasyPrint's default font.
    """
    import weasyprint
    from weasyprint.text.fonts import FontConfiguration

    font_config = FontConfiguration()
    css = weasyprint.CSS(
        filename=str(PDF_RESOURCES / "style.css"), font_config=font_config
    )
    # WeasyPrint's font configuration calls back into its own module when it is
    # finalized, which fails once the interpreter has torn those modules down.
    # Dropping the cache at exit finalizes it while that is still safe.
    atexit.register(pdf_stylesheet.cache_clear)
    return css, font_config


def write_pdf_rendition(
    metadata: Metadata, url_fetcher=None, file: str | None = None, **options
) -> bytes | None:
    """Render a record as a tagged pdf, None when it cannot be rendered at all.

    A record that carries the html of a post - which today is one read through
    the InvenioRDM reader - is rendered whole: the title page, then the post.
    Every other record has its title page and stops there, which is a record
    of the metadata rather than of the work, and is what any input can give.

    ``url_fetcher`` is handed to WeasyPrint for the images the post links, and
    any further ``options`` go to ``write_pdf`` - among them ``pdf_variant``,
    which defaults to PDF/A-3a.

    ``file`` also writes the rendition there, through `write_output`, which
    takes the compression suffixes with it: ``post.pdf.gz`` and ``post.pdf.zst``
    are written compressed. It refuses to overwrite, as every other output
    format does. The bytes are returned either way, since what a caller does
    with a rendition is usually to send it somewhere rather than keep it.
    """
    weasyprint = load_weasyprint()
    if weasyprint is None:
        return None

    css, font_config = pdf_stylesheet()
    # WeasyPrint picks its own fetcher when none is given; naming its default
    # explicitly would go through an api it deprecated in 69.
    fetcher = {"url_fetcher": url_fetcher} if url_fetcher is not None else {}
    options.setdefault("pdf_variant", PDF_VARIANT)
    # nothing to attach when there is no post to attach: the html the pdf was
    # rendered from is the only file it carries
    if presence(metadata.content):
        options.setdefault("attachments", [to_pdf_attachment(metadata, weasyprint)])
    document = weasyprint.HTML(
        string=to_pdf_html(metadata), base_url=str(PDF_RESOURCES), **fetcher
    ).render(stylesheets=[css], font_config=font_config)
    pdf = finish_pdf(document.write_pdf(**options), metadata)
    if file:
        write_output(file, pdf, [".pdf"])
    return pdf


def read_pdf_metadata(pdf: bytes) -> dict:
    """Read a rendition's own metadata back out of the pdf.

    Reads the XMP packet, which is where PDF/A keeps the metadata the
    InvenioRDM writer put there when it rendered the post, the two markers
    that say the pdf is tagged - a structure tree, and a catalog declaring it
    marked - and the names of the embedded files. Anything absent from the pdf
    is absent from the result.

    pikepdf is imported here rather than at module level: it pulls in libqpdf,
    which costs more to import than the rest of this module put together, and
    only the pdf path should pay for it.
    """
    import pikepdf

    metadata = {}
    with pikepdf.open(io.BytesIO(pdf)) as document:
        catalog = document.Root
        metadata["tagged"] = (
            bool(catalog.get("/MarkInfo", {}).get("/Marked", False))
            and "/StructTreeRoot" in catalog
        )
        if "/Lang" in catalog:
            metadata["language"] = str(catalog.Lang)
        attachments = {
            name: document.attachments[name].get_file().mime_type
            for name in document.attachments
        }
        if attachments:
            metadata["attachments"] = attachments

        xmp = document.open_metadata()
        for key, property_ in (
            ("id", "dc:identifier"),
            ("title", "dc:title"),
            ("authors", "dc:creator"),
            ("description", "dc:description"),
            ("license", "dc:rights"),
            ("license_url", "xmpRights:WebStatement"),
            ("keywords", "pdf:Keywords"),
            ("generator", "xmp:CreatorTool"),
            ("created", "xmp:CreateDate"),
            ("modified", "xmp:ModifyDate"),
            ("producer", "pdf:Producer"),
        ):
            value = xmp.get(property_, None)
            if value:
                metadata[key] = value
        # a single string of comma-separated keywords in the pdf, a list here
        if metadata.get("keywords", None):
            metadata["keywords"] = [k.strip() for k in metadata["keywords"].split(",")]
        part = xmp.get("pdfaid:part", None)
        if part:
            level = xmp.get("pdfaid:conformance", "")
            metadata["variant"] = f"PDF/A-{part}{level.lower()}"
    return metadata


def read_pdf_attachment(pdf: bytes, name: str | None = None) -> bytes | None:
    """Read an embedded file back out of the pdf, the first one by default"""
    import pikepdf

    with pikepdf.open(io.BytesIO(pdf)) as document:
        names = list(document.attachments)
        if name is None:
            name = names[0] if names else None
        if name is None or name not in names:
            return None
        return document.attachments[name].get_file().read_bytes()
