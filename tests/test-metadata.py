"""Metadata tests"""
import pytest
from commonmeta import Metadata, MetadataList


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
    with pytest.raises(ValueError):
        Metadata(string)


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
