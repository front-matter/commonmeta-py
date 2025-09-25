"""Crossref XML writer for commonmeta-py"""

import io
import logging
from datetime import datetime
from time import time
from typing import Dict, Optional, Union

import orjson as json
import requests
from dateutil.parser import parse as date_parse
from furl import furl
from isbnlib import canonical, is_isbn10, is_isbn13
from marshmallow import Schema, fields
from requests_toolbelt.multipart.encoder import MultipartEncoder

from ..base_utils import compact, dig, parse_xml, unparse_xml, unparse_xml_list, wrap
from ..constants import Commonmeta
from ..doi_utils import doi_from_url, is_rogue_scholar_doi, validate_doi
from ..utils import validate_url
from .inveniordm_writer import push_inveniordm, update_legacy_record

log = logging.getLogger(__name__)

POSTED_CONTENT_TYPES = [
    "preprint",
    "working_paper",
    "letter",
    "dissertation",
    "report",
    "review",
    "other",
]

MARSHMALLOW_MAP = {
    "abstracts": "jats:abstract",
    "license": "ai:program",
    "funding_references": "fr:program",
    "relations": "rel:program",
    "references": "citation_list",
}


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
    isbn = fields.String()
    issn = fields.String()
    publisher = fields.Dict()
    description = fields.Dict()
    funding_references = fields.Dict(data_key="fr:program")
    license = fields.Dict(data_key="ai:program")
    relations = fields.Dict(data_key="rel:program")
    archive_locations = fields.List(fields.Dict())
    doi_data = fields.Dict(data_key="doi_data")
    references = fields.Dict(data_key="citation_list")


