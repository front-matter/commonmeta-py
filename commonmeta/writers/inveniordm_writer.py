"""InvenioRDM writer for commonmeta-py"""

import re
from time import time
from typing import Optional
from urllib.parse import urlparse

import orjson as json
import pydash as py_
import requests

from ..base_utils import compact, parse_attributes, presence, wrap
from ..constants import (
    CM_TO_INVENIORDM_TRANSLATIONS,
    COMMUNITY_TRANSLATIONS,
    CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS,
    INVENIORDM_IDENTIFIER_TYPES,
)
from ..date_utils import get_iso8601_date
from ..doi_utils import doi_from_url, normalize_doi
from ..utils import (
    FOS_MAPPINGS,
    get_language,
    id_from_url,
    normalize_url,
    pages_as_string,
    validate_orcid,
    validate_ror,
)


def write_inveniordm(metadata):
    """Write inveniordm"""
    if metadata is None or metadata.write_errors is not None:
        return None
    _type = CM_TO_INVENIORDM_TRANSLATIONS.get(metadata.type, "Other")
    creators = [
        to_inveniordm_creator(i)
        for i in wrap(metadata.contributors)
        if i.get("contributorRoles", None) == ["Author"]
    ]
    identifiers = [
        {
            "identifier": i.get("identifier", None),
            "scheme": INVENIORDM_IDENTIFIER_TYPES.get(
                i.get("identifierType", None), "other"
            ),
        }
        for i in wrap(metadata.identifiers)
        if i.get("identifierType", None) != "DOI"
    ]
    identifiers.append(
        {
            "identifier": metadata.url,
            "scheme": "url",
        }
    )
    references = [to_inveniordm_reference(i) for i in wrap(metadata.references)]
    related_identifiers = [
        to_inveniordm_related_identifier(i)
        for i in wrap(metadata.relations)
        if i.get("id", None) and i.get("type", None) != "IsPartOf"
    ]
    funding = compact(
        [
            to_inveniordm_funding(i)
            for i in wrap(metadata.funding_references)
            if i.get("funderName", None)
        ]
    )
    container = metadata.container if metadata.container else {}
    journal_title = (
        container.get("title", None)
        if _type not in ["inbook", "inproceedings"]
        and container.get("type") in ["Journal", "Periodical", "Blog"]
        else None
    )
    issn = (
        container.get("identifier", None)
        if container.get("identifierType", None) == "ISSN"
        else None
    )
    volume = container.get("volume", None)
    issue = container.get("issue", None)
    pages = pages_as_string(container)

    dates = []
    for date in metadata.date.keys():
        if metadata.date.get(date, None) is None:
            continue
        t = date.lower()
        if t == "published":
            t = "issued"
        elif t == "accessed":
            t = "other"
        dates.append(
            {
                "date": metadata.date.get(date),
                "type": {"id": t},
            }
        )

    subjects = [to_inveniordm_subject(i) for i in wrap(metadata.subjects)]
    return compact(
        {
            "pids": {
                "doi": {
                    "identifier": doi_from_url(metadata.id),
                    "provider": "external",
                },
            },
            "access": {"record": "public", "files": "public"},
            "files": {"enabled": False},
            "metadata": compact(
                {
                    "resource_type": {"id": _type},
                    "creators": creators,
                    "title": parse_attributes(
                        metadata.titles, content="title", first=True
                    ),
                    "publisher": metadata.publisher.get("name", None)
                    if metadata.publisher
                    else None,
                    "publication_date": get_iso8601_date(metadata.date.get("published"))
                    if metadata.date.get("published", None)
                    else None,
                    "dates": presence(dates),
                    "subjects": presence(subjects),
                    "description": parse_attributes(
                        metadata.descriptions, content="description", first=True
                    ),
                    "rights": [{"id": metadata.license.get("id").lower()}]
                    if metadata.license.get("id", None)
                    else None,
                    "languages": [
                        {"id": get_language(metadata.language, format="alpha_3")}
                    ]
                    if metadata.language
                    else None,
                    "identifiers": identifiers,
                    "references": presence(references),
                    "related_identifiers": presence(related_identifiers),
                    "funding": presence(funding),
                    "version": metadata.version,
                }
            ),
            "custom_fields": compact(
                {
                    "journal:journal": compact(
                        {
                            "title": journal_title,
                            "issn": issn,
                            "volume": volume,
                            "issue": issue,
                            "pages": pages,
                        }
                    ),
                    "rs:content_html": presence(metadata.content),
                    "rs:image": presence(metadata.image),
                    "rs:generator": container.get("platform", None),
                }
            ),
        }
    )


