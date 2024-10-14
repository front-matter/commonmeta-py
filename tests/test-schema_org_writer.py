# pylint: disable=invalid-name
"""Test schema.org writer"""

from os import path
import orjson as json
import pytest

from commonmeta import Metadata


@pytest.mark.vcr
def test_journal_article():
    "journal article"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.7554/elife.01567"
    assert schema_org.get("@type") == "ScholarlyArticle"
    assert (
        schema_org.get("name")
        == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert len(schema_org.get("author")) == 5
    assert schema_org.get("author")[0] == {
        "givenName": "Martial",
        "familyName": "Sankar",
        "name": "Martial Sankar",
        "affiliations": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
            }
        ],
        "@type": "Person",
    }
    assert schema_org.get("description").startswith(
        "Among various advantages, their small size makes model"
    )
    assert schema_org.get("publisher") == {
        "@type": "Organization",
        "name": "eLife Sciences Publications, Ltd",
    }
    assert schema_org.get("datePublished") == "2014-02-11"
    assert schema_org.get("url") == "https://elifesciences.org/articles/01567"
    assert schema_org.get("periodical") == {
        "issn": "2050-084X",
        "@type": "Journal",
        "name": "eLife",
    }
    assert schema_org.get("pageStart") is None
    assert schema_org.get("pageEnd") is None
    assert schema_org.get("inLanguage") == "English"
    assert (
        schema_org.get("license")
        == "https://creativecommons.org/licenses/by/3.0/legalcode"
    )
    assert len(schema_org.get("encoding")) == 2
    assert schema_org.get("encoding")[0] == {
        "@type": "MediaObject",
        "contentUrl": "https://cdn.elifesciences.org/articles/01567/elife-01567-v1.pdf",
        "encodingFormat": "application/pdf",
    }


def test_inveniordm_software():
    "inveniordm software"
    string = path.join(path.dirname(__file__), "fixtures", "inveniordm-software.json")
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.7752775"
    assert subject.type == "Software"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.5281/zenodo.7752775"
    assert schema_org.get("@type") == "SoftwareSourceCode"
    assert schema_org.get("name") == "commonmeta-ruby"
    assert len(schema_org.get("author")) == 1
    assert schema_org.get("author")[0] == {
        "id": "https://orcid.org/0000-0003-1419-2405",
        "givenName": "Martin",
        "familyName": "Fenner",
        "affiliations": [{"name": "Front Matter"}],
        "@type": "Person",
        "name": "Martin Fenner",
    }
    assert schema_org.get("description").startswith(
        "Ruby gem and command-line utility for conversion"
    )
    assert schema_org.get("publisher") == {"@type": "Organization", "name": "Zenodo"}
    assert schema_org.get("datePublished") == "2023-03-20"
    assert schema_org.get("url") == "https://zenodo.org/records/7752775"
    assert schema_org.get("periodical") == {
        "additionalType": "Repository",
        "name": "Zenodo",
    }
    assert schema_org.get("pageStart") is None
    assert schema_org.get("pageEnd") is None
    assert schema_org.get("inLanguage") is None
    assert schema_org.get("license") == "https://opensource.org/licenses/MIT"
    assert len(schema_org.get("encoding")) == 1
    assert schema_org.get("encoding")[0] == {
        "@type": "MediaObject",
        "contentUrl": "https://zenodo.org/api/files/7cd6cc32-96a6-405d-b0ff-1811b378cc69/front-matter/commonmeta-ruby-v3.0.1.zip",
        "encodingFormat": "application/zip",
        "name": "front-matter/commonmeta-ruby-v3.0.1.zip",
        "size": 5061453,
    }
    assert (
        schema_org.get("codeRepository")
        == "https://github.com/front-matter/commonmeta-ruby"
    )


