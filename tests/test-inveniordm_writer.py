# pylint: disable=invalid-name
"""InvenioRDM writer tests"""

import re
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import orjson as json
import pytest
from conftest import image_response, offline_url_fetcher, sample_metadata
from requests.exceptions import RequestException

import commonmeta
from commonmeta import Metadata
from commonmeta.base_utils import dig
from commonmeta.io_utils import (
    read_pdf_attachment,
    read_pdf_metadata,
    to_pdf_content,
    to_pdf_html,
    to_pdf_text,
    write_pdf_rendition,
)
from commonmeta.writers.inveniordm_writer import record_matches, upsert_record

PDF_RESOURCES = Path(commonmeta.__file__).parent / "resources" / "pdf"


def assert_pdf_metadata(pdf: bytes, subject: Metadata) -> dict:
    """The rendition carries the record's identity, byline and terms.

    Read back out of the pdf rather than off the record, so this covers the
    whole round trip: the meta tags and the xmp fragment the writer builds,
    what WeasyPrint makes of them, and `read_pdf_metadata` reading them again.
    """
    metadata = read_pdf_metadata(pdf)
    authors = [
        contributor
        for contributor in subject.contributors or []
        if "Author" in (contributor.get("roles") or [])
    ]
    person = authors[0].get("person") or {}
    first = " ".join(
        name for name in (person.get("given_name"), person.get("family_name")) if name
    ) or (authors[0].get("organization") or {}).get("name")

    assert metadata["id"] == subject.id
    # a pdf's own metadata is text: the markup a title or a description
    # carries is rendered on the page, not repeated here
    assert metadata["title"] == to_pdf_text(subject.title)
    assert len(metadata["authors"]) == len(authors)
    assert metadata["authors"][0] == first
    assert metadata.get("license") == (subject.license or {}).get("id")
    assert metadata.get("description") == to_pdf_text(subject.description)
    return metadata


