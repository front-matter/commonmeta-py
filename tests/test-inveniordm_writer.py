# pylint: disable=invalid-name
"""InvenioRDM writer tests"""

import orjson as json
import pytest
from pydash import py_

from commonmeta import Metadata


@pytest.mark.vcr
def test_publication():
    "publication"
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.5281/zenodo.5244404"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-article"
    assert len(py_.get(inveniordm, "metadata.creators")) == 21
    assert py_.get(inveniordm, "metadata.creators.0") == {
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
        py_.get(inveniordm, "metadata.title")
        == "The Origins of SARS-CoV-2: A Critical Review"
    )
    assert py_.get(inveniordm, "metadata.publisher") == "Zenodo"
    assert py_.get(inveniordm, "metadata.publication_date") == "2021-08-18"
    assert py_.get(inveniordm, "metadata.languages.0.id") is None
    assert py_.get(inveniordm, "metadata.version") == "Authors' final version"
    assert py_.get(inveniordm, "metadata.description").startswith(
        "The Origins of SARS-CoV-2: A Critical Review"
    )
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-nc-nd-4.0"}]
    assert py_.get(inveniordm, "metadata.identifiers") == [
        {"identifier": "https://zenodo.org/records/5244404", "scheme": "url"}
    ]
    assert py_.get(inveniordm, "metadata.related_identifiers") == [
        {
            "identifier": "10.5281/zenodo.5075887",
            "relation_type": {"id": "isversionof"},
            "scheme": "doi",
        }
    ]
    assert py_.get(inveniordm, "metadata.funding") is None
    assert py_.get(inveniordm, "metadata.content") is None
    assert py_.get(inveniordm, "metadata.image") is None
    assert py_.get(inveniordm, "files.enabled") == False


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-article"
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.7554/elife.01567"
    assert len(py_.get(inveniordm, "metadata.creators")) == 5
    assert py_.get(inveniordm, "metadata.creators.0") == {
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
        py_.get(inveniordm, "metadata.title")
        == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert (
        py_.get(inveniordm, "metadata.publisher") == "eLife Sciences Publications, Ltd"
    )
    assert py_.get(inveniordm, "metadata.publication_date") == "2014-02-11"
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "Among various advantages, their small size makes model organisms preferred subjects of investigation."
    )
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-3.0"}]
    assert py_.get(inveniordm, "metadata.identifiers") == [
        {"identifier": "https://elifesciences.org/articles/01567", "scheme": "url"}
    ]
    related_identifiers = py_.get(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 30
    assert related_identifiers[0] == {
        "identifier": "10.1038/nature02100",
        "relation_type": {
            "id": "references",
        },
        "scheme": "doi",
    }
    assert related_identifiers[27] == {
        "identifier": "10.5061/dryad.b835k",
        "relation_type": {
            "id": "issupplementedby",
        },
        "scheme": "doi",
    }
    assert related_identifiers[28] == {
        "identifier": "10.7554/elife.01567.017",
        "relation_type": {
            "id": "isreviewedby",
        },
        "scheme": "doi",
    }
    assert py_.get(inveniordm, "metadata.funding") == [
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
    assert py_.get(inveniordm, "metadata.content") is None
    assert py_.get(inveniordm, "metadata.image") is None
    assert py_.get(inveniordm, "files.enabled") == False


@pytest.mark.vcr
def test_rogue_scholar():
    "Rogue Scholar"
    string = "https://beta.rogue-scholar.org/api/records/1xr7q-9fp18"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/dv8z6-a6s33"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.53731/dv8z6-a6s33"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert len(py_.get(inveniordm, "metadata.creators")) == 1
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Fenner",
            "given_name": "Martin",
            "name": "Fenner, Martin",
            "type": "personal",
            "identifiers": [{"identifier": "0000-0003-1419-2405", "scheme": "orcid"}],
        }
    }
    assert (
        py_.get(inveniordm, "metadata.title")
        == "Rogue Scholar learns about communities"
    )
    assert py_.get(inveniordm, "metadata.publisher") is None
    assert py_.get(inveniordm, "metadata.publication_date") == "2024-10-07"

    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2024-10-17T18:54:34Z", "type": {"id": "updated"}}
    ]
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "The Rogue Scholar infrastructure started migrating to InvenioRDM infrastructure a few weeks ago."
    )
    assert py_.get(inveniordm, "metadata.subjects") is None
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    assert py_.get(inveniordm, "metadata.identifiers") == [
        {
            "identifier": "https://beta.rogue-scholar.org/records/1xr7q-9fp18",
            "scheme": "url",
        }
    ]
    assert py_.get(inveniordm, "metadata.related_identifiers") is None
    assert py_.get(inveniordm, "metadata.funding") is None
    assert py_.get(inveniordm, "custom_fields.journal:journal.title") == "Front Matter"
    assert py_.get(inveniordm, "custom_fields.journal:journal.issn") == "2749-9952"
    # assert py_.get(inveniordm, "metadata.content").startswith("a")
    # assert py_.get(inveniordm, "metadata.image") == 2
    assert py_.get(inveniordm, "files.enabled") == False


