"""InvenioRDM writer for commonmeta-py"""

import logging
from time import time
from typing import Dict, Optional

import orjson as json
import requests

from ..base_utils import compact, dig, parse_attributes, presence, wrap
from ..constants import (
    CM_TO_INVENIORDM_TRANSLATIONS,
    COMMUNITY_TRANSLATIONS,
    CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS,
    INVENIORDM_IDENTIFIER_TYPES,
    Commonmeta,
)
from ..date_utils import get_iso8601_date
from ..doi_utils import doi_from_url, is_rogue_scholar_doi, normalize_doi
from ..utils import (
    FOS_MAPPINGS,
    get_language,
    id_from_url,
    normalize_url,
    pages_as_string,
    string_to_slug,
    validate_orcid,
    validate_ror,
)

log = logging.getLogger(__name__)


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
    citations = [to_inveniordm_reference(i) for i in wrap(metadata.citations)]
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
                    "provider": "crossref"
                    if is_rogue_scholar_doi(metadata.id, ra="crossref")
                    else "external",
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
                    "rs:citations": presence(citations),
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

    def write_item(item):
        """write inveniordm item for inveniordm list"""

        return write_inveniordm(item)

    return [write_item(item) for item in metalist.items]


def push_inveniordm(metadata: Commonmeta, host: str, token: str, **kwargs) -> Dict:
    """Push record to InvenioRDM"""

    try:
        doi = normalize_doi(metadata.id)
        if doi is None:
            raise ValueError("no doi provided")

        record = {
            "doi": doi,
        }

        # extract optional information needed
        # uuid is the Rogue Scholar uuid
        # community_id is the id of the primary community of the record,
        # in the case of Rogue Scholar the blog community

        if hasattr(metadata, "identifiers") and metadata.identifiers:
            for identifier in metadata.identifiers:
                if (
                    isinstance(identifier, dict)
                    and identifier.get("identifierType") == "UUID"
                    and identifier.get("identifier")
                ):
                    record["uuid"] = identifier.get("identifier")
                    continue

        if hasattr(metadata, "relations") and metadata.relations:
            community_index = None
            for i, relation in enumerate(metadata.relations):
                if relation.get("type") == "IsPartOf" and relation.get(
                    "id", ""
                ).startswith(f"https://{host}/api/communities/"):
                    slug = relation.get("id").split("/")[5]
                    community_id = search_by_slug(slug, "blog", host, token)
                    if community_id:
                        record["community"] = slug
                        record["community_id"] = community_id
                        community_index = i
                        continue

            if community_index is not None:
                metadata.relations.pop(community_index)

        # upsert record via the InvenioRDM API
        record = upsert_record(metadata, host, token, record)

        # optionally add record to InvenioRDM communities
        record = add_record_to_communities(metadata, host, token, record)

        # optionally update external services
        record = update_external_services(metadata, host, token, record, **kwargs)

    except Exception as e:
        print(f"Error in push_inveniordm: {str(e)}")
        log.error(
            f"Unexpected error in push_inveniordm: {str(e)}",
            exc_info=True,
            extra={"host": host, "record_id": record.get("id")},
        )
        record["status"] = "error"

    return record


def push_inveniordm_list(metalist, host: str, token: str, **kwargs) -> list:
    """Push inveniordm list to InvenioRDM, returns list of push results."""

    if metalist is None:
        return None
    items = [push_inveniordm(item, host, token, **kwargs) for item in metalist.items]
    return json.dumps(items, option=json.OPT_INDENT_2)


def upsert_record(metadata: Commonmeta, host: str, token: str, record: dict) -> dict:
    """Upsert InvenioRDM record, based on DOI"""

    output = write_inveniordm(metadata)

    # Check if record already exists in InvenioRDM
    record["id"] = search_by_doi(doi_from_url(record.get("doi")), host, token)

    if record.get("id", None) is not None:
        # Create draft record from published record
        record = edit_published_record(record, host, token)

        # Update draft record
        record = update_draft_record(record, host, token, output)
    else:
        # Create draft record for DOI that is external or needs to be registered
        # (currently only supported for Crossref PID provider)
        record = create_draft_record(record, host, token, output)

    # Publish draft record
    record = publish_draft_record(record, host, token)

    return record


