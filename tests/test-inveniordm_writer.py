# pylint: disable=invalid-name
"""InvenioRDM writer tests"""

import orjson as json
import pytest
from os import path
from pydash import py_

from commonmeta import Metadata, MetadataList


@pytest.mark.vcr
def test_publication():
    "publication"
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-article"
    assert py_.get(inveniordm, "metadata.doi") == "10.5281/zenodo.5244404"
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


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-article"
    assert py_.get(inveniordm, "metadata.doi") == "10.7554/elife.01567"
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

    assert py_.get(inveniordm, "metadata.title") == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    assert py_.get(inveniordm, "metadata.publisher") == "eLife Sciences Publications, Ltd"
    assert py_.get(inveniordm, "metadata.publication_date") == "2014-02-11"
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "Among various advantages, their small size makes model organisms preferred subjects of investigation."
    )


@pytest.mark.vcr
def test_rogue_scholar():
    "Rogue Scholar"
    string = "https://beta.rogue-scholar.org/api/records/kqfsz-qzd05"
    subject = Metadata(string)
    assert subject.id == "https://demo.front-matter.io/records/kqfsz-qzd05"
    assert subject.type == "Image"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "metadata.resource_type.id") == "image-other"
    assert py_.get(inveniordm, "metadata.doi") is None
    assert len(py_.get(inveniordm, "metadata.creators")) == 4
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Burton",
            "given_name": "Phillip",
            "name": "Burton, Phillip",
            "type": "personal",
            "identifiers": [{"identifier": "0000-0002-1825-0097", "scheme": "orcid"}],
        }
    }
    assert py_.get(inveniordm, "metadata.title") == "Elliott Group's gallery"
    assert py_.get(inveniordm, "metadata.publisher") == "InvenioRDM"
    assert py_.get(inveniordm, "metadata.publication_date") == "1994-02"
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.version") == "v0.0.1"
    assert py_.get(inveniordm, "metadata.description").startswith(
        "One state discussion green sit if."
    )


@pytest.mark.vcr
def test_from_json_feed():
    "JSON Feed"
    string = "https://api.rogue-scholar.org/posts/9e24e4be-1915-48cc-a6b0-c23da5bc2857"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/ewrv712-2k7rx6d"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert py_.get(inveniordm, "metadata.doi") == "10.53731/ewrv712-2k7rx6d"
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
    assert py_.get(inveniordm, "metadata.publisher") == "Front Matter"
    assert py_.get(inveniordm, "metadata.publication_date") == "2019-03-28T01:00:00"
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.identifiers") == [
        {"identifier": "9e24e4be-1915-48cc-a6b0-c23da5bc2857", "scheme": "UUID"}
    ]
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "Persistent identifiers (PIDs) are not only important"
    )
