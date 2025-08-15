# pylint: disable=invalid-name,too-many-lines
"""Jsonfeed reader tests"""

import pytest

from commonmeta import Metadata
from commonmeta.readers.jsonfeed_reader import get_jsonfeed_uuid


def vcr_config():
    return {"record_mode": "new_episodes"}


@pytest.mark.vcr
def test_wordpress_with_references():
    "Wordpress with references"
    string = "https://api.rogue-scholar.org/posts/4e4bf150-751f-4245-b4ca-fe69e3c3bb24"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/hke8v-d1e66"
    assert subject.type == "BlogPost"
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
        "affiliations": [
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
        "name": "Front Matter",
    }
    assert len(subject.references) > 1
    assert subject.references[0] == {
        "unstructured": "Bilbey, S.A., Hall, J.E., and Hall, D.A. 2000. Preliminary results on a new haplocanthosaurid sauropod dinosaur from the lower Morrison Formation of northeastern Utah. Journal of Vertebrate Paleontology 20(supp. to no. 3): 30A.",
    }
    assert subject.relations == [
        {
            "id": "https://rogue-scholar.org/api/communities/svpow",
            "type": "IsPartOf",
        },
        {"id": "https://portal.issn.org/resource/ISSN/3033-3695", "type": "IsPartOf"},
    ]
    assert subject.identifiers == [
        {
            "identifier": "4e4bf150-751f-4245-b4ca-fe69e3c3bb24",
            "identifierType": "UUID",
        },
        {"identifier": "https://svpow.com/?p=20992", "identifierType": "GUID"},
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Sauropod Vertebra Picture of the Week",
        "identifier": "3033-3695",
        "identifierType": "ISSN",
        "platform": "WordPress.com",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "Brian Curtice and Colin Boisvert are presenting our talk on this project at 2:00 pm MDT this afternoon, at the 14th Symposium on Mesozoic Terrestrial Ecosystems and Biota (MTE14) in Salt Lake City, and the related paper is in the MTE14 volume in The Anatomical Record."
        )
    )
    assert len(subject.files) == 4
    assert subject.files[0] == {
        "mimeType": "text/markdown",
        "url": "https://api.rogue-scholar.org/posts/10.59350/hke8v-d1e66.md",
    }
    assert subject.subjects == [
        {"subject": "FOS: Earth and related environmental sciences"},
        {"subject": "MTE14"},
        {"subject": "Barosaurus"},
        {"subject": "Cervical"},
        {"subject": "Conferences"},
        {"subject": "Diplodocids"},
    ]
    assert subject.language == "en"
    assert subject.content.startswith(
        '\r\n<div data-shortcode="caption" id="attachment_21038"'
    )
    assert subject.image is None
    assert subject.version is None
    assert subject.state == "stale"


