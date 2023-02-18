"""Test codemeta reader"""
from os import path
import pytest
from talbot import Metadata
from talbot.readers.codemeta_reader import get_codemeta, read_codemeta


@pytest.mark.vcr
def test_rdataone():
    """rdataone"""
    string = path.join(path.dirname(__file__), 'fixtures', 'codemeta.json')
    subject = Metadata(string)
    assert subject.pid == 'https://doi.org/10.5063/f1m61h5x'
    assert subject.url == 'https://github.com/dataoneorg/rdataone'
    assert subject.types == {'resourceTypeGeneral': 'Software', 'schemaOrg': 'SoftwareSourceCode', 'citeproc': 'article-journal', 'bibtex': 'misc', 'ris': 'COMP'}
    assert subject.creators == [{'nameType': 'Personal', 'name': 'Matt Jones', 'affiliation': [{'name': 'NCEAS'}]}, {'nameType': 'Personal', 'name': 'Peter Slaughter', 'affiliation': [{'name': 'NCEAS'}]}, {'nameType': 'Organizational', 'name': 'University of California, Santa Barbara'}]
    assert subject.titles == [{'title': 'R Interface to the DataONE REST API'}]
    assert subject.descriptions[0]['description'].startswith('Provides read and write access to data and metadata')
    # assert subject.subjects == [{'subject': 'data sharing'}], [{'subject': 'data repository'}], [{'subject': 'dataone'}]
    assert subject.dates == [{'date': '2016-05-27', 'dateType': 'Issued'}, {'date': '2016-05-27', 'dateType': 'Created'}, {'date': '2016-05-27', 'dateType': 'Updated'}]
    assert subject.publisher == 'https://cran.r-project.org'
    assert subject.publication_year == 2016
    assert subject.rights == [{'rightsIdentifier': 'Apache-2.0', 'rightsUri': None}]
    assert subject.version == '2.0.0'
    assert subject.state == 'findable'

#     it 'rdataone' do
#       input = "#{fixture_path}codemeta.json"
#       subject = described_class.new(input: input)
#       expect(subject.id).to eq('https://doi.org/10.5063/f1m61h5x')
#       expect(subject.url).to eq('https://github.com/DataONEorg/rdataone')
#       expect(subject.types).to eq('bibtex' => 'misc', 'citeproc' => 'article-journal',
#                                   'resourceTypeGeneral' => 'Software', 'ris' => 'COMP', 'schemaOrg' => 'SoftwareSourceCode')
#       expect(subject.creators).to eq([{ 'affiliation' => [{ 'name' => 'NCEAS' }],
#                                         'familyName' => 'Jones',
#                                         'givenName' => 'Matt',
#                                         'name' => 'Jones, Matt',
#                                         'nameIdentifiers' =>
#           [{ 'nameIdentifier' => 'https://orcid.org/0000-0003-0077-4738',
#              'nameIdentifierScheme' => 'ORCID',
#              'schemeUri' => 'https://orcid.org' }],
#                                         'nameType' => 'Personal' },
#                                       { 'affiliation' => [{ 'name' => 'NCEAS' }],
#                                         'familyName' => 'Slaughter',
#                                         'givenName' => 'Peter',
#                                         'name' => 'Slaughter, Peter',
#                                         'nameIdentifiers' =>
#                                          [{ 'nameIdentifier' => 'https://orcid.org/0000-0002-2192-403X',
#                                             'nameIdentifierScheme' => 'ORCID',
#                                             'schemeUri' => 'https://orcid.org' }],
#                                         'nameType' => 'Personal' },
#                                       { 'name' => 'University of California, Santa Barbara',
#                                         'nameType' => 'Organizational' }])
#       expect(subject.titles).to eq([{ 'title' => 'R Interface to the DataONE REST API' }])
#       expect(subject.descriptions.first['description']).to start_with('Provides read and write access to data and metadata')
#       expect(subject.subjects).to eq([{ 'subject' => 'data sharing' }, { 'subject' => 'data repository' },
#                                       { 'subject' => 'dataone' }])
#       expect(subject.version_info).to eq('2.0.0')
#       expect(subject.dates).to eq([{ 'date' => '2016-05-27', 'dateType' => 'Issued' },
#                                    { 'date' => '2016-05-27', 'dateType' => 'Created' }, { 'date' => '2016-05-27', 'dateType' => 'Updated' }])
#       expect(subject.publication_year).to eq('2016')
#       expect(subject.publisher).to eq('https://cran.r-project.org')
#       expect(subject.rights_list).to eq([{ 'rights' => 'Apache License 2.0',
#                                            'rightsIdentifier' => 'apache-2.0',
#                                            'rightsIdentifierScheme' => 'SPDX',
#                                            'rightsUri' => 'http://www.apache.org/licenses/LICENSE-2.0',
#                                            'schemeUri' => 'https://spdx.org/licenses/' }])
#     end

