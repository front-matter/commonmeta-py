# pylint: disable=invalid-name
"""Test schema.org reader"""
import pytest
from commonmeta import Metadata
from commonmeta.readers.schema_org_reader import schema_org_geolocation


@pytest.mark.vcr
def test_blog_posting():
    "blog posting"
    string = "https://blog.front-matter.io/posts/eating-your-own-dog-food"
    subject = Metadata(string)
    if not subject.is_valid:
        print(subject.errors)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r79vxn1-97aq74v-ag58n"
    assert subject.type == "Article"
    assert subject.url == "https://blog.front-matter.io/posts/eating-your-own-dog-food"
    assert subject.titles[0] == {"title": "Eating your own Dog Food"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "familyName": "Fenner",
        "givenName": "Martin",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {
        "published": "2016-12-20",
        "updated": "2023-09-07T08:34:41Z",
    }
    assert subject.publisher == {"name": "Front Matter"}
    assert subject.references is None
    assert subject.container == {
        "identifier": "https://blog.front-matter.io/",
        "identifierType": "URL",
        "title": "Front Matter",
        "type": "Periodical",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Eating your own dog food is a slang term to describe")
    )
    assert subject.subjects == [{"subject": "feature"}]
    assert subject.language == "en"
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_zenodo():
    "zenodo"
    string = "https://www.zenodo.org/records/1196821"
    subject = Metadata(string)
    if not subject.is_valid:
        print(subject.errors)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.1196821"
    assert subject.type == "Other"
    assert subject.url == "https://zenodo.org/records/1196821"
    assert subject.titles[0] == {
        "title": (
            "PsPM-SC4B: SCR, ECG, EMG, PSR and respiration measurements in a "
            "delay fear conditioning task with auditory CS and electrical US"
        )
    }
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "type": "Person",
        "id": "https://orcid.org/0000-0001-9688-838X",
        "contributorRoles": ["Author"],
        "givenName": "Matthias",
        "familyName": "Staib",
    }
    assert subject.license == {
        "id": "CC-BY-SA-4.0",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/legalcode",
    }
    assert subject.date["published"] == "2018-03-14"
    assert subject.publisher == {"name": "Zenodo"}
    assert subject.references is None
    assert subject.container == {}
    assert subject.funding_references is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("This dataset includes pupil size response")
    )
    assert subject.subjects == [
        {"subject": "pupil size response"},
        {"subject": "skin conductance response"},
        {"subject": "electrocardiogram"},
        {"subject": "electromyogram"},
        {"subject": "electrodermal activity"},
        {"subject": "galvanic skin response"},
        {"subject": "psr"},
        {"subject": "scr"},
        {"subject": "ecg"},
        {"subject": "emg"},
        {"subject": "eda"},
        {"subject": "gsr"},
    ]
    assert subject.language == "eng"
    assert subject.version == "1.0.2"
    assert subject.provider == "DataCite"


def test_pangaea():
    "pangaea"
    string = "https://doi.pangaea.de/10.1594/PANGAEA.836178"
    subject = Metadata(string)
    if not subject.is_valid:
        print(subject.errors)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1594/pangaea.836178"
    assert subject.type == "Dataset"
    assert subject.url == "https://doi.pangaea.de/10.1594/PANGAEA.836178"
    assert subject.titles[0] == {
        "title": "Hydrological and meteorological investigations in a lake near Kangerlussuaq, west Greenland"
    }
    assert len(subject.contributors) == 8
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
    assert subject.date == {"published": "2014-09-25"}
    assert subject.publisher == {"name": "PANGAEA"}
    assert subject.references is None
    assert subject.container == {
        "identifier": "https://www.pangaea.de/",
        "identifierType": "URL",
        "title": "PANGAEA",
        "type": "DataRepository",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Few hydrological studies have been made in Greenland")
    )
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.version is None
    assert subject.geo_locations == [
        {"geoLocationPoint": {"pointLongitude": -50.18037, "pointLatitude": 67.12594}}
    ]
    assert subject.provider == "DataCite"


def test_dataverse():
    "dataverse"
    string = "https://doi.org/10.7910/dvn/nj7xso"
    subject = Metadata(string, via="schema_org")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7910/dvn/nj7xso"
    assert subject.type == "Dataset"
    assert (
        subject.url
        == "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NJ7XSO"
    )
    assert subject.titles[0] == {"title": "Summary data ankylosing spondylitis GWAS"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Organization",
        "contributorRoles": ["Author"],
        "name": "International Genetics of Ankylosing Spondylitis Consortium (IGAS)",
    }
    assert subject.license == {
        "id": "CC0-1.0",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
    }
    assert subject.date == {"published": "2017-09-30", "updated": "2017-09-30"}
    assert subject.publisher == {"name": "Harvard Dataverse"}
    assert subject.references is None
    assert subject.container == {
        "identifier": "https://dataverse.harvard.edu",
        "identifierType": "URL",
        "title": "Harvard Dataverse",
        "type": "DataRepository",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Summary of association tests for Nature Genetics publication")
    )
    assert subject.subjects == [
        {"subject": "Medicine, Health and Life Sciences"},
        {"subject": "Genome-Wide Association Studies"},
        {"subject": "Ankylosing spondylitis"},
    ]
    assert subject.language == "en"
    assert subject.version == "1"
    # assert subject.geo_locations is None
    assert subject.provider == "DataCite"


