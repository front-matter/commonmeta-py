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
    assert len(subject.creators) == 5
    assert subject.creators[0] == {'affiliation': [{'name': 'Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland'}], 'familyName': 'Hardtke', 'givenName': 'Christian S', 'name': 'Christian S Hardtke', 'nameType': 'Personal'}
    assert subject.contributors == None
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
    assert subject.funding_references == None
    assert subject.container == { 
        'identifier': '2050-084X',
        'identifierType': 'ISSN',
        'title': 'eLife', 
        'type': 'Journal',
        'volume': '3' }
    assert subject.descriptions == [{'description': 
        ('<jats:p>Among various advantages, their small size makes '                'model organisms preferred subjects of investigation. Yet, '
        'even in model systems detailed analysis of numerous '
        'developmental processes at cellular level is severely '
        'hampered by their scale. For instance, secondary growth of '
        'Arabidopsis hypocotyls creates a radial pattern of highly '
        'specialized tissues that comprises several thousand cells '
        'starting from a few dozen. This dynamic process is difficult '
        'to follow because of its scale and because it can only be '
        'investigated invasively, precluding comprehensive '
        'understanding of the cell proliferation, differentiation, '
        'and patterning events involved. To overcome such limitation, '
        'we established an automated quantitative histology approach. '
        'We acquired hypocotyl cross-sections from tiled '
        'high-resolution images and extracted their information '
        'content using custom high-throughput image processing and '
        'segmentation. Coupled with automated cell type recognition '
        'through machine learning, we could establish a cellular '
        'resolution atlas that reveals vascular morphodynamics during '
        'secondary growth, for example equidistant phloem pole '
        'formation.</jats:p>'),            
        'descriptionType': 'Abstract'}]
    assert subject.subjects == [
        {'subject': 'General Immunology and Microbiology'},
        {'subject': 'General Biochemistry, Genetics and Molecular Biology'},
        {'subject': 'General Medicine'},
        {'subject': 'General Neuroscience'}
    ]
    assert subject.language == 'en'
    assert subject.version_info == None
    assert subject.agency == 'Crossref'

def test_journal_article():
    "journal article"
    subject = Metadata("10.1371/journal.pone.0000030")
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
                              'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://dx.plos.org/10.1371/journal.pone.0000030"
    assert subject.titles[0] == "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    assert len(subject.creators) == 5
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Sylvia Krobitsch', 'givenName': 'Sylvia', 'familyName': 'Krobitsch'}
    assert subject.contributors == [{'familyName': 'Janbon', 'givenName': 'Guilhem', 'name': 'Guilhem Janbon', 'nameType': 'Personal'}]
    assert subject.rights_list == [{ 'rights': 'Creative Commons Attribution 4.0 International',
                                     'rightsIdentifier': 'cc-by-4.0',
                                     'rightsIdentifierScheme': 'SPDX',
                                     'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode',
                                     'schemeUri': 'https://spdx.org/licenses/' }]
    assert subject.dates == [
        { 'date': '2006-12-20', 'dateType': 'Issued' },
        { 'date': '2021-08-06', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2006'
    assert subject.date_registered == '2006-12-20'
    assert subject.publisher == 'Public Library of Science (PLoS)'
    assert subject.issn == '1932-6203'
    assert len(subject.related_identifiers) == 68
    assert subject.related_identifiers[0] == { 
        'relatedIdentifier': '1932-6203',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1056/nejm199109123251104',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references == None
    assert subject.container == { 
        'identifier': '1932-6203',
        'identifierType': 'ISSN',
        'title': 'PLoS ONE', 
        'type': 'Journal',
        'issue': '1',
        'volume': '1',
        'firstPage': 'e30' }
    assert subject.subjects == [{'subject': 'Multidisciplinary'}]
    assert subject.language == 'en'
    assert subject.descriptions == None
    assert subject.version_info == None
    assert subject.agency == 'Crossref'

def test_journal_article_with_funding():
    'journal article with funding'
    subject = Metadata("10.3389/fpls.2019.00816")
    assert subject.id == "https://doi.org/10.3389/fpls.2019.00816"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
                              'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://www.frontiersin.org/article/10.3389/fpls.2019.00816/full"
    assert subject.titles[0] == "Transcriptional Modulation of Polyamine Metabolism in Fruit Species Under Abiotic and Biotic Stress"
    assert len(subject.creators) == 4
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Noam Alkan', 'givenName': 'Noam', 'familyName': 'Alkan'}
    assert subject.contributors == None
    assert subject.rights_list == [{ 'rights': 'Creative Commons Attribution 4.0 International',
                                     'rightsIdentifier': 'cc-by-4.0',
                                     'rightsIdentifierScheme': 'SPDX',
                                     'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode',
                                     'schemeUri': 'https://spdx.org/licenses/' }]
    assert subject.dates == [
        { 'date': '2019-07-02', 'dateType': 'Issued' },
        { 'date': '2019-09-22', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2019'
    assert subject.date_registered == '2019-07-02'
    assert subject.publisher == 'Frontiers Media SA'
    assert subject.issn == '1664-462X'
    assert len(subject.related_identifiers) == 70
    assert subject.related_identifiers[0] == { 
        'relatedIdentifier': '1664-462X',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.17660/actahortic.2004.632.41',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references == [
        {'awardNumber': 'CA17111',
        'funderIdentifier': 'https://doi.org/10.13039/501100000921',
        'funderIdentifierType': 'Crossref Funder ID',
        'funderName': 'COST (European Cooperation in Science and Technology)'}
    ]
    assert subject.container == { 
        'identifier': '1664-462X',
        'identifierType': 'ISSN',
        'title': 'Frontiers in Plant Science', 
        'type': 'Journal',
        'volume': '10' }
    assert subject.subjects == [{'subject': 'Plant Science'}]
    assert subject.language == None
    assert subject.descriptions == None
    assert subject.version_info == None
    assert subject.agency == 'Crossref'

def test_journal_article_original_language():
    "journal article with original language"
    subject = Metadata('https://doi.org/10.7600/jspfsm.56.60')
    assert subject.id == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
                              'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://www.jstage.jst.go.jp/article/jspfsm/56/1/56_1_60/_article/-char/ja/"
    # assert subject.titles[0] == "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    assert len(subject.creators) == 1
    assert subject.creators[0] == {'nameType': 'Organizational', 'name': ':(unav)'}
    assert subject.contributors == None
    assert subject.rights_list == None
    assert subject.dates == [
        { 'date': '2007', 'dateType': 'Issued' },
        { 'date': '2021-05-20', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2007'
    assert subject.date_registered == '2012-08-30'
    assert subject.publisher == 'The Japanese Society of Physical Fitness and Sports Medicine'
    assert subject.issn == '1881-4751'
    assert len(subject.related_identifiers) == 8
    assert subject.related_identifiers[0] == { 
        'relatedIdentifier': '1881-4751',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1161/01.cir.95.6.1686',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references == None
    assert subject.container == { 
        'identifier': '1881-4751',
        'identifierType': 'ISSN',
        'title': 'Japanese Journal of Physical Fitness and Sports Medicine', 
        'type': 'Journal',
        'issue': '1',
        'volume': '56',
        'firstPage': '60',
        'lastPage': '60' }
    assert subject.subjects == [
        {'subject': 'Physical Therapy, Sports Therapy and Rehabilitation'},
        {'subject': 'Orthopedics and Sports Medicine'}
    ]
    assert subject.language == 'en'
    assert subject.descriptions == None
    assert subject.version_info == None
    assert subject.agency == 'Crossref'