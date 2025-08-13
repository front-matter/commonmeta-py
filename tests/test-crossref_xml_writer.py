"""crossref_xml_writer tests for commonmeta-py"""

from collections import OrderedDict
from os import path

import pydash as py_
import pytest

from commonmeta import Metadata, MetadataList
from commonmeta.base_utils import parse_xml
from commonmeta.writers.crossref_xml_writer import normalize_isbn_crossref


def test_write_crossref_xml_header():
    """Write crossref_xml header"""
    string = "https://doi.org/10.1371/journal.pone.0000030"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    lines = subject.write(to="crossref_xml").split("\n")
    assert subject.is_valid
    assert lines[0] == '<?xml version="1.0" encoding="utf-8"?>'
    assert (
        lines[1]
        == '<doi_batch xmlns="http://www.crossref.org/schema/5.4.0" version="5.4.0">'
    )


def test_write_metadata_as_crossref_xml():
    """Write metadata as crossref_xml"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.7554/elife.01567"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 5
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Martial",
        "surname": "Sankar",
        "affiliations": {
            "institution": {
                "institution_name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
            }
        },
    }
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "Among various advantages, their small size makes model organisms preferred subjects of investigation."
    )
    assert py_.get(crossref_xml, "doi_data.doi") == "10.7554/elife.01567"
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 27
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "key": "bib1",
        "volume": "426",
        "cYear": "2003",
        "article_title": "APL regulates vascular tissue identity in Arabidopsis",
        "doi": "10.1038/nature02100",
    }


@pytest.mark.vcr
def test_write_crossref_xml_list():
    """write_crossref_xml_list"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref-list.json")
    subject_list = MetadataList(string, via="crossref")
    assert len(subject_list.items) == 20

    crossref_xml_list = subject_list.write(to="crossref_xml")
    assert subject_list.is_valid
    crossref_xml_list = parse_xml(crossref_xml_list, dialect="crossref")
    crossref_xml_list = py_.get(crossref_xml_list, "doi_batch.body.journal", [])
    assert len(crossref_xml_list) == 20
    crossref_xml = crossref_xml_list[0]
    assert (
        py_.get(crossref_xml, "journal_article.doi_data.doi")
        == "10.1306/703c7c64-1707-11d7-8645000102c1865d"
    )
    assert (
        py_.get(crossref_xml, "journal_article.titles.0.title")
        == "Hydrocarbon Potential of Columbia Plateau--an Overview: ABSTRACT"
    )
    assert len(py_.get(crossref_xml, "journal_article.contributors.person_name")) == 1
    assert py_.get(crossref_xml, "journal_article.contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "surname": "Newell P. Campbell",
    }
    assert py_.get(crossref_xml, "abstract") is None


@pytest.mark.vcr
def test_write_commonmeta_list_as_crossref_xml():
    """write_commonmeta_list crossref_xml"""
    string = path.join(path.dirname(__file__), "fixtures", "json_feed.json")
    subject_list = MetadataList(string)
    assert len(subject_list.items) == 15

    crossref_xml_list = subject_list.write(to="crossref_xml")
    assert subject_list.is_valid
    crossref_xml_list = parse_xml(crossref_xml_list, dialect="crossref")
    crossref_xml_list = py_.get(crossref_xml_list, "doi_batch.body.posted_content", [])
    assert len(crossref_xml_list) == 15
    crossref_xml = crossref_xml_list[0]
    assert py_.get(crossref_xml, "doi_data.doi") == "10.59350/26ft6-dmv65"
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Das BUA Open Science Dashboard Projekt: die Entwicklung disziplinspezifischer Open-Science-Indikatoren"
    )
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "given_name": "Maatje Sophia",
        "sequence": "first",
        "surname": "Duine",
    }
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "Autorinnen: Maaike Duine (ORCiD) und Maxi Kindling (ORCiD)"
    )


def test_normalize_isbn_crossref():
    """Test normalize_isbn_crossref"""
    assert normalize_isbn_crossref("9783161484100") == "978-3161484100"
    assert normalize_isbn_crossref("9783662463703") == "978-3662463703"
    assert normalize_isbn_crossref("9781108348843") == "978-1108348843"
    assert normalize_isbn_crossref("invalid-isbn") is None


