"""BibTeX reader tests"""

import pytest

from commonmeta import Metadata
from commonmeta.readers.bibtex_reader import read_bibtex


def test_journal_article():
    """Journal article from crossref.bib fixture."""
    string = open("tests/fixtures/crossref.bib").read()
    subject = Metadata(string, via="bibtex")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"
    assert subject.url == "http://elifesciences.org/lookup/doi/10.7554/eLife.01567"
    assert subject.title == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    assert len(subject.contributors) == 5
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Martial", "family_name": "Sankar"},
        "roles": ["Author"],
    }
    assert subject.contributors[4] == {
        "type": "Person",
        "person": {"given_name": "Christian S", "family_name": "Hardtke"},
        "roles": ["Author"],
    }
    assert subject.date_published == "2014-02"
    assert subject.description == "Among various advantages, their small size makes model organisms preferred subjects of investigation. Yet, even in model systems detailed analysis of numerous developmental processes at cellular level is severely hampered by their scale."
    assert subject.license == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
        "title": "Creative Commons Attribution 3.0 Unported",
    }
    assert subject.publisher == {"name": "eLife Sciences Organisation, Ltd."}
    assert subject.container == {
        "type": "Journal",
        "title": "eLife",
        "identifier": "2050-084X",
        "identifier_type": "ISSN",
        "volume": "3",
    }
    assert subject.identifiers == [
        {"identifier": "https://doi.org/10.7554/elife.01567", "identifier_type": "DOI"}
    ]
    assert subject.provider == "BibTeX"


def test_dissertation():
    """PhD thesis from pure.bib fixture."""
    string = open("tests/fixtures/pure.bib").read()
    subject = Metadata(string, via="bibtex")
    assert subject.id == "dbbe66e459a446a0b6fddf42d3401ccb"
    assert subject.type == "Dissertation"
    assert subject.title == "A multiscale analysis of the urban heat island effect: from city averaged temperatures to the energy demand of individual buildings"
    assert subject.contributors == [
        {
            "type": "Person",
            "person": {"given_name": "Y.", "family_name": "Toparlar"},
            "roles": ["Author"],
        }
    ]
    assert subject.date_published == "2018-04-25"
    assert subject.description == "Designing the climates of cities"
    assert subject.publisher == {"name": "Technische Universiteit Eindhoven"}
    assert subject.container == {
        "type": "Periodical",
        "identifier": "978-90-386-4503-2",
        "identifier_type": "ISBN",
    }
    assert subject.language == "en"
    assert subject.identifiers is None
    assert subject.provider == "BibTeX"


def test_inline_journal_article():
    """Journal article parsed from inline BibTeX string."""
    bibtex = """@article{Ralser2006,
  author    = {Ralser, Markus and Querfurth, Rainer and Warnatz, Hans-Jörg and Lehrach, Hans and Birchmeier, Carmen and Vinaixa, Maria},
  title     = {An efficient and economic enhancer mix for PCR},
  journal   = {Biochemical and Biophysical Research Communications},
  year      = {2006},
  volume    = {347},
  number    = {3},
  pages     = {747--757},
  doi       = {10.1016/j.bbrc.2006.06.136},
  issn      = {0006-291X},
}"""
    subject = Metadata(bibtex, via="bibtex")
    assert subject.id == "https://doi.org/10.1016/j.bbrc.2006.06.136"
    assert subject.type == "JournalArticle"
    assert subject.title == "An efficient and economic enhancer mix for PCR"
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Markus", "family_name": "Ralser"},
        "roles": ["Author"],
    }
    assert subject.date_published == "2006"
    assert subject.container == {
        "type": "Journal",
        "title": "Biochemical and Biophysical Research Communications",
        "identifier": "0006-291X",
        "identifier_type": "ISSN",
        "volume": "347",
        "issue": "3",
        "first_page": "747",
        "last_page": "757",
    }


