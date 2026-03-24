"""Utils module for commonmeta-py"""

from __future__ import annotations

import os
import re
import time
from typing import Any
from urllib.parse import urlparse

import bibtexparser
import orjson as json
import pycountry
import yaml
from bs4 import BeautifulSoup
from furl import furl
from idutils import validators
from isbnlib import canonical, is_isbn10, is_isbn13

from .base_utils import (
    compact,
    dig,
    first,
    omit,
    parse_attributes,
    pascal_case,
    unique,
    wrap,
)
from .constants import DATACITE_CONTRIBUTOR_TYPES, OPENALEX_SUBFIELD_MAPPINGS
from .doi_utils import doi_as_url, doi_from_url, get_doi_ra, normalize_doi, validate_doi

NORMALIZED_LICENSES = {
    "https://creativecommons.org/licenses/by/1.0": "https://creativecommons.org/licenses/by/1.0/legalcode",
    "https://creativecommons.org/licenses/by/2.0": "https://creativecommons.org/licenses/by/2.0/legalcode",
    "https://creativecommons.org/licenses/by/2.5": "https://creativecommons.org/licenses/by/2.5/legalcode",
    "https://creativecommons.org/licenses/by/3.0": "https://creativecommons.org/licenses/by/3.0/legalcode",
    "https://creativecommons.org/licenses/by/3.0/us": "https://creativecommons.org/licenses/by/3.0/legalcode",
    "https://creativecommons.org/licenses/by/4.0": "https://creativecommons.org/licenses/by/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nc/1.0": "https://creativecommons.org/licenses/by-nc/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nc/2.0": "https://creativecommons.org/licenses/by-nc/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nc/2.5": "https://creativecommons.org/licenses/by-nc/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nc/3.0": "https://creativecommons.org/licenses/by-nc/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nc/4.0": "https://creativecommons.org/licenses/by-nc/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/1.0": "https://creativecommons.org/licenses/by-nd-nc/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/2.0": "https://creativecommons.org/licenses/by-nd-nc/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/2.5": "https://creativecommons.org/licenses/by-nd-nc/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/3.0": "https://creativecommons.org/licenses/by-nd-nc/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/4.0": "https://creativecommons.org/licenses/by-nd-nc/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/1.0": "https://creativecommons.org/licenses/by-nc-sa/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/2.0": "https://creativecommons.org/licenses/by-nc-sa/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/2.5": "https://creativecommons.org/licenses/by-nc-sa/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/3.0": "https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/3.0/us": "https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nd/1.0": "https://creativecommons.org/licenses/by-nd/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nd/2.0": "https://creativecommons.org/licenses/by-nd/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nd/2.5": "https://creativecommons.org/licenses/by-nd/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nd/3.0": "https://creativecommons.org/licenses/by-nd/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nd/4.0": "https://creativecommons.org/licenses/by-nd/2.0/legalcode",
    "https://creativecommons.org/licenses/by-sa/1.0": "https://creativecommons.org/licenses/by-sa/1.0/legalcode",
    "https://creativecommons.org/licenses/by-sa/2.0": "https://creativecommons.org/licenses/by-sa/2.0/legalcode",
    "https://creativecommons.org/licenses/by-sa/2.5": "https://creativecommons.org/licenses/by-sa/2.5/legalcode",
    "https://creativecommons.org/licenses/by-sa/3.0": "https://creativecommons.org/licenses/by-sa/3.0/legalcode",
    "https://creativecommons.org/licenses/by-sa/4.0": "https://creativecommons.org/licenses/by-sa/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/1.0": "https://creativecommons.org/licenses/by-nc-nd/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/2.0": "https://creativecommons.org/licenses/by-nc-nd/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/2.5": "https://creativecommons.org/licenses/by-nc-nd/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/3.0": "https://creativecommons.org/licenses/by-nc-nd/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/4.0": "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
    "https://creativecommons.org/licenses/publicdomain": "https://creativecommons.org/licenses/publicdomain/",
    "https://creativecommons.org/publicdomain/zero/1.0": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
}

UNKNOWN_INFORMATION = {
    ":unac": "temporarily inaccessible",
    ":unal": "unallowed, suppressed intentionally",
    ":unap": "not applicable, makes no sense",
    ":unas": "value unassigned (e.g., Untitled)",
    ":unav": "value unavailable, possibly unknown",
    ":unkn": "known to be unknown (e.g., Anonymous, Inconnue)",
    ":none": "never had a value, never will",
    ":null": "explicitly and meaningfully empty",
    ":tba": "to be assigned or announced later",
    ":etal": "too numerous to list (et alia)",
}

HTTP_SCHEME = "http://"
HTTPS_SCHEME = "https://"

FOS_MAPPINGS = {
    "Natural sciences": "http://www.oecd.org/science/inno/38235147.pdf?1",
    "Mathematics": "http://www.oecd.org/science/inno/38235147.pdf?1.1",
    "Computer and information sciences": "http://www.oecd.org/science/inno/38235147.pdf?1.2",
    "Physical sciences": "http://www.oecd.org/science/inno/38235147.pdf?1.3",
    "Chemical sciences": "http://www.oecd.org/science/inno/38235147.pdf?1.4",
    "Earth and related environmental sciences": "http://www.oecd.org/science/inno/38235147.pdf?1.5",
    "Biological sciences": "http://www.oecd.org/science/inno/38235147.pdf?1.6",
    "Other natural sciences": "http://www.oecd.org/science/inno/38235147.pdf?1.7",
    "Engineering and technology": "http://www.oecd.org/science/inno/38235147.pdf?2",
    "Civil engineering": "http://www.oecd.org/science/inno/38235147.pdf?2.1",
    "Electrical engineering, electronic engineering, information engineering": "http://www.oecd.org/science/inno/38235147.pdf?2.2",
    "Mechanical engineering": "http://www.oecd.org/science/inno/38235147.pdf?2.3",
    "Chemical engineering": "http://www.oecd.org/science/inno/38235147.pdf?2.4",
    "Materials engineering": "http://www.oecd.org/science/inno/38235147.pdf?2.5",
    "Medical engineering": "http://www.oecd.org/science/inno/38235147.pdf?2.6",
    "Environmental engineering": "http://www.oecd.org/science/inno/38235147.pdf?2.7",
    "Environmental biotechnology": "http://www.oecd.org/science/inno/38235147.pdf?2.8",
    "Industrial biotechnology": "http://www.oecd.org/science/inno/38235147.pdf?2.9",
    "Nano technology": "http://www.oecd.org/science/inno/38235147.pdf?2.10",
    "Other engineering and technologies": "http://www.oecd.org/science/inno/38235147.pdf?2.11",
    "Medical and health sciences": "http://www.oecd.org/science/inno/38235147.pdf?3",
    "Basic medicine": "http://www.oecd.org/science/inno/38235147.pdf?3.1",
    "Clinical medicine": "http://www.oecd.org/science/inno/38235147.pdf?3.2",
    "Health sciences": "http://www.oecd.org/science/inno/38235147.pdf?3.3",
    "Health biotechnology": "http://www.oecd.org/science/inno/38235147.pdf?3.4",
    "Other medical sciences": "http://www.oecd.org/science/inno/38235147.pdf?3.5",
    "Agricultural sciences": "http://www.oecd.org/science/inno/38235147.pdf?4",
    "Agriculture, forestry, and fisheries": "http://www.oecd.org/science/inno/38235147.pdf?4.1",
    "Animal and dairy science": "http://www.oecd.org/science/inno/38235147",
    "Veterinary science": "http://www.oecd.org/science/inno/38235147",
    "Agricultural biotechnology": "http://www.oecd.org/science/inno/38235147",
    "Other agricultural sciences": "http://www.oecd.org/science/inno/38235147",
    "Social science": "http://www.oecd.org/science/inno/38235147.pdf?5",
    "Social sciences": "http://www.oecd.org/science/inno/38235147.pdf?5",
    "Psychology": "http://www.oecd.org/science/inno/38235147.pdf?5.1",
    "Economics and business": "http://www.oecd.org/science/inno/38235147.pdf?5.2",
    "Educational sciences": "http://www.oecd.org/science/inno/38235147.pdf?5.3",
    "Sociology": "http://www.oecd.org/science/inno/38235147.pdf?5.4",
    "Law": "http://www.oecd.org/science/inno/38235147.pdf?5.5",
    "Political science": "http://www.oecd.org/science/inno/38235147.pdf?5.6",
    "Social and economic geography": "http://www.oecd.org/science/inno/38235147.pdf?5.7",
    "Media and communications": "http://www.oecd.org/science/inno/38235147.pdf?5.8",
    "Other social sciences": "http://www.oecd.org/science/inno/38235147.pdf?5.9",
    "Humanities": "http://www.oecd.org/science/inno/38235147.pdf?6",
    "History and archaeology": "http://www.oecd.org/science/inno/38235147.pdf?6.1",
    "Languages and literature": "http://www.oecd.org/science/inno/38235147.pdf?6.2",
    "Philosophy, ethics and religion": "http://www.oecd.org/science/inno/38235147.pdf?6.3",
    "Arts (arts, history of arts, performing arts, music)": "http://www.oecd.org/science/inno/38235147.pdf?6.4",
    "Other humanities": "http://www.oecd.org/science/inno/38235147.pdf?6.5",
}

