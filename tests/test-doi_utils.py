import pytest
from talbot.doi_utils import doi_as_url, validate_doi, validate_prefix, get_doi_ra, doi_resolver

def test_doi_as_url():
    "doi_as_url"
    assert "https://doi.org/10.1371/journal.pone.0042793" == doi_as_url("10.1371/JOURNAL.PONE.0042793")
    assert None == doi_as_url(None)

def test_validate_doi():
    "validate_doi"
    assert "10.1371/journal.pone.0042793" == validate_doi("10.1371/journal.pone.0042793")

def test_validate_prefix():
    "validate_prefix"
    assert "10.1371" == validate_prefix("10.1371/journal.pone.0042793")
    assert "10.1371" == validate_prefix("doi:10.1371/journal.pone.0042793")
    assert "10.1371" == validate_prefix("http://doi.org/10.1371/journal.pone.0042793")
    assert "10.1371" == validate_prefix("10.1371")

def test_get_doi_ra():
    "get_doi_ra"
    assert "Crossref" == get_doi_ra("10.1371/journal.pone.0042793")
    assert "DataCite" == get_doi_ra("https://doi.org/10.5061/dryad.8515")
    assert "mEDRA" == get_doi_ra("https://doi.org/10.1392/roma081203")
    assert "KISTI" == get_doi_ra("https://doi.org/10.5012/bkcs.2013.34.10.2889")
    assert "JaLC" == get_doi_ra("https://doi.org/10.11367/grsj1979.12.283")
    assert "OP" == get_doi_ra("https://doi.org/10.2903/j.efsa.2018.5239")
    # not a valid prefix
    assert None == get_doi_ra("https://doi.org/10.a/dryad.8515x")
    # not found
    assert None == get_doi_ra("https://doi.org/10.99999/dryad.8515x")

def test_doi_resolver():
    "doi_resolver"
    assert 'https://doi.org/' == doi_resolver('10.5061/DRYAD.8515')
    # doi with protocol
    assert 'https://doi.org/' == doi_resolver('doi:10.5061/DRYAD.8515')
    # https url
    assert 'https://doi.org/' == doi_resolver('https://doi.org/10.5061/DRYAD.8515')
    # dx.doi.org url
    assert 'https://doi.org/' == doi_resolver('http://dx.doi.org/10.5061/DRYAD.8515')
    # datacite stage resolver
    assert 'https://handle.stage.datacite.org/' == doi_resolver('https://handle.stage.datacite.org/10.5061/dryad.8515')
    # datacite stage resolver http
    assert 'https://handle.stage.datacite.org/' == doi_resolver('http://handle.stage.datacite.org/10.5061/dryad.8515')
    # force datacite stage resolver
    assert 'https://handle.stage.datacite.org/' == doi_resolver('https://doi.org/10.5061/dryad.8515', sandbox=True)