@pytest.mark.vcr
def test_inveniordm_presentation():
    "inveniordm presentation"
    string = "https://zenodo.org/api/records/8173303"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.8173303"
    assert subject.type == "Presentation"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.5281/zenodo.8173303"
    assert schema_org.get("@type") == "PresentationDigitalDocument"
    assert (
        schema_org.get("name")
        == "11 July 2023 (Day 2) CERN – NASA Open Science Summit Sketch Notes"
    )
    assert len(schema_org.get("author")) == 1
    assert schema_org.get("author")[0] == {
        "id": "https://orcid.org/0000-0002-8960-9642",
        "givenName": "Heidi",
        "familyName": "Seibold",
        "@type": "Person",
        "name": "Heidi Seibold",
    }
    assert schema_org.get("description").startswith(
        "CERN/NASA “Accelerating the Adoption of Open Science”"
    )
    assert schema_org.get("publisher") == {"@type": "Organization", "name": "Zenodo"}
    assert schema_org.get("datePublished") == "2023-07-21"
    assert schema_org.get("url") == "https://zenodo.org/records/8173303"
    assert schema_org.get("periodical") == {
        "additionalType": "Repository",
        "name": "Zenodo",
    }
    assert schema_org.get("pageStart") is None
    assert schema_org.get("pageEnd") is None
    assert schema_org.get("inLanguage") is None
    assert (
        schema_org.get("license")
        == "https://creativecommons.org/licenses/by/4.0/legalcode"
    )
    assert len(schema_org.get("encoding")) == 1
    assert schema_org.get("encoding")[0] == {
        "@type": "MediaObject",
        "contentUrl": "https://zenodo.org/api/records/8173303/files/20230711-CERN-NASA-Open-Science-Summit-Summary-Drawings.pdf/content",
        "name": "20230711-CERN-NASA-Open-Science-Summit-Summary-Drawings.pdf",
        "size": 13994803,
    }


@pytest.mark.vcr
def test_inveniordm_publication():
    "inveniordm publication"
    string = "https://zenodo.org/api/records/5244404"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.5244404"
    assert subject.type == "JournalArticle"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.5281/zenodo.5244404"
    assert schema_org.get("@type") == "ScholarlyArticle"
    assert schema_org.get("name") == "The Origins of SARS-CoV-2: A Critical Review"
    assert len(schema_org.get("author")) == 21
    assert schema_org.get("author")[0] == {
        "givenName": "Edward C",
        "familyName": "Holmes",
        "affiliations": [
            {
                "name": "School of Life and Environmental Sciences and School of Medical Sciences, The University of Sydney, Sydney, NSW 2006, Australia"
            }
        ],
        "@type": "Person",
        "name": "Edward C Holmes",
    }
    assert schema_org.get("description").startswith(
        "The Origins of SARS-CoV-2: A Critical Review Holmes et al."
    )
    assert schema_org.get("publisher") == {"@type": "Organization", "name": "Zenodo"}
    assert schema_org.get("datePublished") == "2021-08-18"
    assert schema_org.get("url") == "https://zenodo.org/records/5244404"
    assert schema_org.get("periodical") == {
        "additionalType": "Repository",
        "name": "Zenodo",
    }
    assert schema_org.get("pageStart") is None
    assert schema_org.get("pageEnd") is None
    assert schema_org.get("inLanguage") is None
    assert (
        schema_org.get("license")
        == "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
    )
    assert len(schema_org.get("encoding")) == 3
    assert schema_org.get("encoding")[0] == {
        "@type": "MediaObject",
        "contentUrl": "https://zenodo.org/api/records/5244404/files/Holmes_et_al_(2021)_Cell_Supplementary.pdf/content",
        "name": "Holmes_et_al_(2021)_Cell_Supplementary.pdf",
        "size": 197003,
    }


@pytest.mark.vcr
def test_inveniordm_report():
    "inveniordm report"
    string = "https://zenodo.org/api/records/3871094"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.3871094"
    assert subject.type == "JournalArticle"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.5281/zenodo.3871094"
    assert schema_org.get("@type") == "ScholarlyArticle"
    assert schema_org.get("name") == "An open letter to Mehra et al and The Lancet"
    assert len(schema_org.get("author")) == 1
    assert schema_org.get("author")[0] == {
        "id": "https://orcid.org/0000-0001-5524-0325",
        "givenName": "James Watson on the behalf of 201",
        "familyName": "signatories",
        "affiliations": [{"name": "Mahidol Oxford Tropical Medicine Research Unit"}],
        "@type": "Person",
        "name": "James Watson on the behalf of 201 signatories",
    }
    assert schema_org.get("description").startswith(
        "Open letter to MR Mehra, SS Desai, F Ruschitzka, and AN Patel"
    )
    assert schema_org.get("publisher") == {"@type": "Organization", "name": "Zenodo"}
    assert schema_org.get("datePublished") == "2020-05-28"
    assert schema_org.get("url") == "https://zenodo.org/records/3871094"
    assert schema_org.get("periodical") == {
        "additionalType": "Repository",
        "name": "Zenodo",
    }
    assert schema_org.get("pageStart") is None
    assert schema_org.get("pageEnd") is None
    assert schema_org.get("inLanguage") == "English"
    assert (
        schema_org.get("license")
        == "https://creativecommons.org/licenses/by/4.0/legalcode"
    )
    assert len(schema_org.get("encoding")) == 1
    assert schema_org.get("encoding")[0] == {
        "@type": "MediaObject",
        "contentUrl": "https://zenodo.org/api/records/3871094/files/Open Letter V4.pdf/content",
        "name": "Open Letter V4.pdf",
        "size": 130482,
    }


