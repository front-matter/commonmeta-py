from __future__ import annotations

import importlib.metadata
import time

import click
import orjson as json

from commonmeta import Metadata, MetadataList  # __version__
from commonmeta.api_utils import update_ghost_post_via_api
from commonmeta.backend import (
    BACKEND_PYTHON_SUPPORTED,
    BackendError,
    require_backend,
)
from commonmeta.doi_utils import decode_doi, encode_doi, validate_prefix
from commonmeta.io_utils import get_extension, write_output, write_pdf


@click.group()
@click.option("--show-errors", default=False)
def cli(show_errors):
    if show_errors:
        click.echo("Show errors mode is on")


def main() -> None:
    """Console-script entry point for the ``commonmeta`` command.

    The commands split by what they work on. Converting and depositing a record
    - convert, put, push, encode, decode - are implemented here, so they work
    from a plain ``pip install commonmeta-py`` (e.g. InvenioRDM) with no native
    extension. Everything that works on the local commonmeta database - list,
    import, build, enrich, export, search, stats, match, migrate, settings,
    validate - belongs to commonmeta-rs and is forwarded to it verbatim, so its
    flags are documented and parsed in one place rather than described twice.
    """
    cli()


# What a filename is allowed to be called for each format, and what a name
# says the format is when --to is left out. A .json or .html could be several
# of them, so those say nothing.
OUTPUT_EXTENSIONS = {
    "bibtex": [".bib"],
    "citation": [".html"],
    "commonmeta": [".json"],
    "crossref": [".json"],
    "crossref_xml": [".xml"],
    "csl": [".json"],
    "datacite": [".json"],
    "inveniordm": [".json"],
    "orcid": [".json"],
    "pdf": [".pdf"],
    "ris": [".ris"],
    "ror": [".json"],
    "schema_org": [".json"],
}
FORMAT_EXTENSIONS = {
    ".bib": "bibtex",
    ".pdf": "pdf",
    ".ris": "ris",
    ".xml": "crossref_xml",
}


def format_from_output(output: str | None) -> str | None:
    """The format a --output filename names, where it names one on its own.

    `get_extension` looks past a compression suffix, so refs.bib.gz names
    bibtex as refs.bib does.
    """
    if not output:
        return None
    _, extension, _ = get_extension(output)
    return FORMAT_EXTENSIONS.get(extension.lower())


# Output formats that serialize to JSON and can be pretty-printed.
JSON_FORMATS = {
    "commonmeta",
    "crossref",
    "datacite",
    "inveniordm",
    "schema_org",
    "csl",
}


def echo_output(output, to: str) -> None:
    """Echo writer output, pretty-printing (2-space indent) JSON formats and
    leaving text/XML formats (bibtex, ris, citation, crossref_xml) untouched."""
    if output is None:
        return
    if to in JSON_FORMATS:
        try:
            output = json.dumps(json.loads(output), option=json.OPT_INDENT_2)
        except (ValueError, TypeError):
            pass
    click.echo(output)


@cli.command()
@click.argument("input", type=str, required=True)
@click.option("--from", "--via", "-f", "via", type=str, default=None)
@click.option(
    "--to",
    "-t",
    type=str,
    default=None,
    help="Output format [default: commonmeta, or what --output is named].",
)
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--doi", type=str)
@click.option("--prefix", type=str)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
@click.option(
    "--no-network",
    is_flag=True,
    default=False,
    help="Disable outbound network requests; fails if the input must be fetched",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False, writable=True),
    help="Write the output to this file instead of the terminal.",
)
@click.option("--show-errors/--no-errors", type=bool, show_default=True, default=False)
def convert(
    input,
    via,
    to,
    style,
    locale,
    doi,
    prefix,
    depositor,
    email,
    registrant,
    no_network,
    output,
    show_errors,
):
    # --no-network is enforced at fetch time inside Metadata: DOI/URL, ROR and
    # ORCID inputs can be served from the local SQLite store via the Rust
    # backend, so whether the network is needed depends on a store miss, not on
    # the input type. A miss under --no-network raises BackendError.
    try:
        metadata = Metadata(
            input, via=via, doi=doi, prefix=prefix, no_network=no_network
        )
    except BackendError as error:
        raise click.ClickException(str(error))
    if show_errors and not metadata.is_valid:
        raise click.ClickException(str(metadata.errors))

    to = to or format_from_output(output) or "commonmeta"

    if to == "pdf":
        # a pdf is bytes, so it is named rather than echoed
        if not output:
            raise click.ClickException(
                "--to pdf writes a file: name it with --output, e.g. -o post.pdf"
            )
        try:
            pdf = write_pdf(metadata, output)
        except (ValueError, OSError) as error:
            raise click.ClickException(str(error)) from error
        click.echo(f"Wrote {output} ({len(pdf)} bytes)")
        return

    result = metadata.write(
        to=to,
        style=style,
        locale=locale,
        depositor=depositor,
        email=email,
        registrant=registrant,
    )
    if output:
        try:
            write_output(output, result, OUTPUT_EXTENSIONS.get(to, [".json"]))
        except (ValueError, OSError) as error:
            raise click.ClickException(str(error)) from error
        click.echo(f"Wrote {output}")
    else:
        echo_output(result, to)
    if show_errors and metadata.write_errors:
        raise click.ClickException(str(metadata.write_errors))


