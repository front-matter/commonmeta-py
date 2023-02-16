"""Test utils"""
from os import path
import pytest
from talbot.utils import (
    dict_to_spdx,
    normalize_orcid,
    validate_orcid,
    normalize_id,
    normalize_ids,
    normalize_cc_url,
    from_citeproc,
    find_from_format_by_id,
    find_from_format_by_string,
    from_schema_org,
    from_schema_org_creators,
    pages_as_string,
    subjects_as_string,
    to_citeproc,
    to_ris,
    to_schema_org,
    to_schema_org_container,
    to_schema_org_identifiers,
)
from talbot.base_utils import wrap


def test_dict_to_spdx_id():
    "dict_to_spdx id"
    assert {
        "rights": "Creative Commons Attribution 4.0 International",
        "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
        "rightsIdentifier": "cc-by-4.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    } == dict_to_spdx({"rightsIdentifier": "cc-by-4.0"})


def test_dict_to_spdx_url():
    "dict_to_spdx url"
    assert {
        "rights": "Creative Commons Attribution 4.0 International",
        "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
        "rightsIdentifier": "cc-by-4.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    } == dict_to_spdx(
        {"rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode"}
    )


def test_dict_to_spdx_not_found():
    "dict_to_spdx not found"
    assert {"rightsUri": "info:eu-repo/semantics/openaccess"} == dict_to_spdx(
        {"rightsUri": "info:eu-repo/semantics/openAccess"}
    )


def test_validate_orcid():
    "validate_orcid"
    assert "0000-0002-2590-225X" == validate_orcid(
        "http://orcid.org/0000-0002-2590-225X"
    )
    # orcid https
    assert "0000-0002-2590-225X" == validate_orcid(
        "https://orcid.org/0000-0002-2590-225X"
    )
    # orcid id
    assert "0000-0002-2590-225X" == validate_orcid("0000-0002-2590-225X")
    # orcid www
    assert "0000-0002-2590-225X" == validate_orcid(
        "https://www.orcid.org/0000-0002-2590-225X"
    )
    # orcid with spaces
    assert "0000-0002-1394-3097" == validate_orcid("0000 0002 1394 3097")
    # orcid sandbox
    assert "0000-0002-2590-225X" == validate_orcid(
        "http://sandbox.orcid.org/0000-0002-2590-225X"
    )
    # orcid sandbox https
    assert "0000-0002-2590-225X" == validate_orcid(
        "https://sandbox.orcid.org/0000-0002-2590-225X"
    )
    # orcid wrong id format
    assert None is validate_orcid("0000-0002-1394-309")
    # None
    assert None is validate_orcid(None)


def test_normalize_orcid():
    "normalize_orcid"
    assert "https://orcid.org/0000-0002-2590-225X" == normalize_orcid(
        "http://orcid.org/0000-0002-2590-225X"
    )
    # orcid https
    assert "https://orcid.org/0000-0002-2590-225X" == normalize_orcid(
        "https://orcid.org/0000-0002-2590-225X"
    )
    # orcid id
    assert "https://orcid.org/0000-0002-2590-225X" == normalize_orcid(
        "0000-0002-2590-225X"
    )
    # invalid orcid id
    assert None == normalize_orcid(
        "0002-2590-225X"
    )
    # None
    assert None is normalize_orcid(None)


def test_normalize_id():
    "normalize_id"
    assert "https://doi.org/10.5061/dryad.8515" == normalize_id(
        "10.5061/DRYAD.8515")
    # doi as url
    assert "https://doi.org/10.5061/dryad.8515" == normalize_id(
        "http://dx.doi.org/10.5061/DRYAD.8515"
    )
    # url
    assert "https://blog.datacite.org/eating-your-own-dog-food" == normalize_id(
        "https://blog.datacite.org/eating-your-own-dog-food/"
    )
    # http url
    assert "https://blog.datacite.org/eating-your-own-dog-food" == normalize_id(
        "http://blog.datacite.org/eating-your-own-dog-food/"
    )
    # url with utf-8
    # assert 'http://www.xn--8ws00zhy3a.com/eating-your-own-dog-food' == normalize_id('http://www.詹姆斯.com/eating-your-own-dog-food/')
    # ftp
    assert None is normalize_id(
        "ftp://blog.datacite.org/eating-your-own-dog-food/")
    # invalid url
    assert None is normalize_id("http://")
    # bytes object
    assert "https://blog.datacite.org/eating-your-own-dog-food" == normalize_id(
        b"https://blog.datacite.org/eating-your-own-dog-food/"
    )
    # string
    assert None is normalize_id("eating-your-own-dog-food")
    # filename
    assert None is normalize_id("crossref.xml")
    # sandbox via url
    assert (
        "https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7"
        == normalize_id("https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7")
    )
    # sandbox via options
    assert (
        "https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7"
        == normalize_id("10.20375/0000-0001-ddb8-7", sandbox=True)
    )
    # None
    assert None is normalize_id(None)


def test_normalize_ids():
    "normalize_ids"
    # doi
    ids = [
        {"@type": "CreativeWork", "@id": "https://doi.org/10.5438/0012"},
        {"@type": "CreativeWork", "@id": "https://doi.org/10.5438/55E5-T5C0"},
    ]
    response = [
        {
            "relatedIdentifier": "10.5438/0012",
            "relatedIdentifierType": "DOI",
            "resourceTypeGeneral": "Text",
        },
        {
            "relatedIdentifier": "10.5438/55e5-t5c0",
            "relatedIdentifierType": "DOI",
            "resourceTypeGeneral": "Text",
        },
    ]
    assert response == normalize_ids(ids=ids)
    # url
    ids = [
        {
            "@type": "CreativeWork",
            "@id": "https://blog.datacite.org/eating-your-own-dog-food/",
        }
    ]
    response = [
        {
            "relatedIdentifier": "https://blog.datacite.org/eating-your-own-dog-food",
            "relatedIdentifierType": "URL",
            "resourceTypeGeneral": "Text",
        }
    ]
    assert response == normalize_ids(ids=ids)


def test_normalize_cc_url():
    """normalize_cc_url"""
    assert 'https://creativecommons.org/licenses/by/4.0/legalcode' == normalize_cc_url(
        'https://creativecommons.org/licenses/by/4.0/')
    assert 'https://creativecommons.org/publicdomain/zero/1.0/legalcode' == normalize_cc_url(
        'https://creativecommons.org/publicdomain/zero/1.0')
    # http scheme
    assert 'https://creativecommons.org/publicdomain/zero/1.0/legalcode' == normalize_cc_url(
        'http://creativecommons.org/publicdomain/zero/1.0')
    assert None is normalize_cc_url(None)
    assert None is normalize_cc_url(
        {'url': 'https://creativecommons.org/licenses/by/4.0/legalcode'})


def test_from_citeproc():
    "from_citeproc"
    assert [
        {
            "@type": "Person",
            "affiliation": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
            "familyName": "Sankar",
            "givenName": "Martial",
            "name": "Martial Sankar",
        }
    ] == from_citeproc(
        [
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
        ]
    )
    assert [
        {
            "@type": "Organization",
            "name": "University of Lausanne",
        }
    ] == from_citeproc(
        [
            {
                "literal": "University of Lausanne",
                "sequence": "first",
            }
        ]
    )
    assert [
        {
            "@type": "Organization",
            "name": "University of Lausanne",
        }
    ] == from_citeproc(
        [
            {
                "name": "University of Lausanne",
                "sequence": "first",
            }
        ]
    )


def find_from_format():
    """find_from_format"""


def test_find_from_format_by_id():
    "find_from_format_by_id"
    assert "crossref" == find_from_format_by_id("10.1371/journal.pone.0042793")
    assert "datacite" == find_from_format_by_id(
        "https://doi.org/10.5061/dryad.8515")
    assert "medra" == find_from_format_by_id("10.1392/roma081203")
    assert "kisti" == find_from_format_by_id(
        "https://doi.org/10.5012/bkcs.2013.34.10.2889"
    )
    assert "jalc" == find_from_format_by_id(
        "https://doi.org/10.11367/grsj1979.12.283")
    assert "op" == find_from_format_by_id(
        "https://doi.org/10.2903/j.efsa.2018.5239")
    # cff
    # assert "cff" == find_from_format_by_id(
    #     "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
    # )
    # # cff repository url
    # # assert "cff" == find_from_format_by_id(
    # #    "https://github.com/citation-file-format/ruby-cff"
    # # )
    # # codemeta
    # assert "codemeta" == find_from_format_by_id(
    #     "https://github.com/datacite/maremma/blob/master/codemeta.json"
    # )
    # # npm
    # assert "npm" == find_from_format_by_id(
    #     "https://github.com/datacite/bracco/blob/master/package.json"
    # )
    # # schema_org
    # assert "schema_org" == find_from_format_by_id(
    #     "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GAOC03"
    # )


def test_find_from_format_by_string():
    """find_from_format_by_string"""
    filepath = path.join(path.dirname(__file__), 'fixtures', 'datacite.json')
    with open(filepath, encoding='utf-8') as file:
        string = file.read()
    assert "datacite" == find_from_format_by_string(string)
    assert None is find_from_format_by_string('{"foo": "bar"}')
    assert None is find_from_format_by_string(None)


def test_from_schema_org():
    "from_schema_org"
    author = {
        "@type": "Person",
        "@id": "http://orcid.org/0000-0003-1419-2405",
        "givenName": "Martin",
        "familyName": "Fenner",
        "name": "Martin Fenner",
    }
    assert {
        "givenName": "Martin",
        "familyName": "Fenner",
        "name": "Martin Fenner",
        "type": "Person",
        "id": "http://orcid.org/0000-0003-1419-2405",
    } == from_schema_org(author)


def test_from_schema_org_creators():
    "from_schema_org creators"
    authors = [
        {
            "@type": "Person",
            "@id": "http://orcid.org/0000-0003-1419-2405",
            "givenName": "Martin",
            "familyName": "Fenner",
            "name": "Martin Fenner",
            "affiliation": {
                "@id": "https://ror.org/04wxnsj81",
                "name": "DataCite",
                "@type": "Organization",
            },
        }
    ]
    response = from_schema_org_creators(authors)
    assert response == [{'givenName': 'Martin', 'familyName': 'Fenner', 'affiliation': {'__content__': 'DataCite', 'affiliationIdentifier': 'https://ror.org/04wxnsj81', 'affiliationIdentifierScheme': 'ROR', 'schemeUri': 'https://ror.org/'},
                         'nameIdentifier': [{'__content__': 'http://orcid.org/0000-0003-1419-2405', 'nameIdentifierScheme': 'ORCID', 'schemeUri': 'https://orcid.org'}], 'creatorName': {'nameType': 'Personal', '__content__': 'Martin Fenner'}}]
    # without affiliation
    authors = [
        {
            "@type": "Person",
            "@id": "http://orcid.org/0000-0003-1419-2405",
            "givenName": "Martin",
            "familyName": "Fenner",
            "name": "Martin Fenner",
        }
    ]
    response = from_schema_org_creators(authors)
    assert response == [{'givenName': 'Martin', 'familyName': 'Fenner', 'nameIdentifier': [{'__content__': 'http://orcid.org/0000-0003-1419-2405', 'nameIdentifierScheme': 'ORCID',
                                                                                            'schemeUri': 'https://orcid.org'}], 'creatorName': {'nameType': 'Personal', '__content__': 'Martin Fenner'}}]


def test_pages_as_string():
    """pages as string"""
    container = {
        "firstPage": "2832",
        "identifier": "0012-9658",
        "identifierType": "ISSN",
        "issue": "11",
        "lastPage": "2841",
        "title": "Ecology",
        "type": "Journal",
        "volume": "87",
    }
    assert "2832-2841" == pages_as_string(container)
    container = {
        "type": "Journal",
        "title": "Publications",
        "firstPage": "15",
        "issue": "2",
        "volume": "6",
        "identifier": "2304-6775",
        "identifierType": "ISSN",
    }
    assert "15" == pages_as_string(container)
    assert None is pages_as_string(None)


def test_subjects_as_string():
    """subjects as string"""
    subjects = [
        {"subject": "Ecology", "scheme": "http://id.loc.gov/authorities/subjects"},
        {"subject": "Biodiversity", "scheme": "http://id.loc.gov/authorities/subjects"}
    ]
    assert "Ecology, Biodiversity" == subjects_as_string(subjects)
    assert None is subjects_as_string(None)


def test_to_citeproc():
    """to citeproc"""
    authors = [
        {
            "ORCID": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        }
    ]
    organization_authors = [
        {
            "name": "University of California, Berkeley"
        }

    ]
    assert [{'family': 'Jones', 'given': 'Matt'}] == to_citeproc(authors)
    assert [{'literal': 'University of California, Berkeley'}
            ] == to_citeproc(organization_authors)


def test_to_ris():
    """to ris"""
    authors = [
        {
            "ORCID": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        }
    ]
    organization_authors = [
        {
            "name": "University of California, Berkeley"
        }

    ]
    assert ['Jones, Matt'] == to_ris(authors)
    assert ['University of California, Berkeley'] == to_ris(
        organization_authors)


def test_to_schema_org():
    """to schema.org"""
    author = {
        "id": "http://orcid.org/0000-0003-0077-4738",
        "type": "Person",
        "givenName": "Matt",
        "familyName": "Jones",
    }
    organization_author = {
        "id": "https://ror.org/01an7q238",
        "type": "Organization",
        "name": "University of California, Berkeley"
    }

    assert {'givenName': 'Matt', 'familyName': 'Jones', '@type': 'Person',
            '@id': 'http://orcid.org/0000-0003-0077-4738'} == to_schema_org(author)
    assert {'name': 'University of California, Berkeley', '@type': 'Organization',
            '@id': 'https://ror.org/01an7q238'} == to_schema_org(organization_author)
    assert None is to_schema_org(None)


def test_to_schema_org_container():
    """to schema.org container"""
    pangaea = {
        "identifier": "https://www.pangaea.de/",
        "identifierType": "URL",
        "title": "PANGAEA",
        "type": "DataRepository",
    }
    assert {'@id': 'https://www.pangaea.de/', '@type': 'Periodical',
            'name': 'PANGAEA'} == to_schema_org_container(pangaea)
    assert None is to_schema_org_container("Pangaea")
    assert None is to_schema_org_container(None)


def test_to_schema_org_identifiers():
    """to schema.org identifiers"""
    identifiers = [{
        "identifier": "10.5061/dryad.8515",
        "identifierType": "DOI",
    }]
    assert [{'@type': 'PropertyValue', 'propertyID': 'DOI',
            'value': '10.5061/dryad.8515'}] == to_schema_org_identifiers(identifiers)
    assert [] == to_schema_org_identifiers(wrap(None))
