[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1cebb9b4147144a2a221e512729e2576)](https://www.codacy.com/gh/front-matter/talbot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=front-matter/talbot&amp;utm_campaign=Badge_Grade)
![GitHub](https://img.shields.io/github/license/front-matter/talbot?logo=MIT)

# Talbot

Talbot is a Python library to convert scholarly metadata, modelled after the [briard ruby gem](https://github.com/front-matter/briard). Briard is work in progress, the first release is
planned for March 2023.

## Installation

Dev version

    pip install git+https://github.com/front-matter/talbot.git#egg=talbot

Or build it yourself locally

    git clone https://github.com/front-matter/talbot.git
    cd Talbot
    make install

## Supported Metadata Formats

Talbot reads and/or writes these metadata formats:

| Format                                                                                           | Name          | Content Type                           | Read    | Write   |
| ------------------------------------------------------------------------------------------------ | ------------- | -------------------------------------- | ------- | ------- |
| [CrossRef Unixref XML](https://www.crossref.org/schema/documentation/unixref1.1/unixref1.1.html) | crossref      | application/vnd.crossref.unixref+xml   | planned | planned |
| [Crossref JSON](https://api.crossref.org)                                                        | crossref_json | application/vnd.crossref+json          | yes     | no      |
| [DataCite XML](https://schema.datacite.org/)                                                     | datacite      | application/vnd.datacite.datacite+xml  | planned | planned |
| [DataCite JSON](https://api.datacite.org/)                                                       | datacite_json | application/vnd.datacite.datacite+json | yes     | planned |
| [Schema.org (in JSON-LD)](http://schema.org/)                                                    | schema_org    | application/vnd.schemaorg.ld+json      | yes     | yes     |
| [RDF XML](http://www.w3.org/TR/rdf-syntax-grammar/)                                              | rdf_xml       | application/rdf+xml                    | no      | later   |
| [RDF Turtle](http://www.w3.org/TeamSubmission/turtle/)                                           | turtle        | text/turtle                            | no      | later   |
| [Citeproc JSON](https://citationstyles.org/)                                                     | citeproc      | pplication/vnd.citationstyles.csl+json | planned | yes     |
| [Formatted text citation](https://citationstyles.org/)                                           | citation      | text/x-bibliography                    | no      | yes     |
| [Codemeta](https://codemeta.github.io/)                                                          | codemeta      | application/vnd.codemeta.ld+json       | planned | planned |
| [Citation File Format (CFF)](https://citation-file-format.github.io/)                            | cff           | application/vnd.cff+yaml               | planned | planned |
| [JATS](https://jats.nlm.nih.gov/)                                                                | jats          | application/vnd.jats+xml               | later   | later   |
| [CSV](ttps://en.wikipedia.org/wiki/Comma-separated_values)                                       | csv           | text/csv                               | no      | later   |
| [BibTex](http://en.wikipedia.org/wiki/BibTeX)                                                    | bibtex        | application/x-bibtex                   | planned | yes     |
| [RIS](http://en.wikipedia.org/wiki/RIS_(file_format))                                            | ris           | application/x-research-info-systems    | planned | yes     |

_Planned_: we plan to implement this format for the first public release.  
_Later_: we plan to implement this format in a later release.

## Documentation

Documentation (work in progress) for using the library is available at [Front Matter Documentation](https://docs.front-matter.io/talbot/).

## Meta

-   Please note that this project is released with a [Contributor Code of Conduct](https://github.com/front-matter/talbot/blob/main/CODE_OF_CONDUCT.md>). By participating in this project you agree to abide by its terms.
-   License: [MIT](https://github.com/front-matter/talbot/blob/main/LICENSE)
