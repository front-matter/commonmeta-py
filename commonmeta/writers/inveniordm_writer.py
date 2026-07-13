"""InvenioRDM writer for commonmeta-py"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import orjson as json
from requests.exceptions import RequestException

from commonmeta.readers.inveniordm_reader import search_by_doi, search_by_guid

from ..api_utils import http
from ..base_utils import (
    compact,
    dig,
    first,
    presence,
    scrub,
    unique,
    wrap,
)
from ..constants import (
    CM_TO_INVENIORDM_CONTRIBUTOR_ROLES,
    CM_TO_INVENIORDM_TRANSLATIONS,
    COMMUNITY_TRANSLATIONS,
    INVENIORDM_IDENTIFIER_TYPES,
    OPENALEX_TOPIC_SUBFIELD_MAPPINGS,
)
from ..date_utils import get_iso8601_date
from ..doi_utils import doi_from_url, is_rogue_scholar_doi, normalize_doi
from ..utils import (
    FOS_MAPPINGS,
    OPENALEX_TO_FOS_MAPPINGS,
    get_language,
    id_from_url,
    normalize_url,
    pages_as_string,
    string_to_slug,
    validate_orcid,
    validate_ror,
)

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList

log = logging.getLogger(__name__)


def write_inveniordm(metadata: Metadata) -> dict:
    """Write inveniordm"""
    if metadata is None or metadata.write_errors is not None:
        return {}
    if is_rogue_scholar_doi(metadata.id, ra="crossref"):
        pids = {
            "doi": {
                "identifier": doi_from_url(metadata.id),
                "provider": "crossref",
            },
        }
    # elif is_rogue_scholar_doi(metadata.id, ra="datacite"):
    #     # DataCite DOIs should not be provided in the InvenioRDM writer
    #     pids = None
    else:
        pids = {
            "doi": {"identifier": doi_from_url(metadata.id), "provider": "external"},
        }
    _type = CM_TO_INVENIORDM_TRANSLATIONS.get(metadata.type, "Other")
    creators = [
        to_inveniordm_creator(i)
        for i in wrap(metadata.contributors)
        if "Author" in wrap(i.get("roles", None))
    ]
    contributors = scrub(
        [
            to_inveniordm_contributor(i)
            for i in wrap(metadata.contributors)
            if "Author" not in wrap(i.get("roles", None))
        ]
    )
    identifiers = [
        {
            "identifier": i.get("identifier", None),
            "scheme": INVENIORDM_IDENTIFIER_TYPES.get(
                i.get("identifier_type", None), "other"
            ),
        }
        for i in wrap(metadata.identifiers)
        if i.get("identifier_type", None) != "DOI"
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
    funding = unique(
        [
            to_inveniordm_funding(i)
            for i in wrap(metadata.funding_references)
            if i.get("funder_name", None)
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
        if container.get("identifier_type", None) == "ISSN"
        else None
    )
    volume = container.get("volume", None)
    issue = container.get("issue", None)
    pages = pages_as_string(container)

    date_fields = compact(
        {
            "published": metadata.date_published,
            "updated": metadata.date_updated,
            **(metadata.dates or {}),
        }
    )
    dates = []
    for d, v in date_fields.items():
        t = d.lower()
        if t == "published":
            t = "issued"
        elif t == "accessed":
            t = "other"
        dates.append({"date": v, "type": {"id": t}})

    # Flatten subjects list since to_inveniordm_subject can return multiple subjects
    # Deduplicate by ID to handle multiple subfields mapping to same FOS
    all_subjects = [
        s for i in wrap(metadata.subjects) for s in (to_inveniordm_subject(i) or [])
    ]
    seen_ids = set()
    subjects = []
    for subject in all_subjects:
        subject_id = subject.get("id")
        if subject_id is None or subject_id not in seen_ids:
            subjects.append(subject)
            if subject_id is not None:
                seen_ids.add(subject_id)

    # files = to_files(metadata)

    return compact(
        {
            "pids": pids,
            "access": {"record": "public", "files": "public"},
            "files": {"enabled": False},
            "metadata": compact(
                {
                    "resource_type": {"id": _type},
                    "creators": creators,
                    "contributors": presence(contributors),
                    "title": metadata.title,
                    "publisher": (
                        metadata.publisher.get("name", None)
                        if metadata.publisher
                        else None
                    ),
                    "publication_date": (
                        get_iso8601_date(metadata.date_published)
                        if metadata.date_published
                        else None
                    ),
                    "dates": presence(dates),
                    "subjects": presence(subjects),
                    "description": metadata.description,
                    "rights": (
                        [{"id": metadata.license.get("id").lower()}]
                        if metadata.license.get("id", None)
                        else None
                    ),
                    "languages": (
                        [{"id": get_language(metadata.language, format="alpha_3")}]
                        if metadata.language
                        else None
                    ),
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
                    "feed:generator": container.get("platform", None),
                }
            ),
        }
    )


def to_inveniordm_identifiers(_id: str | None) -> list | None:
    """Format a v1.0 person.id (ORCID) as InvenioRDM identifiers"""
    identifier = validate_orcid(_id)
    if identifier:
        return [
            {
                "identifier": identifier,
                "scheme": "orcid",
            }
        ]
    return None


def to_inveniordm_creator(creator: dict) -> dict:
    """Convert a v1.0 {type, person|organization, roles} contributor to an
    InvenioRDM creator"""
    _type = creator.get("type", None)
    organization = creator.get("organization", None)
    person = creator.get("person", None) or {}
    given_name = person.get("given_name", None)
    family_name = person.get("family_name", None)
    if family_name:
        name = ", ".join([family_name, given_name or ""])
    elif organization:
        name = organization.get("name", None)
    else:
        name = None
    _id = organization.get("id", None) if organization else person.get("id", None)

    return compact(
        {
            "person_or_org": compact(
                {
                    "name": name,
                    "given_name": given_name,
                    "family_name": family_name,
                    "type": _type.lower() + "al" if _type else None,
                    "identifiers": to_inveniordm_identifiers(_id),
                }
            ),
            "affiliations": to_inveniordm_affiliations(person),
        }
    )


def to_inveniordm_contributor(contributor: dict) -> dict:
    """Convert a v1.0 {type, person|organization, roles} contributor to an
    InvenioRDM contributor"""
    _type = contributor.get("type", None)
    organization = contributor.get("organization", None)
    person = contributor.get("person", None) or {}
    given_name = person.get("given_name", None)
    family_name = person.get("family_name", None)
    if family_name:
        name = ", ".join([family_name, given_name or ""])
    elif organization:
        name = organization.get("name", None)
    else:
        name = None
    _id = organization.get("id", None) if organization else person.get("id", None)

    role = first(wrap(contributor.get("roles", None)))
    _role = (
        {"id": CM_TO_INVENIORDM_CONTRIBUTOR_ROLES.get(role)}
        if CM_TO_INVENIORDM_CONTRIBUTOR_ROLES.get(role)
        else None
    )
    if _role is None:
        return None
    return compact(
        {
            "person_or_org": compact(
                {
                    "name": name,
                    "given_name": given_name,
                    "family_name": family_name,
                    "type": _type.lower() + "al" if _type else None,
                    "identifiers": to_inveniordm_identifiers(_id),
                }
            ),
            "role": _role,
            "affiliations": to_inveniordm_affiliations(person),
        }
    )


def to_inveniordm_subject(sub: dict) -> list | None:
    """Convert subject to inveniordm subject. Adds scheme based on id pattern.
    For subfields, also returns a FOS subject if a mapping exists."""
    if sub.get("subject", None) is None:
        return None

    if sub.get("id", "").startswith("https://openalex.org/domains/"):
        scheme = "Domains"
    elif sub.get("id", "").startswith("https://openalex.org/fields/"):
        scheme = "Fields"
    elif sub.get("id", "").startswith("https://openalex.org/subfields/"):
        scheme = "Subfields"
    elif sub.get("id", "").startswith("https://openalex.org/T"):
        scheme = "Topics"
    elif sub.get("id", "").startswith("http://www.oecd.org/science/inno/38235147.pdf"):
        scheme = "FOS"
    else:
        scheme = None

    result = [
        compact(
            {
                "id": sub.get("id", None),
                "subject": sub.get("subject"),
                "scheme": scheme,
            }
        )
    ]

    # If this is a subfield, also add a FOS subject if mapping exists
    if sub.get("id", "").startswith("https://openalex.org/subfields/"):
        # Extract subfield ID (last part of URL)
        subfield_id = sub.get("id", "").split("/")[-1]
        fos_name = OPENALEX_TO_FOS_MAPPINGS.get(subfield_id, None)
        if fos_name:
            fos_id = FOS_MAPPINGS.get(fos_name, None)
            existing_ids = {
                s.get("id")
                for s in result
                if isinstance(s, dict) and s.get("id") is not None
            }
            if fos_id and fos_id not in existing_ids:
                result.append(
                    compact(
                        {
                            "id": fos_id,
                            "subject": f"FOS: {fos_name}",
                            "scheme": "FOS",
                        }
                    )
                )

    return result


def to_inveniordm_affiliations(person: dict) -> list | None:
    """Convert a v1.0 person's affiliations to inveniordm affiliations."""

    def format_affiliation(affiliation):
        # affiliation identifiers are ROR-only in v1.0; emit the InvenioRDM
        # affiliation id only for ROR-typed identifiers.
        ror = (
            affiliation.get("identifier", None)
            if affiliation.get("identifier_type", None) == "ROR"
            else None
        )
        return compact(
            {
                "id": id_from_url(ror),
                "name": affiliation.get("name", None),
            }
        )

    return scrub(
        [format_affiliation(i) for i in wrap(person.get("affiliations", None))]
    )


