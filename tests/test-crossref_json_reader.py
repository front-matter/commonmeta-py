import pytest 
# import os
# import vcr
 #import requests
from talbot import Metadata
# from requests.exceptions import HTTPError

@pytest.mark.vcr
def test_doi_with_data_citation():
    "DOi with data citation"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
        'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 
        'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://elifesciences.org/articles/01567"
    assert subject.titles[0] == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    assert len(subject.creators) == 5
    assert subject.creators[0] == {'affiliation': [{'name': 'Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland'}], 'familyName': 'Hardtke', 'givenName': 'Christian S', 'name': 'Christian S Hardtke', 'nameType': 'Personal'}
    assert subject.contributors is None
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
    # assert subject.funding_references == [{'name': 'SystemsX'}, {'name': 'EMBO longterm post-doctoral fellowships'},
    #     {'name': 'Marie Heim-Voegtlin'}, {'DOI': '10.13039/501100006390', 'doi-asserted-by': 'crossref', 'name': 'University of Lausanne'},
    #     {'name': 'SystemsX'}, {'DOI': '10.13039/501100003043', 'doi-asserted-by': 'publisher', 'name': 'EMBO'}]
    assert subject.container == { 
        'identifier': '2050-084X',
        'identifierType': 'ISSN',
        'title': 'eLife', 
        'type': 'Journal',
        'volume': '3' }
    assert subject.descriptions == [{'description': 
        ('<jats:p>Among various advantages, their small size makes '                
        'model organisms preferred subjects of investigation. Yet, '
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
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_journal_article():
    "journal article"
    subject = Metadata("10.1371/journal.pone.0000030")
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
        'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 
        'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://dx.plos.org/10.1371/journal.pone.0000030"
    assert subject.titles[0] == "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    assert len(subject.creators) == 5
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Sylvia Krobitsch', 
        'givenName': 'Sylvia', 'familyName': 'Krobitsch'}
    assert subject.contributors == [{'familyName': 'Janbon', 'givenName': 'Guilhem',
        'name': 'Guilhem Janbon', 'nameType': 'Personal'}]
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
    assert subject.funding_references is None
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
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_journal_article_with_funding():
    'journal article with funding'
    subject = Metadata("10.3389/fpls.2019.00816")
    assert subject.id == "https://doi.org/10.3389/fpls.2019.00816"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
        'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle',
        'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://www.frontiersin.org/article/10.3389/fpls.2019.00816/full"
    assert subject.titles[0] == "Transcriptional Modulation of Polyamine Metabolism in Fruit Species Under Abiotic and Biotic Stress"
    assert len(subject.creators) == 4
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Noam Alkan', 
        'givenName': 'Noam', 'familyName': 'Alkan'}
    assert subject.contributors is None
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
        'resourceTypeGeneral': 'Collection'}
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
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_journal_article_original_language():
    "journal article with original language"
    subject = Metadata('https://doi.org/10.7600/jspfsm.56.60')
    assert subject.id == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
        'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle',
        'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://www.jstage.jst.go.jp/article/jspfsm/56/1/56_1_60/_article/-char/ja/"
    # assert subject.titles[0] == "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    assert len(subject.creators) == 1
    assert subject.creators[0] == {'nameType': 'Organizational', 'name': ':(unav)'}
    assert subject.contributors is None
    assert subject.rights_list is None
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
    assert subject.funding_references is None
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
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_journal_article_with_rdf_for_container():
    "journal article with RDF for container"
    subject = Metadata('https://doi.org/10.1163/1937240X-00002096')
    assert subject.id == "https://doi.org/10.1163/1937240x-00002096"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
        'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle',
        'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://academic.oup.com/jcb/article-lookup/doi/10.1163/1937240X-00002096"
    assert subject.titles[0] == "Global distribution of Fabaeformiscandona subacuta: an\xa0exotic\xa0invasive Ostracoda on the Iberian Peninsula?"
    assert len(subject.creators) == 8
    assert subject.creators[0] == {'familyName': 'Karanovic',
        'givenName': 'Ivana',
        'name': 'Ivana Karanovic',
        'nameType': 'Personal'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '2012-01-01', 'dateType': 'Issued' },
        { 'date': '2019-07-05', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2012'
    assert subject.date_registered == '2012-11-20'
    assert subject.publisher == 'Oxford University Press (OUP)'
    assert subject.issn == '1937-240X'
    assert len(subject.related_identifiers) == 44
    assert subject.related_identifiers[0] == { 
        'relatedIdentifier': '1937-240X',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1002/aqc.1122',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container == { 
        'identifier': '1937-240X',
        'identifierType': 'ISSN',
        'title': 'Journal of Crustacean Biology', 
        'type': 'Journal',
        'issue': '6',
        'volume': '32',
        'firstPage': '949',
        'lastPage': '961'}
    assert subject.subjects == [
        {'subject': 'Aquatic Science'}
    ]
    assert subject.language == 'en'
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_book_chapter_with_rdf_for_container():
    "book chapter with RDF for container"
    subject = Metadata('https://doi.org/10.1007/978-3-642-33191-6_49')
    assert subject.id == "https://doi.org/10.1007/978-3-642-33191-6_49"
    assert subject.types == {'bibtex': 'inbook', 'citeproc': 'chapter',
        'resourceType': 'BookChapter', 'resourceTypeGeneral':'BookChapter', 'ris': 'CHAP', 'schemaOrg': 'Chapter'}
    assert subject.url == "http://link.springer.com/10.1007/978-3-642-33191-6_49"
    assert subject.titles[0] == "Human Body Orientation Estimation in Multiview Scenarios"
    assert len(subject.creators) == 3
    assert subject.creators[0] == {'familyName': 'Knoll',
        'givenName': 'Alois',
        'name': 'Alois Knoll',
        'nameType': 'Personal'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '2012', 'dateType': 'Issued' },
        { 'date': '2020-11-24', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2012'
    assert subject.date_registered == '2012-08-21'
    assert subject.publisher == 'Springer Berlin Heidelberg'
    assert subject.issn == '1611-3349'
    assert len(subject.related_identifiers) == 8
    assert subject.related_identifiers[0] == { 
        'relatedIdentifier': '1611-3349',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1109/avss.2011.6027284',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container == { 
        'identifier': '1611-3349',
        'identifierType': 'ISSN',
        'title': 'Advances in Visual Computing', 
        'type': 'Book',
        'firstPage': '499',
        'lastPage': '508'}
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_posted_content():
    "posted content"
    subject = Metadata('https://doi.org/10.1101/097196')
    assert subject.id == "https://doi.org/10.1101/097196"
    assert subject.types == {'bibtex': 'article', 'citeproc': 'article-journal',
        'resourceType': 'PostedContent', 'resourceTypeGeneral':'Preprint',
        'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle'}
    assert subject.url == "http://biorxiv.org/lookup/doi/10.1101/097196"
    assert subject.titles[0] == "A Data Citation Roadmap for Scholarly Data Repositories"
    assert len(subject.creators) == 11
    assert subject.creators[0] == {'familyName': 'Clark',
        'givenName': 'Timothy',
        'name': 'Timothy Clark',
        'nameType': 'Personal'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '2016-12-28', 'dateType': 'Issued' },
        { 'date': '2020-01-18', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2016'
    assert subject.date_registered == '2016-12-29'
    assert subject.publisher == 'Cold Spring Harbor Laboratory'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 8
    assert subject.related_identifiers[0] == {
        'relatedIdentifier': '10.2481/dsj.osom13-043',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions == [{'description': '<jats:title>Abstract</jats:title><jats:p>This article presents a practical roadmap for scholarly data repositories to implement data citation in accordance with the Joint Declaration of Data Citation Principles, a synopsis and harmonization of the recommendations of major science policy bodies. The roadmap was developed by the Repositories Expert Group, as part of the Data Citation Implementation Pilot (DCIP) project, an initiative of FORCE11.org and the NIH BioCADDIE (<jats:ext-link xmlns:xlink="http://www.w3.org/1999/xlink" ext-link-type="uri" xlink:href="https://biocaddie.org">https://biocaddie.org</jats:ext-link>) program. The roadmap makes 11 specific recommendations, grouped into three phases of implementation: a) required steps needed to support the Joint Declaration of Data Citation Principles, b) recommended steps that facilitate article/data publication workflows, and c) optional steps that further improve data citation support provided by data repositories.</jats:p>', 'descriptionType': 'Abstract'}]
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_peer_review():
    'peer review'
    subject = Metadata('10.7554/elife.55167.sa2')
    assert subject.id == "https://doi.org/10.7554/elife.55167.sa2"
    assert subject.types == {'bibtex': 'misc', 'citeproc': 'article-journal',
        'resourceType': 'PeerReview', 'resourceTypeGeneral':'PeerReview',
        'ris': 'GEN', 'schemaOrg': 'Review'}
    assert subject.url == "https://elifesciences.org/articles/55167#sa2"
    assert subject.titles[0] == "Author response: SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters"
    assert len(subject.creators) == 8
    assert subject.creators[0] == {'familyName': 'Barnett',
        'givenName': 'Alex H',
        'name': 'Alex H Barnett',
        'nameType': 'Personal',
        'affiliation': [{'name': 'Center for Computational Mathematics, Flatiron Institute, New York, United States'}]}
    assert subject.contributors is None
    assert subject.rights_list == [{'rights': 'Creative Commons Attribution 4.0 International',
        'rightsIdentifier': 'cc-by-4.0',
        'rightsIdentifierScheme': 'SPDX',
        'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode',
        'schemeUri': 'https://spdx.org/licenses/'}]
    assert subject.dates == [
        { 'date': '2020-04-29', 'dateType': 'Issued' },
        { 'date': '2020-05-19', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2020'
    assert subject.date_registered == '2020-05-19'
    assert subject.publisher == 'eLife Sciences Publications, Ltd'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_dissertation():
    'dissertation'
    subject = Metadata('10.14264/uql.2020.791')
    assert subject.id == "https://doi.org/10.14264/uql.2020.791"
    assert subject.types == {'bibtex': 'phdthesis', 'citeproc': 'thesis',
        'resourceType': 'Dissertation', 'resourceTypeGeneral':'Dissertation',
        'ris': 'THES', 'schemaOrg': 'Thesis'}
    assert subject.url == "http://espace.library.uq.edu.au/view/UQ:23a1e74"
    assert subject.titles[0] == "School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers"
    assert len(subject.creators) == 1
    assert subject.creators[0] == {'familyName': 'Collingwood',
        'givenName': 'Patricia Maree',
        'name': 'Patricia Maree Collingwood',
        'nameType': 'Personal'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '2020-06-08', 'dateType': 'Issued' },
        { 'date': '2020-06-08', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2020'
    assert subject.date_registered == '2020-06-08'
    assert subject.publisher == 'University of Queensland Library'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_doi_with_sici():
    'doi with sici'
    subject = Metadata('10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2')
    assert subject.id == "https://doi.org/10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    assert subject.types == {'bibtex': 'article', 'citeproc': 'article-journal',
        'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle'}
    assert subject.url == "http://doi.wiley.com/10.1890/0012-9658(2006)87[2832:TIOPMA]2.0.CO;2"
    assert subject.titles[0] == "THE IMPACT OF PARASITE MANIPULATION AND PREDATOR FORAGING BEHAVIOR ON PREDATOR–PREY COMMUNITIES"
    assert len(subject.creators) == 2
    assert subject.creators[0] == {'familyName': 'Rands',
        'givenName': 'S. A.',
        'name': 'S. A. Rands',
        'nameType': 'Personal'}
    assert subject.contributors is None
    assert subject.rights_list == [{'rightsURI': 'https://doi.wiley.com/10.1002/tdm_license_1.1'}]
    assert subject.dates == [
        { 'date': '2006-11', 'dateType': 'Issued' },
        { 'date': '2019-04-28', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2006'
    assert subject.date_registered == '2007-06-04'
    assert subject.publisher == 'Wiley'
    assert subject.issn == '0012-9658'
    assert len(subject.related_identifiers) == 35
    assert subject.related_identifiers[0] == {
        'relatedIdentifier': '0012-9658',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1098/rspb.2002.2213',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container == {'firstPage': '2832', 'identifier': '0012-9658', 'identifierType': 'ISSN', 'issue': '11',
        'lastPage': '2841', 'title': 'Ecology', 'type': 'Journal', 'volume': '87'}
    assert subject.subjects == [{'subject': 'Ecology, Evolution, Behavior and Systematics'}]
    assert subject.language == 'en'
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_doi_with_orcid():
    'doi_with_orcid'
    subject = Metadata("10.1155/2012/291294")
    assert subject.id == "https://doi.org/10.1155/2012/291294"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
                              'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "http://www.hindawi.com/journals/pm/2012/291294/"
    assert subject.titles[0] == "Delineating a Retesting Zone Using Receiver Operating Characteristic Analysis on Serial QuantiFERON Tuberculosis Test Results in US Healthcare Workers"
    assert len(subject.creators) == 7
    assert subject.creators[0] == {'affiliation': [{'name': 'War Related Illness and Injury Study Center '
        '(WRIISC) and Mental Illness Research Education and '
        'Clinical Center (MIRECC), Department of Veterans '
        'Affairs, Palo Alto, CA 94304, USA'},
        {'name': 'Department of Psychiatry and Behavioral Sciences, '
        'Stanford University School of Medicine, Stanford, CA 94304, USA'}],
        'nameType': 'Personal', 'name': 'Jerome A. Yesavage', 'givenName': 'Jerome A.', 'familyName': 'Yesavage'}
    assert subject.contributors is None
    assert subject.rights_list == [{ 'rights': 'Creative Commons Attribution 3.0 Unported',
        'rightsIdentifier': 'cc-by-3.0',
        'rightsIdentifierScheme': 'SPDX',
        'rightsURI': 'https://creativecommons.org/licenses/by/3.0/legalcode',
        'schemeUri': 'https://spdx.org/licenses/' }]
    assert subject.dates == [
        { 'date': '2012', 'dateType': 'Issued' },
        { 'date': '2016-08-02', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2012'
    assert subject.date_registered == '2012-12-30'
    assert subject.publisher == 'Hindawi Limited'
    assert subject.issn == '2090-1844'
    assert len(subject.related_identifiers) == 18
    assert subject.related_identifiers[0] == {
        'relatedIdentifier': '2090-1844',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1378/chest.12-0045',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container == {
        'identifier': '2090-1844',
        'identifierType': 'ISSN',
        'title': 'Pulmonary Medicine',
        'type': 'Journal',
        'volume': '2012',
        'firstPage': '1',
        'lastPage': '7' }
    assert subject.subjects == [
        {'subject': 'Pulmonary and Respiratory Medicine'},
        {'subject': 'General Medicine'}
    ]
    assert subject.language == 'en'
    assert subject.descriptions == [{'description': '<jats:p><jats:italic>Objective</jats:italic>. To find a statistically significant separation point for the QuantiFERON Gold In-Tube (QFT) interferon gamma release assay that could define an optimal “retesting zone” for use in serially tested low-risk populations who have test “reversions” from initially positive to subsequently negative results.<jats:italic>Method</jats:italic>. Using receiver operating characteristic analysis (ROC) to analyze retrospective data collected from 3 major hospitals, we searched for predictors of reversion until statistically significant separation points were revealed. A confirmatory regression analysis was performed on an additional sample.<jats:italic>Results</jats:italic>. In 575 initially positive US healthcare workers (HCWs), 300 (52.2%) had reversions, while 275 (47.8%) had two sequential positive tests. The most statistically significant (Kappa\u2009=\u20090.48, chi-square\u2009=\u2009131.0,<mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" id="M1"><mml:mrow><mml:mi>P</mml:mi><mml:mo>&lt;</mml:mo><mml:mn>0.001</mml:mn></mml:mrow></mml:math>) separation point identified by the ROC for predicting reversion was the tuberculosis antigen minus-nil (TBag-nil) value at 1.11 International Units per milliliter (IU/mL). The second separation point was found at TBag-nil at 0.72\u2009IU/mL (Kappa\u2009=\u20090.16, chi-square\u2009=\u20098.2,<mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" id="M2"><mml:mrow><mml:mi>P</mml:mi><mml:mo>&lt;</mml:mo><mml:mn>0.01</mml:mn></mml:mrow></mml:math>). The model was validated by the regression analysis of 287\u2009HCWs.<jats:italic>Conclusion</jats:italic>. Reversion likelihood increases as the TBag-nil approaches the manufacturer\'s cut-point of 0.35\u2009IU/mL. The most statistically significant separation point between those who test repeatedly positive and those who revert is 1.11\u2009IU/mL. Clinicians should retest low-risk individuals with initial QFT results\u2009&lt;\u20091.11\u2009IU/mL.</jats:p>', 'descriptionType': 'Abstract'}]
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_date_in_future():
    'date_in_future'
    subject = Metadata("10.1016/j.ejphar.2015.03.018")
    assert subject.id == "https://doi.org/10.1016/j.ejphar.2015.03.018"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
        'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR',
        'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://linkinghub.elsevier.com/retrieve/pii/S0014299915002332"
    assert subject.titles[0] == "Paving the path to HIV neurotherapy: Predicting SIV CNS disease"
    assert len(subject.creators) == 10
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Joseph L. Mankowski', 'givenName': 'Joseph L.', 'familyName': 'Mankowski'}
    assert subject.contributors is None
    assert subject.rights_list == [{'rightsURI': 'https://www.elsevier.com/tdm/userlicense/1.0'}]
    assert subject.dates == [
        { 'date': '2015-07', 'dateType': 'Issued' },
        { 'date': '2020-08-31', 'dateType': 'Updated'}
    ]
    assert subject.publication_year == '2015'
    assert subject.date_registered == '2015-04-06'
    assert subject.publisher == 'Elsevier BV'
    assert subject.issn == '0014-2999'
    assert len(subject.related_identifiers) == 88
    assert subject.related_identifiers[0] == { 
        'relatedIdentifier': '0014-2999',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1111/hiv.12134',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references == [
        {'awardNumber': 'R01 NS089482', 'funderIdentifier': 'https://doi.org/10.13039/100000002',
        'funderIdentifierType': 'Crossref Funder ID', 'funderName': 'NIH'},
        {'awardNumber': 'R01 NS077869', 'funderIdentifier': 'https://doi.org/10.13039/100000002',
        'funderIdentifierType': 'Crossref Funder ID', 'funderName': 'NIH'},
        {'awardNumber': 'P01 MH070306', 'funderIdentifier': 'https://doi.org/10.13039/100000002',
        'funderIdentifierType': 'Crossref Funder ID', 'funderName': 'NIH'},
        {'awardNumber': 'P40 OD013117', 'funderIdentifier': 'https://doi.org/10.13039/100000002',
        'funderIdentifierType': 'Crossref Funder ID', 'funderName': 'NIH'}, 
        {'awardNumber': 'T32 OD011089', 'funderIdentifier': 'https://doi.org/10.13039/100000002',
        'funderIdentifierType': 'Crossref Funder ID', 'funderName': 'NIH'}]
    assert subject.container == {
        'identifier': '0014-2999',
        'identifierType': 'ISSN',
        'title': 'European Journal of Pharmacology',
        'type': 'Journal',
        'volume': '759',
        'firstPage': '303',
        'lastPage': '312' }
    assert subject.subjects == [
        {'subject': 'Pharmacology'}
    ]
    assert subject.language == 'en'
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_vor_with_url():
    'vor_with_url'
    subject = Metadata("10.1038/hdy.2013.26")
    assert subject.id == "https://doi.org/10.1038/hdy.2013.26"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
                              'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle', 'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "http://www.nature.com/articles/hdy201326"
    assert subject.titles[0] == "Albinism in phylogenetically and geographically distinct populations of Astyanax cavefish arises through the same loss-of-function Oca2 allele"
    assert len(subject.creators) == 2
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'H Wilkens', 'givenName': 'H', 'familyName': 'Wilkens'}
    assert subject.contributors is None
    assert subject.rights_list == [{'rightsURI': 'https://www.springer.com/tdm'}]
    assert subject.dates == [
        { 'date': '2013-04-10', 'dateType': 'Issued' },
        { 'date': '2021-12-02', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2013'
    assert subject.date_registered == '2013-04-10'
    assert subject.publisher == 'Springer Science and Business Media LLC'
    assert subject.issn == '1365-2540'
    assert len(subject.related_identifiers) == 35
    assert subject.related_identifiers[0] == {
        'relatedIdentifier': '1365-2540',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1111/j.1095-8312.2003.00230.x',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container == {
        'identifier': '1365-2540',
        'identifierType': 'ISSN',
        'title': 'Heredity',
        'type': 'Journal',
        'volume': '111',
        'issue': '2',
        'firstPage': '122',
        'lastPage': '130' }
    assert subject.subjects == [
        {'subject': 'Genetics (clinical)'},
        {'subject': 'Genetics'}
    ]
    assert subject.language == 'en'
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_dataset():
    'dataset'
    subject = Metadata("10.2210/pdb4hhb/pdb")
    assert subject.id == "https://doi.org/10.2210/pdb4hhb/pdb"
    assert subject.types == { 'bibtex': 'misc', 'citeproc': 'article-journal',
        'resourceType': 'Component', 'resourceTypeGeneral':'Text', 'ris': 'GEN',
        'schemaOrg': 'CreativeWork' }
    assert subject.url == "https://www.wwpdb.org/pdb?id=pdb_00004hhb"
    assert subject.titles[0] == "THE CRYSTAL STRUCTURE OF HUMAN DEOXYHAEMOGLOBIN AT 1.74 ANGSTROMS RESOLUTION"
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'M.F. Perutz',
        'givenName': 'M.F.', 'familyName': 'Perutz'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '1984-07-17', 'dateType': 'Issued' },
        { 'date': '2021-03-30', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '1984'
    assert subject.date_registered == '2006-01-05'
    assert subject.publisher == 'Worldwide Protein Data Bank'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_component():
    'component'
    subject = Metadata("10.1371/journal.pmed.0030277.g001")
    assert subject.id == "https://doi.org/10.1371/journal.pmed.0030277.g001"
    assert subject.types == { 'bibtex': 'misc', 'citeproc': 'article-journal',
        'resourceType': 'Component', 'resourceTypeGeneral':'Text', 'ris': 'GEN',
        'schemaOrg': 'CreativeWork' }
    assert subject.url == "https://dx.plos.org/10.1371/journal.pmed.0030277.g001"
    assert subject.titles == []
    assert subject.creators[0] == {'nameType': 'Organizational', 'name': ':(unav)'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '2015-10-20', 'dateType': 'Issued' },
        { 'date': '2018-10-19', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2015'
    assert subject.date_registered == '2015-10-20'
    assert subject.publisher == 'Public Library of Science (PLoS)'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_dataset_usda():
    'dataset usda'
    subject = Metadata("10.2737/RDS-2018-0001")
    assert subject.id == "https://doi.org/10.2737/rds-2018-0001"
    assert subject.types == { 'bibtex': 'misc', 'citeproc': 'dataset',
                              'resourceType': 'Dataset', 'resourceTypeGeneral':'Dataset',
                              'ris': 'DATA', 'schemaOrg': 'Dataset' }
    assert subject.url == "https://www.fs.usda.gov/rds/archive/Catalog/RDS-2018-0001"
    assert subject.titles[0] == "Fledging times of grassland birds"
    assert subject.creators[0] == {'affiliation': [{'name': 'University of Manitoba'}],
        'nameType': 'Personal', 'name': 'Christoph S. Ng', 'givenName': 'Christoph S.', 
        'familyName': 'Ng'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '2017-08-09', 'dateType': 'Issued' },
        { 'date': '2021-07-01', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2017'
    assert subject.date_registered == '2017-08-09'
    assert subject.publisher == 'Forest Service Research Data Archive'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 5
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.1674/0003-0031-178.1.47',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container == {'title': 'Forest Service Research Data Archive', 'type': 'Periodical'}
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'

def test_book_chapter():
    'book chapter'
    subject = Metadata("10.1007/978-3-662-46370-3_13")
    assert subject.id == "https://doi.org/10.1007/978-3-662-46370-3_13"
    assert subject.types == { 'bibtex': 'inbook', 'citeproc': 'chapter',
                              'resourceType': 'BookChapter', 'resourceTypeGeneral':'BookChapter',
                              'ris': 'CHAP', 'schemaOrg': 'Chapter' }
    assert subject.url == "http://link.springer.com/10.1007/978-3-662-46370-3_13"
    assert subject.titles[0] == "Clinical Symptoms and Physical Examinations"
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Tom Clement Ludvigsen',
        'givenName': 'Tom Clement', 'familyName': 'Ludvigsen'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '2015', 'dateType': 'Issued' },
        { 'date': '2015-04-13', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2015'
    assert subject.date_registered == '2015-04-13'
    assert subject.publisher == 'Springer Berlin Heidelberg'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 0
    assert subject.funding_references is None
    assert subject.container == {'title': 'Shoulder Stiffness', 'type': 'Book',
        'firstPage': '155', 'lastPage': '158'}
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'


def test_another_book_chapter():
    'another book chapter'
    subject = Metadata("10.1007/978-3-319-75889-3_1")
    assert subject.id == "https://doi.org/10.1007/978-3-319-75889-3_1"
    assert subject.types == { 'bibtex': 'inbook', 'citeproc': 'chapter',
                              'resourceType': 'BookChapter', 'resourceTypeGeneral':'BookChapter',
                              'ris': 'CHAP', 'schemaOrg': 'Chapter' }
    assert subject.url == "http://link.springer.com/10.1007/978-3-319-75889-3_1"
    assert subject.titles[0] == "Climate Change and Increasing Risk of Extreme Heat"
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Hunter M. Jones',
        'givenName': 'Hunter M.', 'familyName': 'Jones'}
    assert subject.contributors is None
    assert subject.rights_list == [{'rightsURI': 'https://www.springer.com/tdm'}]
    assert subject.dates == [
        { 'date': '2018', 'dateType': 'Issued' },
        { 'date': '2019-10-16', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2018'
    assert subject.date_registered == '2018-04-17'
    assert subject.publisher == 'Springer International Publishing'
    assert subject.issn == '2523-3629'
    assert len(subject.related_identifiers) == 30
    assert subject.funding_references is None
    assert subject.container == {'type': 'Book', 'title': 'SpringerBriefs in Medical Earth Sciences',
        'identifier': '2523-3629', 'identifierType': 'ISSN', 'firstPage': '1', 'lastPage': '13'}
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'


def test_yet_another_book_chapter():
    'yet another book chapter'
    subject = Metadata("https://doi.org/10.4018/978-1-4666-1891-6.ch004")
    assert subject.id == "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    assert subject.types == { 'bibtex': 'inbook', 'citeproc': 'chapter',
                              'resourceType': 'BookChapter', 'resourceTypeGeneral':'BookChapter',
                              'ris': 'CHAP', 'schemaOrg': 'Chapter' }
    assert subject.url == "http://services.igi-global.com/resolvedoi/resolve.aspx?doi=10.4018/978-1-4666-1891-6.ch004"
    assert subject.titles[0] == "Unsupervised and Supervised Image Segmentation Using Graph Partitioning"
    assert subject.creators[0] == {'affiliation': [{'name': 'Université de Lyon, France'}],
        'nameType': 'Personal', 'name': 'Charles-Edmond Bichot',
        'givenName': 'Charles-Edmond', 'familyName': 'Bichot'}
    assert subject.contributors is None
    assert subject.rights_list is None
    assert subject.dates == [
        { 'date': '2012-08-08', 'dateType': 'Issued' },
        { 'date': '2019-07-02', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2012'
    assert subject.date_registered == '2012-08-08'
    assert subject.publisher == 'IGI Global'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 27
    assert subject.funding_references is None
    assert subject.container == {'type': 'Book', 'title': 'Graph-Based Methods in Computer Vision',
        'firstPage': '72', 'lastPage': '94'}
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions == [{'description': '<jats:p>Image segmentation is an important research area in computer vision and its applications in different disciplines, such as medicine, are of great importance. It is often one of the very first steps of computer vision or pattern recognition methods. This is because segmentation helps to locate objects and boundaries into images. The objective of segmenting an image is to partition it into disjoint and homogeneous sets of pixels. When segmenting an image it is natural to try to use graph partitioning, because segmentation and partitioning share the same high-level objective, to partition a set into disjoints subsets. However, when using graph partitioning for segmenting an image, several big questions remain: What is the best way to convert an image into a graph? Or to convert image segmentation objectives into graph partitioning objectives (not to mention what are image segmentation objectives)? What are the best graph partitioning methods and algorithms for segmenting an image? In this chapter, the author tries to answer these questions, both for unsupervised and supervised image segmentation approach, by presenting methods and algorithms and by comparing them.</jats:p>', 'descriptionType': 'Abstract'}]
    assert subject.version_info is None
    assert subject.agency == 'Crossref'


def test_missing_creator():
    'missing creator'
    subject = Metadata("10.3390/publications6020015")
    assert subject.id == "https://doi.org/10.3390/publications6020015"
    assert subject.types == { 'bibtex': 'article', 'citeproc': 'article-journal',
                              'resourceType': 'JournalArticle', 'resourceTypeGeneral':'JournalArticle',
                              'ris': 'JOUR', 'schemaOrg': 'ScholarlyArticle' }
    assert subject.url == "https://www.mdpi.com/2304-6775/6/2/15"
    assert subject.titles[0] == "Converting the Literature of a Scientific Field to Open Access through Global Collaboration: The Experience of SCOAP3 in Particle Physics"
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Salvatore Mele',
        'givenName': 'Salvatore', 'familyName': 'Mele'}
    assert subject.contributors is None
    assert subject.rights_list == [{'rights': 'Creative Commons Attribution 4.0 International', 'rightsIdentifier': 'cc-by-4.0', 'rightsIdentifierScheme': 'SPDX',
        'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode', 'schemeUri': 'https://spdx.org/licenses/'}]
    assert subject.dates == [
        { 'date': '2018-04-09', 'dateType': 'Issued' },
        { 'date': '2021-07-22', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2018'
    assert subject.date_registered == '2018-04-10'
    assert subject.publisher == 'MDPI AG'
    assert subject.issn == '2304-6775'
    assert len(subject.related_identifiers) == 6
    assert subject.related_identifiers[0] == { 
        'relatedIdentifier': '2304-6775',
        'relatedIdentifierType': 'ISSN',
        'relationType': 'IsPartOf',
        'resourceTypeGeneral': 'Collection' }
    assert subject.related_identifiers[-1] == {
        'relatedIdentifier': '10.4119/unibi/ub.2014.18',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container == {'type': 'Journal', 'title': 'Publications',
        'firstPage': '15', 'issue': '2', 'volume': '6', 'identifier': '2304-6775',
        'identifierType': 'ISSN'}
    assert subject.subjects == [
        {'subject': 'Computer Science Applications'},
        {'subject': 'Media Technology'},
        {'subject': 'Communication'},
        {'subject': 'Business and International Management'},
        {'subject': 'Library and Information Sciences'}
    ]
    assert subject.language == 'en'
    assert subject.descriptions == [
        {'description': '<jats:p>Gigantic particle accelerators, incredibly complex '
        'detectors, an antimatter factory and the discovery of the '
        'Higgs boson—this is part of what makes CERN famous. Only a '
        'few know that CERN also hosts the world largest Open Access '
        'initiative: SCOAP3. The Sponsoring Consortium for Open '
        'Access Publishing in Particle Physics started operation in '
        '2014 and has since supported the publication of 20,000 Open '
        'Access articles in the field of particle physics, at no '
        'direct cost, nor burden, for individual authors worldwide. '
        'SCOAP3 is made possible by a 3000-institute strong '
        'partnership, where libraries re-direct funds previously used '
        'for subscriptions to ‘flip’ articles to ‘Gold Open Access’. '
        'With its recent expansion, the initiative now covers about '
        '90% of the journal literature of the field. This article '
        'describes the economic principles of SCOAP3, the '
        'collaborative approach of the partnership, and finally '
        'summarizes financial results after four years of successful '
        'operation.</jats:p>',
        'descriptionType': 'Abstract'
        }
    ]
    assert subject.version_info is None
    assert subject.agency == 'Crossref'


def test_book():
    'book' 
    subject = Metadata("https://doi.org/10.1017/9781108348843")
    assert subject.id == "https://doi.org/10.1017/9781108348843"
    assert subject.types == { 'bibtex': 'book', 'citeproc': 'book',
                              'resourceType': 'Monograph', 'resourceTypeGeneral':'Book',
                              'ris': 'BOOK', 'schemaOrg': 'Book' }
    assert subject.url == "https://www.cambridge.org/core/product/identifier/9781108348843/type/book"
    assert subject.titles[0] == "The Politics of the Past in Early China"
    assert subject.creators[0] == {'nameType': 'Personal', 'name': 'Vincent S. Leung',
        'givenName': 'Vincent S.', 'familyName': 'Leung'}
    assert subject.contributors is None
    assert subject.rights_list == [{'rightsURI': 'https://www.cambridge.org/core/terms'}]
    assert subject.dates == [
        { 'date': '2019-07-01', 'dateType': 'Issued' },
        { 'date': '2022-09-22', 'dateType': 'Updated' }
    ]
    assert subject.publication_year == '2019'
    assert subject.date_registered == '2019-07-01'
    assert subject.publisher == 'Cambridge University Press'
    assert subject.issn is None
    assert len(subject.related_identifiers) == 90
    assert subject.related_identifiers[0] == {
        'relatedIdentifier': '10.1093/acprof:oso/9780199367344.001.0001',
        'relatedIdentifierType': 'DOI',
        'relationType': 'References' }
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version_info is None
    assert subject.agency == 'Crossref'
