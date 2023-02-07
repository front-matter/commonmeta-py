# Talbot

Talbot is a Python library to convert scholarly metadata, modelled after the [briard ruby gem](https://github.com/front-matter/briard). Briard is work in progress, the first release is
**planned** for April 2023.

## Installation

Dev version

```
pip install git+https://github.com/front-matter/talbot.git#egg=talbot
```

Or build it yourself locally

```
git clone https://github.com/front-matter/talbot.git
cd Talbot
make install
```

## Features

Talbot reads and/or writes these metadata formats:

<table class="table table-bordered table-striped">
  <thead>
    <tr>
      <th>Format</th>
      <th>Name</th>
      <th>Content Type</th>
      <th>Read</th>
      <th>Write</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href='https://www.crossref.org/schema/documentation/unixref1.1/unixref1.1.html'>CrossRef Unixref XML</a></td>
      <td>crossref</td>
      <td>application/vnd.crossref.unixref+xml</td>
      <td>**planned**</td>
      <td>**planned**</td>
   </tr>
    <tr>
      <td><a href='https://api.crossref.org'>CrossRef JSON</a></td>
      <td>crossref_json</td>
      <td>application/vnd.crossref+json</td>
      <td>Yes</td>
      <td>No</td>
   </tr>
    <tr>
      <td><a href='https://schema.datacite.org/'>DataCite XML</a></td>
      <td>datacite</td>
      <td>application/vnd.datacite.datacite+xml</td>
      <td>**planned**</td>
      <td>**planned**</td>
    </tr>
    <tr>
      <td><a href='https://api.datacite.org/'>DataCite JSON</a></td>
      <td>datacite_json</td>
      <td>application/vnd.datacite.datacite+json</td>
      <td>**planned**</td>
      <td>**planned**</td>
    </tr>
    <tr>
      <td><a href='http://schema.org/'>Schema.org in JSON-LD</a></td>
      <td>schema_org</td>
      <td>application/vnd.schemaorg.ld+json</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td><a href='http://www.w3.org/TR/rdf-syntax-grammar/'>RDF XML</a></td>
      <td>rdf_xml</td>
      <td>application/rdf+xml</td>
      <td>No</td>
      <td>No</td>
    </tr>
    <tr>
      <td><a href='http://www.w3.org/TeamSubmission/turtle/'>RDF Turtle</a></td>
      <td>turtle</td>
      <td>text/turtle</td>
      <td>No</td>
      <td>No</td>
    </tr>
    <tr>
      <td><a href='https://citationstyles.org/'>Citeproc JSON</a></td>
      <td>citeproc</td>
      <td>application/vnd.citationstyles.csl+json</td>
      <td>**planned**</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td><a href='https://citationstyles.org/'>Formatted text citation</a></td>
      <td>citation</td>
      <td>text/x-bibliography</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td><a href='https://codemeta.github.io/'>Codemeta</a></td>
      <td>codemeta</td>
      <td>application/vnd.codemeta.ld+json</td>
      <td>planed</td>
      <td>**planned**</td>
    </tr>
    <tr>
      <td><a href='https://citation-file-format.github.io/'>CFF</a></td>
      <td>citation file format (cff)</td>
      <td>application/vnd.cff+yaml</td>
      <td>**planned**</td>
      <td>**planned**</td>
    </tr>
    <tr>
      <td><a href='https://jats.nlm.nih.gov/'>JATS</a></td>
      <td>jats</td>
      <td>application/vnd.jats+xml</td>
      <td>No</td>
      <td>**planned**</td>
    </tr>
    <tr>
      <td><a href='https://en.wikipedia.org/wiki/Comma-separated_values'>CSV</a></td>
      <td>csv</td>
      <td>text/csv</td>
      <td>No</td>
      <td>**planned**</td>
    </tr>
    <tr>
      <td><a href='http://en.wikipedia.org/wiki/BibTeX'>BibTeX</a></td>
      <td>bibtex</td>
      <td>application/x-bibtex</td>
      <td>**planned**</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td><a href='http://en.wikipedia.org/wiki/RIS_(file_format)'>RIS</a></td>
      <td>ris</td>
      <td>application/x-research-info-systems</td>
      <td>**planned**</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

## Meta

* Please note that this project is released with a [Contributor Code of Conduct](https://github.com/front-matter/talbot/blob/main/CODE_OF_CONDUCT.md>). By participating in this project you agree to abide by its terms.
* License: [MIT](https://github.com/front-matter/talbot/blob/main/LICENSE)
