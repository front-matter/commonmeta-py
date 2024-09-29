"""schema_org reader for commonmeta-py"""

from typing import Optional
import io
import orjson as json
from datetime import datetime
from collections import defaultdict
import httpx
from pydash import py_
from bs4 import BeautifulSoup
import pikepdf

from ..utils import (
    dict_to_spdx,
    normalize_cc_url,
    from_schema_org,
    from_schema_org_creators,
    normalize_id,
    normalize_ids,
    normalize_url,
    name_to_fos,
    get_language,
)
from ..readers.crossref_reader import get_crossref
from ..readers.datacite_reader import get_datacite
from ..base_utils import wrap, compact, presence, parse_attributes, sanitize
from ..author_utils import get_authors
from ..date_utils import (
    get_iso8601_date,
    strip_milliseconds,
    get_datetime_from_pdf_time,
)
from ..doi_utils import doi_from_url, get_doi_ra, validate_doi
from ..translators import web_translator
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

    # if pid represents a DOI, get metadata from Crossref or DataCite
    if doi_from_url(pid):
        return get_doi_meta(doi_from_url(pid))
    try:
        response = httpx.get(url, timeout=10, follow_redirects=True, **kwargs)
    except httpx.ConnectError as error:
        return {
            "@id": url,
            "@type": "WebPage",
            "state": "not_found",
            "via": "schema_org",
            "errors": [str(error)],
        }

    if response.status_code >= 400:
        if response.status_code in [404, 410]:
            state = "not_found"
        elif response.status_code in [401, 403]:
            state = "forbidden"
        else:
            state = "bad_request"
        return {"@id": url, "@type": "WebPage", "state": state, "via": "schema_org"}
    elif response.headers.get("content-type") == "application/pdf":
        try:
            pdf = pikepdf.Pdf.open(io.BytesIO(response.content))
            meta = pdf.docinfo if pdf.docinfo else {}
            if meta.get("/doi", None) is not None:
                return get_doi_meta(meta.get("/doi"))
            date_modified = (
                get_datetime_from_pdf_time(meta.get("/ModDate"))
                if meta.get("/ModDate", None)
                else None
            )
            name = meta.get("/Title", None)
            return compact(
                {
                    "@id": url,
                    "@type": "DigitalDocument",
                    "via": "schema_org",
                    "name": str(name),
                    "datePublished": date_modified,
                    "dateAccessed": datetime.now().isoformat("T", "seconds")
                    if date_modified is None
                    else None,
                }
            )
        except Exception as error:
            print(error)
            return {
                "@id": url,
                "@type": "WebPage",
                "state": "bad_request",
                "via": "schema_org",
            }

    soup = BeautifulSoup(response.text, "html.parser")

    # load html meta tags
    data = get_html_meta(soup)

    # load site-specific metadata
    data |= web_translator(soup, url)

    # load schema.org metadata. If there are multiple schema.org blocks, load them all,
    # and pick the first one with a supported type
    list = [
        json.loads(x.text) for x in soup.find_all("script", type="application/ld+json")
    ]
    json_ld = next(
        (i for i in list if i.get("@type", None) in SO_TO_CM_TRANSLATIONS),
        None,
    )
    if json_ld is not None:
        data |= json_ld

    # if @id is a DOI, get metadata from Crossref or DataCite
    if validate_doi(data.get("@id", None)):
        return get_doi_meta(data.get("@id", None))

    # if @id is None, use url
    elif data.get("@id", None) is None:
        data["@id"] = url

    # if @type is None, use WebSite
    elif data.get("@type", None) is None:
        data["@type"] = "WebSite"

    # author and creator are synonyms
    if data.get("author", None) is None and data.get("creator", None) is not None:
        data["author"] = data["creator"]

    return data | {"via": "schema_org", "state": "findable"}


