[![DOI](https://zenodo.org/badge/570526578.svg)](https://zenodo.org/doi/10.5281/zenodo.8340374)
[![Build](https://github.com/front-matter/commonmeta-py/actions/workflows/build.yml/badge.svg)](https://github.com/front-matter/commonmeta-py/actions/workflows/build.yml)
[![PyPI version](https://img.shields.io/pypi/v/commonmeta-py.svg)](https://pypi.org/project/commonmeta-py/)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=front-matter_commonmeta-py&metric=coverage)](https://sonarcloud.io/summary/new_code?id=front-matter_commonmeta-py)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=front-matter_commonmeta-py&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=front-matter_commonmeta-py)
[![docs](https://img.shields.io/badge/docs-passing-blue)](https://python.commonmeta.org)
![GitHub](https://img.shields.io/github/license/front-matter/commonmeta-py?logo=MIT)

# commonmeta-py

commonmeta-py is a Python library to implement Commonmeta, the common Metadata Model for Scholarly Metadata. Use commonmeta-py to convert scholarly metadata, in a variety of formats, listed below. Commonmeta-py is work in progress, the first release on PyPi (version 0.5.0) was on February 16, 2023. Up until version 0.5.1, the library was called talbot. Commonmeta-py is modelled after the [commonmeta-ruby ruby gem](https://github.com/front-matter/commonmeta-ruby).

commonmeta-py uses semantic versioning. Currently, its major version number is still at 0, meaning the API is not yet stable, and breaking changes are expected in the internal API and commonmeta JSON format.

## Installation

Stable version

    pip (or pip3) install commonmeta-py

Dev version

    pip install git+https://github.com/front-matter/commonmeta-py.git#egg=commonmeta-py

## Supported Metadata Formats

Commometa-py reads and/or writes these metadata formats:

| Format                                                                                           | Name          | Content Type                           | Read    | Write   |
| ------------------------------------------------------------------------------------------------ | ------------- | -------------------------------------- | ------- | ------- |
| Commonmeta  | commonmeta    | application/vnd.commonmeta+json        | yes     | yes     |
| [CrossRef XML](https://www.crossref.org/schema/documentation/unixref1.1/unixref1.1.html) | crossref_xml      | application/vnd.crossref.unixref+xml   | yes | yes |
| [Crossref](https://api.crossref.org)                                                             | crossref | application/vnd.crossref+json          | yes     | n/a     |
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
| [BibTex](http://en.wikipedia.org/wiki/BibTeX)                                                    | bibtex        | application/x-bibtex                   | later | yes     |
| [RIS](http://en.wikipedia.org/wiki/RIS_(file_format))                                            | ris           | application/x-research-info-systems    | yes   | yes     |
| [InvenioRDM](https://inveniordm.docs.cern.ch/reference/metadata/)                                | inveniordm    | application/vnd.inveniordm.v1+json     | yes   | yes     |
| [JSON Feed](https://www.jsonfeed.org/)                                                           | json_feed_item     | application/feed+json    | yes | later     |

_commonmeta_: the Commonmeta format is the native format for the library and used internally.
_Planned_: we plan to implement this format for the v1.0 public release.  
_Later_: we plan to implement this format in a later release.

## Documentation

Documentation (work in progress) for using the library is available at the [commonmeta-py Documentation](https://python.commonmeta.org/) website and includes several interactive Jupyter Notebooks .

## Meta

Please note that this project is released with a [Contributor Code of Conduct](https://github.com/front-matter/commonmeta-py/blob/main/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.  

License: [MIT](https://github.com/front-matter/commonmeta-py/blob/main/LICENSE)