@pytest.mark.vcr
def test_write_crossref_xml_journal_article_plos():
    """Write crossref_xml journal article plos"""
    string = "https://doi.org/10.1371/journal.pone.0000030"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert py_.get(crossref_xml, "language") == "en"
    assert py_.get(crossref_xml, "doi_data.doi") == "10.1371/journal.pone.0000030"
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 73
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    )
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 6
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "given_name": "Markus",
        "sequence": "first",
        "surname": "Ralser",
    }
    assert py_.get(crossref_xml, "abstract") is None


@pytest.mark.vcr
def test_write_crossref_xml_posted_content():
    """Write crossref_xml posted_content"""
    string = "https://doi.org/10.1101/2020.12.01.406702"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.1101/2020.12.01.406702"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "type") == "preprint"
    assert py_.get(crossref_xml, "language") is None
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 8
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "ORCID": "https://orcid.org/0000-0002-9346-671X",
        "given_name": "Luke R.",
        "surname": "Joyce",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Identification of a novel cationic glycolipid in<i>Streptococcus agalactiae</i>that contributes to brain entry and meningitis"
    )
    assert py_.get(crossref_xml, "posted_date") == {
        "day": "1",
        "month": "12",
        "year": "2020",
    }
    assert py_.get(crossref_xml, "institution.institution_name") == "bioRxiv"
    assert py_.get(crossref_xml, "item_number") is None
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "AbstractBacterial membrane lipids are critical for membrane bilayer formation"
    )
    assert py_.get(crossref_xml, "doi_data.doi") == "10.1101/2020.12.01.406702"
    assert (
        py_.get(crossref_xml, "doi_data.resource")
        == "http://biorxiv.org/lookup/doi/10.1101/2020.12.01.406702"
    )
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 61
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "key": "2024080502174202000_2020.12.01.406702v5.1",
        "doi": "10.1002/iub.240",
    }


@pytest.mark.vcr
def test_write_crossref_journal_article_from_datacite():
    """Write crossref_xml journal article from datacite"""
    string = "10.2312/geowissenschaften.1989.7.181"
    subject = Metadata(string, via="datacite")
    assert subject.id == "https://doi.org/10.2312/geowissenschaften.1989.7.181"
    assert subject.descriptions == [
        {"description": "Die Geowissenschaften", "type": "Other"}
    ]

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert py_.get(crossref_xml, "language") == "en"
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "An Overview of the Geology of Canadian Gold Occurrences"
    )
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "David J",
        "surname": "Mossman",
    }
    assert py_.get(crossref_xml, "abstract.0.p").startswith("Die Geowissenschaften")


@pytest.mark.vcr
def test_write_crossref_schema_org_front_matter():
    """Write crossref_xml schema_org front_matter"""
    string = "https://blog.front-matter.io/posts/editorial-by-more-than-200-call-for-emergency-action-to-limit-global-temperature-increases-restore-biodiversity-and-protect-health"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/r9nqx6h-97aq74v-ag7bw"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "language") is None
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Editorial by more than 200 health journals: Call for emergency action to limit global temperature increases, restore biodiversity, and protect health"
    )
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "More than 200 health journals today published an editorial calling for urgent action"
    )


@pytest.mark.vcr
def test_write_crossref_another_schema_org_front_matter():
    """Write crossref_xml another schema_org front_matter"""
    string = "https://blog.front-matter.io/posts/dryad-interview-jen-gibson"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/rceh7pn-tzg61kj-7zv63"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "language") is None
    assert py_.get(crossref_xml, "titles.0.title") == "Dryad: Interview with Jen Gibson"
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "In October Jen Gibson started as the new Executive Director for the Dryad Data Repository."
    )


@pytest.mark.vcr
def test_write_crossref_embedded_schema_org_front_matter():
    """Write crossref_xml embedded schema_org front_matter"""
    string = path.join(
        path.dirname(__file__), "fixtures", "schema_org_front-matter.json"
    )
    subject = Metadata(string, via="schema_org")
    assert subject.id == "https://doi.org/10.53731/r9nqx6h-97aq74v-ag7bw"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "ORCID": "https://orcid.org/0000-0003-1419-2405",
        "sequence": "first",
        "given_name": "Martin",
        "surname": "Fenner",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Editorial by more than 200 health journals: Call for emergency action to limit global temperature increases, restore biodiversity, and protect health"
    )
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "More than 200 health journals today published an editorial calling for urgent action to keep average global temperature increases below 1.5°C"
    )


@pytest.mark.vcr
def test_write_crossref_schema_org_from_another_science_blog():
    """Write crossref_xml schema_org from another science blog"""
    string = "https://donnywinston.com/posts/implementing-the-fair-principles-through-fair-enabling-artifacts-and-services/"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.57099/11h5yt3819"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "ORCID": "https://orcid.org/0000-0002-8424-0604",
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Donny",
        "surname": "Winston",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Implementing the FAIR Principles Through FAIR-Enabling Artifacts and Services"
    )
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "How does a Research Software Engineer (RSE)"
    )


