"""Test doi_utils module for commonmeta-py"""

import re

import pytest

from commonmeta.doi_utils import (
    crossref_api_query_url,
    crossref_api_url,
    datacite_api_url,
    decode_doi,
    doi_as_url,
    doi_from_url,
    doi_resolver,
    encode_doi,
    generate_substack_doi,
    generate_wordpress_doi,
    get_doi_ra,
    is_rogue_scholar_doi,
    normalize_doi,
    short_doi_as_doi,
    validate_doi,
    validate_doi_from_guid,
    validate_prefix,
    validate_suffix,
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
    assert None is doi_from_url("https://doi.org/")
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
    # a short DOI gives the DOI it resolves to, as doi_from_url finds it in
    # the resolved URL
    assert (
        "10.1002/1521-3773(20000804)39:15%3c2756::aid-anie2756%3e3.0.co;2-i"
        == doi_from_url("https://doi.org/d8g2nw")
    )
    assert doi_from_url("https://doi.org/d8g2nw") == doi_from_url(
        "https://doi.org/10/d8g2nw"
    )


@pytest.mark.parametrize(
    "url,doi",
    [
        pytest.param(
            "https://doi.org/https://doi.org/10.31223/X58H9G",
            "10.31223/x58h9g",
            id="doi url inside a doi url",
        ),
        pytest.param(
            "https://doi.org/https://doi.org/10.48550/arXiv.1706.03762",
            "10.48550/arxiv.1706.03762",
            id="arxiv doi inside a doi url",
        ),
        pytest.param("https://doi.org/abc-def", None, id="not a short doi"),
    ],
)
def test_doi_from_url_is_not_fooled_by_paths_that_look_like_short_dois(url, doi):
    """A doi.org path that is not a short DOI isn't resolved as one.

    A blog post linking https://doi.org/https://doi.org/10.31223/X58H9G gave
    the whole URL back as the DOI, and the Crossref deposit failed its schema.
    """
    assert doi_from_url(url) == doi


def test_short_doi_as_doi():
    """Short DOI as DOI"""
    assert (
        "https://doi.org/10.1002/1521-3773(20000804)39:15%3C2756::AID-ANIE2756%3E3.0.CO;2-I"
        == short_doi_as_doi("https://doi.org/d8g2nw")
    )
    assert None is short_doi_as_doi("https://doi.org/")


def test_validate_doi():
    "validate_doi"
    assert "10.1371/journal.pone.0042793" == validate_doi(
        "10.1371/journal.pone.0042793"
    )
    assert "10.1371/journal.pone.0042793" == validate_doi(
        "https://doi.org/10.1371/journal.pone.0042793"
    )
    assert None is validate_doi("https://doi.org/20.1371/journal.pone.0042793")


def test_validate_doi_from_guid():
    "validate doi from guid"
    prefix = "10.59350"
    guid = "https://doi.org/10.59350/yb098-wm38"
    assert validate_doi_from_guid(prefix, guid, checksum=True)
    # ignore checksum
    assert validate_doi_from_guid(prefix, guid[:-2], checksum=False)


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
    assert "journal.pone.0042793" == validate_suffix(
        "http://doi.org/10.1371/journal.pone.0042793"
    )
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


def test_decode_doi():
    """Decode base32-encoded DOI"""
    # doi without checksum
    doi = "10.5555/f9zqn-sf065"
    response = decode_doi(doi, checksum=False)
    assert response == 538751765283013
    # doi with checksum
    doi = "10.54900/ka4bq-90315"
    response = decode_doi(doi, checksum=True)
    assert response == 663718962179
    # doi with wrong checksum
    doi = "10.54900/d3ck1-skq20"
    response = decode_doi(doi, checksum=True)
    assert response == 0
    # doi expressed as url
    doi = "https://doi.org/10.54900/b8pcg-q9k70"
    response = decode_doi(doi)
    assert response == 387298385203
    # doi not base32-encoded
    doi = "10.1371/journal.pone.0042793"
    response = decode_doi(doi)
    assert response == 0


@pytest.mark.parametrize(
    ("number", "doi"),
    [
        pytest.param(2**40, "https://doi.org/10.5555/10000-00008-7", id="2**40"),
        pytest.param(2**45 - 1, "https://doi.org/10.5555/zzzzz-zzzz4-0", id="2**45-1"),
        pytest.param(2**65, "https://doi.org/10.5555/10000-00000-00002-3", id="2**65"),
    ],
)
def test_decode_doi_with_a_split_checksum(number, doi):
    """A checksum split by a hyphen still decodes, and validates as a guid."""
    assert encode_doi("10.5555", number) == doi
    assert decode_doi(doi) == number
    assert validate_doi_from_guid("10.5555", doi)


def test_encode_doi_with_number():
    """Generate a random DOI with preset number"""
    response = encode_doi("10.5555", number=123456789012)
    assert response == "https://doi.org/10.5555/3jz9j-6gm44"


@pytest.mark.parametrize(
    ("number", "doi"),
    [
        pytest.param(214901993, "https://doi.org/10.59350/006cy-97960", id="substack"),
        pytest.param(1, "https://doi.org/10.59350/00000-00195", id="one"),
        pytest.param(
            123456789012, "https://doi.org/10.59350/3jz9j-6gm44", id="ten-already"
        ),
    ],
)
def test_encode_doi_with_number_pads_to_ten_characters(number, doi):
    """A small number is padded to the form a random suffix has, and still
    decodes back to itself with a checksum that holds."""
    assert encode_doi("10.59350", number) == doi
    assert decode_doi(doi) == number
    assert validate_doi_from_guid("10.59350", doi)


def test_encode_doi_random_suffix_has_ten_characters():
    """A random suffix is padded too: one in 32 random numbers is short."""
    for _ in range(2000):
        assert re.fullmatch(
            r"https://doi\.org/10\.5555/[0-9a-z]{5}-[0-9a-z]{5}", encode_doi("10.5555")
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


def test_generate_wordpress_doi():
    """Generate a WordPress DOI"""
    response = generate_wordpress_doi(
        prefix="10.5555",
        slug="pkp",
        guid="https://sfupkp.dev.affinitybridge.com/?p=1456",
    )
    assert response == "https://doi.org/10.5555/pkp.1456"

    # No post_id in guid
    response = generate_wordpress_doi(
        prefix="10.5555",
        slug="pkp",
        guid="https://sfupkp.dev.affinitybridge.com/2022/11/04/world-digital-preservation-day-2022-using-pkp-pn-to-keep-journals-data-for-all-for-good-forever/",
    )
    assert response.startswith("https://doi.org/10.5555/")


def test_generate_substack_doi():
    """Generate a Substack DOI"""
    response = generate_substack_doi(
        prefix="10.5555", slug="stephenturner", guid="167348334"
    )
    assert response == "https://doi.org/10.5555/stephenturner.167348334"


# The same cases as commonmeta-rs' test_normalize_doi_parity_cases (doi_utils.rs).
@pytest.mark.parametrize(
    "doi,expected",
    [
        ("10.5555/ABC", "https://doi.org/10.5555/abc"),
        ("doi:10.5555/abc", "https://doi.org/10.5555/abc"),
        ("http://doi.org/10.5555/abc", "https://doi.org/10.5555/abc"),
        ("https://dx.doi.org/10.5555/abc", "https://doi.org/10.5555/abc"),
        ("https://commonmeta.org/10.5555/abc", "https://doi.org/10.5555/abc"),
        (
            "https://handle.stage.datacite.org/10.5555/ABC",
            "https://handle.stage.datacite.org/10.5555/abc",
        ),
        (
            "10.1890/0012-9658(2006)87[2832:TIOPMA]2.0.CO;2",
            "https://doi.org/10.1890/0012-9658(2006)87%5B2832:tiopma%5D2.0.co;2",
        ),
        (
            "https://doi.org/10.1890/0012-9658(2006)87%5b2832:tiopma%5D2.0.co;2",
            "https://doi.org/10.1890/0012-9658(2006)87%5B2832:tiopma%5D2.0.co;2",
        ),
        (
            "doi:10.1206/0003-0090(2003)277<0001:TSSAAA>2.0.CO;2",
            "https://doi.org/10.1206/0003-0090(2003)277%3C0001:tssaaa%3E2.0.co;2",
        ),
        ("10.5555/a b", None),
        ("10.555/abc", None),
        ("https://example.org/10.5555/abc", None),
        ("", None),
    ],
)
def test_normalize_doi_parity_cases(doi, expected):
    assert normalize_doi(doi) == expected
