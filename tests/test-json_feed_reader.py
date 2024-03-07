# pylint: disable=invalid-name,too-many-lines
"""JSON Feed reader tests"""

import pytest

from commonmeta import Metadata
from commonmeta.readers.json_feed_reader import (
    get_json_feed_item_uuid,
)


@pytest.mark.vcr
def test_wordpress_with_references():
    "Wordpress with references"
    string = "https://api.rogue-scholar.org/posts/4e4bf150-751f-4245-b4ca-fe69e3c3bb24"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/hke8v-d1e66"
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://svpow.com/2023/06/09/new-paper-curtice-et-al-2023-on-the-first-haplocanthosaurus-from-dry-mesa"
    )
    assert subject.titles[0] == {
        "title": "New paper: Curtice et al. (2023) on the first <i>Haplocanthosaurus</i> from Dry Mesa"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0001-6082-3103",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Matt",
        "familyName": "Wedel",
        "affiliation": [
            {
                "id": "https://ror.org/05167c961",
                "name": "Western University of Health Sciences",
            }
        ],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2023-06-09T21:54:23",
        "updated": "2023-06-09T21:54:23",
    }
    assert subject.publisher == {
        "name": "Sauropod Vertebra Picture of the Week",
    }
    assert len(subject.references) > 1
    assert subject.references[0] == {
        "key": "ref1",
        "url": "https://sauroposeidon.files.wordpress.com/2010/04/foster-and-wedel-2014-haplocanthosaurus-from-snowmass-colorado.pdf",
    }
    assert subject.relations is None

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
    assert subject.container == {
        "type": "Periodical",
        "title": "Sauropod Vertebra Picture of the Week",
        "identifier": "https://rogue-scholar.org/blogs/svpow",
        "identifierType": "URL",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("<em> Haplocanthosaurus </em> tibiae and dorsal vertebrae.")
    )
    assert len(subject.files) == 4
    assert subject.files[0] == {
        "mimeType": "text/markdown",
        "url": "https://api.rogue-scholar.org/posts/10.59350/hke8v-d1e66.md",
    }
    assert subject.subjects == [{"subject": "Earth and related environmental sciences"}]
    assert subject.language == "en"
    assert subject.version is None


@pytest.mark.vcr
def test_post_with_relationships():
    "post with isIdenticalTo relationships"
    string = "https://api.rogue-scholar.org/posts/9e24e4be-1915-48cc-a6b0-c23da5bc2857"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/ewrv712-2k7rx6d"
    assert subject.type == "Article"
    assert subject.url == "https://blog.front-matter.io/posts/introducing-the-pid-graph"
    assert subject.titles[0] == {"title": "Introducing the PID Graph"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
        "affiliation": [{"id": "https://ror.org/04wxnsj81", "name": "DataCite"}],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2019-03-28T01:00:00",
        "updated": "2023-09-07T13:48:44",
    }
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert len(subject.references) == 0
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://doi.org/10.13039/501100000780",
            "funderIdentifierType": "Crossref Funder ID",
            "award_uri": "https://doi.org/10.3030/777523",
            "awardNumber": "777523",
        }
    ]
    assert subject.relations == [
        {
            "id": "https://www.project-freya.eu/en/blogs/blogs/the-pid-graph",
            "type": "IsIdenticalTo",
        },
        {"id": "https://doi.org/10.5438/jwvf-8a66", "type": "IsIdenticalTo"},
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    assert subject.container == {
        "type": "Periodical",
        "title": "Front Matter",
        "identifier": "2749-9952",
        "identifierType": "ISSN",
    }


@pytest.mark.vcr
def test_post_with_funding():
    "post with funding"
    string = "https://api.rogue-scholar.org/posts/5adbb6d4-1fe2-4da2-8cf4-c897f88a02d9"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/vnevh-vaw22"
    assert subject.type == "Article"
    assert subject.url == "https://upstream.force11.org/informate-where-are-the-data"
    assert subject.titles[0] == {"title": "INFORMATE: Where Are the Data?"}
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-3585-6733",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Ted",
        "familyName": "Habermann",
        "affiliation": [
            {"id": "https://ror.org/05bp8ka05", "name": "Metadata Game Changers"}
        ],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2023-12-05T10:00:43",
        "updated": "2023-12-07T19:29:37",
    }
    assert subject.publisher == {
        "name": "Upstream",
    }
    assert len(subject.references) == 0
    assert subject.relations is None
    assert subject.funding_references == [
        {
            "funderName": "National Science Foundation",
            "funderIdentifier": "https://doi.org/10.13039/100000001",
            "funderIdentifierType": "Crossref Funder ID",
            "award_uri": "https://www.nsf.gov/awardsearch/showaward?awd_id=2134956",
            "awardNumber": "2134956",
        }
    ]
    assert subject.container == {
        "type": "Periodical",
        "title": "Upstream",
        "identifier": "https://rogue-scholar.org/blogs/upstream",
        "identifierType": "URL",
    }


