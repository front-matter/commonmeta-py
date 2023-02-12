"""schema_org reader for Talbot"""
import json
import requests
from pydash import py_
from bs4 import BeautifulSoup

from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    wrap,
    compact,
    camel_case,
    parse_attributes,
    from_schema_org,
    from_schema_org_creators,
    from_schema_org_contributors,
    presence,
    sanitize,
    normalize_id,
    normalize_ids,
    normalize_url,
    name_to_fos,
    get_geolocation_point,
    get_geolocation_box,
)
from ..author_utils import get_authors
from ..date_utils import get_iso8601_date, strip_milliseconds
from ..doi_utils import doi_from_url
from ..constants import (
    SO_TO_BIB_TRANSLATIONS,
    SO_TO_CP_TRANSLATIONS,
    SO_TO_DC_TRANSLATIONS,
    SO_TO_DC_RELATION_TYPES,
    SO_TO_DC_REVERSE_RELATION_TYPES,
    SO_TO_RIS_TRANSLATIONS,
)


def get_schema_org(pid=None, **kwargs):
    """get_schema_org"""
    if pid is None:
        return {"string": None, "state": "not_found"}

    url = pid
    response = requests.get(url, kwargs, timeout=5)
    if response.status_code != 200:
        return {"string": None, "state": "not_found"}

    soup = BeautifulSoup(response.text, "html.parser")
    json_ld = soup.find("script", type="application/ld+json")
    if json_ld is not None:
        string = json.loads(json_ld.text)
    else:
        string = {}

    # workaround for doi if not included with schema.org
    if not string.get("@id", "").startswith("https://doi.org/"):
        pid = (
            soup.select_one("meta[name='citation_doi']")
            or soup.select_one("meta[name='dc.identifier']")
            or soup.select_one('[rel="canonical"]')
        )
        if pid is not None:
            string["@id"] = pid.get("content", None) or pid.get("href", None)

    # workaround for type if not included with schema.org
    if string.get("@type", None) is None:
        type_ = soup.select_one("meta[property='og:type']")
        if type_ is not None:
            string["@type"] = str(type_["content"]).capitalize()

    # workaround for url if not included with schema.org
    if string.get("url", None) is None:
        url = soup.select_one("meta[property='og:url']")
        if url is not None:
            string["url"] = url["content"]

    # workaround for title if not included with schema.org
    if string.get("name", None) is None:
        title = (
            soup.select_one("meta[name='citation_title']")
            or soup.select_one("meta[name='dc.title']")
            or soup.select_one("meta[property='og:title']")
        )
        if title is not None:
            string["name"] = title["content"]

    # workaround for description if not included with schema.org
    if string.get("description", None) is None:
        description = soup.select_one(
            "meta[name='citation_abstract']"
        ) or soup.select_one("meta[name='dc.description']")
        if description is not None:
            string["description"] = description["content"]

    # workaround for keywords if not included with schema.org
    if string.get("keywords", None) is None:
        keywords = soup.select_one("meta[name='citation_keywords']")
        if keywords is not None:
            string["keywords"] = str(keywords["content"]).replace(";", ",")

    # workaround for publication_date if not included with schema.org
    if string.get("datePublished", None) is None:
        date = soup.select_one(
            "meta[name='citation_publication_date']"
        ) or soup.select_one("meta[name='dc.date']")
        if date is not None:
            string["datePublished"] = get_iso8601_date(date["content"])

    # workaround if license not included with schema.org
    license_ = soup.select_one("meta[name='dc.rights']")
    if license_ is not None:
        string["license"] = license_["content"]

    # workaround for html language attribute if no language is set via schema.org
    if string.get("inLanguage", None) is None:
        lang = soup.select_one("meta[name='dc.language']") or soup.select_one(
            "meta[name='citation_language']"
        )
        if lang is not None:
            string["inLanguage"] = lang["content"]
        else:
            lang = soup.select_one("html")["lang"]
            if lang is not None:
                string["inLanguage"] = lang

    # workaround if issn not included with schema.org
    name = soup.select_one("meta[property='og:site_name']")
    issn = soup.select_one("meta[name='citation_issn']")
    string["isPartOf"] = compact(
        {
            "name": name["content"] if name else None,
            "issn": issn["content"] if issn else None,
        }
    )

    # workaround if not all authors are included with schema.org (e.g. in Ghost metadata)
    auth = soup.select("meta[name='citation_author']")
    authors = []
    for aut in auth:
        length = len(str(aut["content"]).split(" "))
        if length == 0:
            continue
        if length == 1:
            author = {"@type": "Organization", "name": str(aut["content"])}
        else:
            given_name = " ".join(
                str(aut["content"]).split(" ")[0: length - 1])
            author = {
                "@type": "Person",
                "name": str(aut["content"]),
                "givenName": given_name,
                "familyName": str(aut["content"]).rsplit(' ', maxsplit=1)[-1],
            }
        authors.append(author)

    if string.get("author", None) is None and string.get("creator", None) is not None:
        string["author"] = string["creator"]
    if len(authors) > len(wrap(string.get("author", None))):
        string["author"] = authors

    # workaround if publisher not included with schema.org (e.g. Zenodo)
    if string.get("publisher", None) is None:
        publisher = soup.select_one("meta[property='og:site_name']")
        string["publisher"] = compact(
            {"name": publisher["content"] if publisher else None}
        )

    return string


