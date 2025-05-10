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
            {"id": "https://ror.org/019whta54", "name": "University of Lausanne"}
        ],
    }
    assert subject.identifiers == [
        {
            "identifier": "https://openalex.org/W2121398592",
            "identifierType": "OpenAlex",
        },
        {"identifier": "https://doi.org/10.7554/elife.01567", "identifierType": "DOI"},
        {"identifier": "2121398592", "identifierType": "MAG"},
        {
            "identifier": "https://pubmed.ncbi.nlm.nih.gov/24520159",
            "identifierType": "PMID",
        },
        {
            "identifier": "https://www.ncbi.nlm.nih.gov/pmc/articles/3917233",
            "identifierType": "PMCID",
        },
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }

    assert subject.date == {"published": "2014-02-11"}
    assert subject.publisher == {
        "name": "eLife Sciences Publications Ltd",
    }
    assert len(subject.references) == 25
    assert subject.references[0] == {
        "id": "https://doi.org/10.1007/bf00994018",
        "title": "Support-vector networks",
        "publicationYear": 1995,
        "volume": "20",
        "issue": "3",
        "firstPage": "273",
        "lastPage": "297",
    }
    assert subject.relations is None
    assert subject.funding_references == [
        {
            "funderName": "Schweizerischer Nationalfonds zur Förderung der Wissenschaftlichen Forschung",
            "funderIdentifier": "https://ror.org/00yjd3n13",
            "funderIdentifierType": "ROR",
        },
        {
            "funderName": "EMBO",
            "funderIdentifier": "https://ror.org/04wfr2810",
            "funderIdentifierType": "ROR",
        },
        {
            "funderName": "Université de Lausanne",
            "funderIdentifier": "https://ror.org/019whta54",
            "funderIdentifierType": "ROR",
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
    assert subject.titles[0] == {
        "title": "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    }
    assert len(subject.contributors) == 5
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0001-9535-7413",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Markus",
        "familyName": "Ralser",
        "affiliations": [
            {
                "id": "https://ror.org/03ate3e03",
                "name": "Max Planck Institute for Molecular Genetics",
            }
        ],
    }
    assert subject.identifiers == [
        {
            "identifier": "https://openalex.org/W1982728624",
            "identifierType": "OpenAlex",
        },
        {
            "identifier": "https://doi.org/10.1371/journal.pone.0000030",
            "identifierType": "DOI",
        },
        {"identifier": "1982728624", "identifierType": "MAG"},
        {
            "identifier": "https://pubmed.ncbi.nlm.nih.gov/17183658",
            "identifierType": "PMID",
        },
        {
            "identifier": "https://www.ncbi.nlm.nih.gov/pmc/articles/1762313",
            "identifierType": "PMCID",
        },
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {"published": "2006-12-20"}
    assert subject.publisher == {
        "name": "Public Library of Science",
    }
    assert len(subject.references) == 50
    assert subject.references[-1] == {
        "title": "[Glycolytic enzyme defects and neurodegeneration].",
        "publicationYear": 1998,
        "volume": "192",
        "issue": "5",
        "firstPage": "929",
        "lastPage": "45",
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
        "lastPage": "e30",
    }
    assert subject.subjects == [
        {"subject": "Physiology"},
        {"subject": "Surgery"},
        {"subject": "Cell Biology"},
    ]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Triosephosphate isomerase (TPI) deficiency is an autosomal recessive disorder caused by various mutations in the gene encoding the key glycolytic enzyme TPI. A drastic decrease in TPI activity and an increased level of its substrate, dihydroxyacetone phosphate, have been measured in unpurified cell extracts of affected individuals. These observations allowed concluding that the different mutations in the TPI alleles result in catalytically inactive enzymes. However, despite a high occurrence of TPI null alleles within several human populations, the frequency of this disorder is exceptionally rare. In order to address this apparent discrepancy, we generated a yeast model allowing us to perform comparative in vivo analyses of the enzymatic and functional properties of the different enzyme variants. We discovered that the majority of these variants exhibit no reduced catalytic activity per se. Instead, we observed, the dimerization behavior of TPI is influenced by the particular mutations investigated, and by the use of a potential alternative translation initiation site in the TPI gene. Additionally, we demonstrated that the overexpression of the most frequent TPI variant, Glu104Asp, which displays altered dimerization features, results in diminished endogenous TPI levels in mammalian cells. Thus, our results reveal that enzyme deregulation attributable to aberrant dimerization of TPI, rather than direct catalytic inactivation of the enzyme, underlies the pathogenesis of TPI deficiency. Finally, we discovered that yeast cells expressing a TPI variant exhibiting reduced catalytic activity are more resistant against oxidative stress caused by the thiol-oxidizing reagent diamide. This observed advantage might serve to explain the high allelic frequency of TPI null alleles detected among human populations.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
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
    assert subject.titles[0] == {
        "title": "Transcriptional Modulation of Polyamine Metabolism in Fruit Species Under Abiotic and Biotic Stress"
    }
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0001-7552-0164",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Ana Margarida",
        "familyName": "Fortes",
        "affiliations": [
            {"id": "https://ror.org/01c27hj86", "name": "University of Lisbon"}
        ],
    }
    assert subject.identifiers == [
        {
            "identifier": "https://openalex.org/W2955786964",
            "identifierType": "OpenAlex",
        },
        {
            "identifier": "https://doi.org/10.3389/fpls.2019.00816",
            "identifierType": "DOI",
        },
        {"identifier": "2955786964", "identifierType": "MAG"},
        {
            "identifier": "https://pubmed.ncbi.nlm.nih.gov/31333688",
            "identifierType": "PMID",
        },
        {
            "identifier": "https://www.ncbi.nlm.nih.gov/pmc/articles/6614878",
            "identifierType": "PMCID",
        },
    ]
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {
        "published": "2019-07-02",
    }
    assert subject.publisher == {
        "name": "Frontiers Media",
    }
    assert len(subject.references) == 45
    assert subject.references[-1] == {
        "id": "https://doi.org/10.3389/fpls.2018.01010",
        "title": "Osmotic Stress and ABA Affect Immune Response and Susceptibility of Grapevine Berries to Gray Mold by Priming Polyamine Accumulation",
        "publicationYear": 2018,
        "volume": "9",
    }
    assert subject.funding_references == [
        {
            "awardNumber": "CA17111",
            "funderIdentifier": "https://ror.org/01bstzn19",
            "funderIdentifierType": "ROR",
            "funderName": "European Cooperation in Science and Technology",
        }
    ]
    assert subject.container == {
        "identifier": "1664-462X",
        "identifierType": "ISSN",
        "title": "Frontiers in Plant Science",
        "type": "Journal",
        "volume": "10",
    }
    assert subject.subjects == [
        {"subject": "Molecular Biology"},
        {"subject": "Plant Science"},
    ]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Polyamines are growth regulators that have been widely implicated in abiotic and biotic stresses. They are also associated with fruit set, ripening, and regulation of fruit quality-related traits. Modulation of their content confers fruit resilience, with polyamine application generally inhibiting postharvest decay. Changes in the content of free and conjugated polyamines in response to stress are highly dependent on the type of abiotic stress applied or the lifestyle of the pathogen. Recent studies suggest that exogenous application of polyamines or modulation of polyamine content by gene editing can confer tolerance to multiple abiotic and biotic stresses simultaneously. In this review, we explore data on polyamine synthesis and catabolism in fruit related to pre- and postharvest stresses. Studies of mutant plants, priming of stress responses, and treatments with polyamines and polyamine inhibitors indicate that these growth regulators can be manipulated to increase fruit productivity with reduced use of pesticides and therefore, under more sustainable conditions.",
            "type": "Abstract",
        }
    ]
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
            "url": "https://europepmc.org/articles/pmc6614878?pdf=render",
        }
    ]


