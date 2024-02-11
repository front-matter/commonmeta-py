"""kbase reader for Commonmeta"""
from pydash import py_

from ..utils import normalize_url, normalize_doi, from_curie, from_kbase
from ..base_utils import compact, wrap, presence, sanitize
from ..author_utils import get_authors
from ..date_utils import normalize_date_dict
from ..doi_utils import doi_from_url, validate_doi
from ..constants import (
    COMMONMETA_RELATION_TYPES,
    Commonmeta,
)


def read_kbase(data: dict, **kwargs) -> Commonmeta:
    """read_kbase"""
    meta = data.get("credit_metadata", {})
    read_options = kwargs or {}

    _id = from_curie(meta.get("identifier", None))
    _type = "Dataset"
    contributors = get_authors(from_kbase(wrap(meta.get("contributors", None))))

    publisher = meta.get("publisher", None)
    if publisher is not None:
        publisher = {
            "id": from_curie(publisher.get("organization_id", None)),
            "name": publisher.get("organization_name", None),
        }
    titles = [format_title(i) for i in wrap(meta.get("titles", None))]

    date: dict = {}

    # convert date list to dict
    for sub in wrap(meta.get("dates", None)):
        data_type = sub.get("event", None)
        date[data_type.capitalize() if data_type else None] = sub.get("date", None)
    date = normalize_date_dict(date)

    container = compact(
        {
            "id": "https://www.re3data.org/repository/r3d100012864",
            "type": "DataRepository",
            "title": "KBase",
        }
    )
    license_ = meta.get("license", None)
    if license_:
        license_ = license_[0]
    descriptions = meta.get("descriptions", None)
    for des in wrap(descriptions):
        des["description"] = sanitize(des["description_text"])
        des["type"] = (
            des["description_type"]
            if des["description_type"] in ["Abstract", "Description", "Summary"]
            else None
        )
        py_.omit(des, ["description_text", "description_type"])
    language = meta.get("language", None)

    # subjects = [name_to_fos(i) for i in wrap(py_.get(meta, "metadata.keywords"))]

    version = meta.get("version", None)
    references = get_references(wrap(meta.get("related_identifiers")))
    related_identifiers = get_related_identifiers(wrap(meta.get("related_identifiers")))
    funding_references = get_funding_references(wrap(meta.get("funding", None)))
    files = [get_file(i) for i in wrap(meta.get("content_url"))]

    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "id": _id,
        "type": _type,
        "doi": doi_from_url(_id),
        "url": normalize_url(meta.get("url", None)),
        "contributors": contributors,
        "titles": titles,
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional properties
        "additional_type": None,
        "subjects": None,
        "language": language,
        "alternate_identifiers": None,
        "sizes": None,
        "formats": None,
        "version": py_.get(meta, "metadata.version"),
        "license": presence(license_),
        "descriptions": descriptions,
        "geo_locations": None,
        "funding_references": presence(funding_references),
        "references": presence(references),
        "related_identifiers": presence(related_identifiers),
        # other properties
        "files": presence(files),
        "container": container,
        "provider": "KBase",
        "state": state,
        "schema_version": py_.get(data, "credit_metadata_schema_version"),
    } | read_options


def format_title(title: dict) -> dict:
    """format_title"""
    _type = title.get("title_type", None)
    return compact(
        {
            "title": title.get("title", None),
            "type": _type
            if _type in ["AlternativeTitle", "Subtitle", "TranslatedTitle"]
            else None,
        }
    )


def get_references(references: list) -> list:
    """get_references"""

    def is_reference(reference):
        """is_reference"""
        return reference.get("relationship_type", None) in [
            "DataCite:Cites",
            "DataCite:References",
            "DataCite:IsSupplementedBy",
        ]

    def map_reference(reference):
        """map_reference"""
        identifier = from_curie(reference.get("id", None))
        identifier_type = "DOI" if validate_doi(identifier) else "URL"
        if identifier and identifier_type == "DOI":
            reference["doi"] = normalize_doi(identifier)
        elif identifier and identifier_type == "URL":
            reference["url"] = normalize_url(identifier)
        reference = py_.omit(
            reference,
            [
                "id",
                "relationship_type",
            ],
        )
        return reference

    return [map_reference(i) for i in references if is_reference(i)]


def get_file(file: str) -> dict:
    """get_file"""
    return compact({"url": file})


def get_related_identifiers(related_identifiers: list) -> list:
    """get_related_identifiers"""

    def map_related_identifier(related_identifier: dict) -> dict:
        """get_related_identifier"""
        identifier = from_curie(related_identifier.get("id", None))
        _type = related_identifier.get("relationship_type", None)
        # remove DataCite: and Crossref: prefixes
        _type = _type.split(":")[1] if _type else None
        if normalize_url(identifier):
            identifier = normalize_url(identifier)
        # TODO: resolvable url for other identifier types
        else:
            identifier = None
        return {
            "id": identifier,
            "type": _type,
        }

    identifiers = [map_related_identifier(i) for i in related_identifiers]
    return [i for i in identifiers if i["type"] in COMMONMETA_RELATION_TYPES]


def get_funding_references(funding_references: list) -> list:
    """get_funding_references"""

    def map_funding_reference(funding_reference: dict) -> dict:
        """map_funding_reference"""
        funder_identifier = py_.get(funding_reference, "funder.organization_id", None)
        funder_identifier_type = (
            funder_identifier.split(":")[0] if funder_identifier else None
        )
        return compact(
            {
                "funderIdentifier": from_curie(funder_identifier),
                "funderIdentifierType": funder_identifier_type,
                "funderName": py_.get(
                    funding_reference, "funder.organization_name", None
                ),
                "awardNumber": funding_reference.get("grant_id", None),
                "award_uri": funding_reference.get("grant_url", None),
            }
        )

    return [map_funding_reference(i) for i in funding_references]


def format_descriptions(descriptions: list) -> list:
    """format_descriptions"""
    return [
        {
            "description": sanitize(i),
            "descriptionType": "Abstract" if index == 0 else "Other",
        }
        for index, i in enumerate(descriptions)
        if i
    ]