FOS_TO_STRING_MAPPINGS = {
    "Natural sciences": "naturalSciences",
    "Mathematics": "mathematics",
    "Computer and information sciences": "computerAndInformationSciences",
    "Physical sciences": "physicalSciences",
    "Chemical sciences": "chemicalSciences",
    "Earth and related environmental sciences": "earthAndRelatedEnvironmentalSciences",
    "Biological sciences": "biologicalSciences",
    "Other natural sciences": "otherNaturalSciences",
    "Engineering and technology": "engineeringAndTechnology",
    "Civil engineering": "civilEngineering",
    "Electrical engineering, electronic engineering, information engineering": "electricalEngineering",
    "Mechanical engineering": "mechanicalEngineering",
    "Chemical engineering": "chemicalEngineering",
    "Materials engineering": "materialsEngineering",
    "Medical engineering": "medicalEngineering",
    "Environmental engineering": "environmentalEngineering",
    "Environmental biotechnology": "environmentalBiotechnology",
    "Industrial biotechnology": "industrialBiotechnology",
    "Nano technology": "nanoTechnology",
    "Other engineering and technologies": "otherEngineeringAndTechnologies",
    "Medical and health sciences": "medicalAndHealthSciences",
    "Basic medicine": "basicMedicine",
    "Clinical medicine": "clinicalMedicine",
    "Health sciences": "healthSciences",
    "Health biotechnology": "healthBiotechnology",
    "Other medical sciences": "otherMedicalSciences",
    "Agricultural sciences": "agriculturalSciences",
    "Agriculture, forestry, and fisheries": "agricultureForestryAndFisheries",
    "Animal and dairy science": "animalAndDairyScience",
    "Veterinary science": "veterinaryScience",
    "Agricultural biotechnology": "agriculturalBiotechnology",
    "Other agricultural sciences": "otherAgriculturalSciences",
    "Social science": "socialScience",
    "Psychology": "psychology",
    "Economics and business": "economicsAndBusiness",
    "Educational sciences": "educationalSciences",
    "Sociology": "sociology",
    "Law": "law",
    "Political science": "politicalScience",
    "Social and economic geography": "socialAndEconomicGeography",
    "Media and communications": "mediaAndCommunications",
    "Other social sciences": "otherSocialSciences",
    "Humanities": "humanities",
    "History and archaeology": "historyAndArchaeology",
    "Languages and literature": "languagesAndLiterature",
    "Philosophy, ethics and religion": "philosophyEthicsAndReligion",
    "Arts (arts, history of arts, performing arts, music)": "artsArtsHistoryOfArtsPerformingArtsMusic",
    "Other humanities": "otherHumanities",
}


