import pytest
from talbot import utils
from talbot.utils import (
    parse_attributes, 
    get_date_from_date_parts, 
    get_date_from_parts,
    get_date_parts,
    dict_to_spdx, 
    normalize_orcid, 
    validate_orcid,
    normalize_id,
    normalize_ids,
    wrap, unwrap, 
    compact, 
    from_citeproc,
    crossref_api_url, datacite_api_url,
    presence,
    sanitize,
    find_from_format_by_id,
    from_schema_org,
    from_schema_org_creators,
    pages_as_string,
    from_schema_org_contributors
)

def test_parse_attributes():
    "parse_attributes"
    # string
    assert '10.5061/DRYAD.8515' == parse_attributes('10.5061/DRYAD.8515')
    # dict
    assert '10.5061/DRYAD.8515' == parse_attributes({ '__content__': '10.5061/DRYAD.8515' })
    # list
    assert '10.5061/DRYAD.8515' == parse_attributes([ { '__content__': '10.5061/DRYAD.8515' } ])

    # it 'array of strings' do
    #   element = %w[datacite doi metadata featured]
    #   response = subject.parse_attributes(element)
    #   expect(response).to eq(%w[datacite doi metadata featured])
    # end

    # None
    assert None is parse_attributes(None)
    # kwargs['first]
    #assert '10.5061/DRYAD.8515' == parse_attributes([ { '__content__': '10.5061/DRYAD.8515' }, '__content__': '10.5061/DRYAD.8516' } ], first=True)

def test_get_date_from_date_parts():
    "get_date_from_date_parts"
    assert "2012-01-01" == get_date_from_date_parts({"date-parts": [[2012, 1, 1]]})
    assert '2012-01' == get_date_from_date_parts({"date-parts": [[2012, 1]]})
    assert '2012' == get_date_from_date_parts({"date-parts": [[2012]]})
    assert None is get_date_from_date_parts({"date-parts": []})
    assert None is get_date_from_date_parts({})
    assert None is get_date_from_date_parts(None)

def test_get_date_from_parts():
    "get_date_from_parts"
    assert '2012-01-01' == get_date_from_parts(2012, 1, 1)
    assert '2012-01' == get_date_from_parts(2012, 1)
    assert '2012' == get_date_from_parts(2012)
    assert None is get_date_from_parts()

def test_get_date_parts():
    "get_date_parts"
    assert {'date-parts': [[2012, 1, 1]]} == get_date_parts("2012-01-01")
    assert {'date-parts': [[2012, 1]]} == get_date_parts("2012-01")
    assert {'date-parts': [[2012]]} == get_date_parts("2012")
    assert { 'date-parts': [[]] } == get_date_parts(None)

def test_wrap():
    "wrap"
    # None
    assert [] == wrap(None)
    # dict
    assert [{'name': 'test'}] == wrap({'name': 'test'})
    # list
    assert [{'name': 'test'}] == wrap([{'name': 'test'}])

def test_unwrap():
    "unwrap"
    # None
    assert None is unwrap([])
    # dict
    assert {'name': 'test'} == unwrap([{'name': 'test'}])
    # list
    assert [{'name': 'test'}, {'name': 'test2'}] == unwrap([{'name': 'test'}, {'name': 'test2'}])

def test_presence():
    "presence"
    assert None is presence("")
    assert None is presence([])
    assert None is presence({})
    assert 'test' == presence('test')
    assert [1] == presence([1])
    assert {'test': 1} == presence({'test': 1})

def test_compact():
    "compact"
    assert { 'name': 'test' } == compact({ 'name': 'test', 'other': None })

def test_dict_to_spdx_id():
    "dict_to_spdx id"
    assert { 'rights': 'Creative Commons Attribution 4.0 International',
             'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode',
             'rightsIdentifier': 'cc-by-4.0', 'rightsIdentifierScheme': 'SPDX',
             'schemeUri': 'https://spdx.org/licenses/' } == dict_to_spdx({ 'rightsIdentifier': 'cc-by-4.0' })

def test_dict_to_spdx_url():
    "dict_to_spdx url"
    assert { 'rights': 'Creative Commons Attribution 4.0 International',
             'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode', 
             'rightsIdentifier': 'cc-by-4.0', 'rightsIdentifierScheme': 'SPDX',
             'schemeUri': 'https://spdx.org/licenses/' } == dict_to_spdx({ 'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode' })

def test_dict_to_spdx_not_found():
    "dict_to_spdx not found"
    assert { 'rightsURI': 'info:eu-repo/semantics/openaccess' } == dict_to_spdx({ 'rightsURI': 'info:eu-repo/semantics/openAccess' })