@pytest.mark.vcr
def test_publication():
    "publication"
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.5281/zenodo.5244404"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-article"
    assert len(dig(inveniordm, "metadata.creators")) == 21
    assert dig(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Holmes",
            "given_name": "Edward C",
            "name": "Holmes, Edward C",
            "type": "personal",
        },
        "affiliations": [
            {
                "name": "School of Life and Environmental Sciences and School of Medical Sciences, The University of Sydney, Sydney, NSW 2006, Australia"
            }
        ],
    }
    assert (
        dig(inveniordm, "metadata.title")
        == "The Origins of SARS-CoV-2: A Critical Review"
    )
    assert dig(inveniordm, "metadata.publisher") == "Zenodo"
    assert dig(inveniordm, "metadata.publication_date") == "2021-08-18"
    assert dig(inveniordm, "metadata.languages.0.id") is None
    assert dig(inveniordm, "metadata.version") == "Authors' final version"
    assert dig(inveniordm, "metadata.description").startswith(
        "The Origins of SARS-CoV-2: A Critical Review"
    )
    assert dig(inveniordm, "metadata.rights") == [{"id": "cc-by-nc-nd-4.0"}]
    assert dig(inveniordm, "metadata.identifiers") == [
        {"identifier": "https://zenodo.org/records/5244404", "scheme": "url"}
    ]
    assert dig(inveniordm, "metadata.related_identifiers") == [
        {
            "identifier": "10.5281/zenodo.5075887",
            "relation_type": {"id": "isversionof"},
            "scheme": "doi",
        }
    ]
    assert dig(inveniordm, "metadata.funding") is None
    assert dig(inveniordm, "custom_fields.rs:content_html") is None
    assert dig(inveniordm, "custom_fields.rs:image") is None
    assert not dig(inveniordm, "files.enabled")


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    inveniordm = subject.write(to="inveniordm")
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-article"
    assert dig(inveniordm, "pids.doi.identifier") == "10.7554/elife.01567"
    assert len(dig(inveniordm, "metadata.creators")) == 5
    assert dig(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Sankar",
            "given_name": "Martial",
            "name": "Sankar, Martial",
            "type": "personal",
        },
        "affiliations": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, "
                "Lausanne, Switzerland",
            },
        ],
    }

    assert (
        dig(inveniordm, "metadata.title")
        == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert dig(inveniordm, "metadata.publisher") == "eLife Sciences Publications, Ltd"
    assert dig(inveniordm, "metadata.publication_date") == "2014-02-11"
    assert dig(inveniordm, "metadata.languages.0.id") == "eng"
    assert dig(inveniordm, "metadata.version") is None
    assert dig(inveniordm, "metadata.description").startswith(
        "Among various advantages, their small size makes model organisms preferred subjects of investigation."
    )
    assert dig(inveniordm, "metadata.rights") == [{"id": "cc-by-3.0"}]
    assert dig(inveniordm, "metadata.identifiers") == [
        {"identifier": "https://elifesciences.org/articles/01567", "scheme": "url"}
    ]
    related_identifiers = dig(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 1
    assert related_identifiers[0] == {
        "identifier": "10.5061/dryad.b835k",
        "relation_type": {
            "id": "issupplementedby",
        },
        "scheme": "doi",
    }
    references = dig(inveniordm, "metadata.references")
    assert len(references) == 27
    assert references[0] == {
        "identifier": "10.1038/nature02100",
        "reference": "APL regulates vascular tissue identity in Arabidopsis",
        "scheme": "doi",
    }
    assert dig(inveniordm, "metadata.funding") == [
        {"funder": {"name": "SystemsX"}},
        {"funder": {"name": "EMBO longterm post-doctoral fellowships"}},
        {"funder": {"name": "Marie Heim-Voegtlin"}},
        {
            "funder": {
                "id": "019whta54",
                "name": "University of Lausanne",
            },
        },
        {
            "funder": {
                "id": "04wfr2810",
                "name": "EMBO",
            },
        },
        {
            "funder": {
                "id": "00yjd3n13",
                "name": "Swiss National Science Foundation",
            },
        },
    ]
    assert dig(inveniordm, "custom_fields.rs:content_html") is None
    assert dig(inveniordm, "custom_fields.rs:image") is None
    assert not dig(inveniordm, "files.enabled")


@pytest.mark.vcr
def test_rogue_scholar(write_pdf_file):
    "Rogue Scholar"
    string = "https://rogue-scholar.org/api/records/1xr7q-9fp18"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.53731/dv8z6-a6s33"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.53731/dv8z6-a6s33"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert len(dig(inveniordm, "metadata.creators")) == 1
    assert dig(inveniordm, "metadata.creators.0") == {
        "affiliations": [
            {
                "name": "Front Matter",
            },
        ],
        "person_or_org": {
            "family_name": "Fenner",
            "given_name": "Martin",
            "name": "Fenner, Martin",
            "type": "personal",
            "identifiers": [{"identifier": "0000-0003-1419-2405", "scheme": "orcid"}],
        },
    }
    assert dig(inveniordm, "metadata.title") == "Rogue Scholar learns about communities"
    assert dig(inveniordm, "metadata.publisher") == "Front Matter"
    assert dig(inveniordm, "metadata.publication_date") == "2024-10-07"

    assert dig(inveniordm, "metadata.dates") == [
        {"date": "2024-10-07T13:41:37", "type": {"id": "issued"}},
        {"date": "2025-01-23T17:42:32", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "metadata.languages.0.id") == "eng"
    assert dig(inveniordm, "metadata.version") == "v1"
    assert dig(inveniordm, "metadata.description").startswith(
        "The Rogue Scholar infrastructure started migrating to InvenioRDM infrastructure a few weeks ago."
    )
    assert dig(inveniordm, "metadata.subjects") == [
        {
            "id": "https://openalex.org/subfields/1710",
            "subject": "Information Systems",
            "scheme": "Subfields",
        },
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?1.2",
            "scheme": "FOS",
            "subject": "FOS: Computer and information sciences",
        },
        {"subject": "Rogue Scholar"},
    ]
    assert dig(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    assert dig(inveniordm, "metadata.identifiers") == [
        {"identifier": "c5c2e4e7-ac05-413b-b377-f989a72a5356", "scheme": "uuid"},
        {"identifier": "https://doi.org/10.53731/dv8z6-a6s33", "scheme": "guid"},
        {"identifier": "1xr7q-9fp18", "scheme": "other"},
        {
            "identifier": "https://blog.front-matter.de/posts/rogue-scholar-learns-about-communities/",
            "scheme": "url",
        },
    ]
    # the record's concept (parent) DOI, surfaced as an IsVersionOf relation
    assert dig(inveniordm, "metadata.related_identifiers") == [
        {
            "identifier": "10.53731/2ych7-jqc35",
            "scheme": "doi",
            "relation_type": {"id": "isversionof"},
        }
    ]
    assert dig(inveniordm, "metadata.funding") is None
    assert dig(inveniordm, "custom_fields.journal:journal.title") == "Front Matter"
    assert dig(inveniordm, "custom_fields.journal:journal.issn") == "2749-9952"
    # assert dig(inveniordm, "custom_fields.rs:content_html").startswith("a")
    # assert dig(inveniordm, "custom_fields.rs:image") == 2
    assert not dig(inveniordm, "files.enabled")
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_organizational_author(write_pdf_file):
    "Rogue Scholar organizational author"
    string = "https://rogue-scholar.org/api/records/fz2vh-31684"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/wg8rv-awm24"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/wg8rv-awm24"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert len(dig(inveniordm, "metadata.creators")) == 1
    assert dig(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Habgood-Coote",
            "given_name": "Joshua",
            "name": "Habgood-Coote, Joshua",
            "type": "personal",
        },
    }
    assert (
        dig(inveniordm, "metadata.title")
        == "Neil Levy, Philosophy, Bullshit, and Peer Review"
    )
    assert dig(inveniordm, "metadata.publisher") == "Front Matter"
    assert dig(inveniordm, "metadata.publication_date") == "2025-02-11"
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_blog_post(write_pdf_file):
    "JSON Feed"
    string = "https://rogue-scholar.org/api/records/7tatc-wh557"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/dn2mm-m9q51"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/dn2mm-m9q51"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert len(dig(inveniordm, "metadata.creators")) == 1
    assert dig(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Dingemanse",
            "given_name": "Mark",
            "name": "Dingemanse, Mark",
            "type": "personal",
        },
    }
    assert dig(inveniordm, "metadata.title") == "Linguistic roots of connectionism"
    assert dig(inveniordm, "metadata.publication_date") == "2021-07-22"
    assert dig(inveniordm, "metadata.dates") == [
        {"date": "2021-07-22T08:39:07", "type": {"id": "issued"}},
        {"date": "2024-02-04T21:05:36", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "metadata.languages.0.id") == "eng"
    assert dig(inveniordm, "metadata.identifiers") == [
        {"identifier": "525a7d13-fe07-4cab-ac54-75d7b7005647", "scheme": "uuid"},
        {"identifier": "https://ideophone.org/?p=5639", "scheme": "guid"},
        {"identifier": "7tatc-wh557", "scheme": "other"},
        {
            "identifier": "https://ideophone.org/linguistic-roots-of-connectionism/",
            "scheme": "url",
        },
    ]
    assert dig(inveniordm, "metadata.version") == "v1"
    assert dig(inveniordm, "metadata.description").startswith(
        "This Lingbuzz preprint by Baroni is a nice read if you"
    )
    assert dig(inveniordm, "metadata.subjects") == [
        {
            "id": "https://openalex.org/subfields/1203",
            "subject": "Language and Linguistics",
            "scheme": "Subfields",
        },
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?6.2",
            "scheme": "FOS",
            "subject": "FOS: Languages and literature",
        },
        {"subject": "Linguistics"},
        {"subject": "Threads"},
    ]
    assert dig(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    references = dig(inveniordm, "metadata.references")
    assert len(references) == 6
    assert references[0] == {
        "reference": "Baroni, M. (2021, June). On the proper role of linguistically-oriented deep net analysis in linguistic theorizing. LingBuzz. Retrieved from",
        "identifier": "https://ling.auf.net/lingbuzz/006031",
        "scheme": "url",
    }
    assert dig(inveniordm, "custom_fields.journal:journal.title") == "The Ideophone"
    assert dig(inveniordm, "custom_fields.journal:journal.issn") is None
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        '<p>This <a rel="noreferrer noopener" href="https://ling.auf.net/lingbuzz/006031"'
    )
    assert (
        dig(inveniordm, "custom_fields.rs:image")
        == "https://ideophone.org/files/E4FEkLuWUAI6IwO-696x1024.png"
    )
    assert not dig(inveniordm, "files.enabled")
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_affiliations(write_pdf_file):
    "JSON Feed affiliations"
    string = "https://rogue-scholar.org/api/records/v7a82-05b98"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/mg09a-5ma64"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert inveniordm is not None
    assert subject.is_valid
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/mg09a-5ma64"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert len(dig(inveniordm, "metadata.creators")) == 4
    assert dig(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "name": "Beucke, Daniel",
            "given_name": "Daniel",
            "family_name": "Beucke",
            "type": "personal",
            "identifiers": [{"identifier": "0000-0003-4905-1936", "scheme": "orcid"}],
        },
        "affiliations": [
            {
                "id": "05745n787",
                "name": "Niedersächsische Staats-und Universitätsbibliothek Göttingen",
            }
        ],
    }
    assert (
        dig(inveniordm, "metadata.title")
        == "Report on the Hands-On Lab 'Scenarios for the Development of Open Access Repositories' at the 112th BiblioCon"
    )
    assert dig(inveniordm, "metadata.publication_date") == "2024-07-14"
    assert dig(inveniordm, "metadata.dates") == [
        {"date": "2024-07-14T22:00:00", "type": {"id": "issued"}},
        {"date": "2024-07-14T22:00:00", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "metadata.languages.0.id") == "eng"
    assert dig(inveniordm, "metadata.identifiers") == [
        {"identifier": "6d1feb10-057a-4fc2-acb0-ac95e19741af", "scheme": "uuid"},
        {
            "identifier": "https://infomgnt.org/posts/2024-07-15-hands-on-lab-report/",
            "scheme": "guid",
        },
        {"identifier": "v7a82-05b98", "scheme": "other"},
        {
            "identifier": "https://infomgnt.org/posts/2024-07-15-hands-on-lab-report",
            "scheme": "url",
        },
    ]
    assert dig(inveniordm, "metadata.version") == "v1"
    assert dig(inveniordm, "metadata.description").startswith(
        "In the beginning of June 2024,"
    )
    assert dig(inveniordm, "metadata.subjects") == [
        {
            "id": "https://openalex.org/subfields/3309",
            "scheme": "Subfields",
            "subject": "Library and Information Sciences",
        },
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?6.5",
            "scheme": "FOS",
            "subject": "FOS: Other humanities",
        },
        {
            "subject": "Lab Life",
        },
        {
            "subject": "Research",
        },
    ]
    assert dig(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    references = dig(inveniordm, "metadata.references")
    assert len(references) == 4
    assert references[0] == {
        "reference": "Häder, M. (2014). <i>Delphi-Befragungen</i>. Springer Fachmedien Wiesbaden.",
        "identifier": "10.1007/978-3-658-01928-0",
        "scheme": "doi",
    }
    assert (
        dig(inveniordm, "custom_fields.journal:journal.title")
        == "Research Group Information Management @ Humboldt-Universität zu Berlin"
    )
    assert dig(inveniordm, "custom_fields.journal:journal.issn") == "2944-6848"
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        "<p>In the beginning of June 2024"
    )
    assert (
        dig(inveniordm, "custom_fields.rs:image")
        == "https://infomgnt.org/posts/2024-07-15-hands-on-lab-report/112th_bibliocon.jpeg"
    )
    assert not dig(inveniordm, "files.enabled")
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_dates(write_pdf_file):
    "JSON Feed dates"
    string = "https://rogue-scholar.org/api/records/8vkjg-x6j96"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/k9zxj-pek64"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/k9zxj-pek64"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.publication_date") == "2018-08-28"
    assert dig(inveniordm, "metadata.dates") == [
        {"date": "2018-08-28T01:05:10Z", "type": {"id": "issued"}},
        {"date": "2018-10-19T21:13:05Z", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        "<p>I was lucky enough to have Phil Mannion as one of the peer-reviewers"
    )
    assert (
        dig(inveniordm, "custom_fields.rs:image")
        == "https://svpow.wordpress.com/wp-content/uploads/2018/08/figure-a-different-kinds-of-horizontal.jpeg?w=480&h=261"
    )
    # TODO: fix test
    # assert (
    #     dig(inveniordm, "custom_fields.rs:doi")
    #     == "https://svpow.wordpress.com/wp-content/uploads/2018/08/figure-a-different-kinds-of-horizontal.jpeg?w=480&h=261"
    # )
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_funding():
    "JSON Feed funding"
    string = "https://rogue-scholar.org/api/records/y3sy6-27n54"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/hnegw-6rx17"
    assert subject.type == "BlogPost"
    # assert subject.funding_references is not None

    inveniordm = subject.write(to="inveniordm")
    # assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/hnegw-6rx17"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "THOR Final Event programme is out!"
    # assert dig(inveniordm, "metadata.funding") == [
    #     {
    #         "award": {
    #             "identifiers": [
    #                 {
    #                     "identifier": "10.3030/654039",
    #                     "scheme": "doi",
    #                 },
    #             ],
    #             "number": "654039",
    #             "title": {
    #                 "en": "THOR – Technical and Human Infrastructure for Open Research",
    #             },
    #         },
    #         "funder": {
    #             "id": "019w4f821",
    #             "name": "European Union",
    #         },
    #     }
    # ]
    # assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
    #     "<p>Come and join us at the Università degli Studi di Roma"
    # )
    assert dig(inveniordm, "custom_fields.rs:image") is None
    assert dig(inveniordm, "custom_fields.rs:doi") == "https://doi.org/10.59350/thor"


@pytest.mark.vcr
def test_rogue_scholar_more_funding(write_pdf_file):
    "JSON Feed more funding"
    string = "https://rogue-scholar.org/api/records/qz2sd-6tw29"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/m99dx-x9g53"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/m99dx-x9g53"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "Summer Meeting of the Editorial Board"
    assert dig(inveniordm, "metadata.funding") == [
        {
            "award": {
                "identifiers": [
                    {
                        "identifier": "https://gepris-extern.dfg.de/gepris/projekt/422587133",
                        "scheme": "url",
                    },
                ],
                "number": "422587133",
                "title": {
                    "en": "re3data – Offene und nutzerorientierte Referenz für "
                    "Forschungsdatenrepositorien (re3data COREF)",
                },
            },
            "funder": {
                "id": "018mejw64",
                "name": "Deutsche Forschungsgemeinschaft",
            },
        }
    ]
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        '<img alt="" src="https://coref.project.re3data.org/images/7/b/6/1/b/'
    )
    assert dig(inveniordm, "custom_fields.rs:image") is None
    assert dig(inveniordm, "custom_fields.rs:doi") == "https://doi.org/10.59350/coref"
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_references(write_pdf_file):
    "JSON Feed references"
    string = "https://rogue-scholar.org/api/records/trhz1-s0336"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.53731/r79v4e1-97aq74v-ag578"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.53731/r79v4e1-97aq74v-ag578"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert (
        dig(inveniordm, "metadata.title")
        == "Differences between ORCID and DataCite Metadata"
    )
    related_identifiers = dig(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 2
    assert related_identifiers[0] == {
        "identifier": "10.5438/bc11-cqw1",
        "relation_type": {"id": "isidenticalto"},
        "scheme": "doi",
    }
    assert dig(inveniordm, "metadata.funding") == [
        {
            "funder": {"name": "European Commission", "id": "00k4n6c32"},
            "award": {
                "number": "654039",
                "identifiers": [{"scheme": "doi", "identifier": "10.3030/654039"}],
            },
        }
    ]
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        "<p>One of the first tasks for DataCite"
    )
    assert (
        dig(inveniordm, "custom_fields.rs:image")
        == "https://storage.ghost.io/c/c5/33/c533c955-b5f3-4ff1-ae2d-6b52a212e602/content/images/2023/09/cat_and_dog-1.png"
    )
    # TODO: fix test
    # assert (
    #     dig(inveniordm, "custom_fields.rs:doi")
    #     == "https://svpow.wordpress.com/wp-content/uploads/2018/08/figure-a-different-kinds-of-horizontal.jpeg?w=480&h=261"
    # )
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_unstructured_references(write_pdf_file):
    "JSON Feed unstructured references"
    string = "https://rogue-scholar.org/api/records/345qb-aan84"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/27ewm-zn378"
    assert subject.type == "BlogPost"
    assert len(subject.references) == 7

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/27ewm-zn378"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert (
        dig(inveniordm, "metadata.title")
        == "To what extent is science a strong-link problem?"
    )
    references = dig(inveniordm, "metadata.references")
    assert len(references) == 7
    assert references[0] == {
        "identifier": "10.1128/iai.05661-11",
        "reference": "Fang, F. C., Casadevall, A.&amp; Morrison, R. P. (2011). Retracted Science and the Retraction Index. <i>Infection and Immunity</i>, <i>79</i>(10), 3855–3859.",
        "scheme": "doi",
    }
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_citations(write_pdf_file):
    "JSON Feed citations"
    string = "https://rogue-scholar.org/api/records/w2nqy-wxa44"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/dcw3y-7em87"
    assert subject.type == "BlogPost"
    # assert len(subject.citations) == 2

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/dcw3y-7em87"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "Use of CiTO in CiteULike"
    # citations are now represented as IsReferencedBy relations, written to
    # custom_fields.pidbox:citations
    # assert len(citations) == 2
    # assert citations[0] == {
    #     "identifier": "10.1007/s11192-013-1108-3",
    #     "reference": "Parinov, S., &amp; Kogalovsky, M. (2013). Semantic linkages in research "
    #     "information systems as a new data source for scientometric studies. "
    #     "<i>Scientometrics</i>, <i>98</i>(2), 927–943.",
    #     "scheme": "doi",
    # }
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_relations(write_pdf_file):
    "JSON Feed relations"
    string = "https://rogue-scholar.org/api/records/4jymf-n5m83"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.54900/zg929-e9595"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.54900/zg929-e9595"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "Large Language Publishing"
    related_identifiers = dig(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 2
    assert related_identifiers[0] == {
        "identifier": "10.18357/kula.291",
        "relation_type": {"id": "ispreviousversionof"},
        "scheme": "doi",
    }
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        "<p><em>The New York Times</em> ushered in the New Year with"
    )
    assert (
        dig(inveniordm, "custom_fields.rs:image")
        == "https://upstream.force11.org/content/images/2023/12/pexels-viktor-talashuk-2377295.jpg"
    )
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_rogue_scholar_broken_reference(write_pdf_file):
    "JSON Feed relations"
    string = "https://rogue-scholar.org/api/records/jehpc-qpc91"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/z78kb-qrz59"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/z78kb-qrz59"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert (
        dig(inveniordm, "metadata.title")
        == "2024 mpox outbreak: common analytics tasks and available R tools"
    )
    references = dig(inveniordm, "metadata.references")
    assert len(references) == 6
    assert references[0] == {
        "identifier": "10.4269/ajtmh.23-0215",
        "reference": "Charniga, K., McCollum, A. M., Hughes, C. M., Monroe, B., Kabamba, J., Lushima, R. S., Likafi, T., Nguete, B., Pukuta, E., Muyamuna, E., Muyembe Tamfum, J.-J., Karhemere, S., Kaba, D., &amp; Nakazawa, Y. (2024). Updating Reproduction Number Estimates for Mpox in the Democratic Republic of Congo Using Surveillance Data. <i>The American Journal of Tropical Medicine and Hygiene</i>, <i>110</i>(3), 561–568.",
        "scheme": "doi",
    }
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_external_doi(write_pdf_file):
    "external DOI used by Rogue Scholar"
    string = "https://rogue-scholar.org/api/records/9jsrb-jtc73"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.57689/dini-blog.20210712"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.57689/dini-blog.20210712"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert (
        dig(inveniordm, "metadata.title")
        == "Eine Musterdienstvereinbarung fürs FIS – ein Beispiel der TIB"
    )
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_post_with_contributor_roles(write_pdf_file):
    "post with contributor roles"
    string = "https://rogue-scholar.org/api/records/apt10-14q04"
    subject = Metadata(string, via="inveniordm")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/510pg-zzf58"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/510pg-zzf58"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.creators") == [
        {
            "person_or_org": {
                "name": "Salmon, Ma\xeblle",
                "given_name": "Ma\xeblle",
                "family_name": "Salmon",
                "type": "personal",
                "identifiers": [
                    {"identifier": "0000-0002-2815-0399", "scheme": "orcid"}
                ],
            }
        },
        {
            "person_or_org": {
                "name": "Bellini Saibene, Yanina",
                "given_name": "Yanina",
                "family_name": "Bellini Saibene",
                "type": "personal",
                "identifiers": [
                    {"identifier": "0000-0002-4522-7466", "scheme": "orcid"}
                ],
            }
        },
    ]
    # assert dig(inveniordm, "metadata.contributors") == [
    #     {
    #         "person_or_org": {
    #             "name": "LaZerte, Steffi",
    #             "given_name": "Steffi",
    #             "family_name": "LaZerte",
    #             "type": "personal",
    #             "identifiers": [
    #                 {"identifier": "0000-0002-7690-8360", "scheme": "orcid"}
    #             ],
    #         },
    #         "role": {
    #             "id": "editor",
    #         },
    #     }
    # ]
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_post_with_interviewee_roles(write_pdf_file):
    "post with interviewee roles"
    string = "https://rogue-scholar.org/api/records/ssrar-vhq35"
    subject = Metadata(string, via="inveniordm")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/s8m95-ap410"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/s8m95-ap410"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert len(dig(inveniordm, "metadata.creators")) == 9
    assert dig(inveniordm, "metadata.contributors") is None
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_multiple_subfields(write_pdf_file):
    "post with multiple subfields"
    string = "https://rogue-scholar.org/api/records/nnx9s-74a78"
    subject = Metadata(string, via="inveniordm")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/1srmw-yb311"
    assert subject.type == "BlogPost"

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/1srmw-yb311"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.subjects") == [
        {
            "id": "https://openalex.org/subfields/1307",
            "subject": "Cell Biology",
            "scheme": "Subfields",
        },
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?1.6",
            "subject": "FOS: Biological sciences",
            "scheme": "FOS",
        },
        {
            "id": "https://openalex.org/T12287",
            "subject": "Fibroblast Growth Factor Research",
            "scheme": "Topics",
        },
        {
            "id": "https://openalex.org/subfields/1312",
            "subject": "Molecular Biology",
            "scheme": "Subfields",
        },
        {"subject": "Publishing"},
        {"subject": "Science"},
        {"subject": "Cancer"},
        {"subject": "Cell Biology"},
        {"subject": "FGFR3"},
    ]
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr
def test_content_with_external_src(write_pdf_file):
    "external DOI used by Rogue Scholar"
    string = "https://rogue-scholar.org/api/records/xtmqd-gwg60"
    subject = Metadata(string, via="inveniordm")
    assert subject.id == "https://doi.org/10.59350/vwd81-p8z85"
    assert subject.type == "BlogPost"
    assert re.search(
        'src="https://chem-bla-ics.linkedchemistry.info/assets/images/imageResolutionLoss.png"',
        subject.content,
    )

    inveniordm = subject.write(to="inveniordm")
    assert subject.is_valid
    assert inveniordm is not None
    inveniordm = json.loads(inveniordm)
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/vwd81-p8z85"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "Archiving, but not really"
    assert re.search(
        'src="https://chem-bla-ics.linkedchemistry.info/assets/images/imageResolutionLoss.png"',
        dig(inveniordm, "custom_fields.rs:content_html"),
    )
    assert_pdf_metadata(write_pdf_file(subject), subject)


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_upsert_record_falls_back_to_guid():
    "upsert_record uses GUID from output identifiers when DOI lookup returns None"
    string = "https://rogue-scholar.org/api/records/7tatc-wh557"
    subject = Metadata(string, via="inveniordm")
    assert subject.is_valid

    existing_id = "abc123xyz"
    record = {
        "doi": "10.59350/dn2mm-m9q51",
        "previous_doi": None,
        "community": "ideophone",
        "community_id": "community-uuid",
    }

    with (
        patch(
            "commonmeta.writers.inveniordm_writer.search_by_doi", return_value=None
        ) as mock_doi,
        patch(
            "commonmeta.writers.inveniordm_writer.search_by_guid",
            return_value=existing_id,
        ) as mock_guid,
        patch(
            "commonmeta.writers.inveniordm_writer.get_published_record",
            return_value=None,
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.edit_published_record",
            side_effect=lambda r, *a: {**r, "status": "edited"},
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.update_draft_record",
            side_effect=lambda r, *a: {**r, "status": "updated"},
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.publish_draft_record",
            side_effect=lambda r, *a: {**r, "status": "published"},
        ),
    ):
        result = upsert_record(subject, "rogue-scholar.org", "token", record)

    # DOI search is called with the correct DOI
    mock_doi.assert_called_once_with(
        "10.59350/dn2mm-m9q51", "rogue-scholar.org", "token"
    )

    # GUID search is called with the normalised GUID URL from output identifiers
    mock_guid.assert_called_once_with(
        "https://ideophone.org/?p=5639", "rogue-scholar.org", "token"
    )

    # The existing record id was found via GUID and used for the update path
    assert result["id"] == existing_id
    assert result["status"] == "published"


