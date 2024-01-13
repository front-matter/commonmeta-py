# pylint: disable=invalid-name
"""Citeproc JSON reader tests"""
from os import path
import pytest
from commonmeta import Metadata


def test_default():
    "default"
    string = path.join(path.dirname(__file__), "fixtures", "commonmeta.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.schema_version == "https://commonmeta.org/commonmeta_v0.10.5.json"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://elifesciences.org/articles/01567"
    assert subject.titles[0] == {
        "title": "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    }
    assert len(subject.contributors) == 5
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martial",
        "familyName": "Sankar",
        "affiliation": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
            }
        ],
    }
    assert subject.license == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }

    assert subject.date == {
        "published": "2014-02-11",
        "updated": "2022-03-26",
    }
    assert subject.publisher == {
        "id": "https://api.crossref.org/members/4374",
        "name": "eLife Sciences Publications, Ltd",
    }
    assert len(subject.references) == 27
    assert subject.references[0] == {
        "key": "bib1",
        "doi": "https://doi.org/10.1038/nature02100",
        "contributor": "Bonke",
        "title": "APL regulates vascular tissue identity in Arabidopsis",
        "publicationYear": "2003",
        "volume": "426",
        "firstPage": "181",
        "containerTitle": "Nature",
    }
    assert subject.funding_references == [
        {"funderName": "SystemsX"},
        {"funderName": "EMBO longterm post-doctoral fellowships"},
        {"funderName": "Marie Heim-Voegtlin"},
        {
            "funderName": "University of Lausanne",
            "funderIdentifier": "https://doi.org/10.13039/501100006390",
            "funderIdentifierType": "Crossref Funder ID",
        },
        {"funderName": "SystemsX"},
        {
            "funderIdentifier": "https://doi.org/10.13039/501100003043",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "EMBO",
        },
        {
            "funderIdentifier": "https://doi.org/10.13039/501100001711",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "Swiss National Science Foundation",
        },
        {
            "funderIdentifier": "https://doi.org/10.13039/501100006390",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "University of Lausanne",
        },
    ]
    assert subject.container == {
        "identifier": "2050-084X",
        "identifierType": "ISSN",
        "title": "eLife",
        "type": "Journal",
        "volume": "3",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Among various advantages, their small size makes")
    )
    assert subject.subjects == []
    assert subject.language is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "https://cdn.elifesciences.org/articles/01567/elife-01567-v1.pdf",
        "mimeType": "application/pdf",
    }
    