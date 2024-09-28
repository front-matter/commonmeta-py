# pylint: disable=invalid-name,too-many-lines
"""Crossref reader tests"""

from os import path
import re
import pytest

from commonmeta import Metadata, MetadataList
from commonmeta.readers.crossref_reader import (
    get_crossref,
    read_crossref,
    get_reference,
    get_crossref_list,
    get_random_crossref_id,
)


def vcr_config():
    return {"record_mode": "new_episodes"}


@pytest.mark.vcr
def test_doi_with_data_citation():
    "DOI with data citation"
    string = "10.7554/elife.01567"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://elifesciences.org/articles/01567"
    assert subject.titles[0] == {
        "title": "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    }
    assert len(subject.contributors) == 5
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martial",
        "familyName": "Sankar",
        "affiliations": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
            }
        ],
    }
    assert subject.license == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }

    assert subject.date == {"published": "2014-02-11"}
    assert subject.publisher == {
        "name": "eLife Sciences Publications, Ltd",
    }
    assert len(subject.references) == 27
    assert subject.references[0] == {
        "key": "bib1",
        "id": "https://doi.org/10.1038/nature02100",
        "contributor": "Bonke",
        "title": "APL regulates vascular tissue identity in Arabidopsis",
        "publicationYear": "2003",
        "volume": "426",
        "firstPage": "181",
        "containerTitle": "Nature",
    }
    assert subject.relations == [
        {"type": "IsSupplementedBy", "id": "https://doi.org/10.5061/dryad.b835k"},
        {"type": "HasReview", "id": "https://doi.org/10.7554/elife.01567.017"},
        {"type": "HasReview", "id": "https://doi.org/10.7554/elife.01567.016"},
        {"type": "IsPartOf", "id": "https://portal.issn.org/resource/ISSN/2050-084X"},
    ]
    assert subject.funding_references == [
        {"funderName": "SystemsX"},
        {"funderName": "EMBO longterm post-doctoral fellowships"},
        {"funderName": "Marie Heim-Voegtlin"},
        {
            "funderName": "University of Lausanne",
            "funderIdentifier": "https://doi.org/10.13039/501100006390",
            "funderIdentifierType": "Crossref Funder ID",
        },
        {
            "funderIdentifier": "https://doi.org/10.13039/501100003043",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "EMBO",
        },
        {
            "funderIdentifier": "https://doi.org/10.13039/501100001711",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "Swiss National Science Foundation",
        },
    ]
    assert subject.container == {
        "identifier": "2050-084X",
        "identifierType": "ISSN",
        "title": "eLife",
        "type": "Journal",
        "volume": "3",
    }
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Among various advantages, their small size makes")
    )
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "https://cdn.elifesciences.org/articles/01567/elife-01567-v1.pdf",
        "mimeType": "application/pdf",
    }