def read_schema_org(string=None, **kwargs):
    """read_schema_org"""
    if string is None:
        return {"meta": None, "state": "not_found"}
    meta = string

    read_options = kwargs or {}

    pid = meta.get("@id", None)
    doi = doi_from_url(pid)
    types = None

    # if id.blank? && URI(meta.fetch('@id', '')).host == 'doi.org'
    if pid is None:
        pid = meta.get("identifier", None)
    pid = normalize_id(pid)

    schema_org = (
        camel_case(meta.get("@type")) if meta.get("@type",
                                                  None) else "CreativeWork"
    )
    resource_type_general = SO_TO_DC_TRANSLATIONS.get(schema_org, None)
    types = compact(
        {
            "resourceTypeGeneral": resource_type_general,
            "resourceType": meta.get("additionalType", None),
            "schemaOrg": schema_org,
            "citeproc": SO_TO_CP_TRANSLATIONS.get(schema_org, None)
            or "article-journal",
            "bibtex": SO_TO_BIB_TRANSLATIONS.get(schema_org, None) or "misc",
            "ris": SO_TO_RIS_TRANSLATIONS.get(resource_type_general, None) or "GEN",
        }
    )
    authors = meta.get("author", None) or meta.get("creator", None)
    # Authors should be an object, if it's just a plain string don't try and parse it.
    if not isinstance(authors, str):
        creators = get_authors(from_schema_org_creators(wrap(authors)))
    else:
        creators = authors

    contributors = presence(
        get_authors(from_schema_org_contributors(
            wrap(meta.get("editor", None))))
    )

    if meta.get("name", None) is not None:
        titles = [{"title": meta.get("name")}]
    elif meta.get("headline", None) is not None:
        titles = [{"title": meta.get("headline")}]
    else:
        titles = None

    published_date = strip_milliseconds(meta.get("datePublished", None))
    updated_date = strip_milliseconds(meta.get("dateModified", None))
    dates = [{"date": published_date, "dateType": "Issued"}]
    if updated_date is not None:
        dates.append({"date": updated_date, "dateType": "Updated"})
    publication_year = published_date[0:4] if published_date else None

    publisher = parse_attributes(
        meta.get("publisher", None), content="name", first=True
    )

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_)
        rights_list = [dict_to_spdx(
            {"rightsURI": license_})] if license_ else None
    else:
        rights_list = None

    issn = py_.get(meta, "isPartOf.issn", None)
    cet = "includedInDataCatalog" if schema_org in [
        "Dataset", "Periodical"] else None
    if cet is not None:
        url = parse_attributes(
            from_schema_org(meta.get(cet, None)), content="url", first=True
        )
        container = compact(
            {
                "type": "DataRepository" if schema_org == "Dataset" else "Periodical",
                "title": parse_attributes(
                    from_schema_org(meta.get(cet, None)), content="name", first=True
                ),
                "identifier": url,
                "identifierType": "URL" if url is not None else None,
                "volume": meta.get("volumeNumber", None),
                "issue": meta.get("issueNumber", None),
                "firstPage": meta.get("pageStart", None),
                "lastPage": meta.get("pageEnd", None),
            }
        )
    elif schema_org in ("Article", "BlogPosting"):
        url = py_.get(meta, "publisher.url", None)
        container = compact(
            {
                "type": "Blog",
                "title": py_.get(meta, "isPartOf.name", None),
                "identifier": issn
                if issn is not None
                else url
                if url is not None
                else None,
                "identifierType": "ISSN"
                if issn is not None
                else "URL"
                if url is not None
                else None,
            }
        )
    else:
        container = {}

    related_items = (
        wrap(schema_org_is_identical_to(meta))
        + wrap(schema_org_is_part_of(meta))
        + wrap(schema_org_has_part(meta))
        + wrap(schema_org_is_previous_version_of(meta))
        + wrap(schema_org_is_new_version_of(meta))
        + wrap(schema_org_references(meta))
        + wrap(schema_org_is_referenced_by(meta))
        + wrap(schema_org_is_supplement_to(meta))
        + wrap(schema_org_is_supplemented_by(meta))
    )

    funding_references = py_.map(
        compact(wrap(meta.get("funder", None))),
        lambda fr: compact(  # noqa: E501
            {
                "funderName": fr.get("name", None),
                "funderIdentifier": fr.get("@id", None),
                "funderIdentifierType": "Crossref Funder ID"
                if fr.get("@id", None) is not None
                else None,  # noqa: E501
            }
        ),
    )
    # if fr['@id'].present?
    #   {
    #     'funderName' => fr['name'],
    #     'funderIdentifier' => fr['@id'],
    #     'funderIdentifierType' => fr['@id'].to_s.start_with?('https://doi.org/10.13039') ? 'Crossref Funder ID' : 'Other'
    #   }.compact
    # else
    #   { 'funderName' => fr['name'] }.compact

    if meta.get("description", None) is not None:
        descriptions = [
            {
                "description": sanitize(meta.get("description")),
                "descriptionType": "Abstract",
            }
        ]
    else:
        descriptions = None

    # handle keywords as array and as comma-separated string
    subj = meta.get("keywords", None)
    if isinstance(subj, str):
        subj = subj.lower().split(", ")
    subjects = []
    for subject in wrap(subj):
        if subject.strip() != "":
            subjects += name_to_fos(subject)

    if isinstance(meta.get("inLanguage"), str):
        language = meta.get("inLanguage")
    elif isinstance(meta.get("inLanguage"), list):
        language = py_.get(meta, "inLanguage.0", None)
    elif isinstance(meta.get("inLanguage"), dict):
        language = py_.get(meta, "inLanguage.alternateName", None) or py_.get(
            meta, "inLanguage.name", None
        )
    else:
        language = None

    geo_locations = schema_org_geolocations(meta)

    alternate_identifiers = None
    state = None

    return {
        # required attributes
        "pid": pid,
        "doi": doi,
        "url": normalize_url(meta.get("url", None)),
        "creators": creators,
        "titles": titles,
        "publisher": publisher,
        "publication_year": publication_year,
        "types": types,
        # recommended and optional attributes
        "subjects": presence(subjects),
        "contributors": contributors,
        "dates": dates,
        "language": language,
        "alternate_identifiers": alternate_identifiers,
        "sizes": None,
        "formats": None,
        "version": meta.get("version", None),
        "rights_list": rights_list,
        "descriptions": descriptions,
        "geo_locations": presence(geo_locations),
        "funding_references": presence(funding_references),
        "related_items": related_items,
        # optional attributes
        "container": container,
        "agency": parse_attributes(
            meta.get("provider", None), content="name", first=True
        ),
        "state": state
    } | read_options


