# pylint: disable=invalid-name
"""Test file_utils"""

from os import path, remove

import pytest  # noqa: F401

from commonmeta.file_utils import (
    download_file,
    get_extension,
    read_file,
    read_gz_file,
    read_zip_file,
    uncompress_content,
    unzip_content,
    write_file,
    write_gz_file,
    write_output,
    write_zip_file,
)


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
    assert len(download_file(url, progress=True)) == 18820287


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