def test_journal_article():
    "journal article"
    string = "10.1371/journal.pone.0000030"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://dx.plos.org/10.1371/journal.pone.0000030"
    assert subject.titles[0] == {
        "title": "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    }
    assert len(subject.contributors) == 6
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Markus",
        "familyName": "Ralser",
    }
    assert subject.contributors[5] == {
        "familyName": "Janbon",
        "givenName": "Guilhem",
        "type": "Person",
        "contributorRoles": ["Editor"],
    }

    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {"published": "2006-12-20"}
    assert subject.publisher == {
        "name": "Public Library of Science (PLoS)",
    }
    assert len(subject.references) == 73
    assert subject.references[-1] == {
        "key": "ref73",
        "id": "https://doi.org/10.1056/nejm199109123251104",
        "contributor": "KB Hammond",
        "title": "Efficacy of statewide neonatal screening for cystic fibrosis by assay of trypsinogen concentrations.",
        "publicationYear": "1991",
        "volume": "325",
        "firstPage": "769",
        "containerTitle": "N Engl J Med",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "1932-6203",
        "identifierType": "ISSN",
        "title": "PLoS ONE",
        "type": "Journal",
        "issue": "1",
        "volume": "1",
        "firstPage": "e30",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_journal_article_with_funding():
    "journal article with funding"
    string = "10.3389/fpls.2019.00816"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.3389/fpls.2019.00816"
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "https://www.frontiersin.org/article/10.3389/fpls.2019.00816/full"
    )
    assert subject.titles[0] == {
        "title": "Transcriptional Modulation of Polyamine Metabolism in Fruit Species Under Abiotic and Biotic Stress"
    }
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Ana Margarida",
        "familyName": "Fortes",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {
        "published": "2019-07-02",
    }
    assert subject.publisher == {
        "name": "Frontiers Media SA",
    }
    assert len(subject.references) == 70
    assert subject.references[-1] == {
        "key": "ref70",
        "id": "https://doi.org/10.17660/actahortic.2004.632.41",
        "contributor": "Zheng",
        "title": "Effects of polyamines and salicylic acid on postharvest storage of “Ponkan” mandarin",
        "publicationYear": "2004",
        "volume": "632",
        "firstPage": "317",
        "containerTitle": "Acta Hortic.",
    }
    assert subject.funding_references == [
        {
            "awardNumber": "CA17111",
            "funderIdentifier": "https://doi.org/10.13039/501100000921",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "COST (European Cooperation in Science and Technology)",
        }
    ]
    assert subject.container == {
        "identifier": "1664-462X",
        "identifierType": "ISSN",
        "title": "Frontiers in Plant Science",
        "type": "Journal",
        "volume": "10",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_journal_article_original_language():
    "journal article with original language"
    string = "https://doi.org/10.7600/jspfsm.56.60"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "https://www.jstage.jst.go.jp/article/jspfsm/56/1/56_1_60/_article/-char/ja"
    )
    assert subject.titles is None
    assert subject.contributors is None
    assert subject.license is None
    assert subject.date == {"published": "2007"}
    assert subject.publisher == {
        "name": "The Japanese Society of Physical Fitness and Sports Medicine",
    }
    assert len(subject.references) == 7
    assert subject.references[-1] == {
        "key": "7",
        "id": "https://doi.org/10.1161/01.cir.95.6.1686",
        "unstructured": "Cheitlin MD et al. Circulation 95 : 1686-1744, 1997",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "1881-4751",
        "identifierType": "ISSN",
        "title": "Japanese Journal of Physical Fitness and Sports Medicine",
        "type": "Journal",
        "issue": "1",
        "volume": "56",
        "firstPage": "60",
        "lastPage": "60",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_journal_article_with_rdf_for_container():
    "journal article with RDF for container"
    string = "https://doi.org/10.1163/1937240X-00002096"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1163/1937240x-00002096"
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "https://academic.oup.com/jcb/article-lookup/doi/10.1163/1937240X-00002096"
    )
    assert subject.titles[0] == {
        "title": "Global distribution of Fabaeformiscandona subacuta: an&nbsp;exotic&nbsp;invasive Ostracoda on the Iberian Peninsula?"
    }
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Andreu",
        "familyName": "Escrivà",
    }
    assert subject.license is None
    assert subject.date == {"published": "2012-01-01"}
    assert subject.publisher == {
        "name": "Oxford University Press (OUP)",
    }
    assert len(subject.references) == 111
    assert subject.references[-1] == {
        "key": "bibr111",
        "contributor": "Zenina",
        "title": "Ostracod assemblages of the freshened part of Amursky Bay and lower reaches of Razdolnaya River (Sea of Japan)",
        "publicationYear": "2008",
        "volume": "Vol. 1",
        "firstPage": "156",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "1937-240X",
        "identifierType": "ISSN",
        "title": "Journal of Crustacean Biology",
        "type": "Journal",
        "issue": "6",
        "volume": "32",
        "firstPage": "949",
        "lastPage": "961",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_book_chapter_with_rdf_for_container():
    "book chapter with RDF for container"
    string = "https://doi.org/10.1007/978-3-642-33191-6_49"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-642-33191-6_49"
    assert subject.type == "BookChapter"
    assert subject.url == "http://link.springer.com/10.1007/978-3-642-33191-6_49"
    assert subject.titles[0] == {
        "title": "Human Body Orientation Estimation in Multiview Scenarios"
    }
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Lili",
        "familyName": "Chen",
    }
    assert subject.license is None
    assert subject.date == {"published": "2012"}
    assert subject.publisher == {"name": "Springer Berlin Heidelberg"}
    assert len(subject.references) == 11
    assert subject.references[-1] == {
        "key": "49_CR11",
        "unstructured": "Griesser, A., Roeck, D.S., Neubeck, A., Van Gool, L.: Gpu-based foreground-background segmentation using an extended colinearity criterion. In: Proc. of Vison, Modeling, and Visualization (VMV), pp. 319–326 (2005)",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "1611-3349",
        "identifierType": "ISSN",
        "title": "Lecture Notes in Computer Science",
        "type": "Book",
        "firstPage": "499",
        "lastPage": "508",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_posted_content():
    "posted content"
    string = "https://doi.org/10.1101/097196"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1101/097196"
    assert subject.type == "Article"
    assert subject.url == "http://biorxiv.org/lookup/doi/10.1101/097196"
    assert subject.titles[0] == {
        "title": "A Data Citation Roadmap for Scholarly Data Repositories"
    }
    assert len(subject.contributors) == 11
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
    }
    assert subject.license == {'id': 'CC-BY-4.0', 'url': 'https://creativecommons.org/licenses/by/4.0/legalcode'}
    assert subject.date["published"] == "2016-12-28"
    assert subject.publisher == {
        "name": "Cold Spring Harbor Laboratory",
    }
    assert len(subject.references) == 26
    assert subject.references[0] == {
        "key": "2024080313022960000_097196v2.1",
        "title": "An introduction to the joint principles for data citation",
        "publicationYear": "2015",
        "volume": "41",
        "issue": "3",
        "firstPage": "43",
        "containerTitle": "Bulletin of the American \\ldots",
    }
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container == {"type": "Periodical"}
    assert subject.subjects == [{"subject": "Scientific Communication and Education"}]
    assert subject.language is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "AbstractThis article presents a practical roadmap for scholarly data repositories"
        )
    )
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