# The metadata a record is upserted with, and the record InvenioRDM returns for it:
# vocabulary entries come back expanded, and the record carries server-side fields.
UPSERT_OUTPUT = {
    "access": {"record": "public", "files": "public"},
    "files": {"enabled": False},
    "metadata": {
        "resource_type": {"id": "blogpost"},
        "creators": [{"person_or_org": {"name": "Fenner, Martin", "type": "personal"}}],
        "title": "Test",
        "publication_date": "2024-01-01",
        "languages": [{"id": "eng"}],
    },
    "custom_fields": {"rs:content_html": "<p>Test</p>"},
}
PUBLISHED_RECORD = {
    "id": "fktsh-g4g95",
    "created": "2024-01-01T00:00:00+00:00",
    "updated": "2024-01-02T00:00:00+00:00",
    "revision_id": 4,
    "links": {"self": "https://rogue-scholar.org/api/records/fktsh-g4g95"},
    "access": {
        "record": "public",
        "files": "public",
        "embargo": {"active": False},
        "status": "metadata-only",
    },
    "files": {"enabled": False, "entries": {}, "count": 0},
    "metadata": {
        "resource_type": {"id": "blogpost", "title": {"en": "Blog post"}},
        "creators": [{"person_or_org": {"name": "Fenner, Martin", "type": "personal"}}],
        "title": "Test",
        "publication_date": "2024-01-01",
        "languages": [{"id": "eng", "title": {"en": "English"}}],
    },
    "custom_fields": {"rs:content_html": "<p>Test</p>"},
}


