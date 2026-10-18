---
title: CSL-JSON Writer
weight: 40
---

This page shows how to generate a metadata in [CSL-JSON](https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html#introduction) format. CSL-JSON is used by the [Citation Styles Language](https://citationstyles.org/) to generate formatted citations and bibliographies.

As with all commonmeta-py writer examples, we start by fetching metadata, in this example a journal article via its Crossref DOI, and convert them to the internal commonmeta format.

```python
from commonmeta import Metadata

# Fetch metadata from a DOI
string = "10.7554/elife.01567"
metadata = Metadata(string)

# Check that metadata was fetched and is valid
print(metadata.is_valid)
```

```
True
```

## Generate CSL-JSON

We can now generate CSL-JSON from the metadata in commonmeta format.

```python
csl = metadata.write(to="csl")
print(csl.decode())
```

```
{"type":"article-journal","id":"https://doi.org/10.7554/elife.01567","DOI":"10.7554/elife.01567","URL":"https://elifesciences.org/articles/01567","categories":[],"language":"en","author":[{"family":"Sankar","given":"Martial"},{"family":"Nieminen","given":"Kaisa"},{"family":"Ragni","given":"Laura"},{"family":"Xenarios","given":"Ioannis"},{"family":"Hardtke","given":"Christian S"}],"issued":{"date-parts":[[2014,2,11]]},"abstract":"Among various advantages, their small size makes model organisms preferred subjects of investigation. Yet, even in model systems detailed analysis of numerous developmental processes at cellular level is severely hampered by their scale. For instance, secondary growth of Arabidopsis hypocotyls creates a radial pattern of highly specialized tissues that comprises several thousand cells starting from a few dozen. This dynamic process is difficult to follow because of its scale and because it can only be investigated invasively, precluding comprehensive understanding of the cell proliferation, differentiation, and patterning events involved. To overcome such limitation, we established an automated quantitative histology approach. We acquired hypocotyl cross-sections from tiled high-resolution images and extracted their information content using custom high-throughput image processing and segmentation. Coupled with automated cell type recognition through machine learning, we could establish a cellular resolution atlas that reveals vascular morphodynamics during secondary growth, for example equidistant phloem pole formation.","container-title":"eLife","volume":"3","publisher":"eLife Sciences Publications, Ltd","title":"Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth","copyright":"CC-BY-3.0"}
```

CSL-JSON is similar to the JSON – e.g. in using `date-parts` for dates. However, it has some differences, e.g. in the `type` field. commonmeta therefore supports specific types for CSL-JSON in addition to the `ResourceType` used for Crossref metadata.