@pytest.mark.vcr
def test_post_with_relationships():
    "post with isIdenticalTo relationships"
    string = "https://api.rogue-scholar.org/posts/9e24e4be-1915-48cc-a6b0-c23da5bc2857"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/ewrv712-2k7rx6d"
    assert subject.type == "BlogPost"
    assert (
        subject.url == "https://blog.front-matter.io/posts/introducing-the-pid-graph/"
    )
    assert subject.titles[0] == {"title": "Introducing the PID Graph"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
        "affiliations": [{"id": "https://ror.org/04wxnsj81", "name": "DataCite"}],
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
    assert len(subject.references) == 5
    assert subject.references[0] == {
        "id": "https://doi.org/10.5438/s6d3-k860",
        "type": "Document",
        "unstructured": "Dasler, R., &amp; Cousijn, H. (2018). <i>Are your data being used? Event Data has the answer!</i> (1.0). DataCite. https://doi.org/10.5438/s6d3-k860",
    }
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://ror.org/00k4n6c32",
            "funderIdentifierType": "ROR",
            "awardUri": "https://doi.org/10.3030/777523",
            "awardNumber": "777523",
        }
    ]
    assert subject.relations == [
        {
            "id": "https://www.project-freya.eu/en/blogs/blogs/the-pid-graph",
            "type": "IsIdenticalTo",
        },
        {"id": "https://doi.org/10.5438/jwvf-8a66", "type": "IsIdenticalTo"},
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    assert subject.identifiers == [
        {
            "identifier": "9e24e4be-1915-48cc-a6b0-c23da5bc2857",
            "identifierType": "UUID",
        },
        {
            "identifier": "https://doi.org/10.53731/ewrv712-2k7rx6d",
            "identifierType": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Front Matter",
        "identifier": "2749-9952",
        "identifierType": "ISSN",
        "platform": "Ghost",
    }
    assert subject.content.startswith(
        "<p>Persistent identifiers (PIDs) are not only important"
    )
    assert (
        subject.image
        == "https://blog.front-matter.io/content/images/2022/08/pid_graph_image-1.webp"
    )
    assert subject.state == "stale"


@pytest.mark.vcr
def test_post_with_citations():
    "post with citations"
    string = "https://api.rogue-scholar.org/posts/6d0f1603-4081-4a4c-9bdf-1f0146558935"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/dcw3y-7em87"
    assert subject.type == "BlogPost"
    assert subject.url == "https://opencitations.hypotheses.org/31"
    assert subject.titles[0] == {"title": "Use of CiTO in CiteULike"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0001-5506-523X",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "David M.",
        "familyName": "Shotton",
        "affiliations": [
            {"id": "https://ror.org/052gg0110", "name": "University of Oxford"}
        ],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2010-10-21T16:32:43",
        "updated": "2022-08-04T15:52:06",
    }
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.references is None
    assert subject.citations == [
        {
            "id": "https://doi.org/10.1007/s11192-013-1108-3",
            "published_at": "2013-08-10",
            "unstructured": "Parinov, S., &amp; Kogalovsky, M. (2013). Semantic linkages in "
            "research information systems as a new data source for scientometric "
            "studies. <i>Scientometrics</i>, <i>98</i>(2), 927–943. "
            "https://doi.org/10.1007/s11192-013-1108-3",
            "updated_at": "2025-02-02T19:19:01.385995+00:00",
        },
        {
            "id": "https://doi.org/10.1134/s0361768814060139",
            "published_at": "2014-11",
            "unstructured": "Kogalovsky, M. R., &amp; Parinov, S. I. (2014). Social network "
            "technologies for semantic linking of information objects in "
            "scientific digital library. <i>Programming and Computer Software</i>, "
            "<i>40</i>(6), 314–322. https://doi.org/10.1134/s0361768814060139",
            "updated_at": "2025-02-02T19:18:41.652975+00:00",
        },
    ]
    assert subject.relations == [
        {
            "id": "https://rogue-scholar.org/api/communities/opencitations",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "6d0f1603-4081-4a4c-9bdf-1f0146558935",
            "identifierType": "UUID",
        },
        {
            "identifier": "http://opencitations.wordpress.com/?p=31",
            "identifierType": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "OpenCitations blog",
        "identifier": "https://rogue-scholar.org/blogs/opencitations",
        "identifierType": "URL",
        "platform": "WordPress",
    }
    assert subject.content.startswith(
        "<p>Egon Willighagen, at Uppsala University, has pioneered the use of object properties from CiTO"
    )
    assert subject.image is None


@pytest.mark.vcr
def test_another_post_with_citations():
    "another post with citations"
    string = "https://api.rogue-scholar.org/posts/7314152e-cac7-4bc1-ae99-b73ef67ea7db"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/50ebs-4zq55"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://depth-first.com/articles/2007/10/04/ruby-cdk-for-newbies"
    )
    assert subject.titles[0] == {"title": "Ruby CDK for Newbies"}
    assert subject.citations == [
        {
            "id": "https://doi.org/10.59350/myaw4-dtg76",
            "published_at": "2024-12-08",
            "unstructured": "Willighagen, E. (2024, December 8). Richard L. Apodaca. <i>Front "
            "Matter</i>. https://doi.org/10.59350/myaw4-dtg76",
            "updated_at": "2025-02-02T19:18:39.899725+00:00",
        },
    ]


@pytest.mark.vcr
def test_post_with_relationships_as_doi():
    "post with isIdenticalTo relationships"
    string = "https://api.rogue-scholar.org/posts/10.53731/ewrv712-2k7rx6d"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/ewrv712-2k7rx6d"
    assert subject.type == "BlogPost"
    assert (
        subject.url == "https://blog.front-matter.io/posts/introducing-the-pid-graph/"
    )
    assert subject.titles[0] == {"title": "Introducing the PID Graph"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
        "affiliations": [{"id": "https://ror.org/04wxnsj81", "name": "DataCite"}],
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
    assert len(subject.references) == 5
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://ror.org/00k4n6c32",
            "funderIdentifierType": "ROR",
            "awardUri": "https://doi.org/10.3030/777523",
            "awardNumber": "777523",
        }
    ]
    assert subject.relations == [
        {
            "id": "https://www.project-freya.eu/en/blogs/blogs/the-pid-graph",
            "type": "IsIdenticalTo",
        },
        {"id": "https://doi.org/10.5438/jwvf-8a66", "type": "IsIdenticalTo"},
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    assert subject.identifiers == [
        {
            "identifier": "9e24e4be-1915-48cc-a6b0-c23da5bc2857",
            "identifierType": "UUID",
        },
        {
            "identifier": "https://doi.org/10.53731/ewrv712-2k7rx6d",
            "identifierType": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Front Matter",
        "identifier": "2749-9952",
        "identifierType": "ISSN",
        "platform": "Ghost",
    }
    assert subject.provider == "Crossref"
    assert subject.state == "stale"


@pytest.mark.vcr
def test_post_with_funding():
    "post with funding"
    string = "https://api.rogue-scholar.org/posts/10.54900/vnevh-vaw22"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/vnevh-vaw22"
    assert subject.type == "BlogPost"
    assert subject.url == "https://upstream.force11.org/informate-where-are-the-data"
    assert subject.titles[0] == {"title": "INFORMATE: Where Are the Data?"}
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-3585-6733",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Ted",
        "familyName": "Habermann",
        "affiliations": [
            {"id": "https://ror.org/05bp8ka05", "name": "Metadata Game Changers"}
        ],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2023-12-05T10:00:43",
        "updated": "2025-01-24T18:28:43",
    }
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.references == [
        {
            "id": "https://doi.org/10.5281/zenodo.8284206",
            "type": "Document",
            "unstructured": "Plankytė, V., Macneil, R., &amp; Chen, X. (2023). <i>Guiding "
            "principles for implementing persistent identification and metadata "
            "features on research tools to boost interoperability of research data "
            "and support sample management workflows</i>. Zenodo. "
            "https://doi.org/10.5281/zenodo.8284206",
        }
    ]
    assert subject.relations == [
        {"id": "https://rogue-scholar.org/api/communities/upstream", "type": "IsPartOf"}
    ]
    assert subject.identifiers == [
        {
            "identifier": "5adbb6d4-1fe2-4da2-8cf4-c897f88a02d9",
            "identifierType": "UUID",
        },
        {
            "identifier": "https://doi.org/10.54900/vnevh-vaw22",
            "identifierType": "GUID",
        },
    ]
    assert subject.funding_references == [
        {
            "funderName": "National Science Foundation",
            "funderIdentifier": "https://ror.org/021nxhr62",
            "funderIdentifierType": "ROR",
            "awardUri": "https://www.nsf.gov/awardsearch/showaward?awd_id=2134956",
            "awardNumber": "2134956",
        }
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Upstream",
        "platform": "Ghost",
        "identifier": "https://rogue-scholar.org/blogs/upstream",
        "identifierType": "URL",
    }
    assert subject.content.startswith(
        '<h2 id="introduction">Introduction</h2><p>A recent'
    )
    assert (
        subject.image
        == "https://upstream.force11.org/content/images/2023/11/ashin-k-suresh-mkxTOAxqTTo-unsplash--3-.jpg"
    )
    assert subject.state == "stale"


@pytest.mark.vcr
def test_post_with_more_funding():
    "post with more funding"
    string = "https://api.rogue-scholar.org/posts/10.53731/r294649-6f79289-8cw1y"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r294649-6f79289-8cw1y"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://blog.front-matter.io/posts/new-datacite-orcid-integration-tool"
    )
    assert subject.references is None
    assert subject.relations == [
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    assert subject.identifiers == [
        {
            "identifier": "44690ae5-2ece-403d-8e34-a05668277a29",
            "identifierType": "UUID",
        },
        {
            "identifier": "https://doi.org/10.53731/r294649-6f79289-8cw1y",
            "identifierType": "GUID",
        },
    ]
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://ror.org/00k4n6c32",
            "funderIdentifierType": "ROR",
            "awardUri": "https://cordis.europa.eu/project/id/312788",
            "awardNumber": "312788",
        }
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Front Matter",
        "identifier": "2749-9952",
        "identifierType": "ISSN",
        "platform": "Ghost",
    }