# Mapping from OpenAlex Subfield IDs to OECD FOS category names
# See: https://www.oecd.org/sti/inno/frascati-manual.htm
OPENALEX_TO_FOS_MAPPINGS = {
    # 1.1 Mathematics
    "1804": "Mathematics",  # Statistics, Probability and Uncertainty
    "2602": "Mathematics",  # Algebra and Number Theory
    "2604": "Mathematics",  # Applied Mathematics
    "2605": "Mathematics",  # Computational Mathematics
    "2607": "Mathematics",  # Discrete Mathematics and Combinatorics
    "2608": "Mathematics",  # Geometry and Topology
    "2610": "Mathematics",  # Mathematical Physics
    "2611": "Mathematics",  # Modeling and Simulation
    "2612": "Mathematics",  # Numerical Analysis
    "2613": "Mathematics",  # Statistics and Probability
    "2614": "Mathematics",  # Theoretical Computer Science
    # 1.2 Computer and information sciences
    "1702": "Computer and information sciences",  # Artificial Intelligence
    "1703": "Computer and information sciences",  # Computational Theory and Mathematics
    "1704": "Computer and information sciences",  # Computer Graphics and Computer-Aided Design
    "1705": "Computer and information sciences",  # Computer Networks and Communications
    "1706": "Computer and information sciences",  # Computer Science Applications
    "1707": "Computer and information sciences",  # Computer Vision and Pattern Recognition
    "1708": "Computer and information sciences",  # Hardware and Architecture
    "1709": "Computer and information sciences",  # Human-Computer Interaction
    "1710": "Computer and information sciences",  # Information Systems
    "1711": "Computer and information sciences",  # Signal Processing
    "1712": "Computer and information sciences",  # Software
    # 1.3 Physical sciences
    "1912": "Physical sciences",  # Space and Planetary Science
    "3102": "Physical sciences",  # Acoustics and Ultrasonics
    "3103": "Physical sciences",  # Astronomy and Astrophysics
    "3104": "Physical sciences",  # Condensed Matter Physics
    "3105": "Physical sciences",  # Instrumentation
    "3106": "Physical sciences",  # Nuclear and High Energy Physics
    "3107": "Physical sciences",  # Atomic and Molecular Physics, and Optics
    "3108": "Physical sciences",  # Radiation
    "3109": "Physical sciences",  # Statistical and Nonlinear Physics
    # 1.4 Chemical sciences
    "1602": "Chemical sciences",  # Analytical Chemistry
    "1603": "Chemical sciences",  # Electrochemistry
    "1604": "Chemical sciences",  # Inorganic Chemistry
    "1605": "Chemical sciences",  # Organic Chemistry
    "1606": "Chemical sciences",  # Physical and Theoretical Chemistry
    "1607": "Chemical sciences",  # Spectroscopy
    "2502": "Chemical sciences",  # Biomaterials
    "2505": "Chemical sciences",  # Materials Chemistry
    # 1.5 Earth and related environmental sciences
    "1902": "Earth and related environmental sciences",  # Atmospheric Science
    "1904": "Earth and related environmental sciences",  # Earth-Surface Processes
    "1906": "Earth and related environmental sciences",  # Geochemistry and Petrology
    "1907": "Earth and related environmental sciences",  # Geology
    "1908": "Earth and related environmental sciences",  # Geophysics
    "1910": "Earth and related environmental sciences",  # Oceanography
    "1911": "Earth and related environmental sciences",  # Paleontology
    "2302": "Earth and related environmental sciences",  # Ecological Modeling
    "2303": "Earth and related environmental sciences",  # Ecology
    "2306": "Earth and related environmental sciences",  # Global and Planetary Change
    # 1.6 Biological sciences
    "1105": "Biological sciences",  # Ecology, Evolution, Behavior and Systematics
    "1109": "Biological sciences",  # Insect Science
    "1110": "Biological sciences",  # Plant Science
    "1307": "Biological sciences",  # Cell Biology
    "1309": "Biological sciences",  # Developmental Biology
    "1311": "Biological sciences",  # Genetics
    "1312": "Biological sciences",  # Molecular Biology
    # 2.1 Civil engineering
    "2205": "Civil engineering",  # Civil and Structural Engineering
    "2216": "Civil engineering",  # Architecture
    # 2.2 Electrical engineering, electronic engineering, information engineering
    "2207": "Electrical engineering, electronic engineering, information engineering",  # Control and Systems Engineering
    "2208": "Electrical engineering, electronic engineering, information engineering",  # Electrical and Electronic Engineering
    "2214": "Electrical engineering, electronic engineering, information engineering",  # Media Technology
    # 2.3 Mechanical engineering
    "2203": "Mechanical engineering",  # Automotive Engineering
    "2206": "Mechanical engineering",  # Computational Mechanics
    "2210": "Mechanical engineering",  # Mechanical Engineering
    "2211": "Mechanical engineering",  # Mechanics of Materials
    "2212": "Mechanical engineering",  # Ocean Engineering
    # 2.4 Chemical engineering
    "1506": "Chemical engineering",  # Filtration and Separation
    "1508": "Chemical engineering",  # Process Chemistry and Technology
    # 2.5 Materials engineering
    "2215": "Materials engineering",  # Building and Construction
    "2500": "Materials engineering",  # General Materials Science
    "2503": "Materials engineering",  # Ceramics and Composites
    "2504": "Materials engineering",  # Electronic, Optical and Magnetic Materials
    "2506": "Materials engineering",  # Metals and Alloys
    "2507": "Materials engineering",  # Polymers and Plastics
    "2508": "Materials engineering",  # Surfaces, Coatings and Films
    # 2.6 Medical engineering
    "1502": "Medical engineering",  # Bioengineering
    "2204": "Medical engineering",  # Biomedical Engineering
    "3614": "Medical engineering",  # Radiological and Ultrasound Technology
    # 2.7 Environmental engineering
    "2304": "Environmental engineering",  # Environmental Chemistry
    "2305": "Environmental engineering",  # Environmental Engineering
    "2307": "Environmental engineering",  # Health, Toxicology and Mutagenesis
    "2309": "Environmental engineering",  # Nature and Landscape Conservation
    "2310": "Environmental engineering",  # Pollution
    # 2.9 Industrial Biotechnology
    "2402": "Industrial Biotechnology",  # Applied Microbiology and Biotechnology
    # 2.11 Other engineering and technologies
    "1503": "Other engineering and technologies",  # Catalysis
    "1504": "Other engineering and technologies",  # Chemical Health and Safety
    "1507": "Other engineering and technologies",  # Fluid Flow and Transfer Processes
    "2100": "Other engineering and technologies",  # General Energy
    "2102": "Other engineering and technologies",  # Energy Engineering and Power Technology
    "2103": "Other engineering and technologies",  # Fuel Technology
    "2104": "Other engineering and technologies",  # Nuclear Energy and Engineering
    "2105": "Other engineering and technologies",  # Renewable Energy, Sustainability and the Environment
    "2200": "Other engineering and technologies",  # General Engineering
    "2202": "Other engineering and technologies",  # Aerospace Engineering
    "2209": "Other engineering and technologies",  # Industrial and Manufacturing Engineering
    "2213": "Other engineering and technologies",  # Safety, Risk, Reliability and Quality
    "2308": "Other engineering and technologies",  # Management, Monitoring, Policy and Law
    "2311": "Other engineering and technologies",  # Waste Management and Disposal
    "2312": "Other engineering and technologies",  # Water Science and Technology
    # 3.1 Basic medicine
    "1303": "Basic medicine",  # Biochemistry
    "1304": "Basic medicine",  # Biophysics
    "1306": "Basic medicine",  # Cancer Research
    "1308": "Basic medicine",  # Clinical Biochemistry
    "1310": "Basic medicine",  # Endocrinology
    "1313": "Basic medicine",  # Molecular Medicine
    "1314": "Basic medicine",  # Physiology
    "1315": "Basic medicine",  # Structural Biology
    "2403": "Basic medicine",  # Immunology
    "2404": "Basic medicine",  # Microbiology
    "2405": "Basic medicine",  # Parasitology
    "2406": "Basic medicine",  # Virology
    "2702": "Basic medicine",  # Anatomy
    "2704": "Basic medicine",  # Biochemistry
    "2716": "Basic medicine",  # Genetics
    "2726": "Basic medicine",  # Microbiology
    "2737": "Basic medicine",  # Physiology
    # 3.2 Clinical medicine
    "2703": "Clinical medicine",  # Anesthesiology and Pain Medicine
    "2705": "Clinical medicine",  # Cardiology and Cardiovascular Medicine
    "2706": "Clinical medicine",  # Critical Care and Intensive Care Medicine
    "2707": "Clinical medicine",  # Complementary and alternative medicine
    "2708": "Clinical medicine",  # Dermatology
    "2711": "Clinical medicine",  # Emergency Medicine
    "2712": "Clinical medicine",  # Endocrinology, Diabetes and Metabolism
    "2713": "Clinical medicine",  # Epidemiology
    "2714": "Clinical medicine",  # Family Practice
    "2715": "Clinical medicine",  # Gastroenterology
    "2717": "Clinical medicine",  # Geriatrics and Gerontology
    "2720": "Clinical medicine",  # Hematology
    "2721": "Clinical medicine",  # Hepatology
    "2723": "Clinical medicine",  # Immunology and Allergy
    "2724": "Clinical medicine",  # Internal Medicine
    "2725": "Clinical medicine",  # Infectious Diseases
    "2727": "Clinical medicine",  # Nephrology
    "2728": "Clinical medicine",  # Neurology
    "2729": "Clinical medicine",  # Obstetrics and Gynecology
    "2730": "Clinical medicine",  # Oncology
    "2731": "Clinical medicine",  # Ophthalmology
    "2732": "Clinical medicine",  # Orthopedics and Sports Medicine
    "2733": "Clinical medicine",  # Otorhinolaryngology
    "2734": "Clinical medicine",  # Pathology and Forensic Medicine
    "2735": "Clinical medicine",  # Pediatrics, Perinatology and Child Health
    "2736": "Clinical medicine",  # Pharmacology
    "2738": "Clinical medicine",  # Psychiatry and Mental health
    "2740": "Clinical medicine",  # Pulmonary and Respiratory Medicine
    "2741": "Clinical medicine",  # Radiology, Nuclear Medicine and Imaging
    "2742": "Clinical medicine",  # Rehabilitation
    "2743": "Clinical medicine",  # Reproductive Medicine
    "2745": "Clinical medicine",  # Rheumatology
    "2746": "Clinical medicine",  # Surgery
    "2747": "Clinical medicine",  # Transplantation
    "2748": "Clinical medicine",  # Urology
    "2802": "Clinical medicine",  # Behavioral Neuroscience
    "2803": "Clinical medicine",  # Biological Psychiatry
    "2804": "Clinical medicine",  # Cellular and Molecular Neuroscience
    "2807": "Clinical medicine",  # Endocrine and Autonomic Systems
    "2808": "Clinical medicine",  # Neurology
    "2809": "Clinical medicine",  # Sensory Systems
    # 3.3 Health sciences
    "2718": "Health sciences",  # Health Informatics
    "2739": "Health sciences",  # Public Health, Environmental and Occupational Health
    "2916": "Health sciences",  # Nutrition and Dietetics
    "3600": "Health sciences",  # General Health Professions
    "3603": "Health sciences",  # Complementary and Manual Therapy
    "3604": "Health sciences",  # Emergency Medical Services
    "3605": "Health sciences",  # Health Information Management
    "3607": "Health sciences",  # Medical Laboratory Technology
    "3608": "Health sciences",  # Medical Terminology
    "3609": "Health sciences",  # Occupational Therapy
    "3611": "Health sciences",  # Pharmacy
    "3612": "Health sciences",  # Physical Therapy, Sports Therapy and Rehabilitation
    "3616": "Health sciences",  # Speech and Hearing
    # 3.4 Health biotechnology
    "1305": "Health biotechnology",  # Biotechnology
    "3004": "Health biotechnology",  # Pharmacology
    # 3.5 Other medical sciences
    "1302": "Other medical sciences",  # Aging
    "2910": "Other medical sciences",  # Issues, ethics and legal aspects
    "2911": "Other medical sciences",  # Leadership and Management
    "2922": "Other medical sciences",  # Research and Theory
    "3002": "Other medical sciences",  # Drug Discovery
    "3003": "Other medical sciences",  # Pharmaceutical Science
    "3005": "Other medical sciences",  # Toxicology
    "3500": "Other medical sciences",  # General Dentistry
    "3504": "Other medical sciences",  # Oral Surgery
    "3505": "Other medical sciences",  # Orthodontics
    "3506": "Other medical sciences",  # Periodontics
    # 4.1 Agriculture, forestry, and fisheries
    "1100": "Agriculture, forestry, and fisheries",  # General Agricultural and Biological Sciences
    "1102": "Agriculture, forestry, and fisheries",  # Agronomy and Crop Science
    "1104": "Agriculture, forestry, and fisheries",  # Aquatic Science
    "1107": "Agriculture, forestry, and fisheries",  # Forestry
    "1108": "Agriculture, forestry, and fisheries",  # Horticulture
    "1111": "Agriculture, forestry, and fisheries",  # Soil Science
    # 4.2 Animal and dairy science
    "1103": "Animal and dairy science",  # Animal Science and Zoology
    # 4.3 Veterinary science
    "3402": "Veterinary science",  # Equine
    "3404": "Veterinary science",  # Small Animals
    # 4.5 Other agricultural sciences
    "1106": "Other agricultural sciences",  # Food Science
    # 5.1 Psychology
    "2805": "Psychology",  # Cognitive Neuroscience
    "2806": "Psychology",  # Developmental Neuroscience
    "3200": "Psychology",  # General Psychology
    "3202": "Psychology",  # Applied Psychology
    "3203": "Psychology",  # Clinical Psychology
    "3204": "Psychology",  # Developmental and Educational Psychology
    "3205": "Psychology",  # Experimental and Cognitive Psychology
    "3206": "Psychology",  # Neuropsychology and Physiological Psychology
    "3207": "Psychology",  # Social Psychology
    # 5.2 Economics and business
    "1402": "Economics and business",  # Accounting
    "1403": "Economics and business",  # Business and International Management
    "1404": "Economics and business",  # Management Information Systems
    "1405": "Economics and business",  # Management of Technology and Innovation
    "1406": "Economics and business",  # Marketing
    "1407": "Economics and business",  # Organizational Behavior and Human Resource Management
    "1408": "Economics and business",  # Strategy and Management
    "1409": "Economics and business",  # Tourism, Leisure and Hospitality Management
    "1410": "Economics and business",  # Industrial relations
    "1800": "Economics and business",  # General Decision Sciences
    "1802": "Economics and business",  # Information Systems and Management
    "1803": "Economics and business",  # Management Science and Operations Research
    "2000": "Economics and business",  # General Economics, Econometrics and Finance
    "2002": "Economics and business",  # Economics and Econometrics
    "2003": "Economics and business",  # Finance
    # 5.3 Educational sciences
    "3304": "Educational sciences",  # Education
    # 5.4 Sociology
    "3312": "Sociology",  # Sociology and Political Science
    # 5.5 Law
    "3308": "Law",  # Law
    # 5.6 Political Science
    "3320": "Political Science",  # Political Science and International Relations
    # 5.7 Social and economic geography
    "3305": "Social and economic geography",  # Geography, Planning and Development
    # 5.8 Media and communications
    "3315": "Media and communications",  # Communication
    "3316": "Media and communications",  # Cultural Studies
    # 5.9 Other social sciences
    "3300": "Other social sciences",  # General Social Sciences
    "3303": "Other social sciences",  # Development
    "3306": "Other social sciences",  # Health
    "3307": "Other social sciences",  # Human Factors and Ergonomics
    "3311": "Other social sciences",  # Safety Research
    "3313": "Other social sciences",  # Transportation
    "3314": "Other social sciences",  # Anthropology
    "3317": "Other social sciences",  # Demography
    "3318": "Other social sciences",  # Gender Studies
    "3319": "Other social sciences",  # Life-span and Life-course Studies
    "3321": "Other social sciences",  # Public Administration
    "3322": "Other social sciences",  # Urban Studies
    # 6.1 History and archaeology
    "1202": "History and archaeology",  # History
    "1204": "History and archaeology",  # Archeology
    "3302": "History and archaeology",  # Archeology
    # 6.2 Languages and literature
    "1203": "Languages and literature",  # Language and Linguistics
    "1208": "Languages and literature",  # Literature and Literary Theory
    "3310": "Languages and literature",  # Linguistics and Language
    # 6.3 Philosophy, ethics and religion
    "1211": "Philosophy, ethics and religion",  # Philosophy
    "1212": "Philosophy, ethics and religion",  # Religious studies
    # 6.4 Art (arts, history of arts, performing arts, music)
    "1210": "Art (arts, history of arts, performing arts, music)",  # Music
    "1213": "Art (arts, history of arts, performing arts, music)",  # Visual Arts and Performing Arts
    # 6.5 Other humanities
    "1200": "Other humanities",  # General Arts and Humanities
    "1205": "Other humanities",  # Classics
    "1206": "Other humanities",  # Conservation
    "1207": "Other humanities",  # History and Philosophy of Science
    "1209": "Other humanities",  # Museology
    "3309": "Other humanities",  # Library and Information Sciences
}