@pytest.mark.vcr
def test_from_json_feed():
    "JSON Feed"
    string = "https://api.rogue-scholar.org/posts/525a7d13-fe07-4cab-ac54-75d7b7005647"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/dn2mm-m9q51"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/dn2mm-m9q51"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert len(py_.get(inveniordm, "metadata.creators")) == 1
    assert py_.get(inveniordm, "metadata.creators.0") == {
        "person_or_org": {
            "family_name": "Dingemanse",
            "given_name": "Mark",
            "name": "Dingemanse, Mark",
            "type": "personal",
        },
    }
    assert py_.get(inveniordm, "metadata.title") == "Linguistic roots of connectionism"
    assert py_.get(inveniordm, "metadata.publication_date") == "2021-07-22"
    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2024-02-04T22:05:36", "type": {"id": "updated"}}
    ]
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.identifiers") == [
        {"identifier": "525a7d13-fe07-4cab-ac54-75d7b7005647", "scheme": "uuid"},
        {"identifier": "https://ideophone.org/?p=5639", "scheme": "guid"},
        {
            "identifier": "https://ideophone.org/linguistic-roots-of-connectionism",
            "scheme": "url",
        },
    ]
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "This Lingbuzz preprint by Baroni is a nice read"
    )
    assert py_.get(inveniordm, "metadata.subjects") == [
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?6.2",
            "subject": "Languages and literature",
        },
        {"subject": "Linguistics"},
        {"subject": "Threads"},
    ]
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    related_identifiers = py_.get(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 7
    assert related_identifiers[0] == {
        "identifier": "https://ling.auf.net/lingbuzz/006031",
        "relation_type": {
            "id": "references",
        },
        "scheme": "url",
    }
    assert related_identifiers[1] == {
        "identifier": "10.1038/s41562-017-0163",
        "relation_type": {
            "id": "references",
        },
        "scheme": "doi",
    }
    assert py_.get(inveniordm, "custom_fields.journal:journal.title") == "The Ideophone"
    assert py_.get(inveniordm, "custom_fields.journal:journal.issn") is None
    assert py_.get(inveniordm, "metadata.content").startswith(
        "This [Lingbuzz preprint by\nBaroni](https://ling.auf.net/lingbuzz/006031)"
    )
    assert (
        py_.get(inveniordm, "metadata.image")
        == "https://pbs.twimg.com/media/E4FDxONXwAMFvCh.png"
    )
    assert py_.get(inveniordm, "files.enabled") == False


@pytest.mark.vcr
def test_from_json_feed_affiliations():
    "JSON Feed affiliations"
    string = "https://api.rogue-scholar.org/posts/10.59350/mg09a-5ma64"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/mg09a-5ma64"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/mg09a-5ma64"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert len(py_.get(inveniordm, "metadata.creators")) == 4
    assert py_.get(inveniordm, "metadata.creators.0") == {
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
        py_.get(inveniordm, "metadata.title")
        == "Report on the Hands-On Lab ‘Scenarios for the Development of Open Access Repositories’ at the 112th BiblioCon"
    )
    assert py_.get(inveniordm, "metadata.publication_date") == "2024-07-15"
    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2024-07-15T00:00:00", "type": {"id": "updated"}}
    ]
    assert py_.get(inveniordm, "metadata.languages.0.id") == "eng"
    assert py_.get(inveniordm, "metadata.identifiers") == [
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
    assert py_.get(inveniordm, "metadata.version") is None
    assert py_.get(inveniordm, "metadata.description").startswith(
        "In the beginning of June 2024,"
    )
    assert py_.get(inveniordm, "metadata.subjects") == [
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?1.2",
            "subject": "Computer and information sciences",
        },
        {"subject": "Lab Life"},
        {"subject": "Research"},
    ]
    assert py_.get(inveniordm, "metadata.rights") == [{"id": "cc-by-4.0"}]
    related_identifiers = py_.get(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 4
    assert py_.get(inveniordm, "metadata.related_identifiers[0]") == {
        "identifier": "10.1007/978-3-658-01928-0",
        "relation_type": {"id": "references"},
        "scheme": "doi",
    }
    assert (
        py_.get(inveniordm, "custom_fields.journal:journal.title")
        == "Research Group Information Management @ Humboldt-Universität zu Berlin"
    )
    assert py_.get(inveniordm, "custom_fields.journal:journal.issn") is None
    assert py_.get(inveniordm, "metadata.content").startswith(
        "In the beginning of June 2024, Nature reported on the Japanese Ministry\nof Education's plan to invest 10 billion yen"
    )
    assert (
        py_.get(inveniordm, "metadata.image")
        == "https://infomgnt.org/posts/2024-07-15-hands-on-lab-report/112th_bibliocon.jpeg"
    )
    assert py_.get(inveniordm, "files.enabled") == False


@pytest.mark.vcr
def test_from_json_feed_dates():
    "JSON Feed dates"
    string = "https://api.rogue-scholar.org/posts/10.59350/k9zxj-pek64"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/k9zxj-pek64"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/k9zxj-pek64"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert py_.get(inveniordm, "metadata.publication_date") == "2018-08-28"
    assert py_.get(inveniordm, "metadata.dates") == [
        {"date": "2018-10-19T23:13:05", "type": {"id": "updated"}}
    ]
    assert py_.get(inveniordm, "metadata.content").startswith(
        "I was lucky enough to have Phil Mannion as one of the peer-reviewers"
    )
    assert (
        py_.get(inveniordm, "metadata.image")
        == "https://svpow.files.wordpress.com/2018/08/figure-a-different-kinds-of-horizontal.jpeg?w=480&h=261"
    )


@pytest.mark.vcr
def test_from_json_feed_funding():
    "JSON Feed funding"
    string = "https://api.rogue-scholar.org/posts/10.59350/hnegw-6rx17"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/hnegw-6rx17"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/hnegw-6rx17"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert py_.get(inveniordm, "metadata.title") == "THOR Final Event programme is out!"
    assert py_.get(inveniordm, "metadata.funding") == [
        {
            "award": {"number": "654039"},
            "funder": {
                "id": "00k4n6c32",
                "name": "European Union’s Horizon 2020 research and innovation programme",
            },
        }
    ]
    assert py_.get(inveniordm, "metadata.content").startswith(
        "Come and join us at the Università degli Studi di Roma"
    )
    assert py_.get(inveniordm, "metadata.image") is None


@pytest.mark.vcr
def test_from_json_feed_more_funding():
    "JSON Feed more funding"
    string = "https://api.rogue-scholar.org/posts/10.59350/m99dx-x9g53"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/m99dx-x9g53"
    assert subject.type == "Article"
    print(subject.references)

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.59350/m99dx-x9g53"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert (
        py_.get(inveniordm, "metadata.title") == "Summer Meeting of the Editorial Board"
    )
    assert py_.get(inveniordm, "metadata.funding") == [
        {
            "award": {"number": "422587133"},
            "funder": {
                "id": "018mejw64",
                "name": "Deutsche Forschungsgemeinschaft",
            },
        }
    ]
    assert py_.get(inveniordm, "metadata.content").startswith(
        "![](/images/7/b/6/1/b/7b61bcef98211c200b6c508c172e8833ae50caaa-working.jpg)\n\nSummer Meeting of the Editorial Board"
    )
    assert (
        py_.get(inveniordm, "metadata.image")
        == "https://coref.project.re3data.org/images/7/b/6/1/b/7b61bcef98211c200b6c508c172e8833ae50caaa-working.jpg"
    )


