"""Author utils module for commonmeta-py"""
import re
from typing import List
from urllib.parse import urlparse
from .utils import (
    normalize_orcid,
    normalize_id,
)
from .base_utils import parse_attributes, wrap, presence, compact

from .constants import (
    DATACITE_CONTRIBUTOR_TYPES,
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

    contributor_role = parse_attributes(author.get("contributorType", "Author"))
    if contributor_role != "Author":
        contributor_role = DATACITE_CONTRIBUTOR_TYPES.get(contributor_role, "Other")

    # parse author type, i.e. "Person", "Organization" or not specified
    type_ = parse_attributes(
        author.get("creatorName", None), content="type", first=True
    ) or parse_attributes(
        author.get("contributorName", None), content="type", first=True
    )
    
    # DataCite metadata
    if isinstance(type_, str) and type_.endswith("al"):
        type_ = type_[:-3]

    if not type_ and isinstance(id, str) and urlparse(id).hostname == "ror.org":
        type_ = "Organization"
    elif not type_ and isinstance(id, str) and urlparse(id).hostname == "orcid.org":
        type_ = "Person"
    elif not type_ and (given_name or family_name):
        type_ = "Person"
    elif not type_ and is_personal_name(name):
        type_ = "Person"
    elif not type_ and name:
        type_ = "Organization"

    def format_name_identifier(name_identifier):
        """format_name_identifier"""
        if name_identifier.get("nameIdentifier", None) is None:
            return None
        if name_identifier.get("nameIdentifierScheme", None) == "ORCID":
            return normalize_orcid(name_identifier.get("nameIdentifier", None))
        if name_identifier.get("schemeURI", None) is not None:
            return name_identifier.get("schemeURI") + name_identifier.get(
                "nameIdentifier", None
            )
        return name_identifier.get("nameIdentifier", None)

    id_ = next(
        (format_name_identifier(i) for i in wrap(author.get("nameIdentifiers", None))),
        None,
    )

    # Crossref metadata
    if id_ is None and author.get("ORCID", None):
        id_ = normalize_orcid(author.get("ORCID"))

    if family_name or given_name or (type_ is None and id_ is not None):
        type_ = "Person"
    author = compact(
        {
            "id": id_,
            "type": type_,
            "name": name if not family_name else None,
            "givenName": given_name,
            "familyName": family_name,
            "affiliation": presence(
                get_affiliations(wrap(author.get("affiliation", None)))
            ),
            "contributorRoles": [contributor_role],
        }
    )

    if family_name:
        return author

    if type_ == "Person":
        return compact(
            {
                "id": id_,
                "type": "Person",
                "givenName": given_name,
                "familyName": family_name,
                "affiliation": presence(
                    get_affiliations(wrap(author.get("affiliation", None)))
                ),
                "contributorRoles": [contributor_role],
            }
        )
    return compact(
        {
            "id": id_,
            "type": type_,
            "name": name,
            "affiliation": presence(
                get_affiliations(wrap(author.get("affiliation", None)))
            ),
            "contributorRoles": [contributor_role],
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

    # check for suffixes, e.g. "John Smith, MD"
    if name.split(", ")[-1] in ["MD", "PhD"]:
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
    """parse array of author strings into CSL format"""
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