def add_record_to_communities(
    metadata: Commonmeta, host: str, token: str, record: dict
) -> dict:
    """Add record to one or more InvenioRDM communities"""

    communities = get_record_communities(record, host, token)
    community_ids = [c.get("id") for c in communities] if communities else []

    # Add record to primary community if primary community is specified
    if (
        record.get("community_id", None) is not None
        and record.get("community_id") not in community_ids
    ):
        record = add_record_to_community(record, host, token, record["community_id"])

    # Add record to subject area community if subject area community is specified
    # Subject area communities should exist for all OECD subject areas

    if hasattr(metadata, "subjects"):
        for subject in metadata.subjects:
            subject_name = subject.get("subject", "")
            slug = string_to_slug(subject_name)
            if slug in COMMUNITY_TRANSLATIONS:
                slug = COMMUNITY_TRANSLATIONS[slug]
            community_id = search_by_slug(slug, "topic", host, token)
            if community_id and community_id not in community_ids:
                record = add_record_to_community(record, host, token, community_id)

    # Add record to communities defined as IsPartOf relation in InvenioRDM RelatedIdentifiers
    if hasattr(metadata, "related_identifiers") and metadata.related_identifiers:
        for identifier in metadata.related_identifiers:
            if dig(identifier, "relation_type.id") == "ispartof" and identifier.get(
                "identifier", ""
            ).startswith(f"https://{host}/api/communities/"):
                slug = identifier.get("identifier").split("/")[5]
                community_id = search_by_slug(slug, "topic", host, token)
                if community_id and community_id not in community_ids:
                    record = add_record_to_community(record, host, token, community_id)

    return record


def update_external_services(
    metadata: Commonmeta, host: str, token: str, record: dict, **kwargs
) -> dict:
    """Update external services with changes in InvenioRDM"""

    # optionally update rogue-scholar legacy record
    if host == "rogue-scholar.org" and kwargs.get("legacy_key", None) is not None:
        record = update_legacy_record(
            record, legacy_key=kwargs.get("legacy_key"), field="rid"
        )

    return record


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
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits.0.id")
        return None
    except requests.exceptions.RequestException as e:
        log.error(f"Error searching for DOI {doi}: {str(e)}", exc_info=True)
        return None


def create_draft_record(record, host, token, output):
    """Create a new draft record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            f"https://{host}/api/records", headers=headers, json=output
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        if response.status_code != 201:
            log.error(
                f"Failed to create draft record: {response.status_code} - {response.json()}"
            )
            record["status"] = "failed_create_draft"
            return record
        data = response.json()
        record["id"] = data.get("id", None)
        record["created"] = data.get("created", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "draft"
        return record
    except requests.exceptions.RequestException as e:
        log.error(f"Error creating draft record: {str(e)}", exc_info=True)
        record["status"] = "error_draft"
        return record


def reserve_doi(record, host, token) -> dict:
    """Reserve a DOI for a draft record."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            f"https://{host}/api/records/{record.get('id')}/draft/pids/doi",
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        record["doi"] = data.get("doi", None)
        record["status"] = "doi_reserved"
        return record
    except requests.exceptions.RequestException as e:
        log.error(
            f"Error reserving DOI for record {record['id']}: {str(e)}", exc_info=True
        )
        record["status"] = "error_reserve_doi"
        return record


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
        print("Edited published record:", dig(data, "parent.pids.doi.identifier"))
        record["updated"] = data.get("updated", None)
        record["status"] = "edited"
        return record
    except requests.exceptions.RequestException as e:
        log.error(
            f"Error creating draft from published record: {str(e)}", exc_info=True
        )
        record["status"] = "error_edit_published_record"
        return record


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
        print("Update draft record:", dig(data, "parent.pids.doi.identifier"))
        record["updated"] = data.get("updated", None)
        record["status"] = "updated"
        return record
    except requests.exceptions.RequestException as e:
        log.error(f"Error updating draft record: {str(e)}", exc_info=True)
        record["status"] = "error_update_draft_record"
        return record