def normalize_id(pid: str | bytes | None, **kwargs) -> str | None:
    """Check for valid DOI or HTTP(S) URL"""
    if pid is None:
        return None

    # Convert bytes/bytearray to string
    pid_str: str
    if isinstance(pid, (bytes, bytearray)):
        pid_str = pid.decode()
    else:
        pid_str = pid

    # check for valid DOI
    doi = normalize_doi(pid_str, **kwargs)
    if doi is not None:
        return doi

    # check for valid HTTP uri and ensure https
    f = furl(pid_str)
    if not f.host or f.scheme not in ["http", "https"]:
        return None
    if f.scheme == "http":
        f.scheme = "https"

    return f.url


def normalize_ids(ids: list, relation_type=None) -> list:
    """Normalize identifiers"""

    def format_id(i):
        if i.get("id", None):
            idn = normalize_id(i["id"])
            doi = doi_from_url(idn)
            related_identifier_type = "DOI" if doi is not None else "URL"
            idn = doi or idn
            _type = (
                i.get("type")
                if isinstance(i.get("type", None), str)
                else wrap(i.get("type", None))[0]
            )
            return compact(
                {
                    "relatedIdentifier": idn,
                    "relationType": relation_type,
                    "relatedIdentifierType": related_identifier_type,
                }
            )
        return None

    return [format_id(i) for i in ids]


def normalize_url(
    url: str | None, secure: bool = False, fragments: bool = False, lower: bool = False
) -> str | None:
    """Normalize URL"""
    if url is None or not isinstance(url, str):
        return None
    url = url.strip()
    scheme = urlparse(url).scheme
    if not scheme or scheme not in ["http", "https"]:
        return None
    if secure is True and url.startswith(HTTP_SCHEME):
        url = url.replace(HTTP_SCHEME, HTTPS_SCHEME)
    if lower is True:
        return url.lower()
    return url


def normalize_cc_url(url: str | None) -> str | None:
    """Normalize Creative Commons URL"""
    if url is None or not isinstance(url, str):
        return None
    url = normalize_url(url, secure=True)
    if url and url.endswith("/"):
        url = url.strip("/")
    return NORMALIZED_LICENSES.get(url, url)


def normalize_ror(ror: str | None) -> str | None:
    """Normalize ROR ID"""
    ror = validate_ror(ror)
    if ror is None:
        return None

    # turn ROR ID into URL
    return "https://ror.org/" + ror


def validate_ror(ror: str | None) -> str | None:
    """Validate ROR"""
    if ror is None or not isinstance(ror, str):
        return None
    match = re.search(
        r"\A(?:(?:http|https)://ror\.org/)?([0-9a-z]{7}\d{2})\Z",
        ror,
    )
    if match is None:
        return None
    ror = match.group(1).replace(" ", "-")
    return ror


def validate_url(url: str | None) -> str | None:
    if url is None:
        return None
    elif validate_doi(url):
        return "DOI"
    f = furl(url)
    if f and f.scheme in ["http", "https"]:
        return "URL"
    match = re.search(
        r"\A(ISSN|eISSN) (\d{4}-\d{3}[0-9X]+)\Z",
        url,
    )
    if match is not None:
        return "ISSN"
    return None


def normalize_orcid(orcid: str | None) -> str | None:
    """Normalize ORCID"""
    if orcid is None or not isinstance(orcid, str):
        return None
    orcid = validate_orcid(orcid)
    if orcid is None:
        return None
    return "https://orcid.org/" + orcid


def validate_orcid(orcid: str | None) -> str | None:
    """Validate ORCID"""
    if orcid is None or not isinstance(orcid, str):
        return None
    match = re.search(
        r"\A(?:(?:http|https)://(?:(?:www|sandbox)?\.)?orcid\.org/)?(\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{3}[0-9X]+)\Z",
        orcid,
    )
    if match is None:
        return None
    orcid = match.group(1).replace(" ", "-")
    if not validators.is_orcid(orcid):
        return None
    return orcid


def validate_isni(isni: str | None) -> str | None:
    """Validate ISNI"""
    if isni is None or not isinstance(isni, str):
        return None
    match = re.search(
        r"\A(?:(?:http|https)://isni\.org/isni/)?(\d{4}([ -])?\d{4}([ -])?\d{4}([ -])?\d{3}[0-9X]+)\Z",
        isni,
    )
    if match is None:
        return None
    isni = match.group(1).replace(" ", "").replace("-", "")
    if not validators.is_isni(isni):
        return None
    return isni


def validate_isbn(isbn: str | None) -> str | None:
    """Validate ISBN"""
    if isbn is None or not isinstance(isbn, str):
        return None
    isbn = canonical(isbn)
    if not (is_isbn10(isbn) or is_isbn13(isbn)):
        return None
    return isbn


def validate_mag(mag: str | None) -> str | None:
    """Validate Microsoft Academic Graph ID (mag)"""
    if mag is None or not isinstance(mag, str):
        return None
    match = re.search(
        r"\A(\d{4,10})\Z",
        mag,
    )
    if match is None:
        return None
    return match.group(1)


def validate_openalex(openalex: str | None) -> str | None:
    """Validate OpenAlex ID"""
    if openalex is None or not isinstance(openalex, str):
        return None
    match = re.search(
        r"\A(?:(?:http|https)://openalex\.org/)?([AFIPSW]\d{8,10})\Z",
        openalex,
    )
    if match is None:
        return None
    return match.group(1)