@pytest.mark.vcr
def test_blog_post():
    "blog post"
    string = "https://doi.org/10.53731/ybhah-9jy85"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/ybhah-9jy85"
    assert subject.type == "Article"
    assert (
        subject.url
        == "https://blog.front-matter.io/posts/the-rise-of-the-science-newsletter"
    )
    assert subject.titles[0] == {"title": "The rise of the (science) newsletter"}
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Martin",
        "familyName": "Fenner",
        "affiliations": [{"name": "Front Matter"}],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {"published": "2023-10-04"}
    assert subject.publisher == {"name": "Front Matter"}
    assert len(subject.references) == 2
    assert subject.references[0] == {
        "key": "ref1",
        "id": "https://doi.org/10.1038/d41586-023-02554-0",
        "title": "Thousands of scientists are cutting back on Twitter, seeding angst and uncertainty",
        "publicationYear": "2023",
    }
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2749-9952", "type": "IsPartOf"}
    ]
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "2749-9952",
        "identifierType": "ISSN",
        "type": "Periodical",
    }
    assert subject.subjects == [{"subject": "Computer and information sciences"}]
    assert subject.language is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "Newsletters have been around forever, but their popularity has significantly increased in the past few years"
        )
    )
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files == [
        {
            "mimeType": "text/html",
            "url": "https://blog.front-matter.io/posts/the-rise-of-the-science-newsletter",
        },
        {
            "mimeType": "text/plain",
            "url": "https://api.rogue-scholar.org/posts/10.53731/ybhah-9jy85.md",
        },
        {
            "mimeType": "application/pdf",
            "url": "https://api.rogue-scholar.org/posts/10.53731/ybhah-9jy85.pdf",
        },
        {
            "mimeType": "application/epub+zip",
            "url": "https://api.rogue-scholar.org/posts/10.53731/ybhah-9jy85.epub",
        },
        {
            "mimeType": "application/xml",
            "url": "https://api.rogue-scholar.org/posts/10.53731/ybhah-9jy85.xml",
        },
    ]


def test_peer_review():
    "peer review"
    string = "10.7554/elife.55167.sa2"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.55167.sa2"
    assert subject.type == "PeerReview"
    assert subject.url == "https://elifesciences.org/articles/55167v1/peer-reviews"
    assert subject.titles[0] == {
        "title": "Author response: SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters"
    }
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-5286-4375",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Jeremy",
        "familyName": "Magland",
        "affiliations": [
            {"name": "Center for Computational Mathematics, Flatiron Institute"}
        ],
    }
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.7554/elife.55167.sa2",
            "identifierType": "DOI",
        }
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {"published": "2020-04-29"}
    assert subject.publisher == {
        "name": "eLife Sciences Publications, Ltd",
    }
    assert subject.references is None
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_dissertation():
    "dissertation"
    string = "10.14264/uql.2020.791"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.14264/uql.2020.791"
    assert subject.type == "Dissertation"
    assert subject.url == "http://espace.library.uq.edu.au/view/UQ:23a1e74"
    assert subject.titles[0] == {
        "title": "School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "familyName": "Collingwood",
        "givenName": "Patricia Maree",
        "id": "https://orcid.org/0000-0003-3086-4443",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license is None
    assert subject.date == {"published": "2020-06-08T05:08:58Z"}
    assert subject.publisher == {
        "name": "University of Queensland Library",
    }
    assert subject.references is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_doi_with_sici():
    "doi with sici"
    string = "10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    subject = Metadata(string)
    assert subject.is_valid
    assert (
        subject.id == "https://doi.org/10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    )
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "http://doi.wiley.com/10.1890/0012-9658(2006)87[2832:TIOPMA]2.0.CO;2"
    )
    assert subject.titles[0] == {
        "title": "THE IMPACT OF PARASITE MANIPULATION AND PREDATOR FORAGING BEHAVIOR ON PREDATOR–PREY COMMUNITIES"
    }
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "A.",
        "familyName": "Fenton",
    }
    assert subject.license == {"url": "https://doi.wiley.com/10.1002/tdm_license_1.1"}
    assert subject.date == {"published": "2006-11"}
    assert subject.publisher == {"name": "Wiley"}
    assert len(subject.references) == 39
    assert subject.references[-1] == {
        "key": "i0012-9658-87-11-2832-ydenberg1",
        "unstructured": "R. C. Ydenberg, 1998 .Behavioral decisions about foraging and predator avoidance .Pages343 -378inR. Dukas, editorCognitive ecology: the evolutionary ecology of information processing and decision making University of Chicago Press, Chicago, Illinois, USA.",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "firstPage": "2832",
        "identifier": "0012-9658",
        "identifierType": "ISSN",
        "issue": "11",
        "lastPage": "2841",
        "title": "Ecology",
        "type": "Journal",
        "volume": "87",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_doi_with_orcid():
    "doi_with_orcid"
    string = "10.1155/2012/291294"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1155/2012/291294"
    assert subject.type == "JournalArticle"
    assert subject.url == "http://www.hindawi.com/journals/pm/2012/291294"
    assert subject.titles[0] == {
        "title": "Delineating a Retesting Zone Using Receiver Operating Characteristic Analysis on Serial QuantiFERON Tuberculosis Test Results in US Healthcare Workers"
    }
    assert len(subject.contributors) == 7
    assert subject.contributors[2] == {
        "id": "https://orcid.org/0000-0003-2043-4925",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Beatriz",
        "familyName": "Hernandez",
        "affiliations": [
            {
                "name": "War Related Illness and Injury Study Center (WRIISC) and Mental Illness Research Education and Clinical Center (MIRECC), Department of Veterans Affairs, Palo Alto, CA 94304, USA"
            },
            {
                "name": "Department of Psychiatry and Behavioral Sciences, Stanford University School of Medicine, Stanford, CA 94304, USA"
            },
        ],
    }
    assert subject.license == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }
    assert subject.date == {"published": "2012"}
    assert subject.publisher == {"name": "Hindawi Limited"}
    assert len(subject.references) == 27
    assert subject.references[-1] == {
        "key": "30",
        "id": "https://doi.org/10.1378/chest.12-0045",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "2090-1844",
        "identifierType": "ISSN",
        "title": "Pulmonary Medicine",
        "type": "Journal",
        "volume": "2012",
        "firstPage": "1",
        "lastPage": "7",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Objective. To find a statistically significant separation point for the QuantiFERON Gold In-Tube (QFT) interferon gamma release assay that could define an optimal “retesting zone” for use in serially tested low-risk populations who have test “reversions” from initially positive to subsequently negative results.Method. Using receiver operating characteristic analysis (ROC) to analyze retrospective data collected from 3 major hospitals, we searched for predictors of reversion until statistically significant separation points were revealed. A confirmatory regression analysis was performed on an additional sample.Results. In 575 initially positive US healthcare workers (HCWs), 300 (52.2%) had reversions, while 275 (47.8%) had two sequential positive tests. The most statistically significant (Kappa = 0.48, chi-square = 131.0,P&lt;0.001) separation point identified by the ROC for predicting reversion was the tuberculosis antigen minus-nil (TBag-nil) value at 1.11 International Units per milliliter (IU/mL). The second separation point was found at TBag-nil at 0.72 IU/mL (Kappa = 0.16, chi-square = 8.2,P&lt;0.01). The model was validated by the regression analysis of 287 HCWs.Conclusion. Reversion likelihood increases as the TBag-nil approaches the manufacturer's cut-point of 0.35 IU/mL. The most statistically significant separation point between those who test repeatedly positive and those who revert is 1.11 IU/mL. Clinicians should retest low-risk individuals with initial QFT results &lt; 1.11 IU/mL.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "http://downloads.hindawi.com/journals/pm/2012/291294.pdf",
        "mimeType": "application/pdf",
    }


