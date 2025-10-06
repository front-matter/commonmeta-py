# pylint: disable=invalid-name
"""Test schema.org reader"""

import pytest

from commonmeta import Metadata
from commonmeta.readers.schema_org_reader import schema_org_geolocation


def vcr_config():
    return {"record_mode": "new_episodes"}


@pytest.mark.vcr
def test_blog_posting():
    "blog posting"
    string = "https://blog.front-matter.io/posts/eating-your-own-dog-food"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r79vxn1-97aq74v-ag58n"
    assert subject.type == "BlogPost"
    assert subject.url == "https://blog.front-matter.io/posts/eating-your-own-dog-food/"
    assert subject.titles and subject.titles[0] == {"title": "Eating your own Dog Food"}
    assert subject.contributors and len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {
        "published": "2016-12-20",
    }
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.references == [
        {
            "id": "https://doi.org/10.5438/0012",
            "key": "ref1",
            "unstructured": "DataCite Metadata Working Group, Starr, J., Smaele, M. de ., Ashton, J., Barton, A., Bradford, T., Ciolek-Figiel, A., Dietiker, S., Elliot, J., Genat, B., Harzenetter, K., Hirschmann, B., Jakobsson, S., Mailloux, J.-Y., Newbold, E., Nielsen, L. H., Yahia, M., &amp; Ziedorn, F. (2016). <i>DataCite Metadata Schema Documentation for the Publication and Citation of Research Data v4.0</i>. DataCite e.V.",
        },
        {
            "id": "https://doi.org/10.5438/55e5-t5c0",
            "key": "ref2",
            "unstructured": "Fenner, M. (2016, December 15). <i>Cool DOI's</i>.",
        },
    ]
    assert subject.container == {
        "type": "Periodical",
        "title": "Front Matter",
    }
    assert subject.descriptions and (
        subject.descriptions[0]
        .get("description")
        .startswith("Eating your own dog food is a slang term to describe")
    )
    assert subject.subjects is None
    assert subject.language is None
    assert subject.version == "v1"
    assert subject.provider == "Crossref"


@pytest.mark.vcr
def test_zenodo():
    "zenodo"
    string = "https://www.zenodo.org/records/1196821"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.1196821"
    assert subject.type == "Dataset"
    assert subject.url == "https://zenodo.org/record/1196821"
    assert subject.titles and subject.titles[0] == {
        "title": "Pspm-Sc4B: Scr, Ecg, Emg, Psr And Respiration Measurements In A Delay Fear Conditioning Task With Auditory Cs And Electrical Us"
    }
    assert subject.contributors and len(subject.contributors) == 6
    assert subject.contributors[0] == {
        "type": "Person",
        "id": "https://orcid.org/0000-0001-9688-838X",
        "contributorRoles": ["Author"],
        "givenName": "Matthias",
        "familyName": "Staib",
        "affiliations": [{"name": "University of Zurich, Zurich, Switzerland"}],
    }
    assert subject.license == {
        "id": "CC-BY-SA-4.0",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/legalcode",
    }
    assert subject.date and subject.date["published"] == "2018-03-14"
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.references is None
    assert subject.container is None
    assert subject.funding_references is None
    assert subject.descriptions and (
        subject.descriptions[0]
        .get("description")
        .startswith("This dataset includes pupil size response")
    )
    assert subject.subjects == [
        {"subject": "Pupil Size Response"},
        {"subject": "Skin Conductance Response"},
        {"subject": "Electrocardiogram"},
        {"subject": "Electromyogram"},
        {"subject": "Electrodermal Activity"},
        {"subject": "Galvanic Skin Response"},
        {"subject": "PSR"},
        {"subject": "SCR"},
        {"subject": "ECG"},
        {"subject": "EMG"},
        {"subject": "EDA"},
        {"subject": "GSR"},
    ]
    assert subject.language == "en"
    assert subject.version is None
    assert subject.provider == "DataCite"