@pytest.mark.vcr
def test_from_json_feed_references():
    "JSON Feed references"
    string = "https://api.rogue-scholar.org/posts/10.53731/r79v4e1-97aq74v-ag578"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/r79v4e1-97aq74v-ag578"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert (
        py_.get(inveniordm, "pids.doi.identifier") == "10.53731/r79v4e1-97aq74v-ag578"
    )
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert (
        py_.get(inveniordm, "metadata.title")
        == "Differences between ORCID and DataCite Metadata"
    )
    related_identifiers = py_.get(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 2
    assert related_identifiers[0] == {
        "identifier": "10.5281/zenodo.30799",
        "relation_type": {"id": "references"},
        "scheme": "doi",
    }
    assert related_identifiers[1] == {
        "identifier": "10.5438/bc11-cqw1",
        "relation_type": {"id": "isidenticalto"},
        "scheme": "doi",
    }
    assert py_.get(inveniordm, "metadata.funding") == [
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
    assert py_.get(inveniordm, "metadata.content").startswith(
        "One of the first tasks for DataCite"
    )
    assert (
        py_.get(inveniordm, "metadata.image")
        == "https://blog.front-matter.io/content/images/2023/09/cat_and_dog-1.png"
    )


@pytest.mark.vcr
def test_from_json_feed_relations():
    "JSON Feed relations"
    string = "https://api.rogue-scholar.org/posts/10.54900/zg929-e9595"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.54900/zg929-e9595"
    assert subject.type == "Article"

    inveniordm = json.loads(subject.write(to="inveniordm"))
    assert py_.get(inveniordm, "pids.doi.identifier") == "10.54900/zg929-e9595"
    assert py_.get(inveniordm, "metadata.resource_type.id") == "publication-preprint"
    assert py_.get(inveniordm, "metadata.title") == "Large Language Publishing"
    related_identifiers = py_.get(inveniordm, "metadata.related_identifiers")
    assert len(related_identifiers) == 1
    assert related_identifiers[0] == {
        "identifier": "10.18357/kula.291",
        "relation_type": {"id": "ispreviousversionof"},
        "scheme": "doi",
    }
    assert py_.get(inveniordm, "metadata.content").startswith(
        "*The New York Times* ushered in the New Year with"
    )
    assert (
        py_.get(inveniordm, "metadata.image")
        == "https://upstream.force11.org/content/images/2023/12/pexels-viktor-talashuk-2377295.jpg"
    )
