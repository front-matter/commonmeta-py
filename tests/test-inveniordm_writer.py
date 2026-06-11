# pylint: disable=invalid-name
"""InvenioRDM writer tests"""

import re
from unittest.mock import patch

import orjson as json
import pytest

from commonmeta import Metadata
from commonmeta.base_utils import dig
from commonmeta.writers.inveniordm_writer import upsert_record


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
        "reference": "APL regulates vascular tissue identity in Arabidopsis (2003).",
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
def test_rogue_scholar():
    "Rogue Scholar"
    string = "https://api.rogue-scholar.org/posts/10.53731/dv8z6-a6s33"
    subject = Metadata(string)
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
        {"date": "2024-10-07T02:00:00", "type": {"id": "issued"}},
        {"date": "2026-03-17T00:33:02", "type": {"id": "updated"}},
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
        {
            "identifier": "https://doi.org/10.53731/dv8z6-a6s33",
            "scheme": "guid",
        },
        {
            "identifier": "https://blog.front-matter.de/posts/rogue-scholar-learns-about-communities/",
            "scheme": "url",
        },
    ]
    assert dig(inveniordm, "metadata.related_identifiers") is None
    assert dig(inveniordm, "metadata.funding") is None
    assert dig(inveniordm, "custom_fields.journal:journal.title") == "Front Matter"
    assert dig(inveniordm, "custom_fields.journal:journal.issn") == "2749-9952"
    # assert dig(inveniordm, "custom_fields.rs:content_html").startswith("a")
    # assert dig(inveniordm, "custom_fields.rs:image") == 2
    assert not dig(inveniordm, "files.enabled")


@pytest.mark.vcr
def test_rogue_scholar_organizational_author():
    "Rogue Scholar organizational author"
    string = "https://api.rogue-scholar.org/posts/10.59350/wg8rv-awm24"
    subject = Metadata(string)
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


