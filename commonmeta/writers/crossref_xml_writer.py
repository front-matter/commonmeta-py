"""Crossref XML writer for commonmeta-py"""

from __future__ import annotations

import io
import logging
from datetime import datetime
from time import time
from typing import TYPE_CHECKING, Any, Dict

import orjson as json
import requests
import xmltodict
from dateutil.parser import parse as date_parse
from furl import furl
from isbnlib import canonical, is_isbn10, is_isbn13
from marshmallow import Schema, fields
from requests.exceptions import RequestException
from requests_toolbelt.multipart.encoder import MultipartEncoder

from ..base_utils import (
    compact,
    container_identifier,
    dig,
    get_crossref_xml_head,
    parse_xml,
    presence,
    wrap,
)
from ..constants import CM_TO_CR_CONTRIBUTOR_ROLES, CM_TO_CR_CREDIT_ROLES
from ..doi_utils import doi_from_url, is_rogue_scholar_doi, validate_doi
from ..utils import validate_url
from .inveniordm_writer import push_inveniordm

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList

log = logging.getLogger(__name__)

# posted_content @type enum, Crossref schema 5.5.0 (adds blog and poster;
# drops working_paper, dissertation, report from 5.4.0).
POSTED_CONTENT_TYPES = [
    "preprint",
    "blog",
    "letter",
    "other",
    "poster",
    "review",
]

MARSHMALLOW_MAP = {
    "abstracts": "jats:abstract",
    "license": "ai:program",
    "funding_references": "fr:program",
    "relations": "rel:program",
    "references": "citation_list",
}

# Crossref 5.5.0 contributor roles: traditional contributor_role attribute
# values plus CRediT taxonomy roles.
_ALLOWED_CONTRIBUTOR_ROLES = set(CM_TO_CR_CONTRIBUTOR_ROLES) | set(
    CM_TO_CR_CREDIT_ROLES
)


def _is_allowed_contributor(roles: list) -> bool:
    """A contributor is included if it has no roles (treated as author) or at
    least one role Crossref recognizes."""
    if not roles:
        return True
    return any(role in _ALLOWED_CONTRIBUTOR_ROLES for role in roles)


def _wrap_crossref_body(item: dict[str, Any]) -> dict[str, Any]:
    """Wrap a single Crossref item dict into the correct body structure."""

    if not item:
        return {}

    input_obj: dict[str, Any] = dict(item)
    item_type = next(iter(input_obj))
    attributes = input_obj.get(item_type) or {}
    input_obj.pop(item_type, None)

    if item_type == "book":
        book_metadata = dig(input_obj, "book_metadata") or {}
        input_obj.pop("book_metadata", None)
        book_metadata = {**book_metadata, **input_obj}
        return {"book": {**attributes, "book_metadata": book_metadata}}

    if item_type == "database":
        database_metadata = dig(input_obj, "database_metadata") or {}
        input_obj.pop("database_metadata", None)
        val = input_obj.pop("publisher_item", None)
        institution = input_obj.pop("institution", None)
        if val is not None:
            database_metadata = {**{"titles": val}, **database_metadata}
        database_metadata["institution"] = institution or {}
        component = input_obj.pop("component", None) or {}
        # version_info is not allowed inside a <component> (Crossref 5.5.0)
        input_obj.pop("version_info", None)
        return {
            "database": {
                **attributes,
                "database_metadata": database_metadata,
                "component_list": {"component": component | input_obj},
            }
        }

    if item_type == "journal":
        journal_metadata = dig(input_obj, "journal_metadata") or {}
        journal_issue = dig(input_obj, "journal_issue")
        journal_article = dig(input_obj, "journal_article")
        input_obj.pop("journal_metadata", None)
        input_obj.pop("journal_issue", None)
        input_obj.pop("journal_article", None)
        journal_payload: dict[str, Any] = {
            "journal_metadata": journal_metadata,
        }
        if journal_issue is not None:
            journal_payload["journal_issue"] = journal_issue
        if journal_article is not None:
            journal_payload["journal_article"] = journal_article | input_obj
        else:
            journal_payload |= input_obj
        return {"journal": compact(journal_payload)}

    if item_type == "conference":
        event_metadata = input_obj.pop("event_metadata", None)
        proceedings_metadata = input_obj.pop("proceedings_metadata", None)
        conference_paper_attrs = input_obj.pop("conference_paper", None) or {}
        # version_info is not allowed inside <conference_paper> (Crossref 5.5.0)
        input_obj.pop("version_info", None)
        return {
            "conference": compact(
                {
                    **attributes,
                    "event_metadata": event_metadata,
                    "proceedings_metadata": proceedings_metadata,
                    "conference_paper": compact(
                        {**conference_paper_attrs, **input_obj}
                    ),
                }
            )
        }

    if item_type == "sa_component":
        component = dig(input_obj, "component") or {}
        input_obj.pop("component", None)
        # version_info is not allowed inside a <component> (Crossref 5.5.0)
        input_obj.pop("version_info", None)
        return {
            "sa_component": {
                **attributes,
                "component_list": {"component": component | input_obj},
            }
        }

    return {item_type: attributes | input_obj}