def test_record_matches_an_unchanged_record():
    "a record holding the same metadata matches, despite expanded vocabularies"
    assert record_matches(UPSERT_OUTPUT, PUBLISHED_RECORD) is True


@pytest.mark.parametrize(
    "change",
    [
        {"metadata": {**UPSERT_OUTPUT["metadata"], "title": "Another title"}},
        {"custom_fields": {"rs:content_html": "<p>Edited</p>"}},
        # a field that is newly written
        {"custom_fields": {**UPSERT_OUTPUT["custom_fields"], "rs:image": "img.png"}},
        # a field that is no longer written and has to be cleared
        {"custom_fields": {}},
    ],
)
def test_record_matches_a_changed_record(change):
    "any change to a field the writer owns is detected"
    assert record_matches({**UPSERT_OUTPUT, **change}, PUBLISHED_RECORD) is False


def test_record_matches_ignores_foreign_fields():
    "fields written by another pipeline are left alone"
    published = {
        **PUBLISHED_RECORD,
        "custom_fields": {**PUBLISHED_RECORD["custom_fields"], "feed:updated": "2024"},
    }
    assert record_matches(UPSERT_OUTPUT, published) is True


def test_record_matches_a_longer_list():
    "an appended list entry is a change, not a superset"
    published = {
        **PUBLISHED_RECORD,
        "metadata": {
            **PUBLISHED_RECORD["metadata"],
            "languages": [{"id": "eng"}, {"id": "deu"}],
        },
    }
    assert record_matches(UPSERT_OUTPUT, published) is False


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_upsert_record_skips_an_unchanged_record():
    "an unchanged record is not republished, since that writes a new revision"
    string = "https://rogue-scholar.org/api/records/7tatc-wh557"
    subject = Metadata(string, via="inveniordm")
    assert subject.is_valid

    record = {"doi": "10.59350/dn2mm-m9q51", "previous_doi": None}
    # what the writer is about to send, as InvenioRDM would return it
    output = json.loads(subject.write(to="inveniordm"))
    published = {
        "id": "fktsh-g4g95",
        "created": "2024-01-01T00:00:00+00:00",
        "updated": "2024-01-02T00:00:00+00:00",
        **{k: v for k, v in output.items() if k != "pids"},
    }

    with (
        patch(
            "commonmeta.writers.inveniordm_writer.search_by_doi",
            return_value="fktsh-g4g95",
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.get_published_record",
            return_value=published,
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.edit_published_record"
        ) as mock_edit,
        patch(
            "commonmeta.writers.inveniordm_writer.update_draft_record"
        ) as mock_update,
        patch(
            "commonmeta.writers.inveniordm_writer.publish_draft_record"
        ) as mock_publish,
    ):
        result = upsert_record(subject, "rogue-scholar.org", "token", record)

    assert result["status"] == "unchanged"
    assert result["updated"] == "2024-01-02T00:00:00+00:00"
    mock_edit.assert_not_called()
    mock_update.assert_not_called()
    mock_publish.assert_not_called()


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_upsert_record_skip_unchanged_can_be_turned_off():
    "skip_unchanged=False forces the republish of a record that did not change"
    string = "https://rogue-scholar.org/api/records/7tatc-wh557"
    subject = Metadata(string, via="inveniordm")
    record = {"doi": "10.59350/dn2mm-m9q51", "previous_doi": None}

    with (
        patch(
            "commonmeta.writers.inveniordm_writer.search_by_doi",
            return_value="fktsh-g4g95",
        ),
        patch("commonmeta.writers.inveniordm_writer.get_published_record") as mock_read,
        patch(
            "commonmeta.writers.inveniordm_writer.edit_published_record",
            side_effect=lambda r, *a: {**r, "status": "edited"},
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.update_draft_record",
            side_effect=lambda r, *a: {**r, "status": "updated"},
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.publish_draft_record",
            side_effect=lambda r, *a: {**r, "status": "published"},
        ),
    ):
        result = upsert_record(
            subject, "rogue-scholar.org", "token", record, skip_unchanged=False
        )

    assert result["status"] == "published"
    mock_read.assert_not_called()


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_upsert_record_uploads_the_pdf_before_publishing():
    """Publishing locks a record's files, so the upload goes on the draft."""
    string = "https://rogue-scholar.org/api/records/7tatc-wh557"
    subject = Metadata(string, via="inveniordm")
    record = {"doi": "10.59350/dn2mm-m9q51", "previous_doi": None}
    calls = []

    with (
        patch(
            "commonmeta.writers.inveniordm_writer.search_by_doi",
            return_value="fktsh-g4g95",
        ),
        patch("commonmeta.writers.inveniordm_writer.get_published_record"),
        patch(
            "commonmeta.writers.inveniordm_writer.edit_published_record",
            side_effect=lambda r, *a: r,
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.update_draft_record",
            side_effect=lambda r, *a: r,
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.upload_pdf",
            side_effect=lambda m, h, t, r: calls.append("upload") or r,
        ) as mock_upload,
        patch(
            "commonmeta.writers.inveniordm_writer.publish_draft_record",
            side_effect=lambda r, *a: calls.append("publish")
            or {**r, "status": "published"},
        ),
    ):
        result = upsert_record(
            subject,
            "rogue-scholar.org",
            "token",
            record,
            skip_unchanged=False,
            write_pdf=True,
        )

    assert calls == ["upload", "publish"]
    assert mock_upload.call_args.args[0] is subject
    assert result["status"] == "published"


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_upsert_record_does_not_publish_a_discarded_draft():
    """A draft thrown away for carrying an unpublishable file is not published.

    Publishing it would fail with "One or more files have not completed their
    transfer", which is the state the draft was discarded to escape.
    """
    string = "https://rogue-scholar.org/api/records/7tatc-wh557"
    subject = Metadata(string, via="inveniordm")
    record = {"doi": "10.59350/dn2mm-m9q51", "previous_doi": None}

    with (
        patch(
            "commonmeta.writers.inveniordm_writer.search_by_doi",
            return_value="fktsh-g4g95",
        ),
        patch("commonmeta.writers.inveniordm_writer.get_published_record"),
        patch(
            "commonmeta.writers.inveniordm_writer.edit_published_record",
            side_effect=lambda r, *a: r,
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.update_draft_record",
            side_effect=lambda r, *a: r,
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.upload_pdf",
            side_effect=lambda m, h, t, r: {**r, "status": "draft_discarded"},
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.publish_draft_record"
        ) as mock_publish,
    ):
        result = upsert_record(
            subject,
            "rogue-scholar.org",
            "token",
            record,
            skip_unchanged=False,
            write_pdf=True,
        )

    assert result["status"] == "draft_discarded"
    mock_publish.assert_not_called()


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_upsert_record_does_not_skip_a_record_without_its_pdf():
    """Unchanged metadata is no reason to skip while the file is still missing."""
    string = "https://rogue-scholar.org/api/records/7tatc-wh557"
    subject = Metadata(string, via="inveniordm")
    record = {"doi": "10.59350/dn2mm-m9q51", "previous_doi": None}
    output = json.loads(subject.write(to="inveniordm", write_pdf=True))
    published = {
        "id": "fktsh-g4g95",
        "files": {"enabled": True, "entries": {}},
        **{k: v for k, v in output.items() if k not in ("pids", "files")},
    }

    with (
        patch(
            "commonmeta.writers.inveniordm_writer.search_by_doi",
            return_value="fktsh-g4g95",
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.get_published_record",
            return_value=published,
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.edit_published_record",
            side_effect=lambda r, *a: r,
        ),
        patch(
            "commonmeta.writers.inveniordm_writer.update_draft_record",
            side_effect=lambda r, *a: r,
        ),
        patch("commonmeta.writers.inveniordm_writer.upload_pdf") as mock_upload,
        patch(
            "commonmeta.writers.inveniordm_writer.publish_draft_record",
            side_effect=lambda r, *a: {**r, "status": "published"},
        ),
    ):
        result = upsert_record(
            subject, "rogue-scholar.org", "token", record, write_pdf=True
        )

    assert result["status"] == "published"
    mock_upload.assert_called_once()