@pytest.mark.vcr
def test_pangaea():
    "pangaea"
    string = "https://doi.pangaea.de/10.1594/PANGAEA.836178"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1594/pangaea.836178"
    assert subject.type == "Dataset"
    assert subject.url == "https://doi.pangaea.de/10.1594/PANGAEA.836178"
    assert subject.titles and subject.titles[0] == {
        "title": "Hydrological and meteorological investigations in a lake near Kangerlussuaq, west Greenland"
    }
    assert subject.contributors and len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "familyName": "Johansson",
        "givenName": "Emma",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }
    assert subject.date == {"published": "2014"}
    assert subject.publisher == {"name": "PANGAEA"}
    assert subject.references is None
    assert subject.container is None
    assert subject.descriptions and subject.descriptions[0].get(
        "description"
    ).startswith("Few hydrological studies have been made in Greenland")
    assert subject.subjects == [
        {
            "subject": "GReenland Analogue Surface Project (GRASP)",
        }
    ]
    assert subject.language == "en"
    assert subject.version is None
    assert subject.geo_locations == [
        {"geoLocationPoint": {"pointLongitude": -50.18037, "pointLatitude": 67.12594}},
        {"geoLocationPlace": "Two Boat Lake, Kangerlussuaq, Greenland"},
    ]
    assert subject.provider == "DataCite"


@pytest.mark.vcr
def test_dataverse():
    "dataverse"
    string = "https://doi.org/10.7910/dvn/nj7xso"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7910/dvn/nj7xso"
    assert subject.type == "Dataset"
    assert (
        subject.url
        == "https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/NJ7XSO"
    )
    assert subject.titles and subject.titles[0] == {
        "title": "Summary data ankylosing spondylitis GWAS"
    }
    assert subject.contributors and len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "type": "Organization",
        "contributorRoles": ["Author"],
        "name": "International Genetics Of Ankylosing Spondylitis Consortium (IGAS)",
    }
    assert subject.license is None
    assert subject.date == {
        "available": "2017-09-30",
        "submitted": "2017-09-30",
        "updated": "2017-10-01",
        "published": "2017",
    }
    assert subject.publisher == {"name": "Harvard Dataverse"}
    assert subject.references is None
    assert subject.container is None
    assert subject.descriptions and subject.descriptions[0].get(
        "description"
    ).startswith("Summary of association tests for Nature Genetics")
    assert subject.subjects == [
        {"subject": "Medicine, Health and Life Sciences"},
        {"subject": "Genome-Wide Association Studies"},
        {"subject": "Ankylosing spondylitis"},
    ]
    assert subject.language is None
    assert subject.version == "1.0"
    assert subject.geo_locations is None
    assert subject.provider == "DataCite"


def test_yet_another_blog_post():
    "yet another blog post"
    string = "https://www.johnhawks.net/p/what-were-the-killing-methods-that-neandertals-used-for-large-prey-animals"
    subject = Metadata(string)
    assert subject.is_valid
    assert (
        subject.id
        == "https://www.johnhawks.net/p/what-were-the-killing-methods-that-neandertals-used-for-large-prey-animals"
    )
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://www.johnhawks.net/p/what-were-the-killing-methods-that-neandertals-used-for-large-prey-animals"
    )
    assert subject.titles and subject.titles[0] == {
        "title": "Neandertals hunted dangerous prey. How they killed them."
    }
    assert subject.contributors and len(subject.contributors) == 1
    assert subject.contributors and subject.contributors[0] == {
        "familyName": "Hawks",
        "givenName": "John",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license is None
    assert subject.date == {
        "published": "2022-09-24T17:22:00Z",
        "updated": "2022-09-24T17:22:00Z",
    }
    assert subject.publisher == {
        "name": "John Hawks",
        "description": "Our origins shape our future",
        "identifier": "pub:56991",
        "image": {
            "@type": "ImageObject",
            "contentUrl": "https://substackcdn.com/image/fetch/$s_!GBU1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69c9cf32-de17-42d0-bd89-0b3dab9864b4_256x256.png",
            "thumbnailUrl": "https://substackcdn.com/image/fetch/$s_!GBU1!,w_128,h_128,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69c9cf32-de17-42d0-bd89-0b3dab9864b4_256x256.png",
            "url": "https://substackcdn.com/image/fetch/$s_!GBU1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69c9cf32-de17-42d0-bd89-0b3dab9864b4_256x256.png",
        },
    }
    assert subject.references is None
    assert subject.container == {
        "type": "Periodical",
        "identifier": "https://www.johnhawks.net",
        "identifierType": "URL",
    }
    assert subject.descriptions and (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "With deep experience in the hunt, Neandertals could anticipate the behavior of many of the most dangerous prey animals."
        )
    )
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.version is None
    assert subject.geo_locations is None
    assert subject.provider is None