def to_inveniordm_related_identifier(relation: dict) -> dict | None:
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
    if relation.get("type", None) == "HasReview":
        relation_type = "isreviewedby"
    elif relation.get("type", None) == "IsPreprintOf":
        relation_type = "ispreviousversionof"
    elif relation.get("type", None) is not None:
        relation_type = str(relation.get("type")).lower()
    else:
        return None

    return compact(
        {
            "identifier": identifier,
            "scheme": scheme,
            "relation_type": {"id": relation_type},
        }
    )


def to_inveniordm_reference(reference: dict) -> dict | None:
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

    # the commonmeta `reference` field holds the formatted reference string
    # (falling back to the legacy unstructured/title fields).
    unstructured = reference.get("reference", None) or reference.get(
        "unstructured", None
    )
    if unstructured:
        if reference.get("id", None):
            # remove duplicate ID from unstructured reference
            unstructured = unstructured.replace(reference.get("id"), "")
        # remove optional trailing whitespace
        unstructured = unstructured.rstrip()
    else:
        title = reference.get("title", None)
        unstructured = str(title) if title else "Unknown title"
        if reference.get("publication_year", None):
            unstructured += f" ({reference.get('publication_year')})."

    return compact(
        {
            "reference": unstructured,
            "scheme": scheme,
            "identifier": identifier,
        }
    )


