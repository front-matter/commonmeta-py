"""Test codemeta reader"""
from os import path
import pytest
from commonmeta import Metadata
from commonmeta.readers.codemeta_reader import get_codemeta, read_codemeta


@pytest.mark.vcr
def test_rdataone():
    """rdataone"""
    string = path.join(path.dirname(__file__), 'fixtures', 'codemeta.json')
    subject = Metadata(string)
    assert subject.id == 'https://doi.org/10.5063/f1m61h5x'
    assert subject.type == 'Software'
    assert subject.url == 'https://github.com/DataONEorg/rdataone'
    assert subject.creators == [{'nameType': 'Personal', 'givenName': 'Matt', 'familyName': 'Jones', 'affiliation': [{'name': 'NCEAS'}]}, {'nameType': 'Personal', 'givenName': 'Peter',
                                                                                                                                           'familyName': 'Slaughter', 'affiliation': [{'name': 'NCEAS'}]}, {'nameType': 'Personal', 'givenName': 'University of California, Santa', 'familyName': 'Barbara'}]
    assert subject.titles == [{'title': 'R Interface to the DataONE REST API'}]
    assert subject.descriptions[0]['description'].startswith(
        'Provides read and write access to data and metadata')
    # [{'subject': 'data sharing'}], [{'subject': 'data repository'}], [{'subject': 'dataone'}]
    assert subject.subjects is None
    assert subject.dates == [{'date': '2016-05-27', 'dateType': 'Issued'}, {
        'date': '2016-05-27', 'dateType': 'Created'}, {'date': '2016-05-27', 'dateType': 'Updated'}]
    assert subject.publisher == 'https://cran.r-project.org'
    assert subject.publication_year == 2016
    assert subject.rights == [{'rights': 'Apache License 2.0', 'rightsUri': 'http://www.apache.org/licenses/LICENSE-2.0',
                               'rightsIdentifier': 'apache-2.0', 'rightsIdentifierScheme': 'SPDX', 'schemeUri': 'https://spdx.org/licenses/'}]
    assert subject.version == '2.0.0'
    assert subject.state == 'findable'


def test_metadata_reports():
    """metadata_reports"""
    string = 'https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json'
    subject = Metadata(string)

    assert subject.id == 'https://doi.org/10.5438/wr0x-e194'
    assert subject.type == 'Software'
    assert subject.url == 'https://github.com/datacite/metadata-reports'
    assert len(subject.creators) == 4
    assert subject.creators[0] == {
        'nameType': 'Personal', 'givenName': 'Martin', 'familyName': 'Fenner'}
    assert subject.titles == [{'title': 'DOI Registrations for Software'}]
    assert subject.descriptions[0]['description'].startswith(
        'Analysis of DataCite DOIs registered for software')
    assert subject.subjects is None
    assert subject.dates == [{'date': '2018-05-17', 'dateType': 'Issued'}, {
        'date': '2018-03-09', 'dateType': 'Created'}, {'date': '2018-05-17', 'dateType': 'Updated'}]
    assert subject.publication_year == 2018
    assert subject.publisher == 'DataCite'
    assert subject.rights == [{'rights': 'MIT License', 'rightsIdentifier': 'mit', 'rightsIdentifierScheme': 'SPDX',
                               'rightsUri': 'https://opensource.org/licenses/MIT', 'schemeUri': 'https://spdx.org/licenses/'}]
    assert subject.version is None
    assert subject.state == 'findable'