@pytest.mark.vcr
def test_post_with_funding_ror():
    "post with funding ROR ID"
    string = "https://api.rogue-scholar.org/posts/10.59350/86jd5-wpv70"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/86jd5-wpv70"
    assert subject.type == "BlogPost"
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
        "affiliations": [
            {"id": "https://ror.org/05bp8ka05", "name": "Metadata Game Changers"}
        ],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {
        "published": "2022-03-08T00:39:39",
        "updated": "2024-04-28T18:31:57",
    }
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.references is None
    assert subject.relations == [
        {
            "id": "https://rogue-scholar.org/api/communities/metadatagamechangers",
            "type": "IsPartOf",
        }
    ]
    assert subject.identifiers == [
        {
            "identifier": "24251b1a-c09c-4341-a65c-30cf92a47d73",
            "identifierType": "UUID",
        },
        {"identifier": "62268c301674dc074d971710", "identifierType": "GUID"},
    ]
    assert subject.funding_references == [
        {
            "funderName": "U.S. National Science Foundation",
            "funderIdentifier": "https://ror.org/021nxhr62",
            "funderIdentifierType": "ROR",
            "awardUri": "https://www.nsf.gov/awardsearch/showaward?awd_id=2135874",
            "awardNumber": "2135874",
        }
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Blog - Metadata Game Changers",
        "identifier": "https://rogue-scholar.org/blogs/metadatagamechangers",
        "identifierType": "URL",
        "platform": "Squarespace",
    }
    assert subject.content.startswith(
        '<div id="item-62268c301674dc074d971710"\nclass="sqs-layout sqs-grid-12 columns-12"'
    )
    assert (
        subject.image
        == "https://images.squarespace-cdn.com/content/v1/52ffa419e4b05b374032e6d9/1646696325913-X5EGMEB3U4DHZBM0IQ1X/figure1.png"
    )


