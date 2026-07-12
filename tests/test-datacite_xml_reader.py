# pylint: disable=invalid-name
"""Test datacite_xml reader"""

import json
from os import path

from commonmeta import Metadata
from commonmeta.schema_utils import json_schema_errors


def test_missing_resource_type_general():
    """missing resource_type_general"""
    string = path.join(path.dirname(__file__), "fixtures", "vivli.xml")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5072/00013641"
    assert subject.type == "Other"
    assert subject.publisher == {"name": "Vivli"}
    assert subject.url is None
    assert subject.title == "A Comparative Pilot Study of the Efficacy of Three Portable Oxygen Concentrators During a 6-Minute Walk Test in Patients With Chronic Lung Disease"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Organization",
        "organization": {
            "name": "Vivli"
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == "2018"
    assert subject.references is None
    assert subject.container is None
    assert subject.description is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.version is None
    assert subject.provider == "DataCite"


def test_geo_location_empty():
    """geo_location empty"""
    string = path.join(
        path.dirname(__file__), "fixtures", "datacite-geolocation-empty.xml"
    )
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1594/ieda/111185"
    assert subject.type == "Dataset"
    assert subject.publisher == {"name": "EarthChem"}
    assert subject.title == "Geochemical and grain-size analyses of atmospheric dusts from Pennsylvanian carbonates of the Copacabana Formation (Madre de Dios Basin, Bolivia)"
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Carlos",
            "family_name": "Carvajal"
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.identifiers == [
        {
            "identifier": "http://www.earthchem.org/library/browse/view?id=1185",
            "identifier_type": "URL",
        }
    ]
    assert subject.license == {
        "id": "CC-BY-NC-SA-3.0",
        "title": "Creative Commons Attribution Non Commercial Share Alike 3.0 Unported",
        "url": "https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode",
    }
    assert (subject.date_published == '2018'
        and subject.dates == {'created': '2018-06-20', 'available': '2018-06-21'})
    assert subject.subjects == [
        {"subject": "Global"}
    ]
    assert subject.references is None
    # get_geolocation() correctly extracts the point present in this fixture
    # despite the file's name.
    assert subject.geo_locations == [
        {
            "point_longitude": -68.2975,
            "point_latitude": -11.64583333,
        }
    ]
    assert subject.language == "en"
    assert subject.version == "1.0"
    assert subject.provider == "DataCite"

    commonmeta = json.loads(subject.write())
    assert json_schema_errors(commonmeta, "commonmeta") is None
    assert commonmeta["geo_locations"] == [
        {
            "point_longitude": -68.2975,
            "point_latitude": -11.64583333,
        }
    ]


def test_blog_posting():
    """blog_posting"""
    string = "10.5438/4K3M-NYVG"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5438/4k3m-nyvg"
    assert subject.type == "BlogPost"
    assert subject.contributors == [
        {
            "type": "Person",
            "person": {
                "id": "https://orcid.org/0000-0003-1419-2405",
                "given_name": "Martin",
                "family_name": "Fenner"
            },
            "roles": [
                "Author"
            ]
        }
    ]
    assert subject.title == "Eating your own Dog Food"
    assert subject.publisher == {"name": "DataCite"}
    assert (subject.date_published == '2016-12-20'
        and subject.date_updated == '2016-12-20'
        and subject.dates == {'created': '2016-12-20'})
    assert subject.subjects == [
        {"subject": "datacite"},
        {"subject": "doi"},
        {"subject": "metadata"},
        {
            "subject": "FOS: Computer and information sciences",
        },
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.language == "en"
    assert subject.description.startswith(
        "Eating your own dog food is a slang term"
    )
    assert subject.provider == "DataCite"
