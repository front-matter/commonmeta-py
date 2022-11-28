import pytest
import os
import vcr
import requests
from talbot import Metadata
from requests.exceptions import HTTPError

subject = Metadata("10.7554/elife.01567")

@pytest.mark.vcr
def test_doi_with_data_citation():
    "DOi with data citation"
    
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
                              'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://elifesciences.org/articles/01567"
    assert subject.titles[0] == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    
    #   expect(subject.creators.length).to eq(5)
    #   expect(subject.creators.first).to eq("nameType" => "Personal", 'name' => 'Ralser, Markus',
    #                                        'givenName' => 'Markus', 'familyName' => 'Ralser')
    #   expect(subject.contributors).to eq([{ 'contributorType' => 'Editor', 'familyName' => 'Janbon',
    #                                         'givenName' => 'Guilhem', 'name' => 'Janbon, Guilhem', "nameType"=>"Personal" }])
    assert subject.rights_list == [{ 'rights': 'Creative Commons Attribution 3.0 Unported',
                                     'rightsIdentifier': 'cc-by-3.0',
                                     'rightsIdentifierScheme': 'SPDX',
                                     'rightsURI': 'https://creativecommons.org/licenses/by/3.0/legalcode',
                                     'schemeUri': 'https://spdx.org/licenses/' }]
    
    assert subject.dates == [
        { 'date': '2014-02-11', 'dateType': 'Issued' },
        { 'date': '2022-03-26', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2014'
    assert subject.date_registered == '2014-02-11'
    assert subject.publisher == 'eLife Sciences Publications, Ltd'
    assert subject.issn == '2050-084X'
    assert len(subject.related_identifiers) == 28
    assert subject.related_identifiers[0] == { 
        'relatedIdentifier': '2050-084X',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1038/ncb2764',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    #   expect(subject.related_identifiers.first).to eq('relatedIdentifier' => '1932-6203',
    #                                                   'relatedIdentifierType' => 'ISSN', 'relationType' => 'IsPartOf', 'resourceTypeGeneral' => 'Collection')
    #   expect(subject.related_identifiers.last).to eq(
    #     'relatedIdentifier' => '10.1056/nejm199109123251104', 'relatedIdentifierType' => 'DOI', 'relationType' => 'References'
    #   )
    assert subject.container == { 
        'identifier': '2050-084X',
        'identifierType': 'ISSN',
        'title': 'eLife', 
        'type': 'Journal',
        'volume': '3' }
    assert subject.agency == 'Crossref'