def validate_pmid(pmid: str | None) -> str | None:
    """Validate PubMed ID (pmid)"""
    if pmid is None or not isinstance(pmid, str):
        return None
    match = re.search(
        r"\A(?:(?:http|https)://pubmed\.ncbi\.nlm\.nih\.gov/)?(\d{4,8})\Z",
        pmid,
    )
    if match is None:
        return None
    return match.group(1)


def validate_pmcid(pmcid: str | None) -> str | None:
    """Validate PubMed Central ID (pmcid)"""
    if pmcid is None or not isinstance(pmcid, str):
        return None
    match = re.search(
        r"\A(?:(?:http|https)://www\.ncbi\.nlm\.nih\.gov/pmc/articles/)?(\d{4,8})\Z",
        pmcid,
    )
    if match is None:
        return None
    return match.group(1)


def validate_id(id: str | None) -> tuple[str | None, str | None]:
    """
    Validate an identifier and return the validated identifier and its type.

    Args:
        id: The identifier string to validate

    Returns:
        A tuple containing (validated_id, id_type) or (None, None) if invalid
    """
    if id is None:
        return None, None

    # Check if it's a DOI
    doi = validate_doi(id)
    if doi:
        return doi, "DOI"

    # Check if it's an ORCID
    orcid = validate_orcid(id)
    if orcid:
        return orcid, "ORCID"

    # Check if it's a ROR
    ror = validate_ror(id)
    if ror:
        return ror, "ROR"

    # Check if it's an ISNI
    isni = validate_isni(id)
    if isni:
        return isni, "ISNI"

    # Check if it's an OpenAlex ID
    openalex = validate_openalex(id)
    if openalex:
        return openalex, "OpenAlex"

    # Check if it's a PubMed ID
    pmid = validate_pmid(id)
    if pmid:
        return pmid, "PMID"

    # Check if it's a PubMed Central ID
    pmcid = validate_pmcid(id)
    if pmcid:
        return pmcid, "PMCID"

    # Check if it's a URL
    url_type = validate_url(id)
    if url_type:
        return normalize_url(id), url_type

    # No known valid identifier type was found
    return None, None


def openalex_api_url(id: str | None, identifier_type: str, **kwargs) -> str | None:
    """Return the OpenAlex API URL for a given ID"""
    if identifier_type == "DOI":
        return f"https://api.openalex.org/works/{doi_as_url(id)}"
    if identifier_type == "OpenAlex":
        return f"https://api.openalex.org/works/{id}"
    if identifier_type == "PMID":
        return f"https://api.openalex.org/works?filter=ids.pmid:{id}"
    if identifier_type == "PMCID":
        return f"https://api.openalex.org/works?filter=ids.pmcid:{id}"
    return None


def openalex_api_query_url(query: dict) -> str:
    """Return the OpenAlex API query URL"""
    # Define allowed types
    types = [
        "article",
        "book-chapter",
        "dataset",
        "preprint",
        "dissertation",
        "book",
        "review",
        "paratext",
        "libguides",
        "letter",
        "other",
        "reference-entry",
        "report",
        "editorial",
        "peer-review",
        "erratum",
        "standard",
        "grant",
        "supplementary-materials",
        "retraction",
    ]

    url = "https://api.openalex.org/works"
    f = furl(url)

    # Handle pagination and sample parameters
    number = max(1, min(1000, int(query.get("number", query.get("rows", 10)))))
    page = max(1, int(query.get("page", 1)))

    sample = query.get("sample", False)
    if sample:
        f.args["sample"] = str(number)
    else:
        f.args["per-page"] = str(number)
        f.args["page"] = str(page)
        # Sort results by published date in descending order
        f.args["sort"] = "publication_date:desc"

    # Build filters
    filters = []
    queries = []
    _query = None

    # Handle query parameters
    if query.get("query", None) is not None:
        queries += [query.get("query")]
    for key, value in query.items():
        if key in [
            "query.bibliographic",
            "query.author",
            "query.title",
            "query.container-title",
        ]:
            queries += [f"{key}:{value}"]
    if queries:
        _query = ",".join(queries)
        f.args["query"] = _query

    # Member/IDs filter
    ids = query.get("ids", query.get("member", ""))
    if ids:
        filters.append(f"member:{ids}")

    # Type filter
    type_ = query.get("type_", query.get("type", ""))
    if type_ and type_ in types:
        filters.append(f"type:{type_}")

    # ROR filter
    ror = query.get("ror", "")
    if ror:
        r = validate_ror(ror)
        if r:
            filters.append(f"authorships.institutions.ror:{r}")

    # ORCID filter
    orcid = query.get("orcid", "")
    if orcid:
        o = validate_orcid(orcid)
        if o:
            filters.append(f"authorships.author.orcid:{o}")

    # Year filter
    year = query.get("year", query.get("publication_year", ""))
    if year:
        filters.append(f"publication_year:{year}")

    # Other filters from the original function
    for key, value in query.items():
        if key in [
            "prefix",
            "has-full-text",
            "has-funder",
            "has-license",
        ]:
            filters.append(f"{key}:{value}")

    # Boolean filters
    # if query.get("hasORCID", query.get("has-orcid", False)):
    #     filters.append("has-orcid:true")

    # if query.get("hasReferences", query.get("has-references", False)):
    #     filters.append("has-references:true")

    # if query.get("hasAbstract", query.get("has-abstract", False)):
    #     filters.append("has-abstract:true")

    # Add filters to params if any exist
    if filters:
        f.args["filter"] = ",".join(filters)

    return f.url


def openalex_api_sample_url(number: int = 1, **kwargs) -> str:
    """Return the OpenAlex API URL for a sample of dois"""
    return f"https://api.openalex.org/works?sample={number}"


def normalize_isni(isni: str | None) -> str | None:
    """Normalize ISNI"""
    if isni is None or not isinstance(isni, str):
        return None
    isni = validate_isni(isni)
    if isni is None:
        return None
    return "https://isni.org/isni/" + isni


def normalize_name_identifier(ni: str | None) -> str | None:
    """Normalize name identifier"""
    if ni is None:
        return None
    if isinstance(ni, str):
        return normalize_orcid(ni) or normalize_ror(ni) or normalize_isni(ni)
    if isinstance(ni, dict):
        return format_name_identifier(ni)
    if isinstance(ni, list):
        return next(
            (format_name_identifier(i) for i in wrap(ni.get("nameIdentifiers", None))),
            None,
        )
    return None


def format_name_identifier(ni: str | dict | None) -> str | None:
    """format_name_identifier"""
    if ni is None:
        return None
    elif isinstance(ni, str):
        return normalize_orcid(ni) or normalize_ror(ni) or normalize_isni(ni)
    name_identifier = (
        ni.get("nameIdentifier", None)
        or ni.get("identifier", None)
        or ni.get("publisherIdentifier", None)
    )
    name_identifier_scheme = (
        ni.get("nameIdentifierScheme", None)
        or ni.get("scheme", None)
        or ni.get("publisherIdentifierScheme", None)
    )
    scheme_uri = ni.get("schemeURI", None) or ni.get("schemeUri", None)
    if name_identifier is None:
        return None
    elif name_identifier_scheme in ["ORCID", "orcid"]:
        return normalize_orcid(name_identifier)
    elif name_identifier_scheme == "ISNI":
        return normalize_isni(name_identifier)
    elif name_identifier_scheme == "ROR":
        return normalize_ror(name_identifier)
    elif validate_url(name_identifier) == "URL":
        return name_identifier
    elif isinstance(name_identifier, str) and scheme_uri is not None:
        return scheme_uri + name_identifier
    return None


def normalize_issn(string: str | dict | list | None, **kwargs) -> str | None:
    """Normalize ISSN
    Pick electronic issn if there are multiple
    Format issn as xxxx-xxxx"""
    content = kwargs.get("content", "#text")
    if string is None:
        return None
    if isinstance(string, str):
        issn = string
    elif isinstance(string, dict):
        issn = string.get(content, None)
    elif isinstance(string, list):
        issn = next(
            (i for i in string if i.get("media_type", None) == "electronic"), {}
        ).get(content, None)
    if issn is None:
        return None
    if len(issn) == 9:
        return issn
    if len(issn) == 8:
        return issn[0:4] + "-" + issn[4:8]
    return None


