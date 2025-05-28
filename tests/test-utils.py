# pylint: disable=invalid-name
"""Test utils"""

from os import path

import pytest  # noqa: F401

from commonmeta.base_utils import wrap
from commonmeta.utils import (
    dict_to_spdx,
    extract_curie,
    extract_urls,
    find_from_format_by_ext,
    find_from_format_by_filename,
    find_from_format_by_id,
    find_from_format_by_string,
    format_name_identifier,
    from_csl,
    from_curie,
    from_schema_org,
    from_schema_org_creators,
    get_language,
    github_as_cff_url,
    github_as_codemeta_url,
    github_as_repo_url,
    github_from_url,
    id_from_url,
    issn_as_url,
    issn_from_url,
    normalize_cc_url,
    normalize_id,
    normalize_ids,
    normalize_isni,
    normalize_issn,
    normalize_orcid,
    normalize_ror,
    normalize_url,
    openalex_api_query_url,
    pages_as_string,
    replace_curie,
    string_to_slug,
    subjects_as_string,
    to_csl,
    to_ris,
    to_schema_org,
    to_schema_org_container,
    to_schema_org_creators,
    to_schema_org_identifiers,
    validate_id,
    validate_isni,
    validate_mag,
    validate_openalex,
    validate_orcid,
    validate_pmcid,
    validate_pmid,
    validate_ror,
    validate_url,
)


def test_dict_to_spdx_id():
    "dict_to_spdx id"
    assert {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    } == dict_to_spdx({"id": "CC-BY-4.0"})
    assert {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    } == dict_to_spdx({"id": "cc-by-4.0"})
    assert {
        "id": "Apache-2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0",
    } == dict_to_spdx({"id": "Apache-2.0"})


def test_dict_to_spdx_url():
    "dict_to_spdx url"
    assert {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    } == dict_to_spdx({"url": "https://creativecommons.org/licenses/by/4.0/legalcode"})


def test_dict_to_spdx_not_found():
    "dict_to_spdx not found"
    assert {} == dict_to_spdx({"url": "info:eu-repo/semantics/openAccess"})


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


def test_validate_ror():
    "validate_ror"
    assert "0342dzm54" == validate_ror("https://ror.org/0342dzm54")
    assert "0342dzm54" == validate_ror("0342dzm54")
    # None
    assert None is validate_ror(None)


def test_validate_openalex():
    "validate_openalex"
    assert "W2121398592" == validate_openalex("https://openalex.org/W2121398592")
    # None
    assert None is validate_openalex(None)


def test_validate_pmid():
    "validate_pmid"
    assert "24520159" == validate_pmid("https://pubmed.ncbi.nlm.nih.gov/24520159")
    # None
    assert None is validate_pmid(None)


def test_validate_pmcid():
    "validate_pmcid"
    assert "3917233" == validate_pmcid(
        "https://www.ncbi.nlm.nih.gov/pmc/articles/3917233"
    )
    # None
    assert None is validate_pmcid(None)


def test_validate_mag():
    "validate_mag"
    assert "2121398592" == validate_mag("2121398592")
    # None
    assert None is validate_mag(None)


def test_validate_isni():
    "validate_isni"
    assert "0000000357526882" == validate_isni("https://isni.org/isni/0000000357526882")
    # http
    assert "0000000357526882" == validate_isni("http://isni.org/isni/0000000357526882")
    # only isni id
    assert "0000000357526882" == validate_isni("0000000357526882")
    # None
    assert None is validate_isni(None)


def test_validate_id():
    "validate_id"
    assert ("10.5061/dryad.8515", "DOI") == validate_id(
        "https://doi.org/10.5061/dryad.8515"
    )
    assert ("0000000357526882", "ISNI") == validate_id(
        "https://isni.org/isni/0000000357526882"
    )
    assert ("W2121398592", "OpenAlex") == validate_id(
        "https://openalex.org/W2121398592"
    )
    assert ("0000-0002-2590-225X", "ORCID") == validate_id(
        "http://orcid.org/0000-0002-2590-225X"
    )
    assert ("24520159", "PMID") == validate_id(
        "https://pubmed.ncbi.nlm.nih.gov/24520159"
    )
    assert (
        "3917233",
        "PMCID",
    ) == validate_id("https://www.ncbi.nlm.nih.gov/pmc/articles/3917233")
    assert ("0342dzm54", "ROR") == validate_id("https://ror.org/0342dzm54")
    assert ("http://blog.datacite.org/eating-your-own-dog-food/", "URL") == validate_id(
        "http://blog.datacite.org/eating-your-own-dog-food/"
    )


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
    assert None is normalize_orcid("0002-2590-225X")
    # None
    assert None is normalize_orcid(None)


