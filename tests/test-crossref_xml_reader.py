# pylint: disable=invalid-name,too-many-lines
"""Crossref XML reader tests"""
from os import path
import pytest
from commonmeta import Metadata


@pytest.mark.vcr
def test_doi_with_data_citation():
    "DOI with data citation"
    string = "10.7554/elife.01567"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://elifesciences.org/articles/01567"
    assert subject.titles[0] == {
        "title": "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    }
    assert len(subject.creators) == 5
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Martial",
        "familyName": "Sankar",
        "affiliation": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
            }
        ],
    }
    assert subject.contributors is None
    assert subject.rights == [
        {
            "rights": "Creative Commons Attribution 3.0 Unported",
            "rightsIdentifier": "cc-by-3.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/3.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]
    assert subject.dates == [
        {"date": "2014-02-11", "dateType": "Issued"},
        {"date": "2022-03-26T09:21:50Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2014
    assert subject.publisher == "eLife Sciences Publications, Ltd"
    assert len(subject.references) == 27
    assert subject.references[0] == {
        "key": "bib1",
        "doi": "https://doi.org/10.1038/nature02100",
        "creator": "Bonke",
        "title": "APL regulates vascular tissue identity in Arabidopsis",
        "publicationYear": "2003",
        "volume": "426",
        "firstPage": "181",
        "containerTitle": "Nature",
    }
    assert subject.funding_references == [
        {"funderName": "SystemsX"},
        {"funderName": "EMBO longterm post-doctoral fellowships"},
        {"funderName": "Marie Heim-Voegtlin"},
        {
            "funderName": "University of Lausanne",
            "funderIdentifier": "https://doi.org/10.13039/501100006390",
            "funderIdentifierType": "Crossref Funder ID",
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
    assert subject.agency == "Crossref"


def test_journal_article():
    "journal article"
    string = "10.1371/journal.pone.0000030"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://dx.plos.org/10.1371/journal.pone.0000030"
    assert subject.titles[0] == {
        "title": "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    }
    assert len(subject.creators) == 5
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Markus",
        "familyName": "Ralser",
    }
    assert subject.contributors == [
        {
            "familyName": "Janbon",
            "givenName": "Guilhem",
            "nameType": "Personal",
        }
    ]
    assert subject.rights == [
        {
            "rights": "Creative Commons Attribution 4.0 International",
            "rightsIdentifier": "cc-by-4.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]
    assert subject.dates == [
        {"date": "2006-12-20", "dateType": "Issued"},
        {"date": "2021-08-06T23:49:55Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2006
    assert subject.publisher == "Public Library of Science (PLoS)"
    assert len(subject.references) == 73
    assert subject.references[0] == {
        "key": "ref1",
        "doi": "https://doi.org/10.1056/nejm196502042720503",
        "creator": "AS Schneider",
        "title": "Hereditary Hemolytic Anemia with Triosephosphate Isomerase Deficiency.",
        "publicationYear": "1965",
        "volume": "272",
        "firstPage": "229",
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
    assert subject.agency == "Crossref"


def test_journal_article_with_funding():
    "journal article with funding"
    string = "10.3389/fpls.2019.00816"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.3389/fpls.2019.00816"
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "https://www.frontiersin.org/article/10.3389/fpls.2019.00816/full"
    )
    assert subject.titles[0] == {
        "title": "Transcriptional Modulation of Polyamine Metabolism in Fruit Species Under Abiotic and Biotic Stress"
    }
    assert len(subject.creators) == 4
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Ana Margarida",
        "familyName": "Fortes",
    }
    assert subject.contributors is None
    assert subject.rights == [
        {
            "rights": "Creative Commons Attribution 4.0 International",
            "rightsIdentifier": "cc-by-4.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]
    assert subject.dates[0] == {"date": "2019-07-02", "dateType": "Issued"}
    assert subject.publication_year == 2019
    assert subject.publisher == "Frontiers Media SA"
    assert len(subject.references) == 70
    assert subject.references[0] == {
        "key": "ref1",
        "doi": "https://doi.org/10.1016/j.plaphy.2013.11.002",
        "creator": "Agudelo-Romero",
        "title": "Perturbation of polyamine catabolism affects grape ripening of Vitis vinifera cv. Trincadeira",
        "publicationYear": "2014",
        "volume": "74",
        "firstPage": "141",
        "containerTitle": "Plant Physiol. Biochem.",
    }
    assert subject.funding_references == [
        {"awardNumber": "UID/MULTI/04046/2019"},
        {
            "funderName": "COST (European Cooperation in Science and Technology)",
            "funderIdentifier": "https://doi.org/10.13039/501100000921",
            "funderIdentifierType": "Crossref Funder ID",
            "awardNumber": "CA17111",
        },
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
    assert subject.agency == "Crossref"


def test_journal_article_original_language():
    "journal article with original language"
    string = "https://doi.org/10.7600/jspfsm.56.60"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "https://www.jstage.jst.go.jp/article/jspfsm/56/1/56_1_60/_article/-char/ja"
    )
    assert subject.titles[0].get("title") == "自律神経・循環器応答"
    assert subject.creators == []
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates == [
        {"date": "2007", "dateType": "Issued"},
        {"date": "2021-05-20T22:32:01Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2007
    assert (
        subject.publisher
        == "The Japanese Society of Physical Fitness and Sports Medicine"
    )
    assert len(subject.references) == 7
    assert subject.references[0] == {
        "key": "1",
        "doi": "https://doi.org/10.1111/j.1469-7793.2000.00407.x",
    }
    assert subject.references[-1] == {
        "key": "7",
        "doi": "https://doi.org/10.1161/01.cir.95.6.1686",
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
    assert subject.agency == "Crossref"


def test_journal_article_with_rdf_for_container():
    "journal article with RDF for container"
    string = "https://doi.org/10.1163/1937240X-00002096"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1163/1937240x-00002096"
    assert subject.type ==  "JournalArticle"
    assert (
        subject.url
        == "https://academic.oup.com/jcb/article-lookup/doi/10.1163/1937240X-00002096"
    )
    assert subject.titles[0] == {
        "title": "Global distribution of Fabaeformiscandona subacuta: an exotic invasive Ostracoda on the Iberian Peninsula?"
    }
    assert len(subject.creators) == 8
    assert subject.creators[0] == {
        "givenName": "Francesc",
        "familyName": "Mesquita-Joanes",
        "nameType": "Personal",
    }
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates[0] == {"date": "2012-01-01", "dateType": "Issued"}
    assert subject.publication_year == 2012
    assert subject.publisher == "Oxford University Press (OUP)"
    assert len(subject.references) == 111
    assert subject.references[0] == {
        "key": "bibr1",
        "creator": "Absolon",
        "title": "Die Gattung Candonaim Quartar von Europa",
        "publicationYear": "1978",
        "volume": "88",
        "issue": "5",
        "firstPage": "1",
        "containerTitle": "Rozpravy Ceskoslovenske Akademie Ved, Rada Matematickych A Prirodnich Ved",  # noqa: E501
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
    assert subject.agency == "Crossref"


def test_book_chapter_with_rdf_for_container():
    "book chapter with RDF for container"
    string = "https://doi.org/10.1007/978-3-642-33191-6_49"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1007/978-3-642-33191-6_49"
    assert subject.type == "BookChapter"
    assert subject.url == "http://link.springer.com/10.1007/978-3-642-33191-6_49"
    assert subject.titles[0] == {
        "title": "Human Body Orientation Estimation in Multiview Scenarios"
    }
    assert len(subject.creators) == 3
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Lili",
        "familyName": "Chen",
    }
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates == [
        {"date": "2012", "dateType": "Issued"},
        {"date": "2020-11-24T03:11:32Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2012
    assert subject.publisher == "Springer Science and Business Media LLC"
    assert len(subject.references) == 11
    assert subject.references[-1] == {
        "key": "49_CR11",
        "unstructured": "Griesser, A., Roeck, D.S., Neubeck, A., Van Gool, L.: Gpu-based foreground-background segmentation using an extended colinearity criterion. In: Proc. of Vison, Modeling, and Visualization (VMV), pp. 319–326 (2005)",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "identifier": "1611-3349",
        "identifierType": "ISSN",
        "title": "Lecture Notes in Computer Science",
        "firstPage": "499",
        "lastPage": "508",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_posted_content():
    "posted content"
    string = "https://doi.org/10.1101/097196"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1101/097196"
    assert subject.type == "Article"
    assert subject.url == "http://biorxiv.org/lookup/doi/10.1101/097196"
    assert subject.titles[0] == {
        "title": "A Data Citation Roadmap for Scholarly Data Repositories"
    }
    assert len(subject.creators) == 11
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Martin",
        "familyName": "Fenner",
        "nameIdentifiers": [
            {
                "nameIdentifier": "https://orcid.org/0000-0003-1419-2405",
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        ],
    }
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates[0] == {"date": "2016-12-29", "dateType": "Issued"}
    assert subject.publication_year == 2016
    assert subject.publisher == "Cold Spring Harbor Laboratory"
    assert len(subject.references) == 26
    assert subject.references[0] == {
        "key": "2019071613381284000_097196v2.1",
        "title": "An introduction to the joint principles for data citation",
        "publicationYear": "2015",
        "volume": "41",
        "issue": "3",
        "firstPage": "43",
        "containerTitle": "Bulletin of the American \\ldots",
    }
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
            "This article presents a practical roadmap for scholarly data repositories"
        )
    )
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_peer_review():
    "peer review"
    string = "10.7554/elife.55167.sa2"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.7554/elife.55167.sa2"
    assert subject.type == "Review"
    assert subject.url == "https://elifesciences.org/articles/55167#sa2"
    assert subject.titles[0] == {
        "title": "Author response: SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters"
    }
    assert len(subject.creators) == 8
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Jeremy",
        "familyName": "Magland",
        "nameIdentifiers": [
            {
                "nameIdentifier": "https://orcid.org/0000-0002-5286-4375",
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        ],
        "affiliation": [
            {
                "name": "Center for Computational Mathematics, Flatiron Institute, New York, United States"
            }
        ],
    }
    assert subject.contributors is None
    assert subject.rights == [
        {
            "rights": "Creative Commons Attribution 4.0 International",
            "rightsIdentifier": "cc-by-4.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]
    assert subject.dates == [
        {"date": "2020-04-29", "dateType": "Issued"},
        {"date": "2020-05-19T20:33:37Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2020
    assert subject.publisher == "eLife Sciences Publications, Ltd"
    assert len(subject.references) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_dissertation():
    "dissertation"
    string = "10.14264/uql.2020.791"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.14264/uql.2020.791"
    assert subject.type == "Dissertation"
    assert subject.url == "http://espace.library.uq.edu.au/view/UQ:23a1e74"
    assert subject.titles[0] == {
        "title": "School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers"
    }
    assert len(subject.creators) == 1
    assert subject.creators[0] == {
        "familyName": "Collingwood",
        "givenName": "Patricia Maree",
        "nameType": "Personal",
        "nameIdentifiers": [
            {
                "nameIdentifier": "https://orcid.org/0000-0003-3086-4443",
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        ],
    }
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates[0] == {"date": "2020-06-08", "dateType": "Issued"}
    assert subject.publication_year == 2020
    assert subject.publisher == "University of Queensland Library"
    assert len(subject.references) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_doi_with_sici():
    "doi with sici"
    string = "10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    subject = Metadata(string, via="crossref_xml")
    assert (
        subject.id == "https://doi.org/10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    )
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "http://doi.wiley.com/10.1890/0012-9658(2006)87[2832:TIOPMA]2.0.CO;2"
    )
    assert subject.titles[0].get('title').startswith("THE IMPACT OF PARASITE MANIPULATION AND PREDATOR FORAGING")
    assert len(subject.creators) == 2
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "A.",
        "familyName": "Fenton",
    }
    assert subject.contributors is None
    assert subject.rights == [
        {"rightsUri": "https://doi.wiley.com/10.1002/tdm_license_1.1"}
    ]
    assert subject.dates[0] == {"date": "2006-11", "dateType": "Issued"}
    assert subject.publication_year == 2006
    assert subject.publisher == "Wiley"
    assert len(subject.references) == 39
    assert subject.references[0] == {
        "key": "i0012-9658-87-11-2832-anderson1",
        "doi": "https://doi.org/10.2307/3933",
    }
    assert subject.references[-1] == {
        "key": "i0012-9658-87-11-2832-ydenberg1",
        "unstructured": "R. C. Ydenberg, 1998 .Behavioral decisions about foraging and predator avoidance .Pages343 -378 R. Dukas, editorCognitive ecology: the evolutionary ecology of information processing and decision making University of Chicago Press, Chicago, Illinois, USA.",
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
    assert subject.agency == "Crossref"


def test_doi_with_orcid():
    "doi_with_orcid"
    string = "10.1155/2012/291294"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1155/2012/291294"
    assert subject.type == "JournalArticle"
    assert subject.url == "http://www.hindawi.com/journals/pm/2012/291294"
    assert subject.titles[0] == {
        "title": "Delineating a Retesting Zone Using Receiver Operating Characteristic Analysis on Serial QuantiFERON Tuberculosis Test Results in US Healthcare Workers"
    }
    assert len(subject.creators) == 7
    assert subject.creators[2] == {
        "nameType": "Personal",
        "givenName": "Beatriz",
        "familyName": "Hernandez",
        "affiliation": [
            {
                "name": "War Related Illness and Injury Study Center (WRIISC) and Mental Illness Research Education and Clinical Center (MIRECC), Department of Veterans Affairs, Palo Alto, CA 94304, USA"
            },
            {
                "name": "Department of Psychiatry and Behavioral Sciences, Stanford University School of Medicine, Stanford, CA 94304, USA"
            },
        ],
        "nameIdentifiers": [
            {
                "nameIdentifier": "https://orcid.org/0000-0003-2043-4925",
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        ],
    }
    assert subject.contributors is None
    assert subject.rights == [
        {
            "rights": "Creative Commons Attribution 3.0 Unported",
            "rightsIdentifier": "cc-by-3.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/3.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]
    assert subject.dates[0] == {"date": "2012", "dateType": "Issued"}
    assert subject.publication_year == 2012
    assert subject.publisher == "Hindawi Limited"
    assert len(subject.references) == 27
    assert subject.references[0] == {
        "key": "1",
        "publicationYear": "2009",
        "volume": "179",
        "containerTitle": "American Journal of Respiratory and Critical Care Medicine",
    }
    assert subject.references[-1] == {
        "key": "30",
        "doi": "https://doi.org/10.1378/chest.12-0045",
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
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(". To find a statistically significant separation")
    )
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_date_in_future():
    "date_in_future"
    string = "10.1016/j.ejphar.2015.03.018"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1016/j.ejphar.2015.03.018"
    assert subject.type == "JournalArticle"
    assert (
        subject.url == "https://linkinghub.elsevier.com/retrieve/pii/S0014299915002332"
    )
    assert subject.titles[0] == {
        "title": "Paving the path to HIV neurotherapy: Predicting SIV CNS disease"
    }
    assert len(subject.creators) == 10
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Sarah E.",
        "familyName": "Beck",
    }
    assert subject.contributors is None
    assert subject.rights == [
        {"rightsUri": "https://www.elsevier.com/tdm/userlicense/1.0"}
    ]
    assert subject.dates == [
        {"date": "2015-07", "dateType": "Issued"},
        {"date": "2020-08-31T14:03:39Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2015
    assert subject.publisher == "Elsevier BV"
    assert len(subject.references) == 98
    assert subject.references[0] == {
        "key": "10.1016/j.ejphar.2015.03.018_bib1",
        "creator": "Allen",
        "title": "Characterization of the peptide binding motif of a rhesus MHC class I molecule (Mamu-A*01) that binds an immunodominant CTL epitope from simianimmunodeficiency virus.",
        "publicationYear": "1998",
        "volume": "160",
        "firstPage": "6062",
        "containerTitle": "J. Immunol",
    }
    assert subject.references[-1] == {
        "key": "10.1016/j.ejphar.2015.03.018_bib94",
        "doi": "https://doi.org/10.1111/hiv.12134",
        "creator": "Zoufaly",
        "title": "Immune activation despite suppressive highly active antiretroviral therapy is associated with higher risk of viral blips in HIV-1-infected individuals",
        "publicationYear": "2014",
        "volume": "15",
        "firstPage": "449",
        "containerTitle": "HIV Med.",
    }
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
    assert subject.agency == "Crossref"


def test_vor_with_url():
    "vor_with_url"
    string = "10.1038/hdy.2013.26"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1038/hdy.2013.26"
    assert subject.type == "JournalArticle"
    assert subject.url == "http://www.nature.com/articles/hdy201326"
    assert subject.titles[0] == {
        "title": "Albinism in phylogenetically and geographically distinct populations of Astyanax cavefish arises through the same loss-of-function Oca2 allele"
    }
    assert len(subject.creators) == 2
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "J B",
        "familyName": "Gross",
    }
    assert subject.contributors is None
    assert subject.rights == [{"rightsUri": "https://www.springer.com/tdm"}]
    assert subject.dates == [
        {"date": "2013-04-10", "dateType": "Issued"},
        {"date": "2021-12-02T02:50:35Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2013
    assert subject.publisher == "Springer Science and Business Media LLC"
    assert len(subject.references) == 41
    assert subject.references[0] == {
        "key": "BFhdy201326_CR1",
        "creator": "J Alvarez",
        "publicationYear": "1946",
        "volume": "4",
        "firstPage": "263",
        "containerTitle": "An Esc Nac Cien Biol México",
        "unstructured": "Alvarez J . (1946). Revisión del género Anoptichthys con descipción de una especie nueva (Pisces, Characidae). An Esc Nac Cien Biol México 4: 263–282.",
    }
    assert subject.references[-1] == {
        "key": "BFhdy201326_CR41",
        "doi": "https://doi.org/10.1111/j.1095-8312.2003.00230.x",
        "creator": "H Wilkens",
        "publicationYear": "2003",
        "volume": "80",
        "firstPage": "545",
        "containerTitle": "Biol J Linn Soc",
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
    assert subject.agency == "Crossref"


def test_dataset():
    "dataset"
    string = "10.2210/pdb4hhb/pdb"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.2210/pdb4hhb/pdb"
    assert subject.type == "Component"
    assert subject.url == "https://www.wwpdb.org/pdb?id=pdb_00004hhb"
    assert subject.titles[0] == {
        "title": "THE CRYSTAL STRUCTURE OF HUMAN DEOXYHAEMOGLOBIN AT 1.74 ANGSTROMS RESOLUTION"
    }
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "G.",
        "familyName": "Fermi",
    }
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates == [
        {"date": "1984-07-17", "dateType": "Issued"},
        {"date": "2023-02-07T21:29:26Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 1984
    assert subject.publisher == "Worldwide Protein Data Bank"
    assert len(subject.references) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_component():
    "component"
    string = "10.1371/journal.pmed.0030277.g001"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1371/journal.pmed.0030277.g001"
    assert subject.type == "Component"
    assert subject.url == "https://dx.plos.org/10.1371/journal.pmed.0030277.g001"
    assert subject.titles is None
    assert subject.creators == []
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates[0] == {"date": "2015-10-20", "dateType": "Issued"}
    assert subject.publication_year == 2015
    assert subject.publisher == "Public Library of Science (PLoS)"
    assert len(subject.references) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_dataset_usda():
    "dataset usda"
    string = "10.2737/RDS-2018-0001"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.2737/rds-2018-0001"
    assert subject.type == "Dataset"
    assert subject.url == "https://www.fs.usda.gov/rds/archive/Catalog/RDS-2018-0001"
    assert subject.titles[0] == {"title": "Fledging times of grassland birds"}
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Christine A.",
        "familyName": "Ribic",
        "nameIdentifiers": [
            {
                "nameIdentifier": "https://orcid.org/0000-0003-2583-1778",
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        ],
        "affiliation": [{"name": "U.S. Geological Survey"}],
    }
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates[0] == {"date": "2017-08-09", "dateType": "Issued"}
    assert subject.publication_year == 2017
    assert subject.publisher == "USDA Forest Service"
    assert len(subject.references) == 6
    assert subject.references[-1] == {
        "key": "ref6",
        "doi": "https://doi.org/10.1674/0003-0031-178.1.47",
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
        "type": "Database",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_crossref_xml():
    """crossref.xml"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.7554/elife.01567"


def test_book_chapter():
    "book chapter"
    string = "10.1007/978-3-662-46370-3_13"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1007/978-3-662-46370-3_13"
    assert subject.type == "BookChapter"
    assert subject.url == "https://link.springer.com/10.1007/978-3-662-46370-3_13"
    assert subject.titles[0] == {"title": "Clinical Symptoms and Physical Examinations"}
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Ronald L.",
        "familyName": "Diercks",
    }
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates == [
        {"date": "2015", "dateType": "Issued"},
        {"date": "2023-02-10T08:59:39Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2015
    assert subject.publisher == "Springer Science and Business Media LLC"
    assert len(subject.references) == 22
    assert subject.references[0] == {
        "key": "13_CR1",
        "doi": "https://doi.org/10.1007/s00256-012-1391-8",
        "creator": "KS Ahn",
        "publicationYear": "2012",
        "volume": "41",
        "issue": "10",
        "firstPage": "1301",
        "containerTitle": "Skeletal Radiol",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "title": "Shoulder Stiffness",
        "type": "Book",
        "firstPage": "155",
        "lastPage": "158",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_another_book_chapter():
    "another book chapter"
    string = "10.1007/978-3-319-75889-3_1"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1007/978-3-319-75889-3_1"
    assert subject.type == "BookChapter"
    assert subject.url == "http://link.springer.com/10.1007/978-3-319-75889-3_1"
    assert subject.titles[0] == {
        "title": "Climate Change and Increasing Risk of Extreme Heat"
    }
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Hunter M.",
        "familyName": "Jones",
    }
    assert subject.contributors is None
    assert subject.rights == [{"rightsUri": "https://www.springer.com/tdm"}]
    assert subject.dates[0] == {"date": "2018", "dateType": "Issued"}
    assert subject.publication_year == 2018
    assert subject.publisher == "Springer Science and Business Media LLC"
    assert len(subject.references) == 44
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
    assert subject.agency == "Crossref"


def test_yet_another_book_chapter():
    "yet another book chapter"
    string = "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    assert subject.type == "BookChapter"
    assert (
        subject.url
        == "http://services.igi-global.com/resolvedoi/resolve.aspx?doi=10.4018/978-1-4666-1891-6.ch004"
    )
    assert subject.titles[0] == {
        "title": "Unsupervised and Supervised Image Segmentation Using Graph Partitioning"
    }
    assert subject.creators[0] == {
        "affiliation": [{"name": "Université de Lyon, France"}],
        "nameType": "Personal",
        "givenName": "Charles-Edmond",
        "familyName": "Bichot",
    }
    assert subject.contributors is None
    assert subject.rights is None
    assert subject.dates[0] == {"date": "2012-08-08", "dateType": "Issued"}
    assert subject.publication_year == 2012
    assert subject.publisher == "IGI Global"
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
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Image segmentation is an important research area")
    )
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_missing_creator():
    "missing creator"
    string = "https://doi.org/10.3390/publications6020015"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.3390/publications6020015"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://www.mdpi.com/2304-6775/6/2/15"
    assert subject.titles[0] == {
        "title": "Converting the Literature of a Scientific Field to Open Access through Global Collaboration: The Experience of SCOAP3 in Particle Physics"
    }
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Alexander",
        "familyName": "Kohls",
        "nameIdentifiers": [
            {
                "nameIdentifier": "https://orcid.org/0000-0002-3836-8885",
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        ],
    }
    assert subject.contributors is None
    assert subject.rights == [
        {
            "rights": "Creative Commons Attribution 4.0 International",
            "rightsIdentifier": "cc-by-4.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]
    assert subject.dates == [
        {"date": "2018-04-09", "dateType": "Issued"},
        {"date": "2021-07-22T10:05:05Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2018
    assert subject.publisher == "MDPI AG"
    assert len(subject.references) == 23
    assert subject.references[0] == {
        "key": "ref1",
        "url": "https://council.web.cern.ch/en/content/convention-establishment-european-organization-nuclear-research",
        "unstructured": "CERN Convention for the Establishment of a European Organization for Nuclear Research",
    }
    assert subject.references[-1] == {
        "key": "ref23",
        "url": "http://www.webcitation.org/6xNFQb5iD",
        "unstructured": "SCOAP3 News: APS Joins SCOAP3",
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
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith("Gigantic particle accelerators")
    )
    assert subject.version is None
    assert subject.agency == "Crossref"


def test_book():
    "book"
    string = "https://doi.org/10.1017/9781108348843"
    subject = Metadata(string, via="crossref_xml")
    assert subject.id == "https://doi.org/10.1017/9781108348843"
    assert subject.type == "Book"
    assert (
        subject.url
        == "https://www.cambridge.org/core/product/identifier/9781108348843/type/book"
    )
    assert subject.titles[0] == {"title": "The Politics of the Past in Early China"}
    assert subject.creators[0] == {
        "nameType": "Personal",
        "givenName": "Vincent S.",
        "familyName": "Leung",
    }
    assert subject.contributors is None
    assert subject.rights == [{"rightsUri": "https://www.cambridge.org/core/terms"}]
    assert subject.dates == [
        {"date": "2019-07-01", "dateType": "Issued"},
        {"date": "2022-09-22T13:22:42Z", "dateType": "Updated"},
    ]
    assert subject.publication_year == 2019
    assert subject.publisher == "Cambridge University Press (CUP)"
    assert len(subject.references) == 273
    assert subject.references[0] == {
        "key": "9781108348843#EMT-rl-1_BIBe-r-273",
        "creator": "Qiusheng",
        "title": "Lu Jia de lishi yishi ji qi wenhua yiyi",
        "publicationYear": "1997",
        "volume": "5",
        "firstPage": "67",
        "containerTitle": "Qilu xuekan",
    }
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.agency == "Crossref"
