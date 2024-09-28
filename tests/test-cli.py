"""Test cli"""
import pytest
from click.testing import CliRunner
from commonmeta.cli import convert, encode, decode, json_feed, encode_by_id


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
        "1. Sankar M, Nieminen K, Ragni L, Xenarios I, Hardtke CS. Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth. eLife [Internet]. 2014Feb11;3. Available from: https://elifesciences.org/articles/01567"
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
def test_convert_crossref_xml_from_json_feed():
    """Test crossref_xml generation from json_feed"""
    runner = CliRunner()
    string = "https://api.rogue-scholar.org/posts/d0ca6fa3-3a93-46d3-b820-446938d78f70"
    result = runner.invoke(convert, [string, "--to", "crossref_xml"])
    assert result.exit_code == 0
    assert (
        "<title>CommonMark and the Future of Scholarly Markdown</title>"
        in result.output
    )


@pytest.mark.vcr
def test_convert_datacite_from_json_feed():
    """Test datacite generation from json_feed"""
    runner = CliRunner()
    string = "https://api.rogue-scholar.org/posts/d0ca6fa3-3a93-46d3-b820-446938d78f70"
    result = runner.invoke(convert, [string, "--to", "datacite"])
    assert result.exit_code == 0
    assert "CommonMark and the Future of Scholarly Markdown" in result.output


@pytest.mark.vcr
def test_convert_commonmeta_from_json_feed_no_doi():
    """Test commonmeta generation from json_feed no doi"""
    runner = CliRunner()
    string = "https://api.rogue-scholar.org/posts/a8a84260-1f16-444c-8e70-2cb6702611a0"
    result = runner.invoke(convert, [string, "--prefix", "10.5555"])
    assert result.exit_code == 0
    assert "https://doi.org/10.5555/" in result.output


@pytest.mark.vcr
def test_convert_crossref_xml_from_json_feed_no_doi():
    """Test crossref_xml generation from json_feed no doi"""
    runner = CliRunner()
    string = "https://api.rogue-scholar.org/posts/a8a84260-1f16-444c-8e70-2cb6702611a0"
    result = runner.invoke(
        convert, [string, "--to", "crossref_xml", "--prefix", "10.5555"]
    )
    assert result.exit_code == 0
    assert "<doi>10.5555/" in result.output


@pytest.mark.vcr
def test_json_feed_blog_slug():
    """Test json_feed blog_slug"""
    runner = CliRunner()
    string = "blog_slug"
    result = runner.invoke(
        json_feed, [string, "--id", "6603f220-1683-4366-8663-c4284e9f9a78"]
    )
    assert result.exit_code == 0
    assert "libreas" in result.output


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
    assert "1053628090261604" in result.output


@pytest.mark.vcr
def test_encode_by_id():
    """Test encode by id"""
    runner = CliRunner()
    string = "d0ca6fa3-3a93-46d3-b820-446938d78f70"
    result = runner.invoke(encode_by_id, [string])
    assert result.exit_code == 0
    assert "https://doi.org/10.53731/" in result.output