def _wrap_crossref_body_list(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Wrap a list of Crossref item dicts into the correct body structure."""

    items_by_type: dict[str, list[dict[str, Any]]] = {}

    for item in wrap(items):
        if not item or not isinstance(item, dict):
            continue

        input_obj: dict[str, Any] = dict(item)
        item_type = next(iter(input_obj))
        attributes = input_obj.get(item_type) or {}
        input_obj.pop(item_type, None)

        if item_type == "book":
            book_metadata = dig(input_obj, "book_metadata") or {}
            input_obj.pop("book_metadata", None)
            book_metadata = {**book_metadata, **input_obj}
            wrapped = {"book": {**attributes, "book_metadata": book_metadata}}
            item_type_key = "book"
            payload = wrapped["book"]
        elif item_type == "database":
            database_metadata = dig(input_obj, "database_metadata") or {}
            input_obj.pop("database_metadata", None)
            database_metadata = {**database_metadata, **input_obj}
            wrapped = {
                "database": {**attributes, "database_metadata": database_metadata}
            }
            item_type_key = "database"
            payload = wrapped["database"]
        elif item_type == "journal":
            journal_metadata = dig(input_obj, "journal_metadata") or {}
            journal_issue = dig(input_obj, "journal_issue")
            journal_article = dig(input_obj, "journal_article")
            input_obj.pop("journal_metadata", None)
            input_obj.pop("journal_issue", None)
            input_obj.pop("journal_article", None)
            journal_payload: dict[str, Any] = {
                "journal_metadata": journal_metadata,
            }
            if journal_issue is not None:
                journal_payload["journal_issue"] = journal_issue
            if journal_article is not None:
                journal_payload["journal_article"] = journal_article | input_obj
            else:
                journal_payload |= input_obj
            wrapped = {"journal": compact(journal_payload)}
            item_type_key = "journal"
            payload = wrapped["journal"]
        elif item_type == "sa_component":
            component = dig(input_obj, "component") or {}
            input_obj.pop("component", None)
            # version_info is not allowed inside a <component> (Crossref 5.5.0)
            input_obj.pop("version_info", None)
            wrapped = {
                "sa_component": {
                    **attributes,
                    "component_list": {"component": component | input_obj},
                }
            }
            item_type_key = "sa_component"
            payload = wrapped["sa_component"]
        elif item_type == "conference":
            event_metadata = input_obj.pop("event_metadata", None)
            proceedings_metadata = input_obj.pop("proceedings_metadata", None)
            conference_paper_attrs = input_obj.pop("conference_paper", None) or {}
            # version_info is not allowed inside <conference_paper> (Crossref 5.5.0)
            input_obj.pop("version_info", None)
            wrapped = {
                "conference": compact(
                    {
                        **attributes,
                        "event_metadata": event_metadata,
                        "proceedings_metadata": proceedings_metadata,
                        "conference_paper": compact(
                            {**conference_paper_attrs, **input_obj}
                        ),
                    }
                )
            }
            item_type_key = "conference"
            payload = wrapped["conference"]
        else:
            wrapped = {item_type: attributes | input_obj}
            item_type_key = item_type
            payload = wrapped[item_type]

        items_by_type.setdefault(item_type_key, []).append(payload)

    body_content: dict[str, Any] = {}
    for type_key, bucket in items_by_type.items():
        body_content[type_key] = bucket[0] if len(bucket) == 1 else bucket

    return body_content


def tostring(data: dict | list, *, head: dict | None = None) -> str:
    """Serialize Crossref XML using xmltodict."""
    if not isinstance(data, (dict, list)):
        raise TypeError("Input data must be a dictionary or a list.")

    head = head or {}

    if isinstance(data, dict):
        body = _wrap_crossref_body(dict(data))
    else:
        body = _wrap_crossref_body_list(data)

    output: dict[str, Any] = {
        "doi_batch": {
            "@xmlns": "http://www.crossref.org/schema/5.5.0",
            "@xmlns:ai": "http://www.crossref.org/AccessIndicators.xsd",
            "@xmlns:rel": "http://www.crossref.org/relations.xsd",
            "@xmlns:fr": "http://www.crossref.org/fundref.xsd",
            "@version": "5.5.0",
            "head": get_crossref_xml_head(head),
            "body": body,
        }
    }

    return (
        xmltodict.unparse(output, pretty=True, indent="  ")
        .encode("utf-8")
        .decode("utf-8")
    )


class CrossrefXMLSchema(Schema):
    """Crossref XML schema"""

    # root element
    book = fields.Dict()
    conference = fields.Dict()
    database = fields.Dict()
    dissertation = fields.Dict()
    journal = fields.Dict()
    peer_review = fields.Dict()
    report_paper = fields.Dict()
    pending_publication = fields.Dict()
    posted_content = fields.Dict()
    sa_component = fields.Dict()
    standard = fields.Dict()

    # elements
    group_title = fields.String()
    book_metadata = fields.Dict()
    database_metadata = fields.Dict()
    event_metadata = fields.Dict()
    proceedings_metadata = fields.Dict()
    journal_metadata = fields.Dict()
    journal_issue = fields.Dict()
    journal_article = fields.Dict()
    component = fields.Dict()
    titles = fields.Dict()
    contributors = fields.Dict()
    abstracts = fields.List(fields.Dict(), data_key="jats:abstract")
    publication_date = fields.Dict()
    posted_date = fields.Dict()
    review_date = fields.Dict()
    approval_date = fields.Dict()
    publisher_item = fields.Dict()
    institution = fields.Dict()
    item_number = fields.Dict()
    institution = fields.Dict()
    isbn = fields.List(fields.Dict())
    noisbn = fields.Dict()
    issn = fields.String()
    publisher = fields.Dict()
    description = fields.Dict()
    funding_references = fields.Dict(data_key="fr:program")
    license = fields.Dict(data_key="ai:program")
    relations = fields.Dict(data_key="rel:program")
    archive_locations = fields.List(fields.Dict())
    version_info = fields.Dict()
    doi_data = fields.Dict(data_key="doi_data")
    references = fields.Dict(data_key="citation_list")


def convert_crossref_xml(metadata: Metadata) -> dict | None:
    """Convert Crossref XML"""

    # raise error if type is not supported by Crossref
    if metadata.type not in [
        "Preprint",
        "Blog",
        "BlogPost",
        "BlogVolume",
        "Book",
        "BookChapter",
        "Component",
        "Dataset",
        "Dissertation",
        "JournalArticle",
        "PeerReview",
        "Poster",
        "Presentation",
        "ProceedingsArticle",
        "Report",
        "Standard",
    ]:
        raise CrossrefError(
            f"Type not supported by Crossref: {metadata.type} for {metadata.id}"
        )

    # raise error if doi or url are not present
    if doi_from_url(metadata.id) is None or metadata.url is None:
        raise CrossrefError(f"DOI or URL missing for Crossref XML: {metadata.id}")

    titles = get_titles(metadata)
    contributors = get_contributors(metadata)
    abstracts = get_abstracts(metadata)
    relations = get_relations(metadata)
    doi_data = get_doi_data(metadata)
    references = get_references(metadata)
    funding_references = get_funding_references(metadata)
    license = get_license(metadata)
    kwargs = {}

    if metadata.type in ("Preprint", "BlogPost", "Poster", "Presentation", "Review"):
        # Crossref 5.5.0 posted_content subtypes: BlogPost → blog, Poster →
        # poster, Review → review, Presentation → other. A Preprint uses its additional_type
        # when it names a valid subtype, else defaults to preprint.
        _posted_type = {
            "BlogPost": "blog",
            "Poster": "poster",
            "Review": "review",
            "Presentation": "other",
        }.get(metadata.type)
        if _posted_type is not None:
            kwargs["type"] = _posted_type
        elif metadata.additional_type in POSTED_CONTENT_TYPES:
            kwargs["type"] = metadata.additional_type
        else:
            kwargs["type"] = "preprint"
        kwargs["language"] = metadata.language
        data = compact(
            {
                "posted_content": get_attributes(metadata, **kwargs),
                "group_title": get_group_title(metadata),
                "contributors": contributors,
                "titles": titles,
                "posted_date": get_publication_date(metadata),
                "institution": get_institution(metadata),
                "item_number": get_item_number(metadata),
                "abstracts": abstracts,
                "funding_references": funding_references,
                "license": license,
                "relations": relations,
                "version_info": get_version_info(metadata),
                "doi_data": doi_data,
                "references": references,
            }
        )
    elif metadata.type == "Blog":
        kwargs["language"] = metadata.language
        data = compact(
            {
                "journal": {},
                "journal_metadata": get_journal_metadata(metadata),
            }
        )
    elif metadata.type == "Book":
        kwargs["book_type"] = "monograph"
        # Crossref requires either <isbn> or <noisbn> in book_metadata.
        isbn = get_isbn(metadata, media_type="online")
        data = compact(
            {
                "book": get_attributes(metadata, **kwargs),
                "book_metadata": get_book_metadata(metadata),
                "contributors": contributors,
                "titles": titles,
                "abstracts": abstracts,
                "publication_date": get_publication_date(metadata, media_type="online"),
                "isbn": isbn,
                "noisbn": None if isbn else {"@reason": "monograph"},
                "publisher": get_publisher(metadata),
                "publisher_item": None,
                "funding_references": funding_references,
                "license": license,
                "relations": relations,
                "archive_locations": get_archive_locations(metadata),
                "doi_data": doi_data,
                "references": references,
            }
        )
    elif metadata.type == "BookChapter":
        kwargs["book_type"] = "monograph"
        # Crossref requires either <isbn> or <noisbn> in book_metadata.
        isbn = get_isbn(metadata)
        data = compact(
            {
                "book": get_attributes(metadata, **kwargs),
                "book_metadata": get_book_metadata(metadata),
                "contributors": contributors,
                "titles": titles,
                "publication_date": get_publication_date(metadata, media_type="online"),
                "isbn": isbn,
                "noisbn": None if isbn else {"@reason": "monograph"},
                "publisher": get_publisher(metadata),
                "abstracts": abstracts,
                "funding_references": funding_references,
                "license": license,
                "relations": relations,
                "archive_locations": get_archive_locations(metadata),
                "version_info": get_version_info(metadata),
                "doi_data": doi_data,
                "references": references,
            }
        )
    elif metadata.type == "Component":
        parent_doi = dig(metadata, "container.id")
        if parent_doi is None:
            raise CrossrefError("missing required attribute 'parent_doi'")
        data = compact(
            {
                "sa_component": get_attributes(metadata),
                "component": {
                    "@reg-agency": "CrossRef",
                    "@parent_relation": "isPartOf",
                },
                "description": None,
                "doi_data": doi_data,
            }
        )
    elif metadata.type == "Dataset":
        publisher = dig(metadata, "publisher.name")
        if publisher is not None:
            publisher_item = {
                "title": publisher,
            }
        data = compact(
            {
                "database": {},
                "database_metadata": get_database_metadata(metadata),
                "publisher_item": publisher_item if publisher else None,
                "institution": get_institution(metadata),
                "component": {"@parent_relation": "isPartOf"},
                "titles": titles,
                "contributors": contributors,
                "publication_date": get_publication_date(metadata, media_type="online"),
                "version_info": get_version_info(metadata),
                "doi_data": doi_data,
            }
        )
    elif metadata.type == "Dissertation":
        data = compact(
            {
                "dissertation": get_attributes(metadata, **kwargs),
                "contributors": contributors,
                "titles": titles,
                "approval_date": get_publication_date(metadata),
                "institution": get_institution(metadata),
                "degree": None,
                "isbn": get_isbn(metadata),
                "publisher_item": None,
                "funding_references": funding_references,
                "license": license,
                "relations": relations,
                "version_info": get_version_info(metadata),
                "doi_data": doi_data,
            }
        )

    elif metadata.type == "JournalArticle":
        publisher_item = None
        kwargs["language"] = metadata.language
        data = compact(
            {
                "journal": {},
                "journal_metadata": get_journal_metadata(metadata),
                "journal_issue": get_journal_issue(metadata),
                "journal_article": get_attributes(metadata, **kwargs),
                "titles": titles,
                "contributors": contributors,
                "abstracts": abstracts,
                "publication_date": get_publication_date(metadata, media_type="online"),
                "publisher_item": publisher_item,
                "funding_references": funding_references,
                "license": license,
                "crossmark": None,
                "relations": relations,
                "archive_locations": get_archive_locations(metadata),
                "version_info": get_version_info(metadata),
                "doi_data": doi_data,
                "references": references,
            }
        )
    elif metadata.type == "PeerReview":
        kwargs["type"] = "author-comment"
        kwargs["stage"] = "pre-publication"
        data = compact(
            {
                "peer_review": get_attributes(metadata, **kwargs),
                "contributors": contributors,
                "titles": titles,
                "review_date": get_publication_date(metadata),
                "license": license,
                "relations": relations,
                "doi_data": doi_data,
            }
        )
    elif metadata.type == "ProceedingsArticle":
        # the publisher is carried in proceedings_metadata; conference_paper
        # has no title-bearing publisher_item.
        data = compact(
            {
                "conference": get_attributes(metadata, **kwargs),
                "event_metadata": get_event_metadata(metadata),
                "proceedings_metadata": get_proceedings_metadata(metadata),
                "conference_paper": get_attributes(metadata, **kwargs),
                "contributors": contributors,
                "titles": titles,
                "abstracts": abstracts,
                "publication_date": get_publication_date(metadata),
                "publisher_item": None,
                "funding_references": funding_references,
                "license": license,
                "crossmark": None,
                "relations": relations,
                "archive_locations": get_archive_locations(metadata),
                "version_info": get_version_info(metadata),
                "doi_data": doi_data,
                "references": references,
            }
        )
    elif metadata.type == "Standard":
        publisher_item = None
        data = compact(
            {
                "standard": get_attributes(metadata, **kwargs),
                "journal_metadata": get_journal_metadata(metadata),
                "journal_issue": get_journal_issue(metadata),
                "titles": titles,
                "contributors": contributors,
                "publication_date": get_publication_date(metadata),
                "publisher_item": publisher_item,
                "funding_references": funding_references,
                "license": license,
                "crossmark": None,
                "relations": relations,
                "archive_locations": get_archive_locations(metadata),
                "version_info": get_version_info(metadata),
                "doi_data": doi_data,
                "references": references,
                "component_list": None,
            }
        )
    else:
        raise CrossrefError(
            f"Unexpected metadata type for Crossref XML: {metadata.type} for {metadata.id}"
        )

    return data


def write_crossref_xml(metadata: Metadata) -> dict:
    """Write Crossref XML"""
    if metadata is None:
        raise CrossrefError("No metadata provided for Crossref XML generation")

    # Convert metadata to Crossref XML structure (raises CrossrefError on failure)
    data = convert_crossref_xml(metadata)

    # Check for existing validation errors early
    if metadata.write_errors is not None:
        raise CrossrefError(f"Validation errors in metadata: {metadata.write_errors}")

    # Use the marshmallow schema to dump the data
    schema = CrossrefXMLSchema()
    crossref_xml = schema.dump(data)

    # Ensure consistent field ordering through the defined mapping
    field_order = [MARSHMALLOW_MAP.get(k, k) for k in list(data.keys())]
    crossref_xml = {k: crossref_xml[k] for k in field_order if k in crossref_xml}

    return crossref_xml


def write_crossref_xml_list(metalist: MetadataList) -> list:
    """Write crossref_xml list"""
    if metalist is None or not metalist.is_valid:
        raise CrossrefError("Invalid metalist provided for Crossref XML generation")

    # Use the marshmallow schema to dump the data
    schema = CrossrefXMLSchema()
    crossref_xml_list = []
    for item in metalist.items:
        data = convert_crossref_xml(item)
        if data is None or not isinstance(data, dict):
            log.error(f"Could not convert metadata to Crossref XML: {item.id}")
            continue

        crossref_xml = schema.dump(data)

        # Ensure the order of fields in the XML matches the expected order
        field_order = [MARSHMALLOW_MAP.get(k, k) for k in list(data.keys())]
        crossref_xml = {k: crossref_xml[k] for k in field_order if k in crossref_xml}
        crossref_xml_list.append(crossref_xml)

    # Raise error if there are write_errors
    if presence(metalist.write_errors):
        raise CrossrefError(f"Validation errors in metalist: {metalist.write_errors}")

    return crossref_xml_list


def push_crossref_xml(
    metadata: Metadata,
    login_id: str,
    login_passwd: str,
    test_mode: bool,
    host: str | None,
    token: str | None,
    legacy_conn: str | None,
) -> str:
    """Push crossref_xml to Crossref API, returns the API response."""

    try:
        output = write_crossref_xml(metadata)
        head = {
            "depositor": metadata.depositor,
            "email": metadata.email,
            "registrant": metadata.registrant,
        }
        xml = tostring(output, head=head)
    except (ValueError, CrossrefError) as e:
        log.error(f"Failed to generate XML for upload: {e}")
        return "{}"

    if len(xml) == 0:
        log.error("Failed to generate XML for upload")
        return "{}"

    client = CrossrefXMLClient(
        username=login_id,
        password=login_passwd,
        test_mode=test_mode,
    )
    status = client.post(xml)

    if status != "SUCCESS":
        log.error("Failed to upload XML to Crossref")
        return "{}"

    record = {
        "doi": metadata.id,
        "updated": datetime.now().isoformat("T", "seconds"),
        "status": "submitted",
    }

    # update rogue-scholar record with state findable
    # if state is stale and host and token are provided
    if (
        is_rogue_scholar_doi(metadata.id, ra="crossref")
        and metadata.state == "stale"
        and host is not None
        and token is not None
    ):
        metadata.state = "findable"
        r = push_inveniordm(metadata, host=host, token=token)
        if r["status"] != "error":
            record["status"] = "updated"

    # Return JSON response
    return json.dumps(record, option=json.OPT_INDENT_2).decode("utf-8")


def push_crossref_xml_list(
    metalist: MetadataList,
    login_id: str,
    login_passwd: str,
    test_mode: bool,
    host: str | None,
    token: str | None,
    legacy_conn: str | None,
) -> bytes | None:
    """Push crossref_xml list to Crossref API, returns the API response."""

    try:
        output = write_crossref_xml_list(metalist)
        head = {
            "depositor": metalist.depositor,
            "email": metalist.email,
            "registrant": metalist.registrant,
        }
        xml = tostring(output, head=head)
    except ValueError as e:
        log.error(f"Failed to generate XML for upload: {e}")
        return None

    if len(xml) == 0:
        log.error("Failed to generate XML for upload")
        return None

    client = CrossrefXMLClient(
        username=login_id,
        password=login_passwd,
        test_mode=test_mode,
    )
    status = client.post(xml)

    if status != "SUCCESS":
        log.error("Failed to upload XML to Crossref")
        return None

    items = []
    for item in metalist.items:
        record = {
            "doi": item.id,
            "updated": datetime.now().isoformat("T", "seconds"),
            "status": "submitted",
        }

        # update rogue-scholar record with state findable
        # if state is stale and host and token are provided
        if (
            is_rogue_scholar_doi(item.id, ra="crossref")
            and item.state == "stale"
            and host is not None
            and token is not None
        ):
            item.state = "findable"
            r = push_inveniordm(item, host=host, token=token)
            if r["status"] != "error":
                record["status"] = "updated"
        items.append(record)

    # Return JSON response
    return json.dumps(items, option=json.OPT_INDENT_2)


def get_attributes(obj, **kwargs) -> dict:
    """Get root attributes"""
    return compact(
        {
            "@type": kwargs.get("type", None),
            "@book_type": kwargs.get("book_type", None),
            "@language": kwargs.get("language", None),
            "@stage": kwargs.get("stage", None),
            "@reg-agency": kwargs.get("reg-agency", None),
        }
    )


def get_journal_metadata(obj) -> dict | None:
    """get journal metadata"""
    return compact(
        {
            "@language": dig(obj, "language"),
            "full_title": dig(obj, "container.title") or dig(obj, "title"),
            "issn": get_issn(obj),
            "doi_data": get_doi_data(obj),
        }
    )


def get_book_metadata(obj) -> dict | None:
    return compact(
        {
            "@language": dig(obj, "language"),
        }
    )


def get_database_metadata(obj) -> dict | None:
    return compact(
        {
            "@language": dig(obj, "language"),
        }
    )


def get_event_metadata(obj) -> dict | None:
    """get event metadata"""
    if dig(obj, "container.title") is None:
        return None

    return compact(
        {
            "conference_name": dig(obj, "container.title"),
            "conference_location": dig(obj, "container.location"),
            "conference_date": None,
        }
    )


def get_proceedings_metadata(obj) -> dict | None:
    """get proceedings metadata"""
    if dig(obj, "container.title") is None or dig(obj, "publisher.name") is None:
        return None

    proceedings_metadata = {
        "@language": dig(obj, "language"),
        "proceedings_title": dig(obj, "container.title"),
        "publisher": {
            "publisher_name": dig(obj, "publisher.name"),
        },
        "publication_date": get_publication_date(obj, media_type="online"),
    }
    # Crossref requires either <isbn> or <noisbn> in proceedings_metadata.
    _, cid_type = container_identifier(dig(obj, "container"))
    if cid_type == "ISBN":
        proceedings_metadata["isbn"] = get_isbn(obj)
    else:
        proceedings_metadata["noisbn"] = {"@reason": "simple_series"}
    return compact(proceedings_metadata)


def get_journal_issue(obj) -> dict | None:
    """get journal issue"""
    volume = dig(obj, "container.volume")
    if volume is not None:
        volume = {"volume": volume}
    return compact(
        {
            "publication_date": get_publication_date(obj),
            "journal_volume": volume,
            "issue": dig(obj, "container.issue"),
        }
    )


def get_institution(obj) -> dict | None:
    """get institution"""
    if dig(obj, "publisher.name") is None:
        return None

    return {
        "institution_name": dig(obj, "publisher.name"),
    }


def get_titles(obj) -> dict | None:
    """get titles"""

    titles = {}
    title = dig(obj, "title", None)
    if title is not None:
        titles["title"] = title
    for t in wrap(dig(obj, "additional_titles", [])):
        if isinstance(t, dict) and t.get("type", None) == "Subtitle":
            titles["subtitle"] = t.get("title", None)

    return titles if titles else None


def get_contributors(obj) -> dict | None:
    """get contributors"""

    def map_affiliations(affiliations):
        """Map affiliations to a single <affiliations> element with one
        <institution> child per affiliation. Crossref 5.5.0 allows only one
        <affiliations> per person_name (with multiple institutions inside)."""
        institutions = [
            compact(
                {
                    "institution_name": affiliation.get("name", None),
                    "institution_id": (
                        {
                            "@type": "ror",
                            "#text": affiliation.get("identifier"),
                        }
                        if affiliation.get("identifier_type", None) == "ROR"
                        else None
                    ),
                }
            )
            for affiliation in wrap(affiliations)
        ]
        institutions = [institution for institution in institutions if institution]
        if not institutions:
            return None
        return {"institution": institutions}

    if len(wrap(dig(obj, "contributors"))) == 0:
        return None

    # Crossref 5.5.0 allows the traditional contributor_role attribute values
    # plus the CRediT taxonomy roles; a contributor with no roles is treated as
    # an author (backwards compatible).
    con = [
        c
        for c in dig(obj, "contributors", [])
        if _is_allowed_contributor(wrap(c.get("roles")))
    ]

    person_names = []
    organizations = []
    anonymous_contributors = []

    for num, contributor in enumerate(con):
        roles = wrap(contributor.get("roles"))
        contributor_role = next(
            (
                CM_TO_CR_CONTRIBUTOR_ROLES.get(role)
                for role in roles
                if role and CM_TO_CR_CONTRIBUTOR_ROLES.get(role)
            ),
            "author",
        )
        # CRediT roles are emitted as <role vocab="credit" type="..."> children
        credit_roles = [
            {"@vocab": "credit", "@type": CM_TO_CR_CREDIT_ROLES[role]}
            for role in roles
            if role in CM_TO_CR_CREDIT_ROLES
        ]
        sequence = "first" if num == 0 else "additional"
        organization = contributor.get("organization", None)
        person = contributor.get("person", None) or {}
        if organization and organization.get("name", None) is not None:
            organizations.append(
                {
                    "@contributor_role": contributor_role,
                    "@sequence": sequence,
                    "#text": organization.get("name"),
                }
            )
        elif (
            person.get("given_name", None) is not None
            or person.get("family_name", None) is not None
        ):
            person_names.append(
                compact(
                    {
                        "@contributor_role": contributor_role,
                        "@sequence": sequence,
                        "given_name": person.get("given_name", None),
                        "surname": person.get("family_name", None),
                        "role": credit_roles or None,
                        "affiliations": map_affiliations(
                            person.get("affiliations", None)
                        ),
                        "ORCID": person.get("id", None),
                    }
                )
            )
        else:
            anonymous_contributors.append(
                compact(
                    {
                        "@contributor_role": contributor_role,
                        "@sequence": sequence,
                        "affiliations": map_affiliations(
                            person.get("affiliations", None)
                        ),
                    }
                )
            )

    result = {}
    if person_names:
        result["person_name"] = person_names
    if organizations:
        result["organization"] = organizations
    if anonymous_contributors:
        result["anonymous"] = anonymous_contributors

    return result if result else None


def get_publisher(obj) -> dict | None:
    """get publisher"""
    if dig(obj, "publisher.name") is None:
        return None

    return {
        "publisher_name": dig(obj, "publisher.name"),
    }


def get_abstracts(obj) -> list | None:
    """get abstracts"""
    _description = dig(obj, "description", None)
    descriptions = (
        ([{"description": _description, "type": "Abstract"}] if _description else [])
        + wrap(dig(obj, "additional_descriptions", None))
    ) or None
    if len(wrap(descriptions)) == 0:
        return None

    abstracts = []
    for d in wrap(descriptions):
        if d.get("type", None) == "Abstract":
            abstracts.append(
                {
                    "@xmlns:jats": "http://www.ncbi.nlm.nih.gov/JATS1",
                    "jats:p": d.get("description", None),
                }
            )
        elif d.get("type", None) == "Other":
            abstracts.append(
                {
                    "@xmlns:jats": "http://www.ncbi.nlm.nih.gov/JATS1",
                    "jats:p": d.get("description", None),
                }
            )
    return abstracts


def get_group_title(obj) -> str | None:
    """Get group title from metadata"""
    return dig(obj, "container.title")


def get_item_number(obj) -> dict | None:
    """Insert item number"""
    if len(wrap(dig(obj, "identifiers"))) == 0:
        return None

    for identifier in wrap(dig(obj, "identifiers")):
        if identifier.get("identifier_type", None) == "UUID":
            # strip hyphen from UUIDs, as item_number can only be 32 characters long (UUIDv4 is 36 characters long)
            return {
                "@item_number_type": identifier.get("identifier_type", "").lower(),
                "#text": identifier.get("identifier", None).replace("-", ""),
            }


def get_publication_date(obj, media_type: str | None = None) -> Dict | None:
    """get publication date"""
    pub_date_str = dig(obj, "date_published")
    if pub_date_str is None:
        return None

    try:
        pub_date = date_parse(pub_date_str)
    except (ValueError, TypeError) as e:
        log.warning(f"Failed to parse publication date '{pub_date_str}': {e}")
        return None

    publication_date = {
        "@media_type": media_type,
        "month": f"{pub_date.month:d}",
        "day": f"{pub_date.day:d}",
        "year": str(pub_date.year),
    }

    # If this record includes JATS abstracts, declare the namespace on the
    # publication_date element as well (some downstream consumers/tests expect
    # it there).
    if media_type is not None and get_abstracts(obj):
        publication_date["@xmlns:jats"] = "http://www.ncbi.nlm.nih.gov/JATS1"

    return compact(publication_date)


def get_archive_locations(obj) -> list | None:
    """get archive locations"""
    if len(wrap(dig(obj, "archive_locations"))) == 0:
        return None

    return [
        {"archive": {"@name": location}} for location in dig(obj, "archive_locations")
    ]


def get_version_info(obj) -> dict | None:
    """get version_info"""
    if dig(obj, "version") is None:
        return None
    # TODO: add optional description and xml:lang attributes
    return compact({"version": dig(obj, "version")})


def get_references(obj) -> Dict | None:
    """get references"""
    if len(wrap(dig(obj, "references"))) == 0:
        return None

    citations = []
    for i, ref in enumerate(dig(obj, "references", [])):
        # Validate DOI before using it
        doi = doi_from_url(ref.get("id", None))
        # the commonmeta `reference` field is the formatted reference string
        # (Crossref's unstructured_citation); fall back to the legacy field.
        unstructured = ref.get("reference", None) or ref.get("unstructured", None)

        # include id in unstructured_citation if it is not a DOI
        if (
            doi is None
            and unstructured is not None
            and ref.get("id", None) is not None
            and not unstructured.endswith(ref.get("id"))
        ):
            unstructured += " " + ref.get("id")

        reference = compact(
            {
                "@key": ref.get("key", f"ref{i + 1}"),
                "doi": doi,
                "journal_title": ref.get("journal_title", None),
                "author": ref.get("author", None),
                "volume": ref.get("volume", None),
                "first_page": ref.get("first_page", None),
                "cYear": ref.get("publication_year", None),
                "article_title": ref.get("title", None),
                "unstructured_citation": unstructured,
            }
        )
        citations.append(reference)
    return {"citation": citations}


def get_license(obj) -> dict | None:
    """get license"""
    rights_uri = dig(obj, "license.url")
    if rights_uri is None:
        return None

    return {
        "@xmlns:ai": "http://www.crossref.org/AccessIndicators.xsd",
        "@name": "AccessIndicators",
        "ai:license_ref": [
            {"@applies_to": "vor", "#text": rights_uri},
            {"@applies_to": "tdm", "#text": rights_uri},
        ],
    }


def get_funding_references(obj) -> dict | None:
    """Get funding references"""
    if len(wrap(dig(obj, "funding_references"))) == 0:
        return None

    funding_refs = wrap(dig(obj, "funding_references"))
    assertions = []

    # Check if we need funding groups (multiple funders with award numbers)
    funders_with_awards = [
        f for f in funding_refs if f.get("award_number", None) is not None
    ]
    unique_funders = set(
        f.get("funder_id", None) or f.get("funder_name", None)
        for f in funding_refs
        if f.get("funder_id", None) is not None
        or f.get("funder_name", None) is not None
    )

    use_funding_groups = len(funders_with_awards) > 0 and len(unique_funders) > 1

    for funding_reference in funding_refs:
        group_assertions = []

        # Handle funder identifier/name. funder_id is ROR-only per v1.0.
        funder_id = funding_reference.get("funder_id", None)
        funder_name = funding_reference.get("funder_name", None)

        if funder_id:
            funder_assertion = {"@name": "ror", "#text": funder_id}
            group_assertions.append(funder_assertion)
        elif funder_name:
            funder_assertion = {"@name": "funder_name", "#text": funder_name}
            group_assertions.append(funder_assertion)

        # Handle award number
        award_number = funding_reference.get("award_number", None)
        if award_number:
            award_assertion = {"@name": "award_number", "#text": award_number}
            group_assertions.append(award_assertion)

        # Add to main assertions list
        if use_funding_groups:
            # Wrap in funding group
            funding_group = {
                "@name": "fundgroup",
                "fr:assertion": group_assertions,
            }
            assertions.append(funding_group)
        else:
            # Add assertions directly
            assertions.extend(group_assertions)

    if not assertions:
        return None

    return {
        "@xmlns:fr": "http://www.crossref.org/fundref.xsd",
        "@name": "fundref",
        "fr:assertion": assertions,
    }


def get_relations(obj) -> Dict | None:
    """get relations"""
    if len(wrap(dig(obj, "relations"))) == 0:
        return None

    def format_relation(relation):
        """format relation"""
        relation_type = relation.get("type", None)
        if relation_type is None:
            return None

        if relation_type in [
            "IsPartOf",
            "HasPart",
            "IsReviewOf",
            "HasReview",
            "IsRelatedMaterial",
            "HasRelatedMaterial",
        ]:
            group = "rel:inter_work_relation"
        elif relation_type in [
            "IsIdenticalTo",
            "IsPreprintOf",
            "HasPreprint",
            "IsTranslationOf",
            "HasTranslation",
            "IsVersionOf",
            "HasVersion",
        ]:
            group = "rel:intra_work_relation"
        else:
            return None

        relation_id = relation.get("id", None)
        if relation_id is None:
            return None

        # InvenioRDM community relations (…/api/communities/…) are only used by
        # the InvenioRDM writer to add records to communities; they are not
        # emitted as related works in Crossref XML.
        if "/api/communities/" in relation_id:
            return None

        f = furl(relation_id)
        if validate_doi(relation_id):
            identifier_type = "doi"
            _id = doi_from_url(relation_id)
        elif f.host == "portal.issn.org" and obj.type in ["Preprint", "BlogPost"]:
            identifier_type = "issn"
            _id = f.path.segments[-1] if f.path.segments else None
        elif validate_url(relation_id) == "URL":
            identifier_type = "uri"
            _id = relation_id
        else:
            identifier_type = "other"
            _id = relation_id

        if _id is None:
            return None

        return {
            group: {
                "@relationship-type": relation_type[0].lower() + relation_type[1:],
                "@identifier-type": identifier_type,
                "#text": _id,
            }
        }

    related_items = [
        format_relation(i)
        for i in dig(obj, "relations")
        if format_relation(i) is not None
    ]

    if not related_items:
        return None

    return {
        "@xmlns:rel": "http://www.crossref.org/relations.xsd",
        "@name": "relations",
        "rel:related_item": related_items,
    }


def get_subjects(obj) -> list | None:
    """Get crossref subjects"""
    if dig(obj, "subjects") is None:
        return None
    subjects = []
    for subject in dig(obj, "subjects"):
        if isinstance(subject, dict):
            subjects.append(subject.get("subject", None))
        else:
            subjects.append(subject)
    return subjects


def get_doi_data(obj) -> dict | None:
    """get doi data"""
    if doi_from_url(dig(obj, "id")) is None or dig(obj, "url") is None:
        return None

    items = [{"resource": {"@mime_type": "text/html", "#text": dig(obj, "url")}}]
    for file in wrap(dig(obj, "files")):
        if (
            file.get("mime_type", None) is not None
            and file.get("url", None) is not None
        ):
            items.append(
                {
                    "resource": {
                        "@mime_type": file.get("mime_type"),
                        "#text": file.get("url"),
                    }
                }
            )

    return compact(
        {
            "doi": doi_from_url(dig(obj, "id")),
            "resource": dig(obj, "url"),
            "collection": {
                "@property": "text-mining",
                "item": items,
            },
        }
    )


def get_isbn(obj, media_type: str | None = None) -> list[dict] | None:
    """get isbn. Returns array of objects with #text and @media_type."""
    cid, cid_type = container_identifier(dig(obj, "container"))
    if cid_type != "ISBN" or cid is None:
        return None
    isbn = cid
    normalized_isbn = normalize_isbn_crossref(isbn)
    if normalized_isbn is None:
        return None

    attrs = {}
    if media_type:
        # Map 'online' to 'electronic' as per Crossref XSD requirements
        if media_type == "online":
            media_type = "electronic"
        attrs["media_type"] = media_type

    if attrs:
        return [{"@media_type": attrs.get("media_type"), "#text": normalized_isbn}]
    return [{"#text": normalized_isbn}]


def normalize_isbn_crossref(isbn: str) -> str | None:
    """Normalize ISBN for Crossref XML.

    Crossref XSD pattern: (97(8|9)-)?\\d[\\d \\-]+[\\dX]
    """
    if not isbn:
        return None

    # Get canonical ISBN (removes hyphens and validates)
    isbn_canonical = canonical(isbn)
    if isbn_canonical is None:
        return None

    # For ISBN-13
    if is_isbn13(isbn_canonical):
        return (
            f"{isbn_canonical[:3]}-{isbn_canonical[3:]}"  # Add hyphen after 978 or 979
        )

    # For ISBN-10
    elif is_isbn10(isbn_canonical):
        return isbn_canonical  # ISBN-10 is already in the correct format

    # If we can't properly format it, return None rather than invalid format
    return None


def get_issn(obj):
    """get issn"""
    cid, cid_type = container_identifier(dig(obj, "container"))
    if cid_type == "ISSN":
        return cid

    for identifier in wrap(dig(obj, "identifiers")):
        if identifier.get("identifier_type") == "ISSN":
            return identifier.get("identifier")

    return None


class CrossrefXMLClient:
    """Crossref XML API client wrapper."""

    def __init__(
        self,
        username: str,
        password: str,
        prefixes: list = ["10.5555"],
        test_mode: bool = False,
        timeout: int = 30,
    ):
        """Initialize the Crossref API client wrapper.

        :param username: Crossref login ID.
        :param password: Crossref login password.
        :param timeout: Request timeout in seconds.
        """
        self.login_id = username
        self.login_passwd = password
        self.timeout = timeout
        self.prefixes = [str(prefix) for prefix in prefixes]

        if test_mode:
            self.api_url = "https://test.crossref.org/servlet/deposit"
        else:
            self.api_url = "https://doi.crossref.org/servlet/deposit"

    def post(self, input_xml: str | bytes) -> str:
        """Upload metadata for a new or existing DOI.

        :param input_xml: XML metadata following the Crossref Metadata Schema (str or bytes).
        :return: Status string ('SUCCESS' or '{}' on error).
        """
        try:
            # Convert string to bytes if necessary
            if isinstance(input_xml, str):
                input_xml = input_xml.encode("utf-8")

            # The filename displayed in the Crossref admin interface
            filename = f"{int(time())}"

            multipart_data = MultipartEncoder(
                fields={
                    "fname": (filename, io.BytesIO(input_xml), "application/xml"),
                    "operation": "doMDUpload",
                    "login_id": self.login_id,
                    "login_passwd": self.login_passwd,
                }
            )

            headers = {"Content-Type": multipart_data.content_type}

            # Make the request
            resp = requests.post(
                self.api_url, data=multipart_data, headers=headers, timeout=self.timeout
            )
            resp.raise_for_status()

            return self._parse_response(resp)

        except RequestException as e:
            log.error(f"Failed to upload to Crossref: {e}")
            return "{}"

    def _parse_response(self, resp) -> str:
        """Parse the Crossref API response.

        :param resp: Response object from requests.
        :return: Status string ('SUCCESS' or 'error message' on error).
        """
        try:
            # Check content type
            content_type = resp.headers.get("content-type", "").lower()
            if "xml" not in content_type and "html" not in content_type:
                log.error(f"Unexpected content type: {content_type}")
                log.error(f"Response body: {resp.text}")
                return "{}"

            response = parse_xml(resp.content)

            status = dig(response, "html.body.h2")
            if status != "SUCCESS":
                # Handle error response
                message = dig(response, "html.body.p")
                log.error(f"Crossref API error: {message}")
                return message

            return status

        except Exception as e:
            log.error(f"Failed to parse Crossref response: {e}")
            log.error(
                f"Response content type: {resp.headers.get('content-type', 'unknown')}"
            )
            log.error(f"Response body: {resp.text}")
            return "{}"


"""Errors for the Crossref XML API.

Error responses will be converted into an exception from this module.
"""


class HttpError(Exception):
    """Exception raised when a connection problem happens."""


class CrossrefError(Exception):
    """Exception raised when the server returns a known HTTP error code.

    Known HTTP error codes include:

    * 204 No Content
    * 400 Bad Request
    * 401 Unauthorized
    * 403 Forbidden
    * 404 Not Found
    * 410 Gone (deleted)
    """

    @staticmethod
    def factory(err_code, *args):
        """Create exceptions through a Factory based on the HTTP error code."""
        if err_code == 204:
            return CrossrefNoContentError(*args)
        elif err_code == 400:
            return CrossrefBadRequestError(*args)
        elif err_code == 401:
            return CrossrefUnauthorizedError(*args)
        elif err_code == 403:
            return CrossrefForbiddenError(*args)
        elif err_code == 404:
            return CrossrefNotFoundError(*args)
        elif err_code == 410:
            return CrossrefGoneError(*args)
        else:
            return CrossrefServerError(*args)


class CrossrefServerError(CrossrefError):
    """An internal server error happened on the Crossref end. Try later.

    Base class for all 5XX-related HTTP error codes.
    """


class CrossrefRequestError(CrossrefError):
    """A Crossref request error. You made an invalid request.

    Base class for all 4XX-related HTTP error codes as well as 204.
    """


class CrossrefNoContentError(CrossrefRequestError):
    """DOI is known to Crossref, but not resolvable.

    This might be due to handle's latency.
    """


class CrossrefBadRequestError(CrossrefRequestError):
    """Bad request error.

    Bad requests can include e.g. invalid XML, wrong domain, wrong prefix.
    """


class CrossrefUnauthorizedError(CrossrefRequestError):
    """Bad username or password."""


class CrossrefForbiddenError(CrossrefRequestError):
    """Login problem, record belongs to another party or quota exceeded."""


class CrossrefNotFoundError(CrossrefRequestError):
    """DOI does not exist in the database."""


class CrossrefGoneError(CrossrefRequestError):
    """DOI is no longer available."""