def test_citations_written_to_pidbox_field():
    """IsReferencedBy relations are written to custom_fields.pidbox:citations."""
    record = {
        "id": "fktsh-g4g95",
        "pids": {"doi": {"identifier": "10.53731/kdqkf-nf052"}},
        "metadata": {
            "title": "Test",
            "publication_date": "2024-01-01",
            "resource_type": {"id": "blogpost"},
            "creators": [],
        },
        # deposited under the legacy name; the writer emits the new one
        "custom_fields": {
            "rs:citations": [{"identifier": "10.59350/4q8j1-1ap35", "scheme": "doi"}]
        },
    }
    subject = Metadata(record, via="inveniordm")
    output = subject.write(to="inveniordm")
    assert output is not None
    inveniordm = json.loads(output)
    # no license on this record: rights is omitted rather than raising
    assert dig(inveniordm, "metadata.rights") is None
    assert dig(inveniordm, "custom_fields.pidbox:citations") == [
        {"identifier": "10.59350/4q8j1-1ap35", "scheme": "doi"}
    ]
    assert dig(inveniordm, "custom_fields.rs:citations") is None


def test_write_pdf_defaults_to_false():
    """Records stay metadata-only unless a caller asks for a pdf."""
    from commonmeta.writers.inveniordm_writer import write_inveniordm

    subject = Metadata("10.5281/zenodo.5244404", via="datacite")
    assert write_inveniordm(subject)["files"] == {"enabled": False}


def test_write_pdf_without_content_keeps_files_disabled():
    """A record with no rs:content_html cannot produce a pdf.

    Enabling files for it would fail the publish with "Missing uploaded files".
    """
    from commonmeta.writers.inveniordm_writer import write_inveniordm

    subject = Metadata("10.5281/zenodo.5244404", via="datacite")
    assert not subject.content
    assert write_inveniordm(subject, write_pdf=True)["files"] == {"enabled": False}