@pytest.mark.vcr
def test_write_crossref_schema_org_upstream_blog():
    """Write crossref_xml schema_org upstream blog"""
    string = "https://upstream.force11.org/deep-dive-into-ethics-of-contributor-roles/"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.54900/rf84ag3-98f00rt-0phta"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 4
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Mohammad",
        "surname": "Hosseini",
        "ORCID": "https://orcid.org/0000-0002-2385-985X",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Deep dive into ethics of Contributor Roles: report of a FORCE11 workshop"
    )
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "The FORCE11 attribution working group held a workshop during the 2021 FORCE conference"
    )


@pytest.mark.vcr
def test_jsonfeed_upstream_blog():
    """jsonfeed upstream blog"""
    string = "https://api.rogue-scholar.org/posts/5d14ffac-b9ac-4e20-bdc0-d9248df4e80d"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.54900/n6dnt-xpq48"
    assert subject.type == "BlogPost"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "type") == "other"
    assert py_.get(crossref_xml, "language") == "en"
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Esha",
        "surname": "Datta",
        "ORCID": "https://orcid.org/0000-0001-9165-2757",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Attempts at automating journal subject classification"
    )
    assert py_.get(crossref_xml, "item_number") == {
        "#text": "5d14ffacb9ac4e20bdc0d9248df4e80d",
        "item_number_type": "uuid",
    }
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "Traditionally, journal subject classification was done manually at varying levels of granularity"
    )
    assert len(py_.get(crossref_xml, "doi_data.collection.item")) == 5
    assert py_.get(crossref_xml, "doi_data.collection.item.0.resource") == {
        "#text": "https://upstream.force11.org/attempts-at-automating-journal-subject-classification",
        "mime_type": "text/html",
    }
    assert py_.get(crossref_xml, "doi_data.collection.item.1.resource") == {
        "#text": "https://api.rogue-scholar.org/posts/10.54900/n6dnt-xpq48.md",
        "mime_type": "text/markdown",
    }
    assert crossref_xml.get("group_title") == "Humanities"


@pytest.mark.vcr
def test_jsonfeed_with_references():
    """jsonfeed with references"""
    string = "https://api.rogue-scholar.org/posts/954f8138-0ecd-4090-87c5-cef1297f1470"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.54900/zwm7q-vet94"
    assert subject.subjects == [{"subject": "FOS: Humanities"}, {"subject": "News"}]
    assert len(subject.references) == 11
    assert subject.references[0] == {
        "id": "https://www.software.ac.uk/blog/2014-12-04-its-impossible-conduct-research-without-software-say-7-out-10-uk-researchers",
        "unstructured": "It’s impossible to conduct research without software, say 7 out of 10 UK "
        "researchers. Accessed April 13, 2023. "
        "https://www.software.ac.uk/blog/2014-12-04-its-impossible-conduct-research-without-software-say-7-out-10-uk-researchers",
    }
    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 2
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "ORCID": "https://orcid.org/0000-0001-5934-7525",
        "affiliations": {
            "institution": {
                "institution_id": {
                    "#text": "https://ror.org/047426m28",
                    "type": "ror",
                },
                "institution_name": "University of Illinois Urbana-Champaign",
            },
        },
        "sequence": "first",
        "given_name": "Daniel S.",
        "surname": "Katz",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "The Research Software Alliance (ReSA)"
    )
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "Research software is a key part of most research today."
    )
    assert len(py_.get(crossref_xml, "citation_list.citation")) > 5
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "key": "ref1",
        "unstructured_citation": "It’s impossible to conduct research without software, say 7 out of 10 UK researchers. Accessed April 13, 2023. https://www.software.ac.uk/blog/2014-12-04-its-impossible-conduct-research-without-software-say-7-out-10-uk-researchers",
    }
    assert crossref_xml.get("group_title") == "Humanities"