@pytest.mark.vcr
def test_from_jsonfeed():
    "JSON Feed"
    string = "https://api.rogue-scholar.org/posts/10.59350/dn2mm-m9q51"
    subject = Metadata(string)
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
        {"date": "2021-07-22T02:00:00", "type": {"id": "issued"}},
        {"date": "2026-02-15T08:37:27", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "metadata.languages.0.id") == "eng"
    assert dig(inveniordm, "metadata.identifiers") == [
        {"identifier": "https://ideophone.org/?p=5639", "scheme": "guid"},
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


@pytest.mark.vcr
def test_from_jsonfeed_affiliations():
    "JSON Feed affiliations"
    string = "https://api.rogue-scholar.org/posts/10.59350/mg09a-5ma64"
    subject = Metadata(string)
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
            "family_name": "Beucke",
            "given_name": "Daniel",
            "name": "Beucke, Daniel",
            "type": "personal",
            "identifiers": [{"identifier": "0000-0003-4905-1936", "scheme": "orcid"}],
        },
        "affiliations": [
            {
                "id": "05745n787",
                "name": "Göttingen State and University Library",
            },
        ],
    }
    assert (
        dig(inveniordm, "metadata.title")
        == "Report on the Hands-On Lab 'Scenarios for the Development of Open Access Repositories' at the 112th BiblioCon"
    )
    assert dig(inveniordm, "metadata.publication_date") == "2024-07-14"
    assert dig(inveniordm, "metadata.dates") == [
        {"date": "2024-07-14T02:00:00", "type": {"id": "issued"}},
        {"date": "2026-01-25T06:36:25", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "metadata.languages.0.id") == "eng"
    assert dig(inveniordm, "metadata.identifiers") == [
        {
            "identifier": "https://infomgnt.org/posts/2024-07-15-hands-on-lab-report/",
            "scheme": "guid",
        },
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


@pytest.mark.vcr
def test_from_jsonfeed_dates():
    "JSON Feed dates"
    string = "https://api.rogue-scholar.org/posts/10.59350/k9zxj-pek64"
    subject = Metadata(string)
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
        {
            "date": "2018-08-28T02:00:00",
            "type": {
                "id": "issued",
            },
        },
        {"date": "2025-12-06T00:28:54", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        "<p>I was lucky enough to have Phil Mannion as one of the peer-reviewers"
    )
    assert dig(inveniordm, "custom_fields.rs:image") is None


@pytest.mark.vcr
def test_from_jsonfeed_funding():
    "JSON Feed funding"
    string = "https://api.rogue-scholar.org/posts/10.59350/hnegw-6rx17"
    subject = Metadata(string)
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


@pytest.mark.vcr
def test_from_jsonfeed_more_funding():
    "JSON Feed more funding"
    string = "https://api.rogue-scholar.org/posts/10.59350/m99dx-x9g53"
    subject = Metadata(string)
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


@pytest.mark.vcr
def test_from_jsonfeed_references():
    "JSON Feed references"
    string = "https://api.rogue-scholar.org/posts/10.53731/r79v4e1-97aq74v-ag578"
    subject = Metadata(string)
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
    assert len(related_identifiers) == 1
    assert related_identifiers[0] == {
        "identifier": "10.5438/bc11-cqw1",
        "relation_type": {"id": "isidenticalto"},
        "scheme": "doi",
    }
    assert dig(inveniordm, "metadata.funding") == [
        {
            "award": {
                "number": "654039",
                "identifiers": [{"scheme": "doi", "identifier": "10.3030/654039"}],
            },
            "funder": {
                "id": "00k4n6c32",
                "name": "European Commission",
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


@pytest.mark.vcr
def test_from_jsonfeed_unstructured_references():
    "JSON Feed unstructured references"
    string = "https://api.rogue-scholar.org/posts/10.59350/27ewm-zn378"
    subject = Metadata(string)
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
        "reference": "Fang, F. C., Casadevall, A., &amp; Morrison, R. P. (2011). Retracted Science and the Retraction Index. <i>Infection and Immunity</i>, <i>79</i>(10), 3855–3859.",
        "scheme": "doi",
    }


@pytest.mark.vcr
def test_from_jsonfeed_citations():
    "JSON Feed citations"
    string = "https://api.rogue-scholar.org/posts/10.59350/dcw3y-7em87"
    subject = Metadata(string)
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
    citations = dig(inveniordm, "custom_fields.rs:citations")
    # assert len(citations) == 2
    # assert citations[0] == {
    #     "identifier": "10.1007/s11192-013-1108-3",
    #     "reference": "Parinov, S., &amp; Kogalovsky, M. (2013). Semantic linkages in research "
    #     "information systems as a new data source for scientometric studies. "
    #     "<i>Scientometrics</i>, <i>98</i>(2), 927–943.",
    #     "scheme": "doi",
    # }


@pytest.mark.vcr
def test_from_jsonfeed_relations():
    "JSON Feed relations"
    string = "https://api.rogue-scholar.org/posts/10.54900/zg929-e9595"
    subject = Metadata(string)
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
    assert len(related_identifiers) == 1
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


@pytest.mark.vcr
def test_from_jsonfeed_broken_reference():
    "JSON Feed relations"
    string = "https://api.rogue-scholar.org/posts/10.59350/z78kb-qrz59"
    subject = Metadata(string)
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


@pytest.mark.vcr
def test_external_doi():
    "external DOI used by Rogue Scholar"
    string = "https://api.rogue-scholar.org/posts/10.57689/dini-blog.20210712"
    subject = Metadata(string)
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


@pytest.mark.vcr
def test_post_with_contributor_roles():
    "post with contributor roles"
    string = "https://api.rogue-scholar.org/posts/10.59350/510pg-zzf58"
    subject = Metadata(string)
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


@pytest.mark.vcr
def test_post_with_interviewee_roles():
    "post with interviewee roles"
    string = "https://api.rogue-scholar.org/posts/10.59350/s8m95-ap410"
    subject = Metadata(string)
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


@pytest.mark.vcr
def test_multiple_subfields():
    "post with multiple subfields"
    string = "https://api.rogue-scholar.org/posts/10.59350/1srmw-yb311"
    subject = Metadata(string)
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
        {"subject": "Publishing"},
        {"subject": "Science"},
        {"subject": "Cancer"},
        {"subject": "Cell Biology"},
        {"subject": "FGFR3"},
    ]


@pytest.mark.vcr
def test_content_with_external_src():
    "external DOI used by Rogue Scholar"
    string = "https://api.rogue-scholar.org/posts/10.59350/vwd81-p8z85"
    subject = Metadata(string)
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


@pytest.mark.vcr("test_from_jsonfeed.yaml")
def test_upsert_record_falls_back_to_guid():
    "upsert_record uses GUID from output identifiers when DOI lookup returns None"
    string = "https://api.rogue-scholar.org/posts/10.59350/dn2mm-m9q51"
    subject = Metadata(string)
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
