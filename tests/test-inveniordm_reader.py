# pylint: disable=invalid-name,too-many-lines
"""InvenioRDM reader tests"""
from os import path
import pytest

from commonmeta import Metadata
from commonmeta.readers.inveniordm_reader import (
    get_inveniordm,
    read_inveniordm,
)


@pytest.mark.vcr
def test_software():
    """Software"""
    string = path.join(path.dirname(__file__), "fixtures", "inveniordm-software.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.7752775"
    assert subject.type == "Software"
    assert subject.url == "https://zenodo.org/record/7752775"
    assert subject.titles[0] == {"title": "commonmeta-ruby"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "contributorRoles": ["Author"],
        "type": "Person",
        "id": "https://orcid.org/0000-0003-1419-2405",
        "affiliation": [{"name": "Front Matter"}],
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
    assert subject.related_identifiers == [
        {
            "id": "https://github.com/front-matter/commonmeta-ruby/tree/v3.0.1",
            "type": "IsSupplementTo",
        },
        {"id": "https://doi.org/10.5281/zenodo.5785518", "type": "IsVersionOf"},
    ]

    # assert subject.publisher == {
    #     "name": "Sauropod Vertebra Picture of the Week",
    # }
    # assert len(subject.references) == 3
    # assert subject.references[0] == {
    #     "key": "ref1",
    #     "url": "https://sauroposeidon.files.wordpress.com/2010/04/foster-and-wedel-2014-haplocanthosaurus-from-snowmass-colorado.pdf",
    # }

    # assert subject.funding_references == [
    #     {"funderName": "SystemsX"},
    #     {"funderName": "EMBO longterm post-doctoral fellowships"},
    #     {"funderName": "Marie Heim-Voegtlin"},
    #     {
    #         "funderName": "University of Lausanne",
    #         "funderIdentifier": "https://doi.org/10.13039/501100006390",
    #         "funderIdentifierType": "Crossref Funder ID",
    #     },
    #     {"funderName": "SystemsX"},
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100003043",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "EMBO",
    #     },
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100001711",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "Swiss National Science Foundation",
    #     },
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100006390",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "University of Lausanne",
    #     },
    # ]
    # assert subject.container == {
    #     "title": "Sauropod Vertebra Picture of the Week",
    #     "type": "Periodical",
    # }
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
    assert subject.type == "Speech"
    assert subject.url == "https://zenodo.org/record/8173303"
    assert subject.titles[0] == {
        "title": "11 July 2023 (Day 2) CERN – NASA Open Science Summit Sketch Notes"
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
        "updated": "2023-07-24T20:18:05Z",
    }
    assert subject.related_identifiers == [
        {"id": "https://doi.org/10.5281/zenodo.8173302", "type": "IsVersionOf"},
    ]

    # assert subject.publisher == {
    #     "name": "Sauropod Vertebra Picture of the Week",
    # }
    # assert len(subject.references) == 3
    # assert subject.references[0] == {
    #     "key": "ref1",
    #     "url": "https://sauroposeidon.files.wordpress.com/2010/04/foster-and-wedel-2014-haplocanthosaurus-from-snowmass-colorado.pdf",
    # }

    # assert subject.funding_references == [
    #     {"funderName": "SystemsX"},
    #     {"funderName": "EMBO longterm post-doctoral fellowships"},
    #     {"funderName": "Marie Heim-Voegtlin"},
    #     {
    #         "funderName": "University of Lausanne",
    #         "funderIdentifier": "https://doi.org/10.13039/501100006390",
    #         "funderIdentifierType": "Crossref Funder ID",
    #     },
    #     {"funderName": "SystemsX"},
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100003043",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "EMBO",
    #     },
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100001711",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "Swiss National Science Foundation",
    #     },
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100006390",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "University of Lausanne",
    #     },
    # ]
    # assert subject.container == {
    #     "title": "Sauropod Vertebra Picture of the Week",
    #     "type": "Periodical",
    # }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("CERN/NASA &ldquo;Accelerating the Adoption of Open Science&rdquo;")
    )
    assert subject.subjects is None
    assert subject.language is None
    assert subject.version is None
    assert subject.files == [
        {
            "bucket": "edf85f83-a9ec-4935-85ca-9da47a3815fd",
            "key": "20230711-CERN-NASA-Open-Science-Summit-Summary-Drawings.pdf",
            "checksum": "md5:45d8b11d4ef0da78b9db5397d8e0e8d9",
            "url": "https://zenodo.org/api/files/edf85f83-a9ec-4935-85ca-9da47a3815fd/20230711-CERN-NASA-Open-Science-Summit-Summary-Drawings.pdf",
            "size": 13994803,
            "mimeType": "application/pdf",
        }
    ]


@pytest.mark.vcr
def test_publication():
    """Publication"""
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "Article"
    assert subject.url == "https://zenodo.org/record/5244404"
    assert subject.titles[0] == {
        "title": "The Origins of SARS-CoV-2: A Critical Review"
    }
    assert len(subject.contributors) == 21
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Edward C",
        "familyName": "Holmes",
        "affiliation": [
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
        "updated": "2022-07-01T11:30:53Z",
    }
    assert subject.related_identifiers == [
        {"id": "https://doi.org/10.5281/zenodo.5075887", "type": "IsVersionOf"},
    ]

    # assert subject.publisher == {
    #     "name": "Sauropod Vertebra Picture of the Week",
    # }
    # assert len(subject.references) == 3
    # assert subject.references[0] == {
    #     "key": "ref1",
    #     "url": "https://sauroposeidon.files.wordpress.com/2010/04/foster-and-wedel-2014-haplocanthosaurus-from-snowmass-colorado.pdf",
    # }

    # assert subject.funding_references == [
    #     {"funderName": "SystemsX"},
    #     {"funderName": "EMBO longterm post-doctoral fellowships"},
    #     {"funderName": "Marie Heim-Voegtlin"},
    #     {
    #         "funderName": "University of Lausanne",
    #         "funderIdentifier": "https://doi.org/10.13039/501100006390",
    #         "funderIdentifierType": "Crossref Funder ID",
    #     },
    #     {"funderName": "SystemsX"},
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100003043",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "EMBO",
    #     },
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100001711",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "Swiss National Science Foundation",
    #     },
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100006390",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "University of Lausanne",
    #     },
    # ]
    # assert subject.container == {
    #     "title": "Sauropod Vertebra Picture of the Week",
    #     "type": "Periodical",
    # }
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
    assert subject.language is None
    assert subject.version == "Authors' final version"
    assert len(subject.files) == 3
    assert subject.files[0] == {
        "bucket": "449ea104-433b-4347-889b-a4535cd37e92",
        "key": "gisaid_acknowledgement_table.pdf",
        "checksum": "md5:b1b5979db4d4755601b85f160ce664b9",
        "url": "https://zenodo.org/api/files/449ea104-433b-4347-889b-a4535cd37e92/gisaid_acknowledgement_table.pdf",
        "size": 5335,
        "mimeType": "application/pdf",
    }


@pytest.mark.vcr
def test_dataset():
    """Dataset"""
    string = "https://zenodo.org/api/records/7834392"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.5281/zenodo.7834392"
    assert subject.type == "Dataset"
    assert subject.url == "https://zenodo.org/record/7834392"
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
        "affiliation": [{"name": "Georgia State University"}],
    }
    assert subject.license == {"id": "other-pd", "url": None}
    assert subject.date == {
        "published": "2023-04-16",
        "updated": "2023-04-17T14:26:45Z",
    }
    assert subject.related_identifiers == [
        {"id": "https://arxiv.org/abs/2004.03688", "type": "IsSupplementTo"},
        {"id": "https://doi.org/10.5281/zenodo.3723939", "type": "IsVersionOf"},
    ]

    # assert subject.publisher == {
    #     "name": "Sauropod Vertebra Picture of the Week",
    # }
    # assert len(subject.references) == 3
    # assert subject.references[0] == {
    #     "key": "ref1",
    #     "url": "https://sauroposeidon.files.wordpress.com/2010/04/foster-and-wedel-2014-haplocanthosaurus-from-snowmass-colorado.pdf",
    # }

    # assert subject.funding_references == [
    #     {"funderName": "SystemsX"},
    #     {"funderName": "EMBO longterm post-doctoral fellowships"},
    #     {"funderName": "Marie Heim-Voegtlin"},
    #     {
    #         "funderName": "University of Lausanne",
    #         "funderIdentifier": "https://doi.org/10.13039/501100006390",
    #         "funderIdentifierType": "Crossref Funder ID",
    #     },
    #     {"funderName": "SystemsX"},
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100003043",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "EMBO",
    #     },
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100001711",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "Swiss National Science Foundation",
    #     },
    #     {
    #         "funderIdentifier": "https://doi.org/10.13039/501100006390",
    #         "funderIdentifierType": "Crossref Funder ID",
    #         "funderName": "University of Lausanne",
    #     },
    # ]
    # assert subject.container == {
    #     "title": "Sauropod Vertebra Picture of the Week",
    #     "type": "Periodical",
    # }
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
    assert subject.language == "eng"
    assert subject.version == "162"
    assert len(subject.files) == 24
    assert subject.files[0] == {
        "bucket": "fafb41f4-4679-4ade-8ec6-1e48ecd43072",
        "key": "emojis.zip",
        "checksum": "md5:794aa07e49f5edf3ed72d552321bb2f5",
        "url": "https://zenodo.org/api/files/fafb41f4-4679-4ade-8ec6-1e48ecd43072/emojis.zip",
        "size": 15058751,
        "mimeType": "application/zip",
    }