@pytest.mark.vcr
def test_jsonfeed_with_doi():
    """jsonfeed with DOI"""
    string = "https://api.rogue-scholar.org/posts/1c578558-1324-4493-b8af-84c49eabc52f"
    subject = Metadata(string, doi="10.59350/kz04m-s8z58")
    assert subject.id == "https://doi.org/10.59350/kz04m-s8z58"
    assert subject.subjects == [
        {"subject": "FOS: Social science"},
        {"subject": "Open Access"},
        {"subject": "Open Access Transformation"},
        {"subject": "Open Science"},
    ]

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Heinz",
        "surname": "Pampel",
        "ORCID": "https://orcid.org/0000-0003-3334-2771",
        "affiliations": {
            "institution": {
                "institution_id": {
                    "#text": "https://ror.org/01hcx6992",
                    "type": "ror",
                },
                "institution_name": "Humboldt-Universität zu Berlin",
            },
        },
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "EU-Mitgliedstaaten betonen die Rolle von wissenschaftsgeleiteten Open-Access-Modellen jenseits von APCs"
    )
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "Die EU-Wissenschaftsministerien haben sich auf ihrer heutigen Sitzung in Brüssel unter dem Titel “Council conclusions on high-quality, transparent, open, trustworthy and equitable scholarly publishing"
    )
    assert len(py_.get(crossref_xml, "doi_data.collection.item")) == 5
    assert py_.get(crossref_xml, "doi_data.collection.item.0.resource") == {
        "#text": "https://wisspub.net/2023/05/23/eu-mitgliedstaaten-betonen-die-rolle-von-wissenschaftsgeleiteten-open-access-modellen-jenseits-von-apcs",
        "mime_type": "text/html",
    }
    assert py_.get(crossref_xml, "doi_data.collection.item.1.resource") == {
        "#text": "https://api.rogue-scholar.org/posts/10.59350/kz04m-s8z58.md",
        "mime_type": "text/markdown",
    }
    assert crossref_xml.get("group_title") == "Social science"


@pytest.mark.vcr
def test_jsonfeed_without_doi():
    """jsonfeed without DOI"""
    string = "https://api.rogue-scholar.org/posts/e2ecec16-405d-42da-8b4d-c746840398fa"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/qc0px-76778"
    assert subject.contributors == [
        {
            "type": "Person",
            "id": "https://orcid.org/0000-0001-8448-4521",
            "contributorRoles": ["Author"],
            "givenName": "Nees Jan",
            "familyName": "van Eck",
            "affiliations": [
                {
                    "id": "https://ror.org/027bh9e22",
                    "name": "Leiden University",
                },
            ],
        },
        {
            "type": "Person",
            "contributorRoles": ["Author"],
            "givenName": "Ludo",
            "familyName": "Waltman",
        },
    ]

    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "doi_data.doi") == "10.59350/qc0px-76778"
    assert (
        py_.get(crossref_xml, "doi_data.resource")
        == "https://www.leidenmadtrics.nl/articles/an-open-approach-for-classifying-research-publications"
    )
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 2
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "ORCID": "https://orcid.org/0000-0001-8448-4521",
        "affiliations": {
            "institution": {
                "institution_id": {
                    "#text": "https://ror.org/027bh9e22",
                    "type": "ror",
                },
                "institution_name": "Leiden University",
            },
        },
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Nees Jan",
        "surname": "van Eck",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "An open approach for classifying research publications"
    )
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "Classifying research publications into research topics or research areas is crucial for many bibliometric analyses."
    )


@pytest.mark.vcr
def test_ghost_with_affiliations():
    "ghost with affiliations"
    string = "https://api.rogue-scholar.org/posts/57ed3097-a397-491e-90c0843d1e0102ac"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r796hz1-97aq74v-ag4f3"
    assert subject.type == "BlogPost"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "id": "https://orcid.org/0000-0003-1419-2405",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
        "affiliations": [
            {
                "id": "https://ror.org/04wxnsj81",
                "name": "DataCite",
            }
        ],
    }

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.write_errors is None
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Martin",
        "surname": "Fenner",
        "affiliations": {
            "institution": {
                "institution_name": "DataCite",
                "institution_id": {"type": "ror", "#text": "https://ror.org/04wxnsj81"},
            }
        },
        "ORCID": "https://orcid.org/0000-0003-1419-2405",
    }


@pytest.mark.vcr
def test_jsonfeed_with_organizational_author():
    """jsonfeed item with organizational author"""
    string = "https://api.rogue-scholar.org/posts/5561f8e4-2ff1-4186-a8d5-8dacb3afe414"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/2shz7-ehx26"
    assert subject.contributors == [
        {
            "id": "https://ror.org/0342dzm54",
            "type": "Organization",
            "contributorRoles": ["Author"],
            "name": "Liberate Science",
        }
    ]

    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "contributors.organization") == [
        {"#text": "Liberate Science", "contributor_role": "author", "sequence": "first"}
    ]
    assert (
        py_.get(crossref_xml, "titles.0.title") == "KU Leuven supports ResearchEquals"
    )
    assert len(py_.get(crossref_xml, "doi_data.collection.item")) == 5
    assert py_.get(crossref_xml, "doi_data.collection.item.0.resource") == {
        "#text": "https://libscie.org/ku-leuven-supports-researchequals",
        "mime_type": "text/html",
    }
    assert crossref_xml.get("group_title") == "Social science"