@cli.command()
@click.argument("input", type=str, required=True)
@click.option("--from", "--via", "-f", "via", type=str, default=None)
@click.option("--to", "-t", type=str, default="commonmeta")
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--doi", type=str)
@click.option("--prefix", type=str)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
@click.option("--login-id", "--login_id", "login_id", type=str)
@click.option("--login-passwd", "--login_passwd", "login_passwd", type=str)
@click.option("--test-mode", "--test_mode", "test_mode", type=bool, default=False)
@click.option("--host", type=str)
@click.option("--token", type=str)
@click.option("--legacy-conn", type=str)
@click.option("--show-errors/--no-errors", type=bool, show_default=True, default=False)
def put(
    input,
    via,
    to,
    style,
    locale,
    doi,
    prefix,
    depositor,
    email,
    registrant,
    login_id,
    login_passwd,
    test_mode,
    host,
    token,
    legacy_conn,
    show_errors,
):
    metadata = Metadata(
        input,
        via=via,
        doi=doi,
        depositor=depositor,
        email=email,
        registrant=registrant,
        login_id=login_id,
        login_passwd=login_passwd,
        test_mode=test_mode,
        host=host,
        token=token,
        legacy_conn=legacy_conn,
        prefix=prefix,
    )
    if show_errors and not metadata.is_valid:
        raise click.ClickException(str(metadata.errors) + str(metadata.write_errors))

    click.echo(metadata.push(to=to, style=style, locale=locale))
    if show_errors and metadata.write_errors and len(metadata.write_errors) > 0:
        raise click.ClickException(str(metadata.write_errors))


@cli.command()
@click.argument("string", type=str, required=True)
@click.option("--from", "--via", "-f", "via", type=str)
@click.option("--to", "-t", type=str, default="commonmeta")
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--prefix", type=str)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
@click.option("--login-id", "--login_id", "login_id", type=str)
@click.option("--login-passwd", "--login_passwd", "login_passwd", type=str)
@click.option("--test-mode", "--test_mode", "test_mode", type=bool, default=False)
@click.option("--host", type=str)
@click.option("--token", type=str)
@click.option("--legacy-conn", type=str)
@click.option("--file", type=str)
@click.option("--show-errors/--no-errors", type=bool, show_default=True, default=False)
@click.option("--show-timer/--no-timer", type=bool, show_default=True, default=False)
def push(
    string,
    via,
    to,
    style,
    locale,
    prefix,
    depositor,
    email,
    registrant,
    login_id,
    login_passwd,
    test_mode,
    host,
    token,
    legacy_conn,
    file,
    show_errors,
    show_timer,
):
    start = time.time()
    metadata_list = MetadataList(
        string,
        via=via,
        file=file,
        depositor=depositor,
        email=email,
        registrant=registrant,
        login_id=login_id,
        login_passwd=login_passwd,
        test_mode=test_mode,
        host=host,
        token=token,
        legacy_conn=legacy_conn,
        prefix=prefix,
    )
    end = time.time()
    runtime = end - start
    if show_errors and not metadata_list.is_valid:
        raise click.ClickException(str(metadata_list.errors))

    click.echo(metadata_list.push(to=to, style=style, locale=locale))
    if show_errors and len(metadata_list.write_errors) > 0:
        raise click.ClickException(str(metadata_list.write_errors))
    if show_timer:
        click.echo(f"Runtime: {runtime:.2f} seconds")


