---
title: SchemaOrg Reader
weight: 50
---

This page shows how to read metadata from Schema.org, using a URL with embedded Schema.org JSON-LD.

## Fetch metadata

```python
from commonmeta import Metadata

# Fetch metadata from a URL pointing to a landing page for a scholary resource
string = "https://doi.pangaea.de/10.1594/PANGAEA.836178"
metadata = Metadata(string)

# Check that metadata was fetched and is valid
print(metadata.is_valid)
```

```
True
```

## Inspect the metadata


The metadata are optionally embedded in the HTML of the page, using the [JSON-LD](https://json-ld.org/) format. The metadata are embedded in a `<script>` tag with the `type` attribute set to `application/ld+json` They are converted into the internal commonmeta format.

* `id`: the persistent identifier of the resource
* `type`: the type of the resource in commmonmeta format, e.g `Dataset`, `Software` or `JournalArticle`
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
{"id":"https://doi.org/10.1594/pangaea.836178","type":"Dataset","additional_type":"Supplementary Dataset","container":{"identifiers":[{"identifier":"pangaea.repository","identifier_type":"DataCite"}]},"contributors":[{"type":"Person","person":{"given_name":"Emma","family_name":"Johansson"},"roles":["Author"]},{"type":"Person","person":{"given_name":"Sten","family_name":"Berglund"},"roles":["Author"]},{"type":"Person","person":{"given_name":"Tobias","family_name":"Lindborg"},"roles":["Author"]},{"type":"Person","person":{"given_name":"Johannes","family_name":"Petrone"},"roles":["Author"]},{"type":"Person","person":{"id":"https://orcid.org/0000-0002-6553-8982","given_name":"Dirk","family_name":"van As"},"roles":["Author"]},{"type":"Person","person":{"given_name":"Lars-Göran","family_name":"Gustafsson"},"roles":["Author"]},{"type":"Person","person":{"given_name":"Jens-Ove","family_name":"Näslund"},"roles":["Author"]},{"type":"Person","person":{"id":"https://orcid.org/0000-0001-6058-1466","given_name":"Hjalmar","family_name":"Laudon"},"roles":["Author"]}],"title":"Hydrological and meteorological investigations in a lake near Kangerlussuaq, west Greenland","date_published":"2014","description":"Few hydrological studies have been made in Greenland, other than on glacial hydrology associated with the ice sheet. Understanding permafrost hydrology and hydroclimatic change and variability, however, provides key information for understanding climate change effects and feedbacks in the Arctic landscape. This paper presents a new extensive and detailed hydrological and meteorological open access dataset, with high temporal resolution from a 1.56 km**2 permafrost catchment with a lake underlain by a through talik close to the ice sheet in the Kangerlussuaq region, western Greenland. The paper describes the hydrological site investigations and utilized equipment, as well as the data collection and processing. The investigations were performed between 2010 and 2013. The high spatial resolution, within the investigated area, of the dataset makes it highly suitable for various detailed hydrological and ecological studies on catchment scale.","additional_descriptions":[{"description":"The dataset contains hydrological and meteorological data from a lake catchment in the Kangerlussuaq region, Western Greenland. The investigations were performed during 2010-2013 and the following parameters are included: Soil moisture, Soil temperature, Hydraulic properties of the active layer, meteorological parameters from a local weather station within the catchment, water levels and discharge, sublimation and evaportation measurments, snow depth and snow water content data and time lapse photos.","type":"TechnicalInfo"},{"description":"Supplement to: Johansson, Emma; Berglund, Sten; Lindborg, Tobias; Petrone, Johannes; van As, Dirk; Gustafsson, Lars-Göran; Näslund, Jens-Ove; Laudon, Hjalmar (2015): Hydrological and meteorological investigations in a periglacial lake catchment near Kangerlussuaq, west Greenland – presentation of a new multi-parameter data set. Earth System Science Data, 7(1), 93-108","type":"Other"}],"geo_locations":[{"point_longitude":-50.18037,"point_latitude":67.12594},{"place":"Two Boat Lake, Kangerlussuaq, Greenland"}],"language":"en","license":{"id":"CC-BY-3.0","title":"Creative Commons Attribution 3.0 Unported","url":"https://creativecommons.org/licenses/by/3.0/legalcode"},"provider":"DataCite","publisher":{"name":"PANGAEA"},"relations":[{"id":"https://doi.org/10.5194/essd-7-93-2015","type":"IsSupplementTo"}],"subjects":[{"subject":"Multiple investigations","scheme":"Method"},{"subject":"GReenland Analogue Surface Project (GRASP)","scheme":"Project"}],"url":"https://doi.pangaea.de/10.1594/PANGAEA.836178","schema_version":"https://commonmeta.org/commonmeta_v1.0.json"}
```

## Enhance the metadata with HTML meta tags

The metadata are enhanced with the following HTML meta tags: `citation_doi`, `citation_author`, `citation_title`, `citation_publisher`, `citation_publication_date`, `citation_keywords`, `citation_language`, `citation_issn`. These tags are recommended by [Google Scholar](https://scholar.google.com/intl/en/scholar/inclusion.html#indexing) and widely used by publishers and repositories. Below is an example with embedded HTML meta tags not using Schema.org:

```python
url = "https://verfassungsblog.de/einburgerung-und-ausburgerung"
metadata = Metadata(url)
commonmeta = metadata.write()
print(commonmeta.decode())
```

```
{"id":"https://verfassungsblog.de/einburgerung-und-ausburgerung/","type":"Preprint","container":{"type":"Periodical"},"title":"Einbürgerung und Ausbürgerung","date_published":"2022-12-09T11:51:01Z","date_updated":"2023-02-17T11:40:32Z","description":"Die von der Bundesinnenministerin vorangetriebene Staatsangehörigkeitsrechtsreform zur Erleichterung der Einbürgerung wirft altbekannte Fragen der Zuordnung von Personen zu Staaten und die damit verbundenen Zugehörigkeitsvorstellungen zu einem Staatsvolk auf. Allerdings liegt auch bei dem aktuellen Reformvorhaben die Aufmerksamkeit nur auf dem Erwerb der Staatsangehörigkeit. Dieser Fokus lässt die andere Seite der Medaille unberücksichtigt: Um die Möglichkeit von Mehrstaatigkeit konsequent für das gesamte Staatsangehörigkeitsrecht umzusetzen, muss die Diskussion zusätzlich für das Ausbürgerungsrecht geführt werden.","publisher":{"name":"Verfassungsblog"},"subjects":[{"subject":"Bundesinnenministerium"},{"subject":"Einbürgerung"},{"subject":"Mehrstaatigkeit"},{"subject":"staatsangehörigkeit"}],"url":"https://verfassungsblog.de/einburgerung-und-ausburgerung/","schema_version":"https://commonmeta.org/commonmeta_v1.0.json"}
```