def test_another_blog_with_dois():
    "another blog with dois"
    string = "https://x-dev.pages.jsc.fz-juelich.de/2022/10/05/doi-jekyll.html"
    subject = Metadata(string)
    assert subject.is_valid
    assert (
        subject.id
        == "https://x-dev.pages.jsc.fz-juelich.de//2022/10/05/doi-jekyll.html"
    )
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://x-dev.pages.jsc.fz-juelich.de//2022/10/05/doi-jekyll.html"
    )
    assert subject.titles and subject.titles[0] == {
        "title": "DOIng it Right! (DOIs for This Blog)"
    }
    assert subject.contributors and len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Andreas",
    }
    assert subject.license is None
    assert subject.date == {
        "published": "2022-10-05T14:35:47Z",
        "updated": "2022-10-05T14:35:47Z",
    }
    assert subject.publisher == {"name": "JSC Accelerating Devices Lab"}
    assert subject.references is None
    assert subject.container == {
        "title": "JSC Accelerating Devices Lab",
        "type": "Blog",
    }
    assert subject.descriptions is not None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("1This blog is an experiment.")
    )
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.version is None
    assert subject.geo_locations is None
    assert subject.provider is None


def test_with_upstream_blog_post():
    "with upstream blog post"
    string = "https://upstream.force11.org/welcome-to-upstream/"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/rckn8ey-1fm76va-qsrnf"
    assert subject.type == "BlogPost"
    assert subject.url == "https://upstream.force11.org/welcome-to-upstream/"
    assert subject.titles and subject.titles[0] == {
        "title": "Welcome to Upstream: the new space for scholarly community discussion on all things open"
    }
    assert subject.contributors and len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-7378-2408",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "John",
        "familyName": "Chodacki",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {
        "published": "2021-11-22",
    }
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.references is None
    assert subject.container == {
        "type": "Periodical",
        "title": "Upstream",
    }
    assert subject.descriptions and subject.descriptions[0].get(
        "description"
    ).startswith(
        "Today we are announcing Upstream. And if you're reading this, you're already a part of it!"
    )
    assert subject.subjects is None
    assert subject.language is None
    assert subject.version == "v1"
    assert subject.geo_locations is None
    assert subject.provider == "Crossref"


def test_with_blog_with_datacite_dois():
    "with blog with datacite dois"
    string = "https://blog.dini.de/EPub_FIS/2022/11/21/neue-standortbestimmung-fis-veroeffentlicht/"
    subject = Metadata(string)
    assert subject.is_valid
    assert (
        subject.id
        == "https://blog.dini.de/EPub_FIS/2022/11/21/neue-standortbestimmung-fis-veroeffentlicht/"
    )
    assert subject.type == "WebPage"
    assert (
        subject.url
        == "https://blog.dini.de/EPub_FIS/2022/11/21/neue-standortbestimmung-fis-veroeffentlicht/"
    )


def test_schema_org_geolocation():
    "schema_org geolocations"
    spatial_coverage = {
        "@type": "Place",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 67.12594,
            "longitude": -50.18037,
        },
    }
    none_coverage = {"spatialCoverage": None}
    assert {
        "geoLocationPoint": {"pointLatitude": 67.12594, "pointLongitude": -50.18037}
    } == schema_org_geolocation(spatial_coverage)
    assert None is schema_org_geolocation(none_coverage)


def test_yet_another_ghost_post():
    """yet another ghost post"""
    string = "https://www.ideasurg.pub/why-surgery-needs-ideas/"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://www.ideasurg.pub/why-surgery-needs-ideas/"
    assert subject.type == "Article"
    assert subject.url == "https://www.ideasurg.pub/why-surgery-needs-ideas/"
    assert subject.titles and subject.titles[0] == {
        "title": "Why Surgery Needs I.D.E.A.S."
    }
    assert subject.contributors and len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "familyName": "Sathe",
        "givenName": "Tejas S.",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license is None
    assert subject.date == {
        "published": "2022-12-19T05:42:45Z",
        "updated": "2023-07-25T18:02:32Z",
    }
    assert subject.publisher == {"name": "I.D.E.A.S."}
    assert subject.references is None
    assert subject.container == {
        "type": "Periodical",
        "title": "I.D.E.A.S.",
        "identifier": "https://www.ideasurg.pub/",
        "identifierType": "URL",
    }
    assert subject.descriptions and subject.descriptions[0].get(
        "description"
    ).startswith("I am by no means an expert on the future of academic publishing.")
    assert subject.subjects == [{"subject": "essay"}]
    assert subject.language == "en"
    assert subject.version is None
    assert subject.geo_locations is None
    assert subject.provider is None


