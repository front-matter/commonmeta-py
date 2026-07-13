"""Test cli"""

import pytest
from click.testing import CliRunner

from commonmeta.cli import convert, decode, encode, list


@pytest.fixture(scope="module")
def vcr_config():
    return {"record_mode": "new_episodes"}


@pytest.mark.vcr
def test_convert():
    """Test commonmeta generation"""
    runner = CliRunner()
    string = "10.7554/elife.01567"
    result = runner.invoke(convert, [string])
    assert result.exit_code == 0
    assert "JournalArticle" in result.output


@pytest.mark.vcr
def test_convert_show_error():
    """Test commonmeta generation"""
    runner = CliRunner()
    string = "10.7600"
    result = runner.invoke(convert, [string, "--show-errors"])
    assert result.exit_code == 1
    assert "" in result.output


@pytest.mark.vcr
def test_convert_crossref_xml():
    """Test crossref_xml generation"""
    runner = CliRunner()
    string = "10.7554/elife.01567"
    result = runner.invoke(convert, [string, "--to", "crossref_xml"])
    assert result.exit_code == 0
    assert (
        "<title>Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth</title>"
        in result.output
    )


@pytest.mark.vcr
def test_convert_citation():
    """Test citation generation"""
    runner = CliRunner()
    string = "10.7554/elife.01567"
    result = runner.invoke(
        convert, [string, "--to", "citation", "--style", "vancouver"]
    )
    assert result.exit_code == 0
    assert (
        "Error: citation not available for style vancouver and locale en-US."
        in result.output
    )


@pytest.mark.vcr
def test_convert_datacite():
    """Test datacite generation"""
    runner = CliRunner()
    string = "10.7554/elife.01567"
    result = runner.invoke(convert, [string, "--to", "datacite"])
    assert result.exit_code == 0
    assert "https://elifesciences.org/articles/01567" in result.output


@pytest.mark.vcr
def test_convert_crossref_xml_from_jsonfeed():
    """Test crossref_xml generation from jsonfeed"""
    runner = CliRunner()
    string = "https://api.rogue-scholar.org/posts/10.59350/50ebs-4zq55"
    result = runner.invoke(convert, [string, "--to", "crossref_xml"])
    assert result.exit_code == 0
    assert "<doi>10.59350/50ebs-4zq55</doi>" in result.output


@pytest.mark.vcr
def test_convert_datacite_from_jsonfeed():
    """Test datacite generation from jsonfeed"""
    runner = CliRunner()
    string = "https://api.rogue-scholar.org/posts/10.59350/50ebs-4zq55"
    result = runner.invoke(convert, [string, "--to", "datacite"])
    assert result.exit_code == 0
    assert '"schemaVersion":"http://datacite.org/schema/kernel-4"' in result.output


@pytest.mark.vcr
def test_convert_crossref_xml_from_jsonfeed_no_doi():
    """Test crossref_xml generation from jsonfeed no doi"""
    runner = CliRunner()
    string = "https://api.rogue-scholar.org/posts/10.59350/50ebs-4zq55"
    result = runner.invoke(
        convert, [string, "--to", "crossref_xml", "--prefix", "10.59350"]
    )
    assert result.exit_code == 0
    assert "<doi>10.59350/50ebs-4zq55</doi>" in result.output


@pytest.mark.vcr
def test_list():
    """Test commonmeta list"""
    runner = CliRunner()
    string = "posts.json"
    result = runner.invoke(list, [string])
    assert result.exit_code == 0
    # assert 2 == len(result.output)


def test_encode():
    """Test encode"""
    runner = CliRunner()
    string = "10.5555"
    result = runner.invoke(encode, [string])
    assert result.exit_code == 0
    assert "https://doi.org/10.5555/" in result.output


def test_decode():
    """Test encode"""
    runner = CliRunner()
    string = "https://doi.org/10.5555/xy8km-0q834"
    result = runner.invoke(decode, [string])
    assert result.exit_code == 0
    assert "1028933681896\n" in result.output
