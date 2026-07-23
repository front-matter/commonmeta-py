# pylint: disable=invalid-name,too-many-lines
"""Crossref XML reader tests"""

from os import path

import pytest

from commonmeta import Metadata


def vcr_config():
    return {"record_mode": "new_episodes"}


@pytest.mark.vcr
def test_doi_with_data_citation():
    "DOI with data citation"
    string = "10.7554/elife.01567"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://elifesciences.org/articles/01567"
    assert (
        subject.title
        == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert len(subject.contributors) == 5
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Martial",
            "family_name": "Sankar",
            "affiliations": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-3.0",
        "title": "Creative Commons Attribution 3.0 Unported",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }
    assert subject.date_published == "2014-02-11"
    assert subject.publisher == {
        "name": "eLife Sciences Publications, Ltd",
    }
    assert len(subject.references) == 27
    assert subject.references[0] == {
        "key": "bib1",
        "id": "https://doi.org/10.1038/nature02100",
        "reference": "APL regulates vascular tissue identity in Arabidopsis",
    }
    assert subject.funding_references == [
        {"funder_name": "SystemsX"},
        {"funder_name": "EMBO longterm post-doctoral fellowships"},
        {"funder_name": "Marie Heim-Voegtlin"},
        {
            "funder_id": "https://doi.org/10.13039/501100006390",
            "funder_name": "University of Lausanne",
        },
    ]
    assert subject.dates == {"submitted": "2013-09-20", "accepted": "2013-12-24"}
    # date_updated keeps the full Crossref timestamp (drifts as the record is
    # re-deposited upstream).
    assert subject.date_updated.startswith("20") and subject.date_updated.endswith("Z")
    assert subject.identifiers == [
        {
            "identifier": "https://doi.org/10.7554/elife.01567",
            "identifier_type": "DOI",
        },
        {"identifier": "e01567", "identifier_type": "Other"},
    ]
    assert subject.archive_locations == ["CLOCKSS"]
    assert subject.relations == [
        {"id": "https://portal.issn.org/resource/ISSN/2050-084X", "type": "IsPartOf"},
        {"id": "https://doi.org/10.5061/dryad.b835k", "type": "IsSupplementedBy"},
    ]
    assert subject.container == {
        "identifiers": [{"identifier": "2050-084X", "identifier_type": "ISSN"}],
        "title": "eLife",
        "type": "Journal",
        "volume": "3",
    }
    assert subject.description.startswith(
        "Among various advantages, their small size makes"
    )
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_journal_article():
    "journal article"
    string = "10.1371/journal.pone.0000030"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pone.0000030"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://dx.plos.org/10.1371/journal.pone.0000030"
    assert (
        subject.title
        == "Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization–Not Catalytic Inactivity–of the Mutant Enzymes"
    )
    assert len(subject.contributors) == 6
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Markus", "family_name": "Ralser"},
        "roles": ["Author"],
    }
    assert subject.contributors[5] == {
        "type": "Person",
        "person": {"given_name": "Guilhem", "family_name": "Janbon"},
        "roles": ["Editor"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert (
        subject.date_published == "2006-12-20"
        and subject.date_updated[:10] == "2021-08-06"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "Public Library of Science (PLoS)",
    }
    assert len(subject.references) == 67
    assert subject.references[0] == {
        "key": "ref1",
        "id": "https://doi.org/10.1056/nejm196502042720503",
        "reference": "Hereditary Hemolytic Anemia with Triosephosphate Isomerase Deficiency.",
        "asserted_by": "Crossref",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifiers": [{"identifier": "1932-6203", "identifier_type": "ISSN"}],
        "title": "PLoS ONE",
        "type": "Journal",
        "issue": "1",
        "volume": "1",
        "first_page": "e30",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_journal_article_with_funding():
    "journal article with funding"
    string = "10.3389/fpls.2019.00816"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.3389/fpls.2019.00816"
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "https://www.frontiersin.org/article/10.3389/fpls.2019.00816/full"
    )
    assert (
        subject.title
        == "Transcriptional Modulation of Polyamine Metabolism in Fruit Species Under Abiotic and Biotic Stress"
    )
    assert len(subject.contributors) == 4
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Ana Margarida", "family_name": "Fortes"},
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert (
        subject.date_published == "2019-07-02"
        and subject.date_updated[:10] == "2019-09-22"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "Frontiers Media SA",
    }
    assert len(subject.references) == 69
    assert subject.references[0] == {
        "key": "ref1",
        "id": "https://doi.org/10.1016/j.plaphy.2013.11.002",
        "reference": "Perturbation of polyamine catabolism affects grape ripening of Vitis vinifera cv. Trincadeira",
    }
    assert subject.funding_references == [
        {
            "funder_id": "https://doi.org/10.13039/501100000921",
            "funder_name": "COST (European Cooperation in Science and Technology)",
            "award_number": "CA17111",
        }
    ]
    assert subject.container == {
        "identifiers": [{"identifier": "1664-462X", "identifier_type": "ISSN"}],
        "title": "Frontiers in Plant Science",
        "type": "Journal",
        "volume": "10",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_journal_article_original_language():
    "journal article with original language"
    string = "https://doi.org/10.7600/jspfsm.56.60"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7600/jspfsm.56.60"
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "https://www.jstage.jst.go.jp/article/jspfsm/56/1/56_1_60/_article/-char/ja/"
    )
    assert subject.title == "自律神経・循環器応答"
    assert subject.contributors is None
    assert subject.license is None
    assert (
        subject.date_published == "2007"
        and subject.date_updated[:10] == "2021-05-20"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "The Japanese Society of Physical Fitness and Sports Medicine",
    }
    assert len(subject.references) == 7
    assert subject.references[0] == {
        "key": "1",
        "id": "https://doi.org/10.1111/j.1469-7793.2000.00407.x",
        "reference": "Seals DR Esler MD J Physiol. 528 : 407-417, 2000",
        "asserted_by": "Crossref",
    }
    assert subject.references[-1] == {
        "key": "7",
        "id": "https://doi.org/10.1161/01.cir.95.6.1686",
        "reference": "Cheitlin MD et al. Circulation 95 : 1686-1744, 1997",
        "asserted_by": "Crossref",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifiers": [{"identifier": "1881-4751", "identifier_type": "ISSN"}],
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
    assert subject.provider == "Crossref"


def test_journal_article_with_rdf_for_container():
    "journal article with RDF for container"
    string = "https://doi.org/10.1163/1937240X-00002096"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1163/1937240x-00002096"
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "https://academic.oup.com/jcb/article-lookup/doi/10.1163/1937240X-00002096"
    )
    assert (
        subject.title
        == "Global distribution of Fabaeformiscandona subacuta: an exotic invasive Ostracoda on the Iberian Peninsula?"
    )
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Francesc", "family_name": "Mesquita-Joanes"},
        "roles": ["Author"],
    }
    assert subject.license is None
    assert (
        subject.date_published == "2012-01-01"
        and subject.date_updated[:10] == "2024-05-01"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "Oxford University Press (OUP)",
    }
    assert len(subject.references) == 45
    assert subject.references[0] == {
        "key": "bibr5",
        "id": "https://doi.org/10.1080/08927014.2001.9522785",
        "reference": "The elusive model of a biological invasion process: time to take differences among aquatic and terrestrial ecosystems into account?",
        "asserted_by": "Crossref",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifiers": [{"identifier": "1937-240X", "identifier_type": "ISSN"}],
        "title": "Journal of Crustacean Biology",
        "type": "Journal",
        "issue": "6",
        "volume": "32",
        "first_page": "949",
        "last_page": "961",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_book_chapter_with_rdf_for_container():
    "book chapter with RDF for container"
    string = "https://doi.org/10.1007/978-3-642-33191-6_49"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-642-33191-6_49"
    assert subject.type == "BookChapter"
    assert subject.url == "http://link.springer.com/10.1007/978-3-642-33191-6_49"
    assert subject.title == "Human Body Orientation Estimation in Multiview Scenarios"
    assert len(subject.contributors) == 3
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Lili", "family_name": "Chen"},
        "roles": ["Author"],
    }
    assert subject.license is None
    assert subject.date_published == "2012"
    assert subject.publisher == {
        "name": "Springer Science and Business Media LLC",
    }
    assert len(subject.references) == 11
    assert subject.references[-1] == {
        "key": "49_CR11",
        "reference": "Griesser, A., Roeck, D.S., Neubeck, A., Van Gool, L.: Gpu-based foreground-background segmentation using an extended colinearity criterion. In: Proc. of Vison, Modeling, and Visualization (VMV), pp. 319–326 (2005)",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "identifiers": [{"identifier": "1611-3349", "identifier_type": "ISSN"}],
        "title": "Lecture Notes in Computer Science",
        "first_page": "499",
        "last_page": "508",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_posted_content():
    "posted content"
    string = "https://doi.org/10.1101/097196"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1101/097196"
    assert subject.type == "Preprint"
    assert subject.url == "http://biorxiv.org/lookup/doi/10.1101/097196"
    assert subject.title == "A Data Citation Roadmap for Scholarly Data Repositories"
    assert len(subject.contributors) == 11
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
    assert subject.date_published == "2016-12-29"
    assert subject.publisher == {
        "name": "openRxiv",
    }
    # the leading structured-only citation (no DOI, no unstructured text) is
    # dropped, so the first surviving reference is the unstructured v2.2 entry.
    assert len(subject.references) == 25
    assert subject.references[0] == {
        "key": "2024080313022960000_097196v2.2",
        "reference": "Altman, M. , &amp; Crosas, M. (2013). The Evolution of Data Citation: From Principles to Implementation. IASSIST Quarterly. Retrieved from http://scholar.harvard.edu/mercecrosas/publications/evolution-data-citation-principles-implementation",
    }
    assert subject.funding_references is None
    assert subject.container == {"type": "Periodical"}
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description.startswith(
        "This article presents a practical roadmap for scholarly data repositories"
    )
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_peer_review():
    "peer review"
    string = "10.7554/elife.55167.sa2"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.55167.sa2"
    assert subject.type == "PeerReview"
    assert subject.url == "https://elifesciences.org/articles/55167v1/peer-reviews"
    assert (
        subject.title
        == "Author response: SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters"
    )
    assert len(subject.contributors) == 8
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-5286-4375",
            "given_name": "Jeremy",
            "family_name": "Magland",
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert (
        subject.date_published == "2020-04-29"
        and subject.date_updated[:10] == "2024-04-26"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "eLife Sciences Publications, Ltd",
    }
    assert len(subject.references) == 0
    assert subject.relations == [
        {"id": "https://doi.org/10.7554/elife.55167", "type": "IsReviewOf"}
    ]
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_dissertation():
    "dissertation"
    string = "10.14264/uql.2020.791"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.14264/uql.2020.791"
    assert subject.type == "Dissertation"
    assert subject.url == "http://espace.library.uq.edu.au/view/UQ:23a1e74"
    assert (
        subject.title
        == "School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers"
    )
    assert len(subject.contributors) == 1
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-3086-4443",
            "given_name": "Patricia Maree",
            "family_name": "Collingwood",
        },
        "roles": ["Author"],
    }
    assert subject.license is None
    assert (
        subject.date_published == "2020-06-08"
        and subject.date_updated[:10] == "2020-06-08"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "University of Queensland Library",
    }
    assert len(subject.references) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_doi_with_sici():
    "doi with sici"
    string = "10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert (
        subject.id == "https://doi.org/10.1890/0012-9658(2006)87[2832:tiopma]2.0.co;2"
    )
    assert subject.type == "JournalArticle"
    assert (
        subject.url
        == "http://doi.wiley.com/10.1890/0012-9658(2006)87[2832:TIOPMA]2.0.CO;2"
    )
    assert subject.title.startswith(
        "THE IMPACT OF PARASITE MANIPULATION AND PREDATOR FORAGING"
    )
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "A.", "family_name": "Fenton"},
        "roles": ["Author"],
    }
    assert subject.license == {"url": "https://doi.wiley.com/10.1002/tdm_license_1.1"}
    assert subject.date_published == "2006-11"
    assert subject.publisher == {
        "name": "Wiley",
    }
    assert len(subject.references) == 39
    assert subject.references[0] == {
        "key": "i0012-9658-87-11-2832-anderson1",
        "id": "https://doi.org/10.2307/3933",
    }
    assert subject.references[-1] == {
        "key": "i0012-9658-87-11-2832-ydenberg1",
        "reference": "R. C. Ydenberg, 1998 .Behavioral decisions about foraging and predator avoidance .Pages343 -378 R. Dukas, editorCognitive ecology: the evolutionary ecology of information processing and decision making University of Chicago Press, Chicago, Illinois, USA.",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "first_page": "2832",
        "identifiers": [{"identifier": "0012-9658", "identifier_type": "ISSN"}],
        "issue": "11",
        "last_page": "2841",
        "title": "Ecology",
        "type": "Journal",
        "volume": "87",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_doi_with_orcid():
    "doi_with_orcid"
    string = "10.1155/2012/291294"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1155/2012/291294"
    assert subject.type == "JournalArticle"
    assert subject.url == "http://www.hindawi.com/journals/pm/2012/291294/"
    assert (
        subject.title
        == "Delineating a Retesting Zone Using Receiver Operating Characteristic Analysis on Serial QuantiFERON Tuberculosis Test Results in US Healthcare Workers"
    )
    assert len(subject.contributors) == 7
    assert subject.contributors[2] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-2043-4925",
            "given_name": "Beatriz",
            "family_name": "Hernandez",
            "affiliations": [
                {
                    "name": "War Related Illness and Injury Study Center (WRIISC) and Mental Illness Research Education and Clinical Center (MIRECC), Department of Veterans Affairs, Palo Alto, CA 94304, USA"
                },
                {
                    "name": "Department of Psychiatry and Behavioral Sciences, Stanford University School of Medicine, Stanford, CA 94304, USA"
                },
            ],
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-3.0",
        "title": "Creative Commons Attribution 3.0 Unported",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }
    assert (
        subject.date_published == "2012"
        and subject.date_updated[:10] == "2016-08-02"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "Wiley",
    }
    # structured-only citations without a DOI or unstructured text are dropped.
    assert len(subject.references) == 17
    assert subject.references[0] == {
        "key": "2",
        "id": "https://doi.org/10.1128/cvi.00168-09",
    }
    assert subject.references[-1] == {
        "key": "30",
        "id": "https://doi.org/10.1378/chest.12-0045",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifiers": [{"identifier": "2090-1844", "identifier_type": "ISSN"}],
        "title": "Pulmonary Medicine",
        "type": "Journal",
        "volume": "2012",
        "first_page": "1",
        "last_page": "7",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description.startswith(
        ". To find a statistically significant separation"
    )
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_date_in_future():
    "date_in_future"
    string = "10.1016/j.ejphar.2015.03.018"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1016/j.ejphar.2015.03.018"
    assert subject.type == "JournalArticle"
    assert (
        subject.url == "https://linkinghub.elsevier.com/retrieve/pii/S0014299915002332"
    )
    assert (
        subject.title
        == "Paving the path to HIV neurotherapy: Predicting SIV CNS disease"
    )
    assert len(subject.contributors) == 10
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Sarah E.", "family_name": "Beck"},
        "roles": ["Author"],
    }
    assert subject.license == {"url": "https://www.elsevier.com/tdm/userlicense/1.0"}
    assert (
        subject.date_published == "2015-07"
        and subject.date_updated[:10] == "2023-08-09"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "Elsevier BV",
    }
    assert len(subject.references) == 89
    assert subject.references[0] == {
        "key": "10.1016/j.ejphar.2015.03.018_bib1",
        "id": "https://doi.org/10.4049/jimmunol.160.12.6062",
        "reference": "Characterization of the peptide binding motif of a rhesus MHC class I molecule (Mamu-A*01) that binds an immunodominant CTL epitope from simianimmunodeficiency virus.",
        "asserted_by": "Crossref",
    }
    assert subject.references[-1] == {
        "key": "10.1016/j.ejphar.2015.03.018_bib94",
        "id": "https://doi.org/10.1111/hiv.12134",
        "reference": "Immune activation despite suppressive highly active antiretroviral therapy is associated with higher risk of viral blips in HIV-1-infected individuals",
        "asserted_by": "Crossref",
    }
    assert subject.funding_references == [
        {
            "funder_id": "https://doi.org/10.13039/100000002",
            "funder_name": "NIH",
            "award_number": "R01 NS089482",
        },
        {
            "funder_id": "https://doi.org/10.13039/100000002",
            "funder_name": "NIH",
            "award_number": "R01 NS077869",
        },
        {
            "funder_id": "https://doi.org/10.13039/100000002",
            "funder_name": "NIH",
            "award_number": "P01 MH070306",
        },
        {
            "funder_id": "https://doi.org/10.13039/100000002",
            "funder_name": "NIH",
            "award_number": "P40 OD013117",
        },
        {
            "funder_id": "https://doi.org/10.13039/100000002",
            "funder_name": "NIH",
            "award_number": "T32 OD011089",
        },
    ]
    assert subject.container == {
        "identifiers": [{"identifier": "0014-2999", "identifier_type": "ISSN"}],
        "title": "European Journal of Pharmacology",
        "type": "Journal",
        "volume": "759",
        "first_page": "303",
        "last_page": "312",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_vor_with_url():
    "vor_with_url"
    string = "10.1038/hdy.2013.26"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1038/hdy.2013.26"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://www.nature.com/articles/hdy201326"
    assert (
        subject.title
        == "Albinism in phylogenetically and geographically distinct populations of Astyanax cavefish arises through the same loss-of-function Oca2 allele"
    )
    assert len(subject.contributors) == 2
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "J B", "family_name": "Gross"},
        "roles": ["Author"],
    }
    assert subject.license == {"url": "https://www.springer.com/tdm"}
    assert (
        subject.date_published == "2013-04-10"
        and subject.date_updated[:10] == "2023-05-18"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "Springer Science and Business Media LLC",
    }
    assert len(subject.references) == 41
    assert subject.references[0] == {
        "key": "BFhdy201326_CR1",
        "reference": "Alvarez J . (1946). Revisión del género Anoptichthys con descipción de una especie nueva (Pisces, Characidae). An Esc Nac Cien Biol México 4: 263–282.",
    }
    assert subject.references[-1] == {
        "key": "BFhdy201326_CR41",
        "id": "https://doi.org/10.1111/j.1095-8312.2003.00230.x",
        "reference": "Wilkens H, Strecker U . (2003). Convergent evolution of the "
        "cavefish Astyanax (Characidae: Teleostei): Genetic evidence "
        "from reduced eye-size and pigmentation. Biol J Linn Soc 80: "
        "545–554.",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "identifiers": [{"identifier": "1365-2540", "identifier_type": "ISSN"}],
        "title": "Heredity",
        "type": "Journal",
        "volume": "111",
        "issue": "2",
        "first_page": "122",
        "last_page": "130",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_dataset():
    "dataset"
    string = "10.2210/pdb4hhb/pdb"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.2210/pdb4hhb/pdb"
    assert subject.type == "Dataset"
    assert subject.url == "https://www.wwpdb.org/pdb?id=pdb_00004hhb"
    assert (
        subject.title
        == "THE CRYSTAL STRUCTURE OF HUMAN DEOXYHAEMOGLOBIN AT 1.74 ANGSTROMS RESOLUTION"
    )
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "G.", "family_name": "Fermi"},
        "roles": ["Author"],
    }
    assert subject.license is None
    assert subject.dates is None
    assert subject.date_published.startswith("2006-01")
    assert subject.date_updated.startswith("2025-05")
    assert subject.publisher == {
        "name": "Worldwide Protein Data Bank",
    }
    assert len(subject.references) == 0
    assert subject.funding_references is None
    assert subject.container == {
        "title": "Worldwide Protein Data Bank",
        "type": "DataRepository",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_component():
    "component"
    string = "10.1371/journal.pmed.0030277.g001"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1371/journal.pmed.0030277.g001"
    assert subject.type == "Component"
    assert subject.url == "https://dx.plos.org/10.1371/journal.pmed.0030277.g001"
    assert subject.title is None
    assert subject.contributors is None
    assert subject.license is None
    assert (
        subject.date_published == "2015-10-20"
        and subject.date_updated[:10] == "2018-10-19"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "Public Library of Science (PLoS)",
    }
    assert len(subject.references) == 0
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_dataset_usda():
    "dataset usda"
    string = "10.2737/RDS-2018-0001"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.2737/rds-2018-0001"
    assert subject.type == "Dataset"
    assert subject.url == "https://www.fs.usda.gov/rds/archive/Catalog/RDS-2018-0001"
    assert subject.title == "Fledging times of grassland birds"
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0003-2583-1778",
            "given_name": "Christine A.",
            "family_name": "Ribic",
            "affiliations": [{"name": "U.S. Geological Survey"}],
        },
        "roles": ["Author"],
    }
    assert subject.license is None
    assert (
        subject.date_published == "2017-08-09"
        and subject.date_updated[:10] == "2021-07-01"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "USDA Forest Service",
    }
    assert len(subject.references) == 5
    assert subject.references[-1] == {
        "key": "ref6",
        "id": "https://doi.org/10.1674/0003-0031-178.1.47",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "title": "Forest Service Research Data Archive",
        "type": "DataRepository",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_crossref_xml():
    """crossref.xml"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.7554/elife.01567"


def test_book_chapter():
    "book chapter"
    string = "10.1007/978-3-662-46370-3_13"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-662-46370-3_13"
    assert subject.type == "BookChapter"
    assert subject.url == "https://link.springer.com/10.1007/978-3-662-46370-3_13"
    assert subject.title == "Clinical Symptoms and Physical Examinations"
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Ronald L.", "family_name": "Diercks"},
        "roles": ["Author"],
    }
    assert subject.license is None
    assert subject.date_published == "2015"
    assert subject.publisher == {
        "name": "Springer Science and Business Media LLC",
    }
    assert len(subject.references) == 22
    assert subject.references[0] == {
        "key": "13_CR1",
        "id": "https://doi.org/10.1007/s00256-012-1391-8",
        "reference": "Ahn KS, Kang CH, Oh YW, Jeong WK. Correlation between magnetic resonance imaging and clinical impairment in patients with adhesive capsulitis. Skeletal Radiol. 2012;41(10):1301–8.",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "title": "Shoulder Stiffness",
        "type": "Book",
        "first_page": "155",
        "last_page": "158",
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_another_book_chapter():
    "another book chapter"
    string = "10.1007/978-3-319-75889-3_1"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1007/978-3-319-75889-3_1"
    assert subject.type == "BookChapter"
    assert subject.url == "http://link.springer.com/10.1007/978-3-319-75889-3_1"
    assert subject.title == "Climate Change and Increasing Risk of Extreme Heat"
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Hunter M.", "family_name": "Jones"},
        "roles": ["Author"],
    }
    assert subject.license == {"url": "https://www.springer.com/tdm"}
    assert subject.date_published == "2018"
    assert subject.publisher == {
        "name": "Springer Science and Business Media LLC",
    }
    assert len(subject.references) == 44
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "title": "SpringerBriefs in Medical Earth Sciences",
        "identifiers": [{"identifier": "2523-3629", "identifier_type": "ISSN"}],
        "first_page": "1",
        "last_page": "13",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_yet_another_book_chapter():
    "yet another book chapter"
    string = "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.4018/978-1-4666-1891-6.ch004"
    assert subject.type == "BookChapter"
    assert (
        subject.url
        == "http://services.igi-global.com/resolvedoi/resolve.aspx?doi=10.4018/978-1-4666-1891-6.ch004"
    )
    assert (
        subject.title
        == "Unsupervised and Supervised Image Segmentation Using Graph Partitioning"
    )
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Charles-Edmond",
            "family_name": "Bichot",
            "affiliations": [{"name": "Universit\u00e9 de Lyon, France"}],
        },
        "roles": ["Author"],
    }
    assert subject.license is None
    assert (
        subject.date_published == "2012-08-08"
        and subject.date_updated[:10] == "2019-07-02"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "IGI Global Scientific Publishing",
    }
    assert len(subject.references) == 29
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Book",
        "title": "Graph-Based Methods in Computer Vision",
        "first_page": "72",
        "last_page": "94",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description.startswith(
        "Image segmentation is an important research area"
    )
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_missing_contributor():
    "missing contributor"
    string = "https://doi.org/10.3390/publications6020015"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.3390/publications6020015"
    assert subject.type == "JournalArticle"
    assert subject.url == "https://www.mdpi.com/2304-6775/6/2/15"
    assert (
        subject.title
        == "Converting the Literature of a Scientific Field to Open Access through Global Collaboration: The Experience of SCOAP3 in Particle Physics"
    )
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "id": "https://orcid.org/0000-0002-3836-8885",
            "given_name": "Alexander",
            "family_name": "Kohls",
        },
        "roles": ["Author"],
    }
    assert subject.license == {
        "id": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
    }
    assert (
        subject.date_published == "2018-04-09"
        and subject.date_updated[:10] == "2025-10-11"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "MDPI AG",
    }
    assert len(subject.references) == 22
    assert subject.references[0] == {
        "key": "ref_1",
        "reference": "(2018, February 20). CERN Convention for the Establishment of a European Organization for Nuclear Research. Available online: https://council.web.cern.ch/en/content/convention-establishment-european-organization-nuclear-research.",
    }
    assert subject.references[-1] == {
        "key": "ref_23",
        "reference": "(2018, February 20). SCOAP3 News: APS Joins SCOAP3. Available online: http://www.webcitation.org/6xNFQb5iD.",
    }
    assert subject.funding_references is None
    assert subject.container == {
        "type": "Journal",
        "title": "Publications",
        "first_page": "15",
        "issue": "2",
        "volume": "6",
        "identifiers": [{"identifier": "2304-6775", "identifier_type": "ISSN"}],
    }
    assert subject.subjects is None
    assert subject.language == "en"
    assert subject.description.startswith("Gigantic particle accelerators")
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_book():
    "book"
    string = "https://doi.org/10.1017/9781108348843"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1017/9781108348843"
    assert subject.type == "Book"
    assert (
        subject.url
        == "https://www.cambridge.org/core/product/identifier/9781108348843/type/book"
    )
    assert subject.title == "The Politics of the Past in Early China"
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {"given_name": "Vincent S.", "family_name": "Leung"},
        "roles": ["Author"],
    }
    assert subject.license == {"url": "https://www.cambridge.org/core/terms"}
    assert subject.date_published == "2019-07-01"
    assert subject.publisher == {
        "name": "Cambridge University Press (CUP)",
    }
    # structured-only citations without a DOI or unstructured text are dropped.
    assert len(subject.references) == 100
    assert subject.references[0] == {
        "key": "9781108348843#EMT-rl-1_BIBe-r-266",
        "id": "https://doi.org/10.1093/acprof:oso/9780199367344.001.0001",
    }
    assert subject.funding_references is None
    assert subject.container is None
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"


def test_proceedings_article():
    "proceedings article"
    string = "10.1145/3448016.3452841"
    subject = Metadata(string, via="crossref_xml")
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.1145/3448016.3452841"
    assert subject.type == "ProceedingsArticle"
    assert subject.url == "https://dl.acm.org/doi/10.1145/3448016.3452841"
    assert subject.title == "Vector Quotient Filters"
    assert subject.additional_titles == [
        {
            "title": "Overcoming the Time/Space Trade-Off in Filter Design",
            "type": "Subtitle",
        },
    ]
    assert len(subject.contributors) == 6
    assert subject.contributors[0] == {
        "type": "Person",
        "person": {
            "given_name": "Prashant",
            "family_name": "Pandey",
            "affiliations": [
                {
                    "name": "Lawrence Berkeley National Lab &amp; University of California, Berkeley, Berkeley, CA, USA"
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
        subject.date_published == "2021-06-09"
        and subject.date_updated[:10] == "2025-06-17"
        and subject.dates is None
    )
    assert subject.publisher == {
        "name": "Association for Computing Machinery (ACM)",
    }
    assert len(subject.references) == 56
    assert subject.references[-1] == {
        "key": "e_1_3_2_2_56_1",
        "id": "https://doi.org/10.5555/1364813.1364831",
    }
    assert subject.funding_references == [
        {
            "funder_id": "https://doi.org/10.13039/100000001",
            "funder_name": "NSF (National Science Foundation)",
            "award_number": "CCF 805476, CCF 822388, CCF 1724745,CCF 1715777, CCF 1637458, IIS 1541613, CRII 1947789, CNS 1408695, CNS 1755615, CCF 1439084, CCF 1725543, CSR 1763680, CCF 1716252, CCF 1617618, CNS 1938709, IIS 1247726, CNS-1938709,CCF-1750472,CCF-1452904,CNS-1763680",
        },
        {
            "funder_id": "https://doi.org/10.13039/100000015",
            "funder_name": "DOE U.S. Department of Energy",
            "award_number": "DE-AC02-05CH11231,17-SC-20-SC",
        },
    ]
    assert subject.container == {
        "type": "Proceedings",
        "identifiers": [{"identifier": "9781450383431", "identifier_type": "ISBN"}],
        "title": "Proceedings of the 2021 International Conference on Management of Data",
        "first_page": "1386",
        "last_page": "1399",
        "location": "Virtual Event China",
        "series": "SIGMOD/PODS '21",
    }
    assert subject.subjects is None
    assert subject.language is None
    assert subject.description is None
    assert subject.version is None
    assert subject.provider == "Crossref"
