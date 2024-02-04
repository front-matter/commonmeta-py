# pylint: disable=invalid-name,too-many-lines
"""JSON Feed reader tests"""
import pytest

from commonmeta import Metadata
from commonmeta.readers.json_feed_reader import (
    get_json_feed_item_uuid,
    get_json_feed_unregistered,
    get_json_feed_updated,
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
        "contributorRoles": ["Author"],
        "type": "Person",
        "familyName": "Wedel",
        "givenName": "Matt",
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
        "title": "Sauropod Vertebra Picture of the Week",
        "type": "Periodical",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "Brian Curtice and Colin Boisvert are presenting our talk on this project at 2:00 pm MDT this afternoon,"
        )
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
        "title": "OA.Works Blog",
        "type": "Periodical",
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
def test_blog_post_without_doi():
    "blog post without DOI"
    string = "https://api.rogue-scholar.org/posts/e2ecec16-405d-42da-8b4d-c746840398fa"
    subject = Metadata(string)
    assert subject.is_valid
    assert (
        subject.id
        == "https://www.leidenmadtrics.nl/articles/an-open-approach-for-classifying-research-publications"
    )
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://www.leidenmadtrics.nl/articles/an-open-approach-for-classifying-research-publications"
    )
    assert subject.titles[0] == {
        "title": "An open approach for classifying research publications"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://ror.org/027bh9e22",
        "type": "Organization",
        "contributorRoles": ["Author"],
        "name": "Leiden Madtrics",
    }


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
    assert {"error":"An error occured."} == get_json_feed_item_uuid("notfound")
