# pylint: disable=invalid-name
"""Citeproc JSON reader tests"""

from os import path
from commonmeta import Metadata, MetadataList


def test_default():
    "default"
    string = path.join(path.dirname(__file__), "fixtures", "commonmeta.json")
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
        "affiliation": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
            }
        ],
    }
    assert subject.license == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }

    assert subject.date == {
        "published": "2014-02-11",
        "updated": "2022-03-26",
    }
    assert subject.publisher == {
        "id": "https://api.crossref.org/members/4374",
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
    assert subject.funding_references == [
        {"funderName": "SystemsX"},
        {"funderName": "EMBO longterm post-doctoral fellowships"},
        {"funderName": "Marie Heim-Voegtlin"},
        {
            "funderName": "University of Lausanne",
            "funderIdentifier": "https://doi.org/10.13039/501100006390",
            "funderIdentifierType": "Crossref Funder ID",
        },
        {"funderName": "SystemsX"},
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
        {
            "funderIdentifier": "https://doi.org/10.13039/501100006390",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "University of Lausanne",
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
    assert subject.subjects == []
    assert subject.language is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "https://cdn.elifesciences.org/articles/01567/elife-01567-v1.pdf",
        "mimeType": "application/pdf",
    }


def test_string():
    "string"
    string = """{
  "id": "https://doi.org/10.7554/elife.01567",
  "type": "JournalArticle",
  "url": "https://elifesciences.org/articles/01567",
  "titles": [
    {
      "title": "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    }
  ],
  "contributors": [
    {
      "type": "Person",
      "contributorRoles": ["Author"],
      "givenName": "Martial",
      "familyName": "Sankar",
      "affiliation": [
        {
          "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
        }
      ]
    },
    {
      "type": "Person",
      "contributorRoles": ["Author"],
      "givenName": "Kaisa",
      "familyName": "Nieminen",
      "affiliation": [
        {
          "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
        }
      ]
    },
    {
      "type": "Person",
      "contributorRoles": ["Author"],
      "givenName": "Laura",
      "familyName": "Ragni",
      "affiliation": [
        {
          "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
        }
      ]
    },
    {
      "type": "Person",
      "contributorRoles": ["Author"],
      "givenName": "Ioannis",
      "familyName": "Xenarios",
      "affiliation": [
        {
          "name": "Vital-IT, Swiss Institute of Bioinformatics, Lausanne, Switzerland"
        }
      ]
    },
    {
      "type": "Person",
      "contributorRoles": ["Author"],
      "givenName": "Christian S",
      "familyName": "Hardtke",
      "affiliation": [
        {
          "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
        }
      ]
    }
  ],
  "container": {
    "type": "Journal",
    "title": "eLife",
    "identifier": "2050-084X",
    "identifierType": "ISSN",
    "volume": "3"
  },
  "publisher": {
    "id": "https://api.crossref.org/members/4374",
    "name": "eLife Sciences Publications, Ltd"
  },
  "references": [
    {
      "key": "bib1",
      "doi": "https://doi.org/10.1038/nature02100",
      "contributor": "Bonke",
      "title": "APL regulates vascular tissue identity in Arabidopsis",
      "publicationYear": "2003",
      "volume": "426",
      "firstPage": "181",
      "containerTitle": "Nature"
    },
    {
      "key": "bib2",
      "doi": "https://doi.org/10.1534/genetics.109.104976",
      "contributor": "Brenner",
      "title": "In the beginning was the worm",
      "publicationYear": "2009",
      "volume": "182",
      "firstPage": "413",
      "containerTitle": "Genetics"
    },
    {
      "key": "bib3",
      "doi": "https://doi.org/10.1034/j.1399-3054.2002.1140413.x",
      "contributor": "Chaffey",
      "title": "Secondary xylem development in Arabidopsis: a model for wood formation",
      "publicationYear": "2002",
      "volume": "114",
      "firstPage": "594",
      "containerTitle": "Physiologia Plantarum"
    },
    {
      "key": "bib4",
      "doi": "https://doi.org/10.1162/089976601750399335",
      "contributor": "Chang",
      "title": "Training nu-support vector classifiers: theory and algorithms",
      "publicationYear": "2001",
      "volume": "13",
      "firstPage": "2119",
      "containerTitle": "Neural computation"
    },
    {
      "key": "bib5",
      "doi": "https://doi.org/10.1007/bf00994018",
      "contributor": "Cortes",
      "title": "Support-vector Networks",
      "publicationYear": "1995",
      "volume": "20",
      "firstPage": "273",
      "containerTitle": "Machine Learning"
    },
    {
      "key": "bib6",
      "doi": "https://doi.org/10.1242/dev.119.1.71",
      "contributor": "Dolan",
      "title": "Cellular organisation of the Arabidopsis thaliana root",
      "publicationYear": "1993",
      "volume": "119",
      "firstPage": "71",
      "containerTitle": "Development"
    },
    {
      "key": "bib7",
      "doi": "https://doi.org/10.1016/j.semcdb.2009.09.009",
      "contributor": "Elo",
      "title": "Stem cell function during plant vascular development",
      "publicationYear": "2009",
      "volume": "20",
      "firstPage": "1097",
      "containerTitle": "Seminars in Cell & Developmental Biology"
    },
    {
      "key": "bib8",
      "doi": "https://doi.org/10.1242/dev.091314",
      "contributor": "Etchells",
      "title": "WOX4 and WOX14 act downstream of the PXY receptor kinase to regulate plant vascular proliferation independently of any role in vascular organisation",
      "publicationYear": "2013",
      "volume": "140",
      "firstPage": "2224",
      "containerTitle": "Development"
    },
    {
      "key": "bib9",
      "doi": "https://doi.org/10.1371/journal.pgen.1002997",
      "contributor": "Etchells",
      "title": "Plant vascular cell division is maintained by an interaction between PXY and ethylene signalling",
      "publicationYear": "2012",
      "volume": "8",
      "firstPage": "e1002997",
      "containerTitle": "PLOS Genetics"
    },
    {
      "key": "bib10",
      "doi": "https://doi.org/10.1038/msb.2010.25",
      "contributor": "Fuchs",
      "title": "Clustering phenotype populations by genome-wide RNAi and multiparametric imaging",
      "publicationYear": "2010",
      "volume": "6",
      "firstPage": "370",
      "containerTitle": "Molecular Systems Biology"
    },
    {
      "key": "bib11",
      "doi": "https://doi.org/10.1016/j.biosystems.2012.07.004",
      "contributor": "Granqvist",
      "title": "BaSAR-A tool in R for frequency detection",
      "publicationYear": "2012",
      "volume": "110",
      "firstPage": "60",
      "containerTitle": "Bio Systems"
    },
    {
      "key": "bib12",
      "doi": "https://doi.org/10.1016/j.pbi.2005.11.013",
      "contributor": "Groover",
      "title": "Developmental mechanisms regulating secondary growth in woody plants",
      "publicationYear": "2006",
      "volume": "9",
      "firstPage": "55",
      "containerTitle": "Current Opinion in Plant Biology"
    },
    {
      "key": "bib13",
      "doi": "https://doi.org/10.1105/tpc.110.076083",
      "contributor": "Hirakawa",
      "title": "TDIF peptide signaling regulates vascular stem cell proliferation via the WOX4 homeobox gene in Arabidopsis",
      "publicationYear": "2010",
      "volume": "22",
      "firstPage": "2618",
      "containerTitle": "Plant Cell"
    },
    {
      "key": "bib14",
      "doi": "https://doi.org/10.1073/pnas.0808444105",
      "contributor": "Hirakawa",
      "title": "Non-cell-autonomous control of vascular stem cell fate by a CLE peptide/receptor system",
      "publicationYear": "2008",
      "volume": "105",
      "firstPage": "15208",
      "containerTitle": "Proceedings of the National Academy of Sciences of the United States of America"
    },
    {
      "key": "bib15",
      "doi": "https://doi.org/10.1016/0092-8674(89)90900-8",
      "contributor": "Meyerowitz",
      "title": "Arabidopsis, a useful weed",
      "publicationYear": "1989",
      "volume": "56",
      "firstPage": "263",
      "containerTitle": "Cell"
    },
    {
      "key": "bib16",
      "doi": "https://doi.org/10.1126/science.1066609",
      "contributor": "Meyerowitz",
      "title": "Plants compared to animals: the broadest comparative study of development",
      "publicationYear": "2002",
      "volume": "295",
      "firstPage": "1482",
      "containerTitle": "Science"
    },
    {
      "key": "bib17",
      "doi": "https://doi.org/10.1104/pp.104.040212",
      "contributor": "Nieminen",
      "title": "A weed for wood? Arabidopsis as a genetic model for xylem development",
      "publicationYear": "2004",
      "volume": "135",
      "firstPage": "653",
      "containerTitle": "Plant Physiol"
    },
    {
      "key": "bib18",
      "doi": "https://doi.org/10.1038/nbt1206-1565",
      "contributor": "Noble",
      "title": "What is a support vector machine?",
      "publicationYear": "2006",
      "volume": "24",
      "firstPage": "1565",
      "containerTitle": "Nature Biotechnology"
    },
    {
      "key": "bib19",
      "doi": "https://doi.org/10.1073/pnas.77.3.1516",
      "contributor": "Olson",
      "title": "Classification of cultured mammalian cells by shape analysis and pattern recognition",
      "publicationYear": "1980",
      "volume": "77",
      "firstPage": "1516",
      "containerTitle": "Proceedings of the National Academy of Sciences of the United States of America"
    },
    {
      "key": "bib20",
      "doi": "https://doi.org/10.1093/bioinformatics/btq046",
      "contributor": "Pau",
      "title": "EBImage–an R package for image processing with applications to cellular phenotypes",
      "publicationYear": "2010",
      "volume": "26",
      "firstPage": "979",
      "containerTitle": "Bioinformatics"
    },
    {
      "key": "bib21",
      "doi": "https://doi.org/10.1105/tpc.111.084020",
      "contributor": "Ragni",
      "title": "Mobile gibberellin directly stimulates Arabidopsis hypocotyl xylem expansion",
      "publicationYear": "2011",
      "volume": "23",
      "firstPage": "1322",
      "containerTitle": "Plant Cell"
    },
    {
      "key": "bib22",
      "doi": "https://doi.org/10.5061/dryad.b835k",
      "contributor": "Sankar",
      "title": "Data from: Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth",
      "publicationYear": "2014",
      "containerTitle": "Dryad Digital Repository"
    },
    {
      "key": "bib23",
      "doi": "https://doi.org/10.1016/j.cub.2008.02.070",
      "contributor": "Sibout",
      "title": "Flowering as a condition for xylem expansion in Arabidopsis hypocotyl and root",
      "publicationYear": "2008",
      "volume": "18",
      "firstPage": "458",
      "containerTitle": "Current Biology"
    },
    {
      "key": "bib24",
      "doi": "https://doi.org/10.1111/j.1469-8137.2010.03236.x",
      "contributor": "Spicer",
      "title": "Evolution of development of vascular cambia and secondary growth",
      "publicationYear": "2010",
      "volume": "186",
      "firstPage": "577",
      "containerTitle": "The New Phytologist"
    },
    {
      "key": "bib25",
      "doi": "https://doi.org/10.1007/s00138-011-0345-9",
      "contributor": "Theriault",
      "title": "Cell morphology classification and clutter mitigation in phase-contrast microscopy images using machine learning",
      "publicationYear": "2012",
      "volume": "23",
      "firstPage": "659",
      "containerTitle": "Machine Vision and Applications"
    },
    {
      "key": "bib26",
      "doi": "https://doi.org/10.1016/j.cell.2012.02.048",
      "contributor": "Uyttewaal",
      "title": "Mechanical stress acts via katanin to amplify differences in growth rate between adjacent cells in Arabidopsis",
      "publicationYear": "2012",
      "volume": "149",
      "firstPage": "439",
      "containerTitle": "Cell"
    },
    {
      "key": "bib27",
      "doi": "https://doi.org/10.1038/ncb2764",
      "contributor": "Yin",
      "title": "A screen for morphological complexity identifies regulators of switch-like transitions between discrete cell shapes",
      "publicationYear": "2013",
      "volume": "15",
      "firstPage": "860",
      "containerTitle": "Nature Cell Biology"
    }
  ],
  "date": {
    "published": "2014-02-11",
    "updated": "2022-03-26"
  },
  "descriptions": [
    {
      "description": "Among various advantages, their small size makes model organisms preferred subjects of investigation. Yet, even in model systems detailed analysis of numerous developmental processes at cellular level is severely hampered by their scale. For instance, secondary growth of Arabidopsis hypocotyls creates a radial pattern of highly specialized tissues that comprises several thousand cells starting from a few dozen. This dynamic process is difficult to follow because of its scale and because it can only be investigated invasively, precluding comprehensive understanding of the cell proliferation, differentiation, and patterning events involved. To overcome such limitation, we established an automated quantitative histology approach. We acquired hypocotyl cross-sections from tiled high-resolution images and extracted their information content using custom high-throughput image processing and segmentation. Coupled with automated cell type recognition through machine learning, we could establish a cellular resolution atlas that reveals vascular morphodynamics during secondary growth, for example equidistant phloem pole formation.",
      "type": "Abstract"
    }
  ],
  "license": {
    "id": "CC-BY-3.0",
    "url": "https://creativecommons.org/licenses/by/3.0/legalcode"
  },
  "identifiers": [],
  "fundingReferences": [
    {
      "funderName": "SystemsX"
    },
    {
      "funderName": "EMBO longterm post-doctoral fellowships"
    },
    {
      "funderName": "Marie Heim-Voegtlin"
    },
    {
      "funderName": "University of Lausanne",
      "funderIdentifier": "https://doi.org/10.13039/501100006390",
      "funderIdentifierType": "Crossref Funder ID"
    },
    {
      "funderName": "SystemsX"
    },
    {
      "funderName": "EMBO",
      "funderIdentifier": "https://doi.org/10.13039/501100003043",
      "funderIdentifierType": "Crossref Funder ID"
    },
    {
      "funderName": "Swiss National Science Foundation",
      "funderIdentifier": "https://doi.org/10.13039/501100001711",
      "funderIdentifierType": "Crossref Funder ID"
    },
    {
      "funderName": "University of Lausanne",
      "funderIdentifier": "https://doi.org/10.13039/501100006390",
      "funderIdentifierType": "Crossref Funder ID"
    }
  ],
  "files": [
    {
      "url": "https://cdn.elifesciences.org/articles/01567/elife-01567-v1.pdf",
      "mimeType": "application/pdf"
    },
    {
      "url": "https://cdn.elifesciences.org/articles/01567/elife-01567-v1.xml",
      "mimeType": "application/xml"
    }
  ],
  "subjects": [],
  "provider": "Crossref",
  "schema_version": "https://commonmeta.org/commonmeta_v0.10",
  "state": "findable"
}
"""
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
        "affiliation": [
            {
                "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
            }
        ],
    }
    assert subject.license == {
        "id": "CC-BY-3.0",
        "url": "https://creativecommons.org/licenses/by/3.0/legalcode",
    }

    assert subject.date == {
        "published": "2014-02-11",
        "updated": "2022-03-26",
    }
    assert subject.publisher == {
        "id": "https://api.crossref.org/members/4374",
        "name": "eLife Sciences Publications, Ltd",
    }
    assert len(subject.references) == 27
    assert subject.references[0] == {
        "key": "bib1",
        "doi": "https://doi.org/10.1038/nature02100",
        "contributor": "Bonke",
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
        {"funderName": "SystemsX"},
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
        {
            "funderIdentifier": "https://doi.org/10.13039/501100006390",
            "funderIdentifierType": "Crossref Funder ID",
            "funderName": "University of Lausanne",
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
    assert subject.subjects == []
    assert subject.language is None
    assert subject.version is None
    assert subject.provider == "Crossref"
    assert len(subject.files) == 2
    assert subject.files[0] == {
        "url": "https://cdn.elifesciences.org/articles/01567/elife-01567-v1.pdf",
        "mimeType": "application/pdf",
    }


def test_commonmeta_list():
    "commonmeta list"
    string = path.join(path.dirname(__file__), "fixtures", "commonmeta-list.json")
    subject_list = MetadataList(string)
    assert len(subject_list.items) == 15
    subject = subject_list.items[0]
    assert (
        subject.id
        == "https://blogs.fu-berlin.de/open-access-berlin/2022/05/12/das-bua-open-science-dashboard-projekt-die-entwicklung-disziplinspezifischer-open-science-indikatoren"
    )
    assert subject.type == "Article"
    assert subject.is_valid
