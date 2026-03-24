# pylint: disable=invalid-name,too-many-lines
"""InvenioRDM reader tests"""

from os import path

import pytest

from commonmeta import Metadata


@pytest.mark.vcr
def test_software():
    """Software"""
    string = path.join(path.dirname(__file__), "fixtures", "inveniordm-software.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.7752775"
    assert subject.type == "Software"
    assert subject.url == "https://zenodo.org/records/7752775"
    assert subject.titles[0] == {"title": "commonmeta-ruby"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "contributorRoles": ["Author"],
        "type": "Person",
        "id": "https://orcid.org/0000-0003-1419-2405",
        "affiliations": [{"name": "Front Matter"}],
        "familyName": "Fenner",
        "givenName": "Martin",
    }
    assert subject.license == {
        "id": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }

    assert subject.date == {
        "published": "2023-03-20",
        "updated": "2023-03-20T14:26:48Z",
    }
    assert subject.relations == [
        {
            "id": "https://github.com/front-matter/commonmeta-ruby/tree/v3.0.1",
            "type": "IsSupplementTo",
        },
        {"id": "https://doi.org/10.5281/zenodo.5785518", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Ruby gem and command-line utility for conversion of DOI metadata")
    )
    assert subject.subjects == [
        {"subject": "ruby"},
        {"subject": "metadata"},
        {"subject": "software citation"},
        {"subject": "research software"},
    ]
    assert subject.container == {
        "id": "https://www.re3data.org/repository/r3d100010468",
        "type": "Repository",
        "title": "Zenodo",
    }
    assert subject.language is None
    assert subject.version == "v3.0.1"
    assert subject.files == [
        {
            "bucket": "7cd6cc32-96a6-405d-b0ff-1811b378cc69",
            "checksum": "md5:3a1f043dffdd529035b7269449f17448",
            "key": "front-matter/commonmeta-ruby-v3.0.1.zip",
            "mimeType": "application/zip",
            "size": 5061453,
            "url": "https://zenodo.org/api/files/7cd6cc32-96a6-405d-b0ff-1811b378cc69/front-matter/commonmeta-ruby-v3.0.1.zip",
        },
    ]


@pytest.mark.vcr
def test_presentation():
    """Presentation"""
    string = "https://zenodo.org/api/records/8173303"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.8173303"
    assert subject.type == "Presentation"
    assert subject.url == "https://zenodo.org/records/8173303"
    assert subject.titles[0] == {
        "title": "ARCHIVE - 11 July 2023 (Day 2) CERN – NASA Open Science Summit Sketch Notes"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-8960-9642",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Heidi",
        "familyName": "Seibold",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2023-07-21",
        "updated": "2025-01-22T19:42:46Z",
    }
    assert subject.relations == [
        {"id": "https://doi.org/10.5281/zenodo.8173302", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("CERN/NASA “Accelerating the Adoption of Open Science”")
    )
    assert subject.subjects is None
    assert subject.container == {
        "id": "https://www.re3data.org/repository/r3d100010468",
        "type": "Repository",
        "title": "Zenodo",
    }
    assert subject.language is None
    assert subject.version is None
    assert subject.files == [
        {
            "key": "20230711-CERN-NASA-Open-Science-Summit-Summary-Drawings.pdf",
            "checksum": "md5:45d8b11d4ef0da78b9db5397d8e0e8d9",
            "url": "https://zenodo.org/api/records/8173303/files/20230711-CERN-NASA-Open-Science-Summit-Summary-Drawings.pdf/content",
            "size": 13994803,
        }
    ]


@pytest.mark.vcr
def test_publication():
    """Publication"""
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://zenodo.org/records/5244404"
    assert subject.titles[0] == {
        "title": "The Origins of SARS-CoV-2: A Critical Review"
    }
    assert len(subject.contributors) == 21
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Edward C",
        "familyName": "Holmes",
        "affiliations": [
            {
                "name": "School of Life and Environmental Sciences and School of Medical Sciences, The University of Sydney, Sydney, NSW 2006, Australia"
            }
        ],
    }
    assert subject.license == {
        "id": "CC-BY-NC-ND-4.0",
        "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2021-08-18",
        "updated": "2024-07-18T18:54:12Z",
    }
    assert subject.relations == [
        {"id": "https://doi.org/10.5281/zenodo.5075887", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("The Origins of SARS-CoV-2: A Critical Review Holmes et al.")
    )
    assert (
        subject.descriptions[1]
        .get("description")
        .startswith("Authors' final peer-reviewed version.")
    )
    assert subject.subjects == [
        {"subject": "sars-cov-2"},
        {"subject": "covid-19"},
        {"subject": "origins"},
        {"subject": "zoonosis"},
    ]
    assert subject.container == {
        "id": "https://www.re3data.org/repository/r3d100010468",
        "type": "Repository",
        "title": "Zenodo",
    }
    assert subject.language is None
    assert subject.version == "Authors' final version"
    assert len(subject.files) == 3
    assert subject.files[0] == {
        "key": "Holmes_et_al_(2021)_Cell_Supplementary.pdf",
        "checksum": "md5:bdb88fc94708d8fd7d87854031faa8ab",
        "url": "https://zenodo.org/api/records/5244404/files/Holmes_et_al_(2021)_Cell_Supplementary.pdf/content",
        "size": 197003,
    }


@pytest.mark.vcr
def test_publication_with_url():
    """Publication with URL"""
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string, url="https://zenodo.org/records/5075888")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://zenodo.org/records/5075888"
    assert subject.titles[0] == {
        "title": "The Origins of SARS-CoV-2: A Critical Review"
    }
    assert len(subject.contributors) == 21
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Edward C",
        "familyName": "Holmes",
        "affiliations": [
            {
                "name": "School of Life and Environmental Sciences and School of Medical Sciences, The University of Sydney, Sydney, NSW 2006, Australia"
            }
        ],
    }
    assert subject.license == {
        "id": "CC-BY-NC-ND-4.0",
        "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2021-08-18",
        "updated": "2024-07-18T18:54:12Z",
    }
    assert subject.relations == [
        {"id": "https://doi.org/10.5281/zenodo.5075887", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("The Origins of SARS-CoV-2: A Critical Review Holmes et al.")
    )
    assert (
        subject.descriptions[1]
        .get("description")
        .startswith("Authors' final peer-reviewed version.")
    )
    assert subject.subjects == [
        {"subject": "sars-cov-2"},
        {"subject": "covid-19"},
        {"subject": "origins"},
        {"subject": "zoonosis"},
    ]
    assert subject.container == {
        "id": "https://www.re3data.org/repository/r3d100010468",
        "type": "Repository",
        "title": "Zenodo",
    }
    assert subject.language is None
    assert subject.version == "Authors' final version"
    assert len(subject.files) == 3
    assert subject.files[0] == {
        "key": "Holmes_et_al_(2021)_Cell_Supplementary.pdf",
        "checksum": "md5:bdb88fc94708d8fd7d87854031faa8ab",
        "url": "https://zenodo.org/api/records/5244404/files/Holmes_et_al_(2021)_Cell_Supplementary.pdf/content",
        "size": 197003,
    }


@pytest.mark.vcr
def test_dataset():
    """Dataset"""
    string = "https://zenodo.org/api/records/7834392"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.7834392"
    assert subject.type == "Dataset"
    assert subject.url == "https://zenodo.org/records/7834392"
    assert subject.titles[0] == {
        "title": "A large-scale COVID-19 Twitter chatter dataset for open scientific research - an international collaboration"
    }
    assert len(subject.contributors) == 9
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0001-8499-824X",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Juan M.",
        "familyName": "Banda",
        "affiliations": [{"name": "Georgia State University"}],
    }
    assert subject.license == {"id": "other-pd"}
    assert subject.date == {
        "published": "2023-04-16",
        "updated": "2023-04-17T14:26:45Z",
    }
    assert subject.relations == [
        {"id": "https://arxiv.org/abs/2004.03688", "type": "IsSupplementTo"},
        {"id": "https://doi.org/10.5281/zenodo.3723939", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("<em><strong>Version 162&nbsp;of the dataset.")
    )
    assert (
        subject.descriptions[1]
        .get("description")
        .startswith(
            "This dataset will be updated bi-weekly at least with additional tweets, look at the github repo for these updates."
        )
    )
    assert subject.subjects == [
        {"subject": "social media"},
        {"subject": "twitter"},
        {"subject": "nlp"},
        {"subject": "covid-19"},
        {"subject": "covid19"},
    ]
    assert subject.container == {
        "id": "https://www.re3data.org/repository/r3d100010468",
        "type": "DataRepository",
        "title": "Zenodo",
    }
    assert subject.language == "en"
    assert subject.version == "162"
    assert len(subject.files) == 24
    assert subject.files[0] == {
        "key": "frequent_trigrams.csv",
        "checksum": "md5:b1f7edcfd008053c53659131f654f17d",
        "url": "https://zenodo.org/api/records/7834392/files/frequent_trigrams.csv/content",
        "size": 24991,
    }


@pytest.mark.vcr
def test_rogue_scholar():
    """Rogue Scholar"""
    string = "https://rogue-scholar.org/api/records/pevm6-kx104"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/5cj54-ha154"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://aarontay.substack.com/p/the-petrol-tank-for-ai-discovery"
    )
    assert subject.titles[0] == {
        "title": "The Petrol Tank for AI Discovery Might be Running Dry as Publishers close access to scholarly content such as abstracts due to AI incentives"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "id": "https://orcid.org/0000-0003-0159-013X",
        "contributorRoles": ["Author"],
        "givenName": "Aaron",
        "familyName": "Tay",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date["published"] == "2025-09-27T08:53:26"
    assert subject.relations == [
        {"id": "https://doi.org/10.59350/sfw0f-2fe65", "type": "IsVersionOf"}
    ]
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.citations is None
    assert subject.funding_references is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "Elicit.com, Consensus, and Undermind.ai are among the new leading comprehensive cross-disciplinary"
        )
    )
    assert subject.container == {
        "type": "Blog",
        "title": "Aaron Tay's Musings about librarianship",
        "identifier": "https://rogue-scholar.org/communities/musings",
        "identifierType": "URL",
        "platform": "Substack",
    }
    assert subject.subjects == [
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?5.9",
            "subject": "Other social sciences",
        }
    ]
    assert subject.language == "en"
    assert subject.version == "v1"