def test_book_chapter():
    """BookChapter (incollection) entry."""
    bibtex = """@incollection{Smith2020,
  author    = {Smith, John A.},
  title     = {Machine Learning in Practice},
  booktitle = {Handbook of Artificial Intelligence},
  publisher = {Academic Press},
  year      = {2020},
  pages     = {101--130},
  isbn      = {978-0-12-345678-9},
}"""
    subject = Metadata(bibtex, via="bibtex")
    assert subject.type == "BookChapter"
    assert subject.title == "Machine Learning in Practice"
    assert subject.container == {
        "type": "Book",
        "title": "Handbook of Artificial Intelligence",
        "identifier": "978-0-12-345678-9",
        "identifier_type": "ISBN",
        "first_page": "101",
        "last_page": "130",
    }
    assert subject.publisher == {"name": "Academic Press"}


def test_proceedings_article():
    """ProceedingsArticle (inproceedings) entry."""
    bibtex = """@inproceedings{Doe2019,
  author    = {Doe, Jane},
  title     = {Deep Learning for Image Segmentation},
  booktitle = {Proceedings of CVPR 2019},
  year      = {2019},
  pages     = {1234--1242},
}"""
    subject = Metadata(bibtex, via="bibtex")
    assert subject.type == "ProceedingsArticle"
    assert subject.container == {
        "type": "Book",
        "title": "Proceedings of CVPR 2019",
        "first_page": "1234",
        "last_page": "1242",
    }


def test_no_doi_uses_url_as_id():
    """When DOI absent, URL becomes the record ID."""
    bibtex = """@misc{webpage2023,
  title = {Open Science Framework},
  url   = {https://osf.io},
  year  = {2023},
}"""
    subject = Metadata(bibtex, via="bibtex")
    assert subject.id == "https://osf.io"
    assert subject.type == "Other"
    assert subject.url == "https://osf.io"


def test_no_doi_no_url_uses_citekey():
    """Fallback to cite key when no DOI and no URL."""
    bibtex = """@article{myCiteKey,
  author = {Brown, Alice},
  title  = {A Study},
  year   = {2021},
  journal = {Test Journal},
}"""
    subject = Metadata(bibtex, via="bibtex")
    assert subject.id == "myCiteKey"


def test_organization_author():
    """Author name without comma is treated as Organization by the reader.

    bibtexparser v1.4 strips braces, so double-brace org names like
    {{WHO}} lose their brace marker. Names that are not split on comma
    are passed as-is to get_authors; is_personal_name then decides the type.
    Three-word names like 'World Health Organization' that contain no org
    keyword are still classified as Person by is_personal_name. To reliably
    round-trip as Organization, use a name with a recognized org keyword
    (e.g. 'WHO Collaboration').
    """
    bibtex = """@techreport{WHO2022,
  author      = {WHO Collaboration},
  title       = {Global Health Estimates},
  institution = {WHO},
  year        = {2022},
}"""
    subject = Metadata(bibtex, via="bibtex")
    assert subject.type == "Report"
    assert subject.contributors[0]["type"] == "Organization"
    assert subject.contributors[0]["organization"]["name"] == "WHO Collaboration"


def test_empty_input():
    """Empty or None input returns not_found state."""
    result = read_bibtex(None)
    assert result == {"state": "not_found"}

    result = read_bibtex("")
    assert result == {"state": "not_found"}


def test_malformed_bibtex():
    """Bibtex with no entries returns not_found."""
    result = read_bibtex("this is not bibtex")
    assert result == {"state": "not_found"}


def test_language_conversion():
    """Language name 'English' converts to ISO 639-1 code 'en'."""
    string = open("tests/fixtures/pure.bib").read()
    subject = Metadata(string, via="bibtex")
    assert subject.language == "en"


def test_pages_single():
    """Single page number (no range) stored in first_page only."""
    bibtex = """@article{single_page,
  author  = {Lee, Chris},
  title   = {A Note},
  journal = {Letters},
  year    = {2020},
  pages   = {e42},
}"""
    subject = Metadata(bibtex, via="bibtex")
    assert subject.container["first_page"] == "e42"
    assert "last_page" not in subject.container