def dict_to_spdx(dct: dict) -> dict | None:
    """Convert a dict to SPDX"""
    dct.update({"url": normalize_cc_url(dct.get("url", None))})
    file_path = os.path.join(
        os.path.dirname(__file__), "resources", "spdx", "licenses.json"
    )
    with open(file_path, encoding="utf-8") as file:
        string = file.read()
        spdx = json.loads(string).get("licenses")
    license_ = next(
        (
            lic
            for lic in spdx
            if lic["licenseId"].casefold() == dct.get("id", "").casefold()
            or lic["seeAlso"][0] == dct.get("url", None)
        ),
        None,
    )
    if license_ is None:
        return compact(dct)
    #   license = spdx.find do |l|
    #     l['licenseId'].casecmp?(hsh['rightsIdentifier']) || l['seeAlso'].first == normalize_cc_url(hsh['rightsUri']) || l['name'] == hsh['rights'] || l['seeAlso'].first == normalize_cc_url(hsh['rights'])
    #   end
    return compact(
        {
            "id": license_["licenseId"],
            "url": license_["seeAlso"][0],
        }
    )

    #   else
    #     {
    #       'rights': hsh['#text'] || hsh['rights'],
    #       'rightsUri': hsh['rightsUri'] || hsh['rightsUri'],
    #       'rightsIdentifier': hsh['rightsIdentifier'].present? ? hsh['rightsIdentifier'].downcase : None,
    #       'rightsIdentifierScheme': hsh['rightsIdentifierScheme'],
    #       'schemeUri': hsh['schemeUri'],
    #       'lang': hsh['lang']
    #     }.compact
    #   end
    # end


def from_jsonfeed(elements: list) -> list:
    """Convert from JSON Feed elements"""

    def format_element(element):
        """format element"""
        if not isinstance(element, dict):
            return None
        mapping = {"url": "id"}
        for key, value in mapping.items():
            if element.get(key, None) is not None:
                element[value] = element.pop(key)
        return element

    return [format_element(i) for i in elements]


def from_inveniordm(elements: list) -> list:
    """Convert from inveniordm elements"""

    def format_element(element):
        """format element, merging the role and person_or_org subdicts"""
        role = dig(element, "role.id")

        if "person_or_org" in element.keys():
            element = element["person_or_org"]

        if not isinstance(element, dict):
            return None
        mapping = {"orcid": "ORCID"}
        for key, value in mapping.items():
            if element.get(key, None) is not None:
                element[value] = element.pop(key)
        element["contributorType"] = [role.capitalize()] if role else []

        return element

    return [format_element(i) for i in elements]


def to_inveniordm(elements: list) -> list:
    """Convert elements to InvenioRDM"""

    def format_element(i):
        """format element"""
        element = {}
        element["familyName"] = i.get("familyName", None)
        element["givenName"] = i.get("givenName", None)
        element["name"] = i.get("name", None)
        element["type"] = i.get("type", None)
        element["ORCID"] = i.get("ORCID", None)
        return compact(element)

    return [format_element(i) for i in elements]


def from_crossref_xml(elements: list) -> list:
    """Convert from crossref_xml elements"""

    def format_affiliation(element):
        """Format affiliation"""
        return {"name": element}

    def format_element(element):
        """format element"""
        if element.get("name", None) is not None:
            element["type"] = "Organization"
            element["name"] = element.get("name")
        else:
            element["type"] = "Person"
        element["givenName"] = element.get("given_name", None)
        element["familyName"] = element.get("surname", None)
        element["contributorType"] = element.get(
            "contributor_role", "author"
        ).capitalize()
        if element.get("ORCID", None) is not None:
            orcid = first(parse_attributes(element.get("ORCID")))
            element["ORCID"] = normalize_orcid(orcid)
        element = omit(element, "given_name", "surname", "sequence", "contributor_role")
        return compact(element)

    return [format_element(i) for i in elements]


def from_kbase(elements: list) -> list:
    """Convert from kbase elements"""

    def map_contributor_role(role):
        if role.split(":")[0] == "CRediT":
            return pascal_case(role.split(":")[1])
        elif role.split(":")[0] == "DataCite":
            return DATACITE_CONTRIBUTOR_TYPES.get(role.split(":")[1], "Other")
        else:
            return role.split(":")[1]

    def format_element(element):
        """format element"""
        if not isinstance(element, dict):
            return None
        if element.get("contributor_id", None) is not None:
            element["ORCID"] = from_curie(element["contributor_id"])
        element["contributor_roles"] = [
            map_contributor_role(i)
            for i in wrap(element.get("contributor_roles", None))
        ]
        element = omit(element, "contributor_id")
        return compact(element)

    return [format_element(i) for i in elements]


def from_csl(elements: list) -> list:
    """Convert from csl elements"""

    def format_element(element):
        """format element"""
        if element.get("literal", None) is not None:
            element["type"] = "Organization"
            element["name"] = element["literal"]
        elif element.get("name", None) is not None:
            element["type"] = "Organization"
            element["name"] = element.get("name")
        else:
            element["type"] = "Person"
            element["name"] = " ".join(
                [element.get("given", ""), element.get("family", "")]
            )
        element["givenName"] = element.get("given", None)
        element["familyName"] = element.get("family", None)
        element["affiliation"] = element.get("affiliation", None)
        element = omit(element, "given", "family", "literal", "sequence")
        return compact(element)

    return [format_element(i) for i in elements]


def to_csl(elements: list) -> list:
    """Convert elements to CSL-JSON"""

    def format_element(i):
        """format element"""
        element = {}
        element["family"] = i.get("familyName", None)
        element["given"] = i.get("givenName", None)
        element["literal"] = (
            i.get("name", None) if i.get("familyName", None) is None else None
        )
        return compact(element)

    return [format_element(i) for i in elements]


def to_ris(elements: list | None) -> list:
    """Convert element to RIS"""
    if elements is None:
        return []

    def format_element(i):
        """format element"""
        if i.get("familyName", None) and i.get("givenName", None):
            element = ", ".join([i["familyName"], i.get("givenName", None)])
        else:
            element = i.get("name", None)
        return element

    return [
        format_element(i)
        for i in elements
        if i.get("name", None) or i.get("familyName", None)
    ]


def to_schema_org(element: dict | None) -> dict | None:
    """Convert a metadata element to Schema.org"""
    if not isinstance(element, dict):
        return None
    mapping = {"type": "@type", "id": "@id", "title": "name"}
    for key, value in mapping.items():
        if element.get(key, None) is not None:
            element[value] = element.pop(key)
    return element


def to_schema_org_creators(elements: list) -> list:
    """Convert creators to Schema.org"""

    def format_element(element):
        """format element"""
        element["@type"] = element["type"][0:-2] if element.get("type", None) else None
        if element.get("familyName", None) and element.get("name", None) is None:
            element["name"] = " ".join(
                [element.get("givenName", None), element.get("familyName")]
            )
            element["@type"] = "Person"
        else:
            element["@type"] = "Organization"
        element = omit(element, "type", "contributorRoles")
        return compact(element)

    return [format_element(i) for i in elements]


def to_schema_org_container(element: dict | None, **kwargs) -> dict | None:
    """Convert CSL container to Schema.org container"""
    if element is None and kwargs.get("container_title", None) is None:
        return None
    if not isinstance(element, dict):
        return None

    return compact(
        {
            "@id": element.get("identifier", None),
            "@type": "DataCatalog"
            if kwargs.get("type", None) == "DataRepository"
            else "Periodical",
            "name": element.get("title", None) or kwargs.get("container_title", None),
        }
    )


def to_schema_org_identifiers(elements: list) -> list:
    """Convert identifiers to Schema.org"""

    def format_element(i):
        """format element"""
        element = {}
        element["@type"] = "PropertyValue"
        element["propertyID"] = i.get("identifierType", None)
        element["value"] = i.get("identifier", None)
        return compact(element)

    return [format_element(i) for i in elements]


def to_schema_org_relations(related_items: list, relation_type=None) -> list:
    """Convert relatedItems to Schema.org relations"""

    def format_element(i):
        """format element"""
        if i["relatedItemIdentifierType"] == "ISSN" and i["relationType"] == "IsPartOf":
            return compact({"@type": "Periodical", "issn": i["relatedItemIdentifier"]})
        return compact({"@id": normalize_id(i["relatedIdentifier"])})

    # consolidate different relation types
    if relation_type == "References":
        relation_type = ["References", "Cites"]
    else:
        relation_type = [relation_type]

    related_items = [
        ri for ri in wrap(related_items) if ri["relationType"] in relation_type
    ]
    return [format_element(i) for i in related_items]


def find_from_format(
    pid=None, string=None, ext=None, dct=None, filename=None
) -> str | None:
    """Find reader from format"""
    if pid is not None:
        return find_from_format_by_id(pid)
    if string is not None and ext is not None:
        return find_from_format_by_ext(ext)
    if dct is not None:
        return find_from_format_by_dict(dct)
    if string is not None:
        return find_from_format_by_string(string)
    if filename is not None:
        return find_from_format_by_filename(filename)
    return "datacite"