def test_validate_orcid():
    "validate_orcid"
    assert '0000-0002-2590-225X' == validate_orcid('http://orcid.org/0000-0002-2590-225X')
    # orcid https
    assert '0000-0002-2590-225X' == validate_orcid('https://orcid.org/0000-0002-2590-225X')
    # orcid id
    assert '0000-0002-2590-225X' == validate_orcid('0000-0002-2590-225X')
    # orcid www
    assert '0000-0002-2590-225X' == validate_orcid('https://www.orcid.org/0000-0002-2590-225X')
    # orcid with spaces
    assert '0000-0002-1394-3097' == validate_orcid('0000 0002 1394 3097')
    # orcid sandbox    
    assert '0000-0002-2590-225X' == validate_orcid('http://sandbox.orcid.org/0000-0002-2590-225X')
    # orcid sandbox https
    assert '0000-0002-2590-225X' == validate_orcid('https://sandbox.orcid.org/0000-0002-2590-225X')
    # orcid wrong id format
    assert None is validate_orcid('0000-0002-1394-309')

def test_normalize_orcid():
    "normalize_orcid"
    assert 'https://orcid.org/0000-0002-2590-225X' == normalize_orcid('http://orcid.org/0000-0002-2590-225X')
    # orcid https
    assert 'https://orcid.org/0000-0002-2590-225X' == normalize_orcid('https://orcid.org/0000-0002-2590-225X')
    # orcid id
    assert 'https://orcid.org/0000-0002-2590-225X' == normalize_orcid('0000-0002-2590-225X')

def test_normalize_id():
    "normalize_id"
    assert 'https://doi.org/10.5061/dryad.8515' == normalize_id('10.5061/DRYAD.8515')
    # doi as url
    assert 'https://doi.org/10.5061/dryad.8515' == normalize_id('http://dx.doi.org/10.5061/DRYAD.8515')
    # url
    assert 'https://blog.datacite.org/eating-your-own-dog-food' == normalize_id('https://blog.datacite.org/eating-your-own-dog-food/')
    # url with utf-8
    # assert 'http://www.xn--8ws00zhy3a.com/eating-your-own-dog-food' == normalize_id('http://www.詹姆斯.com/eating-your-own-dog-food/')
    # ftp
    assert None is normalize_id('ftp://blog.datacite.org/eating-your-own-dog-food/')
    # invalid url
    assert None is normalize_id('http://')
    # string
    assert None is normalize_id('eating-your-own-dog-food')
    # filename
    assert None is normalize_id('crossref.xml')
    # sandbox via url
    assert 'https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7' == normalize_id('https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7')
    # sandbox via options
    assert 'https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7' == normalize_id('10.20375/0000-0001-ddb8-7', sandbox=True)

def test_normalize_ids():
    "normalize_ids"
    # doi
    ids = [{ '@type': 'CreativeWork', '@id': 'https://doi.org/10.5438/0012' },
         { '@type': 'CreativeWork', '@id': 'https://doi.org/10.5438/55E5-T5C0' }]
    response = [{ 'relatedIdentifier': '10.5438/0012',
        'relatedIdentifierType': 'DOI',
        'resourceTypeGeneral': 'Text' },
        { 'relatedIdentifier': '10.5438/55e5-t5c0',
        'relatedIdentifierType': 'DOI',
        'resourceTypeGeneral': 'Text' }]
    assert response == normalize_ids(ids=ids)
    # url
    ids = [{ '@type': 'CreativeWork',
         '@id': 'https://blog.datacite.org/eating-your-own-dog-food/' }]
    response = [{
        'relatedIdentifier': 'https://blog.datacite.org/eating-your-own-dog-food',
         'relatedIdentifierType': 'URL', 'resourceTypeGeneral': 'Text'
    }]
    assert response == normalize_ids(ids=ids)

def test_from_citeproc():
    "from_citeproc"
    assert [{'@type': 'Person', 'affiliation': [{'name': 'Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland'}],
        'familyName': 'Sankar', 'givenName': 'Martial', 'name': 'Martial Sankar'}] == from_citeproc([{"given": "Martial", "family": "Sankar", "sequence": "first", "affiliation": [{"name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"}]}])

def test_find_from_format_by_id():
    "find_from_format_by_id"
    assert "crossref" == find_from_format_by_id("10.1371/journal.pone.0042793")
    assert "datacite" == find_from_format_by_id("https://doi.org/10.5061/dryad.8515")
    assert "medra" == find_from_format_by_id("10.1392/roma081203")
    assert "kisti" == find_from_format_by_id("https://doi.org/10.5012/bkcs.2013.34.10.2889")
    assert "jalc" == find_from_format_by_id("https://doi.org/10.11367/grsj1979.12.283")
    assert "op" == find_from_format_by_id("https://doi.org/10.2903/j.efsa.2018.5239")
    # cff
    assert 'cff' == find_from_format_by_id('https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff')
    # cff repository url
    assert 'cff' == find_from_format_by_id('https://github.com/citation-file-format/ruby-cff')
    # codemeta
    assert 'codemeta' == find_from_format_by_id('https://github.com/datacite/maremma/blob/master/codemeta.json')
    # npm
    assert 'npm' == find_from_format_by_id('https://github.com/datacite/bracco/blob/master/package.json')
    # schema_org
    assert 'schema_org' == find_from_format_by_id('https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GAOC03')

