# pylint: disable=invalid-name,too-many-lines
"""Openalex reader tests"""

import pytest

from commonmeta import Metadata
from commonmeta.readers.openalex_reader import (
    get_openalex,
    get_random_openalex_id,
    get_references,
    read_openalex,
)


def vcr_config():
    return {"record_mode": "new_episodes"}


@pytest.mark.vcr
def test_doi_with_data_citation():
    "DOI with data citation"
    string = "10.7554/elife.01567"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"
    assert subject.additional_type == "Article"
    assert subject.url == "https://doi.org/10.7554/elife.01567"
    assert subject.title == 'Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth'
    assert len(subject.contributors) == 5
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Martial",
            "family_name": "Sankar",
            "affiliations": [
                {
                    "id": "https://ror.org/019whta54",
                    "name": "University of Lausanne"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.identifiers == [
        {
            "identifier": "https://openalex.org/W2121398592",
            "identifier_type": "OpenAlex",
        },
        {"identifier": "https://doi.org/10.7554/elife.01567", "identifier_type": "DOI"},
        {
            "identifier": "https://pubmed.ncbi.nlm.nih.gov/24520159",
            "identifier_type": "PMID",
        },
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date_published == '2014-02-11'
    assert subject.publisher == {
        "name": "eLife Sciences Publications Ltd",
    }
    # assert len(subject.references) == 25
    # assert subject.references[0] == {
    #     "id": "https://doi.org/10.1007/bf00994018",
    #     "title": "Support-vector networks",
    #     "publicationYear": 1995,
    #     "volume": "20",
    #     "issue": "3",
    #     "firstPage": "273",
    #     "lastPage": "297",
    # }
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "2050-084X",
        "identifier_type": "ISSN",
        "title": "eLife",
        "type": "Journal",
        "volume": "3",
        "first_page": "e01567",
        "last_page": "e01567",
    }
    assert (
        subject.description.startswith("Among various advantages, their small size makes")
    )
    assert subject.subjects == [{"subject": "Plant Science"}]
    assert subject.language == "en"
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    string = "10.1371/journal.pone.0000030"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://doi.org/10.1371/journal.pone.0000030"
    assert subject.title == 'Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes'
    assert len(subject.contributors) == 5
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-9535-7413",
            "given_name": "Markus",
            "family_name": "Ralser",
            "affiliations": [
                {
                    "id": "https://ror.org/03ate3e03",
                    "name": "Max Planck Institute for Molecular Genetics"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.identifiers == [
        {
            "identifier": "https://openalex.org/W1982728624",
            "identifier_type": "OpenAlex",
        },
        {
            "identifier": "https://doi.org/10.1371/journal.pone.0000030",
            "identifier_type": "DOI",
        },
        {
            "identifier": "https://pubmed.ncbi.nlm.nih.gov/17183658",
            "identifier_type": "PMID",
        },
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == '2006-12-20'
    assert subject.publisher == {
        "name": "Public Library of Science",
    }
    # assert len(subject.references) == 50
    # assert subject.references[-1] == {
    #     "title": "[Glycolytic enzyme defects and neurodegeneration].",
    #     "publicationYear": 1998,
    #     "volume": "192",
    #     "issue": "5",
    #     "firstPage": "929",
    #     "lastPage": "45",
    # }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "1932-6203",
        "identifier_type": "ISSN",
        "title": "PLoS ONE",
        "type": "Journal",
        "issue": "1",
        "volume": "1",
        "first_page": "e30",
        "last_page": "e30",
    }
    assert subject.subjects == [
        {"subject": "Physiology"},
        {"subject": "Surgery"},
        {"subject": "Cell Biology"},
    ]
    assert subject.language == "en"
    assert subject.description == 'Triosephosphate isomerase (TPI) deficiency is an autosomal recessive disorder caused by various mutations in the gene encoding the key glycolytic enzyme TPI. A drastic decrease in TPI activity and an increased level of its substrate, dihydroxyacetone phosphate, have been measured in unpurified cell extracts of affected individuals. These observations allowed concluding that the different mutations in the TPI alleles result in catalytically inactive enzymes. However, despite a high occurrence of TPI null alleles within several human populations, the frequency of this disorder is exceptionally rare. In order to address this apparent discrepancy, we generated a yeast model allowing us to perform comparative in vivo analyses of the enzymatic and functional properties of the different enzyme variants. We discovered that the majority of these variants exhibit no reduced catalytic activity per se. Instead, we observed, the dimerization behavior of TPI is influenced by the particular mutations investigated, and by the use of a potential alternative translation initiation site in the TPI gene. Additionally, we demonstrated that the overexpression of the most frequent TPI variant, Glu104Asp, which displays altered dimerization features, results in diminished endogenous TPI levels in mammalian cells. Thus, our results reveal that enzyme deregulation attributable to aberrant dimerization of TPI, rather than direct catalytic inactivation of the enzyme, underlies the pathogenesis of TPI deficiency. Finally, we discovered that yeast cells expressing a TPI variant exhibiting reduced catalytic activity are more resistant against oxidative stress caused by the thiol-oxidizing reagent diamide. This observed advantage might serve to explain the high allelic frequency of TPI null alleles detected among human populations.'
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mime_type": "application/pdf",
            "url": "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0000030&type=printable",
        }
    ]


@pytest.mark.vcr
def test_journal_article_with_funding():
    "journal article with funding"
    string = "10.3389/fpls.2019.00816"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.3389/fpls.2019.00816"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://doi.org/10.3389/fpls.2019.00816"
    assert subject.title == 'Transcriptional Modulation of Polyamine Metabolism in Fruit Species Under Abiotic and Biotic Stress'
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-7552-0164",
            "given_name": "Ana Margarida",
            "family_name": "Fortes",
            "affiliations": [
                {
                    "id": "https://ror.org/01c27hj86",
                    "name": "University of Lisbon"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.identifiers == [
        {
            "identifier": "https://openalex.org/W2955786964",
            "identifier_type": "OpenAlex",
        },
        {
            "identifier": "https://doi.org/10.3389/fpls.2019.00816",
            "identifier_type": "DOI",
        },
        {
            "identifier": "https://pubmed.ncbi.nlm.nih.gov/31333688",
            "identifier_type": "PMID",
        },
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == '2019-07-02'
    assert subject.publisher == {
        "name": "Frontiers Media",
    }
    # assert len(subject.references) == 45
    # assert subject.references[-1] == {
    #     "id": "https://doi.org/10.3389/fpls.2018.01010",
    #     "title": "Osmotic Stress and ABA Affect Immune Response and Susceptibility of Grapevine Berries to Gray Mold by Priming Polyamine Accumulation",
    #     "publicationYear": 2018,
    #     "volume": "9",
    # }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "1664-462X",
        "identifier_type": "ISSN",
        "title": "Frontiers in Plant Science",
        "type": "Journal",
        "volume": "10",
        "first_page": "816",
        "last_page": "816",
    }
    assert subject.subjects == [
        {"subject": "Molecular Biology"},
        {"subject": "Plant Science"},
    ]
    assert subject.language == "en"
    assert subject.description == 'Polyamines are growth regulators that have been widely implicated in abiotic and biotic stresses. They are also associated with fruit set, ripening, and regulation of fruit quality-related traits. Modulation of their content confers fruit resilience, with polyamine application generally inhibiting postharvest decay. Changes in the content of free and conjugated polyamines in response to stress are highly dependent on the type of abiotic stress applied or the lifestyle of the pathogen. Recent studies suggest that exogenous application of polyamines or modulation of polyamine content by gene editing can confer tolerance to multiple abiotic and biotic stresses simultaneously. In this review, we explore data on polyamine synthesis and catabolism in fruit related to pre- and postharvest stresses. Studies of mutant plants, priming of stress responses, and treatments with polyamines and polyamine inhibitors indicate that these growth regulators can be manipulated to increase fruit productivity with reduced use of pesticides and therefore, under more sustainable conditions.'
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_journal_article_original_language():
    "journal article with original language"
    string = "https://doi.org/10.7600/jspfsm.56.60"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.title is None
    assert subject.contributors == [
        {
            "type": "Person",
            "person": {"given_name": "宮地", "family_name": "元彦"},
            "roles": ["Author"],
        },
        {
            "type": "Person",
            "person": {"given_name": "山元", "family_name": "健太"},
            "roles": ["Author"],
        },
    ]
    assert subject.license is None
    assert subject.date_published == '2007-01-01'
    assert subject.publisher == {
        "name": "Japanese Society Of Physical Fitness And Sports Medicine",
    }
    assert len(subject.references) == 7
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1097/01.hjh.0000226186.83192.93",
        "title": "How to assess arterial compliance in humans",
        "publicationYear": 2006,
        "volume": "24",
        "issue": "6",
        "firstPage": "1009",
        "lastPage": "1012",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "0039-906X",
        "identifier_type": "ISSN",
        "title": "Japanese Journal of Physical Fitness and Sports Medicine",
        "type": "Journal",
        "issue": "1",
        "volume": "56",
        "first_page": "60",
        "last_page": "60",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mime_type": "application/pdf",
            "url": "https://www.jstage.jst.go.jp/article/jspfsm/56/1/56_1_60/_pdf",
        }
    ]


@pytest.mark.vcr
def test_journal_article_with_rdf_for_container():
    "journal article with RDF for container"
    string = "https://doi.org/10.1163/1937240X-00002096"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1163/1937240x-00002096"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://doi.org/10.1163/1937240x-00002096"
    assert subject.title == 'Global distribution of Fabaeformiscandona subacuta: an exotic invasive Ostracoda on the Iberian Peninsula?'
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0009-0003-2694-1191",
            "given_name": "Andreu",
            "family_name": "Escriv\u00e0",
            "affiliations": [
                {
                    "id": "https://ror.org/043nxc105",
                    "name": "Universitat de Val\u00e8ncia"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2012-01-01'
    assert subject.publisher == {
        "name": "Oxford University Press",
    }
    assert len(subject.references) == 37
    assert subject.references[-1] == {
        "id": "https://doi.org/10.3176/biol.1959.1.01",
        "title": "ANDMEID EESTI MAGEVETE KARPV\u00c4HILISTE (OSTRACODA) FAUNA KOHTA",
        "publicationYear": 1959,
        "volume": "8",
        "issue": "1",
        "firstPage": "3",
        "lastPage": "14",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "0278-0372",
        "identifier_type": "ISSN",
        "title": "Journal of Crustacean Biology",
        "type": "Journal",
        "issue": "6",
        "volume": "32",
        "first_page": "949",
        "last_page": "961",
    }
    assert subject.subjects == [
        {"subject": "Paleontology"},
        {"subject": "Atmospheric Science"},
        {"subject": "Nature and Landscape Conservation"},
    ]
    assert subject.language == "en"
    assert subject.description == 'Although exotic species of Ostracoda have been recorded from various sites in Europe, none of them have a widespread European distribution. Reviews of existing literature, examination of specimens, and sampling in Spain and Japan has greatly expanded the known distribution of the candonid ostracode Fabaeformiscandona subacuta (Yang, 1982). We herein present new reports of its presence in mainland eastern Asia, Australia, and South America, and we review its distribution on the Iberian Peninsula. Although this species is globally widespread, we hypothesize that it is an invasive species on the Iberian Peninsula in light of the following facts: it is not known from other European countries, its known global distribution is extremely disjunct, it has not been found during palaeo-limnological investigations of European lakes, and on the Iberian Peninsula it is almost exclusively found in artificial, intensely human-impacted habitats, mostly in reservoirs and ricefields.'
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mime_type": "application/pdf",
            "url": "https://academic.oup.com/jcb/article-pdf/32/6/949/10336473/jcb0949.pdf",
        }
    ]


@pytest.mark.vcr
def test_book_chapter_with_rdf_for_container():
    "book chapter with RDF for container"
    string = "https://doi.org/10.1007/978-3-642-33191-6_49"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-642-33191-6_49"
    assert subject.type == "BookChapter"
    assert subject.url == "https://doi.org/10.1007/978-3-642-33191-6_49"
    assert subject.title == 'Human Body Orientation Estimation in Multiview Scenarios'
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-5958-7243",
            "given_name": "Lili",
            "family_name": "Chen",
            "affiliations": [
                {
                    "id": "https://ror.org/02kkvpp62",
                    "name": "Technical University of Munich"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2012-01-01'
    assert subject.publisher == {"name": "Springer Science+Business Media"}
    assert len(subject.references) == 13
    assert subject.references[-1] == {
        "id": "https://doi.org/10.23919/eusipco43300.2018",
        "title": "2018 26th European Signal Processing Conference (EUSIPCO)",
        "publicationYear": 2018,
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "0302-9743",
        "identifier_type": "ISSN",
        "title": "Lecture notes in computer science",
        "type": "BookSeries",
        "first_page": "499",
        "last_page": "508",
    }
    assert subject.subjects == [{"subject": "Computer Vision and Pattern Recognition"}]
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_posted_content():
    "posted content"
    string = "https://doi.org/10.1101/097196"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1101/097196"
    assert subject.type == "Article"
    assert subject.url == "https://doi.org/10.1101/097196"
    assert subject.title == 'A Data Citation Roadmap for Scholarly Data Repositories'
    assert len(subject.contributors) == 11
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "given_name": "Martin",
            "family_name": "Fenner",
            "affiliations": [{"id": "https://ror.org/04wxnsj81", "name": "DataCite"}],
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == "2016-12-28"
    assert subject.publisher == {
        "name": "Cold Spring Harbor Laboratory",
    }
    # assert len(subject.references) == 15
    # assert subject.references[0] == {
    #     "id": "https://doi.org/10.17487/rfc2396",
    #     "title": "Uniform Resource Identifiers (URI): Generic Syntax",
    #     "publicationYear": 1998,
    # }
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Repository",
        "title": "bioRxiv (Cold Spring Harbor Laboratory)",
    }
    assert subject.subjects == [
        {"subject": "Information Systems"},
        {"subject": "Information Systems and Management"},
        {"subject": "Molecular Biology"},
    ]
    assert subject.language == "en"
    assert (
        subject.description.startswith(
            "Abstract This article presents a practical roadmap for scholarly data repositories"
        )
    )
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mime_type": "application/pdf",
            "url": "https://www.biorxiv.org/content/biorxiv/early/2017/10/09/097196.full.pdf",
        }
    ]


@pytest.mark.vcr
def test_blog_post():
    "blog post"
    string = "https://doi.org/10.53731/ybhah-9jy85"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/ybhah-9jy85"
    assert subject.type == "Article"
    assert subject.url == "https://doi.org/10.53731/ybhah-9jy85"
    assert subject.title == 'The rise of the (science) newsletter'
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-1419-2405",
            "given_name": "Martin",
            "family_name": "Fenner",
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == '2023-10-04'
    assert subject.publisher is None
    assert len(subject.references) == 2
    assert subject.references[0] == {
        "id": "https://doi.org/10.1038/d41586-023-02554-0",
        "title": "Thousands of scientists are cutting back on Twitter, seeding angst and uncertainty",
        "publicationYear": 2023,
        "volume": "620",
        "issue": "7974",
        "firstPage": "482",
        "lastPage": "484",
    }
    assert subject.references[1] == {
        "id": "https://doi.org/10.53731/9cdnt-2k006",
        "title": "The Rogue Scholar weekly newsletter launches on Wednesday",
        "publicationYear": 2023,
    }
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects == [{"subject": "Sociology and Political Science"}]
    assert subject.language == "en"
    assert (
        subject.description.startswith(
            "Newsletters have been around forever, but their popularity has significantly increased in the past few years"
        )
    )
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_peer_review():
    "peer review"
    string = "10.7554/elife.55167.sa2"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.55167.sa2"
    assert subject.type == "PeerReview"
    assert subject.url == "https://doi.org/10.7554/elife.55167.sa2"
    assert subject.title == 'Author response: SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters'
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-5286-4375",
            "given_name": "Jeremy F.",
            "family_name": "Magland",
            "affiliations": [
                {
                    "id": "https://ror.org/0508h6p74",
                    "name": "Flatiron Health (United States)"
                },
                {
                    "id": "https://ror.org/00sekdz59",
                    "name": "Flatiron Institute"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.identifiers == [
        {
            "identifier": "https://openalex.org/W3027264027",
            "identifier_type": "OpenAlex",
        },
        {
            "identifier": "https://doi.org/10.7554/elife.55167.sa2",
            "identifier_type": "DOI",
        },
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == '2020-04-29'
    assert subject.publisher is None
    assert subject.references is None
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects == [
        {"subject": "Cognitive Neuroscience"},
        {"subject": "Cellular and Molecular Neuroscience"},
    ]
    assert subject.language == "en"
    assert subject.description == "Ten popular spike sorting codes are reproducibly benchmarked for accuracy on electrophysiology datasets from eleven laboratories with interactive web-based exploration of thousands of ground-truth units."
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_dissertation():
    "dissertation"
    string = "10.14264/uql.2020.791"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.14264/uql.2020.791"
    assert subject.type == "Dissertation"
    assert subject.url == "https://doi.org/10.14264/uql.2020.791"
    assert subject.title == 'School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers'
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-3086-4443",
            "given_name": "Patricia",
            "family_name": "Collingwood"
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2020-05-25'
    assert subject.publisher is None
    assert len(subject.references) == 125
    assert subject.references[0] == {
        "id": "https://doi.org/10.1002/0471721182",
        "title": "Finite Mixture Models",
        "publicationYear": 2000,
        "volume": "6",
        "issue": "1",
        "firstPage": "355",
        "lastPage": "378",
    }
    assert subject.funding_references is None
    assert subject.container == {"title": "The University of Queensland", "type": "Repository"}
    assert subject.subjects == [
        {"subject": "Education"},
        {"subject": "General Health Professions"},
        {"subject": "Clinical Psychology"},
    ]
    assert subject.language == "en"
    assert subject.description == 'Across many samples, scholars have observed negative life course correlates of truancy, but the best published evidence demonstrates that truancy prevention efforts have failed to return truant students to acceptable attendance levels. Meanwhile, concerns about the harms arising from truancy policies — including their role in the school to prison pipeline — have been recognised recently in several democratic nations worldwide. Within this context, my study contributes to the truancy prevention science literature nuance that has been lacking, in an effort to assist future truancy prevention efforts and, in time, evidence-based truancy policy. My study employs a life course perspective and draws upon elements of the age-graded theory of informal social control, interactional theory, and the concepts of turning points or snares to argue that truancy is associated with reduced life opportunities \xad— or reduced capability set — as measured by one’s lack of financial independence. But, I argue that truants do not experience worse outcomes than non-truants uniformly; instead, subgroups of truants (and of young people), exist, and these subgroups may help to understand relationships more accurately than comparing the outcomes of “truants” and “non-truants”. In doing so, my thesis explores the as-yet undocumented connection between two “knowns” in the literature: that truancy is a common adolescent behaviour, and that financial assistance is common, during emerging adulthood. I also seek to add granularity to the general concept that “the higher frequency the truancy, the worse the outcomes” by exploring how truanting frequency features in truants who share the same, and who have different, financial assistance pathways; my intention is to explore for the presence of thresholds at which truancy is not harmful.In this study I use a longitudinal panel survey that follows young Australians from age 15 or 16, until they are aged 20 or 21. I observe their truancy in late adolescence and their annual receipt and reliance upon cash transfers received from family and government in the year truancy is measured, and the subsequent five years. I create inverse probability of treatment weights using six empirically important variables — age, gender, ethnic composition, their family situation at 14, mother’s education level, and whether or not their household received government cash transfers in the year prior to the truancy — to reduce any confounding effect of those variables on this study’s results. My results show that about one in every five young people were truant in one year in late adolescence, and almost one-half of those are truanting once or twice in one year. And while Australian statute makes any act of truancy illegal, fines for truancy range widely (from $10 to $11,000), based on the circumstances of the truancy, and state education policies in Australia mostly do not require a response to truancy until a student truants more than six times in one calendar year.My study identified a positive association between truancy and lower financial independence. The nature of this association, however, differs according to the analytic method I used. The first method — cross-sectional analyses exploring truancy’s association with government transfer receipt and reliance at school-leaving age, and at the last year of the observation period — demonstrates that truancy is positively associated with government transfer receipt and reliance at three-years post truancy, but the association fades by five-years post truancy. The second method \xad— longitudinal analyses that identified government transfer receipt and reliance trajectories ignorant of one’s truanting history, and then tested whether one’s level of truancy is associated with one’s trajectory group — leads to the conclusion that truancy is positively associated with being on one of the four identified government cash transfer receipt trajectory groups (those receiving a relatively low, steady dollar value of government cash transfers). Being a truant does not make a person more or less likely to be member of any of the three government transfer reliance trajectory groups. This demonstration illustrates that comparing outcomes by averaging across all non-truants, and all truants, appears to miss important nuance, compared to what I identified from a longitudinal, subgroup-based analysis. I found no association between truancy and a young person’s receipt of cash transfers from friends or family (private cash transfers). However, there are likely too few instances of private cash transfers in my study’s dataset to detect an effect.Finally, I explored what features appeared to discern which truants occupied each government cash transfer trajectory, finding that truants differed on a range of measures within the domains of truanting frequency; pre-truancy social-structural characteristics; timing of engagement in labour force, education, and training; and family and housing features. These results illustrated that truants are a varied group, and — as other results throughout my study demonstrate — truanting frequency may not be the most suitable way to account for that variation. It is true that young people’s truanting frequencies varied across the trajectories, but the differences did not fall in a predictable or expected pattern. That is, the differences across transfer trajectories do not accord with the principle of “the higher frequency the truancy, the worse the outcomes”. I discuss the implications of my study’s results for theory, truancy prevention and intervention science, policy and practice.'
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_doi_with_sici():
    "doi with sici"
    string = "10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert (
        subject.id == "https://doi.org/10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    )
    assert subject.type == "JournalArticle"
    assert subject.additional_type == "Article"
    assert (
        subject.url == "https://doi.org/10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    )
    assert subject.title == 'THE IMPACT OF PARASITE MANIPULATION AND PREDATOR FORAGING BEHAVIOR ON PREDATOR–PREY COMMUNITIES'
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-7676-917X",
            "given_name": "Andy",
            "family_name": "Fenton",
            "affiliations": [
                {
                    "id": "https://ror.org/04xs57h96",
                    "name": "University of Liverpool"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2006-11-01'
    assert subject.publisher == {"name": "Wiley"}
    assert len(subject.references) == 25
    assert subject.references[-1] == {
        "firstPage": "521",
        "id": "https://doi.org/10.1086/284153",
        "issue": "4",
        "lastPage": "541",
        "publicationYear": 1983,
        "title": "Optimal Foraging and the Form of the Predator Isocline",
        "volume": "122",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "first_page": "2832",
        "identifier": "0012-9658",
        "identifier_type": "ISSN",
        "issue": "11",
        "last_page": "2841",
        "title": "Ecology",
        "type": "Journal",
        "volume": "87",
    }
    assert subject.subjects == [
        {"subject": "Genetics"},
        {"subject": "Ecology"},
        {"subject": "Public Health, Environmental and Occupational Health"},
    ]
    assert subject.language == "en"
    assert subject.description == "Parasites are known to directly affect their hosts at both the individual and population level. However, little is known about their more subtle, indirect effects and how these may affect population and community dynamics. In particular, trophically transmitted parasites may manipulate the behavior of intermediate hosts, fundamentally altering the pattern of contact between these individuals and their predators. Here, we develop a suite of population dynamic models to explore the impact of such behavioral modifications on the dynamics and structure of the predator-prey community. We show that, although such manipulations do not directly affect the persistence of the predator and prey populations, they can greatly alter the quantitative dynamics of the community, potentially resulting in high amplitude oscillations in abundance. We show that the precise impact of host manipulation depends greatly on the predator's functional response, which describes the predator's foraging efficiency under changing prey availabilities. Even if the parasite is rarely observed within the prey population, such manipulations extend beyond the direct impact on the intermediate host to affect the foraging success of the predator, with profound implications for the structure and stability of the predator-prey community."
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_doi_with_orcid():
    "doi_with_orcid"
    string = "10.1155/2012/291294"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1155/2012/291294"
    assert subject.type == "JournalArticle"
    assert subject.additional_type == "Article"
    assert subject.url == "https://doi.org/10.1155/2012/291294"
    assert subject.title == 'Delineating a Retesting Zone Using Receiver Operating Characteristic Analysis on Serial QuantiFERON Tuberculosis Test Results in US Healthcare Workers'
    assert len(subject.contributors) == 7
    assert subject.contributors[2] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-2043-4925",
            "given_name": "Beatriz",
            "family_name": "Hernandez",
            "affiliations": [
                {
                    "id": "https://ror.org/02hd1sz82",
                    "name": "Mental Illness Research, Education and Clinical Centers"
                },
                {
                    "id": "https://ror.org/00f54p054",
                    "name": "Stanford University"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == '2012-01-01'
    assert subject.publisher == {"name": "Hindawi Publishing Corporation"}
    assert len(subject.references) == 22
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1086/593965",
        "title": "Does the Implementation of an Interferon-γ Release Assay in Lieu of a Tuberculin Skin Test Increase Acceptance of Preventive Therapy for Latent Tuberculosis Among Healthcare Workers?",
        "publicationYear": 2009,
        "volume": "30",
        "issue": "2",
        "firstPage": "197",
        "lastPage": "199",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "2090-1836",
        "identifier_type": "ISSN",
        "title": "Pulmonary Medicine",
        "type": "Journal",
        "volume": "2012",
        "first_page": "1",
        "last_page": "7",
    }
    assert subject.subjects == [{"subject": "Microbiology"}]
    assert subject.language == "en"
    assert subject.description == 'Objective. To find a statistically significant separation point for the QuantiFERON Gold In-Tube (QFT) interferon gamma release assay that could define an optimal "retesting zone" for use in serially tested low-risk populations who have test "reversions" from initially positive to subsequently negative results. Method. Using receiver operating characteristic analysis (ROC) to analyze retrospective data collected from 3 major hospitals, we searched for predictors of reversion until statistically significant separation points were revealed. A confirmatory regression analysis was performed on an additional sample. Results. In 575 initially positive US healthcare workers (HCWs), 300 (52.2%) had reversions, while 275 (47.8%) had two sequential positive tests. The most statistically significant (Kappa = 0.48, chi-square = 131.0, P &lt; 0.001) separation point identified by the ROC for predicting reversion was the tuberculosis antigen minus-nil (TBag-nil) value at 1.11 International Units per milliliter (IU/mL). The second separation point was found at TBag-nil at 0.72 IU/mL (Kappa = 0.16, chi-square = 8.2, P &lt; 0.01). The model was validated by the regression analysis of 287 HCWs. Conclusion. Reversion likelihood increases as the TBag-nil approaches the manufacturer\'s cut-point of 0.35 IU/mL. The most statistically significant separation point between those who test repeatedly positive and those who revert is 1.11 IU/mL. Clinicians should retest low-risk individuals with initial QFT results &lt; 1.11 IU/mL.'
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mime_type": "application/pdf",
            "url": "https://downloads.hindawi.com/journals/pm/2012/291294.pdf",
        }
    ]


@pytest.mark.vcr
def test_date_in_future():
    "date_in_future"
    string = "10.1016/j.ejphar.2015.03.018"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1016/j.ejphar.2015.03.018"
    assert subject.type == "JournalArticle"
    assert subject.additional_type == "Article"
    assert subject.url == "https://doi.org/10.1016/j.ejphar.2015.03.018"
    assert subject.title == 'Paving the path to HIV neurotherapy: Predicting SIV CNS disease'
    assert len(subject.contributors) == 10
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-6376-5276",
            "given_name": "Sarah E.",
            "family_name": "Beck",
            "affiliations": [
                {
                    "id": "https://ror.org/00za53h95",
                    "name": "Johns Hopkins University"
                },
                {
                    "id": "https://ror.org/037zgn354",
                    "name": "Johns Hopkins Medicine"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2015-04-06'
    assert subject.publisher == {"name": "Elsevier BV"}
    # assert len(subject.references) == 53
    # assert subject.references[-1] == {
    #     "title": "Immunologic and pathologic manifestations of the infection of rhesus monkeys with simian immunodeficiency virus of macaques.",
    #     "publicationYear": 1990,
    #     "volume": "3",
    #     "issue": "11",
    #     "firstPage": "1023",
    #     "lastPage": "40",
    # }
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "0014-2999",
        "identifier_type": "ISSN",
        "title": "European Journal of Pharmacology",
        "type": "Journal",
        "volume": "759",
        "first_page": "303",
        "last_page": "312",
    }
    assert subject.subjects == [
        {"subject": "Virology"},
        {"subject": "Emergency Medicine"},
        {"subject": "Neurology"},
    ]
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_vor_with_url():
    "vor_with_url"
    string = "10.1038/hdy.2013.26"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1038/hdy.2013.26"
    assert subject.type == "JournalArticle"
    assert subject.additional_type == "Article"
    assert subject.url == "https://doi.org/10.1038/hdy.2013.26"
    assert subject.title == 'Albinism in phylogenetically and geographically distinct populations of Astyanax cavefish arises through the same loss-of-function Oca2 allele'
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-0032-1053",
            "given_name": "Joshua B.",
            "family_name": "Gross",
            "affiliations": [
                {
                    "id": "https://ror.org/01e3m7079",
                    "name": "University of Cincinnati"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2013-04-10'
    assert subject.publisher == {"name": "Springer Nature"}
    assert len(subject.references) == 25
    assert subject.references[-1] == {
        "id": "https://doi.org/10.2307/2407352",
        "title": "Genetic Interpretation of Regressive Evolutionary Processes: Studies on Hybrid Eyes of Two Astyanax Cave Populations (Characidae, Pisces)",
        "publicationYear": 1971,
        "volume": "25",
        "issue": "3",
        "firstPage": "530",
        "lastPage": "530",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "0018-067X",
        "identifier_type": "ISSN",
        "title": "Heredity",
        "type": "Journal",
        "volume": "111",
        "issue": "2",
        "first_page": "122",
        "last_page": "130",
    }
    assert subject.subjects == [
        {"subject": "Global and Planetary Change"},
        {"subject": "Paleontology"},
        {"subject": "Nature and Landscape Conservation"},
    ]
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mime_type": "application/pdf",
            "url": "https://www.nature.com/articles/hdy201326.pdf",
        }
    ]


@pytest.mark.vcr
def test_dataset():
    "dataset"
    string = "10.2210/pdb4hhb/pdb"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.2210/pdb4hhb/pdb"
    assert subject.type == "Dataset"
    assert subject.url == "https://doi.org/10.2210/pdb4hhb/pdb"
    assert subject.title == 'THE CRYSTAL STRUCTURE OF HUMAN DEOXYHAEMOGLOBIN AT 1.74 ANGSTROMS RESOLUTION'
    assert subject.contributors == [
        {
            "type": "Person",
            "person": {
                "given_name": "G.",
                "family_name": "Fermi"
            },
            "roles": [
                "Author"
            ]
        },
        {
            "type": "Person",
            "person": {
                "given_name": "M.F.",
                "family_name": "Perutz"
            },
            "roles": [
                "Author"
            ]
        }
    ]
    assert subject.license is None
    assert subject.date_published == '1984-03-07'
    assert subject.publisher is None
    assert subject.references is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_component():
    "component"
    string = "10.1371/journal.pmed.0030277.g001"
    subject = Metadata(string, via="openalex")
    assert subject.id == "https://doi.org/10.1371/journal.pmed.0030277.g001"
    assert subject.type == "Other"
    assert (
        subject.url
        == "https://figshare.com/articles/figure/_Stimulation_of_IL_32_by_Mycobacteria_/628124"
    )
    assert subject.title == 'Stimulation of IL-32 by Mycobacteria'
    assert len(subject.contributors) == 12
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Mihai G",
            "family_name": "Netea"
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == '2015-12-02'
    assert subject.publisher == {"name": "Figshare (United Kingdom)"}
    assert subject.references is None
    assert subject.funding_references is None
    assert subject.container == {"type": "Repository", "title": "Figshare"}
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description == '&lt;div&gt;&lt;p&gt;(A) Whole blood was diluted 1:4 with RPMI and stimulated with 10 μg/ml sonicated M. tuberculosis (MTB) or M. bovis BCG (BCG). Triton X-100 (0.5%) was added 24 h later, and IL-32 concentration was measured by ECL.&lt;/p&gt;\\n &lt;p&gt;(B) Stimulation of freshly isolated PBMCs with various concentrations of LPS or sonicated M. tuberculosis stimulated IL-32 synthesis in a dose-dependent manner.&lt;/p&gt;\\n &lt;p&gt;(C and D) Freshly isolated PBMCs were stimulated with TLR4 (LPS, 100 ng/ml), TLR2 (Pam3Cys, 10 μg/ml), TLR3 (poly I:C, 5 μg/ml), M. tuberculosis, M. bovis BCG, or S. aureus (all at 1 × 10&lt;sup&gt;7&lt;/sup&gt; microorganisms/milliliter, heat-killed). After 24 h of stimulation, LPS-, &lt;i&gt;M. tuberculosis–,&lt;/i&gt; and M. bovis BCG–stimulated production of IL-32 (C) or IL-6 (D) was measured by ECL.&lt;/p&gt;\\n &lt;p&gt;Data are presented as means ± SEM (&lt;i&gt;n =&lt;/i&gt; 8).&lt;/p&gt;&lt;/div&gt;'
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_dataset_usda():
    "dataset usda"
    string = "10.2737/RDS-2018-0001"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.2737/rds-2018-0001"
    assert subject.type == "Dataset"
    assert subject.url == "https://doi.org/10.2737/rds-2018-0001"
    assert subject.title == 'Fledging times of grassland birds'
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-2583-1778",
            "given_name": "Christine A.",
            "family_name": "Ribic",
            "affiliations": [
                {
                    "id": "https://ror.org/035a68863",
                    "name": "United States Geological Survey"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2017-08-09'
    assert subject.publisher is None
    assert len(subject.references) == 4
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1674/0003-0031-178.1.47",
        "title": "Grassland Bird Productivity in Warm Season Grass Fields in Southwest Wisconsin",
        "publicationYear": 2017,
        "volume": "178",
        "issue": "1",
        "firstPage": "47",
        "lastPage": "63",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "title": "Forest Service Research Data Archive",
        "type": "Repository",
    }
    assert subject.subjects == [
        {"subject": "Ecology"},
        {"subject": "Nature and Landscape Conservation"},
    ]
    assert subject.language == "en"
    assert subject.description == 'This archive contains research data collected and/or funded by Forest Service Research and Development (FS R&amp;D), U.S. Department of Agriculture. It is a resource for accessing both short and long-term FS R&amp;D research data, which includes Experimental Forest and Range data. It is a way to both preserve and share the quality science of our researchers.'
    assert subject.version is None
    assert subject.provider == "OpenAlex"


@pytest.mark.vcr
def test_book_chapter():
    "book chapter"
    string = "10.1007/978-3-662-46370-3_13"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-662-46370-3_13"
    assert subject.type == "BookChapter"
    assert subject.url == "https://doi.org/10.1007/978-3-662-46370-3_13"
    assert subject.title == 'Clinical Symptoms and Physical Examinations'
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-9873-208X",
            "given_name": "Ron L.",
            "family_name": "Diercks",
            "affiliations": [
                {
                    "id": "https://ror.org/03cv38k47",
                    "name": "University Medical Center Groningen"
                },
                {
                    "id": "https://ror.org/012p63287",
                    "name": "University of Groningen"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2015-01-01'
    assert subject.publisher is None
    # assert len(subject.references) == 19
    # assert subject.references[0] == {
    #     "id": "https://doi.org/10.1016/j.jse.2010.08.023",
    #     "title": "Current review of adhesive capsulitis",
    #     "publicationYear": 2010,
    #     "volume": "20",
    #     "issue": "3",
    #     "firstPage": "502",
    #     "lastPage": "514",
    # }
    assert subject.funding_references is None
    assert subject.container == {
        "first_page": "155",
        "last_page": "158",
    }
    assert subject.subjects == [
        {"subject": "Surgery"},
        {"subject": "Pharmacology"},
        {"subject": "Cell Biology"},
    ]
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_another_book_chapter():
    "another book chapter"
    string = "10.1007/978-3-319-75889-3_1"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-319-75889-3_1"
    assert subject.type == "BookChapter"
    assert subject.url == "https://doi.org/10.1007/978-3-319-75889-3_1"
    assert subject.title == 'Climate Change and Increasing Risk of Extreme Heat'
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-4588-3911",
            "given_name": "Hunter",
            "family_name": "Jones",
            "affiliations": [
                {
                    "id": "https://ror.org/02kgve346",
                    "name": "NOAA Oceanic and Atmospheric Research"
                },
                {
                    "id": "https://ror.org/02z5nhe81",
                    "name": "National Oceanic and Atmospheric Administration"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2018-01-01'
    assert subject.publisher == {"name": "Springer International Publishing"}
    # assert len(subject.references) == 25
    # assert subject.references[0] == {
    #     "id": "https://doi.org/10.1126/science.1098704",
    #     "title": "More Intense, More Frequent, and Longer Lasting Heat Waves in the 21st Century",
    #     "publicationYear": 2004,
    #     "volume": "305",
    #     "issue": "5686",
    #     "firstPage": "994",
    #     "lastPage": "997",
    # }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "BookSeries",
        "title": "SpringerBriefs in medical earth sciences",
        "identifier": "2523-3610",
        "identifier_type": "ISSN",
        "first_page": "1",
        "last_page": "13",
    }
    assert subject.subjects == [
        {"subject": "Health, Toxicology and Mutagenesis"},
        {"subject": "Physiology"},
    ]
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_yet_another_book_chapter():
    "yet another book chapter"
    string = "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    assert subject.type == "BookChapter"
    assert subject.url == "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    assert subject.title == 'Unsupervised and Supervised Image Segmentation Using Graph Partitioning'
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Charles\u2010Edmond",
            "family_name": "Bichot",
            "affiliations": [
                {
                    "id": "https://ror.org/029brtt94",
                    "name": "Universit\u00e9 Claude Bernard Lyon 1"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2012-08-08'
    assert subject.publisher == {"name": "IGI Global"}
    # assert len(subject.references) == 25
    # assert subject.funding_references is None
    # assert subject.container == {
    #     "type": "Book",
    #     "title": "IGI Global eBooks",
    #     "first_page": "72",
    #     "last_page": "94",
    # }
    assert subject.subjects == [{"subject": "Computer Vision and Pattern Recognition"}]
    assert subject.language == "en"
    assert subject.description == 'Image segmentation is an important research area in computer vision and its applications in different disciplines, such as medicine, are of great importance. It is often one of the very first steps of computer vision or pattern recognition methods. This is because segmentation helps to locate objects and boundaries into images. The objective of segmenting an image is to partition it into disjoint and homogeneous sets of pixels. When segmenting an image it is natural to try to use graph partitioning, because segmentation and partitioning share the same high-level objective, to partition a set into disjoints subsets. However, when using graph partitioning for segmenting an image, several big questions remain: What is the best way to convert an image into a graph? Or to convert image segmentation objectives into graph partitioning objectives (not to mention what are image segmentation objectives)? What are the best graph partitioning methods and algorithms for segmenting an image? In this chapter, the author tries to answer these questions, both for unsupervised and supervised image segmentation approach, by presenting methods and algorithms and by comparing them.'
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_missing_contributor():
    "missing contributor"
    string = "https://doi.org/10.3390/publications6020015"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.3390/publications6020015"
    assert subject.type == "JournalArticle"
    assert subject.additional_type == "Article"
    assert subject.url == "https://doi.org/10.3390/publications6020015"
    assert subject.title == 'Converting the Literature of a Scientific Field to Open Access through Global Collaboration: The Experience of SCOAP3 in Particle Physics'
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-3836-8885",
            "given_name": "Alexander",
            "family_name": "Kohls",
            "affiliations": [
                {
                    "id": "https://ror.org/01ggx4157",
                    "name": "European Organization for Nuclear Research"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == '2018-04-09'
    assert subject.publisher == {
        "name": "Multidisciplinary Digital Publishing Institute"
    }
    assert len(subject.references) == 10
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1038/nphys3862",
        "title": "Keep posting",
        "publicationYear": 2016,
        "volume": "12",
        "issue": "8",
        "firstPage": "719",
        "lastPage": "719",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Journal",
        "title": "Publications",
        "first_page": "15",
        "last_page": "15",
        "issue": "2",
        "volume": "6",
        "identifier": "2304-6775",
        "identifier_type": "ISSN",
    }
    assert subject.subjects == [
        {"subject": "Statistics, Probability and Uncertainty"},
        {"subject": "Information Systems"},
        {"subject": "Information Systems and Management"},
    ]
    assert subject.language == "en"
    assert subject.description == 'Gigantic particle accelerators, incredibly complex detectors, an antimatter factory and the discovery of the Higgs boson—this is part of what makes CERN famous. Only a few know that CERN also hosts the world largest Open Access initiative: SCOAP3. The Sponsoring Consortium for Open Access Publishing in Particle Physics started operation in 2014 and has since supported the publication of 20,000 Open Access articles in the field of particle physics, at no direct cost, nor burden, for individual authors worldwide. SCOAP3 is made possible by a 3000-institute strong partnership, where libraries re-direct funds previously used for subscriptions to ‘flip’ articles to ‘Gold Open Access’. With its recent expansion, the initiative now covers about 90% of the journal literature of the field. This article describes the economic principles of SCOAP3, the collaborative approach of the partnership, and finally summarizes financial results after four years of successful operation.'
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mime_type": "application/pdf",
            "url": "https://www.mdpi.com/2304-6775/6/2/15/pdf?version=1525347674",
        }
    ]


@pytest.mark.vcr
def test_missing_contributor_name():
    "missing contributor name"
    string = "https://doi.org/10.14264/3e10f66"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.14264/3e10f66"
    assert subject.type == "Dissertation"
    assert subject.url == "https://doi.org/10.14264/3e10f66"
    assert subject.title == 'A computational impact analysis approach leveraging non-conforming spatial, temporal and methodological discretisations'
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-5777-3141",
            "given_name": "Peter",
            "family_name": "Wilson"
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2022-12-16'
    assert subject.publisher is None


@pytest.mark.vcr
def test_too_many_contributor_names():
    "too many contributor names"
    string = "https://doi.org/10.3934/nhm.2009.4.249"
    subject = Metadata(string, via="openalex")
    # assert subject.is_valid
    assert subject.id == "https://doi.org/10.3934/nhm.2009.4.249"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://doi.org/10.3934/nhm.2009.4.249"
    assert subject.title == 'A Hamiltonian perspective to thestabilization of systems of two conservation laws'
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0009-0008-5647-4519",
            "given_name": "Val\u00e9rie",
            "family_name": "dos Santos",
            "affiliations": [
                {
                    "id": "https://ror.org/03kfjwy31",
                    "name": "Laboratoire d'Automatique, de Génie des Procédés et de Génie Pharmaceutique"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.contributors[2] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-6935-1915",
            "given_name": "Yann",
            "family_name": "Le Gorrec",
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2009-01-01'
    assert subject.publisher == {"name": "American Institute of Mathematical Sciences"}


@pytest.mark.vcr
def test_book():
    "book"
    string = "https://doi.org/10.1017/9781108348843"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1017/9781108348843"
    assert subject.type == "Book"
    assert subject.url == "https://doi.org/10.1017/9781108348843"
    assert subject.title == 'The Politics of the Past in Early China'
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-5516-8714",
            "given_name": "Vincent S.",
            "family_name": "Leung"
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.publisher == {"name": "Cambridge University Press"}
    assert len(subject.references) == 53
    assert subject.references[0] == {
        "id": "https://doi.org/10.2307/2928520",
        "title": "Between Memory and History: Les Lieux de Mémoire",
        "publicationYear": 1989,
        "volume": "26",
        "firstPage": "7",
        "lastPage": "24",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "title": "Cambridge University Press eBooks",
        "type": "Book",
    }
    assert subject.subjects == [
        {"subject": "Sociology and Political Science"},
        {"subject": "Cultural Studies"},
        {"subject": "Political Science and International Relations"},
    ]
    assert subject.language == "en"
    assert subject.description == 'Why did the past matter so greatly in ancient China? How did it matter and to whom? This is an innovative study of how the past was implicated in the long transition of power in early China, as embodied by the decline of the late Bronze Age aristocracy and the rise of empires over the first millenium BCE. Engaging with a wide array of historical materials, including inscriptional records, excavated manuscripts, and transmitted texts, Vincent S. Leung moves beyond the historiographical canon and explores how the past was mobilized as powerful ideological capital in diverse political debate and ethical dialogue. Appeals to the past in early China were more than a matter of cultural attitude, Leung argues, but were rather deliberate ways of articulating political thought and challenging ethical debates during periods of crisis. Significant power lies in the retelling of the past.'
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mime_type": "application/pdf",
            "url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/64EA64CE425951C77D90340A7F5AE534/9781108425728c1_20-74.pdf/time_out_of_joint.pdf",
        }
    ]


@pytest.mark.vcr
def test_proceedings_article():
    "proceedings article"
    string = "10.1145/3448016.3452841"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1145/3448016.3452841"
    assert subject.type == "ProceedingsArticle"
    assert subject.additional_type == "Article"
    assert subject.url == "https://doi.org/10.1145/3448016.3452841"
    assert subject.title == 'Vector Quotient Filters'
    assert len(subject.contributors) == 6
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0001-5576-0320",
            "given_name": "Prashant",
            "family_name": "Pandey",
            "affiliations": [
                {
                    "id": "https://ror.org/02jbv0t02",
                    "name": "Lawrence Berkeley National Laboratory"
                },
                {
                    "id": "https://ror.org/01an7q238",
                    "name": "University of California, Berkeley"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date_published == '2021-06-09'
    assert subject.publisher is None
    # assert len(subject.references) == 25
    # assert subject.references[-1] == {
    #     "id": "https://doi.org/10.1137/s009753970444435x",
    #     "title": "Balanced Allocations: The Heavily Loaded Case",
    #     "publicationYear": 2006,
    #     "volume": "35",
    #     "issue": "6",
    #     "firstPage": "1350",
    #     "lastPage": "1385",
    # }
    assert subject.funding_references is None
    assert subject.container == {
        "first_page": "1386",
        "last_page": "1399",
    }
    assert subject.subjects == [{"subject": "Computer Networks and Communications"}]
    assert subject.language == "en"
    assert subject.description == "Today's filters, such as quotient, cuckoo, and Morton, have a trade-off between space and speed; even when moderately full (e.g., 50%-75% full), their performance degrades nontrivially. The result is that today's systems designers are forced to choose between speed and space usage. In this paper, we present the vector quotient filter (VQF). Locally, the VQF is based on Robin Hood hashing, like the quotient filter, but uses power-of-two-choices hashing to reduce the variance of runs, and thus offers consistent, high throughput across load factors. Power-of-two-choices hashing also makes it more amenable to concurrent updates, compared to the cuckoo filter and variants. Finally, the vector quotient filter is designed to exploit SIMD instructions so that all operations have O (1) cost, independent of the size of the filter or its load factor. We show that the vector quotient filter is 2× faster for inserts compared to the Morton filter (a cuckoo filter variant and state-of-the-art for inserts) and has similar lookup and deletion performance as the cuckoo filter (which is fastest for queries and deletes), despite having a simpler design and implementation. The vector quotient filter has minimal performance decline at high load factors, a problem that has plagued modern filters, including quotient, cuckoo, and Morton. Furthermore, we give a thread-safe version of the vector quotient filter and show that insertion throughput scales 3× with four threads compared to a single thread."
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert len(subject.files) == 1
    assert subject.files[0] == {
        "url": "https://dl.acm.org/doi/pdf/10.1145/3448016.3452841",
        "mime_type": "application/pdf",
    }


@pytest.mark.vcr
def test_multipe_titles():
    "multiple titles"
    string = "10.1007/s00120-007-1345-2"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/s00120-007-1345-2"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://doi.org/10.1007/s00120-007-1345-2"
    assert subject.title == 'Penisverletzung durch eine Moulinette'
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Mike",
            "family_name": "Lehsnau",
            "affiliations": [
                {
                    "id": "https://ror.org/011zjcv36",
                    "name": "Unfallkrankenhaus Berlin"
                }
            ]
        },
        "roles": [
            "Author"
        ]
    }
    assert subject.license is None
    assert subject.date_published == '2007-04-13'
    assert subject.publisher == {"name": "Springer Nature"}
    # assert len(subject.references) == 19
    # assert subject.references[-1] == {
    #     "id": "https://doi.org/10.1159/000281702",
    #     "title": "Successful Replantation of a Totally Amputated Penis by Using Microvascular Techniques",
    #     "publicationYear": 1990,
    #     "volume": "45",
    #     "issue": "3",
    #     "firstPage": "177",
    #     "lastPage": "180",
    # }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Journal",
        "identifier": "0340-2592",
        "identifier_type": "ISSN",
        "title": "Der Urologe",
        "volume": "46",
        "issue": "7",
        "first_page": "776",
        "last_page": "779",
    }
    assert subject.subjects == [
        {"subject": "Surgery"},
        {"subject": "Urology"},
        {"subject": "Emergency Medicine"},
    ]
    assert subject.language == "de"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_get_random_id_from_openalex():
    """Random works ID from OpenAlex API. Associated ids can be DOI, PMID and/or PMCID."""
    data = get_random_openalex_id()
    assert len(data) == 1
    assert data[0].get("id", None) is not None
    # 5 random DOIs
    data = get_random_openalex_id(5)
    assert len(data) == 5
    assert data[0].get("id", None) is not None


@pytest.mark.vcr
def test_get_openalex():
    """get_openalex"""
    data = get_openalex("https://doi.org/10.1017/9781108348843")
    assert isinstance(data, dict)
    assert data.get("doi") == "https://doi.org/10.1017/9781108348843"


@pytest.mark.vcr
def test_read_openalex():
    """read_openalex"""
    data = get_openalex("https://doi.org/10.1017/9781108348843")
    meta = read_openalex(data)
    assert isinstance(meta, dict)
    assert meta.get("id") == "https://doi.org/10.1017/9781108348843"


def test_get_references():
    """get_references"""
    referenced_works = [
        "https://openalex.org/W1964940342",
        "https://openalex.org/W1969035038",
        "https://openalex.org/W1983780873",
        "https://openalex.org/W1989943932",
        "https://openalex.org/W2004883389",
        "https://openalex.org/W2024237503",
        "https://openalex.org/W2036350498",
        "https://openalex.org/W2062846487",
    ]
    references = get_references(referenced_works)
    assert len(references) == 8
    assert references[0].get("ids") == {
        "doi": "https://doi.org/10.1038/nbt1206-1565",
        "mag": "1964940342",
        "openalex": "https://openalex.org/W1964940342",
        "pmid": "https://pubmed.ncbi.nlm.nih.gov/17160063",
    }
    assert len(get_references([])) == 0
