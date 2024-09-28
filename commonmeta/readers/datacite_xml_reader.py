"""datacite_xml reader for Commonmeta"""

from collections import defaultdict
import httpx
from pydash import py_

from ..base_utils import compact, wrap, presence, sanitize, parse_attributes
from ..author_utils import get_authors
from ..date_utils import strip_milliseconds, normalize_date_dict
from ..doi_utils import doi_from_url, doi_as_url, datacite_api_url, normalize_doi
from ..utils import normalize_url, normalize_cc_url, dict_to_spdx
from ..constants import DC_TO_CM_TRANSLATIONS, Commonmeta


def get_datacite_xml(pid: str, **kwargs) -> dict:
    """get_datacite_xml"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = datacite_api_url(doi)
    response = httpx.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return py_.get(response.json(), "data.attributes", {}) | {"via": "datacite_xml"}


def read_datacite_xml(data: dict, **kwargs) -> Commonmeta:
    """read_datacite_xml"""
    if data is None:
        return {"state": "not_found"}

    read_options = kwargs or {}

    meta = data.get("resource", {})

    doi = parse_attributes(meta.get("identifier", None))
    _id = doi_as_url(doi) if doi else None

    resource__typegeneral = py_.get(meta, "resourceType.resourceTypeGeneral")
    _type = DC_TO_CM_TRANSLATIONS.get(resource__typegeneral, "Other")
    additional_type = py_.get(meta, "resourceType.#text")

    identifiers = wrap(py_.get(meta, "alternateIdentifiers.alternateIdentifier"))
    identifiers = get_xml_identifiers(identifiers)

    def format_title(title):
        """format_title"""
        if isinstance(title, str):
            return {"title": title}
        if isinstance(title, dict):
            return {
                "title": title.get("#text", None),
                "titleType": title.get("titleType", None),
                "lang": title.get("xml:lang", None),
            }
        return None

    titles = [format_title(i) for i in wrap(py_.get(meta, "titles.title"))]

    contributors = get_authors(wrap(py_.get(meta, "creators.creator")))
    contrib = get_authors(wrap(meta.get("contributors", None)))
    if contrib:
        contributors = contributors + contrib
    publisher = {"name": py_.get(meta, "publisher")}
    date = get_dates(
        wrap(py_.get(meta, "dates.date")), meta.get("publicationYear", None)
    )

    def format_description(description):
        """format_description"""
        if isinstance(description, str):
            return {"description": description, "type": "Abstract"}
        if isinstance(description, dict):
            return compact(
                {
                    "description": sanitize(description.get("#text", None)),
                    "type": description.get("descriptionType", "Abstract"),
                    "language": description.get("xml:lang", None),
                }
            )
        return None

    descriptions = [
        format_description(i) for i in wrap(py_.get(meta, "descriptions.description"))
    ]

    def format_subject(subject):
        """format_subject"""
        if isinstance(subject, str):
            return {"subject": subject, "subjectScheme": "None"}
        if isinstance(subject, dict):
            return compact(
                {
                    "subject": subject.get("#text", None),
                    "subjectScheme": subject.get("subjectScheme", None),
                    "language": subject.get("xml:lang", None),
                }
            )
        return None

    subjects = [format_subject(i) for i in wrap(py_.get(meta, "subjects.subject")) if i]

    def format_geo_location(geo_location):
        """format_geo_location"""
        if isinstance(geo_location, str):
            return {"geoLocationPlace": geo_location}
        if isinstance(geo_location, dict):
            return compact(
                {
                    "geoLocationPoint": compact(
                        {
                            "pointLatitude": compact(
                                geo_location.get("geoLocationPoint.pointLatitude", None)
                            ),
                            "pointLongitude": compact(
                                geo_location.get(
                                    "geoLocationPoint.pointLongitude", None
                                )
                            ),
                        }
                    ),
                    "geoLocationBox": compact(
                        {
                            "westBoundLongitude": compact(
                                geo_location.get(
                                    "geoLocationBox.westBoundLongitude", None
                                )
                            ),
                            "eastBoundLongitude": compact(
                                geo_location.get(
                                    "geoLocationBox.eastBoundLongitude", None
                                )
                            ),
                            "southBoundLatitude": compact(
                                geo_location.get(
                                    "geoLocationBox.southBoundLatitude", None
                                )
                            ),
                            "northBoundLatitude": compact(
                                geo_location.get(
                                    "geoLocationBox.northBoundLatitude", None
                                )
                            ),
                        }
                    ),
                    "geoLocationPolygon": {
                        "polygonPoint": compact(
                            {
                                "pointLatitude": geo_location.get(
                                    "geoLocationPolygon.polygonPoint.pointLatitude",
                                    None,
                                ),
                                "pointLongitude": geo_location.get(
                                    "geoLocationPolygon.polygonPoint.pointLongitude",
                                    None,
                                ),
                            }
                        )
                    },
                    "geoLocationPlace": geo_location.get("geoLocationPlace", None),
                }
            )
        return None

    geo_locations = []  # [format_geo_location(i) for i in wrap(py_.get(meta, "geoLocations.geoLocation")) if i]

    def map_rights(rights):
        """map_rights"""
        return compact(
            {
                "rights": rights.get("#text", None),
                "url": rights.get("rightsURI", None),
                "lang": rights.get("xml:lang", None),
            }
        )

    license_ = wrap(py_.get(meta, "rightsList.rights"))
    if len(license_) > 0:
        license_ = normalize_cc_url(license_[0].get("rightsURI", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    references = get_xml_references(
        wrap(py_.get(meta, "relatedIdentifiers.relatedIdentifier"))
    )
    relations = get_xml_relations(
        wrap(py_.get(meta, "relatedIdentifiers.relatedIdentifier"))
    )

    def map_funding_reference(funding_reference):
        """map_funding_reference"""
        return {
            "funderName": funding_reference.get("funderName", None),
            "funderIdentifier": funding_reference.get("funderIdentifier", None),
            "funderIdentifierType": funding_reference.get("funderIdentifierType", None),
            "awardNumber": funding_reference.get("awardNumber", None),
            "awardTitle": funding_reference.get("awardTitle", None),
        }

    funding_references = []  # [map_funding_reference(i) for i in wrap(py_.get(meta, "fundingReferences.fundingReference"))]

    files = meta.get("contentUrl", None)
    state = "findable" if _id or read_options else "not_found"

    return {
        # required properties
        "id": _id,
        "type": _type,
        "doi": doi_from_url(_id),
        "url": normalize_url(meta.get("url", None)),
        "contributors": presence(contributors),
        "titles": compact(titles),
        "publisher": publisher,
        "date": date,
        # recommended and optional properties
        "additionalType": presence(additional_type),
        "subjects": presence(subjects),
        "language": meta.get("language", None),
        "identifiers": identifiers,
        "version": meta.get("version", None),
        "license": presence(license_),
        "descriptions": presence(descriptions),
        "geoLocations": presence(geo_locations),
        "fundingReferences": presence(funding_references),
        "references": presence(references),
        "relations": presence(relations),
        # other properties
        "date_created": strip_milliseconds(meta.get("created", None)),
        "date_registered": strip_milliseconds(meta.get("registered", None)),
        "date_published": strip_milliseconds(meta.get("published", None)),
        "date_updated": strip_milliseconds(meta.get("updated", None)),
        "files": presence(files),
        "container": presence(meta.get("container", None)),
        "provider": "DataCite",
        "state": state,
        "schema_version": meta.get("xmlns", None),
    } | read_options


def get_xml_identifiers(identifiers: list) -> list:
    """get_identifiers"""

    def is_identifier(identifier):
        """supported identifier types"""
        return identifier.get("alternateIdentifierType", None) in [
            "ARK",
            "arXiv",
            "Bibcode",
            "DOI",
            "Handle",
            "ISBN",
            "ISSN",
            "PMID",
            "PMCID",
            "PURL",
            "URL",
            "URN",
            "Other",
        ]

    def format_identifier(identifier):
        """format_identifier"""

        if is_identifier(identifier):
            type_ = identifier.get("alternateIdentifierType")
        else:
            type_ = "Other"

        return compact(
            {
                "identifier": identifier.get("#text", None),
                "identifierType": type_,
            }
        )

    return [format_identifier(i) for i in identifiers]


def get_xml_references(references: list) -> list:
    """get_xml_references"""

    def is_reference(reference):
        """is_reference"""
        return reference.get("relationType", None) in [
            "Cites",
            "References",
        ] and reference.get("relatedIdentifierType", None) in ["DOI", "URL"]

    def map_reference(reference):
        """map_reference"""
        identifier = reference.get("relatedIdentifier", None)
        identifier_type = reference.get("relatedIdentifierType", None)
        if identifier and identifier_type == "DOI":
            reference["doi"] = normalize_doi(identifier)
        elif identifier and identifier_type == "URL":
            reference["url"] = normalize_url(identifier)
        reference = py_.omit(
            reference,
            [
                "relationType",
                "relatedIdentifier",
                "relatedIdentifierType",
                "resourceTypeGeneral",
                "schemeType",
                "schemeUri",
                "relatedMetadataScheme",
            ],
        )
        return reference

    return [map_reference(i) for i in references if is_reference(i)]


def get_xml_relations(relations: list) -> list:
    """get_xml_relations"""

    def is_relation(relation):
        """is_relation"""
        return relation.get("relationType", None) in [
            "IsNewVersionOf",
            "IsPreviousVersionOf",
            "IsVersionOf",
            "HasVersion",
            "IsPartOf",
            "HasPart",
            "IsVariantFormOf",
            "IsOriginalFormOf",
            "IsIdenticalTo",
            "IsTranslationOf",
            "IsReviewedBy",
            "Reviews",
            "IsPreprintOf",
            "HasPreprint",
            "IsSupplementTo",
        ]

    def map_relation(relation):
        """map_relation"""
        identifier = relation.get("relatedIdentifier", None)
        identifier_type = relation.get("relatedIdentifierType", None)
        if identifier and identifier_type == "DOI":
            relation["doi"] = normalize_doi(identifier)
        elif identifier and identifier_type == "URL":
            relation["url"] = normalize_url(identifier)
        return {
            "id": identifier,
            "type": identifier_type,
        }

    return [map_relation(i) for i in relations if is_relation(i)]


def get_dates(dates: list, publication_year) -> dict:
    """convert date list to dict, rename and/or remove some keys"""
    date: dict = defaultdict(list)
    for sub in dates:
        date[sub.get("dateType", None)] = sub.get("#text", None)
    if date.get("Issued", None) is None and publication_year is not None:
        date["Issued"] = str(publication_year)
    return normalize_date_dict(date)