@pytest.mark.vcr
def test_jsonfeed_with_archived_content():
    """jsonfeed item with archived content"""
    string = "https://api.rogue-scholar.org/posts/570c8129-e867-49e6-8517-bd783627e76e"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/faeph-x4x84"
    assert (
        subject.url
        == "https://wayback.archive-it.org/22143/2023-11-03T19:24:18Z/https://project-thor.eu/2016/08/10/orcid-integration-in-pangaea"
    )

    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Markus",
        "surname": "Stocker",
        "ORCID": "https://orcid.org/0000-0001-5492-3212",
        "affiliations": {
            "institution": {
                "institution_id": {
                    "#text": "https://ror.org/04ers2y35",
                    "type": "ror",
                },
                "institution_name": "University of Bremen",
            },
        },
    }
    assert (
        py_.get(crossref_xml, "titles.0.title") == "ORCID Integration Series: PANGAEA"
    )
    assert len(py_.get(crossref_xml, "doi_data.collection.item")) == 5
    assert py_.get(crossref_xml, "doi_data.collection.item.0.resource") == {
        "mime_type": "text/html",
        "#text": "https://wayback.archive-it.org/22143/2023-11-03T19:24:18Z/https://project-thor.eu/2016/08/10/orcid-integration-in-pangaea",
    }
    assert crossref_xml.get("group_title") == "Computer and information sciences"


@pytest.mark.vcr
def test_jsonfeed_with_relations():
    """jsonfeed item with relations"""
    string = "https://api.rogue-scholar.org/posts/8a4de443-3347-4b82-b57d-e3c82b6485fc"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r79v4e1-97aq74v-ag578"
    assert subject.relations == [
        {"id": "https://doi.org/10.5438/bc11-cqw1", "type": "IsIdenticalTo"},
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    assert len(subject.references) == 1
    # assert subject.references[0] == {
    #     "key": "ref1",
    #     "doi": "https://doi.org/10.5281/zenodo.30799",
    #     "title": "D2.1: Artefact, Contributor, And Organisation Relationship Data Schema",
    #     "publicationYear": "2015",
    # }

    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "One of the first tasks for DataCite in the European Commission-funded THOR project"
    )
    # assert len(py_.get(crossref_xml, "citation_list.citation")) == 1
    # assert py_.get(crossref_xml, "citation_list.citation.0") == {
    #     "key": "ref1",
    #     "cYear": "2015",
    #     "article_title": "D2.1: Artefact, Contributor, And Organisation Relationship Data Schema",
    #     "doi": "10.5281/zenodo.30799",
    # }


@pytest.mark.vcr
def test_jsonfeed_with_relations_and_funding():
    """jsonfeed with relations and funding"""
    string = "https://api.rogue-scholar.org/posts/e58dc9c8-b870-4db2-8896-238b3246c551"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/r79s4nh-97aq74v-ag4t1"
    assert subject.type == "BlogPost"
    assert len(subject.references) == 3
    assert subject.references[0] == {
        "id": "https://doi.org/10.14454/3bpw-w381",
        "type": "ComputationalNotebook",
        "unstructured": "Fenner, M. (2019). <i>Jupyter Notebook FREYA PID Graph Key Performance Indicators (KPIs)</i> (1.1.0). DataCite. https://doi.org/10.14454/3bpw-w381",
    }
    assert subject.relations == [
        {"id": "https://doi.org/10.5438/bv9z-dc66", "type": "IsIdenticalTo"},
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://ror.org/00k4n6c32",
            "funderIdentifierType": "ROR",
            "awardUri": "https://doi.org/10.3030/777523",
            "awardNumber": "777523",
        }
    ]

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "citation_list.citation")) > 1
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "key": "ref1",
        "unstructured_citation": "Fenner, M. (2019). <i>Jupyter Notebook FREYA PID Graph Key Performance Indicators (KPIs)</i> (1.1.0). DataCite. https://doi.org/10.14454/3bpw-w381",
        "doi": "10.14454/3bpw-w381",
    }
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "The connections between scholarly resources generated by persistent identifiers (PIDs) and associated metadata form a graph"
    )
    assert py_.get(crossref_xml, "program.0.assertion") == [
        {"name": "ror", "#text": "https://ror.org/00k4n6c32"},
        {"name": "award_number", "#text": "777523"},
    ]
    assert py_.get(crossref_xml, "program.2") == {
        "name": "relations",
        "xmlns": OrderedDict([("rel", "http://www.crossref.org/relations.xsd")]),
        "related_item": [
            {
                "intra_work_relation": {
                    "relationship-type": "isIdenticalTo",
                    "identifier-type": "doi",
                    "#text": "10.5438/bv9z-dc66",
                }
            },
            {
                "inter_work_relation": {
                    "relationship-type": "isPartOf",
                    "identifier-type": "uri",
                    "#text": "https://rogue-scholar.org/api/communities/front_matter",
                },
            },
            {
                "inter_work_relation": {
                    "relationship-type": "isPartOf",
                    "identifier-type": "issn",
                    "#text": "2749-9952",
                }
            },
        ],
    }
    assert crossref_xml.get("group_title") == "Computer and information sciences"


