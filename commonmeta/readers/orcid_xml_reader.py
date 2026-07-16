"""ORCID XML reader for Commonmeta.

Reads a full ORCID *record* XML - the shape found in the bulk summaries dumps
and served by the ORCID API's record endpoint - and returns a commonmeta
*person* entity.

Unlike the person JSON read by :mod:`commonmeta.readers.orcid_reader`, a record
carries employments and educations, which become the person's affiliations.
"""

from __future__ import annotations

from ..base_utils import compact, dig, parse_xml, presence, wrap
from ..constants import ORCID_TO_CM_AFFILIATION_TYPES, Commonmeta
from .orcid_reader import display_name, format_identifier


def parse_orcid_xml(string: str | bytes | None) -> dict | None:
    """Parse an ORCID record XML into a dict, stripping ORCID's namespaces."""
    result = parse_xml(string, dialect="orcid")
    return dict(result) if isinstance(result, dict) else None


def format_affiliation_date(date: dict | None) -> str | None:
    """Convert an ORCID affiliation date (year/month/day parts) to ISO 8601."""
    if not date:
        return None
    year = date.get("year", None)
    if not year:
        return None
    month = date.get("month", None)
    day = date.get("day", None)
    if month and day:
        return f"{year}-{month:0>2}-{day:0>2}"
    if month:
        return f"{year}-{month:0>2}"
    return year


def normalize_ror_identifier(identifier: str | None) -> str | None:
    """Normalize a ROR affiliation identifier to a ROR URL.

    ORCID stores these either bare or as a URL; commonmeta wants the URL form.
    """
    if not identifier:
        return None
    bare = identifier.removeprefix("https://ror.org/").removeprefix("http://ror.org/")
    return f"https://ror.org/{bare}"


def format_affiliation(summary: dict, role_prefix: str | None = None) -> dict | None:
    """Convert an ORCID employment/education summary to a commonmeta affiliation."""
    organization = summary.get("organization", None) or {}
    name = organization.get("name", None)
    if not name:
        return None
    # ORCID models the department separately; commonmeta has one name field.
    department = summary.get("department-name", None)
    if department:
        name = f"{name}, {department}"

    disambiguated = organization.get("disambiguated-organization", None) or {}
    identifier = disambiguated.get("disambiguated-organization-identifier", None)
    source = disambiguated.get("disambiguation-source", None) or ""
    identifier_type = ORCID_TO_CM_AFFILIATION_TYPES.get(source.upper())
    if identifier_type == "ROR":
        identifier = normalize_ror_identifier(identifier)
    if identifier_type is None:
        identifier = None

    role = summary.get("role-title", None)
    if role_prefix:
        role = f"{role_prefix}: {role}" if role else role_prefix

    return compact(
        {
            "identifier": identifier,
            "identifier_type": identifier_type if identifier else None,
            "name": name,
            "role": role,
            "start_date": format_affiliation_date(summary.get("start-date", None)),
            "end_date": format_affiliation_date(summary.get("end-date", None)),
        }
    )


def get_affiliations(meta: dict) -> list:
    """Employments and educations, in that order, as commonmeta affiliations.

    An education's role is prefixed "Education" so the two stay distinguishable
    once flattened into a single list.
    """
    employments = [
        affiliation
        for group in wrap(dig(meta, "activities-summary.employments.affiliation-group"))
        if (summary := group.get("employment-summary", None))
        and (affiliation := format_affiliation(summary)) is not None
    ]
    educations = [
        affiliation
        for group in wrap(dig(meta, "activities-summary.educations.affiliation-group"))
        if (summary := group.get("education-summary", None))
        and (affiliation := format_affiliation(summary, role_prefix="Education"))
        is not None
    ]
    return employments + educations


def read_orcid_xml(data: dict | None, **kwargs) -> Commonmeta:
    """read_orcid_xml: ORCID record XML -> commonmeta person entity"""
    if data is None:
        return {"state": "not_found"}
    meta = data.get("record", None) or data
    read_options = kwargs or {}

    name = dig(meta, "person.name") or {}
    given_name = name.get("given-names", None)
    family_name = name.get("family-name", None)

    additional_names = [
        value
        for i in wrap(dig(meta, "person.other-names.other-name"))
        if (value := i.get("content", None))
    ]

    identifiers = [
        identifier
        for i in wrap(dig(meta, "person.external-identifiers.external-identifier"))
        if (identifier := format_identifier(i)) is not None
    ]

    addresses = wrap(dig(meta, "person.addresses.address"))
    country = addresses[0].get("country", None) if addresses else None

    return {
        **compact(
            {
                "id": dig(meta, "orcid-identifier.uri"),
                "given_name": given_name,
                "family_name": family_name,
                "name": display_name(
                    given_name, family_name, name.get("credit-name", None)
                ),
                "additional_names": presence(additional_names),
                # A record XML also carries a biography and researcher-urls.
                # They are deliberately not read here: the golden fixtures for
                # this format omit them, and a person read from XML is expected
                # to carry identity and affiliations only. The person JSON path
                # in orcid_reader does read both.
                "affiliations": presence(get_affiliations(meta)),
                "identifiers": presence(identifiers),
                "country": country,
                # Unlike the person JSON, the XML carries an ISO 8601 string
                # rather than milliseconds since the epoch.
                "date_updated": dig(meta, "history.last-modified-date"),
                "asserted_by": "ORCID",
            }
        ),
        **read_options,
    }