def find_from_format_by_id(pid: str) -> str:
    """Find reader from format by id"""
    doi = validate_doi(pid)
    if doi and (registration_agency := get_doi_ra(doi)) is not None:
        return registration_agency.lower()
    if (
        re.match(r"\A(http|https):/(/)?github\.com/(.+)/CITATION.cff\Z", pid)
        is not None
    ):
        return "cff"
    if (
        re.match(r"\A(http|https):/(/)?github\.com/(.+)/codemeta.json\Z", pid)
        is not None
    ):
        return "codemeta"
    if re.match(r"\A(http|https):/(/)?openalex\.org/(.+)\Z", pid) is not None:
        return "openalex"
    if (
        re.match(r"\A(http|https):/(/)?pubmed\.ncbi\.nlm\.nih\.gov/(.+)\Z", pid)
        is not None
    ):
        return "openalex"  # pmid
    if (
        re.match(
            r"\A(http|https):/(/)?www\.ncbi\.nlm\.nih\.gov/pmc/articles/(.+)\Z", pid
        )
        is not None
    ):
        return "openalex"  # pmcid
    if re.match(r"\A(http|https):/(/)?github\.com/(.+)\Z", pid) is not None:
        return "cff"
    if re.match(r"\Ahttps:/(/)?api\.rogue-scholar\.org/posts/(.+)\Z", pid) is not None:
        return "jsonfeed"
    if re.match(r"\Ahttps:/(/)(.+)/api/records/(.+)\Z", pid) is not None:
        return "inveniordm"
    return "schema_org"


def find_from_format_by_ext(ext: str) -> str | None:
    """Find reader from format by ext"""
    if ext == ".bib":
        return "bibtex"
    if ext == ".ris":
        return "ris"
    return None


def find_from_format_by_dict(dct: dict) -> str | None:
    if dct is None or not isinstance(dct, dict):
        return None
    """Find reader from format by dict"""
    if dct.get("schema_version", "").startswith("https://commonmeta.org"):
        return "commonmeta"
    if dct.get("@context", None) == "http://schema.org":
        return "schema_org"
    if dct.get("@context", None) in [
        "https://raw.githubusercontent.com/codemeta/codemeta/master/codemeta.jsonld"
    ]:
        return "codemeta"
    if dct.get("guid", None) is not None:
        return "jsonfeed"
    if dct.get("schemaVersion", "").startswith("http://datacite.org/schema/kernel"):
        return "datacite"
    if dct.get("source", None) == "Crossref":
        return "crossref"
    if dig(dct, "issued.date-parts") is not None:
        return "csl"
    if dig(dct, "conceptdoi") is not None:
        return "inveniordm"
    if dig(dct, "credit_metadata") is not None:
        return "kbase"
    return None


def find_from_format_by_string(string: str | None) -> str | None:
    """Find reader from format by string"""
    if string is None:
        return None
    try:
        data = json.loads(string)
        if not isinstance(data, dict):
            raise TypeError
        if data.get("schema", "").startswith("https://commonmeta.org"):
            return "commonmeta"
        if data.get("items", None) is not None:
            data = data["items"][0]
        if data.get("@context", None) == "http://schema.org":
            return "schema_org"
        if data.get("@context", None) in [
            "https://raw.githubusercontent.com/codemeta/codemeta/master/codemeta.jsonld"
        ]:
            return "codemeta"
        if data.get("guid", None) is not None:
            return "jsonfeed"
        if data.get("schemaVersion", "").startswith(
            "http://datacite.org/schema/kernel"
        ):
            return "datacite"
        if data.get("source", None) == "Crossref":
            return "crossref"
        if dig(data, "issued.date-parts") is not None:
            return "csl"
        if dig(data, "conceptdoi") is not None:
            return "inveniordm"
        if dig(data, "credit_metadata") is not None:
            return "kbase"
    except (TypeError, json.JSONDecodeError):
        pass
    try:
        data = BeautifulSoup(string, "xml")
        if data.find("doi_record"):
            return "crossref_xml"
        if data.find("resource"):
            return "datacite_xml"
    except ValueError:
        pass
    try:
        data = BeautifulSoup(string, "html.parser")
        if (
            data.find("script", type="application/ld+json")
            or data.find("meta", {"name": "citation_doi"})
            or data.find("meta", {"name": "dc.identifier"})
        ):
            return "schema_org"
    except ValueError:
        pass
    try:
        data = yaml.safe_load(string)
        if data.get("cff-version", None):
            return "cff"
    except (yaml.YAMLError, AttributeError):
        pass

    if string.startswith("TY  - "):
        return "ris"
    if any(string.startswith(f"@{t}") for t in bibtexparser.bibdatabase.STANDARD_TYPES):
        return "bibtex"

    # no format found
    return None


def find_from_format_by_filename(filename) -> str | None:
    """Find reader from format by filename"""
    if filename == "CITATION.cff":
        return "cff"
    return None


def from_schema_org(element: dict | None) -> dict | None:
    """Convert schema.org to DataCite"""
    if element is None:
        return None
    element["type"] = element.get("@type", None)
    element["id"] = element.get("@id", None)
    return compact(omit(element, ["@type", "@id"]))


def from_schema_org_creators(elements: list) -> list:
    """Convert schema.org creators to commonmeta"""

    def format_element(i):
        """format element"""
        element = {}
        if isinstance(i, str):
            return {"name": i}
        if urlparse(i.get("@id", None)).hostname == "orcid.org":
            element["id"] = i.get("@id")
            element["type"] = "Person"
        elif isinstance(i.get("@type", None), str):
            element["type"] = i.get("@type")
        elif isinstance(i.get("@type", None), list):
            # Find first element that matches the condition
            element["type"] = next(
                (x for x in i["@type"] if x in ["Person", "Organization"]), None
            )

        # strip text after comma if suffix is an academic title
        if str(i["name"]).split(", ", maxsplit=1)[-1] in [
            "MD",
            "PhD",
            "DVM",
            "DDS",
            "DMD",
            "JD",
            "MBA",
            "MPH",
            "MS",
            "MA",
            "MFA",
            "MSc",
            "MEd",
            "MEng",
            "MPhil",
            "MRes",
            "LLM",
            "LLB",
            "BSc",
            "BA",
            "BFA",
            "BEd",
            "BEng",
            "BPhil",
        ]:
            i["name"] = str(i["name"]).split(", ", maxsplit=1)[0]
        length = len(str(i["name"]).split(" "))
        if i.get("givenName", None):
            element["givenName"] = i.get("givenName", None)
        if i.get("familyName", None):
            element["familyName"] = i.get("familyName", None)
            element["type"] = "Person"
        # parentheses around the last word indicate an organization
        elif length > 1 and not str(i["name"]).rsplit(" ", maxsplit=1)[-1].startswith(
            "("
        ):
            element["givenName"] = " ".join(str(i["name"]).split(" ")[0 : length - 1])
            element["familyName"] = str(i["name"]).rsplit(" ", maxsplit=1)[1:]
        if not element.get("familyName", None):
            element["creatorName"] = compact(
                {
                    "type": i.get("@type", None),
                    "#text": i.get("name", None),
                }
            )

        if isinstance(i.get("affiliation", None), str):
            element["affiliation"] = {"type": "Organization", "name": i["affiliation"]}
        elif urlparse(dig(i, "affiliation.@id", "")).hostname in [
            "ror.org",
            "isni.org",
        ]:
            element["affiliation"] = {
                "id": i["affiliation"]["@id"],
                "type": "Organization",
                "name": i["affiliation"]["name"],
            }
        return compact(element)

    return [format_element(i) for i in wrap(elements)]


def github_from_url(url: str) -> dict:
    """Get github owner, repo, release and path from url"""

    match = re.match(
        r"\Ahttps://(github|raw\.githubusercontent)\.com/(.+)(?:/)?(.+)?(?:/tree/)?(.*)\Z",
        url,
    )
    if match is None:
        return {}
    words = urlparse(url).path.lstrip("/").split("/")
    owner = words[0] if len(words) > 0 else None
    repo = words[1] if len(words) > 1 else None
    release = words[3] if len(words) > 3 else None
    path = "/".join(words[4:]) if len(words) > 3 else ""
    if len(path) == 0:
        path = None

    return compact({"owner": owner, "repo": repo, "release": release, "path": path})


def github_repo_from_url(url: str) -> str | None:
    """Get github repo from url"""
    return github_from_url(url).get("repo", None)


def github_release_from_url(url: str) -> str | None:
    """Get github release from url"""
    return github_from_url(url).get("release", None)