def to_inveniordm_creator(creator: dict) -> dict:
    """Convert creators to inveniordm creators"""

    def format_identifier(id):
        identifier = validate_orcid(id)
        if identifier:
            return [
                {
                    "identifier": identifier,
                    "scheme": "orcid",
                }
            ]
        return None

    _type = creator.get("type", None)
    if creator.get("familyName", None):
        name = ", ".join([creator.get("familyName", ""), creator.get("givenName", "")])
    elif creator.get("name", None):
        name = creator.get("name", None)

    return compact(
        {
            "person_or_org": compact(
                {
                    "name": name,
                    "given_name": creator.get("givenName", None),
                    "family_name": creator.get("familyName", None),
                    "type": _type.lower() + "al" if _type else None,
                    "identifiers": format_identifier(creator.get("id", None)),
                }
            ),
            "affiliations": to_inveniordm_affiliations(creator),
        }
    )


def to_inveniordm_subject(sub: dict) -> Optional[dict]:
    """Convert subject to inveniordm subject"""
    if sub.get("subject", None) is None:
        return None
    if sub.get("subject").startswith("FOS: "):
        subject = sub.get("subject")[5:]
        id_ = FOS_MAPPINGS.get(subject, None)
        return compact(
            {
                "id": id_,
                "subject": subject,
            }
        )
    return compact(
        {
            "subject": sub.get("subject"),
        }
    )


def to_inveniordm_affiliations(creator: dict) -> Optional[list]:
    """Convert affiliations to inveniordm affiliations.
    Returns None if creator is not a person."""

    def format_affiliation(affiliation):
        return compact(
            {
                "id": id_from_url(affiliation.get("id", None)),
                "name": affiliation.get("name", None),
            }
        )

    if creator.get("type", None) != "Person":
        return None

    return compact(
        [format_affiliation(i) for i in wrap(creator.get("affiliations", None))]
    )


def to_inveniordm_related_identifier(relation: dict) -> dict:
    """Convert relation to inveniordm related_identifier"""
    if normalize_doi(relation.get("id", None)):
        identifier = doi_from_url(relation.get("id", None))
        scheme = "doi"
    elif normalize_url(relation.get("id", None)):
        identifier = relation.get("id", None)
        scheme = "url"
    else:
        return None

    # normalize relation types
    relation_type = relation.get("type")
    if relation.get("type") == "HasReview":
        relation_type = "IsReviewedBy"
    elif relation.get("type") == "IsPreprintOf":
        relation_type = "IsPreviousVersionOf"

    return compact(
        {
            "identifier": identifier,
            "scheme": scheme,
            "relation_type": {
                "id": relation_type.lower(),
            },
        }
    )


def to_inveniordm_reference(reference: dict) -> dict:
    """Convert reference to inveniordm reference"""
    if normalize_doi(reference.get("id", None)):
        identifier = doi_from_url(reference.get("id", None))
        scheme = "doi"
    elif normalize_url(reference.get("id", None)):
        identifier = reference.get("id", None)
        scheme = "url"
    else:
        identifier = None
        scheme = None

    if reference.get("unstructured", None) is None:
        # use title as unstructured reference
        if reference.get("title", None):
            unstructured = reference.get("title")
        else:
            unstructured = "Unknown title"

        if reference.get("publicationYear", None):
            unstructured += " (" + reference.get("publicationYear") + ")."

        return compact(
            {
                "reference": unstructured,
                "scheme": scheme,
                "identifier": identifier,
            }
        )
    else:
        unstructured = reference.get("unstructured")

        if reference.get("id", None):
            # remove duplicate ID from unstructured reference
            unstructured = unstructured.replace(reference.get("id"), "")

        # remove optional trailing whitespace
        unstructured = unstructured.rstrip()

        return compact(
            {
                "reference": unstructured,
                "scheme": scheme,
                "identifier": identifier,
            }
        )


def to_inveniordm_funding(funding: dict) -> Optional[dict]:
    """Convert funding to inveniordm funding"""
    if funding.get("funderIdentifierType", None) == "Crossref Funder ID":
        # convert to ROR
        funder_identifier = id_from_url(
            CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS.get(
                funding.get("funderIdentifier", None), None
            )
        )
    else:
        funder_identifier = validate_ror(funding.get("funderIdentifier", None))
    award_number = funding.get("awardNumber", None)
    award_title = funding.get("awardTitle", None)
    if award_title:
        award_title = {"en": award_title}
    if funding.get("awardUri", None):
        award_identifier = funding.get("awardUri", None)
        scheme = "doi" if normalize_doi(award_identifier) else "url"
        if scheme == "doi":
            award_identifier = doi_from_url(award_identifier)
        award_identifiers = [
            {
                "scheme": scheme,
                "identifier": award_identifier,
            },
        ]
    else:
        award_identifiers = None

    if award_number or award_title or award_identifiers:
        return compact(
            {
                "funder": compact(
                    {
                        "name": funding.get("funderName"),
                        "id": funder_identifier,
                    }
                ),
                "award": compact(
                    {
                        "number": award_number,
                        "title": award_title,
                        "identifiers": award_identifiers,
                    }
                ),
            }
        )

    return compact(
        {
            "funder": compact(
                {
                    "name": funding.get("funderName"),
                    "id": funder_identifier,
                }
            ),
        }
    )


