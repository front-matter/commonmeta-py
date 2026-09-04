"""schema_org reader for commonmeta-py"""

from __future__ import annotations

from datetime import datetime

import orjson as json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

from ..author_utils import get_authors
from ..base_utils import (
    compact,
    dig,
    first,
    parse_attributes,
    presence,
    sanitize,
    wrap,
)
from ..constants import (
    CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS,
    OG_TO_SO_TRANSLATIONS,
    SO_TO_CM_TRANSLATIONS,
    SO_TO_DC_RELATION_TYPES,
    SO_TO_DC_REVERSE_RELATION_TYPES,
    Commonmeta,
)
from ..date_utils import (
    get_iso8601_date,
    strip_milliseconds,
)
from ..doi_utils import doi_from_url, get_doi_ra, normalize_doi, validate_doi
from ..readers.crossref_reader import get_crossref
from ..readers.datacite_reader import get_datacite
from ..translators import web_translator
from ..utils import (
    dict_to_spdx,
    from_schema_org,
    from_schema_org_creators,
    get_language,
    name_to_fos,
    normalize_cc_url,
    normalize_id,
    normalize_ids,
    normalize_url,
)


def get_schema_org(pid: str | None, **kwargs) -> dict:
    """get_schema_org"""
    if pid is None:
        return {"state": "not_found"}
    url = pid

    # if pid represents a DOI, get metadata from Crossref or DataCite
    if doi_from_url(pid):
        return get_doi_meta(doi_from_url(pid))
    try:
        response = requests.get(url, timeout=10, allow_redirects=True, **kwargs)
    except ConnectionError as error:
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
    # elif response.headers.get("content-type") == "application/pdf":
    #     try:
    #         pdf = pikepdf.open(io.BytesIO(response.content))
    #         with pdf.open_metadata() as meta:
    #             if meta.get("/doi", None) is not None:
    #                 return get_doi_meta(meta.get("/doi"))
    #             date_modified = (
    #                 get_datetime_from_pdf_time(meta.get("/ModDate"))
    #                 if meta.get("/ModDate", None)
    #                 else None
    #             )
    #             name = meta.get("/Title", None)
    #             return compact(
    #                 {
    #                     "@id": url,
    #                     "@type": "DigitalDocument",
    #                     "via": "schema_org",
    #                     "name": str(name),
    #                     "datePublished": date_modified,
    #                     "dateAccessed": datetime.now().isoformat("T", "seconds")
    #                     if date_modified is None
    #                     else None,
    #                 }
    #             )
    #     except Exception as error:
    #         print(error)
    #         return {
    #             "@id": url,
    #             "@type": "WebPage",
    #             "state": "bad_request",
    #             "via": "schema_org",
    #         }

    data = parse_schema_org_html(response.text, url)

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


def json_ld_nodes(soup) -> list:
    """Every json-ld node a page carries, whatever shape it wrote them in.

    A `<script type="application/ld+json">` holds one node, an array of them,
    or a `@graph` of them -- the last being what WordPress with Yoast writes,
    and the reason a page could carry an Article and be read as carrying
    nothing. Reading only the first shape raised

        AttributeError: 'list' object has no attribute 'get'

    on every page that used one of the others, which aborted the read of the
    reference being validated.

    A block that is not json at all is skipped rather than raising: one broken
    script tag should not lose the page's other metadata, and the pages this
    reads are written by everyone.
    """
    nodes: list = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            block = json.loads(script.text)
        except (json.JSONDecodeError, TypeError):
            continue
        for node in block if isinstance(block, list) else [block]:
            if not isinstance(node, dict):
                continue
            graph = node.get("@graph")
            if isinstance(graph, list):
                nodes.extend(i for i in graph if isinstance(i, dict))
            else:
                nodes.append(node)
    return nodes


def is_supported_type(node: dict) -> bool:
    """Whether a node's @type is one this reads.

    `@type` is a string or a list of them -- `["Article", "BlogPosting"]` is
    ordinary -- and asking whether a list is in a dict raised

        TypeError: unhashable type: 'list'

    which killed the read as surely as a missing type would have been harmless.
    """
    types = node.get("@type")
    if isinstance(types, list):
        return any(isinstance(t, str) and t in SO_TO_CM_TRANSLATIONS for t in types)
    return isinstance(types, str) and types in SO_TO_CM_TRANSLATIONS