def test_write_pdf_with_content_enables_files():
    """Content is what the pdf is rendered from, so files are enabled."""
    from commonmeta.writers.inveniordm_writer import write_inveniordm

    subject = Metadata("10.5281/zenodo.5244404", via="datacite")
    subject.content = "<p>Some post content</p>"
    output = write_inveniordm(subject, write_pdf=True)
    assert output["files"] == {"enabled": True}
    assert output["custom_fields"]["rs:content_html"] == "<p>Some post content</p>"


def test_write_forwards_kwargs_to_the_writer():
    """Metadata.write passes options through to the json writers."""
    import orjson

    subject = Metadata("10.5281/zenodo.5244404", via="datacite")
    subject.content = "<p>Some post content</p>"

    default = orjson.loads(subject.write(to="inveniordm"))
    with_pdf = orjson.loads(subject.write(to="inveniordm", write_pdf=True))

    assert default["files"] == {"enabled": False}
    assert with_pdf["files"] == {"enabled": True}


def test_write_ignores_options_meant_for_another_writer():
    """Every json writer tolerates kwargs it does not use."""
    subject = Metadata("10.5281/zenodo.5244404", via="datacite")
    for fmt in ("commonmeta", "datacite", "schema_org", "csl"):
        assert subject.write(to=fmt, write_pdf=True, style="apa") is not None


def test_push_inveniordm_forwards_write_pdf():
    """push_inveniordm passes the option down to upsert_record."""
    from commonmeta.writers import inveniordm_writer as w

    subject = Metadata("10.5281/zenodo.5244404", via="datacite")
    with (
        patch.object(w, "upsert_record", return_value={}) as upsert,
        patch.object(w, "add_record_to_communities", side_effect=lambda m, h, t, r: r),
        patch.object(
            w, "update_external_services", side_effect=lambda m, h, t, r, **k: r
        ),
    ):
        w.push_inveniordm(subject, "example.org", "token", write_pdf=True)

    assert upsert.call_args.kwargs["write_pdf"] is True


def test_push_inveniordm_defaults_write_pdf_to_false():
    """Callers that say nothing keep metadata-only records."""
    from commonmeta.writers import inveniordm_writer as w

    subject = Metadata("10.5281/zenodo.5244404", via="datacite")
    with (
        patch.object(w, "upsert_record", return_value={}) as upsert,
        patch.object(w, "add_record_to_communities", side_effect=lambda m, h, t, r: r),
        patch.object(
            w, "update_external_services", side_effect=lambda m, h, t, r, **k: r
        ),
    ):
        w.push_inveniordm(subject, "example.org", "token")

    assert upsert.call_args.kwargs["write_pdf"] is False


def test_pdf_resources_are_packaged():
    """The pdf stylesheet and its fonts ship with the package."""
    from pathlib import Path

    import commonmeta

    pdf_dir = Path(commonmeta.__file__).parent / "resources" / "pdf"
    assert (pdf_dir / "style.css").is_file()

    fonts = pdf_dir / "fonts"
    expected = {
        "FiraMono-Regular.otf",
        "FiraSans-Bold.otf",
        "FiraSans-Light.otf",
        "FiraSans-LightItalic.otf",
        "FiraSans-SemiBold.otf",
        "FiraSans-SemiBoldItalic.otf",
    }
    assert expected <= {f.name for f in fonts.iterdir()}
    # Fira Sans is SIL OFL 1.1, which requires the licence to travel with it
    assert (fonts / "LICENSE").is_file()


def test_pdf_stylesheet_font_urls_resolve():
    """Every @font-face url points at a file that is actually shipped."""
    import re
    from pathlib import Path

    import commonmeta

    pdf_dir = Path(commonmeta.__file__).parent / "resources" / "pdf"
    css = (pdf_dir / "style.css").read_text(encoding="utf-8")

    urls = re.findall(r'src:\s*url\("([^"]+)"\)', css)
    assert urls, "no @font-face src urls found"
    for url in urls:
        assert (pdf_dir / url).is_file(), f"{url} is referenced but not shipped"


def test_pdf_stylesheet_has_no_stray_src_declarations():
    """`src` outside @font-face is ignored by every css engine."""
    import re
    from pathlib import Path

    import commonmeta

    css = (
        Path(commonmeta.__file__).parent / "resources" / "pdf" / "style.css"
    ).read_text(encoding="utf-8")

    depth_is_font_face = False
    for line in css.split("\n"):
        stripped = line.strip()
        if stripped.startswith("@font-face"):
            depth_is_font_face = True
        elif stripped == "}":
            depth_is_font_face = False
        elif re.match(r"src:\s*url\(", stripped):
            assert depth_is_font_face, f"stray src declaration: {stripped}"


def test_pdf_stylesheet_font_faces_are_top_level():
    """A nested @font-face is dead css: WeasyPrint does not implement nesting."""
    css = (PDF_RESOURCES / "style.css").read_text(encoding="utf-8")

    depth = 0
    for line in css.split("\n"):
        stripped = line.strip()
        if stripped.startswith("@font-face"):
            assert depth == 0, f"@font-face nested inside another rule: {stripped}"
        depth += stripped.count("{") - stripped.count("}")


def test_pdf_embeds_the_shipped_fonts(write_pdf_file):
    """The bundled Fira faces reach the pdf rather than a system fallback.

    WeasyPrint applies @font-face only when the same FontConfiguration reaches
    both the stylesheet and the render; miss it and the text silently comes out
    in DejaVu Sans. Embedded font names are readable in an uncompressed pdf,
    where they carry the subset prefix WeasyPrint generates (``EYBJQT+``).
    """
    sample = sample_metadata(
        "<h1>Heading</h1>"
        "<p>Body text, <em>emphasis</em> and <code>inline_code()</code>.</p>"
    )
    pdf = write_pdf_file(sample, uncompressed_pdf=True)

    fonts = {m.decode() for m in re.findall(rb"/BaseFont\s*/\w+\+([\w-]+)", pdf)}
    assert "Fira-Sans-Light" in fonts  # html { font-family: Fira Sans; weight 300 }
    assert "Fira-Sans-Bold" in fonts  # h1
    assert "Fira-Sans-Light-Italic" in fonts  # em
    assert "Fira-Mono-Light" in fonts  # code, pre, at weight 300


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_pdf_is_tagged_and_archival(write_pdf_file):
    """The rendition is PDF/A-3a: archival, and tagged for a screen reader.

    A tagged pdf carries a structure tree, so headings, lists and figures reach
    assistive technology as structure rather than as placed glyphs.
    """
    subject = Metadata(
        "https://rogue-scholar.org/api/records/7tatc-wh557", via="inveniordm"
    )

    metadata = read_pdf_metadata(write_pdf_file(subject))

    assert metadata["variant"] == "PDF/A-3a"
    assert metadata["tagged"] is True


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_pdf_embeds_the_feature_image(write_pdf_file):
    """The feature image reaches the title page as an image.

    An image the render cannot fetch leaves its alt text printed across the
    page instead, so this checks for the image object itself.
    """
    import pikepdf

    subject = Metadata(
        "https://rogue-scholar.org/api/records/7tatc-wh557", via="inveniordm"
    )

    pdf = write_pdf_file(subject)

    with pikepdf.open(BytesIO(pdf)) as document:
        page = pikepdf.Page(document.pages[0])
        # get_images() since pikepdf 10, .images on the 9.x line Python 3.9 gets
        images = page.get_images() if hasattr(page, "get_images") else page.images
    assert len(images) == 1


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_pdf_images_are_not_interpolated(write_pdf_file):
    """PDF/A forbids /Interpolate on an image (ISO 19005-3 6.2.8).

    WeasyPrint sets it on every image it draws, and veraPDF fails the file on
    it, so the writer takes the key back out.
    """
    import pikepdf

    subject = Metadata(
        "https://rogue-scholar.org/api/records/7tatc-wh557", via="inveniordm"
    )

    pdf = write_pdf_file(subject)

    with pikepdf.open(BytesIO(pdf)) as document:
        images = [
            obj
            for obj in document.objects
            if isinstance(obj, pikepdf.Stream)
            and obj.get("/Subtype", None) == pikepdf.Name.Image
        ]
        assert images, "no image to check"
        assert all("/Interpolate" not in image for image in images)


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_pdf_embeds_the_post_content(write_pdf_file):
    """rs:content_html travels inside the pdf as the source it was rendered from.

    PDF/A-3 is the variant that allows an embedded file of any type, and it is
    what makes the deposited pdf a container for the post rather than only a
    rendering of it.
    """
    subject = Metadata(
        "https://rogue-scholar.org/api/records/7tatc-wh557", via="inveniordm"
    )

    pdf = write_pdf_file(subject)

    assert read_pdf_metadata(pdf)["attachments"] == {
        "10.59350-dn2mm-m9q51.html": "text/html"
    }
    assert read_pdf_attachment(pdf).decode("utf-8") == subject.content
    assert read_pdf_attachment(pdf, "10.59350-dn2mm-m9q51.html") is not None
    assert read_pdf_attachment(pdf, "absent.html") is None


