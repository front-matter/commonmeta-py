# pylint: disable=invalid-name
"""InvenioRDM writer tests"""

import re

import orjson as json
import pytest

from commonmeta import Metadata
from commonmeta.base_utils import dig


@pytest.mark.vcr
def test_publication():
    "publication"
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"

    inveniordm = json.loads(subject.write(to="inveniordm"))
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

    inveniordm = json.loads(subject.write(to="inveniordm"))
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
    assert len(related_identifiers) == 3
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

    inveniordm = json.loads(subject.write(to="inveniordm"))
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
            "id": "http://www.oecd.org/science/inno/38235147.pdf?1.2",
            "subject": "Computer and information sciences",
        },
        {"subject": "Rogue Scholar"},
    ]
    assert dig(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    assert dig(inveniordm, "metadata.identifiers") == [
        {
            "identifier": "c5c2e4e7-ac05-413b-b377-f989a72a5356",
            "scheme": "uuid",
        },
        {
            "identifier": "https://doi.org/10.53731/dv8z6-a6s33",
            "scheme": "guid",
        },
        {
            "identifier": "https://blog.front-matter.io/posts/rogue-scholar-learns-about-communities/",
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

    inveniordm = json.loads(subject.write(to="inveniordm"))
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
    string = "https://api.rogue-scholar.org/posts/525a7d13-fe07-4cab-ac54-75d7b7005647"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/dn2mm-m9q51"
    assert subject.type == "BlogPost"

    inveniordm = json.loads(subject.write(to="inveniordm"))
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
        {"date": "2021-07-22T09:39:07", "type": {"id": "issued"}},
        {"date": "2024-02-04T22:05:36", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "metadata.languages.0.id") == "eng"
    assert dig(inveniordm, "metadata.identifiers") == [
        {"identifier": "525a7d13-fe07-4cab-ac54-75d7b7005647", "scheme": "uuid"},
        {"identifier": "https://ideophone.org/?p=5639", "scheme": "guid"},
        {
            "identifier": "https://ideophone.org/linguistic-roots-of-connectionism",
            "scheme": "url",
        },
    ]
    assert dig(inveniordm, "metadata.version") == "v1"
    assert dig(inveniordm, "metadata.description").startswith(
        "A preprint claims that “ideas from theoretical linguistics have played no role"
    )
    assert dig(inveniordm, "metadata.subjects") == [
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?6.2",
            "subject": "Languages and literature",
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
        '\n<p>This <a rel="noreferrer noopener" href="https://ling.auf.net/lingbuzz/006031"'
    )
    assert dig(inveniordm, "custom_fields.rs:image") is None
    assert not dig(inveniordm, "files.enabled")


@pytest.mark.vcr
def test_from_jsonfeed_affiliations():
    "JSON Feed affiliations"
    string = "https://api.rogue-scholar.org/posts/10.59350/mg09a-5ma64"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/mg09a-5ma64"
    assert subject.type == "BlogPost"

    inveniordm = json.loads(subject.write(to="inveniordm"))
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
        == "Report on the Hands-On Lab ‘Scenarios for the Development of Open Access Repositories’ at the 112th BiblioCon"
    )
    assert dig(inveniordm, "metadata.publication_date") == "2024-07-15"
    assert dig(inveniordm, "metadata.dates") == [
        {"date": "2024-07-15T00:00:00", "type": {"id": "issued"}},
        {"date": "2024-07-15T00:00:00", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "metadata.languages.0.id") == "eng"
    assert dig(inveniordm, "metadata.identifiers") == [
        {"identifier": "6d1feb10-057a-4fc2-acb0-ac95e19741af", "scheme": "uuid"},
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
            "id": "http://www.oecd.org/science/inno/38235147.pdf?1.2",
            "subject": "Computer and information sciences",
        },
        {"subject": "Lab Life"},
        {"subject": "Research"},
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
        "<p>In the beginning of June 2024, Nature reported on the Japanese\nMinistry of Education’s plan to invest 10 billion"
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

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/k9zxj-pek64"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.publication_date") == "2018-08-28"
    assert dig(inveniordm, "metadata.dates") == [
        {
            "date": "2018-08-28T03:05:10",
            "type": {
                "id": "issued",
            },
        },
        {"date": "2018-10-19T23:13:05", "type": {"id": "updated"}},
    ]
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        "<p>I was lucky enough to have Phil Mannion as one of the peer-reviewers"
    )
    assert (
        dig(inveniordm, "custom_fields.rs:image")
        == "https://svpow.wordpress.com/wp-content/uploads/2018/08/figure-a-different-kinds-of-horizontal.jpeg?w=480&h=261"
    )


@pytest.mark.vcr
def test_from_jsonfeed_funding():
    "JSON Feed funding"
    string = "https://api.rogue-scholar.org/posts/10.59350/hnegw-6rx17"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/hnegw-6rx17"
    assert subject.type == "BlogPost"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/hnegw-6rx17"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "THOR Final Event programme is out!"
    assert dig(inveniordm, "metadata.funding") == [
        {
            "award": {
                "identifiers": [
                    {
                        "identifier": "10.3030/654039",
                        "scheme": "doi",
                    },
                ],
                "number": "654039",
                "title": {
                    "en": "THOR – Technical and Human Infrastructure for Open Research",
                },
            },
            "funder": {
                "id": "019w4f821",
                "name": "European Union",
            },
        }
    ]
    assert dig(inveniordm, "custom_fields.rs:content_html").startswith(
        "<p>Come and join us at the Università degli Studi di Roma"
    )
    assert dig(inveniordm, "custom_fields.rs:image") is None


@pytest.mark.vcr
def test_from_jsonfeed_more_funding():
    "JSON Feed more funding"
    string = "https://api.rogue-scholar.org/posts/10.59350/m99dx-x9g53"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/m99dx-x9g53"
    assert subject.type == "BlogPost"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/m99dx-x9g53"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "Summer Meeting of the Editorial Board"
    assert dig(inveniordm, "metadata.funding") == [
        {
            "award": {
                "identifiers": [
                    {
                        "identifier": "https://gepris.dfg.de/gepris/projekt/422587133",
                        "scheme": "url",
                    },
                ],
                "number": "422587133",
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

    inveniordm = json.loads(subject.write(to="inveniordm"))
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
        == "https://blog.front-matter.io/content/images/2023/09/cat_and_dog-1.png"
    )


@pytest.mark.vcr
def test_from_jsonfeed_unstructured_references():
    "JSON Feed unstructured references"
    string = "https://api.rogue-scholar.org/posts/10.59350/27ewm-zn378"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/27ewm-zn378"
    assert subject.type == "BlogPost"
    assert len(subject.references) == 7

    inveniordm = json.loads(subject.write(to="inveniordm"))
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
    assert len(subject.citations) == 2

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/dcw3y-7em87"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "Use of CiTO in CiteULike"
    citations = dig(inveniordm, "custom_fields.rs:citations")
    assert len(citations) == 2
    assert citations[0] == {
        "identifier": "10.1007/s11192-013-1108-3",
        "reference": "Parinov, S., &amp; Kogalovsky, M. (2013). Semantic linkages in research "
        "information systems as a new data source for scientometric studies. "
        "<i>Scientometrics</i>, <i>98</i>(2), 927–943.",
        "scheme": "doi",
    }


@pytest.mark.vcr
def test_from_jsonfeed_relations():
    "JSON Feed relations"
    string = "https://api.rogue-scholar.org/posts/10.54900/zg929-e9595"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.54900/zg929-e9595"
    assert subject.type == "BlogPost"

    inveniordm = json.loads(subject.write(to="inveniordm"))
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
    string = "https://api.rogue-scholar.org/posts/340de361-9628-481e-9204-527c679446b9"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/z78kb-qrz59"
    assert subject.type == "BlogPost"

    inveniordm = json.loads(subject.write(to="inveniordm"))
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

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert dig(inveniordm, "pids.doi.identifier") == "10.57689/dini-blog.20210712"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert (
        dig(inveniordm, "metadata.title")
        == "Eine Musterdienstvereinbarung fürs FIS – ein Beispiel der TIB"
    )


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

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert dig(inveniordm, "pids.doi.identifier") == "10.59350/vwd81-p8z85"
    assert dig(inveniordm, "metadata.resource_type.id") == "publication-blogpost"
    assert dig(inveniordm, "metadata.title") == "Archiving, but not really"
    assert re.search(
        'src="https://chem-bla-ics.linkedchemistry.info/assets/images/imageResolutionLoss.png"',
        dig(inveniordm, "custom_fields.rs:content_html"),
    )
