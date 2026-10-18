---
title: RIS Writer
weight: 50
---

This page shows how to generate RIS metadata from a scholarly resource retrieved via commonmeta-py. RIS metadata can be imported into reference managers such as Zotero, Mendeley, and EndNote.

## Fetch metadata

As with all commonmeta-py examples, we start by fetching metadata, in this example a journal article via its Crossref DOI, and convert them to the internal commonmeta format.

```python
from commonmeta import Metadata

# Fetch metadata from a DOIq
string = "10.7554/elife.01567"
metadata = Metadata(string)

# Check that metadata was fetched and is valid
print(metadata.is_valid)
```

```
True
```

## Generate RIS

We can now generate RIS metadata from the article metadata.

```python
ris = metadata.write(to="ris")
print(ris.decode())
```

```
TY  - JOUR
T1  - Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth
T2  - eLife
AU  - Sankar, Martial
AU  - Nieminen, Kaisa
AU  - Ragni, Laura
AU  - Xenarios, Ioannis
AU  - Hardtke, Christian S
DO  - 10.7554/elife.01567
UR  - https://elifesciences.org/articles/01567
AB  - Among various advantages, their small size makes model organisms preferred subjects of investigation. Yet, even in model systems detailed analysis of numerous developmental processes at cellular level is severely hampered by their scale. For instance, secondary growth of Arabidopsis hypocotyls creates a radial pattern of highly specialized tissues that comprises several thousand cells starting from a few dozen. This dynamic process is difficult to follow because of its scale and because it can only be investigated invasively, precluding comprehensive understanding of the cell proliferation, differentiation, and patterning events involved. To overcome such limitation, we established an automated quantitative histology approach. We acquired hypocotyl cross-sections from tiled high-resolution images and extracted their information content using custom high-throughput image processing and segmentation. Coupled with automated cell type recognition through machine learning, we could establish a cellular resolution atlas that reveals vascular morphodynamics during secondary growth, for example equidistant phloem pole formation.
PY  - 2014
PB  - eLife Sciences Publications, Ltd
LA  - en
VL  - 3
ER  -
```

## Supported RIS Types

commonmeta-py supports most RIS types and maps them from the internal commonmeta type. Types that are not supported are mapped to `GEN`. Below are examples of RIS metadata for types other than `JOUR` (journal article):

### Book chapter

```python
metadata = Metadata("10.1007/978-3-662-46370-3_13")
ris = metadata.write(to="ris")
print(ris.decode())
```

```
TY  - CHAP
T1  - Clinical Symptoms and Physical Examinations
T2  - Shoulder Stiffness
AU  - Diercks, Ronald L.
AU  - Ludvigsen, Tom Clement
DO  - 10.1007/978-3-662-46370-3_13
UR  - https://link.springer.com/10.1007/978-3-662-46370-3_13
PY  - 2015
PB  - Springer Berlin Heidelberg
LA  - en
SP  - 155
EP  - 158
ER  -
```

### Conference proceedings

```python
metadata = Metadata("10.1109/iccv.2007.4408927")
ris = metadata.write(to="ris")
print(ris.decode())
```

```
TY  - CPAPER
T1  - A Seeded Image Segmentation Framework Unifying Graph Cuts And Random Walker Which Yields A New Algorithm
T2  - 2007 IEEE 11th International Conference on Computer Vision
AU  - Sinop, Ali Kemal
AU  - Grady, Leo
DO  - 10.1109/iccv.2007.4408927
UR  - http://ieeexplore.ieee.org/document/4408927/
PY  - 2007
PB  - IEEE
SP  - 1
EP  - 8
ER  -
```

### Dissertation

```python
metadata = Metadata("10.14264/uql.2020.791")
ris = metadata.write(to="ris")
print(ris.decode())
```

```
TY  - THES
T1  - School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers
T2  - The University of Queensland
AU  - Collingwood, Patricia Maree
DO  - 10.14264/uql.2020.791
UR  - http://espace.library.uq.edu.au/view/UQ:23a1e74
PY  - 2020
PB  - University of Queensland Library
ER  -
```
