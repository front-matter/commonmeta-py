# pylint: disable=invalid-name
"""Commonmeta writer tests"""
from os import path
import re
import orjson as json
import pytest

from commonmeta import Metadata, MetadataList


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    commonmeta = json.loads(subject.write())
    assert commonmeta["id"] == "https://doi.org/10.7554/elife.01567"
    assert commonmeta["url"] == "https://elifesciences.org/articles/01567"
    assert commonmeta["type"] == "JournalArticle"
    assert commonmeta["titles"] == [
        {
            "title": "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
        }
    ]
    assert len(commonmeta["references"]) == 27
    assert commonmeta["references"][0] == {
        "key": "bib1",
        "id": "https://doi.org/10.1038/nature02100",
        "contributor": "Bonke",
        "title": "APL regulates vascular tissue identity in Arabidopsis",
        "publicationYear": "2003",
        "volume": "426",
        "firstPage": "181",
        "containerTitle": "Nature",
    }
    assert commonmeta["license"] == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }
    assert commonmeta["provider"] == "Crossref"


def test_journal_article_crossref_xml():
    "journal article crossref_xml"
    subject = Metadata("10.7554/elife.01567", via="crossref_xml")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    commonmeta = json.loads(subject.write())

    assert commonmeta["id"] == "https://doi.org/10.7554/elife.01567"
    assert commonmeta["url"] == "https://elifesciences.org/articles/01567"
    assert commonmeta["type"] == "JournalArticle"
    assert commonmeta["titles"] == [
        {
            "title": "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
        }
    ]
    assert len(commonmeta["references"]) == 27
    assert commonmeta["references"][0] == {
        "key": "bib1",
        "id": "https://doi.org/10.1038/nature02100",
        "contributor": "Bonke",
        "title": "APL regulates vascular tissue identity in Arabidopsis",
        "publicationYear": "2003",
        "volume": "426",
        "firstPage": "181",
        "containerTitle": "Nature",
    }
    assert commonmeta["license"] == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }
    assert commonmeta["provider"] == "Crossref"


def test_datacite_schema_45():
    """datacite schema 4.5"""
    string = path.join(path.dirname(__file__), "fixtures", "datacite-dataset_v4.5.json")
    subject = Metadata(string)
    print(subject.errors)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.82433/b09z-4k37"

    commonmeta = json.loads(subject.write())
    assert commonmeta["id"] == "https://doi.org/10.82433/b09z-4k37"
    assert commonmeta["url"] == "https://example.com"
    assert commonmeta["type"] == "Dataset"
    assert commonmeta["titles"] == [
        {"title": "Example Title", "language": "en"},
        {"title": "Example Subtitle", "type": "Subtitle", "language": "en"},
        {
            "title": "Example TranslatedTitle",
            "type": "TranslatedTitle",
            "language": "fr",
        },
        {
            "title": "Example AlternativeTitle",
            "type": "AlternativeTitle",
            "language": "en",
        },
    ]
    assert commonmeta["descriptions"] == [
        {"description": "Example Abstract", "type": "Abstract", "language": "en"},
        {"description": "Example Methods", "type": "Methods", "language": "en"},
        {"description": "Example SeriesInformation", "type": "Other", "language": "en"},
        {"description": "Example TableOfContents", "type": "Other", "language": "en"},
        {
            "description": "Example TechnicalInfo",
            "type": "TechnicalInfo",
            "language": "en",
        },
        {"description": "Example Other", "type": "Other", "language": "en"},
    ]
    assert commonmeta["license"] == {
        "id": "CC-PDDC",
        "url": "https://creativecommons.org/licenses/publicdomain/",
    }
    assert commonmeta["provider"] == "DataCite"


@pytest.mark.vcr
def test_write_commonmeta_list():
    """write_commonmeta_list"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref-list.json")
    subject_list = MetadataList(string)
    assert len(subject_list.items) == 20
    commonmeta_list = json.loads(subject_list.write())
    assert len(commonmeta_list["items"]) == 20
    commonmeta = commonmeta_list["items"][0]
    assert (
        commonmeta["id"]
        == "https://doi.org/10.1306/703c7c64-1707-11d7-8645000102c1865d"
    )
    assert commonmeta["type"] == "JournalArticle"
    assert commonmeta["titles"] == [
        {"title": "Hydrocarbon Potential of Columbia Plateau--an Overview: ABSTRACT"}
    ]


@pytest.mark.vcr
def test_write_commonmeta_list_json_feed():
    """write_commonmeta_list json feed"""
    string = path.join(path.dirname(__file__), "fixtures", "json_feed.json")
    subject_list = MetadataList(string)
    assert len(subject_list.items) == 15
    commonmeta_list = json.loads(subject_list.write())
    assert len(commonmeta_list["items"]) == 15
    commonmeta = commonmeta_list["items"][0]
    assert commonmeta["id"] == "https://doi.org/10.59350/26ft6-dmv65"
    assert commonmeta["type"] == "Article"
    assert commonmeta["titles"] == [
        {
            "title": "Das BUA Open Science Dashboard Projekt: die Entwicklung disziplinspezifischer Open-Science-Indikatoren"
        }
    ]


def test_write_commonmeta_missing_doi():
    """Write commonmeta missing doi"""
    string = path.join(path.dirname(__file__), "fixtures", "json_feed_item_no_id.json")
    subject = Metadata(string, via="json_feed_item")
    assert subject.is_valid
    assert re.match(r"\A(https://doi\.org/10\.59350/.+)\Z", subject.id)
    commonmeta = json.loads(subject.write())
    assert re.match(r"\A(https://doi\.org/10\.59350/.+)\Z", commonmeta["id"])
    assert commonmeta["url"] == "https://www.ideasurg.pub/residency-visual-abstract"
    assert commonmeta["type"] == "Article"


def test_write_commonmeta_missing_doi_no_prefix():
    """Write commonmeta missing doi no prefix"""
    string = path.join(
        path.dirname(__file__), "fixtures", "json_feed_item_no_prefix.json"
    )
    subject = Metadata(string, via="json_feed_item")
    assert subject.is_valid
    assert subject.id == "https://www.ideasurg.pub/residency-visual-abstract"
    commonmeta = json.loads(subject.write())
    assert commonmeta["id"] == "https://www.ideasurg.pub/residency-visual-abstract"
    assert commonmeta["url"] == "https://www.ideasurg.pub/residency-visual-abstract"
    assert commonmeta["type"] == "Article"


def test_write_commonmeta_missing_doi_prefix():
    """Write commonmeta missing doi prefix"""
    string = path.join(
        path.dirname(__file__), "fixtures", "json_feed_item_no_prefix.json"
    )
    subject = Metadata(string, via="json_feed_item", prefix="10.5555")
    assert subject.is_valid
    assert re.match(r"\A(https://doi\.org/10\.5555/.+)\Z", subject.id)
    commonmeta = json.loads(subject.write())
    assert re.match(r"\A(https://doi\.org/10\.5555/.+)\Z", commonmeta["id"])
    assert commonmeta["url"] == "https://www.ideasurg.pub/residency-visual-abstract"
    assert commonmeta["type"] == "Article"