def test_date_in_future():
    "date_in_future"
    string = "10.1016/j.ejphar.2015.03.018"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1016/j.ejphar.2015.03.018"
    assert subject.type == "JournalArticle"
    assert (
        subject.url == "https://linkinghub.elsevier.com/retrieve/pii/S0014299915002332"
    )
    assert subject.titles[0] == {
        "title": "Paving the path to HIV neurotherapy: Predicting SIV CNS disease"
    }
    assert len(subject.contributors) == 10
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Sarah E.",
        "familyName": "Beck",
    }
    assert subject.license == {"url": "https://www.elsevier.com/tdm/userlicense/1.0"}
    assert subject.date == {"published": "2015-07"}
    assert subject.publisher == {"name": "Elsevier BV"}
    assert len(subject.references) == 98
    assert subject.references[-1] == {
        "key": "10.1016/j.ejphar.2015.03.018_bib94",
        "id": "https://doi.org/10.1111/hiv.12134",
        "contributor": "Zoufaly",
        "title": "Immune activation despite suppressive highly active antiretroviral therapy is associated with higher risk of viral blips in HIV-1-infected individuals",
        "publicationYear": "2014",
        "volume": "15",
        "firstPage": "449",
        "containerTitle": "HIV Med.",
    }
    assert subject.relations == [
        {"type": "HasReview", "id": "https://doi.org/10.3410/f.725411277.793529613"},
        {"id": "https://portal.issn.org/resource/ISSN/0014-2999", "type": "IsPartOf"},
    ]
    assert subject.funding_references == [
        {
            "awardNumber": "R01 NS089482",
            "funderIdentifier": "https://doi.org/10.13039/100000002",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "NIH",
        },
        {
            "awardNumber": "R01 NS077869",
            "funderIdentifier": "https://doi.org/10.13039/100000002",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "NIH",
        },
        {
            "awardNumber": "P01 MH070306",
            "funderIdentifier": "https://doi.org/10.13039/100000002",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "NIH",
        },
        {
            "awardNumber": "P40 OD013117",
            "funderIdentifier": "https://doi.org/10.13039/100000002",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "NIH",
        },
        {
            "awardNumber": "T32 OD011089",
            "funderIdentifier": "https://doi.org/10.13039/100000002",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "NIH",
        },
    ]
    assert subject.container == {
        "identifier": "0014-2999",
        "identifierType": "ISSN",
        "title": "European Journal of Pharmacology",
        "type": "Journal",
        "volume": "759",
        "firstPage": "303",
        "lastPage": "312",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "https://api.elsevier.com/content/article/PII:S0014299915002332?httpAccept=text/xml",
        "mimeType": "text/xml",
    }