def github_owner_from_url(url: str) -> str | None:
    """Get github owner from url"""
    return github_from_url(url).get("owner", None)


def github_as_owner_url(url: str) -> str | None:
    """Get github owner url from url"""
    github_dict = github_from_url(url)
    if github_dict.get("owner", None) is None:
        return None
    return f"https://github.com/{github_dict.get('owner')}"


def github_as_repo_url(url) -> str | None:
    """Get github repo url from url"""
    github_dict = github_from_url(url)
    if github_dict.get("repo", None) is None:
        return None
    return f"https://github.com/{github_dict.get('owner')}/{github_dict.get('repo')}"


def github_as_release_url(url: str) -> str | None:
    """Get github release url from url"""
    github_dict = github_from_url(url)
    if github_dict.get("release", None) is None:
        return None
    return f"https://github.com/{github_dict.get('owner')}/{github_dict.get('repo')}/tree/{github_dict.get('release')}"


def github_as_codemeta_url(url: str) -> str | None:
    """Get github codemeta.json url from url"""
    github_dict = github_from_url(url)

    if github_dict.get("path", None) and github_dict.get("path", "").endswith(
        "codemeta.json"
    ):
        return f"https://raw.githubusercontent.com/{github_dict.get('owner')}/{github_dict.get('repo')}/{github_dict.get('release')}/{github_dict.get('path')}"
    elif github_dict.get("owner", None):
        return f"https://raw.githubusercontent.com/{github_dict.get('owner')}/{github_dict.get('repo')}/master/codemeta.json"
    else:
        return None


def github_as_cff_url(url: str) -> str | None:
    """Get github CITATION.cff url from url"""
    github_dict = github_from_url(url)

    if github_dict.get("path", None) and github_dict.get("path", "").endswith(
        "CITATION.cff"
    ):
        return f"https://raw.githubusercontent.com/{github_dict.get('owner')}/{github_dict.get('repo')}/{github_dict.get('release')}/{github_dict.get('path')}"
    if github_dict.get("owner", None):
        return f"https://raw.githubusercontent.com/{github_dict.get('owner')}/{github_dict.get('repo')}/main/CITATION.cff"
    return None


def pages_as_string(container: dict | None, page_range_separator="-") -> str | None:
    """Parse pages for BibTeX"""
    if container is None:
        return None
    if container.get("firstPage", None) is None:
        return None
    if container.get("lastPage", None) is None:
        return container.get("firstPage", None)

    return page_range_separator.join(
        [container.get("firstPage"), container.get("lastPage", None)]
    )


def subjects_as_string(subjects) -> str | None:
    """convert subject list to string, e.g. for bibtex"""
    if subjects is None:
        return None

    keywords = []
    for subject in wrap(subjects):
        keywords.append(subject.get("subject", None))
    return ", ".join(keywords)


def string_to_slug(text: str) -> str:
    """Makes a string lowercase and removes non-alphanumeric characters"""

    # Remove optional FOS (Fields of Science) prefix
    text = text.removeprefix("FOS: ")

    # Convert to lowercase and keep only letters and numbers
    result = ""
    for char in text:
        if char.isalnum():
            result += char.lower()

    return result


# def reverse():
#       return { 'citation': wrap(related_identifiers).select do |ri|
#                         ri['relationType'] == 'IsReferencedBy'
#                       end.map do |r|
#                         { '@id': normalize_doi(r['relatedIdentifier']),
#                           '@type': r['resourceTypeGeneral'] validate_orcid 'ScholarlyArticle',
#                           'identifier': r['relatedIdentifierType'] == 'DOI' ? nil : to_identifier(r) }.compact
#                       end.unwrap,
#         'isBasedOn': wrap(related_identifiers).select do |ri|
#                          ri['relationType'] == 'IsSupplementTo'
#                        end.map do |r|
#                          { '@id': normalize_doi(r['relatedIdentifier']),
#                            '@type': r['resourceTypeGeneral'] or 'ScholarlyArticle',
#                            'identifier': r['relatedIdentifierType'] == 'DOI' ? nil : to_identifier(r) }.compact
#                        end.unwrap }.compact


def name_to_fos(name: str) -> dict | None:
    """Convert name to Fields of Science (OECD) subject"""

    subject = name.strip()
    fos_subject = FOS_MAPPINGS.get(name, None)
    if fos_subject is not None:
        return {"subject": f"FOS: {subject}"}
    return {"subject": subject}


def dict_to_fos(dct: dict) -> dict | None:
    """Convert dict to Fields of Science (OECD) subject"""
    if not isinstance(dct, dict):
        return None
    if dct.get("subject", None) is not None:
        return name_to_fos(dct["subject"])
    return None


def dict_to_openalex(dct: dict) -> dict | None:
    """Convert dict to OpenAlex subfield"""
    if not isinstance(dct, dict):
        return None
    if dct.get("id", None) is not None:
        return OPENALEX_SUBFIELD_MAPPINGS.get(dct["id"], None)
    return None


def from_curie(id: str | None) -> str | None:
    """from CURIE"""
    if id is None:
        return None
    _type = id.split(":")[0]
    if _type.upper() == "DOI":
        return doi_as_url(id.split(":")[1])
    elif _type.upper() == "ROR":
        return "https://ror.org/" + id.split(":")[1]
    elif _type.upper() == "ISNI":
        return "https://isni.org/isni/" + id.split(":")[1]
    elif _type.upper() == "ORCID":
        return normalize_orcid(id.split(":")[1])
    elif _type.upper() == "URL":
        return normalize_url(id.split(":")[1])
    elif _type.upper() == "JDP":
        return id.split(":")[1]
    # TODO: resolvable url for other identifier types
    return None


def extract_curie(string: str | None) -> str | None:
    """Extract CURIE"""
    if string is None:
        return None
    match = re.search(
        r"((?:doi|DOI):\s?([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))", string
    )
    if match is None:
        return None
    return doi_as_url(match.group(2))


def replace_curie(string: str | None) -> str | None:
    """Replace CURIE with DOI expressed as URL"""
    if string is None:
        return None
    match = re.sub(
        r"((?:doi|DOI):\s?([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))",
        r"https://doi.org/\2",
        string,
    )
    if match is None:
        return None
    return match


def extract_url(string: str) -> str | None:
    """Extract urls from string, including markdown and html."""

    match = re.search(
        r"((?:http|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))",
        string,
    )
    if match is None:
        return None
    return normalize_url(match.group(1))


def extract_urls(string: str) -> list:
    """Extract urls from string, including markdown and html."""

    urls = re.findall(
        r"((?:http|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))",
        string,
    )
    return unique(urls)


def issn_as_url(issn: str) -> str | None:
    """ISSN as URL"""
    if normalize_issn(issn) is None:
        return None
    return f"https://portal.issn.org/resource/ISSN/{issn}"


def issn_from_url(url: str) -> str | None:
    """ISSN from URL"""
    if url is None:
        return None
    match = re.match(r"\Ahttps://portal.issn.org/resource/ISSN/(.+)\Z", url)
    if match is None:
        return None
    return match.group(1)


def get_language(lang: str | None, format: str = "alpha_2") -> str | None:
    """Provide a language string based on ISO 639, with either a name in English,
    ISO 639-1, or ISO 639-3 code as input. Optionally format as alpha_2 (defaul),
    alpha_3, or name.
    """
    if not lang:
        return None
    if len(lang) == 2:
        language = pycountry.languages.get(alpha_2=lang)
    elif len(lang) == 3:
        language = pycountry.languages.get(alpha_3=lang)
    else:
        language = pycountry.languages.get(name=lang)

    if language is None:
        return None
    elif format == "name":
        return language.name
    elif format == "alpha_3":
        return language.alpha_3

    else:
        return language.alpha_2


def start_case(content: str) -> str:
    """Capitalize first letter of each word without lowercasing the rest"""
    words = content.split(" ")
    content = " ".join([word[0].upper() + word[1:] for word in words])
    return content


def timer_func(func):
    def function_timer(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "{func} took {time} seconds to complete its execution."
        print(msg.format(func=func.__name__, time=runtime))
        return value

    return function_timer


def id_from_url(url: str | None) -> str | None:
    """Return a ID from a URL"""
    if url is None:
        return None

    f = furl(url)
    # check for allowed scheme if string is a URL
    if f.host is not None and f.scheme not in ["http", "https", "ftp"]:
        return None

    return str(f.path).strip("/")


def is_chain_object(string: Any) -> bool:
    """Check if the given string is a ChainObject-like object,
    for example the invenio-rdm-records ChainObject.

    Checks for both the _child and _parent attributes to ensure it's a proper chain object.
    """
    if string is None:
        return False
    return hasattr(string, "_child") and hasattr(string, "_parent")
