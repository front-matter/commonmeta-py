"""schema_org reader for Talbot"""
from typing import Optional
import json
import requests
from pydash import py_
from bs4 import BeautifulSoup

from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    from_schema_org,
    from_schema_org_creators,
    from_schema_org_contributors,
    normalize_id,
    normalize_ids,
    normalize_url,
    name_to_fos,
    get_geolocation_point,
    get_geolocation_box,
)
from ..base_utils import wrap, compact, presence, parse_attributes, sanitize
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
    TalbotMeta,
)


def get_schema_org(pid: Optional[str], **kwargs) -> dict:
    """get_schema_org"""
    if pid is None:
        return {"string": None, "state": "not_found"}

    url = pid
    response = requests.get(url, kwargs, timeout=5)
    if response.status_code != 200:
        return {"string": None, "state": "not_found"}

    soup = BeautifulSoup(response.text, "html.parser")
    # workaround for metadata not included with schema.org but in html meta tags
    data = get_html_meta(soup)
    # load schema.org metadata
    json_ld = soup.find("script", type="application/ld+json")
    if json_ld is not None:
        data |= json.loads(json_ld.text)

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
                "familyName": str(aut["content"]).rsplit(" ", maxsplit=1)[-1],
            }
        authors.append(author)

    if data.get("author", None) is None and data.get("creator", None) is not None:
        data["author"] = data["creator"]
    if len(authors) > len(wrap(data.get("author", None))):
        data["author"] = authors

    return data


def read_schema_org(data: Optional[dict], **kwargs) -> TalbotMeta:
    """read_schema_org"""
    if data is None:
        return {"meta": None, "state": "not_found"}
    meta = data

    read_options = kwargs or {}

    pid = meta.get("@id", None)
    doi = doi_from_url(pid)
    types = None

    # if id.blank? && URI(meta.fetch('@id', '')).host == 'doi.org'
    if pid is None:
        pid = meta.get("identifier", None)
    pid = normalize_id(pid)

    schema_org = meta.get("@type") if meta.get("@type",
                                               None) else "CreativeWork"
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
    publication_year = int(published_date[0:4]) if published_date else None

    publisher = parse_attributes(
        meta.get("publisher", None), content="name", first=True
    )

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_)
        rights = [dict_to_spdx({"rightsUri": license_})] if license_ else None
    else:
        rights = None

    issn = py_.get(meta, "isPartOf.issn")
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
        url = py_.get(meta, "publisher.url")
        container = compact(
            {
                "type": "Blog",
                "title": py_.get(meta, "isPartOf.name"),
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
        wrap(meta.get("funder", None)),
        lambda fr: compact(  # noqa: E501
            {
                "funderName": fr.get("name", None),
                "funderIdentifier": fr.get("@id", None),
                "funderIdentifierType": "Crossref Funder ID"
                if fr.get("@id", None)
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

    # convert keywords as comma-separated string into list
    subj = meta.get("keywords", None)
    if isinstance(subj, str):
        subj = subj.lower().split(", ")
    subjects = py_.map(wrap(subj), name_to_fos)

    if isinstance(meta.get("inLanguage"), str):
        language = meta.get("inLanguage")
    elif isinstance(meta.get("inLanguage"), list):
        language = py_.get(meta, "inLanguage.0")
    elif isinstance(meta.get("inLanguage"), dict):
        language = py_.get(meta, "inLanguage.alternateName") or py_.get(
            meta, "inLanguage.name"
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
        "rights": rights,
        "descriptions": descriptions,
        "geo_locations": presence(geo_locations),
        "funding_references": presence(funding_references),
        "related_items": related_items,
        # optional attributes
        "container": container,
        "agency": parse_attributes(
            meta.get("provider", None), content="name", first=True
        ),
        "state": state,
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
        ids=py_.get(meta, f"@reverse.{relation_type}"),
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
        geo_location_place = {"geoLocationPlace": py_.get(
            geo_location, "geo.address")}
        geo_location_point = get_geolocation_point(geo_location)
        geo_location_box = get_geolocation_box(geo_location)
        for location in [geo_location_place, geo_location_point, geo_location_box]:
            for key, val in location.items():
                formatted_geo_location.setdefault(key, []).append(val)
        geo_locations.append(geo_location_point)
    return geo_locations


def get_html_meta(soup):
    """Get metadata from HTML meta tags"""
    data = {}
    pid = (
        soup.select_one("meta[name='citation_doi']")
        or soup.select_one("meta[name='dc.identifier']")
        or soup.select_one('[rel="canonical"]')
    )
    if pid is not None:
        data["@id"] = pid.get("content", None) or pid.get("href", None)

    type_ = soup.select_one("meta[property='og:type']")
    data["@type"] = type_["content"].capitalize() if type_ else None

    url = soup.select_one("meta[property='og:url']")
    data["url"] = url["content"] if url else None

    title = (
        soup.select_one("meta[name='citation_title']")
        or soup.select_one("meta[name='dc.title']")
        or soup.select_one("meta[property='og:title']")
    )
    data["name"] = title["content"] if title else None

    description = soup.select_one("meta[name='citation_abstract']") or soup.select_one(
        "meta[name='dc.description']"
    )
    data["description"] = description["content"] if description else None

    keywords = soup.select_one("meta[name='citation_keywords']")
    data["keywords"] = (
        str(keywords["content"]).replace(
            ";", ",").rstrip(", ") if keywords else None
    )

    date_published = soup.select_one(
        "meta[name='citation_publication_date']"
    ) or soup.select_one("meta[name='dc.date']")
    data["datePublished"] = (
        get_iso8601_date(date_published["content"]) if date_published else None
    )

    license_ = soup.select_one("meta[name='dc.rights']")
    data["license"] = license_["content"] if license_ else None

    lang = soup.select_one("meta[name='dc.language']") or soup.select_one(
        "meta[name='citation_language']"
    )
    if lang is not None:
        data["inLanguage"] = lang["content"]
    else:
        lang = soup.select_one("html")["lang"]
        if lang is not None:
            data["inLanguage"] = lang

    publisher = soup.select_one("meta[property='og:site_name']")
    data["publisher"] = {"name": publisher["content"]} if publisher else None

    name = soup.select_one("meta[property='og:site_name']")
    issn = soup.select_one("meta[name='citation_issn']")
    data["isPartOf"] = compact(
        {
            "name": name["content"] if name else None,
            "issn": issn["content"] if issn else None,
        }
    )
    return data
