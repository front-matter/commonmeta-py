import pytest
from talbot import utils
from talbot.utils import parse_attributes, get_date_from_date_parts, get_date_from_parts, dict_to_spdx, normalize_orcid, validate_orcid, wrap, unwrap, compact, from_citeproc, presence

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
    assert { 'rightsURI': 'info:eu-repo/semantics/openAccess' } == dict_to_spdx({ 'rightsURI': 'info:eu-repo/semantics/openAccess' })

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

def test_from_citeproc():
    "from_citeproc"
    assert [{'@type': 'Person', 'affiliation': [{'name': 'Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland'}],
        'familyName': 'Sankar', 'givenName': 'Martial', 'name': 'Martial Sankar'}] == from_citeproc([{"given": "Martial", "family": "Sankar", "sequence": "first", "affiliation": [{"name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"}]}])
