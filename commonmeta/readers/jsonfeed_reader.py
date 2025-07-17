"""JSON Feed reader for commonmeta-py"""

from typing import Optional

import requests
from furl import furl
from pydash import py_

from ..author_utils import get_authors
from ..base_utils import parse_attributes, presence, sanitize
from ..constants import Commonmeta
from ..date_utils import get_date_from_unix_timestamp
from ..doi_utils import (
    doi_from_url,
    encode_doi,
    generate_substack_doi,
    generate_wordpress_doi,
    is_rogue_scholar_doi,
    normalize_doi,
    validate_doi,
    validate_doi_from_guid,
    validate_prefix,
)
from ..utils import (
    compact,
    dict_to_spdx,
    from_jsonfeed,
    issn_as_url,
    name_to_fos,
    normalize_url,
    validate_ror,
    validate_url,
    wrap,
)


def get_jsonfeed(pid: str, **kwargs) -> dict:
    """get_jsonfeed"""
    if pid is None:
        return {"state": "not_found"}
    url = normalize_url(pid)
    response = requests.get(url, timeout=10, allow_redirects=True, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json() | {"via": "jsonfeed"}


def read_jsonfeed(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_jsonfeed"""
    if data is None:
        return {"state": "not_found"}
    meta = data
    read_options = kwargs or {}
    url = None
    if py_.get(meta, "blog.status", None) in ["active", "expired"]:
        url = normalize_url(meta.get("url", None))
    elif py_.get(meta, "blog.status", None) == "archived" and meta.get(
        "archive_url", None
    ):
        url = normalize_url(meta.get("archive_url", None))

    # generate DOI string for registration if not provided
    _id = normalize_doi(read_options.get("doi", None) or meta.get("doi", None))
    if _id is None:
        if meta.get("guid") and py_.get(meta, "blog.doi_reg", False):
            # Generate DOI based on blogging platform
            generator = py_.get(meta, "blog.generator")
            prefix = py_.get(meta, "blog.prefix")
            slug = py_.get(meta, "blog.slug")
            guid = meta.get("guid")

            # Import these functions only when needed to avoid circular imports
            if generator in ["WordPress", "WordPress.com"] and prefix and slug and guid:
                _id = generate_wordpress_doi(prefix, slug, guid)
            elif generator == "Substack" and prefix and guid:
                _id = generate_substack_doi(prefix, guid)
            # don't use checksum as some legacy GUIDs (generated with commonmeta Go between May 2024
            # and April 2025) don't have valid checksum
            elif (
                prefix
                and guid
                and validate_doi_from_guid(prefix, guid[:-2], checksum=False)
            ):
                _id = guid

        # If still no DOI but prefix provided and not registered for DOI generation
        elif py_.get(meta, "blog.prefix") and not py_.get(meta, "blog.doi_reg", False):
            prefix = py_.get(meta, "blog.prefix")
            _id = encode_doi(prefix)

        # If override prefix is provided in read_options, use that
        elif read_options.get("prefix"):
            _id = encode_doi(read_options.get("prefix"))

    # fall back to url if no DOI can be generated
    if _id is None:
        _id = url

    _type = "BlogPost"

    if meta.get("authors", None):
        contributors = get_authors(from_jsonfeed(wrap(meta.get("authors"))))
    else:
        contributors = None

    title = parse_attributes(meta.get("title", None))
    titles = [{"title": sanitize(title)}] if title else None

    date: dict = {}
    date["published"] = (
        get_date_from_unix_timestamp(meta.get("published_at", None))
        if meta.get("published_at", None)
        else None
    )
    date["updated"] = (
        get_date_from_unix_timestamp(meta.get("updated_at", None))
        if meta.get("updated_at", None)
        else None
    )

    license_ = py_.get(meta, "blog.license", None)
    if license_ is not None:
        license_ = dict_to_spdx({"url": license_})
    issn = py_.get(meta, "blog.issn", None)
    blog_url = (
        f"https://rogue-scholar.org/blogs/{meta.get('blog_slug')}"
        if meta.get("blog_slug", None)
        else None
    )
    container = compact(
        {
            "type": "Blog",
            "title": py_.get(meta, "blog.title", None),
            "identifier": issn or blog_url,
            "identifierType": "ISSN" if issn else "URL",
            "platform": py_.get(meta, "blog.generator", None),
        }
    )
    publisher = (
        {"name": "Front Matter"}
        if is_rogue_scholar_doi(_id)
        or (
            container.get("identifierType", None) == "URL"
            and furl(container.get("identifier", None)).host == "rogue-scholar.org"
        )
        else None
    )

    description = meta.get("abstract", None) or meta.get("summary", None)
    if description is not None:
        descriptions = [{"description": sanitize(description), "type": "Abstract"}]
    else:
        descriptions = None
    category = py_.get(meta, "blog.category", None)
    if category is not None:
        subjects = [name_to_fos(py_.human_case(category))]
    else:
        subjects = []
    tags = wrap(py_.get(meta, "tags", None))
    if tags is not None:
        subjects += wrap([format_subject(i) for i in tags])
    references = get_references(wrap(meta.get("reference", None)))
    funding_references = get_funding_references(meta)
    relations = get_relations(wrap(meta.get("relationships", None)))
    if meta.get("blog_slug", None):
        relations.append(
            {
                "id": f"https://rogue-scholar.org/api/communities/{meta.get('blog_slug')}",
                "type": "IsPartOf",
            }
        )
    if issn is not None:
        relations.append(
            {
                "id": issn_as_url(issn),
                "type": "IsPartOf",
            }
        )
    identifiers = [
        {"identifier": meta.get("id"), "identifierType": "UUID"},
        {"identifier": meta.get("guid"), "identifierType": "GUID"},
    ]
    content = py_.get(meta, "content_html", "")
    image = py_.get(meta, "image", None)
    files = get_files(_id)
    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "id": _id,
        "type": _type,
        "url": url,
        "contributors": presence(contributors),
        "titles": presence(titles),
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional properties
        "additional_type": None,
        "subjects": presence(subjects),
        "language": meta.get("language", None),
        "identifiers": identifiers,
        "version": None,
        "license": license_,
        "descriptions": descriptions,
        "geoLocations": None,
        "fundingReferences": presence(funding_references),
        "references": presence(references),
        "relations": presence(relations),
        "content": presence(content),
        "image": presence(image),
        "files": files,
        # other properties
        "container": presence(container),
        "provider": "Crossref" if is_rogue_scholar_doi(_id) else None,
        "state": state,
        "schema_version": None,
    } | read_options


def get_references(references: list) -> list:
    """get jsonfeed references."""

    def get_reference(reference: dict) -> Optional[dict]:
        if reference is None or not isinstance(reference, dict):
            return None

        if reference.get("id", None) and validate_doi(reference.get("id")):
            id_ = normalize_doi(reference.get("id"))
        else:
            id_ = normalize_url(reference.get("id", None))

        return compact(
            {
                "id": id_,
                "key": reference.get("key", None),
                "title": reference.get("title", None),
                "publicationYear": reference.get("publicationYear", None),
                "unstructured": reference.get("unstructured", None),
            }
        )

    return [get_reference(i) for i in references]


def get_funding_references(meta: Optional[dict]) -> Optional[list]:
    """get json feed funding references.
    Check that relationships resolve and have type "HasAward" or
    funding is provided by blog metadata"""

    if meta is None or not isinstance(meta, dict):
        return None

    def format_funding(urls: list) -> list:
        """format funding. URLs can either be a list of grant IDs or a funder identifier
        (Open Funder Registry ID or ROR), followed by a grant URL"""
        # Prefix 10.3030 means grant ID from funder is European Commission.
        # CORDIS is the grants portal of the European Commission.
        if len(urls) == 1 and (
            validate_prefix(urls[0]) == "10.3030"
            or furl(urls[0]).host == "cordis.europa.eu"
        ):
            return [
                compact(
                    {
                        "funderName": "European Commission",
                        "funderIdentifier": "https://ror.org/00k4n6c32",
                        "funderIdentifierType": "ROR",
                        "awardUri": urls[0],
                        "awardNumber": urls[0].split("/")[-1],
                    }
                )
            ]
        # Prefix 10.13039 means funder ID from Open Funder registry.
        elif len(urls) == 2 and validate_prefix(urls[0]) == "10.13039":
            if urls[0] == "https://doi.org/10.13039/100000001":
                funder_name = "National Science Foundation"
                funder_identifier = "https://ror.org/021nxhr62"
            else:
                funder_name = None
            f = furl(urls[1])
            # url is for NSF grant
            if f.args["awd_id"] is not None:
                award_number = f.args["awd_id"]
            else:
                award_number = f.path.segments[-1]
            return [
                compact(
                    {
                        "funderName": funder_name,
                        "funderIdentifier": funder_identifier,
                        "funderIdentifierType": "ROR",
                        "awardUri": urls[1],
                        "awardNumber": award_number,
                    }
                )
            ]
        # URL is ROR ID for funder.
        elif len(urls) == 2 and validate_ror(urls[0]):
            f = furl(urls[0])
            _id = f.path.segments[-1]
            response = requests.get(
                f"https://api.ror.org/organizations/{_id}", timeout=10
            )
            ror = response.json()
            funder_name = ror.get("name", None)
            funder_identifier = urls[0]
            funder_identifier_type = "ROR"

            f = furl(urls[1])
            # url is for NSF grant
            if f.args["awd_id"] is not None:
                award_number = f.args["awd_id"]
            else:
                award_number = f.path.segments[-1]
            return [
                compact(
                    compact(
                        {
                            "funderName": funder_name,
                            "funderIdentifier": funder_identifier,
                            "funderIdentifierType": funder_identifier_type,
                            "awardUri": urls[1],
                            "awardNumber": award_number,
                        }
                    )
                )
            ]

    awards = py_.flatten(
        [
            format_funding(i.get("urls"))
            for i in wrap(meta.get("relationships", None))
            if i.get("type", None) == "HasAward"
        ]
    )

    def format_funding_reference(funding: dict) -> dict:
        """format funding reference. Make sure award URI is either a DOI or URL"""

        award_uri = funding.get("awardUri", None)
        if validate_url(funding.get("awardUri", None)) not in ["DOI", "URL"]:
            award_uri = None
        funder_identifier = funding.get("funderIdentifier", None)
        funder_identifier_type = funding.get("funderIdentifierType", None)
        if not funder_identifier_type and validate_ror(
            funding.get("funderIdentifier", None)
        ):
            funder_identifier_type = "ROR"

        return compact(
            {
                "funderName": funding.get("funderName", None),
                "funderIdentifier": funder_identifier,
                "funderIdentifierType": funder_identifier_type,
                "awardTitle": funding.get("awardTitle", None),
                "awardNumber": funding.get("awardNumber", None),
                "awardUri": award_uri,
            }
        )

    funding_references = py_.get(meta, "funding_references")
    if funding_references is not None:
        awards += [
            format_funding_reference(i)
            for i in funding_references
            if i.get("funderName", None)
        ]

    awards += wrap(py_.get(meta, "blog.funding"))
    return py_.uniq(awards)


def get_relations(relations: Optional[list]) -> Optional[list]:
    """get json feed related relations.
    Check that relations resolve and have a supported type"""
    supported_types = [
        "IsNewVersionOf",
        "IsPreviousVersionOf",
        "IsVersionOf",
        "HasVersion",
        "IsPartOf",
        "HasPart",
        "IsVariantFormOf",
        "IsOriginalFormOf",
        "IsIdenticalTo",
        "IsTranslationOf",
        "IsReviewOf",
        "HasReview",
        "IsPreprintOf",
        "HasPreprint",
        "IsSupplementTo",
    ]

    def format_relationship(relation: dict) -> dict:
        """format relationship"""
        _id = relation.get("url", None) or relation.get("urls", None)
        if isinstance(_id, list):
            relations = []
            for url in _id:
                relations.append({"id": url, "type": relation.get("type", None)})
            return relations
        return {
            "id": _id,
            "type": relation.get("type", None),
        }

    return py_.flatten(
        [
            format_relationship(i)
            for i in relations
            if i.get("type", None) in supported_types
        ]
    )


def get_files(pid: str) -> Optional[list]:
    """get json feed file links"""
    doi = doi_from_url(pid)
    if not is_rogue_scholar_doi(doi):
        return None
    return [
        {
            "mimeType": "text/markdown",
            "url": f"https://api.rogue-scholar.org/posts/{doi}.md",
        },
        {
            "mimeType": "application/pdf",
            "url": f"https://api.rogue-scholar.org/posts/{doi}.pdf",
        },
        {
            "mimeType": "application/epub+zip",
            "url": f"https://api.rogue-scholar.org/posts/{doi}.epub",
        },
        {
            "mimeType": "application/xml",
            "url": f"https://api.rogue-scholar.org/posts/{doi}.xml",
        },
    ]


def get_jsonfeed_uuid(id: str):
    """get jsonfeed by uuid"""
    if id is None:
        return None
    url = f"https://api.rogue-scholar.org/posts/{id}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return response.json()
    post = response.json()
    return py_.pick(
        post,
        [
            "id",
            "guid",
            "url",
            "doi",
            "title",
            "blog.slug",
            "blog.issn",
            "blog.prefix",
            "blog.status",
            "published_at",
            "updated_at",
            "indexed_at",
        ],
    )


def get_jsonfeed_blog_slug(id: str):
    """get jsonfeed by id and return blog slug"""
    if id is None:
        return None
    url = f"https://api.rogue-scholar.org/posts/{id}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return response.json()
    post = response.json()
    return py_.get(post, "blog.slug", None)


def format_subject(subject: str) -> Optional[dict]:
    """format subject"""
    if subject is None or not isinstance(subject, str):
        return None
    return {
        "subject": subject,
    }
