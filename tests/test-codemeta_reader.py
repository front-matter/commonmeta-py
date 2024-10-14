# pylint: disable=invalid-name
"""Test codemeta reader"""
from os import path
from commonmeta import Metadata


def test_rdataone():
    """rdataone"""
    string = path.join(path.dirname(__file__), "fixtures", "codemeta.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5063/f1m61h5x"
    assert subject.type == "Software"
    assert subject.url == "https://github.com/DataONEorg/rdataone"
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "type": "Person",
        "id": "https://orcid.org/0000-0003-0077-4738",
        "contributorRoles": ["Author"],
        "givenName": "Matt",
        "familyName": "Jones",
        "affiliations": [{"name": "NCEAS"}],
    }
    assert subject.titles == [{"title": "R Interface to the DataONE REST API"}]
    assert subject.descriptions[0]["description"].startswith(
        "Provides read and write access to data and metadata"
    )
    # [{'subject': 'data sharing'}], [{'subject': 'data repository'}], [{'subject': 'dataone'}]
    assert subject.subjects is None
    assert subject.date == {
        "created": "2016-05-27",
        "published": "2016-05-27",
        "updated": "2016-05-27",
    }
    assert subject.publisher == {"name": "https://cran.r-project.org"}
    assert subject.license == {
        "id": "Apache-2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0",
    }
    assert subject.version == "2.0.0"


def test_metadata_reports():
    """metadata_reports"""
    string = "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5438/wr0x-e194"
    assert subject.type == "Software"
    assert subject.url == "https://github.com/datacite/metadata-reports"
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "type": "Person",
        "id": "https://orcid.org/0000-0003-0077-4738",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
    }
    assert subject.titles == [{"title": "DOI Registrations for Software"}]
    assert subject.descriptions[0]["description"].startswith(
        "Analysis of DataCite DOIs registered for software"
    )
    assert subject.subjects is None
    assert subject.date == {
        "created": "2018-03-09",
        "published": "2018-05-17",
        "updated": "2018-05-17",
    }
    assert subject.publisher == {"name": "DataCite"}
    assert subject.license == {
        "id": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
    assert subject.version is None
