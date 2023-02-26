# pylint: disable=invalid-name
"""Commonmeta writer tests"""
import json
import pytest

from commonmeta import Metadata


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    commonmeta = json.loads(subject.commonmeta())

    assert commonmeta["id"] == "https://doi.org/10.7554/elife.01567"
    assert commonmeta["doi"] == "10.7554/elife.01567"
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
        "doi": "https://doi.org/10.1038/nature02100",
        "creator": "Bonke",
        "title": "APL regulates vascular tissue identity in Arabidopsis",
        "publicationYear": "2003",
        "volume": "426",
        "firstPage": "181",
        "containerTitle": "Nature",
    }
    assert commonmeta["rights"] == [
        {
            "rights": "Creative Commons Attribution 3.0 Unported",
            "rightsIdentifier": "cc-by-3.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/3.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]
    assert commonmeta["agency"] == "Crossref"


def test_journal_article_crossref_xml():
    "journal article crossref_xml"
    subject = Metadata("10.7554/elife.01567", via="crossref_xml")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    commonmeta = json.loads(subject.commonmeta())

    assert commonmeta["id"] == "https://doi.org/10.7554/elife.01567"
    assert commonmeta["doi"] == "10.7554/elife.01567"
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
        "doi": "https://doi.org/10.1038/nature02100",
        "creator": "Bonke",
        "title": "APL regulates vascular tissue identity in Arabidopsis",
        "publicationYear": "2003",
        "volume": "426",
        "firstPage": "181",
        "containerTitle": "Nature",
    }
    assert commonmeta["rights"] == [
        {
            "rights": "Creative Commons Attribution 3.0 Unported",
            "rightsIdentifier": "cc-by-3.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/3.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]
    assert commonmeta["agency"] == "Crossref"