@pytest.mark.vcr
def test_inveniordm_preprint():
    "inveniordm preprint"
    string = "https://zenodo.org/api/records/8120771"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.8120771"
    assert subject.type == "JournalArticle"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.5281/zenodo.8120771"
    assert schema_org.get("@type") == "ScholarlyArticle"
    assert (
        schema_org.get("name")
        == "A SYSTEMATIC REVIEW OF AUTOPSY FINDINGS IN DEATHS AFTER COVID-19 VACCINATION"
    )
    assert len(schema_org.get("author")) == 9
    assert schema_org.get("author")[0] == {
        "givenName": "BS",
        "familyName": "Nicolas Hulscher",
        "affiliations": [{"name": "University of Michigan School of Public Health"}],
        "@type": "Person",
        "name": "BS Nicolas Hulscher",
    }
    assert schema_org.get("description").startswith(
        "<strong>ABSTRACT</strong> <strong>Background:</strong>"
    )
    assert schema_org.get("publisher") == {"@type": "Organization", "name": "Zenodo"}
    assert schema_org.get("datePublished") == "2023-07-06"
    assert schema_org.get("url") == "https://zenodo.org/records/8120771"
    assert schema_org.get("periodical") == {
        "additionalType": "Repository",
        "name": "Zenodo",
    }
    assert schema_org.get("pageStart") is None
    assert schema_org.get("pageEnd") is None
    assert schema_org.get("inLanguage") == "English"
    assert (
        schema_org.get("license")
        == "https://creativecommons.org/licenses/by/4.0/legalcode"
    )
    assert len(schema_org.get("encoding")) == 2
    assert schema_org.get("encoding")[0] == {
        "@type": "MediaObject",
        "contentUrl": "https://zenodo.org/api/records/8120771/files/(Zenodo) AUTOPSY REVIEW MANUSCRIPT.pdf/content",
        "name": "(Zenodo) AUTOPSY REVIEW MANUSCRIPT.pdf",
        "size": 832057,
    }


@pytest.mark.vcr
def test_inveniordm_dataset():
    "inveniordm dataset"
    string = "https://zenodo.org/api/records/7834392"
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.5281/zenodo.7834392"
    assert subject.type == "Dataset"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.5281/zenodo.7834392"
    assert schema_org.get("@type") == "Dataset"
    assert (
        schema_org.get("name")
        == "A large-scale COVID-19 Twitter chatter dataset for open scientific research - an international collaboration"
    )
    assert len(schema_org.get("author")) == 9
    assert schema_org.get("author")[0] == {
        "id": "https://orcid.org/0000-0001-8499-824X",
        "givenName": "Juan M.",
        "familyName": "Banda",
        "affiliations": [{"name": "Georgia State University"}],
        "@type": "Person",
        "name": "Juan M. Banda",
    }
    assert schema_org.get("description").startswith(
        "<em><strong>Version 162&nbsp;of the dataset."
    )
    assert schema_org.get("publisher") == {"@type": "Organization", "name": "Zenodo"}
    assert schema_org.get("datePublished") == "2023-04-16"
    assert schema_org.get("url") == "https://zenodo.org/records/7834392"
    assert schema_org.get("inDataCatalog") is None
    assert schema_org.get("pageStart") is None
    assert schema_org.get("pageEnd") is None
    assert schema_org.get("inLanguage") == "English"
    assert schema_org.get("license") is None
    assert len(schema_org.get("distribution")) == 24
    assert schema_org.get("distribution")[0] == {
        "@type": "DataDownload",
        "contentUrl": "https://zenodo.org/api/records/7834392/files/frequent_trigrams.csv/content",
        "name": "frequent_trigrams.csv",
        "size": 24991,
    }