@pytest.mark.vcr
def test_doi_with_multiple_funding_references():
    "DOI with multiple funding references"
    string = "10.7554/elife.01567"
    subject = Metadata(string, via="crossref")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"
    assert len(subject.funding_references) == 6
    assert subject.funding_references[3] == {
        "funderIdentifier": "https://ror.org/019whta54",
        "funderIdentifierType": "ROR",
        "funderName": "University of Lausanne",
    }
    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert len(py_.get(crossref_xml, "program.0.assertion")) == 6
    assert py_.get(crossref_xml, "program.0.assertion.3") == {
        "name": "ror",
        "#text": "https://ror.org/019whta54",
    }


@pytest.mark.vcr
def test_proceedings_article_with_multiple_funding_references():
    "ProceedingsArticle with multiple funding references"
    string = "10.1145/3448016.3452841"
    subject = Metadata(string, via="crossref")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1145/3448016.3452841"
    assert subject.type == "ProceedingsArticle"
    assert subject.publisher == {"name": "ACM"}
    assert subject.container == {
        "firstPage": "1386",
        "lastPage": "1399",
        "title": "Proceedings of the 2021 International Conference on Management of Data",
        "type": "Proceedings",
    }
    assert len(subject.funding_references) == 2
    assert subject.funding_references[0] == {
        "awardNumber": "CCF 805476, CCF 822388, CCF 1724745,CCF 1715777, CCF 1637458, IIS 1541613, CRII 1947789, CNS 1408695, CNS 1755615, CCF 1439084, CCF 1725543, CSR 1763680, CCF 1716252, CCF 1617618, CNS 1938709, IIS 1247726, CNS-1938709,CCF-1750472,CCF-1452904,CNS-1763680",
        "funderIdentifier": "https://ror.org/021nxhr62",
        "funderIdentifierType": "ROR",
        "funderName": "NSF (National Science Foundation)",
    }
    assert subject.funding_references[1] == {
        "awardNumber": "DE-AC02-05CH11231,17-SC-20-SC",
        "funderIdentifier": "https://ror.org/01bj3aw27",
        "funderIdentifierType": "ROR",
        "funderName": "DOE U.S. Department of Energy",
    }

    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.conference", {})
    assert py_.get(crossref_xml, "program.0.assertion") == [
        {"name": "ror", "#text": "https://ror.org/021nxhr62"},
        {"name": "award_number", "#text": "DE-AC02-05CH11231,17-SC-20-SC"},
    ]
    assert py_.get(crossref_xml, "program.1") == 1
    assert py_.get(crossref_xml, "program.2") == 1
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "Bacterial membrane lipids are critical for membrane bilayer formation"
    )