@pytest.mark.vcr
def test_post_with_even_more_funding():
    "post with even_more funding"
    string = "https://api.rogue-scholar.org/posts/6f2b7003-a77d-4b7b-a88a-8ce78546ddf7"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/s6am1-1sa79"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://chem-bla-ics.linkedchemistry.info/2013/11/08/looking-for-phd-and-postdoc-to-work-on.html"
    )
    assert subject.references is None
    assert subject.relations == [
        {
            "id": "https://rogue-scholar.org/api/communities/chem_bla_ics",
            "type": "IsPartOf",
        }
    ]
    assert subject.identifiers == [
        {
            "identifier": "6f2b7003-a77d-4b7b-a88a-8ce78546ddf7",
            "identifierType": "UUID",
        },
        {
            "identifier": "https://doi.org/10.59350/s6am1-1sa79",
            "identifierType": "GUID",
        },
    ]
    assert subject.funding_references == [
        {
            "funderName": "European Commission",
            "funderIdentifier": "https://ror.org/00k4n6c32",
            "funderIdentifierType": "ROR",
            "awardUri": "https://cordis.europa.eu/project/id/604134",
            "awardNumber": "604134",
            "awardTitle": "eNanoMapper - A Database and Ontology Framework for Nanomaterials Design and Safety Assessment",
        }
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "chem-bla-ics",
        "identifier": "https://rogue-scholar.org/blogs/chem_bla_ics",
        "identifierType": "URL",
        "platform": "Jekyll",
    }


