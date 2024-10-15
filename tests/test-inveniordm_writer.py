# pylint: disable=invalid-name
"""InvenioRDM writer tests"""

import orjson as json
import pytest
from pydash import py_

from commonmeta import Metadata


@pytest.mark.vcr
def test_publication():
    "publication"
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.5281/zenodo.5244404"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-article"
    assert len(py_.get(inveniordm, "metadata.creators")) == 21
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Holmes",
            "given_name": "Edward C",
            "name": "Holmes, Edward C",
            "type": "personal",
        },
        "affiliations": [
            {
                "name": "School of Life and Environmental Sciences and School of Medical Sciences, The University of Sydney, Sydney, NSW 2006, Australia"
            }
        ],
    }
    assert (
        py_.get(inveniordm, "metadata.title")
        == "The Origins of SARS-CoV-2: A Critical Review"
    )
    assert py_.get(inveniordm, "metadata.publisher") == "Zenodo"
    assert py_.get(inveniordm, "metadata.publication_date") == "2021-08-18"
    assert py_.get(inveniordm, "metadata.languages.0.id") is None
    assert py_.get(inveniordm, "metadata.version") == "Authors' final version"
    assert py_.get(inveniordm, "metadata.description").startswith(
        "The Origins of SARS-CoV-2: A Critical Review"
    )
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-nc-nd-4.0"}]
    assert py_.get(inveniordm, "metadata.related_identifiers") == [
        {
            "identifier": "10.5281/zenodo.5075887",
            "relation_type": {"id": "isversionof"},
            "scheme": "doi",
        }
    ]
    assert py_.get(inveniordm, "metadata.funding") is None
    assert py_.get(inveniordm, "files.enabled") == False


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-article"
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.7554/elife.01567"
    assert len(py_.get(inveniordm, "metadata.creators")) == 5
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Sankar",
            "given_name": "Martial",
            "name": "Sankar, Martial",
            "type": "personal",
        },
        "affiliations": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, "
                "Lausanne, Switzerland",
            },
        ],
    }

    assert (
        py_.get(inveniordm, "metadata.title")
        == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert (
        py_.get(inveniordm, "metadata.publisher") == "eLife Sciences Publications, Ltd"
    )
    assert py_.get(inveniordm, "metadata.publication_date") == "2014-02-11"
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "Among various advantages, their small size makes model organisms preferred subjects of investigation."
    )
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-3.0"}]
    related_identifiers = py_.get(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 31
    assert related_identifiers[0] == {
        "identifier": "10.1038/nature02100",
        "relation_type": {
            "id": "references",
        },
        "scheme": "doi",
    }
    assert related_identifiers[27] == {
        "identifier": "10.5061/dryad.b835k",
        "relation_type": {
            "id": "issupplementedby",
        },
        "scheme": "doi",
    }
    assert related_identifiers[28] == {
        "identifier": "10.7554/elife.01567.017",
        "relation_type": {
            "id": "isreviewedby",
        },
        "scheme": "doi",
    }
    assert related_identifiers[30] == {
        "identifier": "2050-084X",
        "relation_type": {
            "id": "ispartof",
        },
        "scheme": "issn",
    }
    assert py_.get(inveniordm, "metadata.funding") == [
        {"funder": {"name": "SystemsX"}},
        {"funder": {"name": "EMBO longterm post-doctoral fellowships"}},
        {"funder": {"name": "Marie Heim-Voegtlin"}},
        {
            "funder": {
                "id": "019whta54",
                "name": "University of Lausanne",
            },
        },
        {
            "funder": {
                "id": "04wfr2810",
                "name": "EMBO",
            },
        },
        {
            "funder": {
                "id": "00yjd3n13",
                "name": "Swiss National Science Foundation",
            },
        },
    ]
    assert py_.get(inveniordm, "files.enabled") == False


@pytest.mark.vcr
def test_rogue_scholar():
    "Rogue Scholar"
    string = "https://beta.rogue-scholar.org/api/records/1xr7q-9fp18"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/dv8z6-a6s33"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.53731/dv8z6-a6s33"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert len(py_.get(inveniordm, "metadata.creators")) == 1
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Fenner",
            "given_name": "Martin",
            "name": "Fenner, Martin",
            "type": "personal",
            "identifiers": [{"identifier": "0000-0003-1419-2405", "scheme": "orcid"}],
        }
    }
    assert (
        py_.get(inveniordm, "metadata.title")
        == "Rogue Scholar learns about communities"
    )
    assert py_.get(inveniordm, "metadata.publisher") is None
    assert py_.get(inveniordm, "metadata.publication_date") == "2024-10-07"

    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2024-10-08T11:51:22Z", "type": {"id": "updated"}}
    ]
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "The Rogue Scholar infrastructure started migrating to InvenioRDM infrastructure a few weeks ago."
    )
    assert py_.get(inveniordm, "metadata.subjects") is None
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    assert py_.get(inveniordm, "metadata.related_identifiers") is None
    assert py_.get(inveniordm, "metadata.funding") is None
    assert py_.get(inveniordm, "files.enabled") == False
    assert py_.get(inveniordm, "custom_fields.journal:journal.title") == "Front Matter"
    assert py_.get(inveniordm, "custom_fields.journal:journal.issn") == "2749-9952"


