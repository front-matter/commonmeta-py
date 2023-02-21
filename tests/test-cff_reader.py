"""Test cff reader"""
from os import path
import pytest
from commonmeta import Metadata


@pytest.mark.vcr
def test_ruby_cff():
    """ruby-cff"""
    string = 'https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff'
    meta = Metadata(string)

    assert meta.pid == 'https://doi.org/10.5281/zenodo.1184077'
    assert meta.url == 'https://github.com/citation-file-format/ruby-cff'
    assert meta.types == {
        'bibtex': 'misc',
        'citeproc': 'article-journal',
        'resourceTypeGeneral': 'Software',
        'ris': 'COMP',
        'schemaOrg': 'SoftwareSourceCode',
    }
    assert meta.creators == [
        {'affiliation': [{'name': 'The University of Manchester, UK'}],
         'familyName': 'Haines',
         'givenName': 'Robert',
         'nameIdentifiers': [{'nameIdentifier': 'https://orcid.org/0000-0002-9538-7919',
                              'nameIdentifierScheme': 'ORCID',
                              'schemeUri': 'https://orcid.org'}],
         'nameType': 'Personal'},
        {'name': 'The Ruby Citation File Format Developers',
         'nameType': 'Organizational'}]
    assert meta.titles == [{'title': 'Ruby CFF Library'}]
    assert meta.descriptions[0]['description'].startswith(
        'This library provides a Ruby interface to manipulate Citation File Format files')
    assert meta.subjects == [{'subject': 'ruby'}, {'subject': 'credit'}, {'subject': 'software citation'}, {'subject': 'research software'}, {
        'subject': 'software sustainability'}, {'subject': 'metadata'}, {'subject': 'citation file format'}, {'subject': 'cff'}]
    assert meta.dates == [{'date': '2022-11-05', 'dateType': 'Issued'}]
    assert meta.version == '1.0.1'
    assert meta.rights == None
    assert meta.related_items is None
    assert meta.publication_year == 2022
    assert meta.publisher == 'GitHub'
    assert meta.state == 'findable'


def test_cff_converter_python():
    """cff-converter-python"""
    string = 'https://github.com/citation-file-format/cff-converter-python/blob/main/CITATION.cff'
    meta = Metadata(string)

    assert meta.pid is None
    assert meta.url == 'https://github.com/citation-file-format/cff-converter-python'
    assert meta.types == {
        'bibtex': 'misc',
        'citeproc': 'article-journal',
        'resourceTypeGeneral': 'Software',
        'ris': 'COMP',
        'schemaOrg': 'SoftwareSourceCode',
    }
    assert meta.creators == [
        {'affiliation': [{'name': 'Netherlands eScience Center'}],
         'familyName': 'Spaaks',
         'givenName': 'Jurriaan H.',
         'nameIdentifiers': [{'nameIdentifier': 'https://orcid.org/0000-0002-7064-4069',
                              'nameIdentifierScheme': 'ORCID',
                              'schemeUri': 'https://orcid.org'}],
         'nameType': 'Personal'},
        {'affiliation': [{'name': 'Netherlands eScience Center'}],
         'familyName': 'Klaver',
         'givenName': 'Tom',
         'nameType': 'Personal'},
        {'affiliation': [{'name': 'Netherlands eScience Center'}],
         'familyName': 'Verhoeven',
         'givenName': 'Stefan',
         'nameIdentifiers': [{'nameIdentifier': 'https://orcid.org/0000-0002-5821-2060',
                              'nameIdentifierScheme': 'ORCID',
                              'schemeUri': 'https://orcid.org'}],
         'nameType': 'Personal'},
        {'affiliation': [{'name': 'Humboldt-Universität zu Berlin'}],
         'familyName': 'Druskat',
         'givenName': 'Stephan',
         'nameIdentifiers': [{'nameIdentifier': 'https://orcid.org/0000-0003-4925-7248',
                              'nameIdentifierScheme': 'ORCID',
                              'schemeUri': 'https://orcid.org'}],
         'nameType': 'Personal'},
        {'affiliation': [{'name': 'University of Oslo'}],
         'familyName': 'Leoncio',
         'givenName': 'Waldir',
         'nameType': 'Personal'}]
    assert meta.titles == [{'title': 'cffconvert'}]
    assert meta.descriptions == [
        {'description': 'Command line program to validate and convert CITATION.cff files.', 'descriptionType': 'Abstract'}]
    assert meta.subjects == [{'subject': 'bibliography'}, {'subject': 'bibtex'}, {'subject': 'cff'}, {'subject': 'citation'}, {
        'subject': 'citation.cff'}, {'subject': 'codemeta'}, {'subject': 'endnote'}, {'subject': 'ris'}, {'subject': 'citation file format'}]
    assert meta.dates == [{'date': '2021-09-22', 'dateType': 'Issued'}]
    assert meta.version == '2.0.0'
    assert meta.rights == None
    assert meta.related_items is None
    assert meta.publication_year == 2021
    assert meta.publisher == 'GitHub'
    assert meta.state == 'findable'


def test_github_repo():
    """github repo"""
    string = 'https://github.com/kyleliang919/Long-context-transformers'
    meta = Metadata(string)

    assert meta.pid == 'https://doi.org/10.5281/zenodo.7651809'
    assert meta.url == 'https://github.com/kyleliang919/Long-context-transformers'
    assert meta.types == {
        'bibtex': 'misc',
        'citeproc': 'article-journal',
        'resourceTypeGeneral': 'Software',
        'ris': 'COMP',
        'schemaOrg': 'SoftwareSourceCode',
    }
    assert meta.creators == [{'nameType': 'Personal', 'nameIdentifiers': [{'nameIdentifier': 'https://orcid.org/0000-0002-0055-8659', 'nameIdentifierScheme': 'ORCID', 'schemeUri': 'https://orcid.org'}], 'givenName': 'Kaizhao', 'familyName': 'Liang'}]
    assert meta.titles == [{'title': 'Long Context Transformer v0.0.1'}]
    assert meta.descriptions is None
    assert meta.subjects is None
    assert meta.dates == [{'date': '2023-02-17', 'dateType': 'Issued'}]
    assert meta.version == '0.0.1'
    assert meta.rights == None
    assert meta.related_items is None
    assert meta.publication_year == 2023
    assert meta.publisher == 'GitHub'
    assert meta.state == 'findable'