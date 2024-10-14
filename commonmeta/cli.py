import click
import time
import pydash as py_
import orjson as json

from commonmeta import Metadata, MetadataList  # __version__
from commonmeta.api_utils import update_ghost_post_via_api
from commonmeta.doi_utils import validate_prefix
from commonmeta.utils import encode_doi, decode_doi
from commonmeta.readers.json_feed_reader import (
    get_json_feed_item_uuid,
)
from commonmeta.readers.crossref_reader import get_random_crossref_id
from commonmeta.readers.datacite_reader import get_random_datacite_id


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
        raise click.ClickException(str(metadata.errors) + str(metadata.write_errors))

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
@click.argument("string", type=str, required=True)
@click.option("--via", "-f", type=str)
@click.option("--to", "-t", type=str, default="commonmeta")
@click.option("--style", "-s", type=str, default="apa")
@click.option("--locale", "-l", type=str, default="en-US")
@click.option("--prefix", type=str)
@click.option("--depositor", type=str)
@click.option("--email", type=str)
@click.option("--registrant", type=str)
@click.option("--filename", type=str)
@click.option("--jsonlines/--no-jsonlines", type=bool, show_default=True, default=False)
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
    filename,
    jsonlines,
    show_errors,
    show_timer,
):
    start = time.time()
    metadata_list = MetadataList(
        string,
        via=via,
        depositor=depositor,
        email=email,
        registrant=registrant,
        prefix=prefix,
        filename=filename,
        jsonlines=jsonlines,
    )
    end = time.time()
    runtime = end - start
    if show_errors and not metadata_list.is_valid:
        raise click.ClickException(str(metadata_list.errors))
    click.echo(metadata_list.write(to=to, style=style, locale=locale))
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
def encode_by_id(id):
    post = get_json_feed_item_uuid(id)
    prefix = py_.get(post, "blog.prefix")
    if validate_prefix(prefix) is None:
        return None
    output = encode_doi(prefix)
    click.echo(output)


@cli.command()
@click.argument("filter", type=str, required=True, default="unregistered")
@click.option("--id", type=str)
def json_feed(filter, id=None):
    if filter == "blog_slug" and id is not None:
        post = get_json_feed_item_uuid(id)
        output = py_.get(post, "blog.slug", "no slug found")
    else:
        output = "no filter specified"
    click.echo(output)


@cli.command()
@click.argument("id", type=str, required=True)
@click.option("--api-key", "-k", type=str, required=True)
@click.option("--api-url", "-u", type=str, required=True)
def update_ghost_post(id, api_key, api_url):
    output = update_ghost_post_via_api(id, api_key, api_url)
    click.echo(output)


if __name__ == "__main__":
    cli()