def to_inveniordm_funding(funding: dict) -> dict | None:
    """Convert a v1.0 flat funding reference (ROR-only funder_id) to
    inveniordm funding"""
    funder_identifier = validate_ror(funding.get("funder_id", None))
    award_number = funding.get("award_number", None)
    award_title = funding.get("award_title", None)
    if award_title:
        award_title = {"en": award_title}
    if funding.get("award_id", None):
        award_identifier = funding.get("award_id", None)
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
                        "name": funding.get("funder_name"),
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
                    "name": funding.get("funder_name"),
                    "id": funder_identifier,
                }
            ),
        }
    )


def to_files(metadata: Metadata) -> list:
    """Convert metadata files to inveniordm files"""

    def format_file(file):
        return compact(
            {
                "key": file.get("key", None),
                "bucket": file.get("bucket", None),
                "size": file.get("size", None),
                "checksum": file.get("checksum", None),
                "checksum_algorithm": file.get("checksumAlgorithm", None),
                "filename": file.get("filename", None),
                "description": file.get("description", None),
            }
        )

    return [format_file(i) for i in wrap(metadata.files)]


def write_inveniordm_list(metalist: MetadataList) -> list | None:
    """Write InvenioRDM list"""

    if metalist is None:
        return None

    def write_item(item) -> dict | None:
        """write inveniordm item for inveniordm list"""

        return write_inveniordm(item)

    return [write_item(item) for item in metalist.items]


def push_inveniordm(metadata: Metadata, host: str, token: str, **kwargs) -> dict:
    """Push record to InvenioRDM"""

    try:
        doi = normalize_doi(metadata.id)
        if doi is None:
            raise ValueError("no doi provided")

        record = {
            "doi": doi,
            "previous_doi": kwargs.get("previous_doi", None),
        }

        # extract optional information needed
        # community_id is the id of the primary community of the record,
        # in the case of Rogue Scholar the blog community

        if metadata.relations:
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
        return record
    except ValueError as ve:
        log.error(
            f"Value error in push_inveniordm: {str(ve)}",
            exc_info=True,
            extra={"host": host, "record_id": metadata.id},
        )
        record = {
            "doi": doi if "doi" in locals() else None,
            "status": "error",
        }
    except Exception as e:
        log.error(
            f"Unexpected error in push_inveniordm: {str(e)}",
            exc_info=True,
            extra={"host": host, "record_id": record.get("id")},
        )
        record["status"] = "error"

    return record


