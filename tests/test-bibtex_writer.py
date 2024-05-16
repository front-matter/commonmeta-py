"""Bibtex writer tests"""

from os import path
import pytest
from commonmeta import Metadata, MetadataList

def vcr_config():
    return {"record_mode": "new_episodes"}

@pytest.mark.vcr
def test_doi_with_data_citation():
    "DOi with data citation"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{10.7554/elife.01567,
    abstract = {Among various advantages, their small size makes model organisms preferred subjects of investigation. Yet, even in model systems detailed analysis of numerous developmental processes at cellular level is severely hampered by their scale. For instance, secondary growth of Arabidopsis hypocotyls creates a radial pattern of highly specialized tissues that comprises several thousand cells starting from a few dozen. This dynamic process is difficult to follow because of its scale and because it can only be investigated invasively, precluding comprehensive understanding of the cell proliferation, differentiation, and patterning events involved. To overcome such limitation, we established an automated quantitative histology approach. We acquired hypocotyl cross-sections from tiled high-resolution images and extracted their information content using custom high-throughput image processing and segmentation. Coupled with automated cell type recognition through machine learning, we could establish a cellular resolution atlas that reveals vascular morphodynamics during secondary growth, for example equidistant phloem pole formation.},
    author = {Sankar, Martial and Nieminen, Kaisa and Ragni, Laura and Xenarios, Ioannis and Hardtke, Christian S},
    copyright = {https://creativecommons.org/licenses/by/3.0/legalcode},
    doi = {10.7554/elife.01567},
    issn = {2050-084X},
    journal = {eLife},
    language = {en},
    month = feb,
    title = {Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth},
    url = {https://elifesciences.org/articles/01567},
    urldate = {2014-02-11},
    year = {2014}
}
"""
    )


@pytest.mark.vcr
def test_doi_for_blog_post():
    "DOi for blog post"
    subject = Metadata("10.53731/avg2ykg-gdxppcd")
    assert subject.id == "https://doi.org/10.53731/avg2ykg-gdxppcd"
    assert subject.type == "Article"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{10.53731/avg2ykg-gdxppcd,
    abstract = {Science blogs have been around for at least 20 years and have become an important part of science communication. So are there any fundamental issues that need fixing? Barriers to Entry Blogging platforms are mature at this point, and the technology is not imposing barriers to entry for most people.},
    author = {Fenner, Martin},
    copyright = {https://creativecommons.org/licenses/by/4.0/legalcode},
    doi = {10.53731/avg2ykg-gdxppcd},
    month = jan,
    title = {Do we need to fix science blogs?},
    url = {https://blog.front-matter.io/posts/need-to-fix-science-blogs},
    urldate = {2023-01-25},
    year = {2023}
}
"""
    )


@pytest.mark.vcr
def test_blog_post():
    "blog post"
    string = "https://upstream.force11.org/welcome-to-upstream/"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.54900/rckn8ey-1fm76va-qsrnf"
    assert subject.type == "Article"
    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{10.54900/rckn8ey-1fm76va-qsrnf,
    abstract = {Today we are announcing &lt;strong&gt; Upstream &lt;/strong&gt; . And if you’re reading this, you’re already a part of it! Upstream is a community blogging platform designed for Open enthusiasts to discuss… you guessed it: all things Open. It’s a space for the whole community to voice opinions, discuss open approaches to scholarly communication, and showcase research.},
    author = {Chodacki, John and Hendricks, Ginny and Ferguson, Christine and Fenner, Martin},
    copyright = {https://creativecommons.org/licenses/by/4.0/legalcode},
    doi = {10.54900/rckn8ey-1fm76va-qsrnf},
    month = nov,
    title = {Welcome to Upstream: the new space for scholarly community discussion on all things open},
    url = {https://upstream.force11.org/welcome-to-upstream},
    urldate = {2021-11-22},
    year = {2021}
}
"""
    )


@pytest.mark.vcr
def test_article_with_pages():
    "article with pages"
    subject = Metadata("https://doi.org/10.1371/journal.ppat.1008184")
    assert subject.id == "https://doi.org/10.1371/journal.ppat.1008184"
    assert subject.type == "JournalArticle"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{10.1371/journal.ppat.1008184,
    author = {Twittenhoff, Christian and Heroven, Ann Kathrin and Mühlen, Sabrina and Dersch, Petra and Narberhaus, Franz and Tran Van Nhieu, Guy},
    copyright = {https://creativecommons.org/licenses/by/4.0/legalcode},
    doi = {10.1371/journal.ppat.1008184},
    issn = {1553-7374},
    issue = {1},
    journal = {PLOS Pathogens},
    language = {en},
    month = jan,
    pages = {e1008184},
    title = {An RNA thermometer dictates production of a secreted bacterial toxin},
    url = {https://dx.plos.org/10.1371/journal.ppat.1008184},
    urldate = {2020-01-17},
    year = {2020}
}
"""
    )


@pytest.mark.vcr
def test_article_dlib_magazine():
    "article dlib magazine"
    subject = Metadata("https://doi.org/10.1045/january2017-burton")
    assert subject.id == "https://doi.org/10.1045/january2017-burton"
    assert subject.type == "JournalArticle"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{10.1045/january2017-burton,
    author = {Burton, Adrian and Aryani, Amir and Koers, Hylke and Manghi, Paolo and La Bruzzo, Sandro and Stocker, Markus and Diepenbroek, Michael and Schindler, Uwe and Fenner, Martin},
    doi = {10.1045/january2017-burton},
    issn = {1082-9873},
    issue = {1/2},
    journal = {D-Lib Magazine},
    language = {en},
    month = jan,
    title = {The Scholix Framework for Interoperability in Data-Literature Information Exchange},
    url = {http://www.dlib.org/dlib/january17/burton/01burton.html},
    urldate = {2017-01},
    year = {2017}
}
"""
    )


@pytest.mark.vcr
def test_inproceedings():
    """inproceedings"""
    subject = Metadata("https://doi.org/10.1145/3448016.3452841", via="crossref_xml")
    assert subject.id == "https://doi.org/10.1145/3448016.3452841"
    assert subject.type == "ProceedingsArticle"
    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@inproceedings{10.1145/3448016.3452841,
    author = {Pandey, Prashant and Conway, Alex and Durie, Joe and Bender, Michael A. and Farach-Colton, Martin and Johnson, Rob},
    booktitle = {Proceedings of the 2021 International Conference on Management of Data},
    copyright = {https://www.acm.org/publications/policies/copyright_policy#Background},
    doi = {10.1145/3448016.3452841},
    isbn = {9781450383431},
    location = {Virtual Event China},
    month = jun,
    pages = {1386--1399},
    publisher = {Association for Computing Machinery (ACM)},
    series = {SIGMOD/PODS '21},
    title = {Vector Quotient Filters: Overcoming the Time/Space Trade-Off in Filter Design},
    url = {https://dl.acm.org/doi/10.1145/3448016.3452841},
    urldate = {2021-06-09},
    year = {2021}
}
"""
    )


@pytest.mark.vcr
def test_book_chapter():
    """book chapter"""
    subject = Metadata("https://doi.org/10.1007/978-3-662-46370-3_13")
    assert subject.id == "https://doi.org/10.1007/978-3-662-46370-3_13"
    assert subject.type == "BookChapter"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@inbook{10.1007/978-3-662-46370-3_13,
    author = {Diercks, Ronald L. and Ludvigsen, Tom Clement},
    booktitle = {Shoulder Stiffness},
    copyright = {https://www.springernature.com/gp/researchers/text-and-data-mining},
    doi = {10.1007/978-3-662-46370-3_13},
    isbn = {9783662463703},
    month = may,
    pages = {155--158},
    publisher = {Springer Berlin Heidelberg},
    title = {Clinical Symptoms and Physical Examinations},
    url = {https://link.springer.com/10.1007/978-3-662-46370-3_13},
    urldate = {2015},
    year = {2015}
}
"""
    )


@pytest.mark.vcr
def test_conference_proceedings():
    """conference proceedings"""
    subject = Metadata("https://doi.org/10.1109/iccv.2007.4408927")
    assert subject.id == "https://doi.org/10.1109/iccv.2007.4408927"
    assert subject.type == "ProceedingsArticle"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@inproceedings{10.1109/iccv.2007.4408927,
    author = {Sinop, Ali Kemal and Grady, Leo},
    booktitle = {2007 IEEE 11th International Conference on Computer Vision},
    doi = {10.1109/iccv.2007.4408927},
    month = may,
    publisher = {IEEE},
    title = {A Seeded Image Segmentation Framework Unifying Graph Cuts And Random Walker Which Yields A New Algorithm},
    url = {http://ieeexplore.ieee.org/document/4408927},
    urldate = {2007},
    year = {2007}
}
"""
    )


@pytest.mark.vcr
def test_phd_thesis():
    """phd thesis"""
    subject = Metadata("10.14264/uql.2020.791")
    assert subject.id == "https://doi.org/10.14264/uql.2020.791"
    assert subject.type == "Dissertation"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@phdthesis{10.14264/uql.2020.791,
    author = {Collingwood, Patricia Maree},
    doi = {10.14264/uql.2020.791},
    institution = {University of Queensland Library},
    month = jun,
    title = {School truancy and financial independence during emerging adulthood: a longitudinal analysis of receipt of and reliance on cash transfers},
    url = {http://espace.library.uq.edu.au/view/UQ:23a1e74},
    urldate = {2020-06-08},
    year = {2020}
}
"""
    )


def test_inveniordm_software():
    "inveniordm software"
    string = path.join(path.dirname(__file__), "fixtures", "inveniordm-software.json")
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.7752775"
    assert subject.type == "Software"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@misc{10.5281/zenodo.7752775,
    abstract = {Ruby gem and command-line utility for conversion of DOI metadata from and to different metadata formats, including schema.org. Fork of version 1.19.12 of the bolognese gem.},
    author = {Fenner, Martin},
    copyright = {https://opensource.org/licenses/MIT},
    doi = {10.5281/zenodo.7752775},
    month = mar,
    publisher = {Zenodo},
    title = {commonmeta-ruby},
    url = {https://zenodo.org/records/7752775},
    urldate = {2023-03-20},
    year = {2023}
}
"""
    )


@pytest.mark.vcr
def test_inveniordm_presentation():
    "inveniordm presentation"
    string = "https://zenodo.org/api/records/8173303"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.8173303"
    assert subject.type == "Presentation"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@misc{10.5281/zenodo.8173303,
    abstract = {CERN/NASA “Accelerating the Adoption of Open Science”, from July 10th-14th at CERN in Geneva, Switzerland https://indico.cern.ch/event/1254282/ 11&nbsp;July 2023 (Day 2)&nbsp;Open Data Sharing},
    author = {Seibold, Heidi},
    copyright = {https://creativecommons.org/licenses/by/4.0/legalcode},
    doi = {10.5281/zenodo.8173303},
    month = jul,
    publisher = {Zenodo},
    title = {11 July 2023 (Day 2) CERN – NASA Open Science Summit Sketch Notes},
    url = {https://zenodo.org/records/8173303},
    urldate = {2023-07-21},
    year = {2023}
}
"""
    )


@pytest.mark.vcr
def test_inveniordm_publication():
    "inveniordm publication"
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{10.5281/zenodo.5244404,
    abstract = {The Origins of SARS-CoV-2: A Critical Review Holmes et al. Published online: 18-Aug-2021,&nbsp;Cell,&nbsp;https://doi.org/10.1016/j.cell.2021.08.017 Since the first reports of a novel SARS-like coronavirus in December 2019 in Wuhan, China, there has been intense interest in understanding how SARS-CoV-2 emerged in the human population. Recent debate has coalesced around two competing ideas: a “laboratory escape” scenario and zoonotic emergence. Here, we critically review the current scientific evidence that may help clarify the origin of SARS-CoV-2. Computer readable versions of data tables, SVG maps, and acknowledgements of sequence data used are available from: https://github.com/sars-cov-2-origins/critical-review &nbsp;},
    author = {Holmes, Edward C and Goldstein, Stephen A and Rasmussen, Angela L and Robertson, David L and Crits-Christoph, Alexander and Wertheim, Joel O and Anthony, Simon J and Barclay, Wendy S and Boni, Maciej F and Doherty, Peter C and Farrar, Jeremy and Geoghegan, Jemma L and Jiang, Xiaowei and Leibowitz, Julian L and Neil, Stuart J D and Skern, Tim and Weiss, Susan R and Worobey, Michael and Andersen, Kristian G and Garry, Robert F and Rambaut, Andrew},
    copyright = {https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode},
    doi = {10.5281/zenodo.5244404},
    month = aug,
    title = {The Origins of SARS-CoV-2: A Critical Review},
    url = {https://zenodo.org/records/5244404},
    urldate = {2021-08-18},
    year = {2021}
}
"""
    )


@pytest.mark.vcr
def test_inveniordm_report():
    "inveniordm report"
    string = "https://zenodo.org/api/records/3871094"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.3871094"
    assert subject.type == "JournalArticle"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{10.5281/zenodo.3871094,
    abstract = {Open letter to MR Mehra, SS Desai, F Ruschitzka, and AN Patel, authors of <strong>“Hydroxychloroquine or chloroquine with or without a macrolide for treatment of COVID-19: a multinational registry analysis”. Lancet. 2020 May 22:S0140-6736(20)31180-6. doi: 10.1016/S0140-6736(20)31180-6. PMID: 32450107</strong> and to Richard Horton (editor of The Lancet).},
    author = {signatories, James Watson on the behalf of 201},
    copyright = {https://creativecommons.org/licenses/by/4.0/legalcode},
    doi = {10.5281/zenodo.3871094},
    language = {eng},
    month = may,
    title = {An open letter to Mehra et al and The Lancet},
    url = {https://zenodo.org/records/3871094},
    urldate = {2020-05-28},
    year = {2020}
}
"""
    )


@pytest.mark.vcr
def test_inveniordm_preprint():
    "inveniordm preprint"
    string = "https://zenodo.org/api/records/8120771"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.8120771"
    assert subject.type == "JournalArticle"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{10.5281/zenodo.8120771,
    abstract = {<strong>ABSTRACT</strong> <strong>Background:</strong> The rapid development and widespread deployment of COVID-19 vaccines, combined with a high number of adverse event reports, have led to concerns over possible mechanisms of injury including systemic lipid nanoparticle (LNP) and mRNA distribution, spike protein-associated tissue damage, thrombogenicity, immune system dysfunction, and carcinogenicity. The aim of this systematic review is to investigate possible causal links between COVID-19 vaccine administration and death using autopsies and post-mortem analysis. &nbsp; <strong>Methods:</strong> We searched for all published autopsy and necropsy reports relating to COVID-19 vaccination up until May 18<sup>th</sup>, 2023. We initially identified 678 studies and, after screening for our inclusion criteria, included 44 papers that contained 325 autopsy cases and one necropsy case. Three physicians independently reviewed all deaths and determined whether COVID-19 vaccination was the direct cause or contributed significantly to death. &nbsp; <strong>Findings:</strong> The most implicated organ system in COVID-19 vaccine-associated death was the cardiovascular system (53%), followed by the hematological system (17%), the respiratory system (8%), and multiple organ systems (7%). Three or more organ systems were affected in 21 cases. The mean time from vaccination to death was 14.3 days. Most deaths occurred within a week from last vaccine administration. A total of 240 deaths (73.9%) were independently adjudicated as directly due to or significantly contributed to by COVID-19 vaccination. &nbsp; <strong>Interpretation:</strong> The consistency seen among cases in this review with known COVID-19 vaccine adverse events, their mechanisms, and related excess death, coupled with autopsy confirmation and physician-led death adjudication, suggests there is a high likelihood of a causal link between COVID-19 vaccines and death in most cases. Further urgent investigation is required for the purpose of clarifying our findings.&nbsp;},
    author = {Nicolas Hulscher, BS and Alexander, Paul E. and Amerling, Richard and Gessling, Heather and Hodkinson, Roger and Makis, William and Risch, Harvey A. and Trozzi, Mark and McCullough, Peter A.},
    copyright = {https://creativecommons.org/licenses/by/4.0/legalcode},
    doi = {10.5281/zenodo.8120771},
    language = {eng},
    month = jul,
    title = {A SYSTEMATIC REVIEW OF AUTOPSY FINDINGS IN DEATHS AFTER COVID-19 VACCINATION},
    url = {https://zenodo.org/records/8120771},
    urldate = {2023-07-06},
    year = {2023}
}
"""
    )


@pytest.mark.vcr
def test_inveniordm_dataset():
    "inveniordm dataset"
    string = "https://zenodo.org/api/records/7834392"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.7834392"
    assert subject.type == "Dataset"

    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@misc{10.5281/zenodo.7834392,
    abstract = {<em><strong>Version 162&nbsp;of the dataset. NOTES: Data for 3/15 - 3/18 was not extracted due to unexpected and unannounced downtime of our university infrastructure. We will try to backfill those days by next release.&nbsp;</strong></em><em><strong>FUTURE CHANGES: Due to the imminent&nbsp;paywalling of Twitter's API access&nbsp;this might be the last full update of this dataset. If the API access is not blocked, we will be stopping updates for this dataset with release 165 - a bit more than 3 years after our initial release. It's been a joy seeing all the work that uses this resource and we are glad that so many found it useful.&nbsp;</strong></em> <em><strong>The dataset files: full_dataset.tsv.gz and&nbsp;full_dataset_clean.tsv.gz have&nbsp;been split in 1 GB&nbsp;parts using the Linux utility called Split. So make sure to join the&nbsp;parts before unzipping. We had to make this change as we had huge issues uploading files larger than 2GB's&nbsp;(hence the delay in the dataset releases).&nbsp;The peer-reviewed publication for this dataset has now been published&nbsp; in&nbsp;Epidemiologia an&nbsp;MDPI journal, and can be accessed here:&nbsp;https://doi.org/10.3390/epidemiologia2030024. Please cite this when using the dataset.</strong></em> <strong>Due to the relevance of the COVID-19 global pandemic, we are releasing our dataset of tweets acquired from the Twitter Stream related to COVID-19 chatter. Since our first release we have received additional data from our new collaborators, allowing this resource to grow to its current size. Dedicated data gathering started from March 11th yielding over 4 million tweets a day. We have added additional data provided by our new collaborators from January 27th to March 27th, to provide extra longitudinal coverage. Version 10 added&nbsp;~1.5 million tweets in the Russian language collected between January 1st and May 8th, gracefully provided to us by:&nbsp;Katya Artemova (NRU HSE) and Elena Tutubalina (KFU). From version 12 we have included daily hashtags, mentions and emoijis and their frequencies the respective zip files. From version 14&nbsp;<em>we</em>&nbsp;have included the tweet identifiers and their respective language for the clean version of the dataset. Since&nbsp;version 20 we have included language and place location for all tweets.</strong> <strong>The data collected from the stream captures all languages, but the higher prevalence are:&nbsp; English, Spanish, and French. We release all tweets and retweets on the full_dataset.tsv file (1,395,222,801 unique tweets), and a cleaned version with no retweets on the full_dataset-clean.tsv file (361,748,721 unique tweets). There are several practical reasons for us to leave the retweets, tracing important tweets and their dissemination is one of them. For NLP tasks we provide the top 1000 frequent terms in frequent_terms.csv, the top 1000 bigrams in frequent_bigrams.csv, and the top 1000 trigrams in frequent_trigrams.csv. Some general statistics per day are included for both datasets in the full_dataset-statistics.tsv and full_dataset-clean-statistics.tsv files. For more statistics and some visualizations visit:&nbsp;http://www.panacealab.org/covid19/&nbsp;</strong> <strong>More details can be found (and will be updated faster at: https://github.com/thepanacealab/covid19_twitter) and our pre-print about the dataset (https://arxiv.org/abs/2004.03688)&nbsp;</strong> <strong>As always, the tweets distributed here are only tweet identifiers (with date and time added) due to the terms and conditions of Twitter to re-distribute Twitter data ONLY for research purposes. They need to be hydrated to be used.</strong>},
    author = {Banda, Juan M. and Tekumalla, Ramya and Wang, Guanyu and Yu, Jingyuan and Liu, Tuo and Ding, Yuning and Artemova, Katya and Tutubalina, Elena and Chowell, Gerardo},
    copyright = {None},
    doi = {10.5281/zenodo.7834392},
    language = {eng},
    month = apr,
    publisher = {Zenodo},
    title = {A large-scale COVID-19 Twitter chatter dataset for open scientific research - an international collaboration},
    url = {https://zenodo.org/records/7834392},
    urldate = {2023-04-16},
    year = {2023}
}
"""
    )


def test_kbase_gulf_of_mexico():
    """kbase gulf of mexico"""
    string = path.join(
        path.dirname(__file__), "fixtures", "10.25982_86723.65_1778009_kbcms.json"
    )
    subject = Metadata(string)
    assert (
        subject.write(to="bibtex")
        == """@misc{10.25982/86723.65/1778009,
    abstract = {xploration of oxygen-depleted marine environments has consistently revealed novel microbial taxa and metabolic capabilities that expand our understanding of microbial evolution and ecology. Marine blue holes are shallow karst formations characterized by low oxygen and high organic matter content. They are logistically challenging to sample, and thus our understanding of their biogeochemistry and microbial ecology is limited. We present a metagenomic and geochemical characterization of Amberjack Hole on the Florida continental shelf (Gulf of Mexico). Dissolved oxygen became depleted at the hole's rim (32 m water depth), remained low but detectable in an intermediate hypoxic zone (40-75 m), and then increased to a secondary peak before falling below detection in the bottom layer (80-110 m), concomitant with increases in nutrients, dissolved iron, and a series of sequentially more reduced sulfur species. Microbial communities in the bottom layer contained heretofore undocumented levels of the recently discovered phylum Woesearchaeota (up to 58% of the community), along with lineages in the bacterial Candidate Phyla Radiation (CPR). Thirty-one high-quality metagenome-assembled genomes (MAGs) showed extensive biochemical capabilities for sulfur and nitrogen cycling, as well as for resisting and respiring arsenic. One uncharacterized gene associated with a CPR lineage differentiated hypoxic from anoxic zone communities. Overall, microbial communities and geochemical profiles were stable across two sampling dates in the spring and fall of 2019. The blue hole habitat is a natural marine laboratory that provides opportunities for sampling taxa with under-characterized but potentially important roles in redox-stratified microbial processes.},
    author = {Patin, Nastassia},
    copyright = {https://creativecommons.org/licenses/by/4.0/},
    doi = {10.25982/86723.65/1778009},
    language = {en-US},
    month = may,
    publisher = {KBase},
    title = {Gulf of Mexico blue hole harbors high levels of novel microbial lineages: A load of cool stuff from the blue hole in the Gulf of Mexico},
    urldate = {2021},
    year = {2021}
}
"""
    )


@pytest.mark.vcr
def test_post_without_doi():
    """blog post without doi"""
    string = "https://api.rogue-scholar.org/posts/c314bfea-2151-4ccc-8fa8-dd0d1000dfbe"
    subject = Metadata(string)
    assert subject.is_valid
    assert (
        subject.id
        == "https://verfassungsblog.de/grundrechtsverwirkung-und-parteiverbote-gegen-radikale-afd-landesverbande-iii"
    )
    assert subject.type == "Article"
    bibtex = subject.write(to="bibtex")

    assert (
        bibtex
        == """@article{https://verfassungsblog.de/grundrechtsverwirkung-und-parteiverbote-gegen-radikale-afd-landesverbande-iii,
    abstract = {Das demokratische Haus in Deutschland brennt. Es ist höchste Zeit, die Instrumente der streitbaren Demokratie gegen Landesverbände der AfD einzusetzen, die mit hoher Wahrscheinlichkeit verfassungswidrig sind, wie die in Thüringen, Sachsen und Sachsen-Anhalt. Warum die Voraussetzungen für Grundrechtsverwirkung und Parteiverbot dort vorliegen, und die Verfassungstreue es auch verlangt, sie zu beantragen, soll dieser dreiteilige Beitrag begründen.},
    author = {Hong, Mathias},
    copyright = {https://creativecommons.org/licenses/by/4.0/legalcode},
    journal = {Verfassungsblog},
    language = {de},
    month = feb,
    title = {Grundrechtsverwirkung und Parteiverbote gegen radikale AfD-Landesverbände (Teil&nbsp;III)},
    url = {https://verfassungsblog.de/grundrechtsverwirkung-und-parteiverbote-gegen-radikale-afd-landesverbande-iii},
    urldate = {2024-02-08},
    year = {2024}
}
"""
    )


@pytest.mark.vcr
def test_write_bibtex_list():
    """write_bibtex_list"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref-list.json")
    subject_list = MetadataList(string, via="crossref")
    assert len(subject_list.items) == 20
    bibtex_list = subject_list.write(to="bibtex")
    lines = bibtex_list.splitlines()
    assert lines[0] == "@article{10.1002/fedr.4910730105,"
    assert lines[1].lstrip() == "author = {Dvořák, František},"
    assert lines[2].lstrip() == "doi = {10.1002/fedr.4910730105},"
