"""Test base utils"""
import pytest

from talbot.base_utils import (
    parse_attributes, presence, compact, wrap, unwrap, camel_case, sanitize)


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
    assert "10.5061/DRYAD.8515" == parse_attributes(
        {"__content__": "10.5061/DRYAD.8515"}
    )
    # dict with other keys
    assert "10.5061/DRYAD.8515" == parse_attributes(
        {"name": "10.5061/DRYAD.8515"}, content="name")
    # list of dicts
    assert ['10.5061/DRYAD.8515', '10.5061/DRYAD.8516'] == parse_attributes(
        [{"__content__": "10.5061/DRYAD.8515"},
            {"__content__": "10.5061/DRYAD.8516"}]
    )
    # first in list of dicts
    assert '10.5061/DRYAD.8515' == parse_attributes(
        [{"__content__": "10.5061/DRYAD.8515"}, {"__content__": "10.5061/DRYAD.8516"}], first=True)
    # list of strings
    assert ['10.5061/DRYAD.8515', '10.5061/DRYAD.8516'] == parse_attributes(
        ["10.5061/DRYAD.8515", "10.5061/DRYAD.8516"])
    # None
    assert None is parse_attributes(None)


def test_camel_case():
    """camel case"""
    assert "camelCase" == camel_case("camel_case")
    assert "camelCase" == camel_case("camel-case")
    assert "" == camel_case("")
    assert None is camel_case(None)


def test_sanitize():
    """Sanitize HTML"""
    text = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    content = "In 1998 <strong>Tim Berners-Lee</strong> coined the term cool URIs"
    assert content == sanitize(text)
    assert content == sanitize({'__content__': text})
    assert content == sanitize([{'__content__': text}])
    assert content == sanitize([{'name': text}], content='name')
    assert None is sanitize([], content='name')

    text = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    content = 'In 1998 Tim Berners-Lee coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    assert content == sanitize(text, tags={"a"})