def test_normalize_ror():
    "normalize_ror"
    assert "https://ror.org/0342dzm54" == normalize_ror("http://ror.org/0342dzm54")


def test_normalize_isni():
    "normalize_isni"
    assert "https://isni.org/isni/0000000357526882" == normalize_isni(
        "http://isni.org/isni/0000 0003 5752 6882"
    )


def test_normalize_id():
    "normalize_id"
    assert "https://doi.org/10.5061/dryad.8515" == normalize_id("10.5061/DRYAD.8515")
    # doi as url
    assert "https://doi.org/10.5061/dryad.8515" == normalize_id(
        "http://dx.doi.org/10.5061/DRYAD.8515"
    )
    # url
    assert "https://blog.datacite.org/eating-your-own-dog-food/" == normalize_id(
        "https://blog.datacite.org/eating-your-own-dog-food/"
    )
    # cff url
    assert (
        "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
        == normalize_id(
            "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
        )
    )
    # codemeta url
    assert (
        "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
        == normalize_id(
            "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
        )
    )
    # http url
    assert "https://blog.datacite.org/eating-your-own-dog-food/" == normalize_id(
        "http://blog.datacite.org/eating-your-own-dog-food/"
    )
    # url with utf-8
    # assert 'http://www.xn--8ws00zhy3a.com/eating-your-own-dog-food' == normalize_id('http://www.詹姆斯.com/eating-your-own-dog-food/')
    # ftp
    assert None is normalize_id("ftp://blog.datacite.org/eating-your-own-dog-food/")
    # invalid url
    assert None is normalize_id("http://")
    # bytes object
    assert "https://blog.datacite.org/eating-your-own-dog-food/" == normalize_id(
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
        {"type": "CreativeWork", "id": "https://doi.org/10.5438/0012"},
        {"type": "CreativeWork", "id": "https://doi.org/10.5438/55E5-T5C0"},
    ]
    response = [
        {
            "relatedIdentifier": "10.5438/0012",
            "relatedIdentifierType": "DOI",
        },
        {
            "relatedIdentifier": "10.5438/55e5-t5c0",
            "relatedIdentifierType": "DOI",
        },
    ]
    assert response == normalize_ids(ids=ids)
    # url
    ids = [
        {
            "type": "CreativeWork",
            "id": "https://blog.datacite.org/eating-your-own-dog-food/",
        }
    ]
    response = [
        {
            "relatedIdentifier": "https://blog.datacite.org/eating-your-own-dog-food/",
            "relatedIdentifierType": "URL",
        }
    ]
    assert response == normalize_ids(ids=ids)


def test_normalize_cc_url():
    """normalize_cc_url"""
    assert "https://creativecommons.org/licenses/by/4.0/legalcode" == normalize_cc_url(
        "https://creativecommons.org/licenses/by/4.0/"
    )
    assert (
        "https://creativecommons.org/publicdomain/zero/1.0/legalcode"
        == normalize_cc_url("https://creativecommons.org/publicdomain/zero/1.0/")
    )
    # http scheme
    assert (
        "https://creativecommons.org/publicdomain/zero/1.0/legalcode"
        == normalize_cc_url("http://creativecommons.org/publicdomain/zero/1.0/")
    )
    assert None is normalize_cc_url(None)
    assert None is normalize_cc_url(
        {"url": "https://creativecommons.org/licenses/by/4.0/legalcode"}
    )


def test_normalize_issn():
    """normalize_issn"""
    # from list
    string = [
        {"media_type": "print", "#text": "13040855"},
        {"media_type": "electronic", "#text": "21468427"},
    ]
    assert "2146-8427" == normalize_issn(string)
    # from empty list
    string = []
    assert None is normalize_issn(string)
    # from dict
    string = {"media_type": "electronic", "#text": "21468427"}
    assert "2146-8427" == normalize_issn(string)
    # from string
    string = "2146-8427"
    assert "2146-8427" == normalize_issn(string)


