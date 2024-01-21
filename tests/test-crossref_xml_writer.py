"""Test crossref_xml_writer module for commonmeta-py"""
import pytest
from os import path
import pydash as py_

from commonmeta import Metadata
from commonmeta.base_utils import parse_xml, wrap


def test_write_crossref_xml_header():
    """Write crossref_xml header"""
    string = "https://doi.org/10.1371/journal.pone.0000030"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    lines = subject.crossref_xml().decode().split("\n")
    assert lines[0] == "<?xml version='1.0' encoding='UTF-8'?>"
    assert lines[1] == '<doi_batch xmlns="http://www.crossref.org/schema/5.3.1" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:fr="http://www.crossref.org/fundref.xsd" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="5.3.1" xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 https://www.crossref.org/schemas/crossref5.3.1.xsd">'
    
    
def test_write_metadata_as_crossref_xml():
    """Write metadata as crossref_xml"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    crossref_xml = subject.crossref_xml()
    crossref_xml = parse_xml(crossref_xml, dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert py_.get(crossref_xml, "doi_data.doi") == "10.7554/elife.01567"
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 27
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "@key": "bib1",
        "volume": "426",
        "cYear": "2003",
        "article_title": "APL regulates vascular tissue identity in Arabidopsis",
        "doi": "10.1038/nature02100",
    }


@pytest.mark.vcr
def test_write_crossref_xml_journal_article_plos():
    """Write crossref_xml journal article plos"""
    string = "https://doi.org/10.1371/journal.pone.0000030"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert py_.get(crossref_xml, "doi_data.doi") == "10.1371/journal.pone.0000030"
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 73
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    )
    assert len(crossref_xml.get("contributors")) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name.0") == {
        "@contributor_role": "author",
        "given_name": "Markus",
        "@sequence": "first",
        "surname": "Ralser",
    }


@pytest.mark.vcr
def test_write_crossref_xml_posted_content():
    """Write crossref_xml posted_content"""
    string = "https://doi.org/10.1101/2020.12.01.406702"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1101/2020.12.01.406702"
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
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
        {"description": "Die Geowissenschaften", "descriptionType": "SeriesInformation"}
    ]
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.journal.journal_article", {})
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "An Overview of the Geology of Canadian Gold Occurrences"
    )
    assert len(crossref_xml.get("contributors")) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name") == {
        "@contributor_role": "author",
        "@sequence": "first",
        "given_name": "David J",
        "surname": "Mossman",
    }


#       expect(subject.valid?).to be false
#       expect(subject.errors).to eq(["property '/descriptions/0' is missing required keys: description"])


@pytest.mark.vcr
def test_write_crossref_schema_org_front_matter():
    """Write crossref_xml schema_org front_matter"""
    string = "https://blog.front-matter.io/posts/editorial-by-more-than-200-call-for-emergency-action-to-limit-global-temperature-increases-restore-biodiversity-and-protect-health"
    subject = Metadata(string, via="schema_org")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r9nqx6h-97aq74v-ag7bw"
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Editorial by more than 200 health journals: Call for emergency action to limit global temperature increases, restore biodiversity, and protect health"
    )


@pytest.mark.vcr
def test_write_crossref_another_schema_org_front_matter():
    """Write crossref_xml another schema_org front_matter"""
    string = "https://blog.front-matter.io/posts/dryad-interview-jen-gibson"
    subject = Metadata(string, via="schema_org")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/rceh7pn-tzg61kj-7zv63"
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
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
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(wrap(crossref_xml.get("contributors"))) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name") == {
        "@contributor_role": "author",
        "ORCID": "https://orcid.org/0000-0003-1419-2405",
        "@sequence": "first",
        "given_name": "Martin",
        "surname": "Fenner",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "Editorial by more than 200 health journals: Call for emergency action to limit global temperature increases, restore biodiversity, and protect health"
    )


@pytest.mark.vcr
def test_write_crossref_schema_org_from_another_science_blog():
    """Write crossref_xml schema_org from another science blog"""
    string = "https://donnywinston.com/posts/implementing-the-fair-principles-through-fair-enabling-artifacts-and-services/"
    subject = Metadata(string, via="schema_org")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.57099/11h5yt3819"
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(wrap(crossref_xml.get("contributors"))) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name") == {
        "@contributor_role": "author",
        "@sequence": "first",
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
    subject = Metadata(string, via="schema_org")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/rf84ag3-98f00rt-0phta"
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(crossref_xml.get("contributors")) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name.0") == {
        "@contributor_role": "author",
        "@sequence": "first",
        "given_name": "Mohammad",
        "surname": "Hosseini",
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
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(crossref_xml.get("contributors")) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name") == {
        "@contributor_role": "author",
        "@sequence": "first",
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
        "@item_number_type": "uuid",
    }
    assert len(py_.get(crossref_xml, "doi_data.item")) == 1
    assert py_.get(crossref_xml, "doi_data.item.0.resource") == {
        "#text": "https://upstream.force11.org/attempts-at-automating-journal-subject-classification",
        "@mime_type": "text/html",
    }


@pytest.mark.vcr
def test_json_feed_item_with_references():
    """json_feed_item with references"""
    string = "https://api.rogue-scholar.org/posts/954f8138-0ecd-4090-87c5-cef1297f1470"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/zwm7q-vet94"
    assert subject.subjects == [{"subject": "Humanities"}]
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "contributors.0.person_name")) == 2
    assert py_.get(crossref_xml, "contributors.0.person_name.0") == {
        "@contributor_role": "author",
        "ORCID": "https://orcid.org/0000-0001-5934-7525",
        "@sequence": "first",
        "given_name": "Daniel S.",
        "surname": "Katz",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "The Research Software Alliance (ReSA)"
    )
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 11
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "@key": "ref1",
        "unstructured_citation": "https://www.software.ac.uk/blog/2014-12-04-its-impossible-conduct-research-without-software-say-7-out-10-uk-researchers",
    }


@pytest.mark.vcr
def test_json_feed_item_with_doi():
    """JSON Feed item with DOI"""
    string = "https://api.rogue-scholar.org/posts/1c578558-1324-4493-b8af-84c49eabc52f"
    subject = Metadata(string, doi="10.59350/9ry27-7cz42")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/9ry27-7cz42"
    assert subject.subjects == [{"subject": "Social sciences"}]
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(crossref_xml.get("contributors")) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name") == {
        "@contributor_role": "author",
        "@sequence": "first",
        "given_name": "Heinz",
        "surname": "Pampel",
        "ORCID": "https://orcid.org/0000-0003-3334-2771",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title")
        == "EU-Mitgliedstaaten betonen die Rolle von wissenschaftsgeleiteten Open-Access-Modellen jenseits von APCs"
    )
    assert py_.get(crossref_xml, "doi_data.item.0") == {
        "resource": {
            "#text": "https://wisspub.net/2023/05/23/eu-mitgliedstaaten-betonen-die-rolle-von-wissenschaftsgeleiteten-open-access-modellen-jenseits-von-apcs",
            "@mime_type": "text/html",
        }
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
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(crossref_xml.get("contributors")) == 1
    assert py_.get(crossref_xml, "contributors.0.organization") == {
        "@contributor_role": "author",
        "@sequence": "first",
        "#text": "Liberate Science",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title") == "KU Leuven supports ResearchEquals"
    )
    assert py_.get(crossref_xml, "doi_data.item.0") == {
        "resource": {
            "@mime_type": "text/html",
            "#text": "https://libscie.org/ku-leuven-supports-researchequals",
        }
    }


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
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(crossref_xml.get("contributors")) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name") == {
        "@contributor_role": "author",
        "@sequence": "first",
        "given_name": "Markus",
        "surname": "Stocker",
        "ORCID": "https://orcid.org/0000-0001-5492-3212",
    }
    assert (
        py_.get(crossref_xml, "titles.0.title") == "ORCID Integration Series: PANGAEA"
    )
    assert py_.get(crossref_xml, "doi_data.item.0") == {
        "resource": {
            "@mime_type": "text/html",
            "#text": "https://project-thor.eu/2016/08/10/orcid-integration-in-pangaea",
        }
    }


@pytest.mark.vcr
def test_json_feed_item_with_relations():
    """JSON Feed item with relations"""
    string = "https://api.rogue-scholar.org/posts/8a4de443-3347-4b82-b57d-e3c82b6485fc"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r79v4e1-97aq74v-ag578"
    assert subject.related_identifiers == [
        {"id": "https://doi.org/10.5438/bc11-cqw1", "type": "IsIdenticalTo"}
    ]
    assert subject.references == [
        {"doi": "https://doi.org/10.5281/zenodo.30799", "key": "ref1"}
    ]
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 1
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "@key": "ref1",
        "doi": "10.5281/zenodo.30799",
    }


@pytest.mark.vcr
def test_json_feed_item_with_relations_and_funding():
    """JSON Feed item with relations and funding"""
    string = "https://api.rogue-scholar.org/posts/e58dc9c8-b870-4db2-8896-238b3246c551"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r79s4nh-97aq74v-ag4t1"
    assert subject.related_identifiers == [
        {"id": "https://doi.org/10.5438/bv9z-dc66", "type": "IsIdenticalTo"}
    ]
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://doi.org/10.13039/501100000780",
            "funderIdentifierType": "Crossref Funder ID",
            "awardNumber": "777523",
        }
    ]
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    assert len(py_.get(crossref_xml, "citation_list.citation")) == 3
    assert py_.get(crossref_xml, "citation_list.citation.0") == {
        "@key": "ref1",
        "doi": "10.14454/3bpw-w381",
    }
    assert py_.get(crossref_xml, "program.0") == {
        "@name": "fundref",
        "@xmlns": {"": "http://www.crossref.org/fundref.xsd"},
        "assertion": {
            "@name": "fundgroup",
            "assertion": [
                {
                    "@name": "funder_name",
                    "assertion": {
                        "@name": "funder_identifier",
                        "#text": "https://doi.org/10.13039/501100000780",
                    },
                    "#text": "European Commission",
                },
                {"@name": "award_number", "#text": "777523"},
            ],
        },
    }


@pytest.mark.vcr
def test_json_feed_item_with_anonymous_author():
    """JSON Feed item with anonymous author"""
    string = "https://api.rogue-scholar.org/posts/a163e340-5b3c-4736-9ab0-8c54fdff6a3c"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/33es7-fqz31"
    crossref_xml = parse_xml(subject.crossref_xml(), dialect="crossref")
    print(crossref_xml)
    crossref_xml = py_.get(crossref_xml, "doi_batch.body.posted_content", {})
    print(crossref_xml)
    assert len(crossref_xml.get("contributors")) == 1
    assert py_.get(crossref_xml, "contributors.0.person_name") == {
        "@contributor_role": "author",
        "@sequence": "first",
        "given_name": "Mathias",
        "surname": "Göbel",
    }