def test_pdf_of_an_untagged_render_is_reported_as_untagged(write_pdf_file):
    """`tagged` says what the pdf carries, rather than what was asked for."""
    pdf = write_pdf_file(sample_metadata("<p>Body</p>"), pdf_variant=None)

    metadata = read_pdf_metadata(pdf)

    assert metadata["tagged"] is False
    assert "variant" not in metadata


@pytest.mark.vcr("test_rogue_scholar.yaml")
def test_pdf_metadata_round_trip(write_pdf_file):
    """What the writer puts in the head of the document comes back out of the pdf."""
    subject = Metadata(
        "https://rogue-scholar.org/api/records/1xr7q-9fp18", via="inveniordm"
    )

    metadata = read_pdf_metadata(write_pdf_file(subject))

    assert metadata["title"] == "Rogue Scholar learns about communities"
    assert metadata["authors"] == ["Martin Fenner"]
    assert metadata["description"].startswith("The Rogue Scholar infrastructure")
    # the keywords the title page prints, said once for the whole pdf: the
    # classification names what it is, the field of science is left out
    assert metadata["keywords"] == ["Information Systems (Subfield)", "Rogue Scholar"]
    assert metadata["generator"] == "Ghost"  # the blog platform, from rs:generator
    assert metadata["created"] == "2024-10-07"
    assert metadata["modified"] == "2025-01-23"
    assert metadata["language"] == "en"
    assert metadata["producer"].startswith("WeasyPrint")


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_to_pdf_html_front_matter(feature_image):
    """The title page carries what the rogue-scholar-api pdf template carried."""
    subject = Metadata(
        "https://rogue-scholar.org/api/records/7tatc-wh557", via="inveniordm"
    )

    html = to_pdf_html(subject)

    assert "<title>Linguistic roots of connectionism</title>" in html
    assert "<h1>Linguistic roots of connectionism</h1>" in html
    assert '<p class="author"><span>Mark Dingemanse</span></p>' in html
    # what the record is, when it came out, and what it came out in
    assert (
        '<div class="date">Blog post published July 22, 2021 in '
        "<i>The Ideophone</i></div>" in html
    )
    assert 'class="identifier"><a href="https://doi.org/10.59350/dn2mm-m9q51"' in html
    assert '<div class="abstract"><h4>Abstract</h4>This Lingbuzz preprint' in html
    # the tags the post gave itself, not the subjects it was classified into
    assert (
        '<div class="keywords"><h4>Keywords</h4>Language and Linguistics '
        "(Subfield), Linguistics, Threads</div>" in html
    )
    # the image travels in the document rather than being linked from the blog
    assert feature_image.call_args.args[0] == (
        "https://ideophone.org/files/E4FEkLuWUAI6IwO-696x1024.png"
    )
    # asked for as an image: a blog behind a filter answers a bare request
    # with 406 Not Acceptable
    assert feature_image.call_args.kwargs["headers"]["Accept"].startswith("image/")
    assert (
        '<img class="feature-image" alt="Feature image" src="data:image/png;base64,'
        in html
    )
    assert '<div class="rights"><h4>Copyright</h4>Copyright ' in html
    assert (
        "&copy;</span> Mark Dingemanse 2021. Distributed under the terms of the "
        '<a href="https://creativecommons.org/licenses/by/4.0/legalcode">Creative '
        "Commons Attribution 4.0 International License</a>, which permits" in html
    )
    # the body is the post content, with an alt description on every image
    assert html.endswith(
        f"</section>{to_pdf_content(subject.content, 'en')}</body></html>"
    )
    assert 'alt="Image"' in html


@pytest.mark.parametrize(
    "content, expected",
    [
        # a tagged pdf needs a description for every image, and WeasyPrint
        # logs an error for each one that has none
        ('<p><img src="rnn.jpg"></p>', 'alt="Image"'),
        ('<p><img src="rnn.jpg" alt=""></p>', 'alt="Image"'),
        # the caption of the figure it sits in says more than a label does
        (
            '<figure><img src="rnn.jpg"><figcaption>A low-rank RNN</figcaption></figure>',
            'alt="A low-rank RNN"',
        ),
        ('<p><img src="rnn.jpg" title="Figure 1"></p>', 'alt="Figure 1"'),
    ],
)
def test_to_pdf_content_describes_every_image(content, expected):
    """An image without an alt description gets one."""
    assert expected in to_pdf_content(content, "en")


def test_to_pdf_content_keeps_the_description_a_post_gives():
    """Content that describes its own images is passed through untouched."""
    content = '<p><img src="rnn.jpg" alt="A low-rank RNN"></p>'

    assert to_pdf_content(content, "en") == content
    assert to_pdf_content("<p>No image here</p>", "en") == "<p>No image here</p>"
    assert to_pdf_content(None, "en") == ""


def test_to_pdf_content_labels_an_image_in_the_language_of_the_post():
    """The label a screen reader reads is in the document's language."""
    assert 'alt="Bild"' in to_pdf_content('<p><img src="rnn.jpg"></p>', "de")


@pytest.mark.parametrize(
    "response",
    [
        # the blog no longer serves it
        SimpleNamespace(raise_for_status=Mock(side_effect=RequestException("404"))),
        # or serves something that is not an image, e.g. an error page
        image_response(b"<html>Not found</html>", "text/html"),
    ],
)
def test_to_pdf_html_leaves_out_an_unusable_feature_image(response):
    """An image that cannot be fetched is left out, not left as a broken img.

    WeasyPrint draws the alt text where an image fails, which would print
    "Feature image" across the title page.
    """
    from commonmeta import io_utils

    sample = sample_metadata("<p>Body</p>")
    sample.image = "https://example.org/feature.png"

    with patch.object(
        io_utils, "http", SimpleNamespace(get=Mock(return_value=response))
    ):
        html = to_pdf_html(sample)

    assert "feature-image" not in html
    assert "Feature image" not in html


@pytest.mark.vcr("test_external_doi.yaml")
def test_to_pdf_html_in_another_language():
    """Front matter labels and the date follow the language of the post."""
    subject = Metadata(
        "https://rogue-scholar.org/api/records/9jsrb-jtc73", via="inveniordm"
    )

    html = to_pdf_html(subject)

    assert html.startswith("<html lang='de'>")
    assert (
        '<div class="date">Blogbeitrag veröffentlicht am 12. Juli 2021 in '
        "<i>Gemeinsamer Blog der DINI AGs</i></div>" in html
    )
    assert "<h4>Zusammenfassung</h4>" in html
    assert "<h4>Urheberrecht</h4>" in html


@pytest.mark.parametrize(
    "license_, expected",
    [
        (
            {"id": "CC-BY-4.0", "url": "https://creativecommons.org/licenses/by/4.0"},
            'Copyright <span class="copyright">&copy;</span> Ada Lovelace 2024. '
            'Distributed under the terms of the <a href="https://creativecommons.org'
            '/licenses/by/4.0">Creative Commons Attribution 4.0 International '
            "License</a>, which permits unrestricted use, distribution, and "
            "reproduction in any medium, provided the original author and source "
            "are credited.",
        ),
        (
            {
                "id": "CC0-1.0",
                "url": "https://creativecommons.org/publicdomain/zero/1.0",
            },
            "This is an open access article, free of all copyright, and may be "
            "freely reproduced, distributed, transmitted, modified, built upon, or "
            "otherwise used by anyone for any lawful purpose. The work is made "
            'available under the <a href="https://creativecommons.org/publicdomain'
            '/zero/1.0">Creative Commons CC0 public domain dedication</a>.',
        ),
        (None, None),
    ],
)
def test_to_pdf_rights(license_, expected):
    """CC0 waives copyright rather than asserting it, and a post may have neither."""
    from commonmeta.io_utils import to_pdf_rights

    sample = sample_metadata("<p>Body</p>")
    sample.license = license_
    sample.date_published = "2024-05-06"

    assert to_pdf_rights(sample, ["Ada Lovelace"], "en") == expected