def convert_crossref_xml(metadata: Commonmeta) -> Optional[dict]:
    """Convert Crossref XML"""

    # return None if type is not supported by Crossref
    if metadata.type not in [
        "Article",
        "BlogPost",
        "Book",
        "BookChapter",
        "Component",
        "Dataset",
        "Dissertation",
        "JournalArticle",
        "PeerReview",
        "ProceedingsArticle",
        "Report",
        "Standard",
    ]:
        log.error(f"Type not supported by Crossref: {metadata.id}")
        return None

    # return None if doi or url are not present
    if doi_from_url(metadata.id) is None or metadata.url is None:
        log.error(f"DOI or URL missing for Crossref XML: {metadata.id}")
        return None

    titles = get_titles(metadata)
    contributors = get_contributors(metadata)
    abstracts = get_abstracts(metadata)
    relations = get_relations(metadata)
    doi_data = get_doi_data(metadata)
    references = get_references(metadata)
    funding_references = get_funding_references(metadata)
    license = get_license(metadata)
    kwargs = {}

    if metadata.type == "Article":
        if metadata.additional_type in POSTED_CONTENT_TYPES:
            kwargs["type"] = metadata.additional_type
        else:
            kwargs["type"] = "other"
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
                "doi_data": doi_data,
                "references": references,
            }
        )
    elif metadata.type == "BlogPost":
        kwargs["type"] = "other"
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
                "doi_data": doi_data,
                "references": references,
            }
        )
    elif metadata.type == "Book":
        kwargs["book_type"] = "monograph"
        data = compact(
            {
                "book": get_attributes(metadata, **kwargs),
                "book_metadata": get_book_metadata(metadata),
                "contributors": contributors,
                "titles": titles,
                "abstracts": abstracts,
                "publication_date": get_publication_date(metadata, media_type="online"),
                "isbn": get_isbn(metadata, media_type="online"),
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
        data = compact(
            {
                "book": get_attributes(metadata, **kwargs),
                "book_metadata": get_book_metadata(metadata),
                "contributors": contributors,
                "titles": titles,
                "publication_date": get_publication_date(metadata, media_type="online"),
                "isbn": get_isbn(metadata),
                "publisher": get_publisher(metadata),
                "abstracts": abstracts,
                "funding_references": funding_references,
                "license": license,
                "relations": relations,
                "archive_locations": get_archive_locations(metadata),
                "doi_data": doi_data,
                "references": references,
            }
        )
    elif metadata.type == "Component":
        data = compact(
            {
                "sa_component": get_attributes(metadata),
                "component": {"@reg-agency": "CrossRef"},
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
        publisher = dig(metadata, "publisher.name")
        if publisher is not None:
            publisher_item = {
                "title": publisher,
            }
        data = compact(
            {
                "conference": get_attributes(metadata, **kwargs),
                "event_metadata": get_event_metadata(metadata),
                "proceedings_metadata": get_proceedings_metadata(metadata),
                "conference_paper": get_attributes(metadata, **kwargs),
                "contributors": contributors,
                "titles": titles,
                "publication_date": get_publication_date(metadata),
                "abstracts": abstracts,
                "publisher_item": publisher_item,
                "funding_references": funding_references,
                "license": license,
                "crossmark": None,
                "relations": relations,
                "archive_locations": get_archive_locations(metadata),
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
                "doi_data": doi_data,
                "references": references,
                "component_list": None,
            }
        )
    else:
        log.error(f"Another error occured for Crossref XML: {metadata.id}")
        data = None
    return data


def write_crossref_xml(metadata: Commonmeta) -> Optional[str]:
    """Write Crossref XML"""
    if metadata is None or not metadata.is_valid:
        log.error("Invalid metadata provided for Crossref XML generation")
        return None

    # Use the marshmallow schema to dump the data
    schema = CrossrefXMLSchema()

    data = convert_crossref_xml(metadata)
    if data is None:
        log.error(f"Could not convert metadata to Crossref XML: {metadata.id}")
        return None

    crossref_xml = schema.dump(data)

    # Ensure consistent field ordering through the defined mapping
    field_order = [MARSHMALLOW_MAP.get(k, k) for k in list(data.keys())]
    crossref_xml = {k: crossref_xml[k] for k in field_order if k in crossref_xml}

    head = {
        "depositor": metadata.depositor,
        "email": metadata.email,
        "registrant": metadata.registrant,
    }

    # Convert to XML
    return unparse_xml(crossref_xml, dialect="crossref", head=head)


def write_crossref_xml_list(metalist) -> Optional[str]:
    """Write crossref_xml list"""
    if metalist is None or not metalist.is_valid:
        log.error("Invalid metalist provided for Crossref XML generation")
        return None

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
    head = {
        "depositor": metalist.depositor,
        "email": metalist.email,
        "registrant": metalist.registrant,
    }
    return unparse_xml_list(crossref_xml_list, dialect="crossref", head=head)


def push_crossref_xml(
    metadata: Commonmeta,
    login_id: str,
    login_passwd: str,
    test_mode: bool,
    host: str,
    token: str,
    legacy_key: str,
) -> str:
    """Push crossref_xml to Crossref API, returns the API response."""

    input_xml = write_crossref_xml(metadata)
    if not input_xml:
        log.error("Failed to generate XML for upload")
        return "{}"

    client = CrossrefXMLClient(
        username=login_id,
        password=login_passwd,
        test_mode=test_mode,
    )
    status = client.post(input_xml)

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

    # update rogue-scholar legacy record if legacy_key is provided
    if is_rogue_scholar_doi(metadata.id, ra="crossref") and legacy_key is not None:
        uuid = dig(metadata, "identifiers.0.identifier")
        if uuid:
            record["uuid"] = uuid
            record = update_legacy_record(record, legacy_key=legacy_key, field="doi")

    # Return JSON response
    return json.dumps(record, option=json.OPT_INDENT_2).decode("utf-8")


def push_crossref_xml_list(
    metalist,
    login_id: str,
    login_passwd: str,
    test_mode: bool,
    host: str,
    token: str,
    legacy_key: str,
) -> str:
    """Push crossref_xml list to Crossref API, returns the API response."""

    input_xml = write_crossref_xml_list(metalist)
    if not input_xml:
        log.error("Failed to generate XML for upload")
        return "{}"

    client = CrossrefXMLClient(
        username=login_id,
        password=login_passwd,
        test_mode=test_mode,
    )
    status = client.post(input_xml)

    if status != "SUCCESS":
        log.error("Failed to upload XML to Crossref")
        return "{}"

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

        # update rogue-scholar legacy record if legacy_key is provided
        if is_rogue_scholar_doi(item.id, ra="crossref") and legacy_key is not None:
            uuid = dig(item, "identifiers.0.identifier")
            if uuid:
                record["uuid"] = uuid
                record = update_legacy_record(
                    record, legacy_key=legacy_key, field="doi"
                )
        items.append(record)

    # Return JSON response
    return json.dumps(items, option=json.OPT_INDENT_2).decode("utf-8")


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


def get_journal_metadata(obj) -> Optional[dict]:
    """get journal metadata"""
    issn = (
        dig(obj, "container.identifier")
        if dig(obj, "container.identifierType") == "ISSN"
        else None
    )
    return compact(
        {
            "@language": dig(obj, "language"),
            "full_title": dig(obj, "container.title"),
            "issn": issn,
        }
    )


def get_book_metadata(obj) -> Optional[dict]:
    return compact(
        {
            "@language": dig(obj, "language"),
        }
    )


def get_database_metadata(obj) -> Optional[dict]:
    return compact(
        {
            "@language": dig(obj, "language"),
        }
    )


def get_event_metadata(obj) -> Optional[dict]:
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


def get_proceedings_metadata(obj) -> Optional[dict]:
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
    if dig(obj, "container.identifierType") == "ISBN":
        proceedings_metadata["isbn"] = get_isbn(obj)
    return compact(proceedings_metadata)


def get_journal_issue(obj) -> Optional[dict]:
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


def get_institution(obj) -> Optional[dict]:
    """get institution"""
    if dig(obj, "publisher.name") is None:
        return None

    return {
        "institution_name": dig(obj, "publisher.name"),
    }


def get_titles(obj) -> Optional[dict]:
    """get titles"""

    titles = {}
    for t in wrap(dig(obj, "titles", [])):
        if isinstance(t, str):
            titles["title"] = t
        elif isinstance(t, dict) and t.get("titleType", None) == "Subtitle":
            titles["subtitle"] = t.get("title", None)
        elif isinstance(t, dict):
            titles["title"] = t.get("title", None)

    return titles if titles else None


def get_contributors(obj) -> Optional[dict]:
    """get contributors"""

    def map_affiliations(affiliations):
        """map affiliations"""
        if affiliations is None:
            return None
        return [
            compact(
                {
                    "institution": compact(
                        {
                            "institution_name": affiliation.get("name", None),
                            "institution_id": {
                                "#text": affiliation.get("id"),
                                "@type": "ror",
                            }
                            if affiliation.get("id", None) is not None
                            else None,
                        }
                    ),
                }
            )
            for affiliation in affiliations
        ]

    if len(wrap(dig(obj, "contributors"))) == 0:
        return None

    con = [
        c
        for c in dig(obj, "contributors", [])
        if c.get("contributorRoles", None) == ["Author"]
        or c.get("contributorRoles", None) == ["Editor"]
    ]

    person_names = []
    organizations = []
    anonymous_contributors = []

    for num, contributor in enumerate(con):
        contributor_role = (
            "author" if "Author" in contributor.get("contributorRoles") else None
        )
        if contributor_role is None:
            contributor_role = (
                "editor" if "Editor" in contributor.get("contributorRoles") else None
            )
        sequence = "first" if num == 0 else "additional"
        if (
            contributor.get("type", None) == "Organization"
            and contributor.get("name", None) is not None
        ):
            organizations.append(
                {
                    "@contributor_role": contributor_role,
                    "@sequence": sequence,
                    "#text": contributor.get("name"),
                }
            )
        elif (
            contributor.get("givenName", None) is not None
            or contributor.get("familyName", None) is not None
        ):
            person_names.append(
                compact(
                    {
                        "@contributor_role": contributor_role,
                        "@sequence": sequence,
                        "given_name": contributor.get("givenName", None),
                        "surname": contributor.get("familyName", None),
                        "affiliations": map_affiliations(
                            contributor.get("affiliations", None)
                        ),
                        "ORCID": contributor.get("id", None),
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
                            contributor.get("affiliations", None)
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


def get_publisher(obj) -> Optional[dict]:
    """get publisher"""
    if dig(obj, "publisher.name") is None:
        return None

    return {
        "publisher_name": dig(obj, "publisher.name"),
    }


def get_abstracts(obj) -> Optional[list]:
    """get abstracts"""
    if len(wrap(dig(obj, "descriptions"))) == 0:
        return None

    abstracts = []
    for d in wrap(dig(obj, "descriptions", [])):
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


def get_group_title(obj) -> Optional[str]:
    """Get group title from metadata"""
    return dig(obj, "container.title")


def get_item_number(obj) -> Optional[dict]:
    """Insert item number"""
    if len(wrap(dig(obj, "identifiers"))) == 0:
        return None

    for identifier in wrap(dig(obj, "identifiers")):
        if identifier.get("identifierType", None) == "UUID":
            # strip hyphen from UUIDs, as item_number can only be 32 characters long (UUIDv4 is 36 characters long)
            return {
                "@item_number_type": identifier.get("identifierType", "").lower(),
                "#text": identifier.get("identifier", None).replace("-", ""),
            }


def get_publication_date(obj, media_type: Optional[str] = None) -> Optional[Dict]:
    """get publication date"""
    pub_date_str = dig(obj, "date.published")
    if pub_date_str is None:
        return None

    try:
        pub_date = date_parse(pub_date_str)
    except (ValueError, TypeError) as e:
        log.warning(f"Failed to parse publication date '{pub_date_str}': {e}")
        return None

    return compact(
        {
            "@media_type": media_type,
            "month": f"{pub_date.month:d}",
            "day": f"{pub_date.day:d}",
            "year": str(pub_date.year),
        }
    )


def get_archive_locations(obj) -> Optional[list]:
    """get archive locations"""
    if len(wrap(dig(obj, "archive_locations"))) == 0:
        return None

    return [
        compact(
            {
                "archive": {"@name": location},
            }
        )
        for location in dig(obj, "archive_locations")
    ]


def get_references(obj) -> Optional[Dict]:
    """get references"""
    if len(wrap(dig(obj, "references"))) == 0:
        return None

    citations = []
    for i, ref in enumerate(dig(obj, "references", [])):
        # Validate DOI before using it
        doi = doi_from_url(ref.get("id", None))
        unstructured = ref.get("unstructured", None)

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
                "cYear": ref.get("publicationYear", None),
                "article_title": ref.get("title", None),
                "unstructured_citation": unstructured,
            }
        )
        citations.append(reference)
    return {"citation": citations}


def get_license(obj) -> Optional[dict]:
    """get license"""
    rights_uri = dig(obj, "license.url")
    if rights_uri is None:
        return None

    return {
        "@xmlns:ai": "http://www.crossref.org/AccessIndicators.xsd",
        "@name": "AccessIndicators",
        "ai:license_ref": [
            {
                "@applies_to": "vor",
                "#text": rights_uri,
            },
            {
                "@applies_to": "tdm",
                "#text": rights_uri,
            },
        ],
    }


def get_funding_references(obj) -> Optional[dict]:
    """Get funding references"""
    if len(wrap(dig(obj, "funding_references"))) == 0:
        return None

    funding_refs = wrap(dig(obj, "funding_references"))
    assertions = []

    # Check if we need funding groups (multiple funders with award numbers)
    funders_with_awards = [
        f for f in funding_refs if f.get("awardNumber", None) is not None
    ]
    unique_funders = set(
        f.get("funderIdentifier", None) or f.get("funderName", None)
        for f in funding_refs
        if f.get("funderIdentifier", None) is not None
        or f.get("funderName", None) is not None
    )

    use_funding_groups = len(funders_with_awards) > 0 and len(unique_funders) > 1

    for funding_reference in funding_refs:
        group_assertions = []

        # Handle funder identifier/name
        funder_identifier = funding_reference.get("funderIdentifier", None)
        funder_identifier_type = funding_reference.get("funderIdentifierType", None)
        funder_name = funding_reference.get("funderName", None)

        if funder_identifier and funder_identifier_type == "ROR":
            funder_assertion = {
                "@name": "ror",
                "#text": funder_identifier,
            }
            group_assertions.append(funder_assertion)
        elif funder_identifier and funder_identifier_type == "Crossref Funder ID":
            # Create nested structure for Crossref Funder ID
            funder_id_assertion = {
                "@name": "funder_identifier",
                "#text": funder_identifier,
            }
            funder_assertion = {
                "@name": "funder_name",
                "#text": funder_name,
                "fr:assertion": [funder_id_assertion],
            }
            group_assertions.append(funder_assertion)
        elif funder_name:
            funder_assertion = {
                "@name": "funder_name",
                "#text": funder_name,
            }
            group_assertions.append(funder_assertion)

        # Handle award number
        award_number = funding_reference.get("awardNumber", None)
        if award_number:
            award_assertion = {
                "@name": "award_number",
                "#text": award_number,
            }
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


def get_relations(obj) -> Optional[Dict]:
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

        f = furl(relation_id)
        if validate_doi(relation_id):
            identifier_type = "doi"
            _id = doi_from_url(relation_id)
        elif f.host == "portal.issn.org" and obj.type in ["Article", "BlogPost"]:
            identifier_type = "issn"
            _id = f.path.segments[-1] if f.path.segments else None
        elif validate_url(relation_id) == "URL":
            identifier_type = "uri"
            _id = relation_id
        else:
            identifier_type = "other"
            _id = relation_id

        return {
            group: compact(
                {
                    "@relationship-type": relation_type[0].lower() + relation_type[1:],
                    "@identifier-type": identifier_type,
                    "#text": _id,
                },
            )
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


def get_subjects(obj) -> Optional[list]:
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


def get_doi_data(obj) -> Optional[dict]:
    """get doi data"""
    if doi_from_url(dig(obj, "id")) is None or dig(obj, "url") is None:
        return None

    items = [
        {
            "resource": {
                "@mime_type": "text/html",
                "#text": dig(obj, "url"),
            }
        }
    ]
    for file in wrap(dig(obj, "files")):
        if file.get("mimeType", None) is not None and file.get("url", None) is not None:
            items.append(
                {
                    "resource": {
                        "@mime_type": file.get("mimeType"),
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


def get_isbn(obj, media_type: Optional[str] = None) -> Optional[Dict]:
    """get isbn"""
    if (
        dig(obj, "container.identifierType") != "ISBN"
        or dig(obj, "container.identifier") is None
    ):
        return None
    isbn = dig(obj, "container.identifier")
    return normalize_isbn_crossref(isbn)


def normalize_isbn_crossref(isbn: str) -> Optional[str]:
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
    if dig(obj, "container.identifierType") != "ISSN":
        return None
    return dig(obj, "container.identifier")


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

    def post(self, input_xml: Union[str, bytes]) -> str:
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

        except requests.exceptions.RequestException as e:
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