@pytest.mark.vcr
def test_ghost_with_institutional_author():
    "ghost with institutional author"
    string = "https://api.rogue-scholar.org/posts/2b3cdd27-5123-4167-9482-3c074392e2d2"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/tfahc-rp566"
    assert subject.type == "BlogPost"
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
        "updated": "2023-01-24T12:11:47",
    }
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.references is None
    assert subject.relations == [
        {"id": "https://rogue-scholar.org/api/communities/oa_works", "type": "IsPartOf"}
    ]
    assert subject.identifiers == [
        {
            "identifier": "2b3cdd27-5123-4167-9482-3c074392e2d2",
            "identifierType": "UUID",
        },
        {"identifier": "63cef642602205003d6f50fb", "identifierType": "GUID"},
    ]
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
        "type": "Blog",
        "title": "OA.Works Blog",
        "identifier": "https://rogue-scholar.org/blogs/oa_works",
        "identifierType": "URL",
        "platform": "Ghost",
    }
    assert (
        subject.descriptions[0].get("description").startswith("After a couple of years")
    )
    assert len(subject.files) == 4
    assert subject.files[0] == {
        "mimeType": "text/markdown",
        "url": "https://api.rogue-scholar.org/posts/10.59350/tfahc-rp566.md",
    }
    assert subject.subjects == [
        {"subject": "FOS: Computer and information sciences"},
        {"subject": "OA.Report"},
    ]
    assert subject.language == "en"
    assert subject.content.startswith(
        '<p><img\nsrc="https://blog.oa.works/content/images/2023/01/nature-website-v2.png"'
    )
    assert (
        subject.image
        == "https://blog.oa.works/content/images/2023/01/nature-website-v2.png"
    )
    assert subject.version is None


