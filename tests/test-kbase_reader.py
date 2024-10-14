# pylint: disable=invalid-name,too-many-lines
"""kbase reader tests"""
from os import path
from commonmeta import Metadata


def test_metatranscriptome():
    """Metatrascriptome"""
    string = path.join(
        path.dirname(__file__), "fixtures", "JDP_5fa4fb4647675a20c852c60b_kbcms.json"
    )
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "5fa4fb4647675a20c852c60b"
    assert subject.type == "Dataset"
    assert subject.url is None
    assert subject.titles[0] == {
        "title": "Metatranscriptome of feshwater microbial communities from Wyoming, USA - littlewindriver_2019_sw_WHONDRS-S19S_0009 (Metagenome Metatranscriptome)"
    }
    assert len(subject.contributors) == 15
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Investigation", "ProjectLeader"],
        "givenName": "Kelly",
        "familyName": "Wrighton",
    }
    assert subject.license is None
    assert subject.date == {"submitted": "2020-11-05"}
    assert subject.relations is None
    assert subject.publisher == {
        "id": "https://ror.org/04xm1d337",
        "name": "Joint Genome Institute",
    }
    assert subject.funding_references == [
        {
            "awardNumber": "505780",
            "award_uri": "https://www.osti.gov/award-doi-service/biblio/10.46936/10.25585/60001289",
            "funderIdentifier": "https://doi.org/10.13039/100000015",
            "funderIdentifierType": "DOI",
            "funderName": "US Department of Energy",
        }
    ]
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("This proposal seeks to create a global census of microbial genome")
    )
    # assert subject.subjects == [
    #     {"subject": "microbial ecology"},
    # ]
    assert subject.container == {
        "id": "https://www.re3data.org/repository/r3d100012864",
        "type": "DataRepository",
        "title": "KBase",
    }
    assert subject.language is None
    assert subject.version is None
    assert subject.files is None


def test_gulf_of_mexico():
    """Metatrascriptome"""
    string = path.join(
        path.dirname(__file__), "fixtures", "10.25982_86723.65_1778009_kbcms.json"
    )
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.25982/86723.65/1778009"
    assert subject.type == "Dataset"
    assert subject.url is None
    assert subject.titles[0] == {
        "title": "Gulf of Mexico blue hole harbors high levels of novel microbial lineages"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "id": "https://orcid.org/0000-0001-8522-7682",
        "contributorRoles": ["DataCuration", "ContactPerson", "WritingOriginalDraft"],
        "givenName": "Nastassia",
        "familyName": "Patin",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
    }

    assert subject.date == {
        "published": "2021",
    }
    assert len(subject.relations) == 8
    assert subject.relations[1] == {
        "id": "https://doi.org/10.6084/m9.figshare.12644018.v3",
        "type": "IsIdenticalTo",
    }
    assert subject.publisher == {"id": "https://ror.org/01znn6x10", "name": "KBase"}
    # assert subject.funding_references == [
    #     {
    #         "awardNumber": "NA18OAR0110291",
    #         "award_uri": "https://dx.doi.org/10.25923/hjf1-zj16",
    #         "funderName": "National Oceanic and Atmospheric Administration Office of Exploration and Research",
    #         "funderIdentifier": "https://ror.org/02z5nhe81",
    #         "funderIdentifierType": "ROR",
    #     }
    # ]
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "xploration of oxygen-depleted marine environments has consistently revealed novel microbial taxa"
        )
    )
    # assert subject.subjects == [
    #     {"subject": "microbial ecology"},
    # ]
    assert subject.container == {
        "id": "https://www.re3data.org/repository/r3d100012864",
        "type": "DataRepository",
        "title": "KBase",
    }
    assert subject.language == "en"
    assert subject.version is None
    assert subject.files is None