#: Types that describe the thing a page belongs to rather than the page. They
#: are read where nothing better is on offer, but never in preference to a work.
CONTAINER_TYPES = {"WebSite", "Blog"}


def pick_json_ld(nodes: list) -> dict | None:
    """The node that describes the work, out of everything the page declares.

    A page rarely declares one thing. WordPress with Yoast writes a `@graph` of
    WebSite, WebPage, Article and Organization, in that order, and taking the
    first supported node would take the site every time -- the reference would
    validate against the blog rather than the post cited. So a work is
    preferred, and a container is the fallback rather than the default.
    """
    supported = [node for node in nodes if is_supported_type(node)]
    works = [node for node in supported if not is_container_type(node)]
    return next(iter(works or supported), None)


def is_container_type(node: dict) -> bool:
    """Whether this node describes a site or a blog rather than a work."""
    types = node.get("@type")
    types = types if isinstance(types, list) else [types]
    return any(t in CONTAINER_TYPES for t in types if isinstance(t, str))


def parse_schema_org_html(html: str, url: str | None = None, content=False) -> dict:
    """The schema.org a page carries: its meta tags, then its json-ld.

    The json-ld wins where the two say different things, since it is the more
    specific of the two. Factored out of `get_schema_org` so a page that is
    not fetched can be read the same way - the html a pdf rendition carries as
    its attachment, which is written by `to_attachment_html`.

    ``content`` reads the body of the page as the content of the work. It is
    off by default: the body of an arbitrary web page is its navigation and
    its widgets as much as its text, and only a page written as one post is
    its post.
    """
    soup = BeautifulSoup(html, "html.parser")

    # load html meta tags
    data = get_html_meta(soup)
    # load site-specific metadata
    data |= web_translator(soup, url)

    # load schema.org metadata. If there are multiple schema.org blocks, load
    # them all, and pick the first one with a supported type
    json_ld = pick_json_ld(json_ld_nodes(soup))
    if json_ld is not None:
        data |= json_ld

    if content and data.get("articleBody", None) is None and soup.body is not None:
        data["articleBody"] = soup.body.decode_contents().strip()
    return data


