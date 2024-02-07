# pylint: disable=invalid-name
"""Citeproc JSON reader tests"""
from os import path
from commonmeta import Metadata


def test_blog_posting():
    "blog posting"
    string = path.join(path.dirname(__file__), "fixtures", "citeproc.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5438/4k3m-nyvg"
    assert subject.type == "Article"
    assert subject.url == "https://blog.datacite.org/eating-your-own-dog-food"
    assert subject.contributors == [
        {
            "familyName": "Fenner",
            "givenName": "Martin",
            "type": "Person",
            "contributorRoles": ["Author"],
        }
    ]
    assert subject.titles == [{"title": "Eating your own Dog Food"}]
    assert subject.descriptions[0]["description"].startswith("Eating your own dog food")
    assert subject.license is None
    assert subject.date == {"published": "2016-12-20"}
    assert subject.provider == "DataCite"


def test_no_categories():
    """no categories"""
    string = path.join(
        path.dirname(__file__), "fixtures", "citeproc-no-categories.json"
    )
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5072/4k3m-nyvg"
    assert subject.type == "Article"
    assert subject.url == "https://blog.datacite.org/eating-your-own-dog-food"
    assert subject.contributors == [
        {
            "familyName": "Fenner",
            "givenName": "Martin",
            "type": "Person",
            "contributorRoles": ["Author"],
        }
    ]
    assert subject.titles == [{"title": "Eating your own Dog Food"}]
    assert subject.descriptions[0]["description"].startswith("Eating your own dog food")
    assert subject.date == {"published": "2016-12-20"}
    assert subject.provider == "DataCite"


def test_no_author():
    """no author"""
    string = path.join(path.dirname(__file__), "fixtures", "citeproc-no-author.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5438/4k3m-nyvg"
    assert subject.type == "Article"
    assert subject.url == "https://blog.datacite.org/eating-your-own-dog-food"
    assert subject.contributors is None
    assert subject.titles == [{"title": "Eating your own Dog Food"}]
    assert subject.descriptions[0]["description"].startswith("Eating your own dog food")
    assert subject.date == {"published": "2016-12-20"}
    assert subject.provider == "DataCite"