def test_yet_another_blog_post():
    "yet another blog post"
    string = "https://johnhawks.net/weblog/what-were-the-killing-methods-that-neandertals-used-for-large-prey-animals"
    subject = Metadata(string)
    assert subject.is_valid
    assert (
        subject.id
        == "https://johnhawks.net/weblog/what-were-the-killing-methods-that-neandertals-used-for-large-prey-animals"
    )
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://johnhawks.net/weblog/what-were-the-killing-methods-that-neandertals-used-for-large-prey-animals"
    )
    assert subject.titles[0] == {
        "title": "Neandertals hunted dangerous prey. How they killed them."
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "familyName": "Hawks",
        "givenName": "John",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license is None
    assert subject.date == {
        "published": "2022-09-24T17:22:00Z",
        "updated": "2023-10-23T03:26:56Z",
    }
    assert subject.publisher == {"name": "John Hawks"}
    assert subject.references is None
    assert subject.container == {
        "type": "Periodical",
        "title": "John Hawks",
        "identifier": "https://johnhawks.net/",
        "identifierType": "URL",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "With deep experience in the hunt, Neandertals could anticipate the behavior of many of the most dangerous prey animals."
        )
    )
    assert subject.subjects == [
        {"subject": "neandertals"},
        {"subject": "hunter-gatherers"},
        {"subject": "hunting"},
        {"subject": "taphonomy"},
        {"subject": "technology"},
        {"subject": "cooperation"},
        {"subject": "middle paleolithic"},
        {"subject": "diet"},
    ]
    assert subject.language == "en"
    assert subject.version is None
    assert subject.geo_locations is None
    assert subject.provider is None


def test_another_blog_with_dois():
    "another blog with dois"
    string = "https://x-dev.pages.jsc.fz-juelich.de/2022/10/05/doi-jekyll.html"
    subject = Metadata(string)
    assert subject.is_valid is False
    assert subject.errors == "{'type': 'Person', 'contributorRoles': ['Author'], 'givenName': 'Andreas'} is not valid under any of the given schemas"
    assert (
        subject.id
        == "https://x-dev.pages.jsc.fz-juelich.de//2022/10/05/doi-jekyll.html"
    )
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://x-dev.pages.jsc.fz-juelich.de//2022/10/05/doi-jekyll.html"
    )
    assert subject.titles[0] == {"title": "DOIng it Right! (DOIs for This Blog)"}
    assert len(subject.contributors) == 1
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
        "type": "Periodical",
    }
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
    assert subject.type == "Article"
    assert subject.url == "https://upstream.force11.org/welcome-to-upstream"
    assert subject.titles[0] == {
        "title": "Welcome to Upstream: the new space for scholarly community discussion on all things open"
    }
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "familyName": "Chodacki",
        "givenName": "John",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {
        "published": "2021-11-22T05:06:00Z",
        "updated": "2024-01-21T18:45:49Z",
    }
    assert subject.publisher == {"name": "Upstream"}
    assert subject.references is None
    assert subject.container == {
        "identifier": "https://upstream.force11.org/",
        "identifierType": "URL",
        "title": "Upstream",
        "type": "Periodical",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "Today we are announcing Upstream. And if you’re reading this, you’re already a part of it"
        )
    )
    assert subject.subjects == [{"subject": "news"}]
    assert subject.language == "en"
    assert subject.version is None
    assert subject.geo_locations is None
    assert subject.provider == "Crossref"


def test_with_blog_with_datacite_dois():
    "with blog with datacite dois"
    string = "https://blog.dini.de/EPub_FIS/2022/11/21/neue-standortbestimmung-fis-veroeffentlicht/"
    subject = Metadata(string)
    assert subject.is_valid
    assert (
        subject.id
        == "https://blog.dini.de/EPub_FIS/2022/11/21/neue-standortbestimmung-fis-veroeffentlicht"
    )
    assert subject.type == "Other"
    assert subject.url is None


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
    assert subject.id == "https://www.ideasurg.pub/why-surgery-needs-ideas"
    assert subject.type == "Article"
    assert subject.url == "https://www.ideasurg.pub/why-surgery-needs-ideas"
    assert subject.titles[0] == {"title": "Why Surgery Needs I.D.E.A.S."}
    assert len(subject.contributors) == 1
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
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("I am by no means an expert on the future of academic publishing.")
    )
    assert subject.subjects == [{"subject": "essay"}]
    assert subject.language == "en"
    assert subject.version is None
    assert subject.geo_locations is None
    assert subject.provider is None
