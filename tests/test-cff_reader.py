"""Test cff reader"""
from os import path
import pytest
from commonmeta import Metadata


@pytest.mark.vcr
def test_ruby_cff():
    """ruby-cff"""
    string = 'https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff'
    subject = Metadata(string)

    assert subject.id == 'https://doi.org/10.5281/zenodo.1184077'
    assert subject.url == 'https://github.com/citation-file-format/ruby-cff'
    assert subject.type == "Software"
    assert subject.creators == [
        {'affiliation': [{'name': 'The University of Manchester, UK'}],
         'familyName': 'Haines',
         'givenName': 'Robert',
         'id': 'https://orcid.org/0000-0002-9538-7919',
         'type': 'Person'},
        {'name': 'The Ruby Citation File Format Developers',
         'type': 'Organization'}]
    assert subject.titles == [{'title': 'Ruby CFF Library'}]
    assert subject.descriptions[0]['description'].startswith(
        'This library provides a Ruby interface to manipulate Citation File Format files')
    assert subject.subjects == [{'subject': 'ruby'}, {'subject': 'credit'}, {'subject': 'software citation'}, {'subject': 'research software'}, {
        'subject': 'software sustainability'}, {'subject': 'metadata'}, {'subject': 'citation file format'}, {'subject': 'cff'}]
    assert subject.date == {'published': '2022-11-05'}
    assert subject.version == '1.0.1'
    assert subject.rights is None
    assert subject.references is None
    assert subject.publisher == 'GitHub'
    assert subject.state == 'findable'


def test_cff_converter_python():
    """cff-converter-python"""
    string = 'https://github.com/citation-file-format/cff-converter-python/blob/main/CITATION.cff'
    subject = Metadata(string)

    assert subject.id is None
    assert subject.url == 'https://github.com/citation-file-format/cff-converter-python'
    assert subject.type == "Software"
    assert subject.creators == [
        {'affiliation': [{'name': 'Netherlands eScience Center'}],
         'familyName': 'Spaaks',
         'givenName': 'Jurriaan H.',
         'id': 'https://orcid.org/0000-0002-7064-4069',
         'type': 'Person'},
        {'affiliation': [{'name': 'Netherlands eScience Center'}],
         'familyName': 'Klaver',
         'givenName': 'Tom',
         'type': 'Person'},
        {'affiliation': [{'name': 'Netherlands eScience Center'}],
         'familyName': 'Verhoeven',
         'givenName': 'Stefan',
         'id': 'https://orcid.org/0000-0002-5821-2060',
         'type': 'Person'},
        {'affiliation': [{'name': 'Humboldt-Universität zu Berlin'}],
         'familyName': 'Druskat',
         'givenName': 'Stephan',
         'id': 'https://orcid.org/0000-0003-4925-7248',
         'type': 'Person'},
        {'affiliation': [{'name': 'University of Oslo'}],
         'familyName': 'Leoncio',
         'givenName': 'Waldir',
         'type': 'Person'}]
    assert subject.titles == [{'title': 'cffconvert'}]
    assert subject.descriptions == [
        {'description': 'Command line program to validate and convert CITATION.cff files.', 'descriptionType': 'Abstract'}]
    assert subject.subjects == [{'subject': 'bibliography'}, {'subject': 'bibtex'}, {'subject': 'cff'}, {'subject': 'citation'}, {
        'subject': 'citation.cff'}, {'subject': 'codemeta'}, {'subject': 'endnote'}, {'subject': 'ris'}, {'subject': 'citation file format'}]
    assert subject.date == {'published': '2021-09-22'}
    assert subject.version == '2.0.0'
    assert subject.rights is None
    assert subject.references is None
    assert subject.publisher == 'GitHub'
    assert subject.state == 'findable'


def test_github_repo():
    """github repo"""
    string = 'https://github.com/kyleliang919/Long-context-transformers'
    subject = Metadata(string)

    assert subject.id == 'https://doi.org/10.5281/zenodo.7651809'
    assert subject.url == 'https://github.com/kyleliang919/Long-context-transformers'
    assert subject.type == 'Software'
    assert subject.creators == [{'type': 'Person', 'id': 'https://orcid.org/0000-0002-0055-8659', 'givenName': 'Kaizhao', 'familyName': 'Liang'}]
    assert subject.titles == [{'title': 'Long Context Transformer v0.0.1'}]
    assert subject.descriptions is None
    assert subject.subjects is None
    assert subject.date == {'published': '2023-02-17'}
    assert subject.version == '0.0.1'
    assert subject.rights is None
    assert subject.references is None
    assert subject.publisher == 'GitHub'
    assert subject.state == 'findable'
