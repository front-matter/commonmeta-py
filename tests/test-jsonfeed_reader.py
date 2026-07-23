# pylint: disable=invalid-name,too-many-lines
"""Jsonfeed reader tests"""

import pytest

from commonmeta import Metadata
from commonmeta.readers.jsonfeed_reader import get_jsonfeed_doi


def vcr_config():
    return {"record_mode": "new_episodes"}


@pytest.mark.vcr
def test_wordpress_with_references():
    "Wordpress with references"
    string = "https://api.rogue-scholar.org/posts/10.59350/hke8v-d1e66"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/hke8v-d1e66"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://svpow.com/2023/06/09/new-paper-curtice-et-al-2023-on-the-first-haplocanthosaurus-from-dry-mesa/"
    )
    assert (
        subject.title
        == "New paper: Curtice et al. (2023) on the first <i>Haplocanthosaurus</i> from Dry Mesa"
    )
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-6082-3103",
            "given_name": "Matt",
            "family_name": "Wedel",
            "affiliations": [
                {
                    "identifier": "https://ror.org/05167c961",
                    "identifier_type": "ROR",
                    "name": "Western University of Health Sciences",
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2023-06-09T00:00:00Z"
        and subject.date_updated == "2026-07-20T06:59:13Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert len(subject.references) > 1
    assert subject.references[0] == {
        "unstructured": "Bilbey, S.A., Hall, J.E., and Hall, D.A. 2000. Preliminary results on a new haplocanthosaurid sauropod dinosaur from the lower Morrison Formation of northeastern Utah. Journal of Vertebrate Paleontology 20(supp. to no. 3): 30A.",
    }
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/3033-3695", "type": "IsPartOf"},
        {"id": "https://rogue-scholar.org/api/communities/svpow", "type": "IsPartOf"},
    ]
    assert subject.identifiers == [
        {"identifier": "https://svpow.com/?p=20992", "identifier_type": "GUID"},
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Sauropod Vertebra Picture of the Week",
        "identifiers": [{"identifier": "3033-3695", "identifier_type": "ISSN"}],
        "platform": "WordPress.com",
    }
    assert subject.description.startswith(
        "<em> Haplocanthosaurus </em> tibiae and dorsal vertebrae"
    )
    assert len(subject.files) == 8
    assert subject.files[0] == {
        "url": "https://svpow.wordpress.com/wp-content/uploads/2023/06/haplocanthosaurus-from-across-the-morrison-curtice-et-al-2023-fig-1.jpg?w=480",
    }
    assert subject.subjects == [
        {"id": "https://openalex.org/subfields/1911", "subject": "Paleontology"},
        {"subject": "MTE14"},
        {"subject": "Barosaurus"},
        {"subject": "Cervical"},
        {"subject": "Conferences"},
        {"subject": "Diplodocids"},
    ]
    assert subject.language == "en"
    assert subject.content.startswith(
        '<div data-shortcode="caption" id="attachment_21038"'
    )
    assert (
        subject.image
        == "https://svpow.wordpress.com/wp-content/uploads/2023/06/haplocanthosaurus-from-across-the-morrison-curtice-et-al-2023-fig-1.jpg?w=480"
    )
    assert subject.version == "v1"
    assert subject.state == "stale"


@pytest.mark.vcr
def test_post_with_relationships():
    "post with isIdenticalTo relationships"
    string = "https://api.rogue-scholar.org/posts/10.53731/ewrv712-2k7rx6d"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/ewrv712-2k7rx6d"
    assert subject.type == "BlogPost"
    assert (
        subject.url == "https://blog.front-matter.de/posts/introducing-the-pid-graph/"
    )
    assert subject.title == "Introducing the PID Graph"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "given_name": "Martin",
            "family_name": "Fenner",
            "affiliations": [
                {
                    "identifier": "https://ror.org/04wxnsj81",
                    "identifier_type": "ROR",
                    "name": "DataCite",
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2019-03-28T00:00:00Z"
        and subject.date_updated == "2026-07-19T17:31:26Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert len(subject.references) == 5
    assert subject.references[0] == {
        "id": "https://doi.org/10.5438/s6d3-k860",
        "unstructured": "Dasler, R.&amp; Cousijn, H. (2018, October 8). Are your data being used? Event Data has the answer!. <i>DataCite Blog</i>.",
    }
    assert subject.funding_references == [
        {
            "funder_id": "https://ror.org/00k4n6c32",
            "funder_name": "European Commission",
            "award_id": "https://doi.org/10.3030/777523",
            "award_number": "777523",
        }
    ]
    assert subject.relations == [
        {
            "id": "https://www.project-freya.eu/en/blogs/blogs/the-pid-graph",
            "type": "IsIdenticalTo",
        },
        {"id": "https://doi.org/10.5438/jwvf-8a66", "type": "IsIdenticalTo"},
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.53731/ewrv712-2k7rx6d",
            "identifier_type": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Front Matter",
        "identifiers": [{"identifier": "2749-9952", "identifier_type": "ISSN"}],
        "platform": "Ghost",
    }
    assert subject.content.startswith(
        "<p>Persistent identifiers (PIDs) are not only important"
    )
    assert (
        subject.image
        == "https://storage.ghost.io/c/c5/33/c533c955-b5f3-4ff1-ae2d-6b52a212e602/content/images/2022/08/pid_graph_image-1.webp"
    )
    assert subject.state == "stale"


@pytest.mark.vcr
def test_post_with_citations():
    "post with citations"
    string = "https://api.rogue-scholar.org/posts/10.59350/dcw3y-7em87"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/dcw3y-7em87"
    assert subject.type == "BlogPost"
    assert subject.url == "https://opencitations.hypotheses.org/31"
    assert subject.title == "Use of CiTO in CiteULike"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-5506-523X",
            "given_name": "David M.",
            "family_name": "Shotton",
            "affiliations": [
                {
                    "identifier": "https://ror.org/052gg0110",
                    "identifier_type": "ROR",
                    "name": "University of Oxford",
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2010-10-21T00:00:00Z"
        and subject.date_updated == "2025-10-24T06:45:16Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.references is None
    # assert subject.citations == [
    #     {
    #         "id": "https://doi.org/10.1007/s11192-013-1108-3",
    #         "published_at": "2013-08-10",
    #         "unstructured": "Parinov, S., &amp; Kogalovsky, M. (2013). Semantic linkages in "
    #         "research information systems as a new data source for scientometric "
    #         "studies. <i>Scientometrics</i>, <i>98</i>(2), 927–943. "
    #         "https://doi.org/10.1007/s11192-013-1108-3",
    #         "updated_at": "2026-05-31T05:56:35.963391+00:00",
    #     },
    #     {
    #         "id": "https://doi.org/10.1134/s0361768814060139",
    #         "published_at": "2014-11",
    #         "unstructured": "Kogalovsky, M. R., &amp; Parinov, S. I. (2014). Social network "
    #         "technologies for semantic linking of information objects in "
    #         "scientific digital library. <i>Programming and Computer Software</i>, "
    #         "<i>40</i>(6), 314–322. https://doi.org/10.1134/s0361768814060139",
    #         "updated_at": "2026-05-31T05:56:31.713165+00:00",
    #     },
    # ]
    assert subject.relations == [
        {"id": "https://doi.org/10.59350/opencitations", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/opencitations",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "http://opencitations.wordpress.com/?p=31",
            "identifier_type": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "OpenCitations blog",
        "identifiers": [
            {
                "identifier": "https://doi.org/10.59350/opencitations",
                "identifier_type": "DOI",
            }
        ],
        "platform": "WordPress",
    }
    assert subject.content.startswith(
        "<p>Egon Willighagen, at Uppsala University, has pioneered the use of object properties from CiTO"
    )
    assert subject.image is None


@pytest.mark.vcr
def test_another_post_with_citations():
    "another post with citations"
    string = "https://api.rogue-scholar.org/posts/10.59350/50ebs-4zq55"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/50ebs-4zq55"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://depth-first.com/articles/2007/10/04/ruby-cdk-for-newbies"
    )
    assert subject.title == "Ruby CDK for Newbies"
    # assert subject.citations == [
    #     {
    #         "id": "https://doi.org/10.59350/myaw4-dtg76",
    #         "published_at": "2024-12-08",
    #         "unstructured": "Willighagen, E. (2024, December 8). Richard L. Apodaca. "
    #         "<i>Chem-bla-ics</i>. https://doi.org/10.59350/myaw4-dtg76",
    #         "updated_at": "2026-05-31T05:56:31.642085+00:00",
    #     },
    #     {
    #         "id": "https://doi.org/10.59350/mn0n8-p9m65",
    #         "published_at": "2024-12-08",
    #         "unstructured": "Willighagen, E. (2024, December 8). Richard L. Apodaca. "
    #         "<i>Chem-bla-ics</i>. https://doi.org/10.59350/mn0n8-p9m65",
    #         "updated_at": "2026-05-31T05:56:35.667294+00:00",
    #     },
    # ]


@pytest.mark.vcr
def test_post_with_relationships_as_doi():
    "post with isIdenticalTo relationships"
    string = "https://api.rogue-scholar.org/posts/10.53731/ewrv712-2k7rx6d"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/ewrv712-2k7rx6d"
    assert subject.type == "BlogPost"
    assert (
        subject.url == "https://blog.front-matter.de/posts/introducing-the-pid-graph/"
    )
    assert subject.title == "Introducing the PID Graph"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "given_name": "Martin",
            "family_name": "Fenner",
            "affiliations": [
                {
                    "identifier": "https://ror.org/04wxnsj81",
                    "identifier_type": "ROR",
                    "name": "DataCite",
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2019-03-28T00:00:00Z"
        and subject.date_updated == "2026-07-19T17:31:26Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert len(subject.references) == 5
    assert subject.funding_references == [
        {
            "funder_id": "https://ror.org/00k4n6c32",
            "funder_name": "European Commission",
            "award_id": "https://doi.org/10.3030/777523",
            "award_number": "777523",
        }
    ]
    assert subject.relations == [
        {
            "id": "https://www.project-freya.eu/en/blogs/blogs/the-pid-graph",
            "type": "IsIdenticalTo",
        },
        {"id": "https://doi.org/10.5438/jwvf-8a66", "type": "IsIdenticalTo"},
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.53731/ewrv712-2k7rx6d",
            "identifier_type": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Front Matter",
        "identifiers": [{"identifier": "2749-9952", "identifier_type": "ISSN"}],
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
    assert subject.url == "https://upstream.force11.org/informate-where-are-the-data/"
    assert subject.title == "INFORMATE: Where Are the Data?"
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-3585-6733",
            "given_name": "Ted",
            "family_name": "Habermann",
            "affiliations": [
                {
                    "identifier": "https://ror.org/05bp8ka05",
                    "identifier_type": "ROR",
                    "name": "Metadata Game Changers",
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2023-12-05T00:00:00Z"
        and subject.date_updated == "2026-07-19T19:04:37Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.references == [
        {
            "id": "https://doi.org/10.5281/zenodo.8284206",
            "unstructured": "Plankytė, V., Macneil, R., & Chen, X. (2023). Guiding "
            "principles for implementing persistent identification and metadata "
            "features on research tools to boost interoperability of research data "
            "and support sample management workflows. "
            "https://doi.org/10.5281/ZENODO.8284206",
        }
    ]
    assert subject.relations == [
        {"id": "https://doi.org/10.54900/upstream", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/upstream",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.54900/vnevh-vaw22",
            "identifier_type": "GUID",
        },
    ]
    assert subject.funding_references == [
        {
            "funder_id": "https://ror.org/021nxhr62",
            "funder_name": "National Science Foundation",
            "award_id": "https://www.nsf.gov/awardsearch/showaward?awd_id=2134956",
            "award_number": "2134956",
        }
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Upstream",
        "platform": "Ghost",
        "identifiers": [
            {
                "identifier": "https://doi.org/10.54900/upstream",
                "identifier_type": "DOI",
            }
        ],
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
        == "https://blog.front-matter.de/posts/new-datacite-orcid-integration-tool/"
    )
    assert subject.references is None
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.53731/r294649-6f79289-8cw1y",
            "identifier_type": "GUID",
        },
    ]
    assert subject.funding_references == [
        {
            "funder_id": "https://ror.org/00k4n6c32",
            "funder_name": "European Commission",
            "award_id": "https://cordis.europa.eu/project/id/312788",
            "award_number": "312788",
        }
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Front Matter",
        "identifiers": [{"identifier": "2749-9952", "identifier_type": "ISSN"}],
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
    assert subject.title == "Metadata Life Cycle: Mountain or Superhighway?"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-3585-6733",
            "given_name": "Ted",
            "family_name": "Habermann",
            "affiliations": [
                {
                    "identifier": "https://ror.org/05bp8ka05",
                    "identifier_type": "ROR",
                    "name": "Metadata Game Changers",
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2022-03-08T00:00:00Z"
        and subject.date_updated == "2025-12-06T10:57:05Z"
    )
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
        {"identifier": "62268c301674dc074d971710", "identifier_type": "GUID"},
    ]
    assert subject.funding_references == [
        {
            "funder_id": "https://ror.org/021nxhr62",
            "funder_name": "National Science Foundation",
            "award_id": "https://www.nsf.gov/awardsearch/showaward?awd_id=2135874",
            "award_number": "2135874",
        }
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Blog - Metadata Game Changers",
        "identifiers": [
            {
                "identifier": "https://rogue-scholar.org/blogs/metadatagamechangers",
                "identifier_type": "URL",
            }
        ],
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
    string = "https://api.rogue-scholar.org/posts/10.59350/s6am1-1sa79"
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
        {"id": "https://doi.org/10.59350/chem_bla_ics", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/chem_bla_ics",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.59350/s6am1-1sa79",
            "identifier_type": "GUID",
        },
    ]
    assert subject.funding_references == [
        {
            "funder_id": "https://ror.org/00k4n6c32",
            "funder_name": "European Commission",
            "award_id": "https://cordis.europa.eu/project/id/604134",
            "award_title": "eNanoMapper - A Database and Ontology Framework for Nanomaterials Design and Safety Assessment",
            "award_number": "604134",
        }
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "chem-bla-ics",
        "identifiers": [
            {
                "identifier": "https://doi.org/10.59350/chem_bla_ics",
                "identifier_type": "DOI",
            }
        ],
        "platform": "Jekyll",
    }


@pytest.mark.vcr
def test_ghost_with_institutional_author():
    "ghost with institutional author"
    string = "https://api.rogue-scholar.org/posts/10.59350/tfahc-rp566"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/tfahc-rp566"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://blog.oa.works/nature-features-oa-reports-work-putting-oa-policy-into-practice"
    )
    assert (
        subject.title
        == "Nature features OA.Report's work putting OA policy into practice!"
    )
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Organization",
        "organization": {"name": "OA.Works"},
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert (
        subject.date_published == "2023-01-24T00:00:00Z"
        and subject.date_updated == "2025-04-13T23:21:55Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.references is None
    assert subject.relations == [
        {"id": "https://doi.org/10.59350/oa_works", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/oa_works",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {"identifier": "63cef642602205003d6f50fb", "identifier_type": "GUID"},
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
        "identifiers": [
            {
                "identifier": "https://doi.org/10.59350/oa_works",
                "identifier_type": "DOI",
            }
        ],
        "platform": "Ghost",
    }
    assert subject.description.startswith("After a couple of years")
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "https://blog.oa.works/content/images/2023/01/nature-website-v2.png",
    }
    assert subject.subjects == [
        {
            "id": "https://openalex.org/subfields/1802",
            "subject": "Information Systems and Management",
        },
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
    assert subject.version == "v1"


@pytest.mark.vcr
def test_ghost_with_affiliations():
    "ghost with affiliations"
    string = "https://api.rogue-scholar.org/posts/10.53731/r294649-6f79289-8cw16"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/r294649-6f79289-8cw16"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://blog.front-matter.de/posts/auto-generating-links-to-data-and-resources/"
    )
    assert subject.title == "Auto generating links to data and resources"
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "given_name": "Martin",
            "family_name": "Fenner",
            "affiliations": [
                {
                    "identifier": "https://ror.org/008zgvp64",
                    "identifier_type": "ROR",
                    "name": "Public Library of Science",
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2013-07-02T00:00:00Z"
        and subject.date_updated == "2026-07-19T18:14:27Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert len(subject.references) == 1
    assert subject.references[0] == {
        "id": "https://doi.org/10.1371/journal.pone.0063184",
        "unstructured": "Kafkas, Ş., Kim, J.-H., McEntyre, J. R.&amp; Larivière, V. (2013). Database Citation in Full Text Biomedical Articles. <i>PLoS ONE</i>, <i>8</i>(5), e63184.",
    }
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/front_matter",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.53731/r294649-6f79289-8cw16",
            "identifier_type": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "Front Matter",
        "identifiers": [{"identifier": "2749-9952", "identifier_type": "ISSN"}],
        "platform": "Ghost",
    }
    assert subject.description.startswith(
        "A few weeks ago Kafkas et al. (2013) published a paper"
    )
    assert len(subject.files) == 1
    assert subject.files[0] == {
        "url": "https://storage.ghost.io/c/c5/33/c533c955-b5f3-4ff1-ae2d-6b52a212e602/content/images/2022/08/journal.pone.0063184.g003.png",
    }
    assert subject.subjects == [
        {"id": "https://openalex.org/subfields/1710", "subject": "Information Systems"},
        {"subject": "Feature"},
    ]
    assert subject.language == "en"
    assert subject.version == "v1"


@pytest.mark.vcr
def test_ghost_with_personal_name_parsing():
    "ghost with with personal name parsing"
    string = "https://api.rogue-scholar.org/posts/10.59350/0vknr-rwv45"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/0vknr-rwv45"
    assert subject.type == "BlogPost"
    assert subject.url == "https://www.ideasurg.pub/surg-resident-voter-turnout/"
    assert (
        subject.title
        == "Voter Turnout Among General Surgery Residents in the 2022 U.S. Midterm Election"
    )
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-0449-4469",
            "given_name": "Tejas S.",
            "family_name": "Sathe",
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2024-05-08T00:00:00Z"
        and subject.date_updated == "2025-08-02T20:32:30Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert len(subject.references) == 5
    assert subject.references[0] == {
        "id": "https://doi.org/10.1001/jamanetworkopen.2021.42527",
        "unstructured": "Ahmed, A., Chouairi, F., &amp; Li, X. (2022). Analysis of Reported Voting Behaviors of US Physicians, 2000-2020. <i>JAMA Network Open</i>, <i>5</i>(1), e2142527.",
    }
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2993-1150", "type": "IsPartOf"},
        {"id": "https://rogue-scholar.org/api/communities/ideas", "type": "IsPartOf"},
    ]
    assert subject.identifiers == [
        {
            "identifier": "66399ca46f25d60001df1427",
            "identifier_type": "GUID",
        },
    ]
    assert subject.container == {
        "identifiers": [{"identifier": "2993-1150", "identifier_type": "ISSN"}],
        "platform": "Ghost",
        "title": "I.D.E.A.S.",
        "type": "Blog",
    }
    assert subject.description.startswith(
        "As residents within the healthcare profession,"
    )
    assert len(subject.files) == 1
    assert subject.files[0] == {
        "url": "https://www.ideasurg.pub/content/images/2024/05/Overall-turnout.svg",
    }
    assert subject.subjects == [
        {"id": "https://openalex.org/subfields/2746", "subject": "Surgery"},
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
    assert subject.version == "v1"


@pytest.mark.vcr
def test_cczero_license():
    "cc zero license"
    string = "https://api.rogue-scholar.org/posts/10.59350/xgwqt-1sq35"
    subject = Metadata(string)
    print(vars(subject))
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/xgwqt-1sq35"
    assert subject.type == "BlogPost"
    assert subject.title == "Epistemic diversity and knowledge production"
    assert subject.license == {
        "id": "CC0-1.0",
        "title": "Creative Commons Zero v1.0 Universal",
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
    assert subject.title == "Large Language Publishing"
    assert subject.relations == [
        {"id": "https://doi.org/10.18357/kula.291", "type": "IsPreviousVersionOf"},
        {"id": "https://doi.org/10.54900/upstream", "type": "IsPartOf"},
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
    assert subject.title == "Drinking from the Firehose? Write More and Publish Less"
    assert subject.relations == [
        {"id": "https://doi.org/10.54900/upstream", "type": "IsPartOf"},
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
def test_post_with_contributor_roles():
    "post with contributor roles"
    string = "https://api.rogue-scholar.org/posts/10.59350/510pg-zzf58"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/510pg-zzf58"
    assert subject.type == "BlogPost"
    assert subject.url == "https://ropensci.org/blog/2025/10/14/blog-roles/"
    assert subject.title == "Recognition Beyond Blog Post Authors"
    assert len(subject.contributors) == 2
    assert subject.contributors[1] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-4522-7466",
            "given_name": "Yanina",
            "family_name": "Bellini Saibene",
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert (
        subject.date_published == "2025-10-14T00:00:00Z"
        and subject.date_updated == "2026-06-09T15:55:20Z"
    )
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.references is None
    assert subject.relations == [
        {"id": "https://doi.org/10.59350/ropensci", "type": "IsPartOf"},
        {
            "id": "https://rogue-scholar.org/api/communities/ropensci",
            "type": "IsPartOf",
        },
    ]
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.59350/510pg-zzf58",
            "identifier_type": "GUID",
        },
    ]
    assert subject.container == {
        "type": "Blog",
        "title": "rOpenSci - open tools for open science",
        "identifiers": [
            {
                "identifier": "https://doi.org/10.59350/ropensci",
                "identifier_type": "DOI",
            }
        ],
        "platform": "Other",
    }
    assert subject.content.startswith("<p>Our own dev guide")
    assert subject.image is None


@pytest.mark.vcr
def test_post_subfield_classification():
    "post subfield classification"
    string = "https://api.rogue-scholar.org/posts/10.59350/qsajq-6tn97"
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
        {"id": "https://openalex.org/subfields/1911", "subject": "Paleontology"},
        {"subject": "Conferences"},
        {"subject": "Debate"},
        {"subject": "Open Access"},
        {"subject": "SSP"},
        {"subject": "Stinkin' Publishers"},
    ]


@pytest.mark.vcr
def test_post_topic_classification():
    "post topic classification"
    string = "https://api.rogue-scholar.org/posts/10.59350/rjt2m-2hy19"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/rjt2m-2hy19"
    assert subject.type == "BlogPost"
    assert (
        subject.url
        == "https://danielskatzblog.wordpress.com/2024/08/20/supporting-core-research-softtware-work/"
    )
    assert subject.title == "Supporting the core work in research software"
    assert subject.description.startswith("(Please cite this post as")
    assert subject.subjects == [
        {
            "id": "https://openalex.org/subfields/1802",
            "subject": "Information Systems and Management",
        },
        {"subject": "RSE"},
    ]


@pytest.mark.vcr
def test_funded_project():
    "funded project"
    string = "https://api.rogue-scholar.org/posts/10.59350/p000s-pth40"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.59350/p000s-pth40"
    assert subject.type == "BlogPost"
    assert subject.title == "THOR's last hurrah"
    # assert subject.funding_references == [
    #     {
    #         "awardNumber": "654039",
    #         "awardTitle": "THOR – Technical and Human Infrastructure for Open Research",
    #         "awardUri": "https://doi.org/10.3030/654039",
    #         "funderIdentifier": "https://ror.org/019w4f821",
    #         "funderIdentifierType": "ROR",
    #         "funderName": "European Union",
    #     },
    # ]


@pytest.mark.vcr
def test_broken_reference():
    "JSON Feed broken reference"
    string = "https://api.rogue-scholar.org/posts/10.59350/z78kb-qrz59"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.59350/z78kb-qrz59"
    assert subject.type == "BlogPost"
    assert len(subject.references) == 6
    assert subject.references[3] == {
        "id": "https://doi.org/10.1016/s2214-109x(23)00198-5",
        "unstructured": "Laurenson-Schafer, H., Sklenovská, N., Hoxha, A., Kerr, S. M., Ndumbi, P., Fitzner, J., Almiron, M., de Sousa, L. A., Briand, S., Cenciarelli, O., Colombe, S., Doherty, M., Fall, I. S., García-Calavaro, C., Haussig, J. M., Kato, M., Mahamud, A. R., Morgan, O. W., Nabeth, P., … Biaukula, V. (2023). Description of the first global outbreak of mpox: an analysis of global surveillance data. <i>The Lancet Global Health</i>, <i>11</i>(7), e1012–e1023.",
    }


@pytest.mark.vcr
def test_get_jsonfeed():
    """Test get_jsonfeed"""
    item = get_jsonfeed_doi("10.59350/hzfr4-z0881")
    assert isinstance(item, dict)
    assert item["guid"] == "https://gigasciencejournal.com/blog/?p=6293"


@pytest.mark.vcr
def test_get_jsonfeed_item_not_found():
    """Test get_jsonfeed_doi not found"""
    assert get_jsonfeed_doi("notfound") is None


@pytest.mark.vcr
def test_get_jsonfeed_blog():
    """Test get_jsonfeed_blog"""
    string = "https://api.rogue-scholar.org/blogs/front_matter"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.53731/front_matter"
    assert subject.type == "Blog"
    assert subject.url == "https://blog.front-matter.de/"
    assert subject.title == "Front Matter"
    assert subject.identifiers == [
        {
            "identifier": "https://blog.front-matter.de/atom",
            "identifier_type": "URL",
        },
        {
            "identifier": "2749-9952",
            "identifier_type": "ISSN",
        },
    ]
    assert (
        subject.description
        == "The Front Matter Blog covers the intersection of science and technology since 2007."
    )
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "given_name": "Martin",
            "family_name": "Fenner",
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_updated == "2026-07-15T08:43:38Z" and subject.dates == {
        "created": "2023-01-01T00:00:00Z"
    }
    assert subject.publisher == {
        "name": "Front Matter",
    }
    assert subject.subjects == [
        {"id": "https://openalex.org/subfields/1710", "subject": "Information Systems"},
    ]
    assert subject.language == "en"


def test_blog_with_doi_keeps_community_relation():
    """A blog with a DOI must still emit the community IsPartOf relation.

    ``push_inveniordm`` assigns the blog community from the
    ``.../api/communities/<slug>`` IsPartOf relation and then removes it. When
    the blog-DOI IsPartOf was an ``elif`` of the community branch, records from
    blogs with a DOI lost community membership (regression in 0.265).
    """
    from commonmeta.readers.jsonfeed_reader import read_jsonfeed

    meta = {
        "id": "https://orion-dbs.community/blog/posts/x",
        "doi": "https://doi.org/10.59350/pdkx9-j2b63",
        "url": "https://orion-dbs.community/blog/posts/x",
        "title": "t",
        "published_at": 1700000000,
        "blog_slug": "orion",
        "blog": {
            "doi": "https://doi.org/10.59350/orion",
            "slug": "orion",
            "title": "ORION-DBs",
            "prefix": "10.59350",
        },
    }
    relations = read_jsonfeed(meta).get("relations")
    # Bibliographic IsPartOf → the blog DOI.
    assert {
        "id": "https://doi.org/10.59350/orion",
        "type": "IsPartOf",
    } in relations
    # Community IsPartOf → consumed by push_inveniordm for membership.
    assert {
        "id": "https://rogue-scholar.org/api/communities/orion",
        "type": "IsPartOf",
    } in relations


def test_blog_without_doi_keeps_community_relation():
    """A blog without an ISSN or DOI still emits the community IsPartOf."""
    from commonmeta.readers.jsonfeed_reader import read_jsonfeed

    meta = {
        "id": "https://example.com/blog/posts/y",
        "doi": "https://doi.org/10.59350/aaaaa-bbbbb",
        "url": "https://example.com/blog/posts/y",
        "title": "t",
        "published_at": 1700000000,
        "blog_slug": "example",
        "blog": {"slug": "example", "title": "Example", "prefix": "10.59350"},
    }
    relations = read_jsonfeed(meta).get("relations")
    assert {
        "id": "https://rogue-scholar.org/api/communities/example",
        "type": "IsPartOf",
    } in relations