#     it 'maremma' do
#       input = "#{fixture_path}maremma/codemeta.json"
#       subject = described_class.new(input: input)
#       expect(subject.valid?).to be true
#       expect(subject.id).to eq('https://doi.org/10.5438/qeg0-3gm3')
#       expect(subject.url).to eq('https://github.com/datacite/maremma')
#       expect(subject.types).to eq('bibtex' => 'misc', 'citeproc' => 'article-journal',
#                                   'resourceTypeGeneral' => 'Software', 'ris' => 'COMP', 'schemaOrg' => 'SoftwareSourceCode')
#       expect(subject.creators).to eq([{ 'affiliation' => [{ 'name' => 'DataCite' }],
#                                         'familyName' => 'Fenner',
#                                         'givenName' => 'Martin',
#                                         'name' => 'Fenner, Martin',
#                                         'nameIdentifiers' =>
#           [{ 'nameIdentifier' => 'https://orcid.org/0000-0003-0077-4738',
#              'nameIdentifierScheme' => 'ORCID',
#              'schemeUri' => 'https://orcid.org' }],
#                                         'nameType' => 'Personal' }])
#       expect(subject.titles).to eq([{ 'title' => 'Maremma: a Ruby library for simplified network calls' }])
#       expect(subject.descriptions.first['description']).to start_with('Simplifies network calls')
#       expect(subject.subjects).to eq([{ 'subject' => 'faraday' }, { 'subject' => 'excon' },
#                                       { 'subject' => 'net/http' }])
#       expect(subject.dates).to eq([{ 'date' => '2017-02-24', 'dateType' => 'Issued' },
#                                    { 'date' => '2015-11-28', 'dateType' => 'Created' }, { 'date' => '2017-02-24', 'dateType' => 'Updated' }])
#       expect(subject.publication_year).to eq('2017')
#       expect(subject.publisher).to eq('DataCite')
#       expect(subject.rights_list).to eq([{ 'rights' => 'MIT License',
#                                            'rightsIdentifier' => 'mit',
#                                            'rightsIdentifierScheme' => 'SPDX',
#                                            'rightsUri' => 'https://opensource.org/licenses/MIT',
#                                            'schemeUri' => 'https://spdx.org/licenses/' }])
#     end

#     it 'metadata_reports' do
#       input = 'https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json'
#       subject = described_class.new(input: input)
#       expect(subject.valid?).to be true
#       expect(subject.id).to eq('https://doi.org/10.5438/wr0x-e194')
#       expect(subject.url).to eq('https://github.com/datacite/metadata-reports')
#       expect(subject.types).to eq('bibtex' => 'misc', 'citeproc' => 'article-journal',
#                                   'resourceTypeGeneral' => 'Software', 'ris' => 'COMP', 'schemaOrg' => 'SoftwareSourceCode')
#       expect(subject.creators.size).to eq(4)
#       expect(subject.creators.last).to eq('familyName' => 'Nielsen', 'givenName' => 'Lars Holm',
#                                           'name' => 'Nielsen, Lars Holm', 'nameIdentifiers' => [{ 'nameIdentifier' => 'https://orcid.org/0000-0001-8135-3489', 'nameIdentifierScheme' => 'ORCID', 'schemeUri' => 'https://orcid.org' }], 'nameType' => 'Personal')
#       expect(subject.titles).to eq([{ 'title' => 'DOI Registrations for Software' }])
#       expect(subject.descriptions.first['description']).to start_with('Analysis of DataCite DOIs registered for software')
#       expect(subject.subjects).to eq([{ 'subject' => 'doi' }, { 'subject' => 'software' },
#                                       { 'subject' => 'codemeta' }])
#       expect(subject.dates).to eq([{ 'date' => '2018-05-17', 'dateType' => 'Issued' },
#                                    { 'date' => '2018-03-09', 'dateType' => 'Created' }, { 'date' => '2018-05-17', 'dateType' => 'Updated' }])
#       expect(subject.publication_year).to eq('2018')
#       expect(subject.publisher).to eq('DataCite')
#       expect(subject.rights_list).to eq([{ 'rights' => 'MIT License',
#                                            'rightsIdentifier' => 'mit',
#                                            'rightsIdentifierScheme' => 'SPDX',
#                                            'rightsUri' => 'https://opensource.org/licenses/MIT',
#                                            'schemeUri' => 'https://spdx.org/licenses/' }])
#     end
#   end
# end
