---
title: Citation Writer
weight: 20
---

This page shows how to generate a formatted citation in one of the 1000s of styles supported by the [Citation Style Language](https://citationstyles.org/). The citation is returned as a string in HTML format, supporting a limited subset of HTML tags (such as `<i>` and `<sup>`).

## Fetch metadata

As with all commonmeta-py examples, we start by fetching metadata, in this example a journal article via its Crossref DOI, an then convert them to the internal commonmeta format.

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

## Generate a formatted citation

Using the `citation` writer, commonmeta-py can generate a formatted citation for the resource, using one of the citation styles defined in the [Citation Style Language](https://github.com/citation-style-language/styles). The default style is `apa`, which is the American Psychological Association 7th Edition style. The style is not only very popular and well-documented, but is one of only a few styles that has specific support for special content types, such as `dataset` and `software`. And unlike many other styles, it includes the DOI expressed as URL in the citation.

### Journal article

```python
from commonmeta import Metadata

metadata = Metadata("10.18558/fil026")
citation = metadata.write(to="citation", style="apa", locale="en-US")
print(citation.decode())
```

```
Laborde, F. (2010). <i>Biografía de Juan Bautista Alberdi</i>. Fundación Ignacio Larramendi. https://doi.org/10.18558/fil026
```

### Conference proceedings

```python
metadata = Metadata("10.1109/iccv.2007.4408927")
citation = metadata.write(to="citation", style="apa", locale="en-US")
print(citation.decode())
```

```
Sinop, A. K., &amp; Grady, L. (2007). A Seeded Image Segmentation Framework Unifying Graph Cuts And Random Walker Which Yields A New Algorithm. In <i>2007 IEEE 11th International Conference on Computer Vision</i> (pp. 1–8). IEEE. https://doi.org/10.1109/iccv.2007.4408927
```

### Book chapter

```python
metadata = Metadata("10.1007/978-3-642-33191-6_49")
citation = metadata.write(to="citation", style="apa", locale="en-US")
print(citation.decode())
```

```
Chen, L., Panin, G., &amp; Knoll, A. (2012). Human Body Orientation Estimation in Multiview Scenarios. In <i>Lecture Notes in Computer Science</i> (pp. 499–508). Springer Berlin Heidelberg. https://doi.org/10.1007/978-3-642-33191-6_49
```

### Dataset

```python
metadata = Metadata("10.5061/dryad.8515")
citation = metadata.write(to="citation", style="apa", locale="en-US")
print(citation.decode())
```

```
Ollomo, B., Durand, P., Prugnolle, F., Douzery, E. J. P., Arnathau, C., Nkoghe, D., Leroy, E., &amp; Renaud, F. (2011). <i>Data from: A new malaria agent in African hominids.</i> (Version 1) [Dataset]. Dryad. https://doi.org/10.5061/dryad.8515
```

### Software

```python
# TODO properly handle software type
metadata = Metadata("10.5281/zenodo.48440")
citation = metadata.write(to="citation", style="apa", locale="en-US")
print(citation.decode())
```

```
Garza, K. (2016). <i>Analysis Tools for Crossover Experiment of UI using Choice Architecture</i> (Version v1.0). Zenodo. https://doi.org/10.5281/zenodo.48440
```

## Popular Citation Styles

Let's try out a few popular citation styles:

```python
# let fetch the original metadata again
metadata = Metadata("10.7554/elife.01567")
```

### American Psychological Association 7th Edition (default)

```python
citation = metadata.write(to="citation", style="apa", locale="en-US")
print(citation.decode())
```

```
Sankar, M., Nieminen, K., Ragni, L., Xenarios, I., &amp; Hardtke, C. S. (2014). Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth. <i>eLife</i>, <i>3</i>. https://doi.org/10.7554/elife.01567
```

### American Medical Association (AMA)

```python
citation = metadata.write(to="citation", style="american-medical-association", locale="en-US")
print(citation.decode())
```

```
1.Sankar M, Nieminen K, Ragni L, Xenarios I, Hardtke CS. Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth. <i>eLife</i>. 2014;3. doi:10.7554/elife.01567
```

### IEEE

```python
citation = metadata.write(to="citation", style="ieee", locale="en-US")
print(citation.decode())
```

```
[1]M. Sankar, K. Nieminen, L. Ragni, I. Xenarios, and C. S. Hardtke, “Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth”, <i>eLife</i>, vol. 3, Feb. 2014, doi: 10.7554/elife.01567.
```

### Chicago Manual of Style 17th Edition (author-date)

```python
citation = metadata.write(to="citation", style="chicago-author-date", locale="en-US")
print(citation.decode())
```

```
Sankar, M., K. Nieminen, L. Ragni, I. Xenarios, and C. S. Hardtke. 2014. “Automated Quantitative Histology Reveals Vascular Morphodynamics During Arabidopsis Hypocotyl Secondary Growth”. <i>eLife</i> 3 (February). https://doi.org/10.7554/elife.01567.
```

## Citation Locales

The other option in the citation writer is the *locale*, which is the language in which the citation is written (words like dates, not the metadata that comes from Crossref). The default locale is `en-US`, we use `es-ES` here. The locales are defined in the [Citation Style Language repository](https://github.com/citation-style-language/locales). I am using an example from Crossref where the metadata are also in Spanish.

```python
metadata = Metadata("10.18558/fil026")
metadata.locale = "es-ES"
metadata.style = "modern-language-association"
citation = metadata.write(to="citation", style="modern-language-association", locale="es-ES")
print(citation.decode())
```

```
Laborde, F. <i>Biografía De Juan Bautista Alberdi</i>. Fundación Ignacio Larramendi, 2010, https://doi.org/10.18558/fil026.
```