def push_inveniordm_list(
    metalist: MetadataList, host: str, token: str, **kwargs
) -> bytes | None:
    """Push inveniordm list to InvenioRDM, returns list of push results."""

    if metalist is None:
        return None
    items = [push_inveniordm(item, host, token, **kwargs) for item in metalist.items]
    return json.dumps(items, option=json.OPT_INDENT_2)


def upsert_record(
    metadata: Metadata,
    host: str,
    token: str,
    record: dict,
) -> dict:
    """Upsert InvenioRDM record, based on DOI"""

    output = write_inveniordm(metadata)

    # Check if record already exists in InvenioRDM
    record["id"] = search_by_doi(doi_from_url(record.get("doi")), host, token)

    # Also check by record guid
    if record["id"] is None:
        guid = next(
            (
                i.get("identifier")
                for i in wrap(metadata.identifiers)
                if i.get("identifier_type") == "GUID" and i.get("identifier")
            ),
            None,
        )
        if guid is not None:
            record["id"] = search_by_guid(guid, host, token)

    if record["previous_doi"] is not None:
        record["previous_id"] = search_by_doi(
            doi_from_url(record["previous_doi"]), host, token
        )

    if record.get("previous_id", None) is not None:
        # Create a new version from the previous record
        record["id"] = record["previous_id"]
        record = create_new_version(record, host, token)

        # Update new version
        record = update_draft_record(record, host, token, output)
    elif record.get("id", None) is not None:
        # Create draft record from published record
        record = edit_published_record(record, host, token)

        # Update draft record with new metadata (except PIDs which should not be updated)
        update_output = {k: v for k, v in output.items() if k != "pids"}
        record = update_draft_record(record, host, token, update_output)
    else:
        # Create draft record for DOI that is external or needs to be registered
        # (currently only supported for Crossref PID provider)
        record = create_draft_record(record, host, token, output)

    # Publish draft record
    record = publish_draft_record(record, host, token)

    return record