def test_to_pdf_rights_credits_more_than_one_author():
    """The copyright line names the first author, then et al."""
    from commonmeta.io_utils import to_pdf_rights

    sample = sample_metadata("<p>Body</p>")
    sample.license = {"id": "CC-BY-4.0", "url": "https://example.org/by"}
    sample.date_published = "2024-05-06"

    rights = to_pdf_rights(sample, ["Ada Lovelace", "Charles Babbage"], "en")

    assert "Ada Lovelace et al. 2024." in rights


def test_to_pdf_html_keeps_the_markup_a_title_carries():
    """Post titles are html: an italicised species name is not the same string.

    https://rogue-scholar.org/records/0fvwt-b6s55 is one whose title reads
    wrong without it.
    """
    sample = sample_metadata(
        "<p>Body</p>",
        title="The atlas/axis complex of <i>Apatosaurus louisae</i> CM 3018",
    )
    sample.description = "A <em>very</em> short description"

    html = to_pdf_html(sample)

    assert (
        "<h1>The atlas/axis complex of <i>Apatosaurus louisae</i> CM 3018</h1>" in html
    )
    assert "<h4>Abstract</h4>A <em>very</em> short description</div>" in html
    # the pdf's own title is text, so the tags come out of it
    assert (
        "<title>The atlas/axis complex of Apatosaurus louisae CM 3018</title>" in html
    )


def test_to_pdf_html_drops_markup_that_is_not_inline():
    """Anything that would lay out, load or run is dropped, not shown as text."""
    sample = sample_metadata(
        "<p>Body</p>", title='Fish & <chips onclick="x()">today</chips>'
    )
    sample.description = "<script>alert(1)</script><p>A description</p>"

    html = to_pdf_html(sample)

    assert "<h1>Fish &amp; today</h1>" in html
    assert "<chips" not in html and "onclick" not in html
    assert '<div class="abstract"><h4>Abstract</h4>A description</div>' in html
    assert "alert(1)" not in html


def test_write_pdf_rendition_without_content(weasyprint):
    """A record with no post content is rendered as its title page alone.

    That is every input but a record read through the InvenioRDM reader, which
    is the one that carries the html of a post.
    """
    sample = sample_metadata(None, title="A record with no post behind it")

    pdf = write_pdf_rendition(sample, url_fetcher=offline_url_fetcher)

    metadata = read_pdf_metadata(pdf)
    assert metadata["title"] == "A record with no post behind it"
    assert metadata["variant"] == "PDF/A-3a"
    # the html the pdf was rendered from is the only file it ever carries
    assert "attachments" not in metadata


def test_upload_pdf_registers_uploads_and_commits():
    """InvenioRDM takes a file in three calls, in that order."""
    from commonmeta.writers import inveniordm_writer as w

    record = {"id": "fktsh-g4g95"}
    sample = sample_metadata("<p>Body</p>")
    with (
        patch.object(w, "write_pdf_rendition", return_value=b"%PDF-1.7 pdf"),
        patch.object(w, "http") as mock_http,
    ):
        mock_http.post.return_value.status_code = 201
        result = w.upload_pdf(sample, "rogue-scholar.org", "token", record)

    base = "https://rogue-scholar.org/api/records/fktsh-g4g95/draft/files"
    assert mock_http.post.call_args_list[0].args[0] == base
    assert mock_http.post.call_args_list[0].kwargs["json"] == [
        {"key": "10.53731-kdqkf-nf052.pdf"}
    ]
    assert mock_http.put.call_args.args[0] == f"{base}/10.53731-kdqkf-nf052.pdf/content"
    assert mock_http.put.call_args.kwargs["data"] == b"%PDF-1.7 pdf"
    assert (
        mock_http.post.call_args_list[1].args[0]
        == f"{base}/10.53731-kdqkf-nf052.pdf/commit"
    )
    assert result["files"] == ["10.53731-kdqkf-nf052.pdf"]


def test_upload_pdf_survives_a_refused_upload():
    """A published record's files are locked; the record is still published."""
    from commonmeta.writers import inveniordm_writer as w

    record = {"id": "fktsh-g4g95"}
    with (
        patch.object(w, "write_pdf_rendition", return_value=b"%PDF-1.7 pdf"),
        patch.object(w, "http") as mock_http,
    ):
        mock_http.post.return_value.status_code = 403
        result = w.upload_pdf(
            sample_metadata("<p>Body</p>"), "rogue-scholar.org", "token", record
        )

    mock_http.put.assert_not_called()
    assert "files" not in result
    assert "status" not in result


def test_to_pdf_byline_links_a_name_to_its_orcid():
    """An author with an orcid gets the iD icon, and the name carries the link."""
    from commonmeta.io_utils import to_pdf_byline

    byline = to_pdf_byline(
        [
            {"name": "Mike Taylor", "orcid": "0000-0002-1003-5675"},
            {"name": "Matt Wedel", "orcid": None},
        ]
    )

    assert byline == (
        '<p class="author">'
        '<a href="https://orcid.org/0000-0002-1003-5675"><span>Mike Taylor</span>'
        '<img class="orcid" alt="ORCID iD" src="orcid.svg" /></a>, '
        "<span>Matt Wedel</span></p>"
    )


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_to_pdf_authors_reads_the_orcid_of_each_author(feature_image):
    """The orcid comes off the contributor, validated rather than assumed."""
    from commonmeta.io_utils import to_pdf_authors

    subject = Metadata(
        "https://rogue-scholar.org/api/records/7tatc-wh557", via="inveniordm"
    )

    assert to_pdf_authors(subject) == [{"name": "Mark Dingemanse", "orcid": None}]

    subject.contributors[0]["person"]["id"] = "https://orcid.org/0000-0002-1003-5675"
    assert to_pdf_authors(subject) == [
        {"name": "Mark Dingemanse", "orcid": "0000-0002-1003-5675"}
    ]


def test_the_orcid_icon_ships_with_the_pdf_resources():
    """The byline references it next to the stylesheet, so it has to be there."""
    assert (PDF_RESOURCES / "orcid.svg").is_file()


def test_to_pdf_keywords_says_what_each_subject_is():
    """A record carries its classifications alongside the blog's own tags.

    The classification has an id saying what it is - an OpenAlex subfield or
    topic - and the tag the post gave itself has none, so a reader can tell
    which of them the post claimed for itself. The field of science is left
    out: it is the coarsest of them and says the least about a post.
    """
    from commonmeta.io_utils import to_pdf_keywords

    sample = sample_metadata("<p>Body</p>")
    sample.subjects = [
        {"id": "https://openalex.org/subfields/1203", "subject": "Language"},
        {"id": "https://openalex.org/T12417", "subject": "Morphology"},
        # the field of science is the coarsest classification, and left out
        {"id": "http://www.oecd.org/science/inno/38235147.pdf?6.2", "subject": "Arts"},
        {"subject": "Linguistics"},
        {"subject": "Threads"},
        {"scheme": "Keyword"},  # nothing to name
    ]

    assert to_pdf_keywords(sample) == [
        "Language (Subfield)",
        "Morphology (Topic)",
        "Linguistics",
        "Threads",
    ]

    sample.subjects = None
    assert to_pdf_keywords(sample) == []


@pytest.mark.vcr("test_rogue_scholar_blog_post.yaml")
def test_pdf_renders_the_orcid_icon_and_its_link(write_pdf_file):
    """The icon is drawn and the byline links to the orcid it belongs to."""
    import pikepdf

    subject = Metadata(
        "https://rogue-scholar.org/api/records/7tatc-wh557", via="inveniordm"
    )
    subject.contributors[0]["person"]["id"] = "https://orcid.org/0000-0002-1003-5675"

    pdf = write_pdf_file(subject)

    with pikepdf.open(BytesIO(pdf)) as document:
        links = [
            str(annotation.A.URI)
            for annotation in document.pages[0].get("/Annots", [])
            if "/A" in annotation and "/URI" in annotation.A
        ]
    assert "https://orcid.org/0000-0002-1003-5675" in links
