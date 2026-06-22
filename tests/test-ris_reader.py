# pylint: disable=invalid-name
"""RIS reader tests"""

import json
from os import path

from commonmeta import Metadata
from commonmeta.schema_utils import json_schema_errors


def test_journal_article():
    "journal article"
    string = path.join(path.dirname(__file__), "fixtures", "crossref.ris")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"
    assert subject.url == "http://elifesciences.org/lookup/doi/10.7554/eLife.01567"
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Martial",
            "family_name": "Sankar"
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.title == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    assert subject.publisher is None
    assert (
        subject.description
        .startswith("Among various advantages,")
    )
    assert subject.license is None
    assert subject.container == {
        "type": "Journal",
        "title": "eLife",
        "volume": "3",
    }
    assert subject.date_published == "2014"

    commonmeta = json.loads(subject.write())
    assert json_schema_errors(commonmeta, "commonmeta") is None
    assert (
        commonmeta["title"]
        == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert commonmeta["date_published"] == "2014"
    assert commonmeta["contributors"][0] == {
        "type": "Person",
        "person": {"given_name": "Martial", "family_name": "Sankar"},
        "roles": ["Author"],
    }


def test_thesis():
    "Thesis, DOI does not exist"
    string = path.join(path.dirname(__file__), "fixtures", "pure.ris")
    subject = Metadata(string)
    assert subject.is_valid is False
    assert subject.errors is None
    assert subject.id is None
    assert subject.type == "Dissertation"
    assert subject.url is None
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Y.",
            "family_name": "Toparlar"
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.title == "A multiscale analysis of the urban heat island effect"
    assert (
        subject.description
        .startswith("Designing the climates of cities")
    )
    assert subject.license is None
    assert subject.container == {
        "title": "from city averaged temperatures to the energy demand of individual buildings"
    }
    assert subject.date_published == "2018-04-25"
    assert subject.dates == {"created": "2018-04-25"}
