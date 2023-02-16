"""Author utils module for Talbot."""
import re
from typing import Optional, List
from .utils import (
    normalize_orcid,
    normalize_id,
)
from .base_utils import parse_attributes, wrap, presence, compact


def get_one_author(author):
    """parse one author string into CSL format"""
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
    contributor_type = parse_attributes(author.get("contributorType", None))
    name_type = parse_attributes(
        author.get("creatorName", None), content="nameType", first=True
    ) or parse_attributes(
        author.get("contributorName", None), content="nameType", first=True
    )

    name_identifiers = []
    for name_identifier in wrap(author.get("nameIdentifiers", [])):
        if name_identifier.get("nameIdentifier", None) is None:
            continue
        if name_identifier.get("nameIdentifierScheme", None) == "ORCID":
            name_ident = compact(
                {
                    "nameIdentifier": normalize_orcid(
                        name_identifier.get("nameIdentifier", None)
                    ),
                    "schemeUri": "https://orcid.org",
                    "nameIdentifierScheme": "ORCID",
                }
            )
            name_identifiers.append(name_ident)
        elif name_identifier.get("schemeURI", None) is not None:
            name_ident = compact(
                {
                    "nameIdentifier": name_identifier.get("schemeURI")
                    + name_identifier.get("nameIdentifier", None),
                    "schemeUri": name_identifier.get("schemeURI"),
                    "nameIdentifierScheme": name_identifier.get(
                        "nameIdentifierScheme", None
                    ),
                }
            )
            name_identifiers.append(name_ident)
        else:
            name_ident = compact(
                {
                    "nameIdentifier": name_identifier.get("nameIdentifier", None),
                    "nameIdentifierScheme": name_identifier.get(
                        "nameIdentifierScheme", None
                    ),
                }
            )
            name_identifiers.append(name_ident)
    if len(name_identifiers) == 0:
        name_identifiers = None

    # Crossref metadata
    if name_identifiers is None and author.get("ORCID", None):
        name_identifiers = [
            {
                "nameIdentifier": normalize_orcid(author.get("ORCID")),
                "schemeUri": "https://orcid.org",
                "nameIdentifierScheme": "ORCID",
            }
        ]

    if family_name or given_name:
        name_type = "Personal"
    elif name_type is None and any(
        ni
        for ni in wrap(name_identifiers)
        if ni.get("nameIdentifierScheme", None) == "ORCID"
    ):
        name_type = "Personal"
    elif name_type is None and any(
        ni
        for ni in wrap(name_identifiers)
        if ni.get("nameIdentifierScheme", None) in ("ISNI", "GRID", "ROR")
    ):
        name_type = "Organizational"
    author = compact(
        {
            "nameType": name_type,
            "name": name if not family_name else None,
            "givenName": given_name,
            "familyName": family_name,
            "nameIdentifiers": name_identifiers,
            "affiliation": presence(get_affiliations(wrap(author.get("affiliation", None)))),
            "contributorType": contributor_type,
        }
    )

    if family_name:
        return author

    if name_type == "Personal":
        return compact(
            {
                "nameType": "Personal",
                "name": name if not family_name else None,
                "givenName": given_name,
                "familyName": family_name,
                "nameIdentifiers": name_identifiers,
                "affiliation": presence(get_affiliations(wrap(author.get("affiliation", None)))),
                "contributorType": contributor_type,
            }
        )
    return compact(
        {
            "nameType": name_type,
            "name": name,
            "nameIdentifiers": name_identifiers,
            "affiliation": presence(get_affiliations(wrap(author.get("affiliation", None)))),
            "contributorType": contributor_type,
        }
    )


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
    """parse array of affiliation strings into CSL format"""
    def format_element(i):
        """format single affiliation element"""
        affiliation_identifier = None
        if isinstance(i, str):
            name = i
            affiliation_identifier_scheme = None
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
            name = i.get("name", None) or i.get("__content__", None)
            affiliation_identifier_scheme = i.get(
                "affiliationIdentifierScheme", None
            )
            scheme_uri = i.get("SchemeURI", None)
        return compact({
            "name": name,
            "affiliationIdentifier": affiliation_identifier,
            "affiliationIdentifierScheme": affiliation_identifier_scheme,
            "schemeUri": scheme_uri,
         })
    return [format_element(i) for i in affiliations]