def read_schema_org(data: dict | None, **kwargs) -> Commonmeta:
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
        contributors += contrib

    if meta.get("name", None) is not None:
        title = meta.get("name")
    elif meta.get("headline", None) is not None:
        title = meta.get("headline")
    else:
        title = None

    date_published = strip_milliseconds(meta.get("datePublished", None))
    date_updated = strip_milliseconds(meta.get("dateModified", None))
    dates: dict = {}
    date_created = strip_milliseconds(meta.get("dateCreated", None))
    if date_created:
        dates["created"] = date_created
    # if no date is found, use today's date
    if date_published is None and date_updated is None:
        dates["accessed"] = read_options.get(
            "dateAccessed", None
        ) or datetime.now().isoformat("T", "seconds")

    publisher = meta.get("publisher", None)
    if publisher is not None:
        _pub_id = (
            normalize_id(publisher.get("@id", None))
            if isinstance(publisher, dict)
            else None
        )
        _pub_name = (
            publisher.get("name", None) if isinstance(publisher, dict) else publisher
        )
        publisher = (
            compact({"id": _pub_id, "name": _pub_name})
            if (_pub_id or _pub_name)
            else None
        )

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_)
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    if _type == "Dataset":
        _title = first(
            parse_attributes(
                from_schema_org(meta.get("includedInDataCatalog", None)),
                content="name",
                first=True,
            )
        )
        container_url = first(
            parse_attributes(
                from_schema_org(meta.get("includedInDataCatalog", None)),
                content="url",
                first=True,
            )
        )
        container = compact(
            {
                "type": "DataRepository",
                "title": _title,
                "identifiers": (
                    [{"identifier": container_url, "identifier_type": "URL"}]
                    if container_url
                    else None
                ),
                "volume": meta.get("volumeNumber", None),
                "issue": meta.get("issueNumber", None),
                "first_page": meta.get("pageStart", None),
                "last_page": meta.get("pageEnd", None),
            }
        )
    else:
        container = schema_org_container(meta, _type)

    references = schema_org_references(meta)
    funding_references = [
        get_funding_reference(i) for i in wrap(meta.get("funder", None))
    ]

    descriptions = [sanitize(i) for i in wrap(meta.get("description"))]
    description = descriptions[0] if descriptions else None
    additional_descriptions = [
        {"description": i, "type": "Abstract"} for i in descriptions[1:]
    ]

    # convert keywords as comma-separated string into list (original casing)
    subj = meta.get("keywords", None)
    if isinstance(subj, str):
        subj = [k.strip() for k in subj.split(",") if k.strip()]
    subjects = schema_org_subjects(meta) or [name_to_fos(i) for i in wrap(subj)]

    if isinstance(meta.get("inLanguage"), str):
        language = meta.get("inLanguage")
    elif isinstance(meta.get("inLanguage"), list):
        language = dig(meta, "inLanguage.0")
    elif isinstance(meta.get("inLanguage"), dict):
        language = dig(meta, "inLanguage.alternateName") or dig(meta, "inLanguage.name")
    else:
        language = None

    geo_locations = [
        schema_org_geolocation(i) for i in wrap(meta.get("spatialCoverage", None))
    ]
    identifiers = schema_org_identifiers(meta)
    provider = (
        get_doi_ra(_id)
        if doi_from_url(_id)
        else first(
            parse_attributes(meta.get("provider", None), content="name", first=True)
        )
    )
    state = "findable"

    return {
        # required attributes
        "id": _id,
        "type": _type,
        # recommended and optional attributes
        "additional_descriptions": presence(additional_descriptions),
        "additional_type": additional_type,
        "container": container,
        "content": meta.get("articleBody", None),
        "contributors": presence(contributors),
        "date_published": date_published,
        "date_updated": date_updated,
        "dates": presence(dates),
        "description": description,
        "files": presence(schema_org_files(meta)),
        "funding_references": presence(funding_references),
        "geo_locations": presence(geo_locations),
        "identifiers": presence(identifiers),
        "image": schema_org_image(meta),
        "language": get_language(language),
        "license": license_,
        "provider": provider,
        "publisher": publisher,
        "references": presence(references),
        "relations": presence(schema_org_relations(meta)),
        "state": state,
        "subjects": presence(subjects),
        "title": title,
        "url": url,
        "version": meta.get("version", None),
    } | read_options


def get_doi_meta(doi: str | None) -> dict:
    """get_doi_meta"""
    if doi is None:
        return {"state": "not_found"}
    ra = get_doi_ra(doi)
    if ra == "Crossref":
        return get_crossref(doi)
    elif ra == "DataCite":
        return get_datacite(doi)
    else:
        return {"state": "not_found"}


def schema_org_related_item(meta, relation_type=None) -> None:
    """Related items"""
    normalize_ids(
        ids=wrap(meta.get(relation_type, None)),
        relation_type=SO_TO_DC_RELATION_TYPES.get(relation_type),
    )


def schema_org_reverse_related_item(meta, relation_type=None) -> None:
    """Reverse related items"""
    normalize_ids(
        ids=wrap(dig(meta, f"@reverse.{relation_type}")),
        relation_type=SO_TO_DC_REVERSE_RELATION_TYPES.get(relation_type),
    )


def schema_org_is_identical_to(meta) -> None:
    """isIdenticalTo is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="sameAs")


def schema_org_is_part_of(meta) -> None:
    """isPartOf is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="isPartOf")


def schema_org_has_part(meta) -> None:
    """hasPart is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="hasPart")


def schema_org_is_previous_version_of(meta) -> None:
    """isPreviousVersionOf is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="PredecessorOf")