@pytest.mark.vcr
def test_arxiv():
    "arxiv"
    string = "https://arxiv.org/abs/1902.02534"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.48550/arxiv.1902.02534"
    assert subject.type == "Article"
    assert subject.url == "https://arxiv.org/abs/1902.02534"
    assert subject.titles and subject.titles[0] == {
        "title": "Crowdsourcing open citations with CROCI -- An analysis of the current status of open citations, and a proposal"
    }
    assert subject.contributors and len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Ivan",
        "familyName": "Heibi",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {
        "submitted": "2019-06-21T06:21:52Z",
        "published": "2019",
        "available": "2019-02",
        "updated": "2019-06-24T00:08:45Z",
    }
    assert subject.publisher == {"name": "arXiv"}
    assert subject.references is None
    assert subject.container is None
    assert subject.descriptions and subject.descriptions[0].get(
        "description"
    ).startswith(
        "In this paper, we analyse the current availability of open citations data in one particular dataset"
    )
    assert subject.subjects == [
        {
            "language": "en",
            "subject": "Digital Libraries (cs.DL)",
        },
        {
            "subject": "FOS: Computer and information sciences",
        },
    ]
    assert subject.language is None
    assert subject.version == "2"
    assert subject.identifiers == [
        {"identifier": "1902.02534", "identifierType": "Other"},
        {
            "identifier": "https://doi.org/10.48550/arxiv.1902.02534",
            "identifierType": "DOI",
        },
    ]
    assert subject.provider == "DataCite"


@pytest.mark.vcr
def test_orcid_blog():
    "orcid blog"
    string = "https://info.orcid.org/orcid-2023-annual-report/"
    subject = Metadata(string)
    assert subject.is_valid is False
    assert subject.id == "https://info.orcid.org/orcid-2023-annual-report/"
    assert subject.type == "WebPage"
    assert subject.state == "forbidden"


@pytest.mark.vcr
def test_journal_page():
    "journal page"
    string = "https://app.pan.pl/article/item/app011052023.html"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.4202/app.01105.2023"
    assert subject.type == "JournalArticle"
    assert subject.titles == [
        {"title": "Novel pneumatic features in the ribs of Brachiosaurus altithorax"}
    ]
    assert subject.date == {"published": "2023"}
    assert subject.publisher == {
        "name": "Polska Akademia Nauk Instytut Paleobiologii (Institute of Paleobiology, Polish Academy of Sciences)"
    }
    assert subject.references is None
    assert subject.container == {
        "identifier": "0567-7920",
        "identifierType": "ISSN",
        "title": "Acta Palaeontologica Polonica",
        "type": "Journal",
        "volume": "68",
    }
    assert subject.provider == "Crossref"


@pytest.mark.vcr
def test_pdf_file():
    "PDF file"
    string = "https://www.vosviewer.com/documentation/manual_vosviewer_1.6.8.pdf"
    subject = Metadata(string)
    assert subject.is_valid is False
    assert (
        subject.id
        == "https://www.vosviewer.com/documentation/manual_vosviewer_1.6.8.pdf"
    )
    assert subject.type == "WebPage"
    assert subject.state == "bad_request"
    assert subject.titles is None
    assert subject.date is None


@pytest.mark.vcr
def test_youtube():
    "YouTube"
    string = "https://www.youtube.com/watch?v=4JsNT1gKe7I"
    subject = Metadata(string)
    # assert subject.is_valid
    assert subject.id == "https://www.youtube.com/watch?v=4JsNT1gKe7I"
    assert subject.type == "Audiovisual"
    assert subject.state == "findable"
    assert subject.titles == [
        {
            "title": "Elsevier's David Tempest explains subscription-contract confidentiality clauses"
        }
    ]
    assert subject.date and subject.date["accessed"] is not None
