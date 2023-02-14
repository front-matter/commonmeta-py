"""Citeproc JSON reader tests"""
from os import path
import pytest
from talbot import Metadata
from talbot.readers.citeproc_reader import read_citeproc

def test_blog_posting():
    "blog posting"
    data = path.join(path.dirname(__file__), 'fixtures', 'citeproc.json')
    subject = Metadata(data)
   
    assert subject.pid == 'https://doi.org/10.5438/4k3m-nyvg'
    assert subject.url == 'https://blog.datacite.org/eating-your-own-dog-food'
    assert subject.types == {'bibtex': 'article', 'citeproc': 'post-weblog', 'resourceTypeGeneral': 'Text', 'ris': 'GEN', 'schemaOrg': 'BlogPosting'}
    assert subject.creators == [{'familyName': 'Fenner', 'givenName': 'Martin', 'nameType': 'Personal'}]
    assert subject.titles == [{'title': 'Eating your own Dog Food'}]
    assert subject.descriptions[0]['description'].startswith('Eating your own dog food')
    assert subject.dates == [{'date': '2016-12-20', 'dateType': 'Issued'}]
    assert subject.publication_year == 2016

def test_no_categories():
    """no categories"""
    data = path.join(path.dirname(__file__), 'fixtures', 'citeproc-no-categories.json')
    subject = Metadata(data)
    assert subject.pid == 'https://doi.org/10.5072/4k3m-nyvg'
    assert subject.url == 'https://blog.datacite.org/eating-your-own-dog-food'
    assert subject.types == {'bibtex': 'article', 'citeproc': 'post-weblog', 'resourceTypeGeneral': 'Text', 'ris': 'GEN', 'schemaOrg': 'BlogPosting'}
    assert subject.creators == [{'familyName': 'Fenner', 'givenName': 'Martin', 'nameType': 'Personal'}]
    assert subject.titles == [{'title': 'Eating your own Dog Food'}]
    assert subject.descriptions[0]['description'].startswith('Eating your own dog food')
    assert subject.dates == [{'date': '2016-12-20', 'dateType': 'Issued'}]
    assert subject.publication_year == 2016


def test_no_author():
    """no author"""
    data = path.join(path.dirname(__file__), 'fixtures', 'citeproc-no-author.json')
    subject = Metadata(data)
    assert subject.pid == 'https://doi.org/10.5438/4k3m-nyvg'
    assert subject.url == 'https://blog.datacite.org/eating-your-own-dog-food'
    assert subject.types == {'bibtex': 'article', 'citeproc': 'post-weblog', 'resourceTypeGeneral': 'Text', 'ris': 'GEN', 'schemaOrg': 'BlogPosting'}
    assert subject.creators == [{'name': ':(unav)', 'nameType': 'Organizational'}]
    assert subject.titles == [{'title': 'Eating your own Dog Food'}]
    assert subject.descriptions[0]['description'].startswith('Eating your own dog food')
    assert subject.dates == [{'date': '2016-12-20', 'dateType': 'Issued'}]
    assert subject.publication_year == 2016
