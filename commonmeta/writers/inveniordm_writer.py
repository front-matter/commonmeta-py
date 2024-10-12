"""InvenioRDM writer for commonmeta-py"""

import orjson as json
from typing import Optional

from ..base_utils import compact, wrap, parse_attributes
from ..date_utils import get_iso8601_date
from ..doi_utils import doi_from_url
from ..constants import CM_TO_INVENIORDM_TRANSLATIONS, INVENIORDM_IDENTIFIER_TYPES
from ..utils import get_language, validate_orcid, id_from_url


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
        if i.get("id", None) != metadata.id
    ]
    container = metadata.container if metadata.container else {}
    journal = (
        container.get("title", None)
        if _type not in ["inbook", "inproceedings"]
        and container.get("type") in ["Journal", "Periodical"]
        else None
    )
    issn = (
        container.get("identifier", None)
        if container.get("identifierType", None) == "ISSN"
        else None
    )

    subjects = [to_inveniordm_subject(i) for i in wrap(metadata.subjects)]
    data = compact(
        {
            "pids": {
                "doi": {
                    "identifier": doi_from_url(metadata.id),
                    "provider": "external",
                },
            },
            "access": {"record": "public", "files": "public"},
            "files": {"enabled": True},
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
                    "dates": [
                        {
                            "date": metadata.date.get("updated"),
                            "type": {"id": "updated"},
                        }
                    ],
                    "subjects": subjects,
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
                    "version": metadata.version,
                }
            ),
            "custom_fields": {
                "journal:journal": compact({"title": journal, "issn": issn}),
            },
        }
    )
    return json.dumps(data)


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


def to_inveniordm_subject(subject: dict) -> dict:
    """Convert subjects to inveniordm subjects"""
    return compact(
        {
            "id": subject.get("id", None),
            "subject": subject.get("subject", None),
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