def write_inveniordm_list(metalist):
    """Write InvenioRDM list"""
    if metalist is None:
        return None
    return [write_inveniordm(item) for item in metalist.items]


def push_inveniordm(metadata, host: str, token: str, legacy_key: str):
    """Push record to InvenioRDM"""

    record = {}
    input = write_inveniordm(metadata)

    try:
        # Remove IsPartOf relation with InvenioRDM community identifier after storing it
        community_index = None
        if hasattr(metadata, "relations") and metadata.relations:
            for i, relation in enumerate(metadata.relations):
                if relation.get("type") == "IsPartOf" and relation.get(
                    "id", ""
                ).startswith("https://rogue-scholar.org/api/communities/"):
                    slug = relation.get("id").split("/")[5]
                    community_id, _ = search_by_slug(slug, "blog", host, token)
                    if community_id:
                        record["community"] = slug
                        record["community_id"] = community_id
                        community_index = i

            # Remove the relation if we found and processed it
            if community_index is not None and hasattr(metadata, "relations"):
                metadata.relations.pop(community_index)

        # Remove InvenioRDM rid after storing it
        # rid_index = None
        # if hasattr(metadata, "identifiers") and metadata.identifiers:
        #     for i, identifier in enumerate(metadata.identifiers):
        #         if identifier.get("identifierType") == "RID" and identifier.get("identifier"):
        #             record["id"] = identifier.get("identifier")
        #             rid_index = i
        #         elif identifier.get("identifierType") == "UUID" and identifier.get("identifier"):
        #             record["uuid"] = identifier.get("identifier")

        # # Remove the identifier if we found and processed it
        # if rid_index is not None and hasattr(metadata, "identifiers"):
        #     metadata.identifiers.pop(rid_index)

        # Check if record already exists in InvenioRDM
        record["id"] = search_by_doi(doi_from_url(metadata.id), host, token)

        if record["id"] is not None:
            # Create draft record from published record
            record = edit_published_record(record, host, token)

            # Update draft record
            record = update_draft_record(record, host, token, input)
        else:
            # Create draft record
            record = create_draft_record(record, host, token, input)

        # Publish draft record
        record = publish_draft_record(record, host, token)

        # Add record to blog community if blog community is specified and exists
        if record.get("community_id", None) is not None:
            record = add_record_to_community(
                record, host, token, record["community_id"]
            )

        # Add record to subject area community if subject area community is specified and exists
        # Subject area communities should exist for all subjects in the FOSMappings

        if hasattr(metadata, "subjects"):
            for subject in metadata.subjects:
                slug = string_to_slug(subject.get("subject", ""))
                if slug in COMMUNITY_TRANSLATIONS:
                    slug = COMMUNITY_TRANSLATIONS[slug]

                community_id = search_by_slug(slug, "topic", host, token)
                if community_id:
                    record = add_record_to_community(record, host, token, community_id)

        # Add record to communities defined as IsPartOf relation in inveniordm metadata's RelatedIdentifiers
        related_identifiers = py_.get(input, "metadata.related_identifiers")

        for identifier in wrap(related_identifiers):
            if py_.get(identifier, "relation_type.id") == "ispartof":
                parsed_url = urlparse(identifier.get("identifier", ""))
                path_parts = parsed_url.path.split("/")

                if (
                    parsed_url.netloc == urlparse(host).netloc
                    and len(path_parts) == 3
                    and path_parts[1] == "communities"
                ):
                    record = add_record_to_community(record, host, token, path_parts[2])

        # optionally update rogue-scholar legacy record
        if host == "rogue-scholar.org" and legacy_key is not None:
            record = update_legacy_record(record, legacy_key)
        print("g", record)
    except Exception as e:
        raise InvenioRDMError(f"Unexpected error: {str(e)}")

    return record


def push_inveniordm_list(metalist, host: str, token: str, legacy_key: str) -> list:
    """Push inveniordm list to InvenioRDM, returns list of push results."""

    if metalist is None:
        return None
    items = [push_inveniordm(item, host, token, legacy_key) for item in metalist.items]
    return json.dumps(items, option=json.OPT_INDENT_2)