def test_article_with_pages():
    "article with pages"
    text = "https://doi.org/10.1371/journal.ppat.1008184"
    subject = Metadata(text)
    assert subject.id == "https://doi.org/10.1371/journal.ppat.1008184"
    assert subject.type == "JournalArticle"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.1371/journal.ppat.1008184"
    assert schema_org.get("@type") == "ScholarlyArticle"
    assert (
        schema_org.get("name")
        == "An RNA thermometer dictates production of a secreted bacterial toxin"
    )
    assert len(schema_org.get("author")) == 5
    assert schema_org.get("author")[0] == {
        "@type": "Person",
        "familyName": "Twittenhoff",
        "givenName": "Christian",
        "name": "Christian Twittenhoff",
    }
    assert schema_org.get("editor") == [
        {
            "givenName": "Guy",
            "familyName": "Tran Van Nhieu",
            "@type": "Person",
            "name": "Guy Tran Van Nhieu",
        }
    ]
    assert schema_org.get("description") is None
    assert schema_org.get("publisher") == {
        "@type": "Organization",
        "name": "Public Library of Science (PLoS)",
    }
    assert schema_org.get("datePublished") == "2020-01-17"
    assert schema_org.get("url") == "https://dx.plos.org/10.1371/journal.ppat.1008184"
    assert schema_org.get("periodical") == {
        "issn": "1553-7374",
        "@type": "Journal",
        "name": "PLOS Pathogens",
    }
    assert schema_org.get("pageStart") == "e1008184"
    assert schema_org.get("pageEnd") is None
    assert schema_org.get("inLanguage") == "English"
    assert (
        schema_org.get("license")
        == "https://creativecommons.org/licenses/by/4.0/legalcode"
    )
    assert schema_org.get("encoding") is None


def test_instrument():
    "instrument"
    string = path.join(path.dirname(__file__), "fixtures", "datacite-instrument.json")
    subject = Metadata(string)
    assert subject.id == "https://doi.org/10.82433/08qf-ee96"
    assert subject.type == "Instrument"

    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.82433/08qf-ee96"
    assert schema_org.get("@type") == "Instrument"
    assert schema_org.get("name") == "Pilatus detector at MX station 14.1"


#     it 'maremma schema.org JSON' do
#       text = 'https://github.com/datacite/maremma'
#       subject = described_class.new(input: input, from: 'codemeta')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5438/qeg0-3gm3')
#       expect(json['@type']).to eq('SoftwareSourceCode')
#       expect(json['name']).to eq('Maremma: a Ruby library for simplified network calls')
#       expect(json['author']).to eq('name' => 'Martin Fenner', 'givenName' => 'Martin',
#                                    'familyName' => 'Fenner', '@type' => 'Person', '@id' => 'https://orcid.org/0000-0003-0077-4738', 'affiliation' => { '@type' => 'Organization', 'name' => 'DataCite' })
#     end

#     it 'Schema.org JSON' do
#       text = 'https://doi.org/10.5281/ZENODO.48440'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5281/zenodo.48440')
#       expect(json['@type']).to eq('SoftwareSourceCode')
#       expect(json['name']).to eq('Analysis Tools For Crossover Experiment Of Ui Using Choice Architecture')
#       expect(json['license']).to eq(['https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode',
#                                      'info:eu-repo/semantics/openAccess'])
#     end

#     it 'Another Schema.org JSON' do
#       text = 'https://doi.org/10.5061/DRYAD.8515'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5061/dryad.8515')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['license']).to eq('https://creativecommons.org/publicdomain/zero/1.0/legalcode')
#       expect(json['keywords']).to eq('plasmodium, malaria, mitochondrial genome, parasites')
#     end

#     it 'Schema.org JSON IsSupplementTo' do
#       text = 'https://doi.org/10.5517/CC8H01S'
#       subject = described_class.new(input: input)
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5517/cc8h01s')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['@reverse']).to eq('isBasedOn' => {
#                                        '@id' => 'https://doi.org/10.1107/s1600536804021154', '@type' => 'ScholarlyArticle'
#                                      })
#     end

#     it 'Schema.org JSON Cyark' do
#       text = 'https://doi.org/10.26301/jgf3-jm06'
#       subject = described_class.new(input: input)
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.26301/jgf3-jm06')
#       expect(json['@type']).to eq('Dataset')
#     end

#     it 'rdataone' do
#       text = "#{fixture_path}codemeta.json"
#       subject = described_class.new(input: input, from: 'codemeta')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5063/f1m61h5x')
#       expect(json['@type']).to eq('SoftwareSourceCode')
#       expect(json['name']).to eq('R Interface to the DataONE REST API')
#       expect(json['author']).to eq([{ 'name' => 'Matt Jones',
#                                       'givenName' => 'Matt',
#                                       'familyName' => 'Jones',
#                                       '@type' => 'Person',
#                                       '@id' => 'https://orcid.org/0000-0003-0077-4738',
#                                       'affiliation' => { '@type' => 'Organization',
#                                                          'name' => 'NCEAS' } },
#                                     { 'name' => 'Peter Slaughter',
#                                       'givenName' => 'Peter',
#                                       'familyName' => 'Slaughter',
#                                       '@type' => 'Person',
#                                       '@id' => 'https://orcid.org/0000-0002-2192-403X',
#                                       'affiliation' => { '@type' => 'Organization',
#                                                          'name' => 'NCEAS' } },
#                                     { "@type"=>"Organization",
#                                       "name"=>"University of California, Santa Barbara" }])
#       expect(json['version']).to eq('2.0.0')
#       expect(json['keywords']).to eq('data sharing, data repository, dataone')
#     end