def test_vor_with_url():
    "vor_with_url"
    string = "10.1038/hdy.2013.26"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1038/hdy.2013.26"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://www.nature.com/articles/hdy201326"
    assert subject.titles[0] == {
        "title": "Albinism in phylogenetically and geographically distinct populations of Astyanax cavefish arises through the same loss-of-function Oca2 allele"
    }
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "J B",
        "familyName": "Gross",
    }
    assert subject.license == {"url": "https://www.springer.com/tdm"}
    assert subject.date == {"published": "2013-04-10"}
    assert subject.publisher == {"name": "Springer Science and Business Media LLC"}
    assert len(subject.references) == 41
    assert subject.references[-1] == {
        "key": "BFhdy201326_CR41",
        "id": "https://doi.org/10.1111/j.1095-8312.2003.00230.x",
        "contributor": "H Wilkens",
        "publicationYear": "2003",
        "volume": "80",
        "firstPage": "545",
        "containerTitle": "Biol J Linn Soc",
        "unstructured": "Wilkens H, Strecker U . (2003). Convergent evolution of the "
        "cavefish Astyanax (Characidae: Teleostei): Genetic evidence "
        "from reduced eye-size and pigmentation. Biol J Linn Soc 80: "
        "545–554.",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "1365-2540",
        "identifierType": "ISSN",
        "title": "Heredity",
        "type": "Journal",
        "volume": "111",
        "issue": "2",
        "firstPage": "122",
        "lastPage": "130",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "http://www.nature.com/articles/hdy201326.pdf",
        "mimeType": "application/pdf",
    }