def schema_org_is_new_version_of(meta) -> None:
    """isNewVersionOf is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="SuccessorOf")


def schema_org_references(meta) -> list:
    """The works this one cites, from schema.org `citation`.

    A citation is a CreativeWork with a name, an @id, or both - the writer
    gives it the doi as its @id and the formatted citation as its name - and
    schema.org also allows the bare string, which is then the citation text.
    """
    references = []
    for citation in wrap(meta.get("citation", None)):
        if isinstance(citation, str):
            references.append({"reference": citation})
            continue
        if not isinstance(citation, dict):
            continue
        reference = compact(
            {
                "id": normalize_id(citation.get("@id", None)),
                "reference": citation.get("name", None),
            }
        )
        if reference:
            references.append(reference)
    return references


# The schema.org properties that carry a relation, read the way the writer
# writes them. The commonmeta types schema.org has no property for cannot
# appear here, and are not read.
SO_TO_CM_RELATION_TYPES = {
    "isPartOf": "IsPartOf",
    "hasPart": "HasPart",
    "sameAs": "IsIdenticalTo",
    "exampleOfWork": "IsVersionOf",
    "workExample": "HasVersion",
    "translationOfWork": "IsTranslationOf",
    "workTranslation": "HasTranslation",
    "isBasedOn": "IsSupplementTo",
    "review": "HasReview",
    "itemReviewed": "IsReviewOf",
}

SO_TO_CM_REVERSE_RELATION_TYPES = {"citation": "IsReferencedBy"}


def schema_org_relations(meta) -> list:
    """Relations, from the schema.org properties that carry them.

    `isPartOf` is read as the container as well, which is what a blog post's
    container is: the relation and the container are two readings of the same
    statement, and both readers of this record write it back.
    """

    def ids(value) -> list:
        out = []
        for item in wrap(value):
            _id = item.get("@id", None) if isinstance(item, dict) else item
            _id = normalize_id(_id) if isinstance(_id, str) else None
            if _id:
                out.append(_id)
        return out

    relations = [
        {"id": _id, "type": relation_type}
        for property_, relation_type in SO_TO_CM_RELATION_TYPES.items()
        for _id in ids(meta.get(property_, None))
    ]
    relations += [
        {"id": _id, "type": relation_type}
        for property_, relation_type in SO_TO_CM_REVERSE_RELATION_TYPES.items()
        for _id in ids(dig(meta, f"@reverse.{property_}"))
    ]
    return relations


def schema_org_subjects(meta) -> list:
    """Subjects from `about`, which keeps the id a keyword string drops."""
    subjects = []
    for term in wrap(meta.get("about", None)):
        if not isinstance(term, dict) or not term.get("name", None):
            continue
        subjects.append(
            compact(
                {
                    "id": term.get("@id", None),
                    "subject": term.get("name", None),
                    "scheme": term.get("inDefinedTermSet", None),
                }
            )
        )
    return subjects


def schema_org_identifiers(meta) -> list:
    """Identifiers from the `identifier` PropertyValues."""
    identifiers = []
    for identifier in wrap(meta.get("identifier", None)):
        if not isinstance(identifier, dict) or not identifier.get("value", None):
            continue
        identifiers.append(
            compact(
                {
                    "identifier": identifier.get("value", None),
                    "identifier_type": identifier.get("propertyID", None),
                    "scheme": identifier.get("name", None),
                }
            )
        )
    return identifiers


def schema_org_image(meta) -> str | None:
    """The image url, from the url, the ImageObject or the list of either."""
    image = first(wrap(meta.get("image", None)))
    if isinstance(image, dict):
        image = image.get("url", None) or image.get("contentUrl", None)
    return image if isinstance(image, str) else None


def schema_org_files(meta) -> list:
    """Files from the MediaObjects a work is encoded or distributed as."""
    files = []
    for media in wrap(meta.get("encoding", None)) + wrap(
        meta.get("distribution", None)
    ):
        if not isinstance(media, dict) or not media.get("contentUrl", None):
            continue
        files.append(
            compact(
                {
                    "key": media.get("name", None),
                    "checksum": media.get("sha256", None),
                    "url": media.get("contentUrl", None),
                    "size": media.get("size", None),
                    "mime_type": media.get("encodingFormat", None),
                }
            )
        )
    return files


# What a container is called in schema.org, where it says so at all.
SO_TO_CM_CONTAINER_TYPES = {"Periodical": "Journal", "Blog": "Blog"}


def schema_org_container(meta, _type: str) -> dict:
    """The container, from `isPartOf`.

    Read for every type rather than for blog posts and preprints alone, and
    with the doi, the issn and the platform the writer puts there. A record
    that names none of them still gets the type its work type implies, which
    is what this reader has always returned.
    """
    part = meta.get("isPartOf", None)
    if isinstance(part, str):
        part = {"name": part}
    if not isinstance(part, dict):
        part = {}

    identifiers = []
    doi = normalize_doi(part.get("@id", None)) if part.get("@id", None) else None
    if doi:
        identifiers.append({"identifier": doi, "identifier_type": "DOI"})
    if part.get("issn", None):
        identifiers.append({"identifier": part["issn"], "identifier_type": "ISSN"})
    container_url = dig(meta, "publisher.url")
    if not identifiers and container_url:
        identifiers.append({"identifier": container_url, "identifier_type": "URL"})

    container_type = (
        SO_TO_CM_CONTAINER_TYPES.get(part.get("@type", None), None)
        or part.get("additionalType", None)
        or {"BlogPost": "Blog", "Preprint": "Periodical"}.get(_type, None)
    )
    return compact(
        {
            "type": container_type,
            "title": part.get("name", None),
            "identifiers": presence(identifiers),
            "platform": dig(part, "provider.name"),
            "volume": meta.get("volumeNumber", None),
            "issue": meta.get("issueNumber", None),
            "first_page": meta.get("pageStart", None),
            "last_page": meta.get("pageEnd", None),
        }
    )


def schema_org_is_referenced_by(meta) -> None:
    """isReferencedBy is a special case because it can be a string or an object."""
    schema_org_reverse_related_item(meta, relation_type="citation")


def schema_org_is_supplement_to(meta) -> None:
    """isSupplementTo is a special case because it can be a string or an object."""
    schema_org_reverse_related_item(meta, relation_type="isBasedOn")


def schema_org_is_supplemented_by(meta) -> None:
    """isSupplementedBy is a special case because it can be a string or an object."""
    schema_org_related_item(meta, relation_type="isBasedOn")


def schema_org_geolocation(geo_location: dict | None) -> dict | None:
    """schema_org_geolocation"""
    if geo_location is None:
        return None

    def _coord(value) -> float | None:
        try:
            return float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    # place is the Place name, falling back to the geo coordinates' address
    place = geo_location.get("name", None) or dig(geo_location, "geo.address")
    longitude = _coord(dig(geo_location, "geo.longitude"))
    latitude = _coord(dig(geo_location, "geo.latitude"))

    result = compact(
        {
            "place": place,
            "point_longitude": longitude,
            "point_latitude": latitude,
        }
    )
    return result or None


def get_html_meta(soup) -> dict:
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

    _type = soup.select_one("meta[name='dc.type']") or soup.select_one(
        "meta[name='DC.type']"
    )
    data["@type"] = _type["content"].capitalize() if _type else None
    if _type is None:
        _type = soup.select_one("meta[property='og:type']")
        data["@type"] = OG_TO_SO_TRANSLATIONS.get(_type["content"]) if _type else None

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
        or soup.select_one("meta[name='title']")
    )
    data["name"] = title["content"] if title else None

    author = soup.select("meta[name='citation_author']")
    data["author"] = [i["content"] for i in author] if author else None

    description = soup.select_one("meta[name='citation_abstract']") or soup.select_one(
        "meta[name='dc.description']"
        or soup.select_one("meta[property='og:description']")
        or soup.select_one("meta[name='twitter:description']")
        or soup.select_one("meta[name='description']")
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


def get_funding_reference(dct) -> dict | None:
    """Get funding reference.

    funder_id is ROR-only per the v1.0 schema. schema.org funder @id is a
    Crossref Funder ID (a doi.org URL); translate to ROR where a translation
    is known, otherwise drop it rather than leaking a non-ROR identifier
    into funder_id.
    """
    funder_id = CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS.get(dct.get("@id", None), None)
    return compact(
        {
            "funder_name": dct.get("name", None),
            "funder_id": funder_id,
        }
    )
