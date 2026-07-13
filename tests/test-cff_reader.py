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
            "type": "Person",
            "person": {
                "id": "https://orcid.org/0000-0002-9538-7919",
                "given_name": "Robert",
                "family_name": "Haines",
                "affiliations": [{"name": "The University of Manchester, UK"}],
            },
            "roles": ["Author"],
        },
        {
            "type": "Organization",
            "organization": {"name": "The Ruby Citation File Format Developers"},
            "roles": ["Author"],
        },
    ]
    assert subject.title == "Ruby CFF Library"
    assert subject.description.startswith(
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
    assert subject.date_published == "2024-10-26"
    assert subject.version == "1.3.0"
    assert subject.license == {
        "id": "Apache-2.0",
        "title": "Apache License 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    }
    assert subject.references == [{"id": "https://doi.org/10.5281/zenodo.1003149"}]
    assert subject.publisher == {"name": "GitHub"}
    assert subject.provider is None


def test_cff_converter_python():
    """cff-converter-python"""
    string = "https://github.com/citation-file-format/cff-converter-python/blob/main/CITATION.cff"
    subject = Metadata(string)
    # commonmeta v1.0 requires `id`; this CFF software has no DOI, so it's
    # correctly invalid.
    assert subject.is_valid is False
    assert subject.id is None
    assert subject.url == "https://github.com/citation-file-format/cffconvert"
    assert subject.type == "Software"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-7064-4069",
            "given_name": "Jurriaan H.",
            "family_name": "Spaaks",
            "affiliations": [{"name": "Netherlands eScience Center"}],
        },
        "roles": ["Author"],
    }
    assert subject.title == "cffconvert"
    assert subject.description == (
        "Command line program to validate and convert CITATION.cff files."
    )
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
    assert subject.date_published == "2021-09-22"
    assert subject.version == "3.0.0a0"
    assert subject.license == {
        "id": "Apache-2.0",
        "title": "Apache License 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    }
    assert subject.references == [{"id": "https://doi.org/10.5281/zenodo.1310751"}]
    assert subject.publisher == {"name": "GitHub"}
    assert subject.provider is None


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
            "person": {
                "id": "https://orcid.org/0000-0002-0055-8659",
                "given_name": "Kaizhao",
                "family_name": "Liang",
            },
            "roles": ["Author"],
        }
    ]
    assert subject.title == "Long Context Transformer v0.0.1"
    assert subject.description is None
    assert subject.subjects is None
    assert subject.date_published == "2023-02-17"
    assert subject.version == "0.0.1"
    assert subject.license is None
    assert subject.references is None
    assert subject.publisher == {"name": "GitHub"}
    assert subject.provider is None