@pytest.mark.vcr
def test_from_json_feed():
    "JSON Feed"
    string = "https://api.rogue-scholar.org/posts/525a7d13-fe07-4cab-ac54-75d7b7005647"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/dn2mm-m9q51"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/dn2mm-m9q51"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert len(py_.get(inveniordm, "metadata.creators")) == 1
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Dingemanse",
            "given_name": "Mark",
            "name": "Dingemanse, Mark",
            "type": "personal",
        },
    }
    assert py_.get(inveniordm, "metadata.title") == "Linguistic roots of connectionism"
    assert py_.get(inveniordm, "metadata.publication_date") == "2021-07-22"
    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2024-02-04T22:05:36", "type": {"id": "updated"}}
    ]
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.identifiers") == [
        {"identifier": "525a7d13-fe07-4cab-ac54-75d7b7005647", "scheme": "other"}
    ]
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "This Lingbuzz preprint by Baroni is a nice read"
    )
    assert py_.get(inveniordm, "metadata.subjects") == [
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?6.2",
            "subject": "Languages and literature",
        },
        {"subject": "Linguistics"},
        {"subject": "Threads"},
    ]
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    assert py_.get(inveniordm, "metadata.related_identifiers") is None
    assert py_.get(inveniordm, "metadata.related_identifiers") is None
    assert py_.get(inveniordm, "files.enabled") == False
    assert py_.get(inveniordm, "custom_fields.journal:journal.title") == "The Ideophone"
    assert py_.get(inveniordm, "custom_fields.journal:journal.issn") is None


@pytest.mark.vcr
def test_from_json_feed_affiliations():
    "JSON Feed affiliations"
    string = "https://api.rogue-scholar.org/posts/10.59350/mg09a-5ma64"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/mg09a-5ma64"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/mg09a-5ma64"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert len(py_.get(inveniordm, "metadata.creators")) == 4
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Beucke",
            "given_name": "Daniel",
            "name": "Beucke, Daniel",
            "type": "personal",
            "identifiers": [{"identifier": "0000-0003-4905-1936", "scheme": "orcid"}],
        },
        "affiliations": [
            {
                "id": "05745n787",
                "name": "Göttingen State and University Library",
            },
        ],
    }
    assert (
        py_.get(inveniordm, "metadata.title")
        == "Report on the Hands-On Lab ‘Scenarios for the Development of Open Access Repositories’ at the 112th BiblioCon"
    )
    assert py_.get(inveniordm, "metadata.publication_date") == "2024-07-15"
    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2024-07-15T00:00:00", "type": {"id": "updated"}}
    ]
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.identifiers") == [
        {"identifier": "6d1feb10-057a-4fc2-acb0-ac95e19741af", "scheme": "other"}
    ]
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "In the beginning of June 2024,"
    )
    assert py_.get(inveniordm, "metadata.subjects") == [
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?1.2",
            "subject": "Computer and information sciences",
        },
        {"subject": "Lab Life"},
        {"subject": "Research"},
    ]
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    assert py_.get(inveniordm, "metadata.related_identifiers") is None
    assert py_.get(inveniordm, "metadata.related_identifiers") is None
    assert py_.get(inveniordm, "files.enabled") == False
    assert (
        py_.get(inveniordm, "custom_fields.journal:journal.title")
        == "Research Group Information Management @ Humboldt-Universität zu Berlin"
    )
    assert py_.get(inveniordm, "custom_fields.journal:journal.issn") is None


@pytest.mark.vcr
def test_from_json_feed_dates():
    "JSON Feed dates"
    string = "https://api.rogue-scholar.org/posts/10.59350/k9zxj-pek64"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/k9zxj-pek64"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/k9zxj-pek64"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert py_.get(inveniordm, "metadata.publication_date") == "2018-08-28"
    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2018-10-19T23:13:05", "type": {"id": "updated"}}
    ]


@pytest.mark.vcr
def test_from_json_feed_funding():
    "JSON Feed funding"
    string = "https://api.rogue-scholar.org/posts/10.59350/hnegw-6rx17"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/hnegw-6rx17"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/hnegw-6rx17"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert py_.get(inveniordm, "metadata.title") == "THOR Final Event programme is out!"
    assert py_.get(inveniordm, "metadata.funding") == [
        {
            "award": [{"number": "654039"}],
            "funder": {
                "id": "00k4n6c32",
                "name": "European Union’s Horizon 2020 research and innovation programme",
            },
        }
    ]


@pytest.mark.vcr
def test_from_json_feed_more_funding():
    "JSON Feed more funding"
    string = "https://api.rogue-scholar.org/posts/10.59350/m99dx-x9g53"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/m99dx-x9g53"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/m99dx-x9g53"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert (
        py_.get(inveniordm, "metadata.title") == "Summer Meeting of the Editorial Board"
    )
    assert py_.get(inveniordm, "metadata.funding") == [
        {
            "award": [{"number": "422587133"}],
            "funder": {
                "id": "018mejw64",
                "name": "Deutsche Forschungsgemeinschaft",
            },
        }
    ]