@pytest.mark.vcr
def test_inveniordm_record_with_references():
    "InvenioRDM record with references"
    string = "https://rogue-scholar.org/api/records/49yb9-h8k11"
    subject = Metadata(string, via="inveniordm")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.64000/wd6rx-vpq73"
    assert subject.type == "BlogPost"
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.container == {
        "identifier": "https://rogue-scholar.org/communities/crossref",
        "identifierType": "URL",
        "platform": "Hugo",
        "title": "Crossref Blog",
        "type": "Blog",
    }
    assert len(subject.references) == 2
    assert subject.references[0] == {
        "id": "https://en.wikipedia.org/wiki/Infrastructure_as_code",
        "unstructured": "projects, C. to W. (2016). <i>Infrastructure as code</i>. Wikimedia "
        "Foundation, Inc.",
    }
    assert subject.references[1] == {
        "id": "https://doi.org/10.64000/4s2ee-wkr84",
        "unstructured": "Bowman, S., Cousijn, H., Rittman, M., &amp; Stoll, L. (2025). The "
        "programs approach: our experiences during the first quarter of 2025. In "
        "<i>Crossref Blog</i>. Crossref.",
    }

    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 2
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "key": "ref1",
        "unstructured_citation": "projects, C. to W. (2016). <i>Infrastructure as code</i>. Wikimedia "
        "Foundation, Inc. https://en.wikipedia.org/wiki/Infrastructure_as_code",
    }
    assert py_.get(crossref_xml, "citation_list.citation.1") == {
        "doi": "10.64000/4s2ee-wkr84",
        "key": "ref2",
        "unstructured_citation": "Bowman, S., Cousijn, H., Rittman, M., &amp; Stoll, L. (2025). The "
        "programs approach: our experiences during the first quarter of 2025. In "
        "<i>Crossref Blog</i>. Crossref.",
    }
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "TLDR: We've successfully moved the main Crossref systems to the cloud!"
    )


@pytest.mark.vcr
def test_book():
    "book"
    string = "https://doi.org/10.1017/9781108348843"
    subject = Metadata(string, via="crossref")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1017/9781108348843"
    assert subject.type == "Book"

    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.book.book_metadata", {})
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Vincent S.",
        "surname": "Leung",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "The Politics of the Past in Early China"
    )
    assert py_.get(crossref_xml, "abstract") is None
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 273
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "key": "9781108348843#EMT-rl-1_BIBe-r-273",
        "volume": "5",
        "cYear": "1997",
        "article_title": "Lu Jia de lishi yishi ji qi wenhua yiyi",
    }


@pytest.mark.vcr
def test_book_chapter():
    "book_chapter"
    string = "https://doi.org/10.1007/978-3-662-46370-3_13"
    subject = Metadata(string, via="crossref")
    assert subject.id == "https://doi.org/10.1007/978-3-662-46370-3_13"
    assert subject.type == "BookChapter"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.book.book_metadata", {})
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Ronald L.",
        "surname": "Diercks",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Clinical Symptoms and Physical Examinations"
    )
    assert py_.get(crossref_xml, "abstract") is None
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 22
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "key": "13_CR1",
        "doi": "10.1007/s00256-012-1391-8",
        "volume": "41",
        "cYear": "2012",
        "unstructured_citation": "Ahn KS, Kang CH, Oh YW, Jeong WK. Correlation between magnetic resonance imaging and clinical impairment in patients with adhesive capsulitis. Skeletal Radiol. 2012;41(10):1301–8.",
    }


@pytest.mark.vcr
def test_dataset():
    "dataset"
    string = "https://doi.org/10.2210/pdb4hhb/pdb"
    subject = Metadata(string, via="crossref")
    assert subject.id == "https://doi.org/10.2210/pdb4hhb/pdb"
    assert subject.type == "Dataset"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(
        crossref_xml, "doi_batch.body.database.component_list.component", {}
    )
    assert py_.get(crossref_xml, "parent_relation") == "isPartOf"
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "THE CRYSTAL STRUCTURE OF HUMAN DEOXYHAEMOGLOBIN AT 1.74 ANGSTROMS RESOLUTION"
    )
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 2
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "G.",
        "surname": "Fermi",
    }
    assert py_.get(crossref_xml, "publication_date") == {
        "day": "7",
        "month": "3",
        "year": "1984",
        "media_type": "online",
    }
    assert py_.get(crossref_xml, "doi_data.doi") == "10.2210/pdb4hhb/pdb"
    assert (
        py_.get(crossref_xml, "doi_data.resource")
        == "https://www.wwpdb.org/pdb?id=pdb_00004hhb"
    )


@pytest.mark.vcr
def test_component():
    "component"
    string = "https://doi.org/10.1371/journal.pmed.0030277.g001"
    subject = Metadata(string, via="crossref")
    assert subject.id == "https://doi.org/10.1371/journal.pmed.0030277.g001"
    assert subject.type == "Component"

    crossref_xml = subject.write(to="crossref_xml")
    assert not subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})