def test_issn_as_url():
    """issn as url"""
    assert "https://portal.issn.org/resource/ISSN/2146-8427" == issn_as_url("2146-8427")
    assert None is issn_as_url("10.5438/0012")


def test_issn_from_url():
    """issn from url"""
    assert "2146-8427" == issn_from_url(
        "https://portal.issn.org/resource/ISSN/2146-8427"
    )
    assert None is issn_from_url("https://doi.org/10.5438/0012")


def test_normalize_url():
    """normalize url"""
    # invalid scheme
    assert normalize_url("%0ahttps:/doi.org/10.48550/arxiv.2405.08841") is None
    assert normalize_url("mailto:info@example.org") is None


def test_from_csl():
    "from_csl"
    assert [
        {
            "type": "Person",
            "affiliation": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
            "familyName": "Sankar",
            "givenName": "Martial",
            "name": "Martial Sankar",
        }
    ] == from_csl(
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
            "type": "Organization",
            "name": "University of Lausanne",
        }
    ] == from_csl(
        [
            {
                "literal": "University of Lausanne",
                "sequence": "first",
            }
        ]
    )
    assert [
        {
            "type": "Organization",
            "name": "University of Lausanne",
        }
    ] == from_csl(
        [
            {
                "name": "University of Lausanne",
                "sequence": "first",
            }
        ]
    )
    assert [
        {
            "affiliation": [],
            "familyName": "Dana Gertrud Schabo",
            "name": " Dana Gertrud Schabo",
            "type": "Person",
        }
    ] == from_csl(
        [
            {
                "family": "Dana Gertrud Schabo",
                "sequence": "first",
                "affiliation": [],
                "type": "Person",
            }
        ]
    )


def find_from_format():
    """find_from_format"""


def test_find_from_format_by_id():
    "find_from_format_by_id"
    assert "crossref" == find_from_format_by_id("10.1371/journal.pone.0042793")
    assert "datacite" == find_from_format_by_id("https://doi.org/10.5061/dryad.8515")
    assert "medra" == find_from_format_by_id("10.1392/roma081203")
    assert "kisti" == find_from_format_by_id(
        "https://doi.org/10.5012/bkcs.2013.34.10.2889"
    )
    assert "jalc" == find_from_format_by_id("https://doi.org/10.11367/grsj1979.12.283")
    assert "op" == find_from_format_by_id("https://doi.org/10.2903/j.efsa.2018.5239")
    # cff
    assert "cff" == find_from_format_by_id(
        "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
    )
    # codemeta
    assert "codemeta" == find_from_format_by_id(
        "https://github.com/datacite/maremma/blob/master/codemeta.json"
    )
    # schema_org
    assert "schema_org" == find_from_format_by_id(
        "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GAOC03"
    )
    # json_feed
    assert "jsonfeed" == find_from_format_by_id(
        "https://api.rogue-scholar.org/posts/c3095752-2af0-40a4-a229-3ceb7424bce2"
    )  # noqa: E501


def test_find_from_format_by_filename():
    """find_from_format_by_filename"""
    assert "cff" == find_from_format_by_filename("CITATION.cff")
    assert None is find_from_format_by_filename("text.docx")


def test_find_from_format_by_ext():
    """find_from_format_by_ext"""
    assert "bibtex" == find_from_format_by_ext(".bib")
    assert "ris" == find_from_format_by_ext(".ris")
    assert None is find_from_format_by_ext(".docx")