@cli.command()
@click.argument("prefix", type=str, required=True)
def encode(prefix: str) -> None:
    if validate_prefix(prefix) is None:
        return None
    output = encode_doi(prefix)
    click.echo(output)


@cli.command()
@click.argument("doi", type=str, required=True)
def decode(doi: str) -> None:
    output = decode_doi(doi)
    click.echo(output)


@cli.command()
@click.argument("id", type=str, required=True)
@click.option("--api-key", "-k", type=str, required=True)
@click.option("--api-url", "-u", type=str, required=True)
def update_ghost_post(id: str, api_key: str, api_url: str) -> None:
    output = update_ghost_post_via_api(id, api_key, api_url)
    click.echo(output)


@cli.command()
def version() -> None:
    version = importlib.metadata.version("commonmeta-py")
    click.echo(f"commonmeta-py {version}")


# --- commands backed by the optional Rust backend (commonmeta-py[backend]) ---
# These are local-SQLite-database and bulk-import/validate features, implemented
# in commonmeta-rs and reached through its PyO3 module. Each forwards its
# arguments verbatim to the commonmeta-rs CLI, which is why they are declared
# with ignore_unknown_options/allow_extra_args: the flags are parsed on the Rust
# side, so this package doesn't duplicate (and drift from) their definitions.
# Without the extra installed they explain how to get it.

# add_help_option=False so `--help` reaches the Rust CLI too: it documents the
# flags these commands actually accept, in far more detail than a click stub
# could. Without it click intercepts --help and prints a docstring instead.
_PASSTHROUGH = dict(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    add_help_option=False,
)


def _run_backend_cli(command: str, args) -> None:
    """Forward a subcommand and its raw arguments to the commonmeta-rs CLI."""
    try:
        backend = require_backend()
        backend.run_cli(["commonmeta", command, *args])
    except BackendError as error:
        raise click.ClickException(str(error)) from error
    except ValueError as error:
        # run_cli raises ValueError on command failure; surface it as a CLI
        # error rather than a traceback.
        raise click.ClickException(str(error)) from error


def _backend_command(name: str, help_text: str) -> click.Command:
    """Build a click command that forwards `name` and its args to the Rust CLI."""

    @click.command(name=name, help=help_text, **_PASSTHROUGH)
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    def command(args) -> None:
        _run_backend_cli(name, args)

    return command


# Docstrings are deliberately short: `--help` reaches the Rust CLI, which
# documents each command's flags in full. These only describe the command for
# `commonmeta --help`.
build = _backend_command(
    "build", "Import records and then enrich the local commonmeta database."
)
enrich = _backend_command(
    "enrich",
    "Enrich the local commonmeta database from Crossref, DataCite, ROR, ORCID.",
)
export = _backend_command("export", "Write a VRAIX SQLite dump as a Parquet file.")
import_ = _backend_command(
    "import", "Import scholarly metadata into the local commonmeta database."
)
list_ = _backend_command(
    "list", "Convert or filter lists of scholarly metadata, from a file or the store."
)
match = _backend_command("match", "Match a string to an identifier.")
migrate = _backend_command("migrate", "Apply any pending database schema migrations.")
search = _backend_command(
    "search",
    "Search the local commonmeta database by name, identifier, or affiliation.",
)
settings = _backend_command(
    "settings", "Show key/value settings stored in the local SQLite database."
)
stats = _backend_command(
    "stats", "Show record counts for the tables of the local SQLite database."
)
validate = _backend_command(
    "validate",
    "Validate records in the local commonmeta database against the v1.0 schema.",
)

# Registered only where the backend can exist. commonmeta-rs requires Python
# 3.14 (abi3-py314), so below that these commands could never work: listing them
# would advertise a capability the interpreter cannot have. On 3.14+ they are
# always listed - the extra may not be installed yet, and then invoking one says
# how to install it. The commands are constructed unconditionally so importing
# them from this module works on any interpreter.
if BACKEND_PYTHON_SUPPORTED:
    for _command in (
        build,
        enrich,
        export,
        import_,
        list_,
        match,
        migrate,
        search,
        settings,
        stats,
        validate,
    ):
        cli.add_command(_command)


if __name__ == "__main__":
    cli()