#     it 'Funding' do
#       text = 'https://doi.org/10.5438/6423'
#       subject = described_class.new(input: input)
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5438/6423')
#       expect(json['@type']).to eq('Collection')
#       expect(json['hasPart'].length).to eq(25)
#       expect(json['hasPart'].first).to eq('@type' => 'CreativeWork', '@id' => 'https://doi.org/10.5281/zenodo.30799')
#       expect(json['funder']).to eq('@id' => 'https://doi.org/10.13039/501100000780',
#                                    '@type' => 'Organization', 'name' => 'European Commission')
#       expect(json['license']).to eq('https://creativecommons.org/licenses/by/4.0/legalcode')
#     end

#     it 'Funding OpenAIRE' do
#       text = 'https://doi.org/10.5281/ZENODO.1239'
#       subject = described_class.new(input: input)
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5281/zenodo.1239')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['funder']).to eq('@id' => 'https://doi.org/10.13039/501100000780',
#                                    '@type' => 'Organization', 'name' => 'European Commission')
#       expect(json['license']).to eq(['https://creativecommons.org/publicdomain/zero/1.0/legalcode',
#                                      'info:eu-repo/semantics/openAccess'])
#     end

#     it 'subject scheme' do
#       text = 'https://doi.org/10.4232/1.2745'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.4232/1.2745')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['name']).to eq('Flash Eurobarometer 54 (Madrid Summit)')
#       expect(json['keywords']).to eq('KAT12 International Institutions, Relations, Conditions, Internationale Politik und Institutionen, Regierung, politische Systeme, Parteien und Verbände, Wirtschaftssysteme und wirtschaftliche Entwicklung, International politics and organisation, Government, political systems and organisation, Economic systems and development')
#     end

#     it 'subject scheme multiple keywords' do
#       text = 'https://doi.org/10.1594/pangaea.721193'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.1594/pangaea.721193')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['name']).to eq('Seawater carbonate chemistry and processes during experiments with Crassostrea gigas, 2007, supplement to: Kurihara, Haruko; Kato, Shoji; Ishimatsu, Atsushi (2007): Effects of increased seawater pCO2 on early development of the oyster Crassostrea gigas. Aquatic Biology, 1(1), 91-98')
#       expect(json['keywords']).to include('animalia, bottles or small containers/aquaria (&lt;20 l)')
#       expect(json['license']).to eq('https://creativecommons.org/licenses/by/3.0/legalcode')
#     end

#     it 'author is organization' do
#       text = "#{fixture_path}gtex.xml"
#       url = 'https://ors.datacite.org/doi:/10.25491/9hx8-ke93'
#       content_url = 'https://storage.googleapis.com/gtex_analysis_v7/single_tissue_eqtl_data/GTEx_Analysis_v7_eQTL_expression_matrices.tar.gz'
#       subject = described_class.new(input: input, url: url, content_url: content_url,
#                                     from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.25491/9hx8-ke93')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['author']).to eq('@type' => 'Organization', 'name' => 'The GTEx Consortium')
#       expect(json['url']).to eq('https://ors.datacite.org/doi:/10.25491/9hx8-ke93')
#       expect(json['encodingFormat']).to eq('application/tar')
#       expect(json['contentSize']).to eq('15.7M')
#       expect(json['contentUrl']).to eq('https://storage.googleapis.com/gtex_analysis_v7/single_tissue_eqtl_data/GTEx_Analysis_v7_eQTL_expression_matrices.tar.gz')
#       expect(json['includedInDataCatalog']).to eq(
#         '@id' => 'https://www.ebi.ac.uk/miriam/main/datatypes/MIR:00000663', '@type' => 'DataCatalog', 'name' => 'GTEx'
#       )
#       expect(json['@reverse']).to eq('isBasedOn' => { '@id' => 'https://doi.org/10.1038/nmeth.4407',
#                                                       '@type' => 'ScholarlyArticle' })
#     end