def search_by_doi(doi, host, token) -> Optional[str]:
    """Search for a record by DOI in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = {"q": f"doi:{doi}", "size": 1}
    try:
        response = requests.get(
            f"https://{host}/api/records", headers=headers, params=params
        )
        response.raise_for_status()
        data = response.json()
        if py_.get(data, "hits.total") or 0 > 0:
            return py_.get(data, "hits.hits.0.id")
        return None
    except requests.exceptions.RequestException as e:
        raise InvenioRDMError(f"Error searching for DOI: {str(e)}")


def create_draft_record(record, host, token, input):
    """Create a new draft record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            f"https://{host}/api/records", headers=headers, json=input
        )
        response.raise_for_status()
        data = response.json()
        return {
            "id": data.get("id", None),
            "created": data.get("created", None),
            "updated": data.get("updated", None),
            "status": "updated",
        }
    except requests.exceptions.RequestException as e:
        raise InvenioRDMError(f"Error creating draft record: {str(e)}")


def edit_published_record(record, host, token):
    """Create a draft from a published record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            f"https://{host}/api/records/{record['id']}/draft", headers=headers
        )
        response.raise_for_status()
        data = response.json()
        record["doi"] = py_.get(data, "pids.doi.identifier")
        record["created"] = data.get("created", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "edited"
        return record
    except requests.exceptions.RequestException as e:
        raise InvenioRDMError(f"Error creating draft from published record: {str(e)}")


def update_draft_record(record, host, token, inveniordm_data):
    """Update a draft record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.put(
            f"https://{host}/api/records/{record['id']}/draft",
            headers=headers,
            json=inveniordm_data,
        )
        response.raise_for_status()
        data = response.json()
        record["created"] = data.get("created", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "updated"
        return record
    except requests.exceptions.RequestException as e:
        raise InvenioRDMError(f"Error updating draft record: {str(e)}")


def publish_draft_record(record, host, token):
    """Publish a draft record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            f"https://{host}/api/records/{record['id']}/draft/actions/publish",
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        record["uuid"] = py_.get(data, "metadata.identifiers.0.identifier")
        record["created"] = data.get("created", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "published"
        return record
    except requests.exceptions.RequestException as e:
        raise InvenioRDMError(f"Error publishing draft record: {str(e)}")


def add_record_to_community(record, host, token, community_id):
    """Add a record to a community in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            f"https://{host}/api/records/{record['id']}/communities",
            headers=headers,
            json={"id": community_id},
        )
        response.raise_for_status()
        return record
    except requests.exceptions.RequestException as e:
        raise InvenioRDMError(f"Error adding record to community: {str(e)}")


def update_legacy_record(record, legacy_key: str):
    """Update corresponding record in Rogue Scholar legacy database."""

    legacy_host = "bosczcmeodcrajtcaddf.supabase.co"

    if not legacy_key:
        return record, ValueError("no legacy key provided")
    if not record.get("uuid", None):
        return record, ValueError("no UUID provided")
    if not record.get("doi", None):
        return ValueError("no valid doi to update")

    now = f"{int(time())}"
    if record.get("id", None) is not None:
        output = {
            "rid": record.get("id"),
            "indexed_at": now,
            "indexed": "true",
            "archived": "true",
        }
    else:
        output = {
            "doi": record.get("doi"),
            "indexed_at": now,
            "indexed": "true",
            "archived": "true",
        }

    request_url = f"https://{legacy_host}/rest/v1/posts?id=eq.{record['uuid']}"
    headers = {
        "Content-Type": "application/json",
        "apikey": legacy_key,
        "Authorization": f"Bearer {legacy_key}",
        "Prefer": "return=minimal",
    }

    try:
        response = requests.patch(request_url, json=output, headers=headers, timeout=30)
        response.raise_for_status()
        if response.status_code != 204:
            return record, Exception(f"Unexpected status code: {response.status_code}")

        record["status"] = "updated_legacy"
        return record

    except requests.exceptions.RequestException as e:
        raise InvenioRDMError(f"Error updating legacy record: {str(e)}")


def search_by_slug(slug, type_value, host, token) -> Optional[str]:
    """Search for a community by slug in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = {"q": f"slug:{slug} AND type:{type_value}", "size": 1}
    try:
        response = requests.get(
            f"https://{host}/api/communities", headers=headers, params=params
        )
        response.raise_for_status()
        data = response.json()
        if py_.get(data, "hits.total") or 0 > 0:
            return py_.get(data, "hits.hits.0.id")
        return None
    except requests.exceptions.RequestException as e:
        raise InvenioRDMError(f"Error searching for community: {str(e)}")


def string_to_slug(text):
    """Convert a string to a slug format"""
    # Replace spaces with hyphens
    slug = re.sub(r"\s+", "-", text.lower())
    # Remove special characters
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r"-+", "-", slug)
    # Remove leading and trailing hyphens
    slug = slug.strip("-")
    return slug


class InvenioRDMError(Exception):
    """Custom exception for InvenioRDM API errors"""
