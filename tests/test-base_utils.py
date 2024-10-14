# pylint: disable=invalid-name
"""Test base utils"""
import pytest  # noqa: F401
from os import path
import pydash as py_

from commonmeta.base_utils import (
    parse_attributes,
    presence,
    compact,
    wrap,
    unwrap,
    sanitize,
    parse_xml,
)


def test_wrap():
    "wrap"
    # None
    assert [] == wrap(None)
    # dict
    assert [{"name": "test"}] == wrap({"name": "test"})
    # list
    assert [{"name": "test"}] == wrap([{"name": "test"}])


def test_unwrap():
    "unwrap"
    # None
    assert None is unwrap([])
    # dict
    assert {"name": "test"} == unwrap([{"name": "test"}])
    # list
    assert [{"name": "test"}, {"name": "test2"}] == unwrap(
        [{"name": "test"}, {"name": "test2"}]
    )


def test_presence():
    "presence"
    assert None is presence("")
    assert None is presence([])
    assert None is presence({})
    assert None is presence([{}])
    assert "test" == presence("test")
    assert [1] == presence([1])
    assert {"test": 1} == presence({"test": 1})


def test_compact():
    "compact"
    assert {"name": "test"} == compact({"name": "test", "other": None})
    assert None is compact(None)


def test_parse_attributes():
    "parse_attributes"
    # string
    assert "10.5061/DRYAD.8515" == parse_attributes("10.5061/DRYAD.8515")
    # dict
    assert "10.5061/DRYAD.8515" == parse_attributes({"#text": "10.5061/DRYAD.8515"})
    # dict with other keys
    assert "10.5061/DRYAD.8515" == parse_attributes(
        {"name": "10.5061/DRYAD.8515"}, content="name"
    )
    # list of dicts
    assert ["10.5061/DRYAD.8515", "10.5061/DRYAD.8516"] == parse_attributes(
        [{"#text": "10.5061/DRYAD.8515"}, {"#text": "10.5061/DRYAD.8516"}]
    )
    # first in list of dicts
    assert "10.5061/DRYAD.8515" == parse_attributes(
        [{"#text": "10.5061/DRYAD.8515"}, {"#text": "10.5061/DRYAD.8516"}], first=True
    )
    # list of strings
    assert ["10.5061/DRYAD.8515", "10.5061/DRYAD.8516"] == parse_attributes(
        ["10.5061/DRYAD.8515", "10.5061/DRYAD.8516"]
    )
    # list of empty strings
    assert None == parse_attributes([""])
    # None
    assert None is parse_attributes(None)


def test_sanitize():
    """Sanitize HTML"""
    text = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    content = "In 1998 <strong>Tim Berners-Lee</strong> coined the term cool URIs"
    assert content == sanitize(text)

    text = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    content = 'In 1998 Tim Berners-Lee coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    assert content == sanitize(text, tags={"a"})


def test_parse_xml():
    "parse XML"
    string = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    data = parse_xml(string)
    assert (
        py_.get(data, "crossref_result.xmlns") == "http://www.crossref.org/qrschema/3.0"
    )


def test_parse_xml_crossref():
    "parse Crossref XML"
    string = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    data = parse_xml(string, dialect="crossref")
    assert (
        py_.get(
            data,
            "crossref_result.query_result.body.query.doi_record.crossref.journal.journal_article.doi_data.doi",
        )
        == "10.7554/eLife.01567"
    )