def test_from_schema_org():
    "from_schema_org"
    author = { '@type': 'Person', '@id': 'http://orcid.org/0000-0003-1419-2405',
        'givenName': 'Martin', 'familyName': 'Fenner', 'name': 'Martin Fenner' }
    assert {'givenName': 'Martin', 'familyName': 'Fenner', 'name': 'Martin Fenner', 
        'type': 'Person', 'id': 'http://orcid.org/0000-0003-1419-2405'} == from_schema_org(author)

def test_from_schema_org_creators():
    "from_schema_org creators"
    authors = [{ '@type': 'Person', '@id': 'http://orcid.org/0000-0003-1419-2405', 
        'givenName': 'Martin', 'familyName': 'Fenner', 'name': 'Martin Fenner', 'affiliation': {
        '@id': 'https://ror.org/04wxnsj81', 'name': 'DataCite', '@type': 'Organization'} }]
    # response = from_schema_org_creators(authors)
    # assert response == [{ 'affiliation': [{ 'affiliationIdentifier': 'https://ror.org/04wxnsj81',
    #     'affiliationIdentifierScheme': 'ROR', '__content__': 'DataCite', 
    #     'schemeUri':'https://ror.org/' }], 'creatorName':
    #     { '__content__': 'Martin Fenner', 'nameType': 'Personal' },
    #     'familyName': 'Fenner', 'givenName': 'Martin', 'nameIdentifier': [
    #     { '__content__': 'http://orcid.org/0000-0003-1419-2405',
    #     'nameIdentifierScheme': 'ORCID', 'schemeUri': 'https://orcid.org' }] }]
    # without affiliation
    authors = [{ '@type': 'Person', '@id': 'http://orcid.org/0000-0003-1419-2405',
        'givenName': 'Martin', 'familyName': 'Fenner', 'name': 'Martin Fenner' }]
    response = from_schema_org_creators(authors)
    # assert response == [{ 'creatorName': { '__content__': 'Martin Fenner',
    #     'nameType': 'Personal' }, 'familyName': 'Fenner', 'givenName': 'Martin',
    #     'nameIdentifier': [{ '__content__': 'http://orcid.org/0000-0003-1419-2405',
    #      'nameIdentifierScheme': 'ORCID', 'schemeUri': 'https://orcid.org' }] }]

def test_pages_as_string():
    """pages as string"""
    container = {'firstPage': '2832', 'identifier': '0012-9658', 'identifierType': 'ISSN', 'issue': '11',
        'lastPage': '2841', 'title': 'Ecology', 'type': 'Journal', 'volume': '87'}
    assert '2832-2841' == pages_as_string(container)
    container = {'type': 'Journal', 'title': 'Publications',
        'firstPage': '15', 'issue': '2', 'volume': '6', 'identifier': '2304-6775',
        'identifierType': 'ISSN'}
    assert '15' == pages_as_string(container)
    assert None is pages_as_string(None)

def test_sanitize():
    """Sanitize HTML"""
    text = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    content = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term cool URIs'
    assert content == sanitize(text)

    text = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    content = 'In 1998 Tim Berners-Lee coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    assert content == sanitize(text, tags={'a'})


def test_crossref_api_url():
    """generate crossref api url"""
    doi = '10.5555/5412'
    url = 'https://api.crossref.org/works/10.5555/5412'
    assert url == crossref_api_url(doi)


def test_datacite_api_url():
    """generate datacite api url"""
    # doi
    doi = '10.5061/DRYAD.8515'
    response = datacite_api_url(doi)
    assert response == 'https://api.datacite.org/dois/10.5061/dryad.8515?include=media,client'
    # doi with protocol
    doi = 'doi:10.5061/DRYAD.8515'
    response = datacite_api_url(doi)
    assert response == 'https://api.datacite.org/dois/10.5061/dryad.8515?include=media,client'
    # https url
    doi = 'https://doi.org/10.5061/dryad.8515'
    response = datacite_api_url(doi)
    assert response == 'https://api.datacite.org/dois/10.5061/dryad.8515?include=media,client'
    # dx.doi.org url
    doi = 'http://dx.doi.org/10.5061/dryad.8515'
    response = datacite_api_url(doi)
    assert response == 'https://api.datacite.org/dois/10.5061/dryad.8515?include=media,client'
    # test resolver
    doi = 'https://handle.stage.datacite.org/10.5061/dryad.8515'
    response = datacite_api_url(doi)
    assert response == 'https://api.stage.datacite.org/dois/10.5061/dryad.8515?include=media,client'
    # test resolver http
    doi = 'http://handle.stage.datacite.org/10.5061/dryad.8515'
    response = datacite_api_url(doi)
    assert response == 'https://api.stage.datacite.org/dois/10.5061/dryad.8515?include=media,client'
    # force test resolver
    doi = 'https://doi.org/10.5061/dryad.8515'
    response = datacite_api_url(doi, sandbox=True)
    assert response == 'https://api.stage.datacite.org/dois/10.5061/dryad.8515?include=media,client'