#     it 'series information' do
#       text = '10.4229/23RDEUPVSEC2008-5CO.8.3'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.4229/23rdeupvsec2008-5co.8.3')
#       expect(json['@type']).to eq('ScholarlyArticle')
#       expect(json['name']).to eq('Rural Electrification With Hybrid Power Systems Based on Renewables - Technical System Configurations From the Point of View of the European Industry')
#       expect(json['author'].count).to eq(3)
#       expect(json['author'].first).to eq("name"=>"Llamas, P.")
#       expect(json['periodical']).to eq('@type' => 'Series', 'firstPage' => 'Spain; 3353',
#                                        'lastPage' => '3356', 'name' => '23rd European Photovoltaic Solar Energy Conference and Exhibition', 'volume' => '1-5 September 2008')
#     end

#     it 'data catalog' do
#       text = '10.25491/8KMC-G314'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.25491/8kmc-g314')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['name']).to eq('Covariates used in eQTL analysis. Includes genotyping principal components and PEER factors')
#       expect(json['author']).to eq('@type' => 'Organization', 'name' => 'The GTEx Consortium')
#       expect(json['includedInDataCatalog']).to eq('@type' => 'DataCatalog', 'name' => 'GTEx')
#       expect(json['identifier']).to eq('@type' => 'PropertyValue', 'propertyID' => 'md5',
#                                        'value' => 'c7c89fe7366d50cd75448aa603c9de58')
#       expect(json['contentUrl']).to eq('https://storage.googleapis.com/gtex_analysis_v7/single_tissue_eqtl_data/GTEx_Analysis_v7_eQTL_covariates.tar.gz')
#     end

#     it 'alternate identifiers' do
#       text = '10.23725/8na3-9s47'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.23725/8na3-9s47')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['name']).to eq('NWD165827.recab.cram')
#       expect(json['author']).to eq("name"=>"TOPMed")
#       expect(json['includedInDataCatalog'].nil?).to be(true)
#       expect(json['identifier']).to eq(
#         [{ '@type' => 'PropertyValue',
#            'propertyID' => 'minid',
#            'value' => 'ark:/99999/fk41CrU4eszeLUDe' },
#          { '@type' => 'PropertyValue',
#            'propertyID' => 'dataguid',
#            'value' => 'dg.4503/c3d66dc9-58da-411c-83c4-dd656aa3c4b7' },
#          { '@type' => 'PropertyValue',
#            'propertyID' => 'md5',
#            'value' => '3b33f6b9338fccab0901b7d317577ea3' }]
#       )
#       expect(json['contentUrl']).to include(
#         's3://cgp-commons-public/topmed_open_access/197bc047-e917-55ed-852d-d563cdbc50e4/NWD165827.recab.cram', 'gs://topmed-irc-share/public/NWD165827.recab.cram'
#       )
#     end

#     it 'affiliation identifier' do
#       text = "#{fixture_path}datacite-example-affiliation.xml"
#       subject = described_class.new(input: input)
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5072/example-full')
#       expect(json['@type']).to eq('SoftwareSourceCode')
#       expect(json['name']).to eq('Full DataCite XML Example')
#       expect(json['author'].length).to eq(3)
#       expect(json['author'].first).to eq('@id' => 'https://orcid.org/0000-0001-5000-0007',
#                                          '@type' => 'Person',
#                                          'affiliation' => { '@id' => 'https://ror.org/04wxnsj81', '@type' => 'Organization',
#                                                             'name' => 'DataCite' },
#                                          'familyName' => 'Miller',
#                                          'givenName' => 'Elizabeth',
#                                          'name' => 'Elizabeth Miller')
#       expect(json['identifier']).to eq(
#         { '@type' => 'PropertyValue',
#           'propertyID' => 'URL',
#           'value' => 'https://schema.datacite.org/meta/kernel-4.2/example/datacite-example-full-v4.2.xml' }
#       )
#       expect(json['license']).to eq('https://creativecommons.org/publicdomain/zero/1.0/legalcode')
#     end

#     it 'geo_location_point' do
#       text = "#{fixture_path}datacite-example-geolocation-2.xml"
#       doi = '10.6071/Z7WC73'
#       subject = described_class.new(input: input, doi: doi)
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.6071/z7wc73')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['name']).to eq('Southern Sierra Critical Zone Observatory (SSCZO), Providence Creek meteorological data, soil moisture and temperature, snow depth and air temperature')
#       expect(json['author'].length).to eq(6)
#       expect(json['author'][2]).to eq('@id' => 'https://orcid.org/0000-0002-8862-1404',
#                                       '@type' => 'Person', 'familyName' => 'Stacy', 'givenName' => 'Erin', 'name' => 'Erin Stacy', 'affiliation' => { '@type' => 'Organization', 'name' => 'UC Merced' })
#       expect(json['includedInDataCatalog'].nil?).to be(true)
#       expect(json['spatialCoverage']).to eq([{ '@type' => 'Place',
#                                                'geo' =>
#         { '@type' => 'GeoCoordinates',
#           'address' => 'Providence Creek (Lower, Upper and P301)',
#           'latitude' => '37.047756',
#           'longitude' => '-119.221094' } },
#                                              { '@type' => 'Place',
#                                                'geo' =>
#                                              { '@type' => 'GeoShape',
#                                                'address' => 'Providence Creek (Lower, Upper and P301)',
#                                                'box' => '37.046 -119.211 37.075 -119.182' } }])
#       expect(json['license']).to eq('https://creativecommons.org/licenses/by/4.0/legalcode')
#     end