def schema_org_related_item(meta, relation_type=None):
    """Related items"""
    normalize_ids(
        ids=meta.get(relation_type, None),
        relation_type=SO_TO_DC_RELATION_TYPES.get(relation_type),
    )


def schema_org_reverse_related_item(meta, relation_type=None):
    """Reverse related items"""
    normalize_ids(
        ids=py_.get(meta, f"@reverse.{relation_type}", None),
        relation_type=SO_TO_DC_REVERSE_RELATION_TYPES.get(relation_type),
    )


def schema_org_is_identical_to(meta):
    """isIdenticalTo is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="sameAs")


def schema_org_is_part_of(meta):
    """isPartOf is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="isPartOf")


def schema_org_has_part(meta):
    """hasPart is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="hasPart")


def schema_org_is_previous_version_of(meta):
    """isPreviousVersionOf is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="PredecessorOf")


def schema_org_is_new_version_of(meta):
    """isNewVersionOf is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="SuccessorOf")


def schema_org_references(meta):
    """references is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="citation")


def schema_org_is_referenced_by(meta):
    """isReferencedBy is a special case because it can be a string or an object."""
    schema_org_reverse_related_item(meta, relation_type="citation")


def schema_org_is_supplement_to(meta):
    """isSupplementTo is a special case because it can be a string or an object."""
    schema_org_reverse_related_item(meta, relation_type="isBasedOn")


def schema_org_is_supplemented_by(meta):
    """isSupplementedBy is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="isBasedOn")


def schema_org_geolocations(meta):
    """Geolocations in Schema.org format"""
    if meta.get("spatialCoverage", None) is None:
        return None
    geo_locations = []
    for geo_location in wrap(meta.get("spatialCoverage", None)):
        formatted_geo_location = {}
        geo_location_place = {'geoLocationPlace': py_.get(
            geo_location, "geo.address", None)}
        geo_location_point = get_geolocation_point(geo_location)
        geo_location_box = get_geolocation_box(geo_location)
        for location in [geo_location_place, geo_location_point, geo_location_box]:
            for key, val in location.items():
                formatted_geo_location.setdefault(key, []).append(val)
        geo_locations.append(geo_location_point)
    return geo_locations
