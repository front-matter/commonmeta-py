"""Test cff reader"""
import pytest
from commonmeta import Metadata


def vcr_config():
    return {"record_mode": "new_episodes"}


@pytest.mark.vcr
def test_ruby_cff():
    """ruby-cff"""
    string = "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.1184077"
    assert subject.url == "https://github.com/citation-file-format/ruby-cff"
    assert subject.type == "Software"
    assert subject.contributors == [
        {
            "affiliation": [{"name": "The University of Manchester, UK"}],
            "familyName": "Haines",
            "givenName": "Robert",
            "id": "https://orcid.org/0000-0002-9538-7919",
            "contributorRoles": ["Author"],
            "type": "Person",
        },
        {
            "name": "The Ruby Citation File Format Developers",
            "contributorRoles": ["Author"],
            "type": "Organization",
        },
    ]
    assert subject.titles == [{"title": "Ruby CFF Library"}]
    assert subject.descriptions[0]["description"].startswith(
        "This library provides a Ruby interface to manipulate Citation File Format files"
    )
    assert subject.subjects == [
        {"subject": "ruby"},
        {"subject": "credit"},
        {"subject": "software citation"},
        {"subject": "research software"},
        {"subject": "software sustainability"},
        {"subject": "metadata"},
        {"subject": "citation file format"},
        {"subject": "CFF"},
    ]
    assert subject.date == {"published": "2024-01-19"}
    assert subject.version == "1.2.0"
    assert subject.license == {
        "id": "Apache-2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0",
    }
    assert subject.references is None
    assert subject.publisher == {"name": "GitHub"}
    assert subject.provider == "DataCite"


def test_cff_converter_python():
    """cff-converter-python"""
    string = "https://github.com/citation-file-format/cff-converter-python/blob/main/CITATION.cff"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id is None
    assert subject.url == "https://github.com/citation-file-format/cffconvert"
    assert subject.type == "Software"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "affiliation": [{"name": "Netherlands eScience Center"}],
        "familyName": "Spaaks",
        "givenName": "Jurriaan H.",
        "id": "https://orcid.org/0000-0002-7064-4069",
        "contributorRoles": ["Author"],
        "type": "Person",
    }
    assert subject.titles == [{"title": "cffconvert"}]
    assert subject.descriptions == [
        {
            "description": "Command line program to validate and convert CITATION.cff files.",
            "type": "Abstract",
        }
    ]
    assert subject.subjects == [
        {"subject": "bibliography"},
        {"subject": "BibTeX"},
        {"subject": "cff"},
        {"subject": "citation"},
        {"subject": "CITATION.cff"},
        {"subject": "CodeMeta"},
        {"subject": "EndNote"},
        {"subject": "RIS"},
        {"subject": "Citation File Format"},
    ]
    assert subject.date == {"published": "2021-09-22"}
    assert subject.version == "3.0.0a0"
    assert subject.license == {
        "id": "Apache-2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0",
    }
    assert subject.references is None
    assert subject.publisher == {"name": "GitHub"}
    assert subject.provider == "GitHub"


def test_github_repo():
    """github repo"""
    string = "https://github.com/kyleliang919/Long-context-transformers"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.7651809"
    assert subject.url == "https://github.com/kyleliang919/Long-context-transformers"
    assert subject.type == "Software"
    assert subject.contributors == [
        {
            "type": "Person",
            "id": "https://orcid.org/0000-0002-0055-8659",
            "contributorRoles": ["Author"],
            "givenName": "Kaizhao",
            "familyName": "Liang",
        }
    ]
    assert subject.titles == [{"title": "Long Context Transformer v0.0.1"}]
    assert subject.descriptions is None
    assert subject.subjects is None
    assert subject.date == {"published": "2023-02-17"}
    assert subject.version == "0.0.1"
    assert subject.license is None
    assert subject.references is None
    assert subject.publisher == {"name": "GitHub"}
    assert subject.provider == "DataCite"