@pytest.mark.vcr
def test_ghost_with_affiliations():
    "ghost with affiliations"
    string = "https://api.rogue-scholar.org/posts/fef48952-87bc-467b-8ebb-0bff92ab9e1a"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r294649-6f79289-8cw16"
    assert subject.type == "BlogPost"
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
        "affiliations": [
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
        "id": "https://doi.org/10.1371/journal.pone.0063184",
        "type": "JournalArticle",
        "unstructured": "Kafkas, Ş., Kim, J.-H., McEntyre, J. R., &amp; Larivière, V. (2013). Database Citation in Full Text Biomedical Articles. <i>PLoS ONE</i>, <i>8</i>(5), e63184. https://doi.org/10.1371/journal.pone.0063184",
    }
    assert subject.relations == [
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
    ]
    assert subject.identifiers == [
        {
            "identifier": "fef48952-87bc-467b-8ebb-0bff92ab9e1a",
            "identifierType": "UUID",
        },
        {
            "identifier": "https://doi.org/10.53731/r294649-6f79289-8cw16",
            "identifierType": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Front Matter",
        "identifier": "2749-9952",
        "identifierType": "ISSN",
        "platform": "Ghost",
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
    assert subject.subjects == [
        {"subject": "FOS: Computer and information sciences"},
        {"subject": "Feature"},
    ]
    assert subject.language == "en"
    assert subject.version is None


@pytest.mark.vcr
def test_ghost_with_personal_name_parsing():
    "ghost with with personal name parsing"
    string = "https://api.rogue-scholar.org/posts/4262e4b7-c2db-467b-b8b0-5b6ec32870a7"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/0vknr-rwv45"
    assert subject.type == "BlogPost"
    assert subject.url == "https://www.ideasurg.pub/surg-resident-voter-turnout"
    assert subject.titles[0] == {
        "title": "Voter Turnout Among General Surgery Residents in the 2022 U.S. Midterm Election"
    }
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
        "published": "2024-05-08T19:10:39",
        "updated": "2024-05-08T19:10:39",
    }
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert len(subject.references) == 5
    assert subject.references[0] == {
        "id": "https://doi.org/10.1001/jamanetworkopen.2021.42527",
        "type": "JournalArticle",
        "unstructured": "Ahmed, A., Chouairi, F., &amp; Li, X. (2022). Analysis of Reported Voting Behaviors of US Physicians, 2000-2020. <i>JAMA Network Open</i>, <i>5</i>(1), e2142527. https://doi.org/10.1001/jamanetworkopen.2021.42527",
    }
    assert subject.relations == [
        {
            "id": "https://rogue-scholar.org/api/communities/ideas",
            "type": "IsPartOf",
        },
        {"id": "https://portal.issn.org/resource/ISSN/2993-1150", "type": "IsPartOf"},
    ]
    assert subject.identifiers == [
        {
            "identifier": "4262e4b7-c2db-467b-b8b0-5b6ec32870a7",
            "identifierType": "UUID",
        },
        {
            "identifier": "66399ca46f25d60001df1427",
            "identifierType": "GUID",
        },
    ]
    assert subject.container == {
        "identifier": "2993-1150",
        "identifierType": "ISSN",
        "platform": "Ghost",
        "title": "I.D.E.A.S.",
        "type": "Blog",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("As residents within the healthcare profession,")
    )
    assert len(subject.files) == 4
    assert subject.files[0] == {
        "mimeType": "text/markdown",
        "url": "https://api.rogue-scholar.org/posts/10.59350/0vknr-rwv45.md",
    }
    assert subject.subjects == [
        {"subject": "FOS: Clinical medicine"},
        {"subject": "Preprint"},
    ]
    assert subject.language == "en"
    assert subject.content.startswith(
        "<p>As residents within the healthcare profession,"
    )
    assert (
        subject.image
        == "https://www.ideasurg.pub/content/images/2024/05/Overall-turnout.svg"
    )
    assert subject.version is None


@pytest.mark.vcr
def test_medium_post_with_multiple_authors():
    """blog post with multiple authors"""
    string = "https://api.rogue-scholar.org/posts/05f01f68-ef81-47d7-a3c1-40aba91d358f"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/jhrs4-22440"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://medium.com/@researchgraph/unveiling-the-synergy-retrieval-augmented-generation-rag-meets-knowledge-graphs-fc0a6900f7eb"
    )
    assert subject.titles[0] == {
        "title": "Unveiling the Synergy: Retrieval Augmented Generation (RAG) Meets Knowledge Graphs"
    }
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "affiliations": [
            {
                "id": "https://ror.org/031rekg67",
                "name": "Swinburne University of Technology",
            },
        ],
        "contributorRoles": ["Author"],
        "familyName": "Astudillo",
        "givenName": "Aland",
        "id": "https://orcid.org/0009-0008-8672-3168",
        "type": "Person",
    }
    assert subject.content.startswith(
        "<p><strong>Tools and Platform for Integration of Knowledge Graph"
    )
    assert (
        subject.image
        == "https://cdn-images-1.medium.com/max/1024/1*bJ3eWZ7301vYDzBomwdLfQ.png"
    )


@pytest.mark.vcr
def test_cczero_license():
    "cc zero license"
    string = "https://api.rogue-scholar.org/posts/10.59350/xgwqt-1sq35"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/xgwqt-1sq35"
    assert subject.type == "BlogPost"
    assert subject.titles[0] == {
        "title": "Epistemic diversity and knowledge production"
    }
    assert subject.license == {
        "id": "CC0-1.0",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
    }


