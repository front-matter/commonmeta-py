"""File utils module for commonmeta-py"""

import gzip
import io
import zipfile
from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm


def read_file(filename: str) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


def uncompress_content(input_bytes: bytes) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(input_bytes)) as gz:
        return gz.read()


def unzip_content(input_bytes: bytes, filename: Optional[str] = None) -> bytes:
    output = b""
    with zipfile.ZipFile(io.BytesIO(input_bytes)) as zf:
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


def download_file(url: str, progress: bool = False) -> bytes:
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    if not progress:
        return resp.content
    # Progress bar
    total = int(resp.headers.get("content-length", 0))

    buf = io.BytesIO()
    with tqdm(total=total, unit="B", unit_scale=True, desc="downloading") as bar:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                buf.write(chunk)
                bar.update(len(chunk))
    return buf.getvalue()


def write_file(filename: str, output: bytes) -> None:
    file_path = Path(filename).expanduser().resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(output)


def write_gz_file(filename: str, output: bytes) -> None:
    file_path = Path(filename).expanduser().resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    gz_path = file_path.with_suffix(file_path.suffix + ".gz")
    with gzip.open(gz_path, "wb") as gzfile:
        gzfile.write(output)


def write_zip_file(filename: str, output: bytes) -> None:
    file_path = Path(filename).expanduser().resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    zip_path = file_path.with_suffix(file_path.suffix + ".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(file_path.name, output)


def get_extension(filename: str, ext: str = "") -> tuple[str, str, str]:
    extension = ""
    compress = ""
    if filename:
        extension = Path(filename).suffix
        if extension == ".gz":
            compress = "gz"
            filename = filename[:-3]
            extension = Path(filename).suffix
        elif extension == ".zip":
            compress = "zip"
            filename = filename[:-4]
            extension = Path(filename).suffix
        else:
            compress = ""
        return filename, extension, compress
    if not ext:
        ext = ".json"
    extension = ext
    compress = ""
    return filename, extension, compress
