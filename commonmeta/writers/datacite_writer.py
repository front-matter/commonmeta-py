"""DataCite writer for commonmeta-py"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base_utils import compact, dig, first, presence, scrub, wrap
from ..constants import (
    CM_TO_BIB_TRANSLATIONS,
    CM_TO_CR_TRANSLATIONS,
    CM_TO_CSL_TRANSLATIONS,
    CM_TO_DC_CONTRIBUTOR_ROLES,
    CM_TO_DC_TRANSLATIONS,
    CM_TO_RIS_TRANSLATIONS,
    CM_TO_SO_TRANSLATIONS,
)
from ..doi_utils import doi_from_url

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


def _wkt_to_polygon_points(wkt: str | None) -> list | None:
    if not wkt or not wkt.startswith("POLYGON((") or not wkt.endswith("))"):
        return None
    body = wkt[len("POLYGON((") : -2]
    points = []
    for pair in body.split(", "):
        parts = pair.strip().split(" ")
        if len(parts) == 2:
            points.append(
                {"pointLongitude": float(parts[0]), "pointLatitude": float(parts[1])}
            )
    return points or None


def _geo_locations_to_datacite(geo_locations: list | None) -> list | None:
    items = []
    for g in wrap(geo_locations):
        point = compact(
            {
                "pointLongitude": g.get("point_longitude", None),
                "pointLatitude": g.get("point_latitude", None),
            }
        )
        box = compact(
            {
                "westBoundLongitude": g.get("box_west_longitude", None),
                "eastBoundLongitude": g.get("box_east_longitude", None),
                "southBoundLatitude": g.get("box_south_latitude", None),
                "northBoundLatitude": g.get("box_north_latitude", None),
            }
        )
        items.append(
            compact(
                {
                    "geoLocationPlace": g.get("place", None),
                    "geoLocationPoint": presence(point),
                    "geoLocationBox": presence(box),
                    "geoLocationPolygon": _wkt_to_polygon_points(
                        g.get("polygon", None)
                    ),
                }
            )
        )
    return presence(items)


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
    publication_year = None
    if metadata.date_published and metadata.date_published[:4].isdigit():
        publication_year = int(metadata.date_published[:4])

    def to_datacite_date(date_item: tuple[str, str]) -> dict:
        """Convert date tuple (key, value) to datacite date"""
        k, v = date_item
        if k == "published":
            k = "issued"
        return {
            "date": v,
            "dateType": k.title(),
        }

    date_fields = compact(
        {
            "published": metadata.date_published,
            "updated": metadata.date_updated,
            **(metadata.dates or {}),
        }
    )
    dates = [to_datacite_date(item) for item in date_fields.items()]

    license_ = (
        [
            compact(
                {
                    "rightsIdentifier": (
                        metadata.license.get("id").lower()
                        if metadata.license.get("id", None)
                        else None
                    ),
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

    all_descriptions = (
        [{"description": metadata.description, "type": "Abstract"}]
        if metadata.description
        else []
    ) + wrap(metadata.additional_descriptions)
    descriptions = [
        compact(
            {
                "description": i.get("description", None),
                "descriptionType": i.get("type", None) or "Other",
                "lang": i.get("language", None),
            }
        )
        for i in all_descriptions
    ]

    all_titles = ([{"title": metadata.title}] if metadata.title else []) + wrap(
        metadata.additional_titles
    )
    titles = to_datacite_titles(all_titles)

    return compact(
        {
            "id": metadata.id,
            "doi": doi_from_url(metadata.id),
            "url": metadata.url,
            "creators": creators,
            "titles": titles,
            "publisher": metadata.publisher,
            "publicationYear": publication_year,
            "container": to_datacite_container(metadata.container),
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
            "geoLocations": _geo_locations_to_datacite(metadata.geo_locations),
            "fundingReferences": [
                to_datacite_funding_reference(f)
                for f in wrap(metadata.funding_references)
            ],
            "schemaVersion": "http://datacite.org/schema/kernel-4",
        }
    )


def to_datacite_container(container: dict | None) -> dict | None:
    """Convert a v1.0 container to a DataCite container."""
    if not container:
        return None
    cid = dig(container, "identifiers.0.identifier")
    cid_type = dig(container, "identifiers.0.identifier_type")
    return compact(
        {
            "type": container.get("type", None),
            "identifier": cid,
            "identifierType": cid_type,
            "title": container.get("title", None),
            "volume": container.get("volume", None),
            "issue": container.get("issue", None),
            "firstPage": container.get("first_page", None),
            "lastPage": container.get("last_page", None),
        }
    )


def to_datacite_affiliations(affiliations) -> list | None:
    """Convert v1.0 affiliations to DataCite affiliation objects, promoting a
    ROR identifier to affiliationIdentifier/affiliationIdentifierScheme."""
    out = []
    for a in wrap(affiliations):
        if isinstance(a, str):
            if a:
                out.append({"name": a})
            continue
        if not isinstance(a, dict):
            continue
        entry = {"name": a.get("name", None)}
        identifier = a.get("identifier", None)
        if identifier and a.get("identifier_type", None) == "ROR":
            entry["affiliationIdentifier"] = identifier
            entry["affiliationIdentifierScheme"] = "ROR"
            entry["schemeUri"] = "https://ror.org"
        out.append(compact(entry))
    return out or None


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
            "affiliation": to_datacite_affiliations(person.get("affiliations", None)),
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
            "affiliation": to_datacite_affiliations(person.get("affiliations", None)),
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
    doi = doi_from_url(reference.get("id", None))
    url = reference.get("id", None)
    return compact(
        {
            # DataCite uses the bare DOI (not the doi.org URL) here.
            "relatedIdentifier": doi if doi else url,
            "relatedIdentifierType": "DOI" if doi else "URL",
            "relationType": "References",
            "resourceTypeGeneral": CM_TO_DC_TRANSLATIONS.get(
                reference.get("type", None), "Other"
            ),
        }
    )


def write_datacite_list(metalist: MetadataList | None) -> list | None:
    """Write DataCite list"""
    if metalist is None:
        return None
    return [write_datacite(item) for item in metalist.items]
