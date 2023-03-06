## Supported Metadata Formats

commonmeta-py reads and/or writes these metadata formats:

| Format                                                                                           | Name          | Content Type                           | Read    | Write   |
| ------------------------------------------------------------------------------------------------ | ------------- | -------------------------------------- | ------- | ------- |
| Commonmeta  | commonmeta    | application/vnd.commonmeta+json        | yes     | yes     |
| [CrossRef Unixref XML](https://www.crossref.org/schema/documentation/unixref1.1/unixref1.1.html) | crossref_xml      | application/vnd.crossref.unixref+xml   | yes | planned |
| [Crossref](https://api.crossref.org)                                                             | crossref | application/vnd.crossref+json          | yes     | no      |
| [DataCite XML](https://schema.datacite.org/)                                                     | datacite_xml      | application/vnd.datacite.datacite+xml  | planned | later |
| [DataCite](https://api.datacite.org/)                                                            | datacite | application/vnd.datacite.datacite+json | yes     | yes |
| [Schema.org (in JSON-LD)](http://schema.org/)                                                    | schema_org    | application/vnd.schemaorg.ld+json      | yes     | yes     |
| [RDF XML](http://www.w3.org/TR/rdf-syntax-grammar/)                                              | rdf_xml       | application/rdf+xml                    | no      | later   |
| [RDF Turtle](http://www.w3.org/TeamSubmission/turtle/)                                           | turtle        | text/turtle                            | no      | later   |
| [Citeproc JSON](https://citationstyles.org/)                                                     | citeproc      | pplication/vnd.citationstyles.csl+json | later | yes     |
| [Formatted text citation](https://citationstyles.org/)                                           | citation      | text/x-bibliography                    | no      | yes     |
| [Codemeta](https://codemeta.github.io/)                                                          | codemeta      | application/vnd.codemeta.ld+json       | yes | later |
| [Citation File Format (CFF)](https://citation-file-format.github.io/)                            | cff           | application/vnd.cff+yaml               | yes | later |
| [JATS](https://jats.nlm.nih.gov/)                                                                | jats          | application/vnd.jats+xml               | later   | later   |
| [CSV](ttps://en.wikipedia.org/wiki/Comma-separated_values)                                       | csv           | text/csv                               | no      | later   |
| [BibTex](http://en.wikipedia.org/wiki/BibTeX)                                                    | bibtex        | application/x-bibtex                   | later | yes     |
| [RIS](http://en.wikipedia.org/wiki/RIS_(file_format))                                            | ris           | application/x-research-info-systems    | later | yes     |

_commonmeta_: the Commonmeta format is the native format for the library and used internally.  
_Planned_: we plan to implement this format in the next minor release.  
_Later_: we plan to implement this format in the next major release.