@pytest.mark.vcr
def test_post_with_more_funding():
    "post with more funding"
    string = "https://api.rogue-scholar.org/posts/44690ae5-2ece-403d-8e34-a05668277a29"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r294649-6f79289-8cw1y"
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://blog.front-matter.io/posts/new-datacite-orcid-integration-tool"
    )
    assert len(subject.references) == 0
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"}
    ]
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://doi.org/10.13039/501100000780",
            "funderIdentifierType": "Crossref Funder ID",
            "award_uri": "https://cordis.europa.eu/project/id/312788",
            "awardNumber": "312788",
        }
    ]
    assert subject.container == {
        "type": "Periodical",
        "title": "Front Matter",
        "identifier": "2749-9952",
        "identifierType": "ISSN",
    }


@pytest.mark.vcr
def test_post_with_funding_ror():
    "post with funding ROR ID"
    string = "https://api.rogue-scholar.org/posts/24251b1a-c09c-4341-a65c-30cf92a47d73"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/86jd5-wpv70"
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://metadatagamechangers.com/blog/2022/3/7/ivfrlw6naf7am3bvord8pldtuyqn4r"
    )
    assert subject.titles[0] == {
        "title": "Metadata Life Cycle: Mountain or Superhighway?"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-3585-6733",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Ted",
        "familyName": "Habermann",
        "affiliation": [
            {"id": "https://ror.org/05bp8ka05", "name": "Metadata Game Changers"}
        ],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2022-03-08T00:39:39",
        "updated": "2022-04-14T20:16:52",
    }
    assert subject.publisher == {
        "name": "Blog - Metadata Game Changers",
    }
    assert len(subject.references) == 0
    assert subject.relations is None
    assert subject.funding_references == [
        {
            "funderName": "National Science Foundation",
            "funderIdentifier": "https://ror.org/021nxhr62",
            "funderIdentifierType": "ROR",
            "award_uri": "https://www.nsf.gov/awardsearch/showaward?awd_id=2135874",
            "awardNumber": "2135874",
        }
    ]
    assert subject.container == {
        "type": "Periodical",
        "title": "Blog - Metadata Game Changers",
        "identifier": "https://rogue-scholar.org/blogs/metadatagamechangers",
        "identifierType": "URL",
    }


@pytest.mark.vcr
def test_ghost_with_institutional_author():
    "ghost with institutional author"
    string = "https://api.rogue-scholar.org/posts/2b3cdd27-5123-4167-9482-3c074392e2d2"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/tfahc-rp566"
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://blog.oa.works/nature-features-oa-reports-work-putting-oa-policy-into-practice"
    )
    assert subject.titles[0] == {
        "title": "Nature features OA.Report's work putting OA policy into practice!"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "contributorRoles": ["Author"],
        "type": "Organization",
        "name": "OA.Works",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2023-01-24T12:11:47",
        "updated": "2023-10-01T17:34:13",
    }
    assert subject.publisher == {
        "name": "OA.Works Blog",
    }
    assert len(subject.references) == 0
    assert subject.relations is None
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
    assert subject.container == {
        "type": "Periodical",
        "title": "OA.Works Blog",
        "identifier": "https://rogue-scholar.org/blogs/oa_works",
        "identifierType": "URL",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "After a couple of years of working to support institutions implementing their OA policies"
        )
    )
    assert len(subject.files) == 4
    assert subject.files[0] == {
        "mimeType": "text/markdown",
        "url": "https://api.rogue-scholar.org/posts/10.59350/tfahc-rp566.md",
    }
    assert subject.subjects == [{"subject": "Computer and information sciences"}]
    assert subject.language == "en"
    assert subject.version is None