def test_dataset():
    "dataset"
    string = "10.2210/pdb4hhb/pdb"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.2210/pdb4hhb/pdb"
    assert subject.type == "Component"
    assert subject.url == "https://www.wwpdb.org/pdb?id=pdb_00004hhb"
    assert subject.titles[0] == {
        "title": "THE CRYSTAL STRUCTURE OF HUMAN DEOXYHAEMOGLOBIN AT 1.74 ANGSTROMS RESOLUTION"
    }
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "G.",
        "familyName": "Fermi",
    }
    assert subject.license is None
    assert subject.date == {"published": "1984-07-17"}
    assert subject.publisher == {"name": "Worldwide Protein Data Bank"}
    assert subject.references is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_component():
    "component"
    string = "10.1371/journal.pmed.0030277.g001"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pmed.0030277.g001"
    assert subject.type == "Component"
    assert subject.url == "https://dx.plos.org/10.1371/journal.pmed.0030277.g001"
    assert subject.titles is None
    assert subject.contributors is None
    assert subject.license is None
    assert subject.date == {"published": "2015-10-20T20:01:19Z"}
    assert subject.publisher == {"name": "Public Library of Science (PLoS)"}
    assert subject.references is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_dataset_usda():
    "dataset usda"
    string = "10.2737/RDS-2018-0001"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.2737/rds-2018-0001"
    assert subject.type == "Dataset"
    assert subject.url == "https://www.fs.usda.gov/rds/archive/Catalog/RDS-2018-0001"
    assert subject.titles[0] == {"title": "Fledging times of grassland birds"}
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-2583-1778",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Christine A.",
        "familyName": "Ribic",
        "affiliations": [{"name": "U.S. Geological Survey"}],
    }
    assert subject.license is None
    assert subject.date == {"published": "2017-08-09T19:44:20Z"}
    assert subject.publisher == {"name": "Forest Service Research Data Archive"}
    assert len(subject.references) == 6
    assert subject.references[-1] == {
        "key": "ref6",
        "id": "https://doi.org/10.1674/0003-0031-178.1.47",
    }
    assert subject.funding_references == [
        {
            "funderIdentifier": "https://doi.org/10.13039/100006959",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "U.S. Forest Service",
        }
    ]
    assert subject.container == {
        "title": "Forest Service Research Data Archive",
        "type": "DataRepository",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_crossref_json():
    """crossref.json"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref.json")
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "mimeType": "application/pdf",
        "url": "https://cdn.elifesciences.org/articles/01567/elife-01567-v1.pdf",
    }


def test_book_chapter():
    "book chapter"
    string = "10.1007/978-3-662-46370-3_13"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-662-46370-3_13"
    assert subject.type == "BookChapter"
    assert subject.url == "https://link.springer.com/10.1007/978-3-662-46370-3_13"
    assert subject.titles[0] == {"title": "Clinical Symptoms and Physical Examinations"}
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Ronald L.",
        "familyName": "Diercks",
    }
    assert subject.license == {
        "url": "https://www.springernature.com/gp/researchers/text-and-data-mining"
    }
    assert subject.date == {"published": "2015"}
    assert subject.publisher == {"name": "Springer Berlin Heidelberg"}
    assert len(subject.references) == 22
    assert subject.references[0] == {
        "key": "13_CR1",
        "id": "https://doi.org/10.1007/s00256-012-1391-8",
        "contributor": "KS Ahn",
        "publicationYear": "2012",
        "volume": "41",
        "issue": "10",
        "firstPage": "1301",
        "containerTitle": "Skeletal Radiol",
        "unstructured": "Ahn KS, Kang CH, Oh YW, Jeong WK. Correlation between "
        "magnetic resonance imaging and clinical impairment in "
        "patients with adhesive capsulitis. Skeletal Radiol. "
        "2012;41(10):1301–8.",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "identifier": "9783662463703",
        "identifierType": "ISBN",
        "title": "Shoulder Stiffness",
        "firstPage": "155",
        "lastPage": "158",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_another_book_chapter():
    "another book chapter"
    string = "10.1007/978-3-319-75889-3_1"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-319-75889-3_1"
    assert subject.type == "BookChapter"
    assert subject.url == "http://link.springer.com/10.1007/978-3-319-75889-3_1"
    assert subject.titles[0] == {
        "title": "Climate Change and Increasing Risk of Extreme Heat"
    }
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Hunter M.",
        "familyName": "Jones",
    }
    assert subject.license == {"url": "https://www.springer.com/tdm"}
    assert subject.date == {"published": "2018"}
    assert subject.publisher == {"name": "Springer International Publishing"}
    assert len(subject.references) == 44
    assert subject.references[0] == {
        "key": "1_CR1",
        "unstructured": "Associated Press First heat, now fog dogging Olympic event planning in Sochi (2014) The National [Internet]. 2014 Feb 17; Available from: https://www.thenational.ae/sport/first-heat-now-fog-dogging-olympic-event-planning-in-sochi-1.280874",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "title": "SpringerBriefs in Medical Earth Sciences",
        "identifier": "2523-3629",
        "identifierType": "ISSN",
        "firstPage": "1",
        "lastPage": "13",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_yet_another_book_chapter():
    "yet another book chapter"
    string = "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    assert subject.type == "BookChapter"
    assert (
        subject.url
        == "http://services.igi-global.com/resolvedoi/resolve.aspx?doi=10.4018/978-1-4666-1891-6.ch004"
    )
    assert subject.titles == [
        {
            "title": "Unsupervised and Supervised Image Segmentation Using Graph Partitioning"
        }
    ]
    assert subject.contributors[0] == {
        "affiliations": [{"name": "Université de Lyon, France"}],
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Charles-Edmond",
        "familyName": "Bichot",
    }
    assert subject.license is None
    assert subject.date == {"published": "2012-08-08T16:54:07Z"}
    assert subject.publisher == {"name": "IGI Global"}
    assert len(subject.references) == 33
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "title": "Graph-Based Methods in Computer Vision",
        "firstPage": "72",
        "lastPage": "94",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions == [
        {
            "description": "Image segmentation is an important research area in computer vision and its applications in different disciplines, such as medicine, are of great importance. It is often one of the very first steps of computer vision or pattern recognition methods. This is because segmentation helps to locate objects and boundaries into images. The objective of segmenting an image is to partition it into disjoint and homogeneous sets of pixels. When segmenting an image it is natural to try to use graph partitioning, because segmentation and partitioning share the same high-level objective, to partition a set into disjoints subsets. However, when using graph partitioning for segmenting an image, several big questions remain: What is the best way to convert an image into a graph? Or to convert image segmentation objectives into graph partitioning objectives (not to mention what are image segmentation objectives)? What are the best graph partitioning methods and algorithms for segmenting an image? In this chapter, the author tries to answer these questions, both for unsupervised and supervised image segmentation approach, by presenting methods and algorithms and by comparing them.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_missing_contributor():
    "missing contributor"
    string = "https://doi.org/10.3390/publications6020015"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.3390/publications6020015"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://www.mdpi.com/2304-6775/6/2/15"
    assert subject.titles[0] == {
        "title": "Converting the Literature of a Scientific Field to Open Access through Global Collaboration: The Experience of SCOAP3 in Particle Physics"
    }
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-3836-8885",
        "type": "Person",
        "affiliations": [
            {
                "name": "CERN, CH-1211 Geneva 23, Switzerland",
            },
        ],
        "contributorRoles": ["Author"],
        "givenName": "Alexander",
        "familyName": "Kohls",
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {"published": "2018-04-09"}
    assert subject.publisher == {"name": "MDPI AG"}
    assert len(subject.references) == 23
    assert subject.references[-1] == {
        "key": "ref_23",
        "unstructured": "(2018, February 20). SCOAP3 News: APS Joins SCOAP3. Available online: http://www.webcitation.org/6xNFQb5iD.",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Journal",
        "title": "Publications",
        "firstPage": "15",
        "issue": "2",
        "volume": "6",
        "identifier": "2304-6775",
        "identifierType": "ISSN",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Gigantic particle accelerators, incredibly complex "
            "detectors, an antimatter factory and the discovery of the "
            "Higgs boson—this is part of what makes CERN famous. Only a "
            "few know that CERN also hosts the world largest Open Access "
            "initiative: SCOAP3. The Sponsoring Consortium for Open "
            "Access Publishing in Particle Physics started operation in "
            "2014 and has since supported the publication of 20,000 Open "
            "Access articles in the field of particle physics, at no "
            "direct cost, nor burden, for individual authors worldwide. "
            "SCOAP3 is made possible by a 3000-institute strong "
            "partnership, where libraries re-direct funds previously used "
            "for subscriptions to ‘flip’ articles to ‘Gold Open Access’. "
            "With its recent expansion, the initiative now covers about "
            "90% of the journal literature of the field. This article "
            "describes the economic principles of SCOAP3, the "
            "collaborative approach of the partnership, and finally "
            "summarizes financial results after four years of successful "
            "operation.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_missing_contributor_name():
    "missing contributor name"
    string = "https://doi.org/10.14264/3e10f66"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.14264/3e10f66"
    assert subject.type == "Dissertation"
    assert subject.url == "https://espace.library.uq.edu.au/view/UQ:3e10f66"
    assert subject.titles[0] == {
        "title": "A computational impact analysis approach leveraging non-conforming spatial, temporal and methodological discretisations"
    }
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0001-5777-3141",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Peter",
        "familyName": "Wilson",
    }
    assert subject.license is None
    assert subject.date == {"published": "2022-12-21T04:12:27Z"}
    assert subject.publisher == {"name": "University of Queensland Library"}


def test_too_many_contributor_names():
    "too many contributor names"
    string = "https://doi.org/10.3934/nhm.2009.4.249"
    subject = Metadata(string)
    # assert subject.is_valid
    assert subject.id == "https://doi.org/10.3934/nhm.2009.4.249"
    assert subject.type == "JournalArticle"
    assert subject.url == "http://aimsciences.org//article/doi/10.3934/nhm.2009.4.249"
    assert subject.titles[0] == {
        "title": "A Hamiltonian perspective to the stabilization of systems of two conservation laws"
    }
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Valérie",
        "familyName": "Dos Santos",
    }
    assert subject.contributors[2] == {
        "contributorRoles": ["Author"],
        "familyName": "Le Gorrec",
        "givenName": "Yann",
        "type": "Person",
    }
    assert subject.license is None
    assert subject.date == {"published": "2009"}
    assert subject.publisher == {
        "name": "American Institute of Mathematical Sciences (AIMS)"
    }


def test_book():
    "book"
    string = "https://doi.org/10.1017/9781108348843"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1017/9781108348843"
    assert subject.type == "Book"
    assert (
        subject.url
        == "https://www.cambridge.org/core/product/identifier/9781108348843/type/book"
    )
    assert subject.titles[0] == {"title": "The Politics of the Past in Early China"}
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Vincent S.",
        "familyName": "Leung",
    }
    assert subject.license == {"url": "https://www.cambridge.org/core/terms"}
    assert subject.publisher == {"name": "Cambridge University Press"}
    assert len(subject.references) == 273
    assert subject.references[0] == {
        "key": "9781108348843#EMT-rl-1_BIBe-r-273",
        "contributor": "Qiusheng",
        "title": "Lu Jia de lishi yishi ji qi wenhua yiyi",
        "publicationYear": "1997",
        "volume": "5",
        "firstPage": "67",
        "containerTitle": "Qilu xuekan",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "9781108348843",
        "identifierType": "ISBN",
        "type": "BookSeries",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert subject.files is None


def test_proceedings_article():
    "proceedings article"
    string = "10.1145/3448016.3452841"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1145/3448016.3452841"
    assert subject.type == "ProceedingsArticle"
    assert subject.url == "https://dl.acm.org/doi/10.1145/3448016.3452841"
    assert subject.titles == [
        {"title": "Vector Quotient Filters"},
        {
            "title": "Overcoming the Time/Space Trade-Off in Filter Design",
            "titleType": "Subtitle",
        },
    ]
    assert len(subject.contributors) == 6
    assert subject.contributors[0] == {
        "affiliations": [
            {
                "name": "Lawrence Berkeley National Lab &amp; University of California, Berkeley, Berkeley, CA, USA"
            }
        ],
        "givenName": "Prashant",
        "familyName": "Pandey",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license == {
        "url": "https://www.acm.org/publications/policies/copyright_policy#Background"
    }
    assert subject.date == {"published": "2021-06-09"}
    assert subject.publisher == {"name": "ACM"}
    assert len(subject.references) == 56
    assert subject.references[-1] == {
        "key": "e_1_3_2_2_56_1",
        "id": "https://doi.org/10.5555/1364813.1364831",
    }
    assert subject.funding_references == [
        {
            "funderName": "NSF (National Science Foundation)",
            "funderIdentifier": "https://doi.org/10.13039/100000001",
            "funderIdentifierType": "Crossref Funder ID",
            "awardNumber": "CCF 805476, CCF 822388, CCF 1724745,CCF 1715777, CCF 1637458, IIS 1541613, CRII 1947789, CNS 1408695, CNS 1755615, CCF 1439084, CCF 1725543, CSR 1763680, CCF 1716252, CCF 1617618, CNS 1938709, IIS 1247726, CNS-1938709,CCF-1750472,CCF-1452904,CNS-1763680",
        },
        {
            "funderName": "DOE U.S. Department of Energy",
            "funderIdentifier": "https://doi.org/10.13039/100000015",
            "funderIdentifierType": "Crossref Funder ID",
            "awardNumber": "DE-AC02-05CH11231,17-SC-20-SC",
        },
    ]
    assert subject.container == {
        "type": "Proceedings",
        "title": "Proceedings of the 2021 International Conference on Management of Data",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 1
    assert subject.files[0] == {
        "url": "https://dl.acm.org/doi/pdf/10.1145/3448016.3452841",
        "mimeType": "application/pdf",
    }


@pytest.mark.vcr
def test_multipe_titles():
    "multiple titles"
    string = "10.1007/s00120-007-1345-2"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/s00120-007-1345-2"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://link.springer.com/10.1007/s00120-007-1345-2"
    assert subject.titles == [
        {"title": "Penisverletzung durch eine Moulinette"},
        {"title": "Penile injury caused by a Moulinette"},
        {
            "title": "Folge einer autoerotischen Selbstverstümmelung",
            "titleType": "Subtitle",
        },
        {"title": "Result of autoerotic self-mutilation", "titleType": "Subtitle"},
    ]
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "M.",
        "familyName": "Lehsnau",
    }
    assert subject.license == {"url": "https://www.springer.com/tdm"}
    assert subject.date == {"published": "2007-07"}
    assert subject.publisher == {"name": "Springer Science and Business Media LLC"}
    assert len(subject.references) == 20
    assert subject.references[-1] == {
        "key": "1345_CR20",
        "id": "https://doi.org/10.1159/000281702",
        "contributor": "Wandschneider",
        "publicationYear": "1990",
        "volume": "45",
        "firstPage": "177",
        "containerTitle": "Urol Int",
        "unstructured": "Wandschneider G, Hellbom B, Pummer K, Primus G (1990) Successful replantation of a totally amputated penis by using microvascular techniques. Urol Int 45: 177–180",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Journal",
        "identifier": "1433-0563",
        "identifierType": "ISSN",
        "title": "Der Urologe",
        "volume": "46",
        "issue": "7",
        "firstPage": "776",
        "lastPage": "779",
    }
    assert subject.subjects is None
    assert subject.language == "de"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "https://link.springer.com/content/pdf/10.1007/s00120-007-1345-2.pdf",
        "mimeType": "application/pdf",
    }


@pytest.mark.vcr
def test_get_random_crossref_id():
    """Random DOI from Crossref API"""
    data = get_random_crossref_id()
    assert len(data) == 1
    assert re.match("^10\\.\\d{4,5}/.+", data[0])
    # 5 random DOIs
    data = get_random_crossref_id(5)
    assert len(data) == 5
    assert re.match("^10\\.\\d{4,5}/.+", data[0])


def test_get_crossref():
    """get_crossref"""
    data = get_crossref("https://doi.org/10.1017/9781108348843")
    assert isinstance(data, dict)
    assert data.get("DOI") == "10.1017/9781108348843"


def test_read_crossref():
    """read_crossref"""
    data = get_crossref("https://doi.org/10.1017/9781108348843")
    meta = read_crossref(data)
    assert isinstance(meta, dict)
    assert meta.get("id") == "https://doi.org/10.1017/9781108348843"


@pytest.mark.vcr
def test_get_crossref_list():
    """get_crossref_list"""
    query = {"prefix": "10.5555", "type": "journal-article"}
    data = get_crossref_list(query)
    assert isinstance(data, list)
    assert len(data) == 20
    assert data[0].get("DOI") == "10.1306/703c7c64-1707-11d7-8645000102c1865d"
    assert data[0].get("type") == "journal-article"


def test_read_crossref_list():
    """read_crossref_list"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref-list.json")
    subject_list = MetadataList(string)
    assert len(subject_list.items) == 20
    subject = subject_list.items[0]
    assert subject.id == "https://doi.org/10.1306/703c7c64-1707-11d7-8645000102c1865d"
    assert subject.type == "JournalArticle"


