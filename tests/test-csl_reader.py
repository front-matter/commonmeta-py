# pylint: disable=invalid-name
"""Citeproc JSON reader tests"""

import json
from os import path

from commonmeta import Metadata
from commonmeta.schema_utils import json_schema_errors


def test_blog_posting():
    "blog posting"
    string = path.join(path.dirname(__file__), "fixtures", "citeproc.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5438/4k3m-nyvg"
    assert subject.type == "BlogPost"
    assert subject.url == "https://blog.datacite.org/eating-your-own-dog-food"
    assert subject.contributors == [
        {
            "type": "Person",
            "person": {"given_name": "Martin", "family_name": "Fenner"},
            "roles": ["Author"],
        }
    ]
    assert subject.title == "Eating your own Dog Food"
    assert subject.description.startswith("Eating your own dog food")
    assert subject.license is None
    assert subject.date_published == "2016-12-20"
    assert subject.provider is None

    commonmeta = json.loads(subject.write())
    assert json_schema_errors(commonmeta, "commonmeta") is None
    assert commonmeta["title"] == "Eating your own Dog Food"
    assert commonmeta["date_published"] == "2016-12-20"
    assert commonmeta["contributors"] == [
        {
            "type": "Person",
            "person": {"given_name": "Martin", "family_name": "Fenner"},
            "roles": ["Author"],
        }
    ]


def test_no_categories():
    """no categories"""
    string = path.join(
        path.dirname(__file__), "fixtures", "citeproc-no-categories.json"
    )
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5072/4k3m-nyvg"
    assert subject.type == "BlogPost"
    assert subject.url == "https://blog.datacite.org/eating-your-own-dog-food"
    assert subject.contributors == [
        {
            "type": "Person",
            "person": {"given_name": "Martin", "family_name": "Fenner"},
            "roles": ["Author"],
        }
    ]
    assert subject.title == "Eating your own Dog Food"
    assert subject.description.startswith("Eating your own dog food")
    assert subject.date_published == "2016-12-20"
    assert subject.provider is None


def test_no_author():
    """no author"""
    string = path.join(path.dirname(__file__), "fixtures", "citeproc-no-author.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5438/4k3m-nyvg"
    assert subject.type == "BlogPost"
    assert subject.url == "https://blog.datacite.org/eating-your-own-dog-food"
    assert subject.contributors is None
    assert subject.title == "Eating your own Dog Food"
    assert subject.description.startswith("Eating your own dog food")
    assert subject.date_published == "2016-12-20"
    assert subject.provider is None
