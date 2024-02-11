"""schema_org reader for commonmeta-py"""
from typing import Optional
import json
from collections import defaultdict
import httpx
from pydash import py_
from bs4 import BeautifulSoup

from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    from_schema_org,
    from_schema_org_creators,
    normalize_id,
    normalize_ids,
    normalize_url,
    name_to_fos,
)
from ..base_utils import wrap, compact, presence, parse_attributes, sanitize
from ..author_utils import get_authors
from ..date_utils import get_iso8601_date, strip_milliseconds
from ..doi_utils import doi_from_url, get_doi_ra
from ..constants import (
    SO_TO_CM_TRANSLATIONS,
    SO_TO_DC_RELATION_TYPES,
    SO_TO_DC_REVERSE_RELATION_TYPES,
    Commonmeta,
)


def get_schema_org(pid: str, **kwargs) -> dict:
    """get_schema_org"""
    if pid is None:
        return {"state": "not_found"}
    url = pid
    response = httpx.get(url, timeout=10, follow_redirects=True, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}

    soup = BeautifulSoup(response.text, "html.parser")
    # workaround for metadata not included with schema.org but in html meta tags
    data = get_html_meta(soup)
    # load schema.org metadata
    json_ld = soup.find("script", type="application/ld+json")
    if json_ld is not None:
        data |= json.loads(json_ld.text)

    # workaround if not all authors are included with schema.org (e.g. in Ghost metadata)
    auth = soup.select("meta[name='citation_author']")

    def format_author(author):
        return {"name": author["content"]}

    authors = [format_author(i) for i in auth]

    if data.get("author", None) is None and data.get("creator", None) is not None:
        data["author"] = data["creator"]
    if len(authors) > len(wrap(data.get("author", None))):
        data["author"] = authors

    return data


def read_schema_org(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_schema_org"""
    if data is None:
        return {"meta": None, "state": "not_found"}
    meta = data

    read_options = kwargs or {}

    _id = meta.get("@id", None)
    if _id is None:
        _id = meta.get("identifier", None)
    _id = normalize_id(_id)
    _type = SO_TO_CM_TRANSLATIONS.get(meta.get("@type", None), "Other")
    additional_type = meta.get("additionalType", None)
    authors = meta.get("author", None) or meta.get("creator", None)
    # Authors should be an object, if it's just a plain string don't try and parse it.
    if not isinstance(authors, str):
        contributors = get_authors(from_schema_org_creators(wrap(authors)))
    else:
        contributors = authors
    contrib = presence(
        get_authors(from_schema_org_creators(wrap(meta.get("editor", None))))
    )
    if contrib:
        contributors = contributors + contrib

    if meta.get("name", None) is not None:
        titles = [{"title": meta.get("name")}]
    elif meta.get("headline", None) is not None:
        titles = [{"title": meta.get("headline")}]
    else:
        titles = None

    date: dict = defaultdict(list)
    date["published"] = strip_milliseconds(meta.get("datePublished", None))
    date["updated"] = strip_milliseconds(meta.get("dateModified", None))

    publisher = meta.get("publisher", None)
    if publisher is not None:
        publisher = py_.omit(
            publisher, ["@type", "logo", "url", "disambiguatingDescription"]
        )

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_)
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    if _type == "Dataset":
        url = parse_attributes(
            from_schema_org(meta.get("includedInDataCatalog", None)),
            content="url",
            first=True,
        )
        container = compact(
            {
                "type": "DataRepository",
                "title": parse_attributes(
                    from_schema_org(meta.get("includedInDataCatalog", None)),
                    content="name",
                    first=True,
                ),
                "identifier": url,
                "identifierType": "URL" if url is not None else None,
                "volume": meta.get("volumeNumber", None),
                "issue": meta.get("issueNumber", None),
                "firstPage": meta.get("pageStart", None),
                "lastPage": meta.get("pageEnd", None),
            }
        )
    elif _type == "Article":
        issn = py_.get(meta, "isPartOf.issn")
        url = py_.get(meta, "publisher.url")
        container = compact(
            {
                "type": "Periodical",
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

    references = wrap(schema_org_references(meta))
    funding_references = [
        get_funding_reference(i) for i in wrap(meta.get("funder", None))
    ]

    descriptions = [
        {
            "description": sanitize(i),
            "descriptionType": "Abstract",
        }
        for i in wrap(meta.get("description"))
    ]

    # convert keywords as comma-separated string into list
    subj = meta.get("keywords", None)
    if isinstance(subj, str):
        subj = subj.lower().split(", ")
    subjects = [name_to_fos(i) for i in wrap(subj)]

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

    geo_locations = [
        schema_org_geolocation(i) for i in wrap(meta.get("spatialCoverage", None))
    ]
    alternate_identifiers = None
    provider = (
        get_doi_ra(_id)
        if doi_from_url(_id)
        else parse_attributes(meta.get("provider", None), content="name", first=True)
    )
    state = None

    return {
        # required attributes
        "id": _id,
        "type": _type,
        "url": normalize_url(meta.get("url", None)),
        "contributors": contributors,
        "titles": titles,
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional attributes
        "additional_type": additional_type,
        "subjects": presence(subjects),
        "language": language,
        "alternate_identifiers": alternate_identifiers,
        "sizes": None,
        "formats": None,
        "version": meta.get("version", None),
        "license": license_,
        "descriptions": presence(descriptions),
        "geo_locations": presence(geo_locations),
        "funding_references": presence(funding_references),
        "references": presence(references),
        # optional attributes
        "container": container,
        "provider": provider,
        "state": state,
    } | read_options


def schema_org_related_item(meta, relation_type=None):
    """Related items"""
    normalize_ids(
        ids=wrap(meta.get(relation_type, None)),
        relation_type=SO_TO_DC_RELATION_TYPES.get(relation_type),
    )


def schema_org_reverse_related_item(meta, relation_type=None):
    """Reverse related items"""
    normalize_ids(
        ids=wrap(py_.get(meta, f"@reverse.{relation_type}")),
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


def schema_org_geolocation(geo_location: Optional[dict]) -> Optional[dict]:
    """Geolocations in Schema.org format"""
    if not isinstance(geo_location, dict):
        return None

    _type = py_.get(geo_location, "geo.@type")
    longitude = py_.get(geo_location, "geo.longitude")
    latitude = py_.get(geo_location, "geo.latitude")

    if _type == "GeoCoordinates":
        return {
            "geoLocationPoint": {"pointLongitude": longitude, "pointLatitude": latitude}
        }
    return None


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

    _type = soup.select_one("meta[property='og:type']")
    data["@type"] = _type["content"].capitalize() if _type else None

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
        str(keywords["content"]).replace(";", ",").rstrip(", ") if keywords else None
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


def get_funding_reference(dct):
    """Get funding reference"""
    return compact(
        {
            "funderName": dct.get("name", None),
            "funderIdentifier": dct.get("@id", None),
            "funderIdentifierType": "Crossref Funder ID"
            if dct.get("@id", None)
            else None,
        }
    )