@pytest.mark.vcr
def test_rogue_scholar_with_citations():
    """Rogue Scholar"""
    string = "https://rogue-scholar.org/api/records/n5tg4-5h654"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.63485/mppz2-19243"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://www.earlham.edu/~peters/fos/2007/05/carl-zimmer-contrasts-wiley-and-plos.html"
    )
    assert subject.titles[0] == {"title": "Carl Zimmer contrasts Wiley and PLoS"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Peter",
        "familyName": "Suber",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date["published"] == "2007-05-24T16:09:00"
    assert subject.relations is None
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.funding_references is None
    assert subject.references is None
    assert subject.citations == [
        {
            "id": "https://doi.org/10.59350/4q8j1-1ap35",
            "unstructured": "Willighagen, E. (2007, May 25). Numbers are copyrighted?. <i>Chem-bla-ics</i>.",
        },
        {
            "id": "https://doi.org/10.59350/jtzzf-jfz50",
            "unstructured": "Willighagen, E. (2007, May 25). Numbers are copyrighted?. <i>Chem-bla-ics</i>.",
        },
    ]
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Carl Zimmer, An Open Mouse")
    )
    assert subject.container == {
        "type": "Blog",
        "title": "Open Access News",
        "identifier": "https://rogue-scholar.org/communities/oan",
        "identifierType": "URL",
        "platform": "Blogger",
    }
    assert subject.subjects == [
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?5",
            "subject": "Social science",
        }
    ]
    assert subject.language == "en"
    assert subject.version == "v1"
    assert subject.state == "findable"


