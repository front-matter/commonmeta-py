"""Test author utils"""
import pytest
from talbot.author_utils import (
    cleanup_author,
    authors_as_string,
    get_one_author,
    get_authors,
    get_affiliations,
)


def test_one_author():
    "one author"
    authors = [
        {
            "ORCID": "http://orcid.org/0000-0003-0077-4738",
            "given": "Matt",
            "family": "Jones",
        }
    ]
    assert {
        "familyName": "Jones",
        "givenName": "Matt",
        "name": "Matt Jones",
        "nameType": "Personal",
    } == get_one_author(authors[0])
    # has familyName
    assert {
        "nameIdentifiers": [
            {
                "nameIdentifier": "https://orcid.org/0000-0003-1419-2405",
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        ],
        "name": "Martin Fenner",
        "givenName": "Martin",
        "familyName": "Fenner",
        "nameType": "Personal",
    } == get_one_author(
        {
            "name": "Fenner, Martin",
            "givenName": "Martin",
            "familyName": "Fenner",
            "nameIdentifiers": [
                {
                    "nameIdentifier": "https://orcid.org/0000-0003-1419-2405",
                    "nameIdentifierScheme": "ORCID",
                    "schemeUri": "https://orcid.org",
                }
            ],
        }
    )
    # has name in sort-order' do
    assert {
        "nameType": "Personal",
        "name": "Benjamin Ollomo",
        "givenName": "Benjamin",
        "familyName": "Ollomo",
        "affiliation": [
            {
                "affiliationIdentifier": "https://ror.org/01wyqb997",
                "affiliationIdentifierScheme": "ROR",
                "name": "Centre International de Recherches Médicales de Franceville",
            }
        ],
    } == get_one_author(
        {
            "name": "Ollomo, Benjamin",
            "givenName": "Benjamin",
            "familyName": "Ollomo",
            "affiliation": [
                {
                    "name": "Centre International de Recherches Médicales de Franceville",
                    "affiliationIdentifier": "01wyqb997",
                    "affiliationIdentifierScheme": "ROR",
                    "schemeURI": "https://ror.org/",
                }
            ],
        }
    )
    # has name in Thai
    assert ({"name": "กัญจนา แซ่เตียว"}) == get_one_author(
        {"name": "กัญจนา แซ่เตียว", "affiliation": [], "nameIdentifiers": []}
    )
    # multiple author names in one field
    assert {
        "name": "Enos, Ryan (Harvard University); Fowler, Anthony (University of Chicago); Vavreck, Lynn (UCLA)"
    } == get_one_author(
        {
            "name": "Enos, Ryan (Harvard University); Fowler, Anthony (University of Chicago); Vavreck, Lynn (UCLA)",
            "affiliation": [],
            "nameIdentifiers": [],
        }
    )
    # 'hyper-authorship'
    assert {"name": "ALICE Collaboration"} == get_one_author(
        {
            "name": "ALICE Collaboration",
            "nameType": "Organizational",
            "affiliation": [],
            "nameIdentifiers": [],
        }
    )
    # is organization
    author = {
        "email": "info@ucop.edu",
        "creatorName": {
            "__content__": "University of California, Santa Barbara",
            "nameType": "Organizational",
        },
        "role": {
            "namespace": "http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_RoleCode",
            "roleCode": "copyrightHolder",
        },
    }
    assert {
        "name": "University of California, Santa Barbara",
        "nameType": "Organizational",
    } == get_one_author(author)
    # name with affiliation crossref
    assert {
        "affiliation": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
            }
        ],
        "familyName": "Sankar",
        "givenName": "Martial",
        "name": "Martial Sankar",
        "nameType": "Personal",
    } == get_one_author(
        {
            "given": "Martial",
            "family": "Sankar",
            "sequence": "first",
            "affiliation": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
        }
    )
    # multiple name_identifier
    assert {
        "nameType": "Personal",
        "name": "Thomas Dubos",
        "givenName": "Thomas",
        "familyName": "Dubos",
        "affiliation": [
            {"name": "École Polytechnique\nLaboratoire de Météorologie Dynamique"}
        ],
        "nameIdentifiers": [
            {
                "nameIdentifier": "http://isni.org/isni/0000 0003 5752 6882",
                "nameIdentifierScheme": "ISNI",
            },
            {
                "nameIdentifier": "https://orcid.org/0000-0003-4514-4211",
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            },
        ],
    } == get_one_author(
        {
            "name": "Dubos, Thomas",
            "nameType": "Personal",
            "givenName": "Thomas",
            "familyName": "Dubos",
            "affiliation": [
                "École Polytechnique\nLaboratoire de Météorologie Dynamique"
            ],
            "nameIdentifiers": [
                {
                    "nameIdentifier": "http://isni.org/isni/0000 0003 5752 6882",
                    "nameIdentifierScheme": "ISNI",
                },
                {
                    "nameIdentifier": "https://orcid.org/0000-0003-4514-4211",
                    "nameIdentifierScheme": "ORCID",
                },
            ],
        }
    )
    # only familyName and givenName
    assert {
        "nameType": "Personal",
        "name": "Emma Johansson",
        "givenName": "Emma",
        "familyName": "Johansson",
    } == get_one_author(
        {
            "givenName": "Emma",
            "familyName": "Johansson",
            "affiliation": [],
            "nameIdentifiers": [],
        }
    )