@pytest.mark.vcr
def test_ghost_with_affiliations():
    "ghost with affiliations"
    string = "https://api.rogue-scholar.org/posts/fef48952-87bc-467b-8ebb-0bff92ab9e1a"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r294649-6f79289-8cw16"
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://blog.front-matter.io/posts/auto-generating-links-to-data-and-resources"
    )
    assert subject.titles[0] == {"title": "Auto generating links to data and resources"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
        "affiliation": [
            {"id": "https://ror.org/008zgvp64", "name": "Public Library of Science"}
        ],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2013-07-02T18:58:00",
        "updated": "2022-08-15T16:14:53",
    }
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert len(subject.references) == 1
    assert subject.references[0] == {
        "doi": "https://doi.org/10.1371/journal.pone.0063184",
        "title": "Database Citation in Full Text Biomedical Articles",
        "publicationYear": "2013",
        "key": "ref1",
    }
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"}
    ]
    assert subject.container == {
        "type": "Periodical",
        "title": "Front Matter",
        "identifier": "2749-9952",
        "identifierType": "ISSN",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("A few weeks ago Kafkas et al. (2013) published a paper")
    )
    assert len(subject.files) == 4
    assert subject.files[0] == {
        "mimeType": "text/markdown",
        "url": "https://api.rogue-scholar.org/posts/10.53731/r294649-6f79289-8cw16.md",
    }
    assert subject.subjects == [{"subject": "Computer and information sciences"}]
    assert subject.language == "en"
    assert subject.version is None


@pytest.mark.vcr
def test_ghost_with_personal_name_parsing():
    "ghost with with personal name parsing"
    string = "https://api.rogue-scholar.org/posts/c3095752-2af0-40a4-a229-3ceb7424bce2"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/kj95y-gp867"
    assert subject.type == "Article"
    assert subject.url == "https://www.ideasurg.pub/residency-visual-abstract"
    assert subject.titles[0] == {"title": "The Residency Visual Abstract"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-0449-4469",
        "contributorRoles": ["Author"],
        "type": "Person",
        "familyName": "Sathe",
        "givenName": "Tejas S.",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2023-04-08T21:32:34",
        "updated": "2023-04-08T21:32:34",
    }
    assert subject.publisher == {
        "name": "I.D.E.A.S.",
    }
    assert len(subject.references) == 0
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2993-1150", "type": "IsPartOf"}
    ]
    assert subject.container == {
        "identifier": "2993-1150",
        "identifierType": "ISSN",
        "title": "I.D.E.A.S.",
        "type": "Periodical",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("My prototype for a Residency Visual Abstract")
    )
    assert len(subject.files) == 4
    assert subject.files[0] == {
        "mimeType": "text/markdown",
        "url": "https://api.rogue-scholar.org/posts/10.59350/kj95y-gp867.md",
    }
    assert subject.subjects == [{"subject": "Clinical medicine"}]
    assert subject.language == "en"
    assert subject.version is None


@pytest.mark.vcr
def test_medium_post_with_institutional_author():
    """blog post with institutional author"""
    string = "https://api.rogue-scholar.org/posts/05f01f68-ef81-47d7-a3c1-40aba91d358f"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/jhrs4-22440"
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://medium.com/@researchgraph/unveiling-the-synergy-retrieval-augmented-generation-rag-meets-knowledge-graphs-fc0a6900f7eb"
    )
    assert subject.titles[0] == {
        "title": "Unveiling the Synergy: Retrieval Augmented Generation (RAG) Meets Knowledge Graphs"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Organization",
        "contributorRoles": ["Author"],
        "name": "Research Graph",
    }


def test_get_json_feed_item():
    """Test get_json_feed_item_id"""
    item = get_json_feed_item_uuid("1357c246-b632-462a-9876-753ef8b6927d")
    assert item["guid"] == "http://gigasciencejournal.com/blog/?p=5621"


def test_get_json_feed_item_not_found():
    """Test get_json_feed_item_id not found"""
    assert {"error": "An error occured."} == get_json_feed_item_uuid("notfound")