def test_find_from_format_by_string():
    """find_from_format_by_string"""
    # commonmeta
    filepath = path.join(path.dirname(__file__), "fixtures", "commonmeta.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "commonmeta" == find_from_format_by_string(string)
    # jsonfeed
    filepath = path.join(path.dirname(__file__), "fixtures", "json_feed_item.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "jsonfeed" == find_from_format_by_string(string)
    # datacite
    filepath = path.join(path.dirname(__file__), "fixtures", "datacite.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "datacite" == find_from_format_by_string(string)
    # crossref
    filepath = path.join(path.dirname(__file__), "fixtures", "crossref.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "crossref" == find_from_format_by_string(string)
    # schema_org
    filepath = path.join(path.dirname(__file__), "fixtures", "schema_org_topmed.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "schema_org" == find_from_format_by_string(string)
    # datacite_xml
    filepath = path.join(path.dirname(__file__), "fixtures", "datacite_dataset.xml")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "datacite_xml" == find_from_format_by_string(string)
    # crossref_xml
    filepath = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "crossref_xml" == find_from_format_by_string(string)
    # ris
    filepath = path.join(path.dirname(__file__), "fixtures", "crossref.ris")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "ris" == find_from_format_by_string(string)
    # bibtex
    filepath = path.join(path.dirname(__file__), "fixtures", "pure.bib")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "bibtex" == find_from_format_by_string(string)
    # cff
    filepath = path.join(path.dirname(__file__), "fixtures", "CITATION.cff")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "cff" == find_from_format_by_string(string)
    # codemeta
    filepath = path.join(path.dirname(__file__), "fixtures", "codemeta_v2.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "codemeta" == find_from_format_by_string(string)
    # csl
    filepath = path.join(path.dirname(__file__), "fixtures", "citeproc.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "csl" == find_from_format_by_string(string)
    filepath = path.join(path.dirname(__file__), "fixtures", "json_feed.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "jsonfeed" == find_from_format_by_string(string)
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
    assert response == [
        {
            "id": "http://orcid.org/0000-0003-1419-2405",
            "type": "Person",
            "givenName": "Martin",
            "familyName": "Fenner",
            "affiliation": {
                "id": "https://ror.org/04wxnsj81",
                "type": "Organization",
                "name": "DataCite",
            },
        }
    ]
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
    assert response == [
        {
            "givenName": "Martin",
            "familyName": "Fenner",
            "id": "http://orcid.org/0000-0003-1419-2405",
            "type": "Person",
        }
    ]


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
        {"subject": "Biodiversity", "scheme": "http://id.loc.gov/authorities/subjects"},
    ]
    assert "Ecology, Biodiversity" == subjects_as_string(subjects)
    assert None is subjects_as_string(None)


def test_to_csl():
    """to csl"""
    authors = [
        {
            "ORCID": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        }
    ]
    organization_authors = [{"name": "University of California, Berkeley"}]
    assert [{"family": "Jones", "given": "Matt"}] == to_csl(authors)
    assert [{"literal": "University of California, Berkeley"}] == to_csl(
        organization_authors
    )


def test_to_ris():
    """to ris"""
    authors = [
        {
            "ORCID": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        }
    ]
    organization_authors = [{"name": "University of California, Berkeley"}]
    assert ["Jones, Matt"] == to_ris(authors)
    assert ["University of California, Berkeley"] == to_ris(organization_authors)
    assert [] == to_ris(None)


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
        "name": "University of California, Berkeley",
    }

    assert {
        "givenName": "Matt",
        "familyName": "Jones",
        "@type": "Person",
        "@id": "http://orcid.org/0000-0003-0077-4738",
    } == to_schema_org(author)
    assert {
        "name": "University of California, Berkeley",
        "@type": "Organization",
        "@id": "https://ror.org/01an7q238",
    } == to_schema_org(organization_author)
    assert None is to_schema_org(None)


def test_to_schema_org_container():
    """to schema.org container"""
    pangaea = {
        "identifier": "https://www.pangaea.de/",
        "identifierType": "URL",
        "title": "PANGAEA",
        "type": "DataRepository",
    }
    assert {
        "@id": "https://www.pangaea.de/",
        "@type": "Periodical",
        "name": "PANGAEA",
    } == to_schema_org_container(pangaea)
    assert None is to_schema_org_container("Pangaea")
    assert None is to_schema_org_container(None)


def test_to_schema_org_creators():
    """to schema.org creators"""
    authors = [{"givenName": "Matt", "familyName": "Jones", "type": "Person"}]
    organization_authors = [{"name": "University of California, Berkeley"}]
    assert [
        {
            "givenName": "Matt",
            "familyName": "Jones",
            "name": "Matt Jones",
            "@type": "Person",
        }
    ] == to_schema_org_creators(authors)
    assert [
        {"name": "University of California, Berkeley", "@type": "Organization"}
    ] == to_schema_org_creators(organization_authors)


def test_to_schema_org_identifiers():
    """to schema.org identifiers"""
    identifiers = [
        {
            "identifier": "10.5061/dryad.8515",
            "identifierType": "DOI",
        }
    ]
    assert [
        {"@type": "PropertyValue", "propertyID": "DOI", "value": "10.5061/dryad.8515"}
    ] == to_schema_org_identifiers(identifiers)
    assert [] == to_schema_org_identifiers(wrap(None))


def test_github_from_url():
    """github from url"""
    url = "https://github.com/datacite/bolognese"
    response = github_from_url(url)
    assert response == {"owner": "datacite", "repo": "bolognese"}
    # organization
    url = "https://github.com/datacite"
    response = github_from_url(url)
    assert response == {"owner": "datacite"}
    # not a repo
    url = "https://docs.github.com/en/get-started"
    assert {} == github_from_url(url)
    # codemeta file
    url = "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
    response = github_from_url(url)
    assert response == {
        "owner": "datacite",
        "repo": "metadata-reports",
        "release": "master",
        "path": "software/codemeta.json",
    }
    # cff file
    url = "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
    response = github_from_url(url)
    assert response == {
        "owner": "citation-file-format",
        "repo": "ruby-cff",
        "release": "main",
        "path": "CITATION.cff",
    }
    # branch
    url = "https://github.com/front-matter/Headline/tree/schlagzeile"
    response = github_from_url(url)
    assert response == {
        "owner": "front-matter",
        "repo": "Headline",
        "release": "schlagzeile",
    }


def test_github_as_codemeta_url():
    """github as codemeta url"""
    url = "https://github.com/datacite/bolognese"
    response = github_as_codemeta_url(url)
    assert (
        response
        == "https://raw.githubusercontent.com/datacite/bolognese/master/codemeta.json"
    )


def test_github_as_cff_url():
    """github as cff url"""
    url = "https://github.com/citation-file-format/ruby-cff"
    response = github_as_cff_url(url)
    assert (
        response
        == "https://raw.githubusercontent.com/citation-file-format/ruby-cff/main/CITATION.cff"
    )


def test_github_as_codemeta_url_file():
    """github as codemeta url file"""
    url = "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
    response = github_as_codemeta_url(url)
    assert (
        response
        == "https://raw.githubusercontent.com/datacite/metadata-reports/master/software/codemeta.json"
    )


def test_github_as_repo_url():
    """github as repo url"""
    # codemeta.json
    url = "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
    response = github_as_repo_url(url)
    assert response == "https://github.com/datacite/metadata-reports"
    # CITATION.cff
    url = "https://raw.githubusercontent.com/citation-file-format/ruby-cff/main/CITATION.cff"
    response = github_as_repo_url(url)
    assert response == "https://github.com/citation-file-format/ruby-cff"
    # any other file
    url = "https://github.com/mkdocs/mkdocs/blob/master/mkdocs/localization.py"
    response = github_as_repo_url(url)
    assert response == "https://github.com/mkdocs/mkdocs"
    # github repo url
    url = "https://github.com/datacite/metadata-reports"
    response = github_as_repo_url(url)
    assert response == "https://github.com/datacite/metadata-reports"


def test_from_curie():
    """from_curie"""
    assert "https://doi.org/10.6084/m9.figshare.12644018.v3" == from_curie(
        "DOI:10.6084/m9.figshare.12644018.v3"
    )
    assert "https://doi.org/10.1080/02724634.2016.1111898" == from_curie(
        "doi:10.1080/02724634.2016.1111898"
    )
    assert "https://ror.org/01znn6x10" == from_curie("ROR:01znn6x10")
    assert "https://orcid.org/0000-0001-8522-7682" == from_curie(
        "ORCID:0000-0001-8522-7682"
    )
    assert "https://isni.org/isni/0000000121099845" == from_curie(
        "ISNI:0000000121099845"
    )


def test_extract_curie():
    """extract_curie"""
    string = """Melstrom, Keegan M., Michael D. D’Emic, Daniel Chure and Jeffrey A.
Wilson. 2016. A juvenile sauropod dinosaur from the Late Jurassic of
Utah, USA, presents further evidence of an avian style air-sac
system. Journal of Vertebrate Paleontology 36(4):e1111898.
doi:10.1080/02724634.2016.1111898"""
    assert "https://doi.org/10.1080/02724634.2016.1111898" == extract_curie(string)


def test_extract_curie_doi_space():
    """extract_curie doi with space"""
    string = """Melstrom, Keegan M., Michael D. D’Emic, Daniel Chure and Jeffrey A.
Wilson. 2016. A juvenile sauropod dinosaur from the Late Jurassic of
Utah, USA, presents further evidence of an avian style air-sac
system. Journal of Vertebrate Paleontology 36(4):e1111898.
DOI: 10.1080/02724634.2016.1111898"""
    assert "https://doi.org/10.1080/02724634.2016.1111898" == extract_curie(string)


def test_replace_curie():
    """replace_curie"""
    string = """Melstrom, Keegan M., Michael D. D’Emic, Daniel Chure and Jeffrey A.
Wilson. 2016. A juvenile sauropod dinosaur from the Late Jurassic of
Utah, USA, presents further evidence of an avian style air-sac
system. Journal of Vertebrate Paleontology 36(4):e1111898. doi:10.1080/02724634.2016.1111898"""
    assert """Melstrom, Keegan M., Michael D. D’Emic, Daniel Chure and Jeffrey A.
Wilson. 2016. A juvenile sauropod dinosaur from the Late Jurassic of
Utah, USA, presents further evidence of an avian style air-sac
system. Journal of Vertebrate Paleontology 36(4):e1111898. https://doi.org/10.1080/02724634.2016.1111898""" == replace_curie(
        string
    )


def test_extract_urls():
    """extract_urls"""
    string = """Zauner, H. (2025, January 9). Sex chromosome madness in the iconic echidna. GigaBlog. https://doi.org/10.59350/9509z-ns663

Willighagen, E. (2024, December 30). FAIR blog-to-blog citations. Chem-Bla-Ics. https://doi.org/10.59350/er1mn-m5q69

Marcum, C. S. (2024, August 27). Drinking from the Firehose? Write More and Publish Less. Upstream. https://doi.org/10.54900/r8zwg-62003"""
    assert [
        "https://doi.org/10.59350/9509z-ns663",
        "https://doi.org/10.59350/er1mn-m5q69",
        "https://doi.org/10.54900/r8zwg-62003",
    ] == extract_urls(string)


def test_extract_urls_markdown():
    """extract_urls markdown"""
    string = """Zauner, H. (2025, January 9). Sex chromosome madness in the iconic
echidna. *GigaBlog*. <https://doi.org/10.59350/9509z-ns663>

Willighagen, E. (2024, December 30). FAIR blog-to-blog citations.
*Chem-Bla-Ics*. <https://doi.org/10.59350/er1mn-m5q69>

Marcum, C. S. (2024, August 27). Drinking from the Firehose? Write More
and Publish Less. *Upstream*. <https://doi.org/10.54900/r8zwg-62003>"""
    assert [
        "https://doi.org/10.59350/9509z-ns663",
        "https://doi.org/10.59350/er1mn-m5q69",
        "https://doi.org/10.54900/r8zwg-62003",
    ] == extract_urls(string)


def test_extract_urls_html():
    """extract_urls html"""
    string = """<p>Zauner, H. (2025, January 9). Sex chromosome madness in the iconic echidna. <em>GigaBlog</em>. <a href="https://doi.org/10.59350/9509z-ns663">https://doi.org/10.59350/9509z-ns663</a></p><p>Willighagen, E. (2024, December 30). FAIR blog-to-blog citations. <em>Chem-Bla-Ics</em>. <a href="https://doi.org/10.59350/er1mn-m5q69">https://doi.org/10.59350/er1mn-m5q69</a></p><p>Marcum, C. S. (2024, August 27). Drinking from the Firehose? Write More and Publish Less. <em>Upstream</em>. <a href="https://doi.org/10.54900/r8zwg-62003">https://doi.org/10.54900/r8zwg-62003</a></p>"""
    assert [
        "https://doi.org/10.59350/9509z-ns663",
        "https://doi.org/10.59350/er1mn-m5q69",
        "https://doi.org/10.54900/r8zwg-62003",
    ] == extract_urls(string)


def test_id_from_url():
    """test_id_from_url"""
    assert "10.6084/m9.figshare.12644018.v3" == id_from_url(
        "https://doi.org/10.6084/m9.figshare.12644018.v3"
    )
    assert "01znn6x10" == id_from_url("https://ror.org/01znn6x10")
    assert "0000-0001-8522-7682" == id_from_url("https://orcid.org/0000-0001-8522-7682")


def test_get_language():
    """Get language from string"""
    assert "English" == get_language("en", format="name")
    assert "Danish" == get_language("dan", format="name")
    assert "eng" == get_language("English", format="alpha_3")
    assert "en" == get_language("English", format="alpha_2")
    assert "en" == get_language("English")
    assert None is get_language("xyz")
    assert "tlh" == get_language("Klingon", format="alpha_3")


def test_validate_url():
    """Check whether URL is DOI, URL or ISSN"""
    assert "DOI" == validate_url("https://doi.org/10.5438/0000-00ss")
    assert "URL" == validate_url("https://blog.datacite.org/eating-your-own-dog-food")
    assert "ISSN" == validate_url("ISSN 2050-084X")
    assert None is validate_url("eating-your-own-dog-food")


def test_openalex_api_query_url():
    """Construct OpenAlex Query URL"""

    # Default case
    query = {}
    url = openalex_api_query_url(query)
    assert (
        url
        == "https://api.openalex.org/works?per-page=10&page=1&sort=publication_date%3Adesc"
    )

    # Custom number and page
    query = {"number": 100, "page": 3}
    url = openalex_api_query_url(query)
    assert (
        url
        == "https://api.openalex.org/works?per-page=100&page=3&sort=publication_date%3Adesc"
    )

    # Basic sample
    query = {"sample": True}
    url = openalex_api_query_url(query)
    assert url == "https://api.openalex.org/works?sample=10"

    # Sample with custom number
    query = {"sample": True, "number": 120}
    url = openalex_api_query_url(query)
    assert url == "https://api.openalex.org/works?sample=120"

    # Sample with ORCID
    query = {"sample": True, "orcid": "0000-0002-8635-8390"}
    url = openalex_api_query_url(query)
    assert (
        url
        == "https://api.openalex.org/works?sample=10&filter=authorships.author.orcid%3A0000-0002-8635-8390"
    )

    # Sample with ROR
    query = {"sample": True, "ror": "041kmwe10"}
    url = openalex_api_query_url(query)
    assert (
        url
        == "https://api.openalex.org/works?sample=10&filter=authorships.institutions.ror%3A041kmwe10"
    )


def test_format_name_identifier():
    """Format name identifier"""
    assert "https://orcid.org/0000-0003-0077-4738" == format_name_identifier(
        {
            "nameIdentifier": "0000-0003-0077-4738",
            "nameIdentifierScheme": "ORCID",
        }
    )
    assert "https://ror.org/02t274463" == format_name_identifier(
        {
            "nameIdentifier": "02t274463",
            "nameIdentifierScheme": "ROR",
            "schemeURI": "https://ror.org/",
        }
    )
    assert "https://isni.org/isni/0000000110230567" == format_name_identifier(
        {
            "nameIdentifier": "0000000110230567",
            "nameIdentifierScheme": "ISNI",
        }
    )
    assert "https://isni.org/isni/0000000110230567" == format_name_identifier(
        "0000000110230567"
    )
    assert "https://isni.org/isni/0000000110230567" == format_name_identifier(
        {
            "nameIdentifier": "0000000110230567",
            "nameIdentifierScheme": "ISNI",
            "schemeURI": "http://isni.org/isni/",
        }
    )
    assert "https://www.wikidata.org/wiki/Q107529885" == format_name_identifier(
        {
            "schemeUri": "https://www.wikidata.org/wiki/",
            "nameIdentifier": "Q107529885",
            "nameIdentifierScheme": "Wikidata",
        }
    )
    assert "https://ror.org/04z8jg394" == format_name_identifier(
        {
            "lang": "en",
            "name": "Example Publisher",
            "schemeUri": "https://ror.org/",
            "publisherIdentifier": "https://ror.org/04z8jg394",
            "publisherIdentifierScheme": "ROR",
        }
    )

def test_string_to_slug():
    """string_to_slug"""
    assert string_to_slug("Legal Helpdesk") == "legal-helpdesk"
    assert string_to_slug("FOS: Law") == "law"
