"""Test doi_utils module for commonmeta-py"""

from commonmeta.doi_utils import (
    doi_as_url,
    doi_from_url,
    validate_doi,
    normalize_doi,
    validate_prefix,
    validate_suffix,
    get_doi_ra,
    doi_resolver,
    crossref_api_url,
    crossref_api_query_url,
    datacite_api_url,
    is_rogue_scholar_doi,
    short_doi_as_doi,
)


def test_doi_as_url():
    "doi_as_url"
    assert "https://doi.org/10.1371/journal.pone.0042793" == doi_as_url(
        "10.1371/JOURNAL.PONE.0042793"
    )
    assert None is doi_as_url(None)


def test_doi_from_url():
    "doi_from_url"
    assert "10.5061/dryad.8515" == doi_from_url("https://doi.org/10.5061/dryad.8515")
    assert "10.5061/dryad.8515" == doi_from_url("10.5061/dryad.8515")
    assert "10.5067/terra+aqua/ceres/cldtyphist_l3.004" == doi_from_url(
        "10.5067/terra+aqua/ceres/cldtyphist_l3.004"
    )
    assert "10.1371/journal.pone.0042793" == doi_from_url(
        "doi:10.1371/journal.pone.0042793"
    )
    assert None is doi_from_url("https://doi.org/10.1371")
    assert None is doi_from_url(None)
    assert "10.5438/55e5-t5c0" == doi_from_url(
        "https://handle.stage.datacite.org/10.5438/55e5-t5c0"
    )
    assert "10.1002/ar.24923" == doi_from_url(
        "https://anatomypubs.onlinelibrary.wiley.com/doi/10.1002/ar.24923"
    )
    assert "10.1111/j.1469-185x.2011.00190.x" == doi_from_url(
        "https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1469-185x.2011.00190.x?casa_token=nmwsv4fd8awaaaaa%3afdas8pvfdobidbfbunhjmgyo6gombapj9ynq_oshepczbgdfptph33yz2zssg2_a79fejpinye4mkjp1"
    )
    assert "10.1111/j.1469-185x.2010.00137.x" == doi_from_url(
        "https://onlinelibrary.wiley.com/doi/10.1111/j.1469-185x.2010.00137.x/epdf"
    )
    assert "10.1371/journal.pone.0072187" == doi_from_url(
        "https://www.plosone.org/article/fetchobject.action?uri=info%3adoi%2f10.1371%2fjournal.pone.0072187&representation=pdf"
    )
    assert (
        "https://doi.org/10.1002/1521-3773(20000804)39:15%3C2756::AID-ANIE2756%3E3.0.CO;2-I"
        == doi_from_url("https://doi.org/d8g2nw")
    )


def test_short_doi_as_doi():
    """Short DOI as DOI"""
    assert (
        "https://doi.org/10.1002/1521-3773(20000804)39:15%3C2756::AID-ANIE2756%3E3.0.CO;2-I"
        == short_doi_as_doi("https://doi.org/d8g2nw")
    )


def test_validate_doi():
    "validate_doi"
    assert "10.1371/journal.pone.0042793" == validate_doi(
        "10.1371/journal.pone.0042793"
    )
    assert "10.1371/journal.pone.0042793" == validate_doi(
        "https://doi.org/10.1371/journal.pone.0042793"
    )


def test_normalize_doi():
    "normalize_doi"
    assert "https://doi.org/10.1371/journal.pone.0042793" == normalize_doi(
        "10.1371/journal.pone.0042793"
    )
    assert "https://doi.org/10.1371/journal.pone.0042793" == normalize_doi(
        "https://doi.org/10.1371/journal.pone.0042793"
    )
    assert "https://doi.org/10.1371/journal.pone.0042793" == normalize_doi(
        "doi:10.1371/journal.pone.0042793"
    )
    assert "https://doi.org/10.1021/jacs.4c02637" == normalize_doi(
        "http://dx.doi.org/10.1021/jacs.4c02637"
    )


def test_validate_prefix():
    "validate_prefix"
    assert "10.1371" == validate_prefix("10.1371/journal.pone.0042793")
    assert "10.1371" == validate_prefix("doi:10.1371/journal.pone.0042793")
    assert "10.1371" == validate_prefix("http://doi.org/10.1371/journal.pone.0042793")
    assert "10.1371" == validate_prefix("10.1371")


def test_validate_suffix():
    "validate_suffix"
    assert "journal.pone.0042793" == validate_suffix("10.1371/journal.pone.0042793")
    assert "journal.pone.0042793" == validate_suffix("doi:10.1371/journal.pone.0042793")
    assert "journal.pone.0042793" == validate_suffix("http://doi.org/10.1371/journal.pone.0042793")
    assert None is validate_suffix("10.1371")
    
    
