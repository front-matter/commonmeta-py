# pylint: disable=invalid-name
"""RIS writer tests"""
import pytest
from os import path

from commonmeta import Metadata, MetadataList


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    ris = subject.write(to="ris").splitlines()
    assert ris[0] == "TY  - JOUR"
    assert (
        ris[1]
        == "T1  - Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert ris[2] == "T2  - eLife"
    assert ris[3] == "AU  - Sankar, Martial"
    assert ris[8] == "DO  - 10.7554/elife.01567"
    assert ris[9] == "UR  - https://elifesciences.org/articles/01567"
    assert ris[10].startswith("AB  - Among various advantages")
    assert ris[11] == "PY  - 2014"
    assert ris[12] == "PB  - eLife Sciences Publications, Ltd"
    assert ris[13] == "LA  - en"
    assert ris[14] == "VL  - 3"
    assert ris[15] == "ER  - "


def test_with_pages():
    "with pages"
    subject = Metadata("https://doi.org/10.1155/2012/291294")
    assert subject.id == "https://doi.org/10.1155/2012/291294"
    assert subject.type == "JournalArticle"

    ris = subject.write(to="ris").splitlines()
    assert ris[0] == "TY  - JOUR"
    assert (
        ris[1]
        == "T1  - Delineating a Retesting Zone Using Receiver Operating Characteristic Analysis on Serial QuantiFERON Tuberculosis Test Results in US Healthcare Workers"
    )
    assert ris[2] == "T2  - Pulmonary Medicine"
    assert ris[3] == "AU  - Thanassi, Wendy"
    assert ris[10] == "DO  - 10.1155/2012/291294"
    assert ris[11] == "UR  - http://www.hindawi.com/journals/pm/2012/291294"
    assert ris[12].startswith("AB  - Objective. To find a statistically significant")
    assert ris[13] == "PY  - 2012"
    assert ris[14] == "PB  - Hindawi Limited"
    assert ris[15] == "LA  - en"
    assert ris[16] == "VL  - 2012"
    assert ris[17] == "SP  - 1"
    assert ris[18] == "EP  - 7"
    assert ris[19] == "ER  - "


#     it 'alternate name' do
#       input = 'https://doi.org/10.3205/ZMA001102'
#       subject = described_class.new(input: input, from: 'datacite')
#       expect(subject.valid?).to be true
#       ris = subject.ris.split("\r\n")
#       expect(ris[0]).to eq('TY  - RPRT')
#       expect(ris[1]).to eq('T1  - Visions and reality: the idea of competence-oriented assessment for German medical students is not yet realised in licensing examinations')
#       expect(ris[2]).to eq('T2  - GMS Journal for Medical Education; 34(2):Doc25')
#       expect(ris[3]).to eq('AU  - Huber-Lang, Markus')
#       expect(ris[9]).to eq('DO  - 10.3205/zma001102')
#       expect(ris[10]).to eq('UR  - http://www.egms.de/en/journals/zma/2017-34/zma001102.shtml')
#       expect(ris[11]).to start_with('AB  - Objective: Competence orientation')
#       expect(ris[12]).to eq('KW  - medical competence')
#       expect(ris[21]).to eq('PY  - 2017')
#       expect(ris[22]).to eq('PB  - German Medical Science GMS Publishing House')
#       expect(ris[23]).to eq('LA  - en')
#       expect(ris[24]).to eq('SN  - 2366-5017')
#       expect(ris[25]).to eq('ER  - ')
#     end

#     it 'Crossref DOI' do
#       input = "#{fixture_path}crossref.bib"
#       subject = described_class.new(input: input, from: 'bibtex')

#       ris = subject.ris.split("\r\n")
#       expect(ris[0]).to eq('TY  - JOUR')
#       expect(ris[1]).to eq('T1  - Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth')
#       expect(ris[2]).to eq('T2  - eLife')
#       expect(ris[3]).to eq('AU  - Sankar, Martial')
#       expect(ris[8]).to eq('DO  - 10.7554/elife.01567')
#       expect(ris[9]).to eq('UR  - http://elifesciences.org/lookup/doi/10.7554/eLife.01567')
#       expect(ris[10]).to eq('AB  - Among various advantages, their small size makes model organisms preferred subjects of investigation. Yet, even in model systems detailed analysis of numerous developmental processes at cellular level is severely hampered by their scale.')
#       expect(ris[11]).to eq('PY  - 2014')
#       expect(ris[12]).to eq('PB  - {eLife} Sciences Organisation, Ltd.')
#       expect(ris[13]).to eq('VL  - 3')
#       expect(ris[14]).to eq('SN  - 2050-084X')
#       expect(ris[15]).to eq('ER  - ')
#     end

#     it 'BlogPosting' do
#       input = 'https://doi.org/10.5438/4K3M-NYVG'
#       subject = described_class.new(input: input, from: 'datacite')
#       expect(subject.valid?).to be true
#       ris = subject.ris.split("\r\n")
#       expect(ris[0]).to eq('TY  - RPRT')
#       expect(ris[1]).to eq('T1  - Eating your own Dog Food')
#       expect(ris[2]).to eq('AU  - Fenner, Martin')
#       expect(ris[3]).to eq('DO  - 10.5438/4k3m-nyvg')
#       expect(ris[4]).to eq('UR  - https://blog.datacite.org/eating-your-own-dog-food/')
#       expect(ris[5]).to eq('AB  - Eating your own dog food is a slang term to describe that an organization should itself use the products and services it provides. For DataCite this means that we should use DOIs with appropriate metadata and strategies for long-term preservation for...')
#       expect(ris[6]).to eq('KW  - datacite')
#       expect(ris[9]).to eq('KW  - FOS: Computer and information sciences')
#       expect(ris[10]).to eq('PY  - 2016')
#       expect(ris[11]).to eq('PB  - DataCite')
#       expect(ris[12]).to eq('LA  - en')
#       expect(ris[13]).to eq('SN  - 10.5438/0000-00ss')
#       expect(ris[14]).to eq('ER  - ')
#     end

#     it 'BlogPosting Citeproc JSON' do
#       input = "#{fixture_path}citeproc.json"
#       subject = described_class.new(input: input, from: 'citeproc')
#       ris = subject.ris.split("\r\n")
#       expect(ris[0]).to eq('TY  - GEN')
#       expect(ris[1]).to eq('T1  - Eating your own Dog Food')
#       expect(ris[2]).to eq('T2  - DataCite Blog')
#       expect(ris[3]).to eq('AU  - Fenner, Martin')
#       expect(ris[4]).to eq('DO  - 10.5438/4k3m-nyvg')
#       expect(ris[5]).to eq('UR  - https://blog.datacite.org/eating-your-own-dog-food')
#       expect(ris[6]).to eq('AB  - Eating your own dog food is a slang term to describe that an organization should itself use the products and services it provides. For DataCite this means that we should use DOIs with appropriate metadata and strategies for long-term preservation for...')
#       expect(ris[7]).to eq('KW  - phylogeny')
#       expect(ris[14]).to eq('PY  - 2016')
#       expect(ris[15]).to eq('PB  - DataCite')
#       expect(ris[16]).to eq('ER  - ')
#     end

#     it 'BlogPosting DataCite JSON' do
#       input = "#{fixture_path}datacite.json"
#       subject = described_class.new(input: input, from: 'datacite_json')
#       ris = subject.ris.split("\r\n")
#       expect(ris[0]).to eq('TY  - RPRT')
#       expect(ris[1]).to eq('T1  - Eating your own Dog Food')
#       expect(ris[2]).to eq('AU  - Fenner, Martin')
#       expect(ris[3]).to eq('DO  - 10.5438/4k3m-nyvg')
#       expect(ris[4]).to eq('AB  - Eating your own dog food is a slang term to describe that an organization should itself use the products and services it provides. For DataCite this means that we should use DOIs with appropriate metadata and strategies for long-term preservation for...')
#       expect(ris[5]).to eq('KW  - datacite')
#       expect(ris[8]).to eq('PY  - 2016')
#       expect(ris[9]).to eq('PB  - DataCite')
#       expect(ris[10]).to eq('SN  - 10.5438/0000-00ss')
#       expect(ris[11]).to eq('ER  - ')
#     end

#     it 'BlogPosting schema.org' do
#       input = 'https://blog.front-matter.io/posts/eating-your-own-dog-food/'
#       subject = described_class.new(input: input, from: 'schema_org')
#       ris = subject.ris.split("\r\n")
#       expect(ris[0]).to eq('TY  - GEN')
#       expect(ris[1]).to eq('T1  - Eating your own Dog Food')
#       expect(ris[2]).to eq('T2  - Front Matter')
#       expect(ris[3]).to eq('AU  - Fenner, Martin')
#       expect(ris[4]).to eq('DO  - 10.53731/r79vxn1-97aq74v-ag58n')
#       expect(ris[5]).to eq('UR  - https://blog.front-matter.io/posts/eating-your-own-dog-food')
#       expect(ris[6]).to eq('AB  - Eating your own dog food is a slang term to describe that an organization should itself use the products and services it provides. For DataCite this means that we should use DOIs with appropriate metadata and strategies for long-term preservation for the scholarly outputs we produce. For the most part this is not research data, but rather technical documents such as the DataCite Schema and its documentation (2016). These outputs also include the posts on this blog, where we discuss topics relev')
#       expect(ris[7]).to eq('KW  - feature')
#       expect(ris[8]).to eq('PY  - 2016')
#       expect(ris[9]).to eq('PB  - Front Matter')
#       expect(ris[10]).to eq('LA  - en')
#       expect(ris[11]).to eq('ER  - ')
#     end

#     it 'Dataset' do
#       input = '10.5061/DRYAD.8515'
#       subject = described_class.new(input: input, from: 'datacite')
#       expect(subject.valid?).to be true
#       ris = subject.ris.split("\r\n")
#       expect(ris[0]).to eq('TY  - DATA')
#       expect(ris[1]).to eq('T1  - Data from: A new malaria agent in African hominids.')
#       expect(ris[2]).to eq('AU  - Ollomo, Benjamin')
#       expect(ris[10]).to eq('DO  - 10.5061/dryad.8515')
#       expect(ris[11]).to eq('UR  - http://datadryad.org/stash/dataset/doi:10.5061/dryad.8515')
#       expect(ris[13]).to eq('KW  - plasmodium')
#       expect(ris[18]).to eq('PB  - Dryad')
#       expect(ris[19]).to eq('LA  - en')
#       expect(ris[20]).to eq('ER  - ')
#     end

#     it 'maremma' do
#       input = 'https://github.com/datacite/maremma'
#       subject = described_class.new(input: input, from: 'codemeta')
#       ris = subject.ris.split("\r\n")
#       expect(ris[0]).to eq('TY  - COMP')
#       expect(ris[1]).to eq('T1  - Maremma: a Ruby library for simplified network calls')
#       expect(ris[2]).to eq('AU  - Fenner, Martin')
#       expect(ris[3]).to eq('DO  - 10.5438/qeg0-3gm3')
#       expect(ris[4]).to eq('UR  - https://github.com/datacite/maremma')
#       expect(ris[5]).to eq('AB  - Ruby utility library for network requests. Based on Faraday and Excon, provides a wrapper for XML/JSON parsing and error handling. All successful responses are returned as hash with key data, all errors in a JSONAPI-friendly hash with key errors.')
#       expect(ris[6]).to eq('KW  - faraday')
#       expect(ris[9]).to eq('PY  - 2017')
#       expect(ris[10]).to eq('PB  - DataCite')
#       expect(ris[11]).to eq('ER  - ')
#     end

#     it 'keywords with subject scheme' do
#       input = 'https://doi.org/10.1594/pangaea.721193'
#       subject = described_class.new(input: input, from: 'datacite')
#       ris = subject.ris.split("\r\n")
#       expect(ris.first).to eq('TY  - DATA')
#       expect(ris).to include('T1  - Seawater carbonate chemistry and processes during experiments with Crassostrea gigas, 2007, supplement to: Kurihara, Haruko; Kato, Shoji; Ishimatsu, Atsushi (2007): Effects of increased seawater pCO2 on early development of the oyster Crassostrea gigas. Aquatic Biology, 1(1), 91-98')
#       expect(ris).to include('AU  - Kurihara, Haruko')
#       expect(ris).to include('DO  - 10.1594/pangaea.721193')
#       expect(ris).to include('UR  - https://doi.pangaea.de/10.1594/PANGAEA.721193')
#       expect(ris).to include('KW  - animalia')
#       expect(ris).to include('KW  - bottles or small containers/aquaria (&lt;20 l)')
#       expect(ris).to include('PY  - 2007')
#       expect(ris).to include('PB  - PANGAEA - Data Publisher for Earth & Environmental Science')
#       expect(ris).to include('LA  - en')
#       expect(ris.last).to eq('ER  - ')
#     end
#   end
# end


@pytest.mark.vcr
def test_write_ris_list():
    """write_ris_list"""
    string = path.join(path.dirname(__file__), "fixtures", "crossref-list.json")
    subject_list = MetadataList(string, via="crossref")
    assert len(subject_list.items) == 20
    ris_list = subject_list.write(to="ris").splitlines()
    assert ris_list[0].startswith("TY  - JOUR")
    assert ris_list[1].startswith(
        "T1  - Hydrocarbon Potential of Columbia Plateau--an Overview: ABSTRACT"
    )