#     it 'geo_location_box' do
#       text = '10.1594/PANGAEA.842237'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.1594/pangaea.842237')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['name']).to eq('Registry of all stations from the Tara Oceans Expedition (2009-2013)')
#       expect(json['author']).to eq([{ "@type"=>"Person", 'familyName' => 'Tara Oceans Consortium',
#                                       'givenName' => 'Coordinators',
#                                       'name' => 'Coordinators Tara Oceans Consortium' },
#                                     { "@type"=>"Person", 'familyName' => 'Tara Oceans Expedition',
#                                       'givenName' => 'Participants',
#                                       'name' => 'Participants Tara Oceans Expedition' }])
#       expect(json['includedInDataCatalog'].nil?).to be(true)
#       expect(json['spatialCoverage']).to eq('@type' => 'Place',
#                                             'geo' => {
#                                               '@type' => 'GeoShape', 'box' => '-64.3088 -168.5182 79.6753 174.9006'
#                                             })
#       expect(json['license']).to eq('https://creativecommons.org/licenses/by/3.0/legalcode')
#     end

#     it 'geo_location_polygon' do
#       text = "#{fixture_path}datacite-example-polygon-v4.1.xml"
#       subject = described_class.new(input: input)
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.5072/example-polygon')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['name']).to eq('Meteo measurements at the Sand Motor')
#       expect(json['author']).to eq('@type' => 'Person', 'familyName' => 'den Heijer', 'givenName' => 'C',
#                                    'name' => 'C den Heijer')
#       expect(json['includedInDataCatalog'].nil?).to be(true)
#       expect(json['spatialCoverage'].dig('geo', 'polygon').length).to eq(34)
#       expect(json['spatialCoverage'].dig('geo',
#                                          'polygon')[0].first).to eq(['4.1738852605822',
#                                                                      '52.03913926329928'])
#     end

#     it 'from schema_org gtex' do
#       text = "#{fixture_path}schema_org_gtex.json"
#       subject = described_class.new(input: input, from: 'schema_org')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.25491/d50j-3083')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['identifier']).to eq('@type' => 'PropertyValue', 'propertyID' => 'md5',
#                                        'value' => '687610993')
#       expect(json['url']).to eq('https://ors.datacite.org/doi:/10.25491/d50j-3083')
#       expect(json['additionalType']).to eq('Gene expression matrices')
#       expect(json['name']).to eq('Fully processed, filtered and normalized gene expression matrices (in BED format) for each tissue, which were used as text into FastQTL for eQTL discovery')
#       expect(json['version']).to eq('v7')
#       expect(json['author']).to eq('@type' => 'Organization', 'name' => 'The GTEx Consortium')
#       expect(json['keywords']).to eq('gtex, annotation, phenotype, gene regulation, transcriptomics')
#       expect(json['datePublished']).to eq('2017')
#       expect(json['contentUrl']).to eq('https://storage.googleapis.com/gtex_analysis_v7/single_tissue_eqtl_data/GTEx_Analysis_v7_eQTL_expression_matrices.tar.gz')
#       expect(json['schemaVersion']).to eq('http://datacite.org/schema/kernel-4')
#       expect(json['includedInDataCatalog']).to eq('@type' => 'DataCatalog', 'name' => 'GTEx')
#       expect(json['publisher']).to eq('@type' => 'Organization', 'name' => 'GTEx')
#       expect(json['funder']).to eq([{ '@id' => 'https://doi.org/10.13039/100000052',
#                                       'name' => 'Common Fund of the Office of the Director of the NIH',
#                                       '@type' => 'Organization' },
#                                     { '@id' => 'https://doi.org/10.13039/100000054',
#                                       'name' => 'National Cancer Institute (NCI)',
#                                       '@type' => 'Organization' },
#                                     { '@id' => 'https://doi.org/10.13039/100000051',
#                                       'name' => 'National Human Genome Research Institute (NHGRI)',
#                                       '@type' => 'Organization' },
#                                     { '@id' => 'https://doi.org/10.13039/100000050',
#                                       'name' => 'National Heart, Lung, and Blood Institute (NHLBI)',
#                                       '@type' => 'Organization' },
#                                     { '@id' => 'https://doi.org/10.13039/100000026',
#                                       'name' => 'National Institute on Drug Abuse (NIDA)',
#                                       '@type' => 'Organization' },
#                                     { '@id' => 'https://doi.org/10.13039/100000025',
#                                       'name' => 'National Institute of Mental Health (NIMH)',
#                                       '@type' => 'Organization' },
#                                     { '@id' => 'https://doi.org/10.13039/100000065',
#                                       'name' => 'National Institute of Neurological Disorders and Stroke (NINDS)',
#                                       '@type' => 'Organization' }])
#       expect(json['provider']).to eq('@type' => 'Organization', 'name' => 'DataCite')
#     end