@pytest.mark.vcr
def test_journal_article_original_language():
    "journal article with original language"
    string = "https://doi.org/10.7600/jspfsm.56.60"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.titles is None
    assert subject.contributors is None
    assert subject.license is None
    assert subject.date == {"published": "2007-01-01"}
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
        "identifierType": "ISSN",
        "title": "Japanese Journal of Physical Fitness and Sports Medicine",
        "type": "Journal",
        "issue": "1",
        "volume": "56",
        "firstPage": "60",
        "lastPage": "60",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
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
    assert subject.titles[0] == {
        "title": "Global distribution of Fabaeformiscandona subacuta: an exotic invasive Ostracoda on the Iberian Peninsula?"
    }
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Andreu",
        "familyName": "Escrivà",
        "affiliations": [
            {"id": "https://ror.org/043nxc105", "name": "Universitat de València"}
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2012-01-01"}
    assert subject.publisher == {
        "name": "Oxford University Press",
    }
    assert len(subject.references) == 40
    assert subject.references[-1] == {"title": "Deleted Work", "publicationYear": 1955}
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "0278-0372",
        "identifierType": "ISSN",
        "title": "Journal of Crustacean Biology",
        "type": "Journal",
        "issue": "6",
        "volume": "32",
        "firstPage": "949",
        "lastPage": "961",
    }
    assert subject.subjects == [
        {"subject": "Paleontology"},
        {"subject": "Atmospheric Science"},
        {"subject": "Nature and Landscape Conservation"},
    ]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Although exotic species of Ostracoda have been recorded from various sites in Europe, none of them have a widespread European distribution. Reviews of existing literature, examination of specimens, and sampling in Spain and Japan has greatly expanded the known distribution of the candonid ostracode Fabaeformiscandona subacuta (Yang, 1982). We herein present new reports of its presence in mainland eastern Asia, Australia, and South America, and we review its distribution on the Iberian Peninsula. Although this species is globally widespread, we hypothesize that it is an invasive species on the Iberian Peninsula in light of the following facts: it is not known from other European countries, its known global distribution is extremely disjunct, it has not been found during palaeo-limnological investigations of European lakes, and on the Iberian Peninsula it is almost exclusively found in artificial, intensely human-impacted habitats, mostly in reservoirs and ricefields.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
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
    assert subject.titles[0] == {
        "title": "Human Body Orientation Estimation in Multiview Scenarios"
    }
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-5958-7243",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Lili",
        "familyName": "Chen",
        "affiliations": [
            {
                "id": "https://ror.org/02kkvpp62",
                "name": "Technical University of Munich",
            }
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2012-01-01"}
    assert subject.publisher == {"name": "Springer Science+Business Media"}
    assert len(subject.references) == 13
    assert subject.references[-1] == {"title": "Deleted Work", "publicationYear": 1955}
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "0302-9743",
        "identifierType": "ISSN",
        "title": "Lecture notes in computer science",
        "type": "BookSeries",
        "firstPage": "499",
        "lastPage": "508",
    }
    assert subject.subjects == [{"subject": "Computer Vision and Pattern Recognition"}]
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
            "url": "https://mediatum.ub.tum.de/doc/1285782/document.pdf",
        }
    ]


@pytest.mark.vcr
def test_posted_content():
    "posted content"
    string = "https://doi.org/10.1101/097196"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1101/097196"
    assert subject.type == "Article"
    assert subject.url == "https://doi.org/10.1101/097196"
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
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date["published"] == "2016-12-28"
    assert subject.publisher == {
        "name": "Cold Spring Harbor Laboratory",
    }
    assert len(subject.references) == 15
    assert subject.references[0] == {
        "id": "https://doi.org/10.17487/rfc2396",
        "title": "Uniform Resource Identifiers (URI): Generic Syntax",
        "publicationYear": 1998,
    }
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "https://www.biorxiv.org",
        "identifierType": "URL",
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
        subject.descriptions[0]
        .get("description")
        .startswith(
            "Abstract This article presents a practical roadmap for scholarly data repositories"
        )
    )
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_blog_post():
    "blog post"
    string = "https://doi.org/10.53731/ybhah-9jy85"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.53731/ybhah-9jy85"
    assert subject.type == "Article"
    assert subject.url == "https://doi.org/10.53731/ybhah-9jy85"
    assert subject.titles[0] == {"title": "The rise of the (science) newsletter"}
    assert len(subject.contributors) == 1
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
    assert subject.date == {"published": "2023-10-04"}
    assert subject.publisher is None
    assert len(subject.references) == 1
    assert subject.references[0] == {
        "id": "https://doi.org/10.1038/d41586-023-02554-0",
        "title": "Thousands of scientists are cutting back on Twitter, seeding angst and uncertainty",
        "publicationYear": 2023,
        "volume": "620",
        "issue": "7974",
        "firstPage": "482",
        "lastPage": "484",
    }
    assert subject.relations is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects == [{"subject": "Sociology and Political Science"}]
    assert subject.language == "en"
    assert (
        subject.descriptions[0]
        .get("description")
        .startswith(
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
    assert subject.titles[0] == {
        "title": "Author response: SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters"
    }
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-5286-4375",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Jeremy F.",
        "familyName": "Magland",
        "affiliations": [
            {"id": "https://ror.org/00sekdz59", "name": "Flatiron Institute"},
            {
                "id": "https://ror.org/0508h6p74",
                "name": "Flatiron Health (United States)",
            },
        ],
    }
    assert subject.identifiers == [
        {
            "identifier": "https://openalex.org/W3027264027",
            "identifierType": "OpenAlex",
        },
        {
            "identifier": "https://doi.org/10.7554/elife.55167.sa2",
            "identifierType": "DOI",
        },
        {
            "identifier": "3027264027",
            "identifierType": "MAG",
        },
    ]
    assert subject.license is None
    assert subject.date == {"published": "2020-04-29"}
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
    assert subject.descriptions == [
        {
            "description": "Article Figures and data Abstract Introduction Results Discussion Materials and methods Data availability References Decision letter Author response Article and author information Metrics Abstract Spike sorting is a crucial step in electrophysiological studies of neuronal activity. While many spike sorting packages are available, there is little consensus about which are most accurate under different experimental conditions. SpikeForest is an open-source and reproducible software suite that benchmarks the performance of automated spike sorting algorithms across an extensive, curated database of ground-truth electrophysiological recordings, displaying results interactively on a continuously-updating website. With contributions from eleven laboratories, our database currently comprises 650 recordings (1.3 TB total size) with around 35,000 ground-truth units. These data include paired intracellular/extracellular recordings and state-of-the-art simulated recordings. Ten of the most popular spike sorting codes are wrapped in a Python package and evaluated on a compute cluster using an automated pipeline. SpikeForest documents community progress in automated spike sorting, and guides neuroscientists to an optimal choice of sorter and parameters for a wide range of probes and brain regions. Introduction Background Direct electrical recording of extracellular potentials (Buzsáki, 2004; Seymour et al., 2017) is one of the most popular modalities for studying neural activity since it is possible to determine, with sub-millisecond time resolution, individual firing events from hundreds (potentially thousands) of cells, and to track the activity of individual neurons over hours or days. Recordings are acquired either from within the living animal (in vivo) or from extracted tissue (ex vivo), at electrodes separated by typically 5–25 µm, with baseline noise on the order of 10 µV RMS and 10–30 kHz sampling rate. Probes for in vivo use—which are usually needle-like to minimize tissue damage during insertion—include microwire monotrodes (Hubel, 1957; Nicolelis et al., 1997), tetrodes (Gray et al., 1995; Harris et al., 2000; Dhawale et al., 2017), and multi-shank probes (with typically 1–4 columns of electrodes per shank) on silicon (Csicsvari et al., 2003; Buzsáki, 2004; Jun et al., 2017b) or polymer (Kuo et al., 2013; Chung et al., 2019) substrates. Multiple such probes are often combined into arrays to cover a larger volume in tandem. For ex vivo use (e.g., explanted retina), planar, two-dimensional multi-electrode arrays (MEAs) are common, allowing channel counts of up to tens of thousands (Eversmann et al., 2003; Litke et al., 2004; Berdondini et al., 2005; Yuan et al., 2016; Tsai et al., 2017). Spike sorting is an essential computational step needed to isolate the activity of individual neurons, or units, within extracellular recordings which combine noisy signals from many neurons. Historically, this procedure has relied on manual steps (Hazan et al., 2006; Prentice et al., 2011; Rossant et al., 2016): putative waveforms crossing an amplitude threshold are visualized in a low-dimensional space (either using peak amplitudes or dimensionality reduction techniques), then clusters are separated by eye. While manual spike sorting is manageable with small numbers of recording channels, the rapid growth in channel counts and data volume in recent years as well as the requirement for reproducibility and objectivity demand automated approaches. Most automated algorithms apply a sequence of steps that include filtering, detection, dimension reduction, and clustering, although these may be combined with (or replaced by) many other approaches such as template matching (Prentice et al., 2011; Pillow et al., 2013; Pachitariu et al., 2016), dictionary learning or basis pursuit (Carlson et al., 2014; Ekanadham et al., 2014), and independent component analysis (Takahashi et al., 2002; Buccino et al., 2018). The past 20 years have seen major efforts to improve these algorithms, with recent work focusing on the challenges arising from probe drift (changing spike waveform shapes), spatiotemporally overlapping spikes, and massive data volumes. We will not attempt a full review here, but instead refer the reader to, for example Fee et al., 1996; Lewicki, 1998; Quiroga, 2012; Einevoll et al., 2012; Rey et al., 2015; Lefebvre et al., 2016; Hennig et al., 2019; Carlson and Carin, 2019. In the last few years, many automated spike sorters have been released and are in wide use. Yet, there is little consensus about which is the best choice for a given probe, brain region and experiment type. Often, decisions are based not on evidence of accuracy or performance but rather on the ease of installation or usage, or historical precedent. Thus, the goals of extracting the highest quality results from experiments and of improving reproducibility across laboratories (Denker et al., 2018; Harris et al., 2016) make objective comparison of the available automated spike sorters a pressing concern. Prior work One approach to assessing spike sorter accuracy is to devise intrinsic quality metrics that are applied to each sorted unit, quantifying, for instance, the feature-space isolation of a cluster of firing events (Pouzat et al., 2002; Schmitzer-Torbert et al., 2005; Hill et al., 2011; Neymotin et al., 2011; Barnett et al., 2016; Chung et al., 2017). Another approach is to use biophysical validation methods such as examining cross-correlograms or discovered place fields (Li et al., 2015; Chung et al., 2017). However, the gold standard, when possible, is to evaluate the sorter by comparing with ground-truth data, that is using recordings where the spike train for one or more units is known a priori. Laboratory acquisition of such recordings is difficult and time-consuming, demanding simultaneous paired extracellular and intra-/juxta-cellular probes (Harris et al., 2000; Franke et al., 2015; Neto et al., 2016; Yger et al., 2018; Allen et al., 2018; Marques-Smith et al., 2018a). Since the number of ground-truth units collected in this way is currently small (one per recording), hybrid recordings (where known synthetic firing events are added to experimental data) (Marre et al., 2012; Steinmetz, 2015; Rossant et al., 2016; Pachitariu et al., 2016; Wouters et al., 2019), and biophysically detailed simulated recordings (Camuñas-Mesa and Quiroga, 2013; Hagen et al., 2015; Gratiy et al., 2018; Buccino and Einevoll, 2019), which can contain 1–2 orders of magnitude more ground-truth units, have also been made available for the purpose of method validation. Recently, such ground-truth data have been used to compare new spike sorting algorithms against preexisting ones (Einevoll et al., 2012; Pachitariu et al., 2016; Chung et al., 2017; Jun et al., 2017a; Lee et al., 2017; Yger et al., 2018). However, the choice of accuracy metrics, sorters, data sets, parameters, and code versions varies among studies, making few of the results reproducible, transparent, or comprehensive enough to be of long-term use for the community. To alleviate these issues, a small number of groups initiated web-facing projects to benchmark spike sorter accuracy, notably G-Node (Franke et al., 2012), a phy hybrid study (Steinmetz, 2015) and spikesortingtest (Mitelut, 2016). To our knowledge, these unmaintained projects are either small-scale snapshots or are only partially realized. Yet, in the related area of calcium imaging, leaderboard-style comparison efforts have been more useful for establishing community benchmarks (Freeman, 2015; Berens et al., 2018). SpikeForest We have addressed the above needs by creating and deploying the SpikeForest software suite. SpikeForest comprises a large database of electrophysiological recordings with ground truth (collected from the community), a parallel processing pipeline that benchmarks the performance of many automated spike sorters, and an interactive website that allows for in-depth exploration of the results. At present, the database includes hundreds of recordings, of the types specified above (paired and state-of-the-art biophysical simulation), contributed by eleven laboratories and containing more than 30,000 ground-truth units. Our pipeline runs the various sorters on the recordings, then finds, for each ground-truth unit, the sorted unit whose firing train is the best match, and finally computes metrics involving the numbers of correct, missing, and false positive spikes. A set of accuracy evaluation metrics are then derived per ground-truth unit for each sorter. By averaging results from many units of a similar recording type, we provide high-level accuracy summaries for each sorter in various experimental settings. In order to understand the failure modes of each sorter, SpikeForest further provides various interactive plots. A central aim of this project is to maximize the transparency and reproducibility of the analyses. To this end, all data—the set of recordings, their ground-truth firings, and firing outputs from all sorters—are available for public download via our Python API. SpikeForest itself is open-source, as are the wrappers to all sorters, the Docker (Merkel, 2014) containers, and all of the parameter settings used in the current study results. In fact, code to rerun any sorting task may be requested via the web interface, and is auto-generated on the fly. Both the code and the formulae (for accuracy, SNR, and other metrics) are documented on the site, with links to the source code repositories. Contribution Our work has three main objectives. The primary goal is to aid neuroscientists in selecting the optimal spike sorting software (and algorithm parameters) for their particular probe, brain region, or application. A second goal is to spur improvements in current and future spike sorting software by providing standardized evaluation criteria. This has already begun to happen as developers of some spike sorting algorithms have already made improvements in direct response to this project. As a byproduct, and in collaboration with the SpikeInterface project (Buccino et al., 2019), we achieve a third objective of providing a software package which enables laboratories to run a suite of many popular, open-source, automatic spike sorters, on their own recordings via a unified Python interface. Results In conjunction with the SpikeInterface project (Buccino et al., 2019), the SpikeForest Python package provides standardized wrappers for the following popular spike sorters: HerdingSpikes2 (Hilgen et al., 2017), IronClust (Jun et al., in preparation), JRCLUST (Jun et al., 2017a), KiloSort (Pachitariu et al., 2016), KiloSort2 (Pachitariu et al., 2019), Klusta (Rossant et al., 2016), MountainSort4 (Chung et al., 2017), SpyKING CIRCUS (Yger et al., 2018), Tridesclous (Garcia and Pouzat, 2019), and WaveClus (Chaure et al., 2018; Quiroga et al., 2004). Details of each of these algorithms are provided in Table 1. Since each of these spike sorters operates within a unique computing environment, we utilize Docker (Merkel, 2014) and Singularity (Kurtzer et al., 2017) containers to rigorously encapsulate the versions and prerequisites for each algorithm, ensuring independent verifiability of results, and circumventing software library conflicts. The electrophysiology recordings (together with ground-truth information) registered in SpikeForest are organized into studies, and studies are then grouped into study sets. Table 1 details all study sets presently in the system. Recordings within a study set share a common origin (e.g., laboratory) and type (e.g., paired), whereas recordings within the same study are associated with very similar simulation parameters or experimental conditions. Table 1 Table of spike sorting algorithms currently included in the SpikeForest analysis. Each algorithm is registered into the system via a Python wrapper. A Docker recipe defines the operating system and environment where the sorter is run. Algorithms with asterisks were updated and optimized using SpikeForest data. For the other algorithms, we used the default or recommended parameters. Sorting algorithmLanguageNotesHerdingSpikes2*PythonDesigned for large-scale, high-density multielectrode arrays. See Hilgen et al., 2017.IronClust*MATLAB and CUDADerived from JRCLUST. See Jun et al., in preparation.JRCLUSTMATLAB and CUDADesigned for high-density silicon probes. See Jun et al., 2017a.KiloSortMATLAB and CUDATemplate matching. See Pachitariu et al., 2016.KiloSort2MATLAB and CUDADerived from KiloSort. See Pachitariu et al., 2019.KlustaPythonExpectation-Maximization masked clustering. See Rossant et al., 2016.MountainSort4Python and C++Density-based clustering via ISO-SPLIT. See Chung et al., 2017.SpyKING CIRCUS*Python and MPIDensity-based clustering and template matching. See Yger et al., 2018.Tridesclous*Python and OpenCLSee Garcia and Pouzat, 2019.WaveClusMATLABSuperparamagnetic clustering. See Chaure et al., 2018; Quiroga et al., 2004. Table 2 Table of study sets currently included in the SpikeForest analysis. Study sets fall into three categories: paired, synthetic, and curated. Each study set comprises one or more studies, which in turn comprise multiple recordings acquired or generated under the same conditions. Study set# Rec. / # Elec. / Dur.Source lab.DescriptionPaired intra/extracellularPAIRED_BOYDEN19 / 32ch / 6-10minE. BoydenSubselected from 64, 128, or 256-ch. probes, mouse cortexPAIRED_CRCNS_HC193 / 4-6ch / 6-12minG. BuzsakiTetrodes or silicon probe (one shank) in rat hippocampusPAIRED_ENGLISH29 / 4-32ch / 1-36minD. EnglishHybrid juxtacellular-Si probe, behaving mouse, various regionsPAIRED_KAMPFF15 / 32ch / 9-20minA. KampffSubselected from 374, 127, or 32-ch. probes, mouse cortexPAIRED_MEA64C_YGER18 / 64ch / 5minO. MarreSubselected from 252-ch. MEA, mouse retinaPAIRED_MONOTRODE100 / 1ch / 5-20minBoyden, Kampff, Marre, BuzsakiSubselected from paired recordings from four labsSimulationSYNTH_BIONET36 / 60ch / 15minAIBSBioNet simulation containing no drift, monotonic drift, and random jumps; used by JRCLUST, IronClustSYNTH_JANELIA60 / 4-64ch / 5-20minM. PachitariuDistributed with KiloSort2, with and without simulated driftSYNTH_MAGLAND80 / 8ch / 10minFlatiron Inst.Synthetic waveforms, Gaussian noise, varying SNR, channel count and unit countSYNTH_MEAREC_NEURONEX60 / 32ch / 10minA. BuccinoSimulated using MEAREC, varying SNR and unit countSYNTH_MEAREC_TETRODE40 / 4ch / 10minA. BuccinoSimulated using MEAREC, varying SNR and unit countSYNTH_MONOTRODE111 / 1ch / 10minQ. QuirogaSimulated by Quiroga lab by mixing averaged real spike waveformsSYNTH_VISAPY6 / 30ch / 5minG. EinevollGenerated using VISAPy simulatorHuman curatedMANUAL_FRANKLAB21 / 4ch / 10-40minL. FrankThree manual curations of the same recordings Each time the collection of spike sorting algorithms and ground-truth datasets are updated, our pipeline, depicted in Figure 1, reruns the ten sorters on the recordings. It then finds, for each ground-truth unit, the sorted unit whose firing train is the best match, and finally computes metrics involving the numbers of correct, missing, and false positive spikes. A set of accuracy evaluation metrics are then derived per ground-truth unit for each sorter and displayed on the website. Figure 1 Download asset Open asset Simplified flow diagram of the SpikeForest analysis pipeline. Each in a collection of spike sorting codes (top) are run on each recording with ground truth (left side) to yield a large matrix of sorting results and accuracy metrics (right). See the section on comparison with ground truth for mathematical notations. Recordings are grouped into 'studies', and those into 'study sets'; these share features such as probe type and laboratory of origin. The web interface summarizes the results table by grouping them into study sets (as in Figure 2), but also allows drilling down to the single study and recording level. Aspects such as extraction of mean waveforms, representative firing events, and computation of per-unit SNR are not shown, for simplicity. Figure 2 Download asset Open asset Main results table from the SpikeForest website showing aggregated results for 10 algorithms applied to 13 registered study sets. The left columns of the table show the average accuracy (see (5)) obtained from averaging over all ground-truth units with SNR above an adjustable threshold, here set to 8. The right columns show the number of ground-truth units with accuracy above an adjustable threshold, here set to 0.8. The first five study sets contain paired recordings with simultaneous extracellular and juxta- or intra-cellular ground truth acquisitions. The next six contain simulations from various software packages. The SYNTH_JANELIA, obtained from Pachitariu et al., 2019, is simulated noise with realistic spike waveforms superimposed at known times. The last study set is a collection of human-curated tetrode data. An asterisk indicates an incomplete (timed out) or failed sorting on a subset of results; in these cases, missing accuracies are imputed using linear regression as described in the Materials and methods. Empty cells correspond to excluded sorter/study set pairs. These results reflect the analysis run of March 23rd, 2020. Web interface The results of the latest SpikeForest analysis may be found at https://spikeforest.flatironinstitute.org and are updated on a regular basis as the ground-truth recordings, sorting algorithms, and sorting parameters are adjusted based on community input. The central element of this web page is the main results matrix (Figure 2) which summarizes results for each sorter listed in Table 1 (using formulae defined later by Equation 5). The average accuracies are mapped to a color scale (heat map), with darker blue indicating higher accuracy, using a nonlinear mapping designed to highlight differences at the upper end. For the average accuracy table on the left, only ground-truth units with SNR above a user-adjustable threshold are included in the average accuracy calculations; the user may then explore interactively the effect of unit amplitude on the sorting accuracies of all sorters. If a sorter either crashes or times out (&gt;1 hr run time) on any recording in a study set, an asterisk is appended to that accuracy result, and the missing values are imputed using linear regression as described in the Materials and methods section (there is also an option to simply exclude the missing data from the calculation). The right table of Figure 2 displays the number of ground truth units with accuracy above a user-adjustable threshold (0.8 by default), regardless of SNR. This latter table may be useful for determining which sorters should be used for applications that benefit from a high yield of accurately sorted units and where the acceptable accuracy threshold is known. The website also allows easy switching between three evaluation metrics (accuracy, precision, and recall) as described in the section on comparison with ground truth. Clicking on any result expands the row into its breakdown across studies. Further breakdowns are possible by clicking on the study names to reveal individual recordings. Clicking on any result brings up a scatter plot of accuracy vs. SNR for each ground-truth unit for that study/sorter pair (e.g., Figure 3, left side). Additional information can then be obtained by clicking on the markers for individual units, revealing individual spike waveforms (e.g., Figure 3, right side). Figure 3 Download asset Open asset Screenshots from the SpikeForest website. (left) Scatter plot of accuracy vs. SNR for each ground-truth unit, for a particular sorter (KiloSort2) and study (a simulated drift dataset from the SYNTH_JANELIA study set). The SNR threshold for the main table calculation is shown as a dashed line, and the user-selected unit is highlighted. Marker area is proportional to the number of events, and the color indicates the particular recording within the study. (right) A subset of spike waveforms (overlaid) corresponding to the selected ground truth unit, in four categories: ground truth, sorted, false negative, and false positive. Parallel operation and run times Since neuroscientist users also need to compare the efficiencies (speeds) of algorithms, we measure total computation time for each algorithm on each study, and provide this as an option for display on the website via a heat map. Run times are measured using our cluster pipeline, which allocates a single core to each sorting job on shared-memory multi-core machines (with GPU resources as needed). Since many jobs thus share I/O and RAM bandwidth on a given node, these cannot be taken as accurate indicators of speeds in ideal, or even typical, laboratory settings. We emphasize that our pipeline has been optimized for generation and updating of the accuracy results, not for speed benchmarking. For these reasons, we will not present run time comparisons in this paper, referring the interested reader to the website. Here we only note that older sorters such as Klusta can be over 30 times slower than more recent GPU-enabled sorters such as KiloSort and IronClust. At present, the total compute time for the 650 recordings and 10 sorters is 380 core hours, yet it takes only 3–4 hr (excluding failing jobs) to complete this analysis when run in parallel on our compute cluster with up to 100–200 jobs running simultaneously (typically 14 jobs per node). Since the system automatically detects which results require updating, the pipeline may be run on a daily basis utilizing minimal compute resources for the usual situation where few (if any) updates are needed. Sorter accuracy comparison results We now draw some initial conclusions about the relative performances of the spike sorters based on the threshold choices in Figure 2. No single spike sorter emerged as the top performer in all study sets, with IronClust, KiloSort2, MountainSort4, and SpyKING CIRCUS each appearing among the most accurate in at least six of the study sets. The higher average accuracy of KiloSort2 over its predecessor KiloSort is evident, especially for paired recordings. However, in synthetic studies, particularly tetrodes, KiloSort finds more units above accuracy 0.8 than KiloSort2. Scatter plots (e.g., Figure 3, left side) show that KiloSort2 can retain high accuracy down to lower SNR than other sorters, but not for all such low-SNR units. While KiloSort2 was among the best performers for six of the study sets, KiloSort and KiloSort2 had higher numbers of crashes than any of the other sorters, including crashing on every one of the SYNTH_VISAPY recordings. It is likely that modifications to sorting parameters could reduce the number of crashes, but attempts so far, including contacting the author, have not yet fixed this problem. In the synthetic datasets, KiloSort2 had the largest number of false positive units (distinct from the false positive rate of a single unit), but this is not currently reported by SpikeForest (see Discussion). IronClust appears among the top average accuracies for eight of the study sets, and is especially strong for the simulated and drifting recordings. For most study sets, IronClust has improved accuracy over its predecessor JRCLUST, and is also improved in terms of speed and reliability (no crashes observed). Although a substantial portion of the development of the IronClust software took place while it had access to the SpikeForest ground truth datasets, the same sorting parameters are used across all studies, limiting the potential for overfitting (see Discussion). MountainSort4 is among the top performers for six of the study sets (based on the average accuracy table) and does particularly well for the low-channel-count datasets (monotrodes and tetrodes). It is not surprising that MountainSort4 is the top performer for MANUAL_FRANKLAB because that data source was used in development of the algorithm (Chung et al., 2017). When considering the left table (average accuracy), SpyKING CIRCUS is among the best sorters for ten study sets. However, it ranks a lot lower in the unit count table on the right of Figure 2. This was an example of a sorter that improved over a period of months as a result of using SpikeForest for benchmarking. HerdingSpikes2 was developed for high-density MEA probes and uses a 2D estimate of the spike location, hence was applied only for recordings with a sufficiently planar electrode array structure (this excluded tetrodes and linear probes). For PAIRED_MEA64C_YGER its performance was similar to other top sorters, but in the other study sets, it was somewhat less accurate. One advantage of HerdingSpikes2 not highlighted in the results table is that it is computationally efficient for large arrays, even without using a GPU. Tridesclous is among the top performers for both MEAREC study sets and for PAIRED_MEA64C_YGER, but had a substantially lower accuracy for most of the other datasets. This algorithm appears to struggle with lower-SNR units. Klusta is substantially less accurate than other sorters in most of the study sets, apart from MANUAL_FRANKLAB where, surprisingly, it found the most units above accuracy 0.8 of any sorter. It also has one of the highest crash/timeout rates. The version of WaveClus used in SpikeForest is only suited for (and only run on) monotrodes; a new version of WaveClus now supports polytrodes, but we have not yet integrated it. We included both paired and synthetic monotrode study sets with studies taken from selected single electrodes of other recordings. Four sorters (HerdingSpikes2, JRCLUST, KiloSort, and KiloSort2) were unable to sort this type of data. Of those that could, MountainSort4 was the most accurate, with accuracies slightly higher than WaveClus. An eleventh algorithm, Yet Another Spike Sorter (YASS) (Lee et al., 2017), was not included in the comparison because, even after considerable effort and reaching out to the authors, its performance was too poor, leading us to suspect an installation or configuration problem. We plan to include YASS in a future version of the analysis. Precision and recall results Depending on the scientific question being asked, researchers may want to place a greater importance on maximizing either precision or recall. Precision is the complement of the false positives rate which corresponds to spikes incorrectly labeled as coming from some true neuron. A low precision (high number of false positives) may result in illusory correlations between units and a potentially false conclusion that the neurons are interacting, or may result in a false correlation between a unit firing and some stimulus or task. A low recall, on the other hand, means a large fraction of the true firing events are missed, causing a general reduction in putative firing rates, and also possibly introducing false correlations. Figure 4 shows aggregated precision and recall scores for the results in the main SpikeForest table, again using the SNR threshold of 8 (keep in mind that conclusions can depend strongly on this threshold). We will not attempt to summarize the entire set of results, only to make two observations. For the paired studies, the sorters that have the highest precisions are IronClust, KiloSort2, MountainSort4, and SpyKING CIRCUS. For the paired and manual studies, precisions are generally a lot lower than recalls, across most sorters. Interestingly, this is not generally true for the synthetic studies (where often the precision is higher than recall), indicating that, despite the sophistication of many of these simulations, they may not yet be duplicating the firing and noise statistics of real-world electrophysiology recordings. Figure 4 Download asset Open asset Results table from the SpikeForest website, similar to the left side of Figure 2 except showing aggregated precision and recall scores rather than accuracy. Precision measures how well the algorithm avoids false positives, whereas recall is the complement of the false negative rate. An asterisk indicates an incomplete (timed out) or failed sorting on a subset of results; in these cases, missing accuracies are imputed using linear regression as described in the Materials and methods. Empty cells correspond to excluded sorter/study set pairs. These results reflect the analysis run of March 23rd, 2020. How well can quality metrics predict accuracy? In addition to informing the selection of a spike sorter, our SpikeForest analysis provides an unprecedented opportunity to compare various quality metrics that can be used to accept or reject sorted units when ground truth is not available (i.e., in a laboratory setting). For each sorter, what is the quality metric (or combination thereof) most predictive of actual accuracy? Figure 5 is based on the SYNTH_JANELIA tetrode study and shows the relationships between ground-truth accuracy and three metrics of the sorted units: SNR, mean firing rate, and inter-spike interval violation rate (ISI-vr) (Hill et al., 2011). The latter is the ratio between the number of refractory period violations (2.5 ms threshold) and the expected number of violations under a Poisson spiking assumption. We observe that these relationships are highly dependent on the spike sorter. For IronClust, the SNR and log ISI-vr are predictive of accuracy, whereas firing rate is much less predictive. For KiloSort and SpyKING CIRCUS, firing rate and SNR are both predictive, but log ISI-vr does not appear to correlate. For KiloSort2 and MountainSort4, firing rate is the only predictive metric of the three. The final column in this plot shows that a linear combination of metrics is a better predictor than any metric alone",
            "type": "Abstract",
        }
    ]
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
    assert subject.titles[0] == {
        "title": "School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers"
    }
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "familyName": "Collingwood",
        "givenName": "Patricia",
        "id": "https://orcid.org/0000-0003-3086-4443",
        "type": "Person",
        "contributorRoles": ["Author"],
    }
    assert subject.license is None
    assert subject.date == {"published": "2020-05-25"}
    assert subject.publisher is None
    assert len(subject.references) == 125
    assert subject.references[0] == {
        "publicationYear": 2000,
        "title": "Finite Mixture Models",
    }
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects == [
        {"subject": "Education"},
        {"subject": "General Health Professions"},
        {"subject": "Clinical Psychology"},
    ]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Across many samples, scholars have observed negative life course correlates of truancy, but the best published evidence demonstrates that truancy prevention efforts have failed to return truant students to acceptable attendance levels. Meanwhile, concerns about the harms arising from truancy policies — including their role in the school to prison pipeline — have been recognised recently in several democratic nations worldwide. Within this context, my study contributes to the truancy prevention science literature nuance that has been lacking, in an effort to assist future truancy prevention efforts and, in time, evidence-based truancy policy. My study employs a life course perspective and draws upon elements of the age-graded theory of informal social control, interactional theory, and the concepts of turning points or snares to argue that truancy is associated with reduced life opportunities \xad— or reduced capability set — as measured by one’s lack of financial independence. But, I argue that truants do not experience worse outcomes than non-truants uniformly; instead, subgroups of truants (and of young people), exist, and these subgroups may help to understand relationships more accurately than comparing the outcomes of “truants” and “non-truants”.&nbsp; In doing so, my thesis explores the as-yet undocumented connection between two “knowns” in the literature: that truancy is a common adolescent behaviour, and that financial assistance is common, during emerging adulthood. I also seek to add granularity to the general concept that “the higher frequency the truancy, the worse the outcomes” by exploring how truanting frequency features in truants who share the same, and who have different, financial assistance pathways; my intention is to explore for the presence of thresholds at which truancy is not harmful.In this study I use a longitudinal panel survey that follows young Australians from age 15 or 16, until they are aged 20 or 21. I observe their truancy in late adolescence and their annual receipt and reliance upon cash transfers received from family and government in the year truancy is measured, and the subsequent five years. I create inverse probability of treatment weights using six empirically important variables — age, gender, ethnic composition, their family situation at 14, mother’s education level, and whether or not their household received government cash transfers in the year prior to the truancy — to reduce any confounding effect of those variables on this study’s results. My results show that about one in every five young people were truant in one year in late adolescence, and almost one-half of those are truanting once or twice in one year. And while Australian statute makes any act of truancy illegal, fines for truancy range widely (from $10 to $11,000), based on the circumstances of the truancy, and state education policies in Australia mostly do not require a response to truancy until a student truants more than six times in one calendar year.My study identified a positive association between truancy and lower financial independence. The nature of this association, however, differs according to the analytic method I used. The first method — cross-sectional analyses exploring truancy’s association with government transfer receipt and reliance at school-leaving age, and at the last year of the observation period — demonstrates that truancy is positively associated with government transfer receipt and reliance at three-years post truancy, but the association fades by five-years post truancy. The second method \xad— longitudinal analyses that identified government transfer receipt and reliance trajectories ignorant of one’s truanting history, and then tested whether one’s level of truancy is associated with one’s trajectory group — leads to the conclusion that truancy is positively associated with being on one of the four identified government cash transfer receipt trajectory groups (those receiving a relatively low, steady dollar value of government cash transfers). Being a truant does not make a person more or less likely to be member of any of the three government transfer reliance trajectory groups. This demonstration illustrates that comparing outcomes by averaging across all non-truants, and all truants, appears to miss important nuance, compared to what I identified from a longitudinal, subgroup-based analysis. I found no association between truancy and a young person’s receipt of cash transfers from friends or family (private cash transfers). However, there are likely too few instances of private cash transfers in my study’s dataset to detect an effect.Finally, I explored what features appeared to discern which truants occupied each government cash transfer trajectory, finding that truants differed on a range of measures within the domains of truanting frequency; pre-truancy social-structural characteristics; timing of engagement in labour force, education, and training; and family and housing features. These results illustrated that truants are a varied group, and — as other results throughout my study demonstrate — truanting frequency may not be the most suitable way to account for that variation. It is true that young people’s truanting frequencies varied across the trajectories, but the differences did not fall in a predictable or expected pattern. That is, the differences across transfer trajectories do not accord with the principle of “the higher frequency the truancy, the worse the outcomes”. I discuss the implications of my study’s results for theory, truancy prevention and intervention science, policy and practice.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
            "url": "https://espace.library.uq.edu.au/view/UQ:23a1e74/s43837034_final_thesis.pdf",
        }
    ]


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
    assert subject.titles[0] == {
        "title": "THE IMPACT OF PARASITE MANIPULATION AND PREDATOR FORAGING BEHAVIOR ON PREDATOR–PREY COMMUNITIES"
    }
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-7676-917X",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Andy",
        "familyName": "Fenton",
        "affiliations": [
            {"id": "https://ror.org/04xs57h96", "name": "University of Liverpool"}
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2006-11-01"}
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
        "firstPage": "2832",
        "identifier": "0012-9658",
        "identifierType": "ISSN",
        "issue": "11",
        "lastPage": "2841",
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
    assert subject.descriptions == [
        {
            "description": "Parasites are known to directly affect their hosts at both the individual and population level. However, little is known about their more subtle, indirect effects and how these may affect population and community dynamics. In particular, trophically transmitted parasites may manipulate the behavior of intermediate hosts, fundamentally altering the pattern of contact between these individuals and their predators. Here, we develop a suite of population dynamic models to explore the impact of such behavioral modifications on the dynamics and structure of the predator-prey community. We show that, although such manipulations do not directly affect the persistence of the predator and prey populations, they can greatly alter the quantitative dynamics of the community, potentially resulting in high amplitude oscillations in abundance. We show that the precise impact of host manipulation depends greatly on the predator's functional response, which describes the predator's foraging efficiency under changing prey availabilities. Even if the parasite is rarely observed within the prey population, such manipulations extend beyond the direct impact on the intermediate host to affect the foraging success of the predator, with profound implications for the structure and stability of the predator-prey community.",
            "type": "Abstract",
        }
    ]
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
            {"id": "https://ror.org/00f54p054", "name": "Stanford University"},
            {
                "id": "https://ror.org/02hd1sz82",
                "name": "Mental Illness Research, Education and Clinical Centers",
            },
        ],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert subject.date == {"published": "2012-01-01"}
    assert subject.publisher == {"name": "Hindawi Publishing Corporation"}
    assert len(subject.references) == 22
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1164/ajrccm-conference.2009.179.1_meetingabstracts.a4101",
        "title": "Diagnosis of Latent Tuberculosis Infection in U.S. Health Care Workers: Reproducibility, Repeatability and 6 Month Follow-Up with Interferon-gamma Release Assays (IGRAs).",
        "publicationYear": 2009,
        "firstPage": "A4101",
        "lastPage": "A4101",
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
    assert subject.subjects == [{"subject": "Microbiology"}]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Objective . To find a statistically significant separation point for the QuantiFERON Gold In-Tube (QFT) interferon gamma release assay that could define an optimal “retesting zone” for use in serially tested low-risk populations who have test “reversions” from initially positive to subsequently negative results. Method . Using receiver operating characteristic analysis (ROC) to analyze retrospective data collected from 3 major hospitals, we searched for predictors of reversion until statistically significant separation points were revealed. A confirmatory regression analysis was performed on an additional sample. Results . In 575 initially positive US healthcare workers (HCWs), 300 (52.2%) had reversions, while 275 (47.8%) had two sequential positive tests. The most statistically significant (Kappa = 0.48, chi-square = 131.0,P&lt;0.001) separation point identified by the ROC for predicting reversion was the tuberculosis antigen minus-nil (TBag-nil) value at 1.11 International Units per milliliter (IU/mL). The second separation point was found at TBag-nil at 0.72 IU/mL (Kappa = 0.16, chi-square = 8.2,P&lt;0.01). The model was validated by the regression analysis of 287 HCWs. Conclusion . Reversion likelihood increases as the TBag-nil approaches the manufacturer's cut-point of 0.35 IU/mL. The most statistically significant separation point between those who test repeatedly positive and those who revert is 1.11 IU/mL. Clinicians should retest low-risk individuals with initial QFT results &lt; 1.11 IU/mL.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
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
    assert subject.titles[0] == {
        "title": "Paving the path to HIV neurotherapy: Predicting SIV CNS disease"
    }
    assert len(subject.contributors) == 10
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-6376-5276",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Sarah E.",
        "familyName": "Beck",
        "affiliations": [
            {"id": "https://ror.org/037zgn354", "name": "Johns Hopkins Medicine"},
            {"id": "https://ror.org/00za53h95", "name": "Johns Hopkins University"},
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2015-04-06"}
    assert subject.publisher == {"name": "Elsevier BV"}
    assert len(subject.references) == 53
    assert subject.references[-1] == {
        "title": "Immunologic and pathologic manifestations of the infection of rhesus monkeys with simian immunodeficiency virus of macaques.",
        "publicationYear": 1990,
        "volume": "3",
        "issue": "11",
        "firstPage": "1023",
        "lastPage": "40",
    }
    assert subject.relations is None
    assert subject.funding_references == [
        {
            "funderName": "National Institutes of Health",
            "funderIdentifier": "https://ror.org/01cwqze88",
            "funderIdentifierType": "ROR",
            "awardNumber": "T32 OD011089",
        },
        {
            "funderName": "National Institutes of Health",
            "funderIdentifier": "https://ror.org/01cwqze88",
            "funderIdentifierType": "ROR",
            "awardNumber": "R01 NS077869",
        },
        {
            "funderName": "National Institutes of Health",
            "funderIdentifier": "https://ror.org/01cwqze88",
            "funderIdentifierType": "ROR",
            "awardNumber": "P40 OD013117",
        },
        {
            "funderName": "National Institutes of Health",
            "funderIdentifier": "https://ror.org/01cwqze88",
            "funderIdentifierType": "ROR",
            "awardNumber": "R01 NS089482",
        },
        {
            "funderName": "National Institutes of Health",
            "funderIdentifier": "https://ror.org/01cwqze88",
            "funderIdentifierType": "ROR",
            "awardNumber": "P01 MH070306",
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
    assert subject.subjects == [
        {"subject": "Virology"},
        {"subject": "Emergency Medicine"},
        {"subject": "Neurology"},
    ]
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
            "url": "https://europepmc.org/articles/pmc4731094?pdf=render",
        }
    ]


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
    assert subject.titles[0] == {
        "title": "Albinism in phylogenetically and geographically distinct populations of Astyanax cavefish arises through the same loss-of-function Oca2 allele"
    }
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-0032-1053",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Joshua B.",
        "familyName": "Gross",
        "affiliations": [
            {"id": "https://ror.org/01e3m7079", "name": "University of Cincinnati"}
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2013-04-10"}
    assert subject.publisher == {"name": "Springer Nature"}
    assert len(subject.references) == 25
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1046/j.1365-294x.2003.01753.x",
        "title": "Genetic divergence between cave and surface populations of <i>Astyanax</i> in Mexico (Characidae, Teleostei)",
        "publicationYear": 2003,
        "volume": "12",
        "issue": "3",
        "firstPage": "699",
        "lastPage": "710",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifier": "0018-067X",
        "identifierType": "ISSN",
        "title": "Heredity",
        "type": "Journal",
        "volume": "111",
        "issue": "2",
        "firstPage": "122",
        "lastPage": "130",
    }
    assert subject.subjects == [
        {"subject": "Global and Planetary Change"},
        {"subject": "Paleontology"},
        {"subject": "Nature and Landscape Conservation"},
    ]
    assert subject.language == "en"
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
            "url": "https://www.nature.com/articles/hdy201326.pdf",
        }
    ]


