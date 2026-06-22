"""Test author utils"""

from commonmeta.author_utils import (
    authors_as_string,
    cleanup_author,
    get_affiliations,
    get_authors,
    get_one_author,
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
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-0077-4738",
            "given_name": "Matt",
            "family_name": "Jones",
        },
        "roles": ["Author"],
    } == get_one_author(authors[0])
    # JSON Feed author with url
    authors = [
        {
            "url": "http://orcid.org/0000-0003-0077-4738",
            "name": "Matt Jones",
        }
    ]
    assert {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-0077-4738",
            "given_name": "Matt",
            "family_name": "Jones",
        },
        "roles": ["Author"],
    } == get_one_author(authors[0])
    # has familyName
    assert {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "given_name": "Martin",
            "family_name": "Fenner",
        },
        "roles": ["Author"],
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
        "person": {
            "given_name": "Benjamin",
            "family_name": "Ollomo",
            "affiliations": [
                {
                    "id": "https://ror.org/01wyqb997",
                    "name": "Centre International de Recherches Médicales de Franceville",
                }
            ],
        },
        "roles": ["Author"],
    } == get_one_author(
        {
            "name": "Ollomo, Benjamin",
            "givenName": "Benjamin",
            "familyName": "Ollomo",
            "affiliations": [
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
    assert {
        "type": "Person",
        "person": {
            "given_name": "กัญจนา",
            "family_name": "แซ่เตียว",
        },
        "roles": ["Author"],
    } == get_one_author(
        {"name": "กัญจนา แซ่เตียว", "affiliations": [], "nameIdentifiers": []}
    )
    # multiple author names in one field
    assert {
        "type": "Organization",
        "organization": {
            "name": "Enos, Ryan (Harvard University); Fowler, Anthony (University of Chicago); Vavreck, Lynn (UCLA)",
        },
        "roles": ["Author"],
    } == get_one_author(
        {
            "name": "Enos, Ryan (Harvard University); Fowler, Anthony (University of Chicago); Vavreck, Lynn (UCLA)",
            "affiliations": [],
            "nameIdentifiers": [],
        }
    )
    # 'hyper-authorship'
    assert {
        "type": "Organization",
        "organization": {"name": "ALICE Collaboration"},
        "roles": ["Author"],
    } == get_one_author(
        {
            "name": "ALICE Collaboration",
            "affiliations": [],
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
        "type": "Organization",
        "organization": {"name": "University of California, Santa Barbara"},
        "roles": ["Author"],
    } == get_one_author(author)
    # name with affiliation crossref
    assert {
        "type": "Person",
        "person": {
            "given_name": "Martial",
            "family_name": "Sankar",
            "affiliations": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
        },
        "roles": ["Author"],
    } == get_one_author(
        {
            "given": "Martial",
            "family": "Sankar",
            "sequence": "first",
            "contributorRoles": ["Author"],
            "affiliations": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
        }
    )
    # multiple name_identifier
    assert {
        "type": "Person",
        "person": {
            "given_name": "Thomas",
            "family_name": "Dubos",
            "affiliations": [
                {"name": "École Polytechnique\nLaboratoire de Météorologie Dynamique"}
            ],
        },
        "roles": ["Author"],
    } == get_one_author(
        {
            "name": "Dubos, Thomas",
            "type": "Person",
            "contributorRoles": ["Author"],
            "givenName": "Thomas",
            "familyName": "Dubos",
            "affiliations": [
                "École Polytechnique\nLaboratoire de Météorologie Dynamique"
            ],
            "nameIdentifiers": [
                {
                    "nameIdentifier": "http://isni.org/isni/0000 0003 5752 6882",
                    "nameIdentifierScheme": "ISNI",
                },
            ],
        }
    )
    # only familyName and givenName
    assert {
        "type": "Person",
        "person": {
            "given_name": "Emma",
            "family_name": "Johansson",
        },
        "roles": ["Author"],
    } == get_one_author(
        {
            "givenName": "Emma",
            "familyName": "Johansson",
            "affiliations": [],
            "nameIdentifiers": [],
        }
    )


def test_cleanup_author():
    "cleanup_author"
    assert cleanup_author("John Smith") == "John Smith"
    assert cleanup_author("Smith, John") == "Smith, John"
    assert cleanup_author("Smith, J.") == "Smith, J."
    assert (
        cleanup_author(
            ",FEMTO-ST/AS2M, ENSMM Besan¸con, 24 rue Alain Savary, 25 000 Besanon"
        )
        is None
    )


def test_authors_as_string():
    "authors_as_string"
    authors = [
        {
            "type": "Person",
            "roles": ["Author"],
            "person": {
                "id": "http://orcid.org/0000-0003-0077-4738",
                "given_name": "Matt",
                "family_name": "Jones",
            },
        },
        {
            "type": "Person",
            "roles": ["Author"],
            "person": {
                "id": "http://orcid.org/0000-0002-2192-403X",
                "given_name": "Peter",
                "family_name": "Slaughter",
            },
        },
        {
            "type": "Organization",
            "organization": {"name": "University of California, Santa Barbara"},
        },
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
            "type": "Person",
            "person": {
                "id": "https://orcid.org/0000-0003-0077-4738",
                "given_name": "Matt",
                "family_name": "Jones",
            },
            "roles": ["Author"],
        },
        {
            "type": "Person",
            "person": {"given_name": "Peter", "family_name": "Slaughter"},
            "roles": ["Author"],
        },
        {
            "type": "Organization",
            "organization": {"name": "University of California, Santa Barbara"},
            "roles": ["Author"],
        },
    ] == get_authors(authors)
    authors = [
        {
            "id": "https://orcid.org/0000-0003-0077-4738",
            "name": "Matt Jones",
            "affiliations": [
                {
                    "name": "University of California, Santa Barbara",
                    "id": "https://ror.org/02t274463",
                }
            ],
        }
    ]
    assert [
        {
            "type": "Person",
            "person": {
                "id": "https://orcid.org/0000-0003-0077-4738",
                "given_name": "Matt",
                "family_name": "Jones",
                "affiliations": [
                    {
                        "name": "University of California, Santa Barbara",
                        "id": "https://ror.org/02t274463",
                    }
                ],
            },
            "roles": ["Author"],
        }
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
    assert [
        {
            "name": "University of California, Santa Barbara",
            "id": "https://ror.org/02t274463",
        }
    ] == get_affiliations(
        [
            {
                "name": "University of California, Santa Barbara",
                "id": "https://ror.org/02t274463",
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
    assert False is is_personal_name("Research Graph")
    assert False is is_personal_name("DH Lab")
    assert False is is_personal_name("Make Data Count")
    assert False is is_personal_name("BJPS Reviewers")