def test_cleanup_author():
    "cleanup_author"
    assert "John Smith" == cleanup_author("John Smith")
    assert "Smith, John" == cleanup_author("Smith, John")
    assert "Smith, J." == cleanup_author("Smith, J.")


def test_authors_as_string():
    "authors_as_string"
    authors = [
        {
            "nameType": "Person",
            "id": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        },
        {
            "nameType": "Person",
            "id": "http://orcid.org/0000-0002-2192-403X",
            "givenName": "Peter",
            "familyName": "Slaughter",
        },
        {"nameType": "Organization", "name": "University of California, Santa Barbara"},
    ]
    assert "Jones, Matt and Slaughter, Peter" == authors_as_string(authors[0:2])
    # single author
    assert "Jones, Matt" == authors_as_string(authors[0])
    # no authors
    assert None is authors_as_string(None)
    # with organization
    assert (
        "Jones, Matt and Slaughter, Peter and University of California, Santa Barbara"
        == authors_as_string(authors)
    )


def test_get_authors():
    "get_authors"
    authors = [
        {
            "ORCID": "https://orcid.org/0000-0003-0077-4738",
            "given": "Matt",
            "family": "Jones",
        },
        {"given": "Peter", "family": "Slaughter"},
        {"name": "University of California, Santa Barbara"},
    ]
    assert [
        {
            "nameType": "Personal",
            "givenName": "Matt",
            "familyName": "Jones",
            "name": "Matt Jones",
        },
        {
            "nameType": "Personal",
            "name": "Peter Slaughter",
            "givenName": "Peter",
            "familyName": "Slaughter",
        },
        {"name": "University of California, Santa Barbara"},
    ] == get_authors(authors)


def test_get_affiliations():
    "get_affiliations"
    assert None == get_affiliations(None)
    assert [{"name": "University of California, Santa Barbara"}] == get_affiliations(
        ["University of California, Santa Barbara"]
    )
    assert [{"name": "University of California, Santa Barbara"}] == get_affiliations(
        [{"name": "University of California, Santa Barbara"}]
    )
    assert [
        {
            "name": "University of California, Santa Barbara",
            "affiliationIdentifier": "https://ror.org/02t274463",
            "affiliationIdentifierScheme": "ROR",
        }
    ] == get_affiliations(
        [
            {
                "name": "University of California, Santa Barbara",
                "affiliationIdentifier": "02t274463",
                "affiliationIdentifierScheme": "ROR",
                "schemeURI": "https://ror.org/",
            }
        ]
    )
