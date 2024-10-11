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
            "affiliation": [
                {
                    "name": "School of Life and Environmental Sciences and School of Medical Sciences, The University of Sydney, Sydney, NSW 2006, Australia"
                }
            ],
            "family_name": "Holmes",
            "given_name": "Edward C",
            "name": "Holmes, Edward C",
            "type": "personal",
        }
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
    assert py_.get(inveniordm, "files.enabled") == True


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
            "affiliation": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
            "family_name": "Sankar",
            "given_name": "Martial",
            "name": "Sankar, Martial",
            "type": "personal",
        }
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
    assert py_.get(inveniordm, "files.enabled") == True


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
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    assert py_.get(inveniordm, "files.enabled") == True
    assert py_.get(inveniordm, "custom_fields.journal:journal.title") == "Front Matter"
    assert py_.get(inveniordm, "custom_fields.journal:journal.issn") == "2749-9952"


@pytest.mark.vcr
def test_from_json_feed():
    "JSON Feed"
    string = "https://api.rogue-scholar.org/posts/9e24e4be-1915-48cc-a6b0-c23da5bc2857"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/ewrv712-2k7rx6d"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.53731/ewrv712-2k7rx6d"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert len(py_.get(inveniordm, "metadata.creators")) == 1
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "affiliation": [
                {
                    "id": "https://ror.org/04wxnsj81",
                    "name": "DataCite",
                },
            ],
            "family_name": "Fenner",
            "given_name": "Martin",
            "name": "Fenner, Martin",
            "type": "personal",
            "identifiers": [{"identifier": "0000-0003-1419-2405", "scheme": "orcid"}],
        }
    }
    assert py_.get(inveniordm, "metadata.title") == "Introducing the PID Graph"
    assert py_.get(inveniordm, "metadata.publication_date") == "2019-03-28"
    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2023-09-07T13:48:44", "type": {"id": "updated"}}
    ]
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.identifiers") == [
        {"identifier": "9e24e4be-1915-48cc-a6b0-c23da5bc2857", "scheme": "UUID"}
    ]
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "Persistent identifiers (PIDs) are not only important"
    )
    assert py_.get(inveniordm, "custom_fields.journal:journal.title") == "Front Matter"
    assert py_.get(inveniordm, "custom_fields.journal:journal.issn") == "2749-9952"