def test_get_reference():
    """get_reference"""
    doi_metadata = {
        "key": "978-1-4666-1891-6.ch004.-31",
        "doi-asserted-by": "crossref",
        "unstructured": "Sinop, A. K., & Grady, L. (2007). A seeded image segmentation framework unifying graph cuts and random walker which yields a new algorithm. Proceedings of the 2007 International Conference on Computer Vision, (pp. 1-8).",
        "DOI": "https://doi.org/10.1109/ICCV.2007.4408927",
    }
    unstructured_metadata = {
        "key": "978-1-4666-1891-6.ch004.-14",
        "first-page": "938",
        "article-title": "Algorithms for partitioning graphs and computer logic based on eigenvectors of connection matrices.",
        "volume": "15",
        "author": "W.Donath",
        "year": "1972",
        "journal-title": "IBM Technical Disclosure Bulletin",
    }
    assert {
        "key": "978-1-4666-1891-6.ch004.-31",
        "id": "https://doi.org/10.1109/iccv.2007.4408927",
        "unstructured": "Sinop, A. K., & Grady, L. (2007). A seeded image segmentation framework unifying graph cuts and random walker which yields a new algorithm. Proceedings of the 2007 International Conference on Computer Vision, (pp. 1-8).",
    } == get_reference(doi_metadata)
    assert {
        "key": "978-1-4666-1891-6.ch004.-14",
        "contributor": "W.Donath",
        "title": "Algorithms for partitioning graphs and computer logic based on eigenvectors of connection matrices.",
        "publicationYear": "1972",
        "volume": "15",
        "firstPage": "938",
        "containerTitle": "IBM Technical Disclosure Bulletin",
    } == get_reference(unstructured_metadata)
    assert None is get_reference(None)