def add_record_to_communities(
    metadata: Metadata, host: str, token: str, record: dict
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
    # Subject area communities should exist for all OpenAlex subfields

    if metadata.subjects:
        for subject in metadata.subjects:
            # OpenAlex subfield
            if subject.get("id", "").startswith("https://openalex.org/subfields/"):
                slug = subject.get("id").split("/")[-1]
                community_id = search_by_slug(slug, "topic", host, token)
                if community_id and community_id not in community_ids:
                    record = add_record_to_community(record, host, token, community_id)
            # OpenAlex subfield of topic
            if subject.get("id", "").startswith("https://openalex.org/T"):
                topic = subject.get("id").split("/")[-1]
                slug = OPENALEX_TOPIC_SUBFIELD_MAPPINGS.get(topic[1:], None)
                if slug is not None:
                    community_id = search_by_slug(slug, "topic", host, token)
                    if community_id and community_id not in community_ids:
                        record = add_record_to_community(
                            record, host, token, community_id
                        )
            subject_name = subject.get("subject", "")
            slug = string_to_slug(subject_name)
            if slug in COMMUNITY_TRANSLATIONS:
                slug = COMMUNITY_TRANSLATIONS[slug]
            community_id = search_by_slug(slug, "topic", host, token)
            if community_id and community_id not in community_ids:
                record = add_record_to_community(record, host, token, community_id)

    # Add record to communities defined as IsPartOf relation in InvenioRDM RelatedIdentifiers
    if metadata.relations:
        for relation in metadata.relations:
            if relation.get("type", None) == "IsPartOf" and relation.get(
                "id", ""
            ).startswith(f"https://{host}/api/communities/"):
                slug = relation.get("id").split("/")[5]
                community_id = search_by_slug(slug, "topic", host, token)
                if community_id and community_id not in community_ids:
                    record = add_record_to_community(record, host, token, community_id)

    return record


def update_external_services(
    metadata: Metadata, host: str, token: str, record: dict, **kwargs
) -> dict:
    """Update external services with changes in InvenioRDM"""

    return record


def create_draft_record(record: dict, host: str, token: str, output: dict) -> dict:
    """Create a new draft record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.post(
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
    except RequestException as e:
        log.error(f"Error creating draft record: {str(e)}", exc_info=True)
        record["status"] = "error_draft"
        return record


def reserve_doi(record: dict, host: str, token: str) -> dict:
    """Reserve a DOI for a draft record."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.post(
            f"https://{host}/api/records/{record.get('id')}/draft/pids/doi",
            headers=headers,
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        response.raise_for_status()
        data = response.json()
        record["doi"] = data.get("doi", None)
        record["status"] = "doi_reserved"
        return record
    except RequestException as e:
        log.error(
            f"Error reserving DOI for record {record['id']}: {str(e)}", exc_info=True
        )
        record["status"] = "error_reserve_doi"
        return record


def edit_published_record(record: dict, host: str, token: str) -> dict:
    """Create a draft from a published record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.post(
            f"https://{host}/api/records/{record['id']}/draft", headers=headers
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        response.raise_for_status()
        data = response.json()
        record["updated"] = data.get("updated", None)
        record["status"] = "edited"
        return record
    except RequestException as e:
        log.error(
            f"Error creating draft from published record: {str(e)}", exc_info=True
        )
        record["status"] = "error_edit_published_record"
        return record


def create_new_version(record: dict, host: str, token: str) -> dict:
    """Create a new version of a published record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.post(
            f"https://{host}/api/records/{record['id']}/versions", headers=headers
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        response.raise_for_status()
        data = response.json()
        record["id"] = data.get("id", None)
        record["updated"] = data.get("updated", None)
        record["status"] = "new_version"
        return record
    except RequestException as e:
        log.error(
            f"Error creating new version from published record: {str(e)}", exc_info=True
        )
        record["status"] = "error_create_new_version"
        return record


def update_draft_record(
    record: dict, host: str, token: str, inveniordm_data: dict
) -> dict:
    """Update a draft record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.put(
            f"https://{host}/api/records/{record['id']}/draft",
            headers=headers,
            json=inveniordm_data,
        )
        if response.status_code == 429:
            record["status"] = "failed_rate_limited"
            return record
        response.raise_for_status()
        data = response.json()
        record["updated"] = data.get("updated", None)
        record["status"] = "updated"
        return record
    except RequestException as e:
        log.error(f"Error updating draft record: {str(e)}", exc_info=True)
        record["status"] = "error_update_draft_record"
        return record


def publish_draft_record(record: dict, host: str, token: str) -> dict:
    """Publish a draft record in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        if not record.get("id", None):
            raise InvenioRDMError("Missing record id")

        response = http.post(
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
    except RequestException as e:
        log.error(f"Error publishing draft record: {str(e)}", exc_info=True)
        record["status"] = "error_publish_draft_record"
        return record


def get_record_communities(record: dict, host: str, token: str) -> list | None:
    """Get record communities by id"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = http.get(
            f"https://{host}/api/records/{record['id']}/communities",
            headers=headers,
        )
        if response.status_code == 429:
            log.warning("Rate limit exceeded while getting communities")
            return None
        response.raise_for_status()
        data = response.json()
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits")
        return None
    except RequestException as e:
        log.error(f"Error getting communities: {str(e)}", exc_info=True)
        return None


def add_record_to_community(
    record: dict, host: str, token: str, community_id: str
) -> dict:
    """Add a record to a community"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    json = {"communities": [{"id": community_id}]}
    try:
        response = http.post(
            f"https://{host}/api/records/{record['id']}/communities",
            headers=headers,
            json=json,
        )
        if response.status_code == 400:
            # InvenioRDM returns 400 when the community has no logo set or the
            # record is already linked to the community.
            data = response.json()
            log.warning(
                "Failed to add record to community: %s",
                data.get("errors", response.text),
                extra={"record_id": record["id"], "community_id": community_id},
            )
        elif response.status_code == 429:
            log.warning(
                "Rate limit exceeded while adding record to community",
                extra={"record_id": record["id"], "community_id": community_id},
            )
        else:
            response.raise_for_status()
        return record
    except RequestException as e:
        log.error("Error adding record to community: %s", str(e), exc_info=True)
        return record


def search_by_slug(slug: str, type: str, host: str, token: str) -> str | None:
    """Search for a community by slug in InvenioRDM"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = [("q", f"slug:{slug}"), ("type", type), ("type", "subject"), ("size", 1)]
    try:
        response = http.get(
            f"https://{host}/api/communities", headers=headers, params=params
        )
        if response.status_code == 429:
            log.warning("Rate limit exceeded while searching for community by slug")
            return None
        response.raise_for_status()
        data = response.json()
        if dig(data, "hits.total", 0) > 0:
            return dig(data, "hits.hits.0.id")
        return None
    except RequestException as e:
        log.error(f"Error searching for community: {str(e)}", exc_info=True)
        return None


class InvenioRDMError(Exception):
    """Custom exception for InvenioRDM API errors"""
