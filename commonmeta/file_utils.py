"""File utils module for commonmeta-py"""

import gzip
import io
import zipfile
from pathlib import Path
from typing import Optional, Union

import requests


def read_file(filename: str) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


def uncompress_content(input: bytes) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(input)) as gz:
        return gz.read()


def unzip_content(input: bytes, filename: Optional[str] = None) -> bytes:
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


def read_zip_file(filename: str, name: Optional[str] = None) -> bytes:
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


def get_extension(filename: str) -> tuple[str, str, Optional[str]]:
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
    elif extension == "":
        compress = None
        filename = filename + ".json"
        extension = ".json"
    else:
        compress = None
    return filename, extension, compress


def write_output(filename: str, input: Union[bytes, str], ext: list[str]) -> None:
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
    else:
        write_file(filename, input)
