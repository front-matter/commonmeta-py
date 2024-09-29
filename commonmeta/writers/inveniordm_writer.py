"""InvenioRDM writer for commonmeta-py"""

import orjson as json

from ..utils import to_inveniordm
from ..base_utils import compact, wrap, presence, parse_attributes
from ..doi_utils import doi_from_url, validate_suffix
from ..constants import CM_TO_INVENIORDM_TRANSLATIONS
from ..utils import pages_as_string, get_language, validate_orcid


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
            "scheme": i.get("identifierType", None),
        }
        for i in wrap(metadata.identifiers)
        if i.get("id", None) != metadata.id
    ]
    publisher = metadata.publisher or {}
    data = compact(
        {
            "metadata": {
                "resource_type": {"id": _type},
                "doi": doi_from_url(metadata.id),
                "creators": creators,
                "title": parse_attributes(metadata.titles, content="title", first=True),
                "publisher": publisher.get("name", None),
                "publication_date": metadata.date.get("published")
                if metadata.date.get("published", None)
                else None,
                "subjects": parse_attributes(
                    wrap(metadata.subjects), content="subject", first=False
                ),
                "contributors": to_inveniordm(wrap(metadata.contributors)),
                "description": parse_attributes(
                    metadata.descriptions, content="description", first=True
                ),
                "license": metadata.license.get("id", None)
                if metadata.license
                else None,
                "languages": [{"id": get_language(metadata.language, format="alpha_3")}]
                if metadata.language
                else None,
                "identifiers": identifiers,
                "version": metadata.version,
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

    return {
        "person_or_org": compact(
            {
                "name": name,
                "given_name": creator.get("givenName", None),
                "family_name": creator.get("familyName", None),
                "type": _type.lower() + "al" if _type else None,
                "identifiers": format_identifier(creator.get("id", None)),
                "affiliation": creator.get("affiliations", None),
            }
        )
    }
