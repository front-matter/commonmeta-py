"""Metadata tests"""

import pytest

from commonmeta import Metadata, MetadataList
from commonmeta.backend import backend_available, require_backend


@pytest.mark.vcr
def test_crossref_doi():
    """crossref doi"""
    string = "10.7554/elife.01567"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"


@pytest.mark.vcr
def test_crossref_doi_as_url():
    """crossref doi as url"""
    string = "https://doi.org/10.7554/elife.01567"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"


# @pytest.mark.vcr
# def test_doi_prefix():
#     """doi prefix"""
#     string = "10.7554"
#     with pytest.raises(ValueError):
#         Metadata(string)


@pytest.mark.vcr
def test_random_string():
    """random string"""
    string = "abc"
    subject = Metadata(string)
    assert subject.id is None


@pytest.mark.vcr
def test_list_of_pids():
    """list of pids"""
    dct = {
        "title": "The title",
        "items": [
            "10.7554/elife.01567",
            "10.1017/9781108348843",
            "10.1145/3448016.3452841",
        ],
    }
    subject_lst = MetadataList(dct, via="crossref")
    assert subject_lst.title == "The title"
    assert len(subject_lst.items) == 3
    subject = subject_lst.items[0]
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"


@pytest.mark.skipif(
    not backend_available(),
    reason="requires the optional Rust backend (commonmeta-py[backend], Python 3.14+)",
)
def test_write_parquet_roundtrip():
    """write list as parquet, then read it back via the Rust backend"""
    dct = {
        "items": [
            {
                "id": "https://doi.org/10.5555/12345678",
                "type": "JournalArticle",
                "titles": [{"title": "A Title"}],
            }
        ]
    }
    subject_lst = MetadataList(dct, via="commonmeta")
    output = subject_lst.write(to="parquet")
    assert isinstance(output, bytes)
    records = require_backend().read_parquet(output)
    assert len(records) == 1
    assert records[0]["id"] == "https://doi.org/10.5555/12345678"


@pytest.mark.skip(
    reason="write(to='zip') needs a backend binding that returns a compressed "
    "archive as bytes; commonmeta-rs only writes zip/tgz to a file path so far "
    "(Python-side compression is intentionally avoided)"
)
def test_write_zip_archive():
    """write list as a zip archive of commonmeta JSON batches"""
    import zipfile
    from io import BytesIO

    dct = {
        "items": [
            {"id": "https://doi.org/10.5555/12345678", "type": "JournalArticle"},
        ]
    }
    subject_lst = MetadataList(dct, via="commonmeta")
    output = subject_lst.write(to="zip", base_name="out.json")
    assert isinstance(output, bytes)
    with zipfile.ZipFile(BytesIO(output)) as zf:
        assert zf.namelist() == ["out.json"]
        assert b"10.5555/12345678" in zf.read("out.json")