@pytest.mark.vcr
def test_dataset():
    "dataset"
    string = "10.2210/pdb4hhb/pdb"
    subject = Metadata(string, via="openalex")
    assert subject.is_valid
    assert subject.id is None
    assert subject.type == "Other"
    assert subject.url is None
    assert subject.titles is None
    assert subject.contributors is None
    assert subject.license is None
    assert subject.date is None
    assert subject.publisher is None
    assert subject.references is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files is None


@pytest.mark.vcr
def test_component():
    "component"
    string = "10.1371/journal.pmed.0030277.g001"
    subject = Metadata(string, via="openalex")
    assert subject.id is None
    assert subject.type == "Other"
    assert subject.url is None
    assert subject.titles is None
    assert subject.contributors is None
    assert subject.license is None
    assert subject.date is None
    assert subject.publisher is None
    assert subject.references is None
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.descriptions is None
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
    assert subject.titles[0] == {"title": "Fledging times of grassland birds"}
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-2583-1778",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Christine A.",
        "familyName": "Ribic",
        "affiliations": [
            {
                "id": "https://ror.org/035a68863",
                "name": "United States Geological Survey",
            }
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2017-08-09"}
    assert subject.publisher is None
    assert len(subject.references) == 4
    print(subject.references)
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1674/0003-0031-178.1.47",
        "title": "Grassland Bird Productivity in Warm Season Grass Fields in Southwest Wisconsin",
        "publicationYear": 2017,
        "volume": "178",
        "issue": "1",
        "firstPage": "47",
        "lastPage": "63",
    }
    assert subject.funding_references == [
        {
            "funderIdentifier": "https://ror.org/03zmjc935",
            "funderIdentifierType": "ROR",
            "funderName": "U.S. Forest Service",
        }
    ]
    assert subject.container == {
        "title": "Forest Service Research Data Archive",
        "type": "Repository",
    }
    assert subject.subjects == [
        {"subject": "Ecology"},
        {"subject": "Nature and Landscape Conservation"},
    ]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "This archive contains research data collected and/or funded by Forest Service Research and Development (FS R&amp;D), U.S. Department of "
            "Agriculture. It is a resource for accessing both short and long-term "
            "FS R&amp;D research data, which includes Experimental Forest and "
            "Range data. It is a way to both preserve and share the quality "
            "science of our researchers.",
            "type": "Abstract",
        }
    ]
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
    assert subject.titles[0] == {"title": "Clinical Symptoms and Physical Examinations"}
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0001-9873-208X",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Ron L.",
        "familyName": "Diercks",
        "affiliations": [
            {
                "id": "https://ror.org/03cv38k47",
                "name": "University Medical Center Groningen",
            },
            {"id": "https://ror.org/012p63287", "name": "University of Groningen"},
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2015-01-01"}
    assert subject.publisher == {"name": "Springer Nature"}
    assert len(subject.references) == 19
    assert subject.references[0] == {
        "id": "https://doi.org/10.1016/j.jse.2010.08.023",
        "title": "Current review of adhesive capsulitis",
        "publicationYear": 2010,
        "volume": "20",
        "issue": "3",
        "firstPage": "502",
        "lastPage": "514",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "title": "Springer eBooks",
        "firstPage": "155",
        "lastPage": "158",
    }
    assert subject.subjects == [
        {"subject": "Surgery"},
        {"subject": "Pharmacology"},
        {"subject": "Cell Biology"},
    ]
    assert subject.language == "en"
    assert subject.descriptions is None
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
    assert subject.titles[0] == {
        "title": "Climate Change and Increasing Risk of Extreme Heat"
    }
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0003-4588-3911",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Hunter",
        "familyName": "Jones",
        "affiliations": [
            {
                "id": "https://ror.org/02z5nhe81",
                "name": "National Oceanic and Atmospheric Administration",
            },
            {
                "id": "https://ror.org/02kgve346",
                "name": "NOAA Oceanic and Atmospheric Research",
            },
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2018-01-01"}
    assert subject.publisher == {"name": "Springer International Publishing"}
    assert len(subject.references) == 25
    assert subject.references[0] == {
        "id": "https://doi.org/10.1126/science.1098704",
        "title": "More Intense, More Frequent, and Longer Lasting Heat Waves in the 21st Century",
        "publicationYear": 2004,
        "volume": "305",
        "issue": "5686",
        "firstPage": "994",
        "lastPage": "997",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "BookSeries",
        "title": "SpringerBriefs in medical earth sciences",
        "identifier": "2523-3610",
        "identifierType": "ISSN",
        "firstPage": "1",
        "lastPage": "13",
    }
    assert subject.subjects == [
        {"subject": "Health, Toxicology and Mutagenesis"},
        {"subject": "Physiology"},
    ]
    assert subject.language == "en"
    assert subject.descriptions is None
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
    assert subject.titles == [
        {
            "title": "Unsupervised and Supervised Image Segmentation Using Graph Partitioning"
        }
    ]
    assert subject.contributors[0] == {
        "affiliations": [
            {
                "id": "https://ror.org/029brtt94",
                "name": "Université Claude Bernard Lyon 1",
            }
        ],
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Charles‐Edmond",
        "familyName": "Bichot",
    }
    assert subject.license is None
    assert subject.date == {"published": "2012-08-08"}
    assert subject.publisher == {"name": "IGI Global"}
    assert len(subject.references) == 25
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "title": "IGI Global eBooks",
        "firstPage": "72",
        "lastPage": "94",
    }
    assert subject.subjects == [{"subject": "Computer Vision and Pattern Recognition"}]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Image segmentation is an important research area in computer vision and its applications in different disciplines, such as medicine, are of great importance. It is often one of the very first steps of computer vision or pattern recognition methods. This is because segmentation helps to locate objects and boundaries into images. The objective of segmenting an image is to partition it into disjoint and homogeneous sets of pixels. When segmenting an image it is natural to try to use graph partitioning, because segmentation and partitioning share the same high-level objective, to partition a set into disjoints subsets. However, when using graph partitioning for segmenting an image, several big questions remain: What is the best way to convert an image into a graph? Or to convert image segmentation objectives into graph partitioning objectives (not to mention what are image segmentation objectives)? What are the best graph partitioning methods and algorithms for segmenting an image? In this chapter, the author tries to answer these questions, both for unsupervised and supervised image segmentation approach, by presenting methods and algorithms and by comparing them.",
            "type": "Abstract",
        }
    ]
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
    assert subject.titles[0] == {
        "title": "Converting the Literature of a Scientific Field to Open Access through Global Collaboration: The Experience of SCOAP3 in Particle Physics"
    }
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0002-3836-8885",
        "type": "Person",
        "affiliations": [
            {
                "id": "https://ror.org/01ggx4157",
                "name": "European Organization for Nuclear Research",
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
    assert subject.publisher == {
        "name": "Multidisciplinary Digital Publishing Institute"
    }
    assert len(subject.references) == 9
    assert subject.references[-1] == {
        "id": "https://doi.org/10.21428/93b40405.a0e5410c",
        "title": "What Is Open Access?",
        "publicationYear": 2012,
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Journal",
        "title": "Publications",
        "firstPage": "15",
        "lastPage": "15",
        "issue": "2",
        "volume": "6",
        "identifier": "2304-6775",
        "identifierType": "ISSN",
    }
    assert subject.subjects == [
        {"subject": "Statistics, Probability and Uncertainty"},
        {"subject": "Information Systems"},
        {"subject": "Information Systems and Management"},
    ]
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
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
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
    assert subject.date == {"published": "2022-12-16"}
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
    assert subject.titles[0] == {
        "title": "A Hamiltonian perspective to the stabilization of systems of two conservation laws"
    }
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0009-0008-5647-4519",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Valérie",
        "familyName": "dos Santos",
        "affiliations": [
            {
                "id": "https://ror.org/03kfjwy31",
                "name": "Automation and Process Engineering Laboratory",
            },
        ],
    }
    assert subject.contributors[2] == {
        "id": "https://orcid.org/0000-0001-6935-1915",
        "contributorRoles": ["Author"],
        "familyName": "Le Gorrec",
        "givenName": "Yann",
        "type": "Person",
        "affiliations": [
            {
                "id": "https://ror.org/004fmxv66",
                "name": "Franche-Comté Électronique Mécanique Thermique et Optique - Sciences et Technologies",
            }
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2009-01-01"}
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
    assert subject.titles[0] == {"title": "The Politics of the Past in Early China"}
    assert subject.contributors[0] == {
        "id": "https://orcid.org/0000-0001-5516-8714",
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Vincent S.",
        "familyName": "Leung",
    }
    assert subject.license is None
    assert subject.publisher is None
    assert len(subject.references) == 95
    assert subject.references[0] == {
        "id": "https://doi.org/10.2307/2928520",
        "title": "Between Memory and History: Les Lieux de Mémoire",
        "publicationYear": 1989,
        "volume": "26",
        "firstPage": "7",
        "lastPage": "24",
    }
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects == [
        {"subject": "Sociology and Political Science"},
        {"subject": "Cultural Studies"},
        {"subject": "Political Science and International Relations"},
    ]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Why did the past matter so greatly in ancient China? How did it matter and to whom? This is an innovative study of how the past was implicated in the long transition of power in early China, as embodied by the decline of the late Bronze Age aristocracy and the rise of empires over the first millenium BCE. Engaging with a wide array of historical materials, including inscriptional records, excavated manuscripts, and transmitted texts, Vincent S. Leung moves beyond the historiographical canon and explores how the past was mobilized as powerful ideological capital in diverse political debate and ethical dialogue. Appeals to the past in early China were more than a matter of cultural attitude, Leung argues, but were rather deliberate ways of articulating political thought and challenging ethical debates during periods of crisis. Significant power lies in the retelling of the past.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert subject.files == [
        {
            "mimeType": "application/pdf",
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
    assert subject.titles == [
        {"title": "Vector Quotient Filters"},
    ]
    assert len(subject.contributors) == 6
    assert subject.contributors[0] == {
        "affiliations": [
            {
                "id": "https://ror.org/02jbv0t02",
                "name": "Lawrence Berkeley National Laboratory",
            },
            {
                "id": "https://ror.org/01an7q238",
                "name": "University of California, Berkeley",
            },
        ],
        "givenName": "Prashant",
        "familyName": "Pandey",
        "type": "Person",
        "id": "https://orcid.org/0000-0001-5576-0320",
        "contributorRoles": ["Author"],
    }
    assert subject.license is None
    assert subject.date == {"published": "2021-06-09"}
    assert subject.publisher is None
    assert len(subject.references) == 25
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1137/s009753970444435x",
        "title": "Balanced Allocations: The Heavily Loaded Case",
        "publicationYear": 2006,
        "volume": "35",
        "issue": "6",
        "firstPage": "1350",
        "lastPage": "1385",
    }
    assert subject.funding_references == [
        {
            "funderName": "National Science Foundation",
            "funderIdentifier": "https://ror.org/021nxhr62",
            "funderIdentifierType": "ROR",
            "awardNumber": "CCF 805476, CCF 822388, CCF 1724745,CCF 1715777, CCF 1637458, IIS 1541613, CRII 1947789, CNS 1408695, CNS 1755615, CCF 1439084, CCF 1725543, CSR 1763680, CCF 1716252, CCF 1617618, CNS 1938709, IIS 1247726, CNS-1938709,CCF-1750472,CCF-1452904,CNS-1763680",
        },
        {
            "funderName": "U.S. Department of Energy",
            "funderIdentifier": "https://ror.org/01bj3aw27",
            "funderIdentifierType": "ROR",
            "awardNumber": "DE-AC02-05CH11231,17-SC-20-SC",
        },
    ]
    assert subject.container == {
        "type": "Proceedings",
        "title": "Proceedings of the 2022 International Conference on Management of Data",
        "firstPage": "1386",
        "lastPage": "1399",
    }
    assert subject.subjects == [{"subject": "Computer Networks and Communications"}]
    assert subject.language == "en"
    assert subject.descriptions == [
        {
            "description": "Today's filters, such as quotient, cuckoo, and Morton, have a trade-off between space and speed; even when moderately full (e.g., 50%-75% full), their performance degrades nontrivially. The result is that today's systems designers are forced to choose between speed and space usage. In this paper, we present the vector quotient filter (VQF). Locally, the VQF is based on Robin Hood hashing, like the quotient filter, but uses power-of-two-choices hashing to reduce the variance of runs, and thus offers consistent, high throughput across load factors. Power-of-two-choices hashing also makes it more amenable to concurrent updates, compared to the cuckoo filter and variants. Finally, the vector quotient filter is designed to exploit SIMD instructions so that all operations have O (1) cost, independent of the size of the filter or its load factor. We show that the vector quotient filter is 2× faster for inserts compared to the Morton filter (a cuckoo filter variant and state-of-the-art for inserts) and has similar lookup and deletion performance as the cuckoo filter (which is fastest for queries and deletes), despite having a simpler design and implementation. The vector quotient filter has minimal performance decline at high load factors, a problem that has plagued modern filters, including quotient, cuckoo, and Morton. Furthermore, we give a thread-safe version of the vector quotient filter and show that insertion throughput scales 3× with four threads compared to a single thread.",
            "type": "Abstract",
        }
    ]
    assert subject.version is None
    assert subject.provider == "OpenAlex"
    assert len(subject.files) == 1
    assert subject.files[0] == {
        "url": "https://dl.acm.org/doi/pdf/10.1145/3448016.3452841",
        "mimeType": "application/pdf",
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
    assert subject.titles == [
        {"title": "Penisverletzung durch eine Moulinette"},
    ]
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "contributorRoles": ["Author"],
        "givenName": "Mike",
        "familyName": "Lehsnau",
        "affiliations": [
            {"id": "https://ror.org/011zjcv36", "name": "Unfallkrankenhaus Berlin"}
        ],
    }
    assert subject.license is None
    assert subject.date == {"published": "2007-04-13"}
    assert subject.publisher == {"name": "Springer Nature"}
    assert len(subject.references) == 19
    assert subject.references[-1] == {
        "id": "https://doi.org/10.1159/000281702",
        "title": "Successful Replantation of a Totally Amputated Penis by Using Microvascular Techniques",
        "publicationYear": 1990,
        "volume": "45",
        "issue": "3",
        "firstPage": "177",
        "lastPage": "180",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Journal",
        "identifier": "0340-2592",
        "identifierType": "ISSN",
        "title": "Der Urologe",
        "volume": "46",
        "issue": "7",
        "firstPage": "776",
        "lastPage": "779",
    }
    assert subject.subjects == [
        {"subject": "Urology"},
        {"subject": "Surgery"},
        {"subject": "Emergency Medicine"},
    ]
    assert subject.language == "de"
    assert subject.descriptions is None
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
