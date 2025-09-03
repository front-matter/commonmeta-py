import importlib.metadata
import time

import click
import orjson as json

from commonmeta import Metadata, MetadataList  # __version__
from commonmeta.api_utils import update_ghost_post_via_api
from commonmeta.doi_utils import decode_doi, encode_doi, validate_prefix
from commonmeta.readers.crossref_reader import get_random_crossref_id
from commonmeta.readers.datacite_reader import get_random_datacite_id
from commonmeta.readers.openalex_reader import get_random_openalex_id


@click.group()
@click.option("--show-errors", default=False)
def cli(show_errors):
    if show_errors:
        click.echo("Show errors mode is on")


@cli.command()
@click.argument("input", type=str, required=True)
@click.option("--via", "-f", type=str, default=None)
@click.option("--to", "-t", type=str, default="commonmeta")
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--doi", type=str)
@click.option("--prefix", type=str)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
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
    show_errors,
):
    metadata = Metadata(input, via=via, doi=doi, prefix=prefix)
    if show_errors and not metadata.is_valid:
        raise click.ClickException(str(metadata.errors))

    click.echo(
        metadata.write(
            to=to,
            style=style,
            locale=locale,
            depositor=depositor,
            email=email,
            registrant=registrant,
        )
    )
    if show_errors and metadata.write_errors:
        raise click.ClickException(str(metadata.write_errors))


@cli.command()
@click.argument("input", type=str, required=True)
@click.option("--via", "-f", type=str, default=None)
@click.option("--to", "-t", type=str, default="commonmeta")
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--doi", type=str)
@click.option("--prefix", type=str)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
@click.option("--login_id", type=str)
@click.option("--login_passwd", type=str)
@click.option("--test_mode", type=bool, default=False)
@click.option("--host", type=str)
@click.option("--token", type=str)
@click.option("--legacy-key", type=str)
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
    legacy_key,
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
        legacy_key=legacy_key,
        prefix=prefix,
    )
    if show_errors and not metadata.is_valid:
        raise click.ClickException(str(metadata.errors) + str(metadata.write_errors))

    click.echo(metadata.push(to=to, style=style, locale=locale))
    if show_errors and len(metadata.write_errors) > 0:
        raise click.ClickException(str(metadata.write_errors))


@cli.command()
@click.argument("string", type=str, required=True)
@click.option("--via", "-f", type=str)
@click.option("--to", "-t", type=str, default="commonmeta")
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--prefix", type=str)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
@click.option("--file", type=str)
@click.option("--show-errors/--no-errors", type=bool, show_default=True, default=False)
@click.option("--show-timer/--no-timer", type=bool, show_default=True, default=False)
def list(
    string,
    via,
    to,
    style,
    locale,
    prefix,
    depositor,
    email,
    registrant,
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
        prefix=prefix,
    )
    end = time.time()
    runtime = end - start
    if show_errors and not metadata_list.is_valid:
        raise click.ClickException(str(metadata_list.errors))
    if file:
        metadata_list.write(to=to, style=style, locale=locale)
    else:
        click.echo(metadata_list.write(to=to, style=style, locale=locale))

    if show_errors and len(metadata_list.write_errors) > 0:
        raise click.ClickException(str(metadata_list.write_errors))
    if show_timer:
        click.echo(f"Runtime: {runtime:.2f} seconds")


@cli.command()
@click.argument("string", type=str, required=True)
@click.option("--via", "-f", type=str)
@click.option("--to", "-t", type=str, default="commonmeta")
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--prefix", type=str)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
@click.option("--login_id", type=str)
@click.option("--login_passwd", type=str)
@click.option("--test_mode", type=bool, default=False)
@click.option("--host", type=str)
@click.option("--token", type=str)
@click.option("--legacy-key", type=str)
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
    legacy_key,
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
        legacy_key=legacy_key,
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
@click.option("--provider", type=str, default="crossref")
@click.option("--prefix", type=str)
@click.option("--type", type=str)
@click.option("--number", "-n", type=int, default=1)
@click.option("--to", "-t", type=str, default="commonmeta")
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--show-errors/--no-errors", type=bool, show_default=True, default=False)
def sample(provider, prefix, type, number, to, style, locale, show_errors):
    if provider == "crossref":
        string = json.dumps(
            {"items": get_random_crossref_id(number, prefix=prefix, _type=type)}
        )
    elif provider == "datacite":
        string = json.dumps({"items": get_random_datacite_id(number)})
    elif provider == "openalex":
        string = json.dumps({"items": get_random_openalex_id(number)})
    else:
        output = "Provider not supported. Use 'crossref' or 'datacite' instead."
        click.echo(output)
    lst = MetadataList(
        string,
        via=provider,
        style=style,
        locale=locale,
    )
    for item in lst.items:
        output = item.write(to=to)
        if show_errors and not item.is_valid:
            message = f"{item}: {item.errors}"
            raise click.ClickException(message)
        click.echo(output)


@cli.command()
@click.argument("prefix", type=str, required=True)
def encode(prefix):
    if validate_prefix(prefix) is None:
        return None
    output = encode_doi(prefix)
    click.echo(output)


@cli.command()
@click.argument("doi", type=str, required=True)
def decode(doi):
    output = decode_doi(doi)
    click.echo(output)


@cli.command()
@click.argument("id", type=str, required=True)
@click.option("--api-key", "-k", type=str, required=True)
@click.option("--api-url", "-u", type=str, required=True)
def update_ghost_post(id, api_key, api_url):
    output = update_ghost_post_via_api(id, api_key, api_url)
    click.echo(output)


@cli.command()
def version():
    version = importlib.metadata.version("commonmeta-py")
    click.echo(f"commonmeta-py {version}")


if __name__ == "__main__":
    cli()