def read_schema_org(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_schema_org"""
    if (
        data is None
        or isinstance(data, dict)
        and data.get("state", None) in ["not_found", "forbidden", "bad_request"]
    ):
        return from_schema_org(data)
    meta = data

    read_options = kwargs or {}

    _id = meta.get("@id", None)
    if _id is None:
        _id = meta.get("identifier", None)
    _id = normalize_id(_id)
    _type = SO_TO_CM_TRANSLATIONS.get(meta.get("@type", None), "WebPage")
    additional_type = meta.get("additionalType", None)
    url = normalize_url(meta.get("url", None)) or _id

    # Authors should be list of objects or strings
    authors = wrap(meta.get("author", None))
    contributors = get_authors(from_schema_org_creators(authors))
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
    # if no date is found, use today's date
    if date == {"published": None, "updated": None}:
        date["accessed"] = read_options.get(
            "dateAccessed", None
        ) or datetime.now().isoformat("T", "seconds")

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
        container_url = parse_attributes(
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
                "identifier": container_url,
                "identifierType": "URL" if container_url is not None else None,
                "volume": meta.get("volumeNumber", None),
                "issue": meta.get("issueNumber", None),
                "firstPage": meta.get("pageStart", None),
                "lastPage": meta.get("pageEnd", None),
            }
        )
    elif _type == "Article":
        issn = py_.get(meta, "isPartOf.issn")
        container_url = py_.get(meta, "publisher.url")
        container = compact(
            {
                "type": "Periodical",
                "title": py_.get(meta, "isPartOf.name"),
                "identifier": issn
                if issn is not None
                else container_url
                if container_url is not None
                else None,
                "identifierType": "ISSN"
                if issn is not None
                else "URL"
                if container_url is not None
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
            "type": "Abstract",
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
    identifiers = None
    provider = (
        get_doi_ra(_id)
        if doi_from_url(_id)
        else parse_attributes(meta.get("provider", None), content="name", first=True)
    )
    state = "findable"

    return {
        # required attributes
        "id": _id,
        "type": _type,
        "url": url,
        "contributors": presence(contributors),
        "titles": titles,
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional attributes
        "additional_type": additional_type,
        "subjects": presence(subjects),
        "language": get_language(language),
        "identifiers": identifiers,
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


def get_doi_meta(doi: str) -> Optional[dict]:
    """get_doi_meta"""
    ra = get_doi_ra(doi)
    if ra == "Crossref":
        return get_crossref(doi)
    elif ra == "DataCite":
        return get_datacite(doi)
    return None


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
        or soup.select_one("meta[name='DC.identifier']")
        or soup.select_one("meta[name='bepress_citation_doi']")
        or soup.select_one('[rel="canonical"]')
    )
    if pid is not None:
        pid = pid.get("content", None) or pid.get("href", None)
        data["@id"] = normalize_id(pid)

    _type = (
        soup.select_one("meta[property='og:type']")
        or soup.select_one("meta[name='dc.type']")
        or soup.select_one("meta[name='DC.type']")
    )
    data["@type"] = _type["content"].capitalize() if _type else None

    url = soup.select_one("meta[property='og:url']") or soup.select_one(
        "meta[name='twitter:url']"
    )
    data["url"] = url["content"] if url else None
    if pid is None and url is not None:
        data["@id"] = url["content"]

    title = (
        soup.select_one("meta[name='citation_title']")
        or soup.select_one("meta[name='dc.title']")
        or soup.select_one("meta[name='DC.title']")
        or soup.select_one("meta[property='og:title']")
        or soup.select_one("meta[name='twitter:title']")
    )
    data["name"] = title["content"] if title else None

    author = soup.select("meta[name='citation_author']")
    data["author"] = [i["content"] for i in author] if author else None

    description = soup.select_one("meta[name='citation_abstract']") or soup.select_one(
        "meta[name='dc.description']"
        or soup.select_one("meta[property='og:description']")
        or soup.select_one("meta[name='twitter:description']")
    )
    data["description"] = description["content"] if description else None

    keywords = soup.select_one("meta[name='citation_keywords']")
    data["keywords"] = (
        str(keywords["content"]).replace(";", ",").rstrip(", ") if keywords else None
    )

    date_published = (
        soup.select_one("meta[name='citation_publication_date']")
        or soup.select_one("meta[name='dc.date']")
        or soup.select_one("meta[property='article:published_time']")
    )
    data["datePublished"] = (
        get_iso8601_date(date_published["content"]) if date_published else None
    )
    date_modified = soup.select_one(
        "meta[property='og:updated_time']"
        or soup.select_one("meta[property='article:modified_time']")
    )
    data["dateModified"] = (
        get_iso8601_date(date_modified["content"]) if date_modified else None
    )
    license_ = soup.select_one("meta[name='dc.rights']")
    data["license"] = license_["content"] if license_ else None

    lang = soup.select_one("meta[name='dc.language']") or soup.select_one(
        "meta[name='citation_language']"
    )
    if lang is not None:
        data["inLanguage"] = lang["content"]
    else:
        html = soup.select_one("html")
        if html is not None:
            lang = html.get("lang", None)
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
