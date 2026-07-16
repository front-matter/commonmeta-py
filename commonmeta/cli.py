from __future__ import annotations

import importlib.metadata
import re
import time
from os import path

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
from commonmeta.readers.crossref_reader import get_random_crossref_id
from commonmeta.readers.datacite_reader import get_random_datacite_id
from commonmeta.readers.openalex_reader import get_random_openalex_id
from commonmeta.readers.vraix_reader import get_vraix_list
from commonmeta.utils import normalize_id


@click.group()
@click.option("--show-errors", default=False)
def cli(show_errors):
    if show_errors:
        click.echo("Show errors mode is on")


def format_from_file(file: str) -> str:
    """Infer the --to output format from a --file extension."""
    if file.endswith(".parquet") or file.endswith(".parquet.zst"):
        return "parquet"
    elif file.endswith(".zip"):
        return "zip"
    elif file.endswith(".tgz") or file.endswith(".tar.gz"):
        return "tgz"
    else:
        return "commonmeta"


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


def require_network(no_network: bool, action: str) -> None:
    """Reject an operation that needs the network when --no-network is set.

    Mirrors commonmeta-rs: operations on local files always succeed, but any
    step that would make an outbound request fails fast with a clear message.
    """
    if no_network:
        raise click.ClickException(
            f"{action} requires network access, but --no-network is set"
        )


def input_requires_network(value) -> bool:
    """A DOI/URL/identifier input must be fetched; a local file or inline
    string is read offline."""
    return isinstance(value, str) and normalize_id(value) is not None


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
@click.option(
    "--no-network",
    is_flag=True,
    default=False,
    help="Disable outbound network requests; fails if the input must be fetched",
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
    show_errors,
):
    if no_network and input_requires_network(input):
        require_network(no_network, "fetching the input record")
    metadata = Metadata(input, via=via, doi=doi, prefix=prefix)
    if show_errors and not metadata.is_valid:
        raise click.ClickException(str(metadata.errors))

    echo_output(
        metadata.write(
            to=to,
            style=style,
            locale=locale,
            depositor=depositor,
            email=email,
            registrant=registrant,
        ),
        to,
    )
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
@click.argument("string", type=str, required=False)
@click.option("--from", "--via", "-f", "via", type=str)
@click.option("--to", "-t", type=str, default=None)
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--prefix", type=str)
@click.option(
    "--number",
    "-n",
    type=int,
    default=10,
    help="Number of records to return with --sample",
)
@click.option(
    "--type",
    "item_type",
    type=str,
    help="Work type filter for --sample --from crossref",
)
@click.option(
    "--sample",
    "sample",
    is_flag=True,
    default=False,
    help="Return random works from --from (crossref, datacite, or openalex)",
)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
@click.option(
    "--date",
    type=str,
    help="VRAIX dump date, YYYY-MM-DD. Reads the --from (crossref/datacite) dump.",
)
@click.option(
    "--input-path",
    type=str,
    help="Local VRAIX SQLite dump, read instead of downloading.",
)
@click.option("--file", type=str)
@click.option(
    "--no-network",
    is_flag=True,
    default=False,
    help="Disable outbound network requests; fails if the operation needs one",
)
@click.option("--show-errors/--no-errors", type=bool, show_default=True, default=False)
@click.option("--show-timer/--no-timer", type=bool, show_default=True, default=False)
def list(
    string,
    via,
    to,
    style,
    locale,
    prefix,
    number,
    item_type,
    sample,
    depositor,
    email,
    registrant,
    date,
    input_path,
    file,
    no_network,
    show_errors,
    show_timer,
):
    start = time.time()
    list_kwargs = dict(
        file=file,
        depositor=depositor,
        email=email,
        registrant=registrant,
        prefix=prefix,
    )
    if sample:
        # random works from an API, e.g. `list --sample --from crossref -n 5`
        require_network(no_network, "--sample")
        provider = via or "crossref"
        if provider == "crossref":
            items = get_random_crossref_id(number, prefix=prefix, _type=item_type)
        elif provider == "datacite":
            items = get_random_datacite_id(number)
        elif provider == "openalex":
            items = get_random_openalex_id(number)
        else:
            raise click.ClickException(
                f"--sample is only supported for --from crossref, datacite, "
                f"or openalex (got {provider!r})"
            )
        metadata_list = MetadataList({"items": items}, via=provider, **list_kwargs)
    # VRAIX daily dump: `list --from crossref --date … ` (the --from value is the
    # source), matching commonmeta-rs. Also triggered by a local --input-path.
    elif date or input_path:
        if not input_path:
            require_network(no_network, "downloading a VRAIX dump")
        items = get_vraix_list(via, date, input_path=input_path)
        metadata_list = MetadataList({"items": items}, via="vraix", **list_kwargs)
    else:
        if input_requires_network(string):
            require_network(no_network, "fetching the input record")
        metadata_list = MetadataList(string, via=via, **list_kwargs)
    end = time.time()
    runtime = end - start
    if show_errors and not metadata_list.is_valid:
        raise click.ClickException(str(metadata_list.errors))
    if to is None:
        to = format_from_file(file) if file else "commonmeta"
    write_kwargs = {"style": style, "locale": locale}
    if to in ("zip", "tgz") and file:
        write_kwargs["base_name"] = re.sub(
            r"\.(zip|tgz|tar\.gz)$", "", path.basename(file)
        )
    if file:
        metadata_list.write(to=to, **write_kwargs)
    else:
        echo_output(metadata_list.write(to=to, **write_kwargs), to)

    if show_errors and len(metadata_list.write_errors) > 0:
        raise click.ClickException(str(metadata_list.write_errors))
    if show_timer:
        click.echo(f"Runtime: {runtime:.2f} seconds")


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
import_ = _backend_command(
    "import", "Import scholarly metadata into the local commonmeta database."
)
match = _backend_command("match", "Match a string to an identifier.")
migrate = _backend_command("migrate", "Apply any pending database schema migrations.")
settings = _backend_command(
    "settings", "Show key/value settings stored in the local SQLite database."
)
validate = _backend_command(
    "validate",
    "Validate records in the local commonmeta database against the v1.0 schema.",
)
package = _backend_command("package", "Write a VRAIX SQLite dump as a Parquet file.")

# Registered only where the backend can exist. commonmeta-rs requires Python
# 3.14 (abi3-py314), so below that these commands could never work: listing them
# would advertise a capability the interpreter cannot have. On 3.14+ they are
# always listed - the extra may not be installed yet, and then invoking one says
# how to install it. The commands are constructed unconditionally so importing
# them from this module works on any interpreter.
if BACKEND_PYTHON_SUPPORTED:
    for _command in (import_, match, migrate, settings, validate, package):
        cli.add_command(_command)


if __name__ == "__main__":
    cli()
