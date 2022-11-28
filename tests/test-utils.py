import pytest
from talbot import utils

def test_get_date_from_date_parts():
    "get_date_from_date_parts"
    assert "2012-01-01" == utils.get_date_from_date_parts({"date-parts": [[2012, 1, 1]]})
    assert '2012-01' == utils.get_date_from_date_parts({"date-parts": [[2012, 1]]})
    assert '2012' == utils.get_date_from_date_parts({"date-parts": [[2012]]})
    assert None == utils.get_date_from_date_parts({"date-parts": []})
    assert None == utils.get_date_from_date_parts({})

def test_get_date_from_parts():
    "get_date_from_parts"
    assert '2012-01-01' == utils.get_date_from_parts(2012, 1, 1)
    assert '2012-01' == utils.get_date_from_parts(2012, 1)
    assert '2012' == utils.get_date_from_parts(2012)
    assert None == utils.get_date_from_parts()

def test_dict_to_spdx_id():
    "dict_to_spdx id"
    assert { 'rights': 'Creative Commons Attribution 4.0 International',
             'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode', 
             'rightsIdentifier': 'cc-by-4.0', 'rightsIdentifierScheme': 'SPDX',
             'schemeUri': 'https://spdx.org/licenses/' } == utils.dict_to_spdx({ 'rightsIdentifier': 'cc-by-4.0' })

def test_dict_to_spdx_url():
    "dict_to_spdx url"
    assert { 'rights': 'Creative Commons Attribution 4.0 International',
             'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode', 
             'rightsIdentifier': 'cc-by-4.0', 'rightsIdentifierScheme': 'SPDX',
             'schemeUri': 'https://spdx.org/licenses/' } == utils.dict_to_spdx({ 'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode' })

def test_dict_to_spdx_not_found():
    "dict_to_spdx not found"
    assert { 'rightsURI': 'info:eu-repo/semantics/openAccess' } == utils.dict_to_spdx({ 'rightsURI': 'info:eu-repo/semantics/openAccess' })
