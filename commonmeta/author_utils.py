"""Author utils module for commonmeta-py"""
import re
from typing import List
from nameparser import HumanName

from .utils import (
    normalize_orcid,
    normalize_id,
    normalize_ror,
    normalize_isni,
    format_name_identifier,
    validate_ror,
    validate_orcid,
)
from .base_utils import parse_attributes, wrap, presence, compact

from .constants import (
    COMMONMETA_CONTRIBUTOR_ROLES,
)


def get_one_author(author):
    """parse one author string into commonmeta format"""
    # if author is a string
    if isinstance(author, str):
        author = {"creatorName": author}

    # malformed XML
    if isinstance(author.get("creatorName", None), list):
        return None

    name = (
        parse_attributes(author.get("creatorName", None))
        or parse_attributes(author.get("contributorName", None))
        or parse_attributes(author.get("name", None))
    )
    given_name = parse_attributes(author.get("givenName", None)) or parse_attributes(
        author.get("given", None)
    )
    family_name = parse_attributes(author.get("familyName", None)) or parse_attributes(
        author.get("family", None)
    )

    name = cleanup_author(name)

    # parse contributor roles, checking for roles supported by commonmeta
    contributor_roles = wrap(
        parse_attributes(author.get("contributorType", None))
    ) or wrap(parse_attributes(author.get("contributor_roles", None)))
    contributor_roles = [
        i for i in contributor_roles if i in COMMONMETA_CONTRIBUTOR_ROLES
    ] or ["Author"]

    # parse author type, i.e. "Person", "Organization" or not specified
    type_ = parse_attributes(
        author.get("creatorName", None), content="type", first=True
    ) or parse_attributes(
        author.get("contributorName", None), content="type", first=True
    )

    # also handle Crossref, JSON Feed, or DataCite metadata
    id_ = author.get("id", None) or author.get("ORCID", None) or author.get("url", None) or next(
            (
                format_name_identifier(i)
                for i in wrap(author.get("nameIdentifiers", None))
            ),
            None,
        )
    id_ = normalize_orcid(id_) or normalize_ror(id_) or normalize_isni(id_) or id_

    # DataCite metadata
    if isinstance(type_, str) and type_.endswith("al"):
        type_ = type_[:-3]

    if not type_ and isinstance(id_, str) and validate_ror(id_) is not None:
        type_ = "Organization"
    elif not type_ and isinstance(id_, str) and validate_orcid(id_) is not None:
        type_ = "Person"
    elif not type_ and (given_name or family_name):
        type_ = "Person"
    elif not type_ and is_personal_name(name):
        type_ = "Person"
    elif not type_ and name:
        type_ = "Organization"

    # split name for type Person into given/family name if not already provided
    if type_ == "Person" and name and not given_name and not family_name:
        names = HumanName(name)

        if names:
            given_name = (
                " ".join([names.first, names.middle]).strip() if names.first else None
            )
            family_name = names.last if names.last else None
        else:
            given_name = None
            family_name = None

    # return author in commonmeta format, using name vs. given/family name
    # depending on type
    return compact(
        {
            "id": id_,
            "type": type_,
            "contributorRoles": contributor_roles,
            "name": name if type_ == "Organization" else None,
            "givenName": given_name if type_ == "Person" else None,
            "familyName": family_name if type_ == "Person" else None,
            "affiliation": presence(
                get_affiliations(wrap(author.get("affiliation", None)))
            ),
        }
    )


def is_personal_name(name):
    """is_personal_name"""
    # personal names are not allowed to contain semicolons
    if ";" in name:
        return False

    # check if a name has only one word, e.g. "FamousOrganization", not including commas
    if len(name.split(" ")) == 1 and "," not in name:
        return False

    # check if name contains words known to be used in organization names
    if any(
        word in name
        for word in [
            "University",
            "College",
            "Institute",
            "School",
            "Center",
            "Department",
            "Laboratory",
            "Library",
            "Museum",
            "Foundation",
            "Society",
            "Association",
            "Company",
            "Corporation",
            "Collaboration",
            "Consortium",
            "Incorporated",
            "Inc.",
            "Institute",
            "Institut",
        ]
    ):
        return False

    # check for suffixes, e.g. "John Smith, MD"
    if name.split(", ")[-1] in ["MD", "PhD", "BS"]:
        return True

    # check of name can be parsed into given/family name
    names = HumanName(name)
    if names and (names.first or names.last):
        return True

    return False


def cleanup_author(author):
    """clean up author string"""
    if author is None:
        return None

    # detect pattern "Smith J.", but not "Smith, John K."
    if "," not in author:
        author = re.sub(r"/([A-Z]\.)?(-?[A-Z]\.)/", ", \1\2", author)

    # remove spaces around hyphens
    author = author.replace(" - ", "-")

    # remove non-standard space characters
    author = re.sub("/[ \t\r\n\v\f]/", " ", author)
    return author


def get_authors(authors):
    """trsnsform                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        array of author dicts into commonmeta format"""
    return presence(list(map(lambda author: get_one_author(author), authors)))


def authors_as_string(authors: List[dict]) -> str:
    """convert authors list to string, e.g. for bibtex"""

    def format_author(author):
        if author.get("familyName", None):
            return f"{author['familyName']}, {author['givenName']}"
        return author["name"]

    return " and ".join([format_author(i) for i in authors])


def get_affiliations(affiliations: List[dict]) -> List[dict]:
    """parse array of affiliation strings into commonmeta format"""

    def format_element(i):
        """format single affiliation element"""
        affiliation_identifier = None
        if isinstance(i, str):
            name = i
            scheme_uri = None
        else:
            if i.get("affiliationIdentifier", None) is not None:
                affiliation_identifier = i["affiliationIdentifier"]
                if i.get("schemeURI", None) is not None:
                    scheme_uri = (
                        i["schemeURI"]
                        if i["schemeURI"].endswith("/")
                        else "{affiliation['schemeURI']}/"
                    )
                affiliation_identifier = (
                    normalize_id(scheme_uri + affiliation_identifier)
                    if (
                        not affiliation_identifier.startswith("https://")
                        and scheme_uri is not None
                    )
                    else normalize_id(affiliation_identifier)
                )
            name = i.get("name", None) or i.get("#text", None)
        return compact(
            {
                "id": affiliation_identifier,
                "name": name,
            }
        )

    return [format_element(i) for i in affiliations]