@pytest.mark.vcr
def test_rogue_scholar_with_parent_doi():
    """Rogue Scholar with parent DOI"""
    string = "https://rogue-scholar.org/api/records/74hx4-qp390"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/qsajq-6tn97"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://svpow.com/2025/10/18/video-of-the-2024-ssp-debate-the-open-access-movement-has-failed/"
    )
    assert subject.titles[0] == {
        "title": 'Video of the 2024 SSP debate: "The open access movement has failed"'
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "id": "https://orcid.org/0000-0002-1003-5675",
        "contributorRoles": ["Author"],
        "givenName": "Mike",
        "familyName": "Taylor",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date["published"] == "2025-10-18T15:34:59"
    # assert subject.relations == [
    #     {"id": "https://doi.org/10.59350/t3d89-8jj38", "type": "IsVersionOf"}
    # ]
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.funding_references is None
    assert subject.references is None
    assert subject.citations is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "Readers with good memories will remember that back in May last year"
        )
    )
    assert subject.container == {
        "type": "Blog",
        "title": "Sauropod Vertebra Picture of the Week",
        "identifier": "3033-3695",
        "identifierType": "ISSN",
        "platform": "WordPress.com",
    }
    assert subject.subjects == [
        {"subject": "Conferences"},
        {"subject": "Debate"},
        {"subject": "Open Access"},
        {"subject": "SSP"},
        {"subject": "Stinkin' Publishers"},
        {"id": "https://openalex.org/subfields/1911", "subject": "Paleontology"},
    ]
    assert subject.language == "en"
    assert subject.version == "v1"
    assert subject.state == "findable"


@pytest.mark.vcr
def test_rogue_scholar_with_contributors():
    """Rogue Scholar"""
    string = "https://rogue-scholar.org/api/records/apt10-14q04"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/510pg-zzf58"
    assert subject.type == "BlogPost"
    assert subject.url == "https://ropensci.org/blog/2025/10/14/blog-roles/"
    assert subject.titles[0] == {"title": "Recognition Beyond Blog Post Authors"}
    assert len(subject.contributors) == 3
    assert subject.contributors[1] == {
        "id": "https://orcid.org/0000-0002-4522-7466",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Yanina",
        "familyName": "Bellini Saibene",
    }
    assert subject.contributors[2] == {
        "id": "https://orcid.org/0000-0002-7690-8360",
        "type": "Person",
        "contributorRoles": ["Editor"],
        "givenName": "Steffi",
        "familyName": "LaZerte",
    }


@pytest.mark.vcr
def test_subfield_classification():
    "subfield classification"
    string = "https://rogue-scholar.org/api/records/23y6y-vh985"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/qsajq-6tn97"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://svpow.com/2025/10/18/video-of-the-2024-ssp-debate-the-open-access-movement-has-failed/"
    )
    assert subject.titles[0] == {
        "title": 'Video of the 2024 SSP debate: "The open access movement has failed"'
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "Readers with good memories will remember that back in May last year"
        )
    )
    assert subject.subjects == [
        {"subject": "Conferences"},
        {"subject": "Debate"},
        {"subject": "Open Access"},
        {"subject": "SSP"},
        {"subject": "Stinkin' Publishers"},
        {"id": "https://openalex.org/subfields/1911", "subject": "Paleontology"},
    ]
