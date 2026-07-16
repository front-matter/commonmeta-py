"""Test cli"""

from os import path
from types import SimpleNamespace

import pytest
from click.testing import CliRunner

from commonmeta.backend import INSTALL_HINT, BackendError
from commonmeta.cli import (
    convert,
    decode,
    encode,
    import_,
    list,
    match,
    migrate,
    package,
    put,
    settings,
    validate,
)

FIXTURES = path.join(path.dirname(__file__), "fixtures")


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
    assert '"schemaVersion": "http://datacite.org/schema/kernel-4"' in result.output


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
    string = path.join(path.dirname(__file__), "fixtures", "posts.json")
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


@pytest.mark.parametrize(
    "command,name",
    [
        (import_, "import"),
        (match, "match"),
        (migrate, "migrate"),
        (settings, "settings"),
        (validate, "validate"),
        (package, "package"),
    ],
    ids=lambda c: c if isinstance(c, str) else c.name,
)
def test_backend_commands_forward_to_rust(command, name, monkeypatch):
    """Backend commands forward their subcommand and raw arguments to the
    commonmeta-rs CLI, which parses the flags. `run_cli` is stubbed here because
    the real one would import a corpus; the contract under test is the handoff."""
    calls = []
    backend = SimpleNamespace(run_cli=calls.append)
    monkeypatch.setattr("commonmeta.cli.require_backend", lambda: backend)

    runner = CliRunner()
    result = runner.invoke(command, ["some-input", "--from", "crossref", "-n", "5"])
    assert result.exit_code == 0
    assert calls == [
        ["commonmeta", name, "some-input", "--from", "crossref", "-n", "5"]
    ]


def test_backend_command_without_backend(monkeypatch):
    """Without the optional extra installed, the command says how to install it
    rather than failing with a traceback."""

    def missing():
        raise BackendError(INSTALL_HINT)

    monkeypatch.setattr("commonmeta.cli.require_backend", missing)
    runner = CliRunner()
    result = runner.invoke(import_, ["10.5555/12345678"])
    assert result.exit_code != 0
    assert "commonmeta-py[backend]" in result.output


def test_backend_command_reports_failure(monkeypatch):
    """A failure inside the Rust CLI surfaces as a CLI error, not a traceback."""

    def boom(args):
        raise ValueError("import: no such file 'nope.sqlite3'")

    monkeypatch.setattr(
        "commonmeta.cli.require_backend", lambda: SimpleNamespace(run_cli=boom)
    )
    runner = CliRunner()
    result = runner.invoke(import_, ["nope.sqlite3"])
    assert result.exit_code != 0
    assert "no such file" in result.output


@pytest.mark.parametrize("flag", ["--from", "-f", "--via"])
def test_convert_from_aliases(flag):
    """--from, -f and the --via back-compat alias all set the input format."""
    runner = CliRunner()
    fixture = path.join(FIXTURES, "inveniordm-software.json")
    result = runner.invoke(convert, [fixture, flag, "inveniordm", "--to", "commonmeta"])
    assert result.exit_code == 0
    assert '"type": "Software"' in result.output


def test_convert_pretty_prints_json():
    """JSON output is pretty-printed (2-space indent)."""
    runner = CliRunner()
    fixture = path.join(FIXTURES, "inveniordm-software.json")
    result = runner.invoke(convert, [fixture, "-f", "inveniordm"])
    assert result.exit_code == 0
    assert '\n  "type": "Software"' in result.output


def test_put_accepts_dashed_option_aliases():
    """put exposes the commonmeta-rs dashed option names (and old aliases)."""
    runner = CliRunner()
    help_text = runner.invoke(put, ["--help"]).output
    for option in ("--login-id", "--login-passwd", "--test-mode", "--from"):
        assert option in help_text


def test_convert_no_network_rejects_doi():
    """--no-network fails fast when the input (a DOI) would need fetching."""
    runner = CliRunner()
    result = runner.invoke(convert, ["10.7554/elife.01567", "--no-network"])
    assert result.exit_code == 1
    assert "requires network access" in result.output


def test_convert_no_network_allows_local_file():
    """--no-network still converts a local file (no request needed)."""
    runner = CliRunner()
    fixture = path.join(FIXTURES, "inveniordm-software.json")
    result = runner.invoke(
        convert, [fixture, "-f", "inveniordm", "--to", "bibtex", "--no-network"]
    )
    assert result.exit_code == 0
    assert "@misc{10.5281/zenodo.7752775" in result.output


def test_list_sample_option_present():
    """list gained the --sample flag (replacing the removed sample command)."""
    runner = CliRunner()
    help_text = runner.invoke(list, ["--help"]).output
    assert "--sample" in help_text
    assert "--number" in help_text


def test_list_sample_no_network_rejects():
    """list --sample needs an API, so --no-network fails fast."""
    runner = CliRunner()
    result = runner.invoke(list, ["--sample", "--from", "crossref", "--no-network"])
    assert result.exit_code == 1
    assert "requires network access" in result.output
