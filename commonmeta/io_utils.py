"""File utils module for commonmeta-py"""

from __future__ import annotations

import gzip
import io
import zipfile
from pathlib import Path

import requests
import zstandard


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
    """Write output to file with supported extension"""

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
