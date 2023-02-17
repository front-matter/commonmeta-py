[![Build](https://github.com/front-matter/talbot/actions/workflows/build.yml/badge.svg)](https://github.com/front-matter/talbot/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/talbot.svg)](https://badge.fury.io/py/talbot)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=front-matter_talbot&metric=coverage)](https://sonarcloud.io/summary/new_code?id=front-matter_talbot)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=front-matter_talbot&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=front-matter_talbot)
[![Usage](https://static.pepy.tech/badge/talbot)](https://pypi.python.org/pypi/talbot/)
![GitHub](https://img.shields.io/github/license/front-matter/talbot?logo=MIT)

# Talbot

Talbot is a Python library to convert scholarly metadata, modelled after the [briard ruby gem](https://github.com/front-matter/briard). Talbot is work in progress, the first release on PyPi (version 0.5.0) was on February 16, 2023.

## Installation

Stable version

    pip (or pip3) install talbot

Dev version

    pip install git+https://github.com/front-matter/talbot.git#egg=talbot

## Supported Metadata Formats

Talbot reads and/or writes these metadata formats:

| Format                                                                                           | Name          | Content Type                           | Read    | Write   |
| ------------------------------------------------------------------------------------------------ | ------------- | -------------------------------------- | ------- | ------- |
| [CrossRef Unixref XML](https://www.crossref.org/schema/documentation/unixref1.1/unixref1.1.html) | crossref_xml      | application/vnd.crossref.unixref+xml   | later | planned |
| [Crossref](https://api.crossref.org)                                                             | crossref | application/vnd.crossref+json          | yes     | no      |
| [DataCite XML](https://schema.datacite.org/)                                                     | datacite_xml      | application/vnd.datacite.datacite+xml  | later | later |
| [DataCite](https://api.datacite.org/)                                                            | datacite | application/vnd.datacite.datacite+json | yes     | yes |
| [Schema.org (in JSON-LD)](http://schema.org/)                                                    | schema_org    | application/vnd.schemaorg.ld+json      | yes     | yes     |
| [RDF XML](http://www.w3.org/TR/rdf-syntax-grammar/)                                              | rdf_xml       | application/rdf+xml                    | no      | later   |
| [RDF Turtle](http://www.w3.org/TeamSubmission/turtle/)                                           | turtle        | text/turtle                            | no      | later   |
| [Citeproc JSON](https://citationstyles.org/)                                                     | citeproc      | pplication/vnd.citationstyles.csl+json | yes | yes     |
| [Formatted text citation](https://citationstyles.org/)                                           | citation      | text/x-bibliography                    | no      | yes     |
| [Codemeta](https://codemeta.github.io/)                                                          | codemeta      | application/vnd.codemeta.ld+json       | yes | later |
| [Citation File Format (CFF)](https://citation-file-format.github.io/)                            | cff           | application/vnd.cff+yaml               | later | later |
| [JATS](https://jats.nlm.nih.gov/)                                                                | jats          | application/vnd.jats+xml               | later   | later   |
| [CSV](ttps://en.wikipedia.org/wiki/Comma-separated_values)                                       | csv           | text/csv                               | no      | later   |
| [BibTex](http://en.wikipedia.org/wiki/BibTeX)                                                    | bibtex        | application/x-bibtex                   | later | yes     |
| [RIS](http://en.wikipedia.org/wiki/RIS_(file_format))                                            | ris           | application/x-research-info-systems    | later | yes     |

_Planned_: we plan to implement this format for the v0.8 public release.  
_Later_: we plan to implement this format in a later release.

## Documentation

Documentation (work in progress) for using the library is available at the [Talbot Documentation](https://talbot.docs.front-matter.io) website and includes several interactive Jupyter Notebooks .

## Meta

Please note that this project is released with a [Contributor Code of Conduct](https://github.com/front-matter/talbot/blob/main/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.  

License: [MIT](https://github.com/front-matter/talbot/blob/main/LICENSE)
