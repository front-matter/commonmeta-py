# pylint: disable=invalid-name,too-many-lines
"""InvenioRDM reader tests"""

from os import path
from unittest.mock import MagicMock, patch

import pytest

from commonmeta import Metadata
from commonmeta.readers.inveniordm_reader import search_by_doi, search_by_guid


@pytest.mark.vcr
def test_software():
    """Software"""
    string = path.join(path.dirname(__file__), "fixtures", "inveniordm-software.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.7752775"
    assert subject.type == "Software"
    assert subject.url == "https://zenodo.org/records/7752775"
    assert subject.title == "commonmeta-ruby"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "given_name": "Martin",
            "family_name": "Fenner",
            "affiliations": [{"name": "Front Matter"}],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "MIT",
        "title": "MIT License",
        "url": "https://opensource.org/license/mit/",
    }

    assert (
        subject.date_published == "2023-03-20"
        and subject.date_updated == "2023-03-20T14:26:48Z"
    )
    assert subject.relations == [
        {
            "id": "https://github.com/front-matter/commonmeta-ruby/tree/v3.0.1",
            "type": "IsSupplementTo",
        },
        {"id": "https://doi.org/10.5281/zenodo.5785518", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert subject.description.startswith(
        "Ruby gem and command-line utility for conversion of DOI metadata"
    )
    assert subject.subjects == [
        {"subject": "ruby"},
        {"subject": "metadata"},
        {"subject": "software citation"},
        {"subject": "research software"},
    ]
    assert subject.container == {
        "identifier": "https://www.re3data.org/repository/r3d100010468",
        "identifier_type": "URL",
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
            "mime_type": "application/zip",
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
    assert (
        subject.title
        == "ARCHIVE - 11 July 2023 (Day 2) CERN – NASA Open Science Summit Sketch Notes"
    )
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-8960-9642",
            "given_name": "Heidi",
            "family_name": "Seibold",
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2023-07-21"
        and subject.date_updated == "2025-01-22T19:42:46Z"
    )
    assert subject.relations == [
        {"id": "https://doi.org/10.5281/zenodo.8173302", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert subject.description.startswith(
        "CERN/NASA “Accelerating the Adoption of Open Science”"
    )
    assert subject.subjects is None
    assert subject.container == {
        "identifier": "https://www.re3data.org/repository/r3d100010468",
        "identifier_type": "URL",
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
    assert subject.title == "The Origins of SARS-CoV-2: A Critical Review"
    assert len(subject.contributors) == 21
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Edward C",
            "family_name": "Holmes",
            "affiliations": [
                {
                    "name": "School of Life and Environmental Sciences and School of Medical Sciences, The University of Sydney, Sydney, NSW 2006, Australia"
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-NC-ND-4.0",
        "title": "Creative Commons Attribution Non Commercial No Derivatives 4.0 International",
        "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
    }

    assert (
        subject.date_published == "2021-08-18"
        and subject.date_updated == "2024-07-18T18:54:12Z"
    )
    assert subject.relations == [
        {"id": "https://doi.org/10.5281/zenodo.5075887", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert subject.description.startswith(
        "The Origins of SARS-CoV-2: A Critical Review Holmes et al."
    )
    assert subject.additional_descriptions[0]["description"].startswith(
        "Authors' final peer-reviewed version."
    )
    assert subject.subjects == [
        {"subject": "sars-cov-2"},
        {"subject": "covid-19"},
        {"subject": "origins"},
        {"subject": "zoonosis"},
    ]
    assert subject.container == {
        "identifier": "https://www.re3data.org/repository/r3d100010468",
        "identifier_type": "URL",
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
    assert subject.title == "The Origins of SARS-CoV-2: A Critical Review"
    assert len(subject.contributors) == 21
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Edward C",
            "family_name": "Holmes",
            "affiliations": [
                {
                    "name": "School of Life and Environmental Sciences and School of Medical Sciences, The University of Sydney, Sydney, NSW 2006, Australia"
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-NC-ND-4.0",
        "title": "Creative Commons Attribution Non Commercial No Derivatives 4.0 International",
        "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
    }

    assert (
        subject.date_published == "2021-08-18"
        and subject.date_updated == "2024-07-18T18:54:12Z"
    )
    assert subject.relations == [
        {"id": "https://doi.org/10.5281/zenodo.5075887", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert subject.description.startswith(
        "The Origins of SARS-CoV-2: A Critical Review Holmes et al."
    )
    assert subject.additional_descriptions[0]["description"].startswith(
        "Authors' final peer-reviewed version."
    )
    assert subject.subjects == [
        {"subject": "sars-cov-2"},
        {"subject": "covid-19"},
        {"subject": "origins"},
        {"subject": "zoonosis"},
    ]
    assert subject.container == {
        "identifier": "https://www.re3data.org/repository/r3d100010468",
        "identifier_type": "URL",
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
    assert (
        subject.title
        == "A large-scale COVID-19 Twitter chatter dataset for open scientific research - an international collaboration"
    )
    assert len(subject.contributors) == 9
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-8499-824X",
            "given_name": "Juan M.",
            "family_name": "Banda",
            "affiliations": [{"name": "Georgia State University"}],
        },
        "roles": ["Author"],
    }
    assert subject.license == {"id": "other-pd"}
    assert (
        subject.date_published == "2023-04-16"
        and subject.date_updated == "2023-04-17T14:26:45Z"
    )
    assert subject.relations == [
        {"id": "https://arxiv.org/abs/2004.03688", "type": "IsSupplementTo"},
        {"id": "https://doi.org/10.5281/zenodo.3723939", "type": "IsVersionOf"},
    ]
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.funding_references is None
    assert subject.description.startswith("<em><strong>Version 162 of the dataset.")
    assert subject.additional_descriptions[0]["description"].startswith(
        "This dataset will be updated bi-weekly at least with additional tweets, look at the github repo for these updates."
    )
    assert subject.subjects == [
        {"subject": "social media"},
        {"subject": "twitter"},
        {"subject": "nlp"},
        {"subject": "covid-19"},
        {"subject": "covid19"},
    ]
    assert subject.container == {
        "identifier": "https://www.re3data.org/repository/r3d100010468",
        "identifier_type": "URL",
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
    assert (
        subject.title
        == "The Petrol Tank for AI Discovery Might be Running Dry as Publishers close access to scholarly content such as abstracts due to AI incentives"
    )
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-0159-013X",
            "given_name": "Aaron",
            "family_name": "Tay",
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == "2025-09-27T08:53:26"
    assert subject.relations == [
        {"id": "https://doi.org/10.59350/sfw0f-2fe65", "type": "IsVersionOf"},
        {"id": "https://doi.org/10.59350/musings", "type": "IsPartOf"},
    ]
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.funding_references is None
    assert subject.description.startswith(
        "Elicit.com, Consensus, and Undermind.ai are among the new leading comprehensive cross-disciplinary"
    )
    assert subject.container == {
        "type": "Blog",
        "title": "Aaron Tay's Musings about Librarianship",
        "identifier": "https://doi.org/10.59350/musings",
        "identifier_type": "DOI",
    }
    assert subject.subjects == [
        {
            "id": "https://openalex.org/subfields/3309",
            "subject": "Library and Information Sciences",
        },
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?6.5",
            "subject": "Other humanities",
        },
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
    assert subject.title == "Carl Zimmer contrasts Wiley and PLoS"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Peter", "family_name": "Suber"},
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == "2007-05-24T16:09:00"
    # citing works are represented as IsReferencedBy relations
    assert subject.relations == [
        {"id": "https://doi.org/10.59350/4q8j1-1ap35", "type": "IsReferencedBy"},
        {"id": "https://doi.org/10.59350/jtzzf-jfz50", "type": "IsReferencedBy"},
        {"id": "https://doi.org/10.63485/enjv5-xh191", "type": "IsVersionOf"},
        {"id": "https://doi.org/10.63485/oan", "type": "IsPartOf"},
    ]
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.funding_references is None
    assert subject.references is None
    assert subject.description.startswith("Carl Zimmer, An Open Mouse")
    assert subject.container == {
        "type": "Blog",
        "title": "Open Access News",
        "identifier": "https://doi.org/10.63485/oan",
        "identifier_type": "DOI",
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
    assert (
        subject.title
        == 'Video of the 2024 SSP debate: "The open access movement has failed"'
    )
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-1003-5675",
            "given_name": "Mike",
            "family_name": "Taylor",
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == "2025-10-18T15:34:59"
    # assert subject.relations == [
    #     {"id": "https://doi.org/10.59350/t3d89-8jj38", "type": "IsVersionOf"}
    # ]
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.funding_references is None
    assert subject.references is None
    assert subject.description.startswith(
        "Readers with good memories will remember that back in May last year"
    )
    assert subject.container == {
        "type": "Blog",
        "title": "Sauropod Vertebra Picture of the Week",
        "identifier": "3033-3695",
        "identifier_type": "ISSN",
    }
    assert subject.subjects == [
        {
            "id": "https://openalex.org/subfields/1911",
            "subject": "Paleontology",
        },
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?1.5",
            "subject": "Earth and related environmental sciences",
        },
        {"subject": "Conferences"},
        {"subject": "Debate"},
        {"subject": "Open Access"},
        {"subject": "SSP"},
        {"subject": "Stinkin' Publishers"},
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
    assert subject.title == "Recognition Beyond Blog Post Authors"
    assert len(subject.contributors) == 3
    assert subject.contributors[1] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-4522-7466",
            "given_name": "Yanina",
            "family_name": "Bellini Saibene",
        },
        "roles": ["Author"],
    }
    assert subject.contributors[2] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-7690-8360",
            "given_name": "Steffi",
            "family_name": "LaZerte",
        },
        "roles": ["Editor"],
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
    assert (
        subject.title
        == 'Video of the 2024 SSP debate: "The open access movement has failed"'
    )
    assert subject.description.startswith(
        "Readers with good memories will remember that back in May last year"
    )
    assert subject.subjects == [
        {
            "id": "https://openalex.org/subfields/1911",
            "subject": "Paleontology",
        },
        {
            "id": "http://www.oecd.org/science/inno/38235147.pdf?1.5",
            "subject": "Earth and related environmental sciences",
        },
        {"subject": "Conferences"},
        {"subject": "Debate"},
        {"subject": "Open Access"},
        {"subject": "SSP"},
        {"subject": "Stinkin' Publishers"},
    ]


# --- Unit tests for search_by_guid / search_by_doi ---


def _mock_response(status_code: int, payload: dict) -> MagicMock:
    """Build a minimal mock requests.Response."""
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = payload
    if status_code >= 400:
        from requests.exceptions import HTTPError

        response.raise_for_status.side_effect = HTTPError(response=response)
    else:
        response.raise_for_status.return_value = None
    return response


def test_search_by_guid_returns_id_when_found():
    """search_by_guid returns the record id from the first hit."""
    hit_id = "abc12-def34"
    payload = {"hits": {"total": 1, "hits": [{"id": hit_id}]}}
    with patch(
        "commonmeta.readers.inveniordm_reader.http.get",
        return_value=_mock_response(200, payload),
    ) as mock_get:
        result = search_by_guid(
            "https://ideophone.org/?p=5639", "rogue-scholar.org", "token"
        )

    assert result == hit_id
    # The query must phrase-quote the GUID so partial URLs don't match
    called_params = mock_get.call_args.kwargs["params"]
    assert (
        called_params["q"]
        == 'metadata.identifiers.identifier:"https://ideophone.org/?p=5639"'
    )


def test_search_by_guid_returns_none_when_not_found():
    """search_by_guid returns None when no record matches the GUID."""
    payload = {"hits": {"total": 0, "hits": []}}
    with patch(
        "commonmeta.readers.inveniordm_reader.http.get",
        return_value=_mock_response(200, payload),
    ):
        result = search_by_guid(
            "https://ideophone.org/?p=9999", "rogue-scholar.org", "token"
        )

    assert result is None


def test_search_by_guid_returns_none_on_rate_limit():
    """search_by_guid returns None when the API responds with 429."""
    with patch(
        "commonmeta.readers.inveniordm_reader.http.get",
        return_value=_mock_response(429, {}),
    ):
        result = search_by_guid(
            "https://ideophone.org/?p=5639", "rogue-scholar.org", "token"
        )

    assert result is None


def test_search_by_doi_returns_id_when_found():
    """search_by_doi returns the record id from the first hit."""
    hit_id = "xyz98-uvw76"
    payload = {"hits": {"total": 1, "hits": [{"id": hit_id}]}}
    with patch(
        "commonmeta.readers.inveniordm_reader.http.get",
        return_value=_mock_response(200, payload),
    ) as mock_get:
        result = search_by_doi("10.59350/dn2mm-m9q51", "rogue-scholar.org", "token")

    assert result == hit_id
    called_params = mock_get.call_args.kwargs["params"]
    assert called_params["q"] == "doi:10.59350/dn2mm-m9q51"


def test_search_by_doi_returns_none_when_not_found():
    """search_by_doi returns None when no record matches the DOI."""
    payload = {"hits": {"total": 0, "hits": []}}
    with patch(
        "commonmeta.readers.inveniordm_reader.http.get",
        return_value=_mock_response(200, payload),
    ):
        result = search_by_doi("10.59350/nonexistent", "rogue-scholar.org", "token")

    assert result is None


def _version_record(own_doi, parent_doi):
    """Minimal InvenioRDM version record dict for relation tests."""
    return {
        "id": "fktsh-g4g95",
        "pids": {"doi": {"identifier": own_doi, "provider": "crossref"}},
        "parent": {"id": "3jbwv-w1332", "pids": {"doi": {"identifier": parent_doi}}},
        "metadata": {
            "title": "Test",
            "publication_date": "2024-01-01",
            "resource_type": {"id": "blogpost"},
            "creators": [],
        },
    }


def test_version_relation_isversionof():
    """A version record links to its concept DOI via IsVersionOf."""
    record = _version_record("10.53731/kdqkf-nf052", "10.53731/3jbwv-w1332")
    subject = Metadata(record, via="inveniordm")
    assert {
        "id": "https://doi.org/10.53731/3jbwv-w1332",
        "type": "IsVersionOf",
    } in subject.relations


def test_parent_relation_hasversion():
    """The parent/concept deposit links to its version via HasVersion."""
    record = _version_record("10.53731/kdqkf-nf052", "10.53731/3jbwv-w1332")
    # The concept deposit passes the parent DOI as a kwarg (ChainObject path).
    subject = Metadata(record, via="inveniordm", parent_doi="10.53731/3jbwv-w1332")
    assert {
        "id": "https://doi.org/10.53731/kdqkf-nf052",
        "type": "HasVersion",
    } in subject.relations


def test_version_relation_no_self_reference():
    """No IsVersionOf when the parent DOI equals the record's own DOI."""
    record = _version_record("10.53731/kdqkf-nf052", "10.53731/kdqkf-nf052")
    subject = Metadata(record, via="inveniordm")
    assert all(r["type"] != "IsVersionOf" for r in (subject.relations or []))
