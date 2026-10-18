---
title: Guide
---

[![Build](https://github.com/front-matter/commonmeta-py/actions/workflows/build.yml/badge.svg)](https://github.com/front-matter/commonmeta-py/actions/workflows/build.yml)
[![PyPI version](https://img.shields.io/pypi/v/commonmeta-py.svg)](https://pypi.org/project/commonmeta-py/)
[![docs](https://img.shields.io/badge/docs-passing-blue)](https://python.commonmeta.org/)
![GitHub](https://img.shields.io/github/license/front-matter/commonmeta-py?logo=MIT)

commonmeta-py is a Python library to implement commonmeta, the metadata format for common scholarly metadata. Use commonmeta-py to convert scholarly metadata from/to a variety of metadata formats, listed below. Commonmeta-py is work in progress, the first release on PyPi (version 0.5.0) was on February 16, 2023. Up until version 0.5.1, the library was called talbot. Commonmeta-py is modelled after the [briard ruby gem](https://github.com/front-matter/briard).

## Installation

commonmeta-py is installed with [uv](https://docs.astral.sh/uv/). Add it as a
library dependency to your project:

```
uv add commonmeta-py
```

To use the `commonmeta` command-line tool, install it globally instead:

```
uv tool install commonmeta-py
```

This makes `commonmeta` available on your `PATH`. Upgrade it later with
`uv tool upgrade commonmeta-py`, or remove it with
`uv tool uninstall commonmeta-py`.

Dev version, from the main branch:

```
uv add git+https://github.com/front-matter/commonmeta-py
```

The Rust backend (bulk import, the local SQLite store, Parquet output) is an
optional extra and needs Python 3.14:

```
uv add "commonmeta-py[backend]"
```

## Testing

commonmeta-py uses `pytest`, `vcrpy` and `hypothesis` for testing. To run the tests, install the dependencies with `uv sync` (add `--extra backend` for the backend tests), then issue one of the following commands from the root folder:

All tests:
```
uv run pytest
```

All tests in a test file, e.g. `tests/test-utils.py`:
```
uv run pytest tests/test-utils.py
```

Run a specific test e.g. `test_datacite_api_url` in `tests/test-utils.py`:
```
uv run pytest tests/test-utils.py -k 'test_datacite_api_url'
```

`vcrpy`records HTTP requests to speed up testing. 

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
| [OpenAlex](https://www.openalex.org/)                                                           | openalex     |    | yes | no     |

_commonmeta_: the Commonmeta format is the native format for the library and used internally.
_Later_: we plan to implement this format in a later release.
