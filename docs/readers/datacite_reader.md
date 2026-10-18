---
title: DataCite Reader
weight: 40
---

This page shows how to read metadata from DataCite, using a DataCite DOI.

## Fetch metadata

```python
from commonmeta import Metadata

# Fetch metadata from a DataCite DOI
string = "https://doi.org/10.5061/dryad.8515"
metadata = Metadata(string)

# Check that metadata was fetched and is valid
print(metadata.is_valid)
```

```
True
```

## Inspect the metadata

The following metadata are required for each DataCite resource:

* `id`: the persistent identifier of the resource, typically a DOI
* `type`: the type of the resource in commonmeta format, e.g. `Dataset`, `Software`, `PhysicalObject` or `JournalArticle`
* `titles`: the title(s) of the resource
* `creators`: the creator(s)/author(s) of the resource
* `publisher`: the publisher of the resource
* `publication_year`: the publication year of the resource

In addition, there are plenty of optional metadata. They are converted into the standardized commonmeta format used internally. This format is close to the metadata format used by DataCite.

```python
commonmeta = metadata.write()
print(commonmeta.decode())
```

```
{"id":"https://doi.org/10.5061/dryad.8515","type":"Dataset","container":{"identifiers":[{"identifier":"dryad.dryad","identifier_type":"DataCite"}]},"contributors":[{"type":"Person","person":{"given_name":"Benjamin","family_name":"Ollomo","affiliations":[{"name":"Centre International de Recherches Médicales de Franceville"}]},"roles":["Author"]},{"type":"Person","person":{"given_name":"Patrick","family_name":"Durand","affiliations":[{"name":"Centre National de la Recherche Scientifique"}]},"roles":["Author"]},{"type":"Person","person":{"given_name":"Franck","family_name":"Prugnolle","affiliations":[{"name":"Centre National de la Recherche Scientifique"}]},"roles":["Author"]},{"type":"Person","person":{"given_name":"Emmanuel J. P.","family_name":"Douzery"},"roles":["Author"]},{"type":"Person","person":{"given_name":"Céline","family_name":"Arnathau","affiliations":[{"name":"Centre National de la Recherche Scientifique"}]},"roles":["Author"]},{"type":"Person","person":{"given_name":"Dieudonné","family_name":"Nkoghe","affiliations":[{"name":"Centre International de Recherches Médicales de Franceville"}]},"roles":["Author"]},{"type":"Person","person":{"given_name":"Eric","family_name":"Leroy","affiliations":[{"name":"Centre International de Recherches Médicales de Franceville"}]},"roles":["Author"]},{"type":"Person","person":{"given_name":"François","family_name":"Renaud","affiliations":[{"name":"Centre National de la Recherche Scientifique"}]},"roles":["Author"]}],"title":"Data from: A new malaria agent in African hominids.","date_published":"2011-02-01T17:22:41Z","dates":{"submitted":"2011-02-01T13:09:15Z","available":"2011-02-01T17:22:41Z"},"description":"Plasmodium falciparum is the major human malaria agent responsible for 200 to 300 million infections and one to three million deaths annually, mainly among African infants. The origin and evolution of this pathogen within the human lineage is still unresolved. A single species, P. reichenowi, which infects chimpanzees, is known to be a close sister lineage of P. falciparum. Here we report the discovery of a new Plasmodium species infecting Hominids. This new species has been isolated in two chimpanzees (Pan troglodytes) kept as pets by villagers in Gabon (Africa). Analysis of its complete mitochondrial genome (5529 nucleotides including Cyt b, Cox I and Cox III genes) reveals an older divergence of this lineage from the clade that includes P. falciparum and P. reichenowi (approximately 21+/-9 Myrs ago using Bayesian methods and considering that the divergence between P. falciparum and P. reichenowi occurred 4 to 7 million years ago as generally considered in the literature). This time frame would be congruent with the radiation of hominoids, suggesting that this Plasmodium lineage might have been present in early hominoids and that they may both have experienced a simultaneous diversification. Investigation of the nuclear genome of this new species will further the understanding of the genetic adaptations of P. falciparum to humans. The risk of transfer and emergence of this new species in humans must be now seriously considered given that it was found in two chimpanzees living in contact with humans and its close relatedness to the most virulent agent of malaria.","additional_descriptions":[{"description":"Ollomo_PLoSPathog_2009Nucleotide alignment concatenation of 4 mitochondrial genes for 17 Plasmodium species and one outgroup.Ollomo_PLoSPathog_2009_PHYMLMaximum likelihood tree inferred from the 4-gene concatenation using PHYML.","type":"Other"}],"geo_locations":[{"place":"Africa"}],"language":"en","license":{"id":"CC0-1.0","title":"Creative Commons Zero v1.0 Universal","url":"https://creativecommons.org/publicdomain/zero/1.0/legalcode"},"provider":"DataCite","publisher":{"name":"Dryad"},"relations":[{"id":"https://doi.org/10.1371/journal.ppat.1000446","type":"IsReferencedBy"}],"subjects":[{"subject":"Plasmodium","scheme":"PLOS Subject Area Thesaurus","scheme_uri":"https://github.com/PLOS/plos-thesaurus"},{"subject":"Malaria","scheme":"PLOS Subject Area Thesaurus","scheme_uri":"https://github.com/PLOS/plos-thesaurus"},{"subject":"mitochondrial genome"},{"subject":"Parasites"}],"url":"https://datadryad.org/dataset/doi:10.5061/dryad.8515","version":"1","schema_version":"https://commonmeta.org/commonmeta_v1.0.json"}
```
