import pytest
from talbot import doi_utils

def test_doi_as_url():
    "doi_as_url"
    assert "https://doi.org/10.1371/journal.pone.0042793" == doi_utils.doi_as_url("10.1371/JOURNAL.PONE.0042793")
    assert None == doi_utils.doi_as_url(None)

def test_validate_prefix():
    "validate_prefix"
    assert "10.1371" == doi_utils.validate_prefix("10.1371/journal.pone.0042793")
    assert "10.1371" == doi_utils.validate_prefix("doi:10.1371/journal.pone.0042793")
    assert "10.1371" == doi_utils.validate_prefix("http://doi.org/10.1371/journal.pone.0042793")
    assert "10.1371" == doi_utils.validate_prefix("10.1371")

def test_get_doi_ra():
    "get_doi_ra"
    assert "Crossref" == doi_utils.get_doi_ra("10.1371/journal.pone.0042793")
    assert "DataCite" == doi_utils.get_doi_ra("https://doi.org/10.5061/dryad.8515")
    assert "mEDRA" == doi_utils.get_doi_ra("https://doi.org/10.1392/roma081203")
    assert "KISTI" == doi_utils.get_doi_ra("https://doi.org/10.5012/bkcs.2013.34.10.2889")
    assert "JaLC" == doi_utils.get_doi_ra("https://doi.org/10.11367/grsj1979.12.283")
    assert "OP" == doi_utils.get_doi_ra("https://doi.org/10.2903/j.efsa.2018.5239")
    # not a valid prefix
    assert None == doi_utils.get_doi_ra("https://doi.org/10.a/dryad.8515x")
    # not found
    assert None == doi_utils.get_doi_ra("https://doi.org/10.99999/dryad.8515x")
