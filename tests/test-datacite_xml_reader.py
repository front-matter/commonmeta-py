# pylint: disable=invalid-name
"""Test datacite_xml reader"""
from os import path
import pytest
from commonmeta import Metadata


def test_missing_resource_type_general():
    """missing resource_type_general"""
    string = path.join(path.dirname(__file__), "fixtures", "vivli.xml")
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5072/00013641"
    assert subject.type == "Other"
    assert subject.doi == "10.5072/00013641"
    assert subject.publisher == "Vivli"
    assert subject.url is None
    assert subject.titles[0] == {
        "title": "A Comparative Pilot Study of the Efficacy of Three Portable Oxygen Concentrators During a 6-Minute Walk Test in Patients With Chronic Lung Disease"
    }
    assert len(subject.creators) == 1
    assert subject.creators[0] == {"name": "Vivli"}
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.date == {'published': '2018'}
    assert subject.references is None
    assert subject.container is None
    assert subject.descriptions is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.version is None
    assert subject.schema_version == "http://datacite.org/schema/kernel-4"
    assert subject.agency == "DataCite"


def test_geo_location_empty():
    """geo_location empty"""
    string = path.join(
        path.dirname(__file__), "fixtures", "datacite-geolocation-empty.xml"
    )
    subject = Metadata(string)

    assert subject.id == "https://doi.org/10.1594/ieda/111185"
    assert subject.type == "Dataset"
    assert subject.publisher == "EarthChem"
    assert subject.titles[0] == {
        "title": "Geochemical and grain-size analyses of atmospheric dusts from Pennsylvanian carbonates of the Copacabana Formation (Madre de Dios Basin, Bolivia)"
    }
    assert len(subject.creators) == 3
    assert subject.creators[0] == {
        "type": "Person",
        "givenName": "Carlos",
        "familyName": "Carvajal",
    }
    assert subject.contributors is None
    assert subject.rights == [
        {
            "rights": "Creative Commons Attribution-NonCommercial-Share Alike 3.0 United States [CC BY-NC-SA 3.0]",
            "rightsURI": "https://creativecommons.org/licenses/by-nc-sa/3.0/us/",
        }
    ]
    assert subject.date == {'published': '2018', 'available': '2018-06-21', 'created': '2018-06-20'}
    assert subject.subjects == [
        {"subject": "Global", "subjectScheme": "coverage scope"}
    ]
    assert subject.references is None
    assert subject.geo_locations is None
    assert subject.language == "en"
    assert subject.version == "1.0"
    assert subject.schema_version == "http://datacite.org/schema/kernel-4"
    assert subject.agency == "DataCite"


def test_blog_posting():
    """blog_posting"""
    string = "10.5438/4K3M-NYVG"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5438/4k3m-nyvg"
    assert subject.type == "Article"
    assert subject.creators == [
        {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "type": "Person",
            "givenName": "Martin",
            "familyName": "Fenner",
        }
    ]
    assert subject.titles == [{"title": "Eating your own Dog Food"}]
    assert subject.publisher == "DataCite"
    assert subject.date == {'published': '2016-12-20', 'created': '2016-12-20', 'updated': '2016-12-20'}
    assert subject.subjects == [{'subject': 'datacite'}, {'subject': 'doi'}, {'subject': 'metadata'}, {'subject': 'FOS: Computer and information sciences', 'subjectScheme': 'Fields of Science and Technology (FOS)'}]
    assert subject.descriptions[0]["description"].startswith("Eating your own dog food is a slang term")
    assert subject.descriptions[0]["descriptionType"] == "Abstract"
    assert subject.agency == "DataCite"
    assert subject.schema_version == "http://datacite.org/schema/kernel-4"
