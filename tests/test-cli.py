"""Test cli"""

from os import path
from types import SimpleNamespace

import pytest
from click.testing import CliRunner

from commonmeta.backend import INSTALL_HINT, BackendError
from commonmeta.cli import (
    build,
    convert,
    decode,
    encode,
    enrich,
    export,
    import_,
    list_,
    match,
    migrate,
    put,
    search,
    settings,
    stats,
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


def test_list_is_the_rust_one(monkeypatch):
    """list works on the local store, and belongs to commonmeta-rs with it.

    Its filters - by member, client, year, orcid, ror, cited-by, the has-* set
    - are parsed there rather than described twice, so the input and the flags
    go over verbatim.
    """
    calls = []
    monkeypatch.setattr(
        "commonmeta.cli.require_backend",
        lambda: SimpleNamespace(run_cli=calls.append),
    )
    string = path.join(path.dirname(__file__), "fixtures", "crossref-list.json")

    result = CliRunner().invoke(list_, [string, "--from", "crossref", "--has-orcid"])

    assert result.exit_code == 0
    assert calls == [
        ["commonmeta", "list", string, "--from", "crossref", "--has-orcid"]
    ]


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
        (build, "build"),
        (enrich, "enrich"),
        (export, "export"),
        (import_, "import"),
        (list_, "list"),
        (match, "match"),
        (migrate, "migrate"),
        (search, "search"),
        (settings, "settings"),
        (stats, "stats"),
        (validate, "validate"),
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


def test_the_cli_is_the_python_one(monkeypatch):
    """The entry point runs these commands rather than handing them all over.

    convert, put, push, encode and decode are implemented here, so they work
    from a plain install with no native extension; the store commands are
    forwarded, and that is the whole of what commonmeta-rs is asked to do.
    """
    from commonmeta import cli as cli_module

    ran = []
    monkeypatch.setattr(cli_module, "cli", lambda: ran.append("python"))
    monkeypatch.setattr(
        "commonmeta.cli.require_backend",
        lambda: pytest.fail("the entry point handed the command to the backend"),
    )

    cli_module.main()

    assert ran == ["python"]


@pytest.mark.vcr
def test_convert_to_pdf(tmp_path, weasyprint, feature_image):
    """convert -t pdf writes the rendition of a post to a file."""
    from commonmeta.io_utils import read_pdf_metadata

    runner = CliRunner()
    output = tmp_path / "post.pdf"

    result = runner.invoke(
        convert,
        [
            "https://rogue-scholar.org/api/records/e1ndf-19s62",
            "--from",
            "inveniordm",
            "--to",
            "pdf",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output
    assert f"Wrote {output}" in result.output
    metadata = read_pdf_metadata(output.read_bytes())
    assert metadata["title"] == "Ten simple rules for scholarly blogging"
    assert metadata["variant"] == "PDF/A-3a"


@pytest.mark.vcr
def test_convert_to_pdf_needs_a_filename():
    """A pdf is bytes, so it is named rather than echoed."""
    runner = CliRunner()

    result = runner.invoke(convert, ["10.7554/elife.01567", "--to", "pdf"])

    assert result.exit_code == 1
    assert "name it with --output" in result.output


@pytest.mark.vcr
def test_convert_to_pdf_without_post_content(tmp_path, weasyprint, feature_image):
    """Any input writes a pdf; one without html writes the title page alone."""
    from commonmeta.io_utils import read_pdf_metadata

    runner = CliRunner()
    output = tmp_path / "article.pdf"

    result = runner.invoke(
        convert, ["10.7554/elife.01567", "--to", "pdf", "--output", str(output)]
    )

    assert result.exit_code == 0, result.output
    metadata = read_pdf_metadata(output.read_bytes())
    assert metadata["title"].startswith("Automated quantitative histology")
    assert metadata["authors"][0] == "Martial Sankar"
    assert "attachments" not in metadata


def test_convert_output_is_for_pdf(tmp_path):
    """Every other format goes to the terminal, and the shell can redirect it."""
    runner = CliRunner()

    result = runner.invoke(
        convert,
        ["10.7554/elife.01567", "--to", "bibtex", "--output", str(tmp_path / "x.bib")],
    )

    assert result.exit_code == 1
    assert "--output is for --to pdf" in result.output


def test_pdf_is_not_a_metadata_format():
    """A pdf is a rendering of a record, not a format a record converts to.

    The CLI writes one; `Metadata.write` produces metadata formats and does
    not know it.
    """
    from commonmeta import Metadata

    with pytest.raises(ValueError, match="Unsupported output format: pdf"):
        Metadata("10.5281/zenodo.5244404", via="datacite").write(to="pdf")


def test_convert_to_pdf_reports_a_render_it_cannot_make(tmp_path, monkeypatch):
    """What io_utils raises, the cli says; it does not traceback."""
    from commonmeta import cli as cli_module

    def unavailable(metadata, file):
        raise ValueError(
            "Could not render the pdf. WeasyPrint needs the pango libraries"
        )

    monkeypatch.setattr(cli_module, "write_pdf", unavailable)

    result = CliRunner().invoke(
        convert,
        ["10.7554/elife.01567", "--to", "pdf", "--output", str(tmp_path / "x.pdf")],
    )

    assert result.exit_code == 1
    assert "needs the pango libraries" in result.output
