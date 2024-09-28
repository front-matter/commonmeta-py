"""DataCite writer for commonmeta-py"""
import orjson as json
from typing import Optional, Union

from ..base_utils import wrap, compact
from ..doi_utils import doi_from_url, normalize_doi
from ..constants import (
    CM_TO_BIB_TRANSLATIONS,
    CM_TO_CSL_TRANSLATIONS,
    CM_TO_CR_TRANSLATIONS,
    CM_TO_DC_TRANSLATIONS,
    CM_TO_RIS_TRANSLATIONS,
    CM_TO_SO_TRANSLATIONS,
    Commonmeta,
)


def write_datacite(metadata: Commonmeta) -> Optional[Union[str, dict]]:
    """Write datacite. Make sure JSON Schema validates before writing"""
    if metadata.write_errors is not None:
        return "{}"

    alternate_identifiers = [
        {
            "alternateIdentifier": i.get("identifier", None),
            "alternateIdentifierType": i.get("identifierType", None),
        }
        for i in wrap(metadata.identifiers)
        if i.get("id", None) != metadata.id
    ]

    creators = [
        to_datacite_creator(i)
        for i in wrap(metadata.contributors)
        if i.get("contributorRoles", None) == ["Author"]
    ]
    contributors = [
        to_datacite_creator(i)
        for i in wrap(metadata.contributors)
        if i.get("contributorRoles", None) != ["Author"]
    ]
    related_identifiers = [
        to_datacite_related_identifier(i)
        for i in wrap(metadata.references)
        if i.get("id", None)
    ]

    resource__typegeneral = CM_TO_DC_TRANSLATIONS.get(metadata.type, "Other")
    resource_type = CM_TO_CR_TRANSLATIONS.get(metadata.type, "Other")
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
        metadata.date.get("published")[:4]
        if metadata.date.get("published", None)
        else None
    )

    def to_datacite_date(date: dict) -> dict:
        """Convert dates to datacite dates"""
        for k, v in date.items():
            if k == "published":
                k = "issued"
            return {
                "date": v,
                "dateType": k.title(),
            }

    dates = [to_datacite_date(i) for i in wrap(metadata.date)]

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

    descriptions = [
        compact(
            {
                "description": i.get("description", None),
                "descriptionType": i.get("type", None) or "Other",
                "lang": i.get("language", None),
            }
        )
        for i in wrap(metadata.descriptions)
    ]

    data = compact(
        {
            "id": metadata.id,
            "doi": doi_from_url(metadata.id),
            "url": metadata.url,
            "creators": creators,
            "titles": metadata.titles,
            "publisher": metadata.publisher,
            "publicationYear": publication_year,
            "subjects": metadata.subjects,
            "contributors": contributors,
            "dates": dates,
            "language": metadata.language,
            "types": types,
            "alternateIdentifiers": alternate_identifiers,
            "relatedIdentifiers": related_identifiers,
            "version": metadata.version,
            "rightsList": license_,
            "descriptions": descriptions,
            "geoLocations": metadata.geo_locations,
            "fundingReferences": metadata.funding_references,
            "schemaVersion": "http://datacite.org/schema/kernel-4",
        }
    )
    return json.dumps(data)


def to_datacite_creator(creator: dict) -> dict:
    """Convert creators to datacite creators"""
    _type = creator.get("type", None)
    if creator.get("familyName", None):
        name = ", ".join([creator.get("familyName", ""), creator.get("givenName", "")])
    elif creator.get("name", None):
        name = creator.get("name", None)
    name_identifiers = creator.get("id", None)
    if name_identifiers:

        def format_name_identifier(name_identifier):
            return {
                "nameIdentifier": name_identifier,
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }

        name_identifiers = [format_name_identifier(i) for i in wrap(name_identifiers)]
    return compact(
        {
            "name": name,
            "givenName": creator.get("givenName", None),
            "familyName": creator.get("familyName", None),
            "nameType": _type + "al" if _type else None,
            "nameIdentifiers": name_identifiers,
            "affiliation": creator.get("affiliations", None),
        }
    )


def to_datacite_titles(titles: list) -> list:
    """Convert titles to datacite titles"""
    return [
        {
            "title": title.get("title", None),
            "titleType": title.get("type", None),
            "lang": title.get("language", None),
        }
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
