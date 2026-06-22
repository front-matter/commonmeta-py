"""DataCite writer for commonmeta-py"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base_utils import compact, first, scrub, wrap
from ..constants import (
    CM_TO_BIB_TRANSLATIONS,
    CM_TO_CR_TRANSLATIONS,
    CM_TO_CSL_TRANSLATIONS,
    CM_TO_DC_CONTRIBUTOR_ROLES,
    CM_TO_DC_TRANSLATIONS,
    CM_TO_RIS_TRANSLATIONS,
    CM_TO_SO_TRANSLATIONS,
)
from ..doi_utils import doi_from_url, normalize_doi
from ..v1_compat import (
    v1_to_date,
    v1_to_descriptions,
    v1_to_geo_locations,
    v1_to_titles,
)

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


def write_datacite(metadata: Metadata) -> dict | None:
    """Write datacite. Make sure JSON Schema validates before writing"""
    if metadata.write_errors is not None:
        return {"errors": metadata.write_errors}

    alternate_identifiers = [
        {
            "alternateIdentifier": i.get("identifier", None),
            "alternateIdentifierType": i.get("identifier_type", None),
        }
        for i in wrap(metadata.identifiers)
        if i.get("id", None) != metadata.id
    ]

    creators = [
        to_datacite_creator(i)
        for i in wrap(metadata.contributors)
        if "Author" in wrap(i.get("roles"))
    ]
    contributors = scrub(
        [
            to_datacite_contributor(i)
            for i in wrap(metadata.contributors)
            if "Author" not in wrap(i.get("roles"))
        ]
    )
    related_identifiers = [
        to_datacite_related_identifier(i)
        for i in wrap(metadata.references)
        if i.get("id", None)
    ]

    resource__typegeneral = CM_TO_DC_TRANSLATIONS.get(metadata.type, "Other")
    resource_type = CM_TO_CR_TRANSLATIONS.get(metadata.type, "Other")
    if metadata.type == "BlogPost":
        resource_type = "BlogPost"
    if resource__typegeneral == resource_type or resource__typegeneral in [
        "Dataset",
        "JournalArticle",
        "Other",
        "Preprint",
        "Software",
    ]:
        resource_type = None
    types = compact(
        {
            "resourceTypeGeneral": resource__typegeneral,
            "resourceType": resource_type,
            "schemaOrg": CM_TO_SO_TRANSLATIONS.get(metadata.type, "CreativeWork"),
            "citeproc": CM_TO_CSL_TRANSLATIONS.get(metadata.type, "article"),
            "bibtex": CM_TO_BIB_TRANSLATIONS.get(metadata.type, "misc"),
            "ris": CM_TO_RIS_TRANSLATIONS.get(metadata.type, "GEN"),
        }
    )
    publication_year = (
        metadata.date_published[:4] if metadata.date_published else None
    )

    def to_datacite_date(date_item: tuple[str, str]) -> dict:
        """Convert date tuple (key, value) to datacite date"""
        k, v = date_item
        if k == "published":
            k = "issued"
        return {
            "date": v,
            "dateType": k.title(),
        }

    date = v1_to_date(metadata.date_published, metadata.date_updated, metadata.dates)
    dates = [to_datacite_date(item) for item in (date or {}).items()]

    license_ = (
        [
            compact(
                {
                    "rightsIdentifier": metadata.license.get("id").lower()
                    if metadata.license.get("id", None)
                    else None,
                    "rightsIdentifierScheme": "SPDX",
                    "rightsUri": metadata.license.get("url", None),
                    "schemeUri": "https://spdx.org/licenses/",
                }
            )
        ]
        if metadata.license
        else None
    )

    subjects = [
        compact(
            {
                "valueURI": i.get("id", None),
                "subject": i.get("subject", None),
                "lang": i.get("language", None),
            }
        )
        for i in wrap(metadata.subjects)
    ]

    descriptions = [
        compact(
            {
                "description": i.get("description", None),
                "descriptionType": i.get("type", None) or "Other",
                "lang": i.get("language", None),
            }
        )
        for i in wrap(
            v1_to_descriptions(metadata.description, metadata.additional_descriptions)
        )
    ]

    titles = to_datacite_titles(
        wrap(v1_to_titles(metadata.title, metadata.additional_titles))
    )

    return compact(
        {
            "id": metadata.id,
            "doi": doi_from_url(metadata.id),
            "url": metadata.url,
            "creators": creators,
            "titles": titles,
            "publisher": metadata.publisher,
            "publicationYear": publication_year,
            "subjects": subjects,
            "contributors": contributors,
            "dates": dates,
            "language": metadata.language,
            "types": types,
            "alternateIdentifiers": alternate_identifiers,
            "relatedIdentifiers": related_identifiers,
            "version": metadata.version,
            "rightsList": license_,
            "descriptions": descriptions,
            "geoLocations": v1_to_geo_locations(metadata.geo_locations),
            "fundingReferences": [
                to_datacite_funding_reference(f)
                for f in wrap(metadata.funding_references)
            ],
            "schemaVersion": "http://datacite.org/schema/kernel-4",
        }
    )


def to_datacite_name_identifiers(_id: str | None) -> list | None:
    """Format a v1.0 person.id (ORCID) as DataCite nameIdentifiers"""
    if not _id:
        return None
    return [
        {
            "nameIdentifier": i,
            "nameIdentifierScheme": "ORCID",
            "schemeUri": "https://orcid.org",
        }
        for i in wrap(_id)
    ]


def to_datacite_creator(creator: dict) -> dict:
    """Convert a v1.0 {type, person|organization, roles} contributor to a
    DataCite creator"""
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
            "name": name,
            "givenName": given_name,
            "familyName": family_name,
            "nameType": _type + "al" if _type else None,
            "nameIdentifiers": to_datacite_name_identifiers(_id),
            "affiliation": person.get("affiliations", None),
        }
    )


def to_datacite_contributor(contributor: dict) -> dict:
    """Convert a v1.0 {type, person|organization, roles} contributor to a
    DataCite contributor"""
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
    _role = CM_TO_DC_CONTRIBUTOR_ROLES.get(role, None)
    if _role is None:
        return None
    return compact(
        {
            "name": name,
            "givenName": given_name,
            "familyName": family_name,
            "nameType": _type + "al" if _type else None,
            "nameIdentifiers": to_datacite_name_identifiers(_id),
            "affiliation": person.get("affiliations", None),
            "contributorType": _role,
        }
    )


def to_datacite_funding_reference(funding: dict) -> dict:
    """Convert a v1.0 flat funding reference to a DataCite fundingReference"""
    funder_id = funding.get("funder_id", None)
    return compact(
        {
            "funderName": funding.get("funder_name", None),
            "funderIdentifier": funder_id,
            "funderIdentifierType": "ROR" if funder_id else None,
            "awardUri": funding.get("award_id", None),
            "awardTitle": funding.get("award_title", None),
            "awardNumber": funding.get("award_number", None),
        }
    )


def to_datacite_titles(titles: list) -> list:
    """Convert titles to datacite titles"""
    return [
        compact(
            {
                "title": title.get("title", None),
                "titleType": title.get("type", None),
                "lang": title.get("language", None),
            }
        )
        for title in titles
    ]


def to_datacite_related_identifier(reference: dict) -> dict:
    """Convert reference to datacite related_identifier"""
    _id = normalize_doi(reference.get("id", None))
    url = reference.get("id", None)
    return compact(
        {
            "relatedIdentifier": _id if _id else url,
            "relatedIdentifierType": "DOI" if _id else "URL",
            "relationType": "References",
        }
    )


def write_datacite_list(metalist: MetadataList | None) -> list | None:
    """Write DataCite list"""
    if metalist is None:
        return None
    return [write_datacite(item) for item in metalist.items]
