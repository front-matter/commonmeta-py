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
        "person": {
            "id": "https://orcid.org/0000-0003-0077-4738",
            "given_name": "Matt",
            "family_name": "Jones",
            "affiliations": [{"name": "NCEAS"}],
        },
        "roles": ["Author"],
    }
    assert subject.title == "R Interface to the DataONE REST API"
    assert subject.description.startswith(
        "Provides read and write access to data and metadata"
    )
    # [{'subject': 'data sharing'}], [{'subject': 'data repository'}], [{'subject': 'dataone'}]
    assert subject.subjects is None
    assert (
        subject.date_published == "2016-05-27"
        and subject.date_updated == "2016-05-27"
        and subject.dates == {"created": "2016-05-27"}
    )
    assert subject.publisher == {"name": "https://cran.r-project.org"}
    assert subject.license == {
        "id": "Apache-2.0",
        "title": "Apache License 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
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
        "person": {
            "id": "https://orcid.org/0000-0003-0077-4738",
            "given_name": "Martin",
            "family_name": "Fenner",
        },
        "roles": ["Author"],
    }
    assert subject.title == "DOI Registrations for Software"
    assert subject.description.startswith(
        "Analysis of DataCite DOIs registered for software"
    )
    assert subject.subjects is None
    assert (
        subject.date_published == "2018-05-17"
        and subject.date_updated == "2018-05-17"
        and subject.dates == {"created": "2018-03-09"}
    )
    assert subject.publisher == {"name": "DataCite"}
    assert subject.license == {
        "id": "MIT",
        "title": "MIT License",
        "url": "https://opensource.org/license/mit/",
    }
    assert subject.version is None