def publish_draft_record(record, host, token):
    """Publish a draft record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        if not record.get("id", None):
            raise InvenioRDMError("Missing record id")

        response = requests.post(
            f"https://{host}/api/records/{record['id']}/draft/actions/publish",
            headers=headers,
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        if response.status_code != 202:
            log.error(
                f"Failed to publish draft record: {response.status_code} - {response.json()}"
            )
            record["status"] = "error_publish_draft_record"
            return record
        data = response.json()
        record["created"] = data.get("created", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "published"
        return record
    except requests.exceptions.RequestException as e:
        log.error(f"Error publishing draft record: {str(e)}", exc_info=True)
        record["status"] = "error_publish_draft_record"
        return record


def get_record_communities(record, host, token):
    """Get record communities by id"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(
            f"https://{host}/api/records/{record['id']}/communities",
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits")
        return None
    except requests.exceptions.RequestException as e:
        log.error(f"Error getting communities: {str(e)}", exc_info=True)
        return None


def add_record_to_community(record, host, token, community_id):
    """Add a record to a community"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    json = {"communities": [{"id": community_id}]}
    try:
        response = requests.post(
            f"https://{host}/api/records/{record['id']}/communities",
            headers=headers,
            json=json,
        )
        response.raise_for_status()
        return record
    except requests.exceptions.RequestException as e:
        log.error(f"Error adding record to community: {str(e)}", exc_info=True)
        return record


def update_legacy_record(record, legacy_key: str, field: str = None) -> dict:
    """Update corresponding record in Rogue Scholar legacy database."""

    legacy_host = "bosczcmeodcrajtcaddf.supabase.co"
    try:
        if not legacy_key:
            raise ValueError("no legacy key provided")
        if not record.get("uuid", None):
            raise ValueError("no UUID provided")

        now = f"{int(time())}"
        if field == "rid" and record.get("id", None) is not None:
            output = {
                "rid": record.get("id"),
                "doi": record.get("doi", None),
                "indexed_at": now,
                "indexed": "true",
                "archived": "true",
                "registered": "false",
            }
        elif record.get("doi", None) is not None:
            output = {
                "registered": "true",
            }
            # output = {
            #     "doi": record.get("doi"),
            #     "indexed_at": now,
            #     "indexed": "true",
            #     "archived": "true",
            #     "registered": "false",
            # }
        else:
            print(f"nothing to update for id {record.get('uuid')}")
            return record  # nothing to update

        request_url = f"https://{legacy_host}/rest/v1/posts?id=eq.{record['uuid']}"
        headers = {
            "Content-Type": "application/json",
            "apikey": legacy_key,
            "Authorization": f"Bearer {legacy_key}",
            "Prefer": "return=minimal",
        }
        response = requests.patch(request_url, json=output, headers=headers, timeout=30)
        if response.status_code != 204:
            return Exception(f"Unexpected status code: {response.status_code}")

        record["status"] = "updated_legacy"
        return record

    except requests.exceptions.RequestException as e:
        log.error(f"Error updating legacy record: {str(e)}", exc_info=True)
        record["status"] = "error_update_legacy_record"
        return record


def search_by_slug(slug: str, type: str, host: str, token: str) -> Optional[str]:
    """Search for a community by slug in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = [("q", f"slug:{slug}"), ("type", type), ("type", "subject"), ("size", 1)]
    try:
        response = requests.get(
            f"https://{host}/api/communities", headers=headers, params=params
        )
        response.raise_for_status()
        data = response.json()
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits.0.id")
        return None
    except requests.exceptions.RequestException as e:
        log.error(f"Error searching for community: {str(e)}", exc_info=True)
        return None


class InvenioRDMError(Exception):
    """Custom exception for InvenioRDM API errors"""