#     it 'from schema_org topmed' do
#       text = "#{fixture_path}schema_org_topmed.json"
#       subject = described_class.new(input: input, from: 'schema_org')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.23725/8na3-9s47')
#       expect(json['@type']).to eq('Dataset')
#       expect(json['identifier']).to eq(
#         [{ '@type' => 'PropertyValue',
#            'propertyID' => 'md5',
#            'value' => '3b33f6b9338fccab0901b7d317577ea3' },
#          { '@type' => 'PropertyValue',
#            'propertyID' => 'minid',
#            'value' => 'ark:/99999/fk41CrU4eszeLUDe' },
#          { '@type' => 'PropertyValue',
#            'propertyID' => 'dataguid',
#            'value' => 'dg.4503/c3d66dc9-58da-411c-83c4-dd656aa3c4b7' }]
#       )
#       expect(json['url']).to eq('https://ors.datacite.org/doi:/10.23725/8na3-9s47')
#       expect(json['additionalType']).to eq('CRAM file')
#       expect(json['name']).to eq('NWD165827.recab.cram')
#       expect(json['author']).to eq('@type' => 'Organization', 'name' => 'TOPMed IRC')
#       expect(json['keywords']).to eq('topmed, whole genome sequencing')
#       expect(json['datePublished']).to eq('2017-11-30')
#       expect(json['contentUrl']).to eq([
#                                          's3://cgp-commons-public/topmed_open_access/197bc047-e917-55ed-852d-d563cdbc50e4/NWD165827.recab.cram', 'gs://topmed-irc-share/public/NWD165827.recab.cram'
#                                        ])
#       expect(json['schemaVersion']).to eq('http://datacite.org/schema/kernel-4')
#       expect(json['publisher']).to eq('@type' => 'Organization', 'name' => 'TOPMed')
#       expect(json['citation']).to eq('@id' => 'https://doi.org/10.23725/2g4s-qv04',
#                                      '@type' => 'Dataset')
#       expect(json['funder']).to eq('@id' => 'https://doi.org/10.13039/100000050',
#                                    '@type' => 'Organization', 'name' => 'National Heart, Lung, and Blood Institute (NHLBI)')
#       expect(json['provider']).to eq('@type' => 'Organization', 'name' => 'DataCite')
#     end

#     it 'interactive resource without dates' do
#       text = 'https://doi.org/10.34747/g6yb-3412'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.schema_org)
#       expect(json['@id']).to eq('https://doi.org/10.34747/g6yb-3412')
#       expect(json['@type']).to eq('CreativeWork')
#       expect(json['datePublished']).to eq('2019')
#     end
#   end
# end


@pytest.mark.vcr
def test_json_feed_item_upstream_blog():
    """json_feed_item upstream blog"""
    string = "https://api.rogue-scholar.org/posts/5d14ffac-b9ac-4e20-bdc0-d9248df4e80d"
    subject = Metadata(string)
    assert subject.is_valid
    assert subject.id == "https://doi.org/10.54900/n6dnt-xpq48"
    assert subject.type == "Article"
    schema_org = json.loads(subject.write(to="schema_org"))
    assert schema_org.get("@id") == "https://doi.org/10.54900/n6dnt-xpq48"
    assert schema_org.get("@type") == "Article"
    assert (
        schema_org.get("name")
        == "Attempts at automating journal subject classification"
    )
    assert len(schema_org.get("encoding")) == 4
    assert schema_org.get("encoding")[1] == {
        "@type": "MediaObject",
        "contentUrl": "https://api.rogue-scholar.org/posts/10.54900/n6dnt-xpq48.pdf",
        "encodingFormat": "application/pdf",
    }
