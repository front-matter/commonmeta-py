"""Test crossref_xml_writer module for commonmeta-py"""

import pytest
from os import path
import pydash as py_
import re
from collections import OrderedDict

from commonmeta import Metadata, MetadataList
from commonmeta.base_utils import parse_xml


def test_write_crossref_xml_header():
    """Write crossref_xml header"""
    string = "https://doi.org/10.1371/journal.pone.0000030"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    lines = subject.write(to="crossref_xml").decode().split("\n")
    assert lines[0] == '<?xml version="1.0" encoding="UTF-8"?>'
    assert (
        lines[1]
        == '<doi_batch xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.crossref.org/schema/5.3.1" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:fr="http://www.crossref.org/fundref.xsd" xmlns:mml="http://www.w3.org/1998/Math/MathML" xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 https://www.crossref.org/schemas/crossref5.3.1.xsd" version="5.3.1">'
    )


def test_write_metadata_as_crossref_xml():
    """Write metadata as crossref_xml"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    crossref_xml = subject.write(to="crossref_xml")
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert py_.get(crossref_xml, "doi_data.doi") == "10.7554/elife.01567"
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 26
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
    crossref_xml_list = parse_xml(
        subject_list.write(to="crossref_xml"), dialect="crossref"
    )
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


@pytest.mark.vcr
def test_write_commonmeta_list_as_crossref_xml():
    """write_commonmeta_list crossref_xml"""
    string = path.join(path.dirname(__file__), "fixtures", "json_feed.json")
    subject_list = MetadataList(string)
    assert len(subject_list.items) == 15
    crossref_xml_list = parse_xml(
        subject_list.write(to="crossref_xml"), dialect="crossref"
    )
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


@pytest.mark.vcr
def test_write_crossref_xml_journal_article_plos():
    """Write crossref_xml journal article plos"""
    string = "https://doi.org/10.1371/journal.pone.0000030"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert py_.get(crossref_xml, "doi_data.doi") == "10.1371/journal.pone.0000030"
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 67
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


@pytest.mark.vcr
def test_write_crossref_xml_posted_content():
    """Write crossref_xml posted_content"""
    string = "https://doi.org/10.1101/2020.12.01.406702"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1101/2020.12.01.406702"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "doi_data.doi") == "10.1101/2020.12.01.406702"
    assert (
        py_.get(crossref_xml, "doi_data.resource")
        == "http://biorxiv.org/lookup/doi/10.1101/2020.12.01.406702"
    )


@pytest.mark.vcr
def test_write_crossref_journal_article_from_datacite():
    """Write crossref_xml journal article from datacite"""
    string = "10.2312/geowissenschaften.1989.7.181"
    subject = Metadata(string, via="datacite")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.2312/geowissenschaften.1989.7.181"
    assert subject.descriptions == [
        {"description": "Die Geowissenschaften", "type": "Other"}
    ]
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
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


#       expect(subject.valid?).to be false
#       expect(subject.errors).to eq(["property '/descriptions/0' is missing required keys: description"])


@pytest.mark.vcr
def test_write_crossref_schema_org_front_matter():
    """Write crossref_xml schema_org front_matter"""
    string = "https://blog.front-matter.io/posts/editorial-by-more-than-200-call-for-emergency-action-to-limit-global-temperature-increases-restore-biodiversity-and-protect-health"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r9nqx6h-97aq74v-ag7bw"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Editorial by more than 200 health journals: Call for emergency action to limit global temperature increases, restore biodiversity, and protect health"
    )


@pytest.mark.vcr
def test_write_crossref_another_schema_org_front_matter():
    """Write crossref_xml another schema_org front_matter"""
    string = "https://blog.front-matter.io/posts/dryad-interview-jen-gibson"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/rceh7pn-tzg61kj-7zv63"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert py_.get(crossref_xml, "titles.0.title") == "Dryad: Interview with Jen Gibson"


@pytest.mark.vcr
def test_write_crossref_embedded_schema_org_front_matter():
    """Write crossref_xml embedded schema_org front_matter"""
    string = path.join(
        path.dirname(__file__), "fixtures", "schema_org_front-matter.json"
    )
    subject = Metadata(string, via="schema_org")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r9nqx6h-97aq74v-ag7bw"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
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


def test_write_crossref_xml_missing_doi():
    """Write crossref_xml missing doi"""
    string = path.join(path.dirname(__file__), "fixtures", "json_feed_item_no_id.json")
    subject = Metadata(string, via="json_feed_item")
    assert subject.is_valid
    assert re.match(r"\A(https://doi\.org/10\.59350/.+)\Z", subject.id)
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2993-1150", "type": "IsPartOf"}
    ]
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert re.match(r"\A(10\.59350/.+)\Z", py_.get(crossref_xml, "doi_data.doi"))
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "ORCID": "https://orcid.org/0000-0003-0449-4469",
        "sequence": "first",
        "given_name": "Tejas S.",
        "surname": "Sathe",
    }
    assert py_.get(crossref_xml, "titles.0.title") == "The Residency Visual Abstract"
    assert py_.get(crossref_xml, "program.1") == {
        "name": "relations",
        "xmlns": OrderedDict([("", "http://www.crossref.org/relations.xsd")]),
        "related_item": {
            "inter_work_relation": {
                "relationship-type": "isPartOf",
                "identifier-type": "issn",
                "#text": "2993-1150",
            }
        },
    }


def test_write_crossref_xml_missing_doi_no_prefix():
    """Write crossref_xml missing doi no prefix"""
    string = path.join(
        path.dirname(__file__), "fixtures", "json_feed_item_no_prefix.json"
    )
    subject = Metadata(string, via="json_feed_item")
    assert subject.is_valid
    assert subject.id == "https://www.ideasurg.pub/residency-visual-abstract"
    crossref_xml = subject.write(to="crossref_xml")
    assert subject.write_errors == "None is not of type 'string'"
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    assert py_.get(crossref_xml, "doi_batch.body") is None


@pytest.mark.vcr
def test_write_crossref_schema_org_from_another_science_blog():
    """Write crossref_xml schema_org from another science blog"""
    string = "https://donnywinston.com/posts/implementing-the-fair-principles-through-fair-enabling-artifacts-and-services/"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.57099/11h5yt3819"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
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


@pytest.mark.vcr
def test_write_crossref_schema_org_upstream_blog():
    """Write crossref_xml schema_org upstream blog"""
    string = "https://upstream.force11.org/deep-dive-into-ethics-of-contributor-roles/"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/rf84ag3-98f00rt-0phta"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
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


@pytest.mark.vcr
def test_json_feed_item_upstream_blog():
    """json_feed_item upstream blog"""
    string = "https://api.rogue-scholar.org/posts/5d14ffac-b9ac-4e20-bdc0-d9248df4e80d"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/n6dnt-xpq48"
    assert subject.type == "Article"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
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
    assert len(py_.get(crossref_xml, "doi_data.collection.item")) == 5
    assert py_.get(crossref_xml, "doi_data.collection.item.0.resource") == {
        "#text": "https://upstream.force11.org/attempts-at-automating-journal-subject-classification",
        "mime_type": "text/html",
    }
    assert py_.get(crossref_xml, "doi_data.collection.item.1.resource") == {
        "#text": "https://api.rogue-scholar.org/posts/10.54900/n6dnt-xpq48.md",
        "mime_type": "text/plain",
    }
    assert crossref_xml.get("group_title") == "Humanities"


@pytest.mark.vcr
def test_json_feed_item_with_references():
    """json_feed_item with references"""
    string = "https://api.rogue-scholar.org/posts/954f8138-0ecd-4090-87c5-cef1297f1470"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/zwm7q-vet94"
    assert subject.subjects == [{"subject": "Humanities"}]
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 2
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "ORCID": "https://orcid.org/0000-0001-5934-7525",
        "sequence": "first",
        "given_name": "Daniel S.",
        "surname": "Katz",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "The Research Software Alliance (ReSA)"
    )
    assert len(py_.get(crossref_xml, "citation_list.citation")) > 5
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "key": "ref1",
        "unstructured_citation": "https://www.software.ac.uk/blog/2014-12-04-its-impossible-conduct-research-without-software-say-7-out-10-uk-researchers",
    }
    assert crossref_xml.get("group_title") == "Humanities"


@pytest.mark.vcr
def test_json_feed_item_with_doi():
    """JSON Feed item with DOI"""
    string = "https://api.rogue-scholar.org/posts/1c578558-1324-4493-b8af-84c49eabc52f"
    subject = Metadata(string, doi="10.59350/9ry27-7cz42")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/9ry27-7cz42"
    assert subject.subjects == [{"subject": "Social sciences"}]
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Heinz",
        "surname": "Pampel",
        "ORCID": "https://orcid.org/0000-0003-3334-2771",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "EU-Mitgliedstaaten betonen die Rolle von wissenschaftsgeleiteten Open-Access-Modellen jenseits von APCs"
    )
    assert len(py_.get(crossref_xml, "doi_data.collection.item")) == 5
    assert py_.get(crossref_xml, "doi_data.collection.item.0.resource") == {
        "#text": "https://wisspub.net/2023/05/23/eu-mitgliedstaaten-betonen-die-rolle-von-wissenschaftsgeleiteten-open-access-modellen-jenseits-von-apcs",
        "mime_type": "text/html",
    }
    assert py_.get(crossref_xml, "doi_data.collection.item.1.resource") == {
        "#text": "https://api.rogue-scholar.org/posts/10.59350/9ry27-7cz42.md",
        "mime_type": "text/plain",
    }
    assert crossref_xml.get("group_title") == "Social sciences"


@pytest.mark.vcr
def test_json_feed_item_without_doi():
    """JSON Feed item without DOI"""
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
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
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


@pytest.mark.vcr
def test_ghost_with_affiliations():
    "ghost with affiliations"
    string = "https://api.rogue-scholar.org/posts/57ed3097-a397-491e-90c0843d1e0102ac"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r796hz1-97aq74v-ag4f3"
    assert subject.type == "Article"
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
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
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
def test_json_feed_item_with_organizational_author():
    """JSON Feed item with organizational author"""
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
    print(subject.write(to="crossref_xml"))
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.organization")) == 1
    assert py_.get(crossref_xml, "contributors.organization.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "#text": "Liberate Science",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title") == "KU Leuven supports ResearchEquals"
    )
    assert len(py_.get(crossref_xml, "doi_data.collection.item")) == 5
    assert py_.get(crossref_xml, "doi_data.collection.item.0.resource") == {
        "mime_type": "text/html",
        "#text": "https://libscie.org/ku-leuven-supports-researchequals",
    }
    assert crossref_xml.get("group_title") == "Social sciences"


@pytest.mark.vcr
def test_json_feed_item_with_archived_content():
    """JSON Feed item with archived content"""
    string = "https://api.rogue-scholar.org/posts/570c8129-e867-49e6-8517-bd783627e76e"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/faeph-x4x84"
    assert (
        subject.url == "https://project-thor.eu/2016/08/10/orcid-integration-in-pangaea"
    )
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
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
        "#text": "https://project-thor.eu/2016/08/10/orcid-integration-in-pangaea",
    }
    assert crossref_xml.get("group_title") == "Computer and information sciences"


@pytest.mark.vcr
def test_json_feed_item_with_relations():
    """JSON Feed item with relations"""
    string = "https://api.rogue-scholar.org/posts/8a4de443-3347-4b82-b57d-e3c82b6485fc"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r79v4e1-97aq74v-ag578"
    assert subject.relations == [
        {"id": "https://doi.org/10.5438/bc11-cqw1", "type": "IsIdenticalTo"},
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    # assert len(subject.references) == 1
    # assert subject.references[0] == {
    #     "key": "ref1",
    #     "doi": "https://doi.org/10.5281/zenodo.30799",
    #     "title": "D2.1: Artefact, Contributor, And Organisation Relationship Data Schema",
    #     "publicationYear": "2015",
    # }
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    # assert len(py_.get(crossref_xml, "citation_list.citation")) == 1
    # assert py_.get(crossref_xml, "citation_list.citation.0") == {
    #     "key": "ref1",
    #     "cYear": "2015",
    #     "article_title": "D2.1: Artefact, Contributor, And Organisation Relationship Data Schema",
    #     "doi": "10.5281/zenodo.30799",
    # }


@pytest.mark.vcr
def test_json_feed_item_with_relations_and_funding():
    """JSON Feed item with relations and funding"""
    string = "https://api.rogue-scholar.org/posts/e58dc9c8-b870-4db2-8896-238b3246c551"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r79s4nh-97aq74v-ag4t1"
    # assert len(subject.references) == 3
    # assert subject.references[0] == {
    #     "key": "ref1",
    #     "doi": "https://doi.org/10.5281/zenodo.30799",
    #     "title": "D2.1: Artefact, Contributor, And Organisation Relationship Data Schema",
    #     "publicationYear": "2015",
    # }
    assert subject.relations == [
        {"id": "https://doi.org/10.5438/bv9z-dc66", "type": "IsIdenticalTo"},
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://doi.org/10.13039/501100000780",
            "funderIdentifierType": "Crossref Funder ID",
            "award_uri": "https://doi.org/10.3030/777523",
            "awardNumber": "777523",
        }
    ]
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    # assert len(py_.get(crossref_xml, "citation_list.citation")) > 1
    # assert py_.get(crossref_xml, "citation_list.citation.0") == {
    #     "key": "ref1",
    #     "cYear": "2019",
    #     "article_title": "Jupyter Notebook FREYA PID Graph Key Performance Indicators (KPIs)",
    #     "doi": "10.14454/3bpw-w381",
    # }
    assert py_.get(crossref_xml, "program.0") == {
        "name": "fundref",
        "xmlns": {"": "http://www.crossref.org/fundref.xsd"},
        "assertion": {
            "name": "fundgroup",
            "assertion": [
                {
                    "name": "funder_name",
                    "assertion": {
                        "name": "funder_identifier",
                        "#text": "https://doi.org/10.13039/501100000780",
                    },
                    "#text": "European Commission",
                },
                {"name": "award_number", "#text": "777523"},
            ],
        },
    }
    assert py_.get(crossref_xml, "program.2") == {
        "name": "relations",
        "xmlns": OrderedDict([("", "http://www.crossref.org/relations.xsd")]),
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
                    "identifier-type": "issn",
                    "#text": "2749-9952",
                }
            },
        ],
    }
    assert crossref_xml.get("group_title") == "Computer and information sciences"


@pytest.mark.vcr
def test_json_feed_item_with_anonymous_author():
    """JSON Feed item with anonymous author"""
    string = "https://api.rogue-scholar.org/posts/a163e340-5b3c-4736-9ab0-8c54fdff6a3c"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/33es7-fqz31"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Mathias",
        "surname": "Göbel",
    }
    assert crossref_xml.get("group_title") == "Computer and information sciences"


@pytest.mark.vcr
def test_json_feed_item_with_references():
    """JSON Feed item with references"""
    string = "https://api.rogue-scholar.org/posts/525a7d13-fe07-4cab-ac54-75d7b7005647"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/dn2mm-m9q51"
    assert subject.relations is None
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.person_name")) == 1
    assert py_.get(crossref_xml, "contributors.person_name.0") == {
        "contributor_role": "author",
        "sequence": "first",
        "given_name": "Mark",
        "surname": "Dingemanse",
    }


@pytest.mark.vcr
def test_software():
    """software"""
    string = "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.1184077"
    assert subject.url == "https://github.com/citation-file-format/ruby-cff"
    assert subject.type == "Software"
    crossref_xml = parse_xml(subject.write(to="crossref_xml"), dialect="crossref")
    assert py_.get(crossref_xml, "doi_batch.body") is None
    assert (
        subject.write_errors
        == "None is not one of ['BookChapter', 'BookPart', 'BookSection', 'BookSeries', 'BookSet', 'BookTrack', 'Book', 'Component', 'Database', 'Dataset', 'Dissertation', 'EditedBook', 'Entry', 'Grant', 'JournalArticle', 'JournalIssue', 'JournalVolume', 'Journal', 'Monograph', 'Other', 'PeerReview', 'PostedContent', 'ProceedingsArticle', 'ProceedingsSeries', 'Proceedings', 'ReferenceBook', 'ReferenceEntry', 'ReportComponent', 'ReportSeries', 'Report', 'Standard']"
    )
