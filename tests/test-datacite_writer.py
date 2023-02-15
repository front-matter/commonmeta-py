import pytest
from os import path
import json
from talbot import Metadata


@pytest.mark.vcr
def test_write_metadata_as_datacite_json():
    """Write metadata as datacite json"""
    subject = Metadata("10.7554/eLife.01567")
    assert subject.pid == "https://doi.org/10.7554/elife.01567"

    datacite = json.loads(subject.datacite())
    assert datacite["id"] == "https://doi.org/10.7554/elife.01567"
    assert datacite["doi"] == "10.7554/elife.01567"
    assert datacite["url"] == "https://elifesciences.org/articles/01567"
    assert datacite["types"] == {
        "bibtex": "article",
        "citeproc": "article-journal",
        "resourceType": "JournalArticle",
        "resourceTypeGeneral": "JournalArticle",
        "ris": "JOUR",
        "schemaOrg": "ScholarlyArticle",
    }
    assert datacite["titles"] == [
        {"title": "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"}
    ]
    assert len(datacite["relatedItems"]) == 28
    assert datacite["relatedItems"][0] == {'relationType': 'IsPartOf', 'relatedItemIdentifierType': 'ISSN',
                                           'resourceTypeGeneral': 'Collection', 'relatedItemIdentifier': '2050-084X'}
    assert datacite["rightsList"] == [
        {
            "rights": "Creative Commons Attribution 3.0 Unported",
            "rightsIdentifier": "cc-by-3.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/3.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]


def test_with_orcid_id():
    """With ORCID ID"""
    subject = Metadata("https://doi.org/10.1155/2012/291294")
    assert subject.pid == "https://doi.org/10.1155/2012/291294"

    datacite = json.loads(subject.datacite())
    print(datacite['creators'])
    assert datacite["creators"][2]["name"] == 'Hernandez, Beatriz'
    assert datacite["creators"][2]["nameIdentifiers"][0]["nameIdentifier"] == "https://orcid.org/0000-0003-2043-4925"
    assert datacite["creators"][2]["nameIdentifiers"][0]["nameIdentifierScheme"] == "ORCID"
    assert datacite["creators"][2]["nameIdentifiers"][0]["schemeUri"] == "https://orcid.org"


def test_with_data_citation():
    """with data citation"""
    subject = Metadata("10.7554/eLife.01567")
    assert subject.pid == "https://doi.org/10.7554/elife.01567"

    datacite = json.loads(subject.datacite())
    assert datacite["url"] == "https://elifesciences.org/articles/01567"
    assert datacite["types"] == {
        "bibtex": "article",
        "citeproc": "article-journal",
        "resourceType": "JournalArticle",
        "resourceTypeGeneral": "JournalArticle",
        "ris": "JOUR",
        "schemaOrg": "ScholarlyArticle",
    }
    assert datacite["titles"] == [
        {"title": "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"}
    ]
    assert len(datacite["relatedItems"]) == 28
    assert datacite["relatedItems"][0] == {'relationType': 'IsPartOf', 'relatedItemIdentifierType': 'ISSN',
                                           'resourceTypeGeneral': 'Collection', 'relatedItemIdentifier': '2050-084X'}
    assert datacite["rightsList"] == [
        {
            "rights": "Creative Commons Attribution 3.0 Unported",
            "rightsIdentifier": "cc-by-3.0",
            "rightsIdentifierScheme": "SPDX",
            "rightsUri": "https://creativecommons.org/licenses/by/3.0/legalcode",
            "schemeUri": "https://spdx.org/licenses/",
        }
    ]

#     it 'Crossref DOI' do
#       input = "#{fixture_path}crossref.bib"
#       subject = described_class.new(input: input, from: 'bibtex')
#       datacite = JSON.parse(subject.datacite_json)
#       expect(datacite.fetch('types')).to eq('bibtex' => 'article', 'citeproc' => 'article-journal',
#                                             'resourceType' => 'JournalArticle', 'resourceTypeGeneral' => 'JournalArticle', 'ris' => 'JOUR', 'schemaOrg' => 'ScholarlyArticle')
#       expect(datacite.fetch('titles')).to eq([{ 'title' => 'Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth' }])
#       expect(datacite.dig('descriptions', 0,
#                           'description')).to start_with('Among various advantages, their small size makes model organisms preferred subjects of investigation.')
#       expect(datacite.fetch('creators').length).to eq(5)
#       expect(datacite.fetch('creators').first).to eq('nameType' => 'Personal',
#                                                      'name' => 'Sankar, Martial', 'givenName' => 'Martial', 'familyName' => 'Sankar')
#     end


def test_blogposting_citeproc_json():
    """BlogPosting Citeproc JSON"""
    data = path.join(path.dirname(__file__), 'fixtures', 'citeproc.json')
    subject = Metadata(data)
    assert subject.pid == "https://doi.org/10.5438/4k3m-nyvg"

    datacite = json.loads(subject.datacite())
    assert datacite["url"] == "https://blog.datacite.org/eating-your-own-dog-food"
    assert datacite["types"] == {
        "bibtex": "article",
        "citeproc": "post-weblog",
        "resourceTypeGeneral": "Text",
        "ris": "GEN",
        "schemaOrg": "BlogPosting",
    }
    assert datacite["titles"] == [
        {"title": "Eating your own Dog Food"}
    ]
    assert datacite["descriptions"][0]["description"].startswith(
        "Eating your own dog food")
    assert datacite["creators"] == [
        {'name': 'Fenner, Martin', 'givenName': 'Martin', 'familyName': 'Fenner', 'nameType': 'Personal'}]


def test_rdataone():
    """Rdataone"""
    data = path.join(path.dirname(__file__), 'fixtures', 'codemeta.json')
    subject = Metadata(data)
    assert subject.pid == "https://doi.org/10.5063/f1m61h5x"

    datacite = json.loads(subject.datacite())
    assert datacite["titles"] == [
        {"title": "R Interface to the DataONE REST API"}
    ]
    assert len(datacite["creators"]) == 3
    assert datacite["creators"][0] == {
        'name': 'Matt Jones', 'nameType': 'Personal', 'affiliation': [{'name': 'NCEAS'}]}
    assert datacite["version"] == "2.0.0"


#     it 'maremma' do
#       input = 'https://github.com/datacite/maremma'
#       subject = described_class.new(input: input, from: 'codemeta')
#       datacite = JSON.parse(subject.datacite_json)
#       expect(datacite.fetch('titles')).to eq([{ 'title' => 'Maremma: a Ruby library for simplified network calls' }])
#       expect(datacite.fetch('creators')).to eq([{ 'affiliation' => [{ 'name' => 'DataCite' }],
#                                                   'familyName' => 'Fenner',
#                                                   'givenName' => 'Martin',
#                                                   'name' => 'Fenner, Martin',
#                                                   'nameIdentifiers' =>
#          [{ 'nameIdentifier' => 'https://orcid.org/0000-0003-0077-4738',
#             'nameIdentifierScheme' => 'ORCID', 'schemeUri' => 'https://orcid.org' }],
#                                                   'nameType' => 'Personal' }])
#     end


def test_from_schema_org():
    """Schema.org"""
    subject = Metadata(
        'https://blog.front-matter.io/posts/eating-your-own-dog-food/')
    assert subject.pid == "https://doi.org/10.53731/r79vxn1-97aq74v-ag58n"

    datacite = json.loads(subject.datacite())
    assert datacite["doi"] == "10.53731/r79vxn1-97aq74v-ag58n"
    assert datacite["url"] == "https://blog.front-matter.io/posts/eating-your-own-dog-food"
    assert datacite["titles"] == [
        {"title": "Eating your own Dog Food"}
    ]
    assert datacite["creators"] == [
        {
            "name": "Martin Fenner",
            "nameType": "Personal",
        }
    ]
    assert datacite["descriptions"][0]["description"].startswith(
        "Eating your own dog food")
    assert datacite["types"] == {
        "bibtex": "article",
        "citeproc": "article-newspaper",
        "resourceTypeGeneral": "Preprint",
        "ris": "GEN",
        "schemaOrg": "Article",
    }