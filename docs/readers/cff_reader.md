---
title: CFF Reader
weight: 10
---

This page shows how to read metadata in [Citation File Format (CFF)](https://citation-file-format.github.io/).

## Fetch the metadata

```python
from commonmeta import Metadata

# Fetch metadata from a GitHub repository that contains a CITATION.cff file
string = "https://github.com/kyleliang919/Long-context-transformers"
metadata = Metadata(string)

# Check that metadata was fetched and is valid
print(metadata.is_valid)
```

```
True
```

## Inspect the metadata

The following metadata are required for each Crossref resource:

* `id`: the persistent identifier of the resource (e.g. a DOI or repository URL)
* `type`: the type of the resource in commonmeta format, for `CFF` it is always `Software`
* `url`: the URL of the resource, typically a code repository URL
* `titles`: the title(s) of the resource
* `creators`: the creator(s)/author(s) of the resource
* `publisher`: the publisher of the resource
* `publication_year`: the publication year of the resource

In addition, there are plenty of optional metadata. They are converted into the internal commonmeta format.

```python
commonmeta = metadata.write()
print(commonmeta.decode())
```

```
{"id":"https://doi.org/10.5281/zenodo.7651809","type":"Software","contributors":[{"type":"Person","person":{"id":"https://orcid.org/0000-0002-0055-8659","given_name":"Kaizhao","family_name":"Liang"},"roles":["Author"]}],"title":"Long Context Transformer v0.0.1","date_published":"2023-02-17","publisher":{"name":"GitHub"},"url":"https://github.com/kyleliang919/Long-context-transformers","version":"0.0.1","schema_version":"https://commonmeta.org/commonmeta_v1.0.json"}
```
