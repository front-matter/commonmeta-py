[![DOI](https://zenodo.org/badge/570526578.svg)](https://zenodo.org/doi/10.5281/zenodo.8340374)
[![Build](https://github.com/front-matter/commonmeta-py/actions/workflows/build.yml/badge.svg)](https://github.com/front-matter/commonmeta-py/actions/workflows/build.yml)
[![PyPI version](https://img.shields.io/pypi/v/commonmeta-py.svg)](https://pypi.org/project/commonmeta-py/)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=front-matter_commonmeta-py&metric=coverage)](https://sonarcloud.io/summary/new_code?id=front-matter_commonmeta-py)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=front-matter_commonmeta-py&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=front-matter_commonmeta-py)
[![docs](https://img.shields.io/badge/docs-passing-blue)](https://python.commonmeta.org)
![GitHub](https://img.shields.io/github/license/front-matter/commonmeta-py?logo=MIT)

# commonmeta-py

commonmeta-py is a Python library to implement Commonmeta, the common Metadata Model for Scholarly Metadata. Use commonmeta-py to convert scholarly metadata, in a variety of formats, listed below. The first release on PyPi (version 0.5.0) was on February 16, 2023. Up until version 0.5.1, the library was called talbot. Commonmeta is also available as a Rust library [commonmeta-rs](https://codeberg.org/front-matter/commonmeta-rs).

commonmeta-py uses semantic versioning. Currently, its major version number is still at 0, meaning the API is not yet stable, and breaking changes are expected in the internal API and commonmeta JSON format.

## Installation

Add commonmeta-py as a library dependency to your project:

    uv add commonmeta-py

To use the `commonmeta` command-line tool, install it globally with
[uv](https://docs.astral.sh/uv/) instead:

    uv tool install commonmeta-py

This makes `commonmeta` available on your `PATH`. Upgrade it later with
`uv tool upgrade commonmeta-py`, or remove it with `uv tool uninstall
commonmeta-py`.

## Supported Metadata Formats

Commometa-py reads and/or writes these metadata formats:

| Format                                                                                           | Name          | Content Type                           | Read    | Write   |
| ------------------------------------------------------------------------------------------------ | ------------- | -------------------------------------- | ------- | ------- |
| Commonmeta  | commonmeta    | application/vnd.commonmeta+json        | yes     | yes     |
| [CrossRef XML](https://www.crossref.org/schema/documentation/unixref1.1/unixref1.1.html) | crossref_xml      | application/vnd.crossref.unixref+xml   | yes | yes |
| [Crossref](https://api.crossref.org)                                                             | crossref | application/vnd.crossref+json          | yes     | yes    |
| [DataCite](https://api.datacite.org/)                                                            | datacite | application/vnd.datacite.datacite+json | yes     | yes |
| [Schema.org (in JSON-LD)](http://schema.org/)                                                    | schema_org    | application/vnd.schemaorg.ld+json      | yes     | yes     |
| [RDF XML](http://www.w3.org/TR/rdf-syntax-grammar/)                                              | rdf_xml       | application/rdf+xml                    | no      | later   |
| [RDF Turtle](http://www.w3.org/TeamSubmission/turtle/)                                           | turtle        | text/turtle                            | no      | later   |
| [CSL-JSON](https://citationstyles.org/)                                                     | csl      | application/vnd.citationstyles.csl+json | yes | yes     |
| [Formatted text citation](https://citationstyles.org/)                                           | citation      | text/x-bibliography                    | n/a     | yes     |
| [Codemeta](https://codemeta.github.io/)                                                          | codemeta      | application/vnd.codemeta.ld+json       | yes | later |
| [Citation File Format (CFF)](https://citation-file-format.github.io/)                            | cff           | application/vnd.cff+yaml               | yes | later |
| [JATS](https://jats.nlm.nih.gov/)                                                                | jats          | application/vnd.jats+xml               | later   | later   |
| [CSV](ttps://en.wikipedia.org/wiki/Comma-separated_values)                                       | csv           | text/csv                               | no      | later   |
| [BibTex](http://en.wikipedia.org/wiki/BibTeX)                                                    | bibtex        | application/x-bibtex                   | yes | yes     |
| [RIS](http://en.wikipedia.org/wiki/RIS_(file_format))                                            | ris           | application/x-research-info-systems    | yes   | yes     |
| [InvenioRDM](https://inveniordm.docs.cern.ch/reference/metadata/)                                | inveniordm    | application/vnd.inveniordm.v1+json     | yes   | yes     |
| [JSON Feed](https://www.jsonfeed.org/)                                                           | jsonfeed     | application/feed+json    | yes | later     |
| [OpenAlex](https://www.openalex.org/)                                                           | openalex     |    | yes | no     |

_commonmeta_: the Commonmeta format is the native format for the library and used internally.
_Planned_: we plan to implement this format for the v1.0 public release.
_Later_: we plan to implement this format in a later release.

## Command-line interface

Installing commonmeta-py provides a `commonmeta` command with the subcommands
`convert`, `list`, `put`, `push`, `encode`, and `decode`.

You can also run the CLI without installing anything, using
[uv](https://docs.astral.sh/uv/). Because the package name (`commonmeta-py`)
differs from the command name (`commonmeta`), pass it with `--from`:

```sh
uvx --from commonmeta-py commonmeta convert 10.5555/12345678 --to csl
```

The examples below use `commonmeta ...`; prefix them with
`uvx --from commonmeta-py` to run the same commands without installing.

```sh
# Encode/decode a Crockford base32 identifier suffix given a DOI prefix
commonmeta encode 10.5555
commonmeta decode 10.5555/nwbyp-29t86

# Convert a single record between formats, fetching it by DOI
# (--from is auto-detected from a DOI/URL, so it can usually be omitted)
commonmeta convert 10.5555/12345678 --to csl

# Convert a local file and write the result to disk
commonmeta convert record.json --from commonmeta --to csl --file out.json

# Render a formatted citation (CSL style + locale)
commonmeta convert 10.5555/12345678 --to citation --style apa --locale en-US

# Convert to Crossref XML, DataCite JSON, schema.org, BibTeX, or RIS
commonmeta convert 10.5555/12345678 --to crossref_xml
commonmeta convert 10.5555/12345678 --to datacite

# Convert a list of records from a local JSON/JSONL file
commonmeta list records.json --to bibtex --file out.bib

# Read a VRAIX daily dump and convert it (the --from value is the source)
commonmeta list --from crossref --date 2026-06-15 --to commonmeta --file out.json

# Fetch a batch of random records from an API (crossref, datacite, or openalex)
commonmeta list --sample --from crossref --number 5

# Register records with a live InvenioRDM instance (creates/updates and publishes
# real records — registration is currently only supported with --to inveniordm)
commonmeta push records.json --to inveniordm --host rogue-scholar.org --token TOKEN

# Same as push, but for a single record (DOI, URL, or file path)
commonmeta put 10.5555/12345678 --from crossref --to inveniordm --host rogue-scholar.org --token TOKEN

# Work fully offline — fails fast if a network call would be required
commonmeta convert record.json --from commonmeta --to csl --no-network
```

Use `commonmeta <subcommand> --help` for the full list of options. `--from`/`-f`
sets the input format (auto-detected when omitted) and `--to`/`-t` the output
format. JSON output (`commonmeta`, `datacite`, `schema_org`, `crossref`,
`inveniordm`, `csl`) is pretty-printed; use `--file` to write to disk instead of
stdout.

`convert` and `list` accept `--no-network`: any step that would make an outbound
request (fetching a DOI/URL, `--sample`, or downloading a VRAIX dump) fails
immediately with a clear message, while operations on local files always
succeed. `push` and `put` always require network access.

## Documentation

Documentation (work in progress) for using the library is available at the [commonmeta-py Documentation](https://python.commonmeta.org/) website.

## Meta

Please note that this project is released with a [Contributor Code of Conduct](https://github.com/front-matter/commonmeta-py/blob/main/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

License: [MIT](https://github.com/front-matter/commonmeta-py/blob/main/LICENSE)