@pytest.mark.vcr
def test_peer_review():
    "peer review"
    string = "https://doi.org/10.7554/elife.55167.sa2"
    subject = Metadata(string, via="crossref")
    assert subject.id == "https://doi.org/10.7554/elife.55167.sa2"
    assert subject.type == "PeerReview"
    assert subject.date == {"published": "2020-04-29"}

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.peer_review", {})
    assert py_.get(crossref_xml, "type") == "author-comment"
    assert py_.get(crossref_xml, "stage") == "pre-publication"
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 8
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Jeremy",
        "surname": "Magland",
        "ORCID": "https://orcid.org/0000-0002-5286-4375",
        "affiliations": {
            "institution": {
                "institution_name": "Center for Computational Mathematics, Flatiron Institute",
            },
        },
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Author response: SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters"
    )
    assert py_.get(crossref_xml, "review_date") == {
        "day": "29",
        "month": "4",
        "year": "2020",
    }


@pytest.mark.vcr
def test_dissertation():
    "dissertation"
    string = "https://doi.org/10.14264/uql.2020.791"
    subject = Metadata(string, via="crossref")
    assert subject.id == "https://doi.org/10.14264/uql.2020.791"
    assert subject.type == "Dissertation"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.dissertation", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Patricia Maree",
        "surname": "Collingwood",
        "ORCID": "https://orcid.org/0000-0003-3086-4443",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers"
    )
    assert py_.get(crossref_xml, "approval_date") == {
        "day": "8",
        "month": "6",
        "year": "2020",
    }
    assert py_.get(crossref_xml, "doi_data.doi") == "10.14264/uql.2020.791"
    assert (
        py_.get(crossref_xml, "doi_data.resource")
        == "http://espace.library.uq.edu.au/view/UQ:23a1e74"
    )


@pytest.mark.vcr
def test_arxiv():
    "arxiv preprint"
    string = "https://doi.org/10.48550/arXiv.2311.16162"
    subject = Metadata(string, via="datacite")
    assert subject.id == "https://doi.org/10.48550/arxiv.2311.16162"
    assert subject.type == "Article"

    crossref_xml = subject.write(to="crossref_xml")
    assert subject.is_valid
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "language") is None
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 10
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Hui",
        "surname": "Yin",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Leveraging Artificial Intelligence Technology for Mapping Research to Sustainable Development Goals: A Case Study"
    )
    assert py_.get(crossref_xml, "posted_date") == {
        "day": "13",
        "month": "8",
        "year": "2023",
    }
    assert py_.get(crossref_xml, "abstract.0.p").startswith(
        "The number of publications related to the Sustainable Development Goals (SDGs) continues to grow."
    )
    assert py_.get(crossref_xml, "program.0.license_ref") == [
        {
            "applies_to": "vor",
            "#text": "https://creativecommons.org/licenses/by/4.0/legalcode",
        },
        {
            "applies_to": "tdm",
            "#text": "https://creativecommons.org/licenses/by/4.0/legalcode",
        },
    ]
    assert py_.get(crossref_xml, "doi_data.doi") == "10.48550/arxiv.2311.16162"
    assert (
        py_.get(crossref_xml, "doi_data.resource") == "https://arxiv.org/abs/2311.16162"
    )


@pytest.mark.vcr
def test_archived():
    "archived"
    string = "https://doi.org/10.5694/j.1326-5377.1943.tb44329.x"
    subject = Metadata(string, via="crossref")
    assert subject.id == "https://doi.org/10.5694/j.1326-5377.1943.tb44329.x"
    assert subject.type == "JournalArticle"

    # crossref_xml = subject.write(to="crossref_xml")
    # assert subject.is_valid
    # crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    # crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    # assert py_.get(crossref_xml, "language") == "en"
    # assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    # assert py_.get(crossref_xml, "contributors.person_name.0") == {
    #     "contributor_role": "author",
    #     "sequence": "first",
    #     "given_name": "H.",
    #     "surname": "Baker",
    # }
    # assert (
    #     py_.get(crossref_xml, "titles.0.title")
    #     == "A case of acute yellow atrophy of the liver"
    # )
    # assert py_.get(crossref_xml, "publication_date") == {
    #     "day": "1",
    #     "month": "1",
    #     "year": "1943",
    #     "media_type": "online",
    # }
    # assert py_.get(crossref_xml, "doi_data.doi") == "10.5694/j.1326-5377.1943.tb44329.x"
    # assert (
    #     py_.get(crossref_xml, "doi_data.resource")
    #     == "https://www.mja.com.au/journal/1943/1/1/case-acute-yellow-atrophy-liver"
    # )
