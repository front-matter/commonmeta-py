"""Test author utils"""
import pytest
from commonmeta.author_utils import (
    cleanup_author,
    authors_as_string,
    get_one_author,
    get_authors,
    get_affiliations,
    is_personal_name,
)
from commonmeta.base_utils import wrap


def test_one_author():
    "one author"
    # Crossref author with ORCID
    authors = [
        {
            "ORCID": "http://orcid.org/0000-0003-0077-4738",
            "given": "Matt",
            "family": "Jones",
        }
    ]
    assert {
        "id": "https://orcid.org/0000-0003-0077-4738",
        "type": "Person",
        "contributorRoles": ["Author"],
        "familyName": "Jones",
        "givenName": "Matt",
    } == get_one_author(authors[0])
    # Crossref author with url
    authors = [
        {
            "url": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        }
    ]
    assert {
        "id": "https://orcid.org/0000-0003-0077-4738",
        "type": "Person",
        "contributorRoles": ["Author"],
        "familyName": "Jones",
        "givenName": "Matt",
    } == get_one_author(authors[0])
    # has familyName
    assert {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
    } == get_one_author(
        {
            "name": "Fenner, Martin",
            "givenName": "Martin",
            "familyName": "Fenner",
            "contributorRoles": ["Author"],
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
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Benjamin",
        "familyName": "Ollomo",
        "affiliation": [
            {
                "id": "https://ror.org/01wyqb997",
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
    assert (
        {
            "givenName": "กัญจนา",
            "familyName": "แซ่เตียว",
            "contributorRoles": ["Author"],
            "type": "Person",
        }
    ) == get_one_author(
        {"name": "กัญจนา แซ่เตียว", "affiliation": [], "nameIdentifiers": []}
    )
    # multiple author names in one field
    assert {
        "name": "Enos, Ryan (Harvard University); Fowler, Anthony (University of Chicago); Vavreck, Lynn (UCLA)",
        "type": "Organization",
        "contributorRoles": ["Author"],
    } == get_one_author(
        {
            "name": "Enos, Ryan (Harvard University); Fowler, Anthony (University of Chicago); Vavreck, Lynn (UCLA)",
            "affiliation": [],
            "nameIdentifiers": [],
        }
    )
    # 'hyper-authorship'
    assert {
        "contributorRoles": ["Author"],
        "type": "Organization",
        "name": "ALICE Collaboration",
    } == get_one_author(
        {
            "name": "ALICE Collaboration",
            "affiliation": [],
            "id": None,
        }
    )
    # is organization
    author = {
        "email": "info@ucop.edu",
        "creatorName": {
            "#text": "University of California, Santa Barbara",
        },
        "role": {
            "namespace": "http://www.ngdc.noaa.gov/metadata/published/xsd/schema/resources/Codelist/gmxCodelists.xml#CI_RoleCode",
            "roleCode": "copyrightHolder",
        },
    }
    assert {
        "name": "University of California, Santa Barbara",
        "type": "Organization",
        "contributorRoles": ["Author"],
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
        "type": "Person",
        "contributorRoles": ["Author"],
    } == get_one_author(
        {
            "given": "Martial",
            "family": "Sankar",
            "sequence": "first",
            "contributorRoles": ["Author"],
            "affiliation": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
        }
    )
    # multiple name_identifier
    assert {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Thomas",
        "familyName": "Dubos",
        "affiliation": [
            {"name": "École Polytechnique\nLaboratoire de Météorologie Dynamique"}
        ],
        "id": "http://isni.org/isni/0000 0003 5752 6882",
    } == get_one_author(
        {
            "name": "Dubos, Thomas",
            "type": "Person",
            "contributorRoles": ["Author"],
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
        "type": "Person",
        "contributorRoles": ["Author"],
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
            "type": "Person",
            "contributorRoles": ["Author"],
            "id": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        },
        {
            "type": "Person",
            "contributorRoles": ["Author"],
            "id": "http://orcid.org/0000-0002-2192-403X",
            "givenName": "Peter",
            "familyName": "Slaughter",
        },
        {"type": "Organization", "name": "University of California, Santa Barbara"},
    ]
    assert "Jones, Matt and Slaughter, Peter" == authors_as_string(wrap(authors[0:2]))
    # single author
    assert "Jones, Matt" == authors_as_string(wrap(authors[0]))
    # no authors
    assert "" == authors_as_string(wrap(None))
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
        {
            "name": "University of California, Santa Barbara",
        },
    ]
    assert [
        {
            "id": "https://orcid.org/0000-0003-0077-4738",
            "type": "Person",
            "contributorRoles": ["Author"],
            "givenName": "Matt",
            "familyName": "Jones",
        },
        {
            "type": "Person",
            "contributorRoles": ["Author"],
            "givenName": "Peter",
            "familyName": "Slaughter",
        },
        {
            "name": "University of California, Santa Barbara",
            "type": "Organization",
            "contributorRoles": ["Author"],
        },
    ] == get_authors(authors)


def test_get_affiliations():
    "get_affiliations"
    assert [] == get_affiliations(wrap(None))
    assert [{"name": "University of California, Santa Barbara"}] == get_affiliations(
        ["University of California, Santa Barbara"]
    )
    assert [{"name": "University of California, Santa Barbara"}] == get_affiliations(
        [{"name": "University of California, Santa Barbara"}]
    )
    assert [
        {
            "name": "University of California, Santa Barbara",
            "id": "https://ror.org/02t274463",
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


def test_is_personal_name():
    """is personal name"""
    assert True is is_personal_name("Fenner, Martin")
    assert False is is_personal_name("University of California, Santa Barbara")
    assert False is is_personal_name("ALICE Collaboration")
    assert True is is_personal_name("กัญจนา แซ่เตียว")
    assert False is is_personal_name(
        "International Genetics of Ankylosing Spondylitis Consortium (IGAS)"
    )