@pytest.mark.vcr
def test_post_with_peer_reviewed_version():
    "post with peer-reviewed version"
    string = "https://api.rogue-scholar.org/posts/10.54900/zg929-e9595"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/zg929-e9595"
    assert subject.type == "BlogPost"
    assert subject.titles[0] == {"title": "Large Language Publishing"}
    assert subject.relations == [
        {
            "id": "https://doi.org/10.18357/kula.291",
            "type": "IsPreprintOf",
        },
        {
            "id": "https://rogue-scholar.org/api/communities/upstream",
            "type": "IsPartOf",
        },
    ]
    assert subject.content.startswith(
        "<p><em>The New York Times</em> ushered in the New Year"
    )
    assert (
        subject.image
        == "https://upstream.force11.org/content/images/2023/12/pexels-viktor-talashuk-2377295.jpg"
    )


@pytest.mark.vcr
def test_post_with_peer_review():
    "post with peer-review"
    string = "https://api.rogue-scholar.org/posts/10.54900/r8zwg-62003"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/r8zwg-62003"
    assert subject.type == "BlogPost"
    assert subject.titles[0] == {
        "title": "Drinking from the Firehose? Write More and Publish Less"
    }
    assert subject.relations == [
        {
            "id": "https://metaror.org/kotahi/articles/40",
            "type": "HasReview",
        },
        {
            "id": "https://rogue-scholar.org/api/communities/upstream",
            "type": "IsPartOf",
        },
    ]
    assert subject.content.startswith(
        '<figure class="kg-card kg-image-card kg-card-hascaption">'
    )
    assert subject.image is None


@pytest.mark.vcr
def test_funded_project():
    "funded project"
    string = "https://api.rogue-scholar.org/posts/10.59350/p000s-pth40"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/p000s-pth40"
    assert subject.type == "BlogPost"
    assert subject.titles[0] == {"title": "THOR’s last hurrah"}
    assert subject.funding_references == [
        {
            "awardNumber": "654039",
            "awardTitle": "THOR – Technical and Human Infrastructure for Open Research",
            "awardUri": "https://doi.org/10.3030/654039",
            "funderIdentifier": "https://ror.org/019w4f821",
            "funderName": "European Union",
        },
    ]


@pytest.mark.vcr
def test_broken_reference():
    "JSON Feed broken reference"
    string = "https://api.rogue-scholar.org/posts/340de361-9628-481e-9204-527c679446b9"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/z78kb-qrz59"
    assert subject.type == "BlogPost"
    assert len(subject.references) == 6
    assert subject.references[3] == {
        "id": "https://doi.org/10.1016/s2214-109x(23)00198-5",
        "type": "JournalArticle",
        "unstructured": "Laurenson-Schafer, H., Sklenovská, N., Hoxha, A., Kerr, S. M., Ndumbi, P., Fitzner, J., Almiron, M., de Sousa, L. A., Briand, S., Cenciarelli, O., Colombe, S., Doherty, M., Fall, I. S., García-Calavaro, C., Haussig, J. M., Kato, M., Mahamud, A. R., Morgan, O. W., Nabeth, P., … Biaukula, V. (2023). Description of the first global outbreak of mpox: an analysis of global surveillance data. <i>The Lancet Global Health</i>, <i>11</i>(7), e1012–e1023. https://doi.org/10.1016/s2214-109x(23)00198-5",
    }


def test_get_jsonfeed():
    """Test get_jsonfeed"""
    item = get_jsonfeed_uuid("1357c246-b632-462a-9876-753ef8b6927d")
    assert item["guid"] == "http://gigasciencejournal.com/blog/?p=5621"


def test_get_jsonfeed_item_not_found():
    """Test get_json_feed_item_id not found"""
    assert {"error": "An error occured."} == get_jsonfeed_uuid("notfound")