def test_get_doi_ra():
    "get_doi_ra"
    assert "Crossref" == get_doi_ra("10.1371/journal.pone.0042793")
    assert "DataCite" == get_doi_ra("https://doi.org/10.5061/dryad.8515")
    assert "mEDRA" == get_doi_ra("https://doi.org/10.1392/roma081203")
    assert "KISTI" == get_doi_ra("https://doi.org/10.5012/bkcs.2013.34.10.2889")
    assert "JaLC" == get_doi_ra("https://doi.org/10.11367/grsj1979.12.283")
    assert "OP" == get_doi_ra("https://doi.org/10.2903/j.efsa.2018.5239")
    # not a valid prefix
    assert None is get_doi_ra("https://doi.org/10.a/dryad.8515x")
    # not found
    assert None is get_doi_ra("https://doi.org/10.99999/dryad.8515x")


def test_doi_resolver():
    "doi_resolver"
    assert "https://doi.org/" == doi_resolver("10.5061/DRYAD.8515")
    # doi with protocol
    assert "https://doi.org/" == doi_resolver("doi:10.5061/DRYAD.8515")
    # https url
    assert "https://doi.org/" == doi_resolver("https://doi.org/10.5061/DRYAD.8515")
    # dx.doi.org url
    assert "https://doi.org/" == doi_resolver("http://dx.doi.org/10.5061/DRYAD.8515")
    # datacite stage resolver
    assert "https://handle.stage.datacite.org/" == doi_resolver(
        "https://handle.stage.datacite.org/10.5061/dryad.8515"
    )
    # datacite stage resolver http
    assert "https://handle.stage.datacite.org/" == doi_resolver(
        "http://handle.stage.datacite.org/10.5061/dryad.8515"
    )
    # force datacite stage resolver
    assert "https://handle.stage.datacite.org/" == doi_resolver(
        "https://doi.org/10.5061/dryad.8515", sandbox=True
    )


def test_crossref_api_url():
    """generate crossref api url"""
    doi = "10.5555/5412"
    url = "https://api.crossref.org/works/10.5555/5412"
    assert url == crossref_api_url(doi)


def test_datacite_api_url():
    """generate datacite api url"""
    # doi
    doi = "10.5061/DRYAD.8515"
    response = datacite_api_url(doi)
    assert (
        response
        == "https://api.datacite.org/dois/10.5061/dryad.8515?include=media,client"
    )
    # doi with protocol
    doi = "doi:10.5061/DRYAD.8515"
    response = datacite_api_url(doi)
    assert (
        response
        == "https://api.datacite.org/dois/10.5061/dryad.8515?include=media,client"
    )
    # https url
    doi = "https://doi.org/10.5061/dryad.8515"
    response = datacite_api_url(doi)
    assert (
        response
        == "https://api.datacite.org/dois/10.5061/dryad.8515?include=media,client"
    )
    # dx.doi.org url
    doi = "http://dx.doi.org/10.5061/dryad.8515"
    response = datacite_api_url(doi)
    assert (
        response
        == "https://api.datacite.org/dois/10.5061/dryad.8515?include=media,client"
    )
    # test resolver
    doi = "https://handle.stage.datacite.org/10.5061/dryad.8515"
    response = datacite_api_url(doi)
    assert (
        response
        == "https://api.stage.datacite.org/dois/10.5061/dryad.8515?include=media,client"
    )
    # test resolver http
    doi = "http://handle.stage.datacite.org/10.5061/dryad.8515"
    response = datacite_api_url(doi)
    assert (
        response
        == "https://api.stage.datacite.org/dois/10.5061/dryad.8515?include=media,client"
    )
    # force test resolver
    doi = "https://doi.org/10.5061/dryad.8515"
    response = datacite_api_url(doi, sandbox=True)
    assert (
        response
        == "https://api.stage.datacite.org/dois/10.5061/dryad.8515?include=media,client"
    )


def test_is_rogue_scholar():
    """Check if doi is from Rogue Scholar"""
    assert True is is_rogue_scholar_doi("10.53731/cjx855h-hn5jtq8")
    assert False is is_rogue_scholar_doi("10.1371/journal.pone.0000030")


def test_crossref_api_query_url():
    """generate crossref api query url"""
    query = {"has-full-text": "true", "has-references": "true"}
    response = crossref_api_query_url(query)
    assert (
        response
        == "https://api.crossref.org/works?rows=20&filter=has-full-text%3Atrue%2Chas-references%3Atrue"
    )
    query = {"prefix": "10.5555", "type": "journal-article"}
    response = crossref_api_query_url(query)
    assert (
        response
        == "https://api.crossref.org/works?rows=20&filter=prefix%3A10.5555%2Ctype%3Ajournal-article"
    )
    query = {"member": "31795", "has-references": "true", "rows": 100}
    response = crossref_api_query_url(query)
    assert (
        response
        == "https://api.crossref.org/works?rows=100&filter=member%3A31795%2Chas-references%3Atrue"
    )
