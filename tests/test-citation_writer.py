# pylint: disable=invalid-name
"""Citation writer tests"""
import os
import pytest
from commonmeta import Metadata


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    assert subject.style == "apa"
    assert subject.locale == "en-US"
    assert (
        subject.citation()
        == "Sankar, M., Nieminen, K., Ragni, L., Xenarios, I., &amp; Hardtke, C. S. (2014). Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth. <i>Elife</i>, <i>3</i>. https://doi.org/10.7554/elife.01567"
    )


def test_journal_article_vancouver_style():
    "journal article vancouver style"
    subject = Metadata("10.7554/elife.01567", style="vancouver", locale="en-US")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    assert subject.style == "vancouver"
    assert subject.locale == "en-US"
    assert (
        subject.citation()
        == "1. Sankar M, Nieminen K, Ragni L, Xenarios I, Hardtke CS. Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth. eLife [Internet]. 2014Feb11;3. Available from: https://elifesciences.org/articles/01567"
    )


def test_dataset():
    """dataset"""
    subject = Metadata("https://doi.org/10.5061/DRYAD.8515")
    assert (
        subject.citation()
        == "Ollomo, B., Durand, P., Prugnolle, F., Douzery, E. J. P., Arnathau, C., Nkoghe, D., Leroy, E., &amp; Renaud, F. (2011). <i>Data from: A new malaria agent in African hominids.</i> (Version 1) [Data set]. Dryad. https://doi.org/10.5061/dryad.8515"
    )


def test_missing_author():
    "missing author"
    subject = Metadata("10.3390/publications6020015", style="apa", locale="en-US")
    assert subject.id == "https://doi.org/10.3390/publications6020015"
    assert subject.type == "JournalArticle"

    assert subject.style == "apa"
    assert subject.locale == "en-US"
    assert (
        subject.citation()
        == "Kohls, A., &amp; Mele, S. (2018). Converting the Literature of a Scientific Field to Open Access through Global Collaboration: The Experience of SCOAP3 in Particle Physics. <i>Publications</i>, <i>6</i>(2), 15. https://doi.org/10.3390/publications6020015"
    )


def test_software_with_version():
    """software with version"""
    subject = Metadata("https://doi.org/10.5281/zenodo.2598836")
    assert (
        subject.citation()
        == "Studies, L. F. E. A. N. S. E. (2019). <i>lenses-lab/LYAO_RT-2018JA026426: Original Release</i> (1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.2598836"
    )


def test_software_via_cff():
    """software via cff"""
    subject = Metadata("https://github.com/blebon/directChillFoam")
    # assert subject.citation(
    # ) == 'Liang, K. (2023). <i>Long Context Transformer v0.0.1</i> (0.0.1) [Computer software]. GitHub. https://doi.org/10.5281/zenodo.7651809'


#  missing date["published"]
# def test_kbase_metatranscriptome():
#     """Metatrascriptome"""
#     string = os.path.join(
#         os.path.dirname(__file__), "fixtures", "JDP_5fa4fb4647675a20c852c60b_kbcms.json"
#     )
#     subject = Metadata(string)
#     assert (
#         subject.citation()
#         == "Patin, N. (2021). Gulf of Mexico blue hole harbors high levels of novel microbial lineages [Data set]. In <i>KBase</i>. KBase. https://doi.org/10.25982/86723.65/1778009"
#     )


def test_kbase_gulf_of_mexico():
    """kbase gulf of mexico"""
    string = os.path.join(
        os.path.dirname(__file__), "fixtures", "10.25982_86723.65_1778009_kbcms.json"
    )
    subject = Metadata(string)
    assert (
        subject.citation()
        == "Patin, N. (2021). Gulf of Mexico blue hole harbors high levels of novel microbial lineages [Data set]. In <i>KBase</i>. KBase. https://doi.org/10.25982/86723.65/1778009"
    )
