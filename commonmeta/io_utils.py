"""File utils module for commonmeta-py.

Reading and writing files, including compression and PDF.
"""

from __future__ import annotations

import atexit
import gzip
import io
import logging
import os
import re
import sys
import zipfile
from base64 import b64encode
from datetime import date as date_type
from datetime import datetime
from functools import lru_cache
from html import escape, unescape
from pathlib import Path
from typing import TYPE_CHECKING

import nh3
import requests
import zstandard
from babel.core import UnknownLocaleError
from babel.dates import format_date
from bs4 import BeautifulSoup

from .api_utils import http
from .base_utils import dig, presence, unique, wrap
from .date_utils import get_iso8601_date
from .doi_utils import doi_from_url
from .utils import get_language, validate_orcid

if TYPE_CHECKING:
    from .metadata import Metadata

log = logging.getLogger(__name__)


def read_file(filename: str) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


def uncompress_content(input: bytes) -> bytes:
    with gzip.GzipFile(fileobj=io.BytesIO(input)) as gz:
        return gz.read()


def unzip_content(input: bytes, filename: str | None = None) -> bytes:
    output = b""
    with zipfile.ZipFile(io.BytesIO(input)) as zf:
        for info in zf.infolist():
            if filename and info.filename != filename:
                continue
            with zf.open(info) as file:
                output += file.read()
    return output


def read_gz_file(filename: str) -> bytes:
    input_bytes = read_file(filename)
    return uncompress_content(input_bytes)


def read_zip_file(filename: str, name: str | None = None) -> bytes:
    input_bytes = read_file(filename)
    return unzip_content(input_bytes, name)


def download_file(url: str) -> bytes:
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    return resp.content


def write_file(filename: str, output: bytes) -> None:
    with open(filename, "xb") as f:
        f.write(output)


def write_gz_file(filename: str, output: bytes) -> None:
    with gzip.open(filename, "xb") as gzfile:
        gzfile.write(output)


def write_zip_file(filename: str, output: bytes) -> None:
    path = Path(filename)
    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(path.name, output)


def write_zst_file(filename: str, output: bytes) -> None:
    compressor = zstandard.ZstdCompressor()
    with open(filename, "xb") as f:
        f.write(compressor.compress(output))


def get_extension(filename: str) -> tuple[str, str, str | None]:
    """Extract extension and compression from filename"""
    extension = Path(filename).suffix
    if extension == ".gz":
        compress = ".gz"
        filename = filename[:-3]
        extension = Path(filename).suffix
    elif extension == ".zip":
        compress = ".zip"
        filename = filename[:-4]
        extension = Path(filename).suffix
    elif extension == ".zst":
        compress = ".zst"
        filename = filename[:-4]
        extension = Path(filename).suffix
    elif extension == "":
        compress = None
        filename = filename + ".json"
        extension = ".json"
    else:
        compress = None
    return filename, extension, compress


def write_output(filename: str, input: bytes | str, ext: list[str]) -> None:
    """Write output to file with supported extension.

    Text formats arrive as a string and binary ones - a pdf rendition, a
    parquet file - as bytes; both are written as they are, so `ext` is what
    says which extensions a caller means to produce.
    """

    # Convert string to bytes if necessary
    if isinstance(input, str):
        input = input.encode("utf-8")

    filename, extension, compress = get_extension(filename)
    if extension not in ext:
        raise ValueError(
            f"File format not supported. Please provide a filename with {ext} extension."
        )
    if compress == ".gz":
        write_gz_file(filename + compress, input)
    elif compress == ".zip":
        write_zip_file(filename + compress, input)
    elif compress == ".zst":
        write_zst_file(filename + compress, input)
    else:
        write_file(filename, input)


# Stylesheet and fonts for the pdf rendition, shipped with the package.
PDF_RESOURCES = Path(__file__).parent / "resources" / "pdf"

# The PDF variant used for writing PDF files. # WeasyPrint only knows the accessible ("a") conformance levels since 67, hence
# the >=69 floor in pyproject.toml.
PDF_VARIANT = "pdf/a-3a"

# The markup a title or a description is allowed to carry into the pdf. Post
# titles are html, and an italicised species name says something an escaped
# <i> does not; anything that lays out, loads or runs is dropped.
PDF_INLINE_TAGS = {
    "a",
    "abbr",
    "b",
    "br",
    "cite",
    "code",
    "em",
    "i",
    "mark",
    "q",
    "s",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "u",
}

# What the id of a subject says it is: an OpenAlex subfield is /subfields/
# <number> and a topic is /T<number>. A tag the post gave itself has no id, and
# is named as it is - which is what tells the two apart on the page.
SUBJECT_LABELS = (
    ("https://openalex.org/subfields/", "Subfield"),
    ("https://openalex.org/T", "Topic"),
)

# The field of science a record was classified into. Left off the title page:
# it is the coarsest of the three classifications and the one that says least
# about a post - "Languages and literature" under a post about connectionism.
FOS_SUBJECT_PREFIX = "http://www.oecd.org/science/inno/38235147.pdf?"

# The characters a page drops rather than draw from a colour font: the
# pictograph blocks, the dingbats and miscellaneous symbols that have an emoji
# presentation, and the joiners and selectors that build the rest out of them.
# A run of them takes the spaces around it with it, so a title that used one
# as a separator does not keep the gap where it stood.
EMOJI = re.compile(
    "[ \t]*"
    "[\U0001f000-\U0001faff\u2600-\u27bf\u2b00-\u2bff\ufe0f\u20e3\u200d]+"
    "[ \t]*"
)

#: The csl locale a record is cited in, for the languages a rendition is
#: written in. Anything else is cited in en-US, the locale citeproc falls back
#: to anyway.
PDF_CITATION_LOCALES = {
    "en": "en-US",
    "de": "de-DE",
    "es": "es-ES",
    "fr": "fr-FR",
    "it": "it-IT",
    "pt": "pt-PT",
}

#: What holds the words of a name together on the page.
NO_BREAK_SPACE = "\u00a0"

# Front matter headings, in the languages rogue-scholar-api translated them to.
PDF_TITLES = {
    "published": {
        "en": "Published",
        "de": "Veröffentlicht",
        "es": "Publicado",
        "fr": "Publié",
        "it": "Pubblicato",
        "pt": "Publicados",
    },
    "abstract": {
        "en": "Abstract",
        "de": "Zusammenfassung",
        "es": "Resumen",
        "fr": "Résumé",
        "it": "Riassunto",
        "pt": "Resumo",
    },
    "copyright": {
        "en": "Copyright",
        "de": "Urheberrecht",
        "es": "Copyright",
        "fr": "Droit d'auteur",
        "it": "Copyright",
        "pt": "Direitos de autor",
    },
    "keywords": {
        "en": "Keywords",
        "de": "Schlüsselwörter",
        "es": "Palabras clave",
        "fr": "Mots clés",
        "it": "Parole chiave",
        "pt": "Palavras-chave",
    },
    # the alt description an image gets when the post gives it none
    "image": {
        "en": "Image",
        "de": "Bild",
        "es": "Imagen",
        "fr": "Image",
        "it": "Immagine",
        "pt": "Imagem",
    },
    "citation": {
        "en": "Recommended citation",
        "de": "Empfohlene Zitierweise",
        "es": "Cita recomendada",
        "fr": "Citation recommandée",
        "it": "Citazione consigliata",
        "pt": "Citação recomendada",
    },
    "references": {
        "en": "References",
        "de": "Literatur",
        "es": "Referencias",
        "fr": "Références",
        "it": "Riferimenti",
        "pt": "Referências",
    },
    # and the one the poster frame of a video gets
    "video": {
        "en": "Video",
        "de": "Video",
        "es": "Vídeo",
        "fr": "Vidéo",
        "it": "Video",
        "pt": "Vídeo",
    },
}

#: What a work is called on the title page. The English name of a type is its
#: camel case split into words - a JournalArticle is a journal article - so
#: only the other languages are named here.
PDF_TYPE_NAMES = {
    "de": {
        "Audiovisual": "Audiovisuelles Medium",
        "Blog": "Blog",
        "BlogPost": "Blogbeitrag",
        "BlogVolume": "Blogjahrgang",
        "Book": "Buch",
        "BookChapter": "Buchkapitel",
        "BookPart": "Buchteil",
        "BookSection": "Buchabschnitt",
        "BookSeries": "Buchreihe",
        "BookSet": "Buchsammlung",
        "Collection": "Sammlung",
        "Component": "Komponente",
        "ComputationalNotebook": "Computational Notebook",
        "Database": "Datenbank",
        "Dataset": "Datensatz",
        "Dissertation": "Dissertation",
        "Document": "Dokument",
        "Entry": "Eintrag",
        "Event": "Veranstaltung",
        "Figure": "Abbildung",
        "Grant": "Förderung",
        "Image": "Bild",
        "Instrument": "Instrument",
        "InteractiveResource": "Interaktive Ressource",
        "Journal": "Zeitschrift",
        "JournalArticle": "Zeitschriftenartikel",
        "JournalIssue": "Zeitschriftenheft",
        "JournalVolume": "Zeitschriftenband",
        "LegalDocument": "Rechtsdokument",
        "Manuscript": "Manuskript",
        "Map": "Karte",
        "Model": "Modell",
        "OutputManagementPlan": "Datenmanagementplan",
        "Patent": "Patent",
        "PeerReview": "Gutachten",
        "Performance": "Aufführung",
        "PersonalCommunication": "Persönliche Mitteilung",
        "PhysicalObject": "Physisches Objekt",
        "Poster": "Poster",
        "Preprint": "Preprint",
        "Presentation": "Präsentation",
        "Proceedings": "Konferenzband",
        "ProceedingsArticle": "Konferenzbeitrag",
        "ProceedingsSeries": "Konferenzreihe",
        "Report": "Bericht",
        "ReportComponent": "Berichtskomponente",
        "ReportSeries": "Berichtsreihe",
        "Review": "Begutachtung",
        "Service": "Dienst",
        "Software": "Software",
        "Sound": "Tonaufnahme",
        "Standard": "Norm",
        "StudyRegistration": "Studienregistrierung",
        "WebPage": "Webseite",
        "Workflow": "Workflow",
    },
    "es": {
        "Audiovisual": "Material audiovisual",
        "Blog": "Blog",
        "BlogPost": "Entrada de blog",
        "BlogVolume": "Volumen de blog",
        "Book": "Libro",
        "BookChapter": "Capítulo de libro",
        "BookPart": "Parte de libro",
        "BookSection": "Sección de libro",
        "BookSeries": "Serie de libros",
        "BookSet": "Colección de libros",
        "Collection": "Colección",
        "Component": "Componente",
        "ComputationalNotebook": "Cuaderno computacional",
        "Database": "Base de datos",
        "Dataset": "Conjunto de datos",
        "Dissertation": "Tesis",
        "Document": "Documento",
        "Entry": "Entrada",
        "Event": "Evento",
        "Figure": "Figura",
        "Grant": "Subvención",
        "Image": "Imagen",
        "Instrument": "Instrumento",
        "InteractiveResource": "Recurso interactivo",
        "Journal": "Revista",
        "JournalArticle": "Artículo de revista",
        "JournalIssue": "Número de revista",
        "JournalVolume": "Volumen de revista",
        "LegalDocument": "Documento legal",
        "Manuscript": "Manuscrito",
        "Map": "Mapa",
        "Model": "Modelo",
        "OutputManagementPlan": "Plan de gestión de datos",
        "Patent": "Patente",
        "PeerReview": "Revisión por pares",
        "Performance": "Actuación",
        "PersonalCommunication": "Comunicación personal",
        "PhysicalObject": "Objeto físico",
        "Poster": "Póster",
        "Preprint": "Prepublicación",
        "Presentation": "Presentación",
        "Proceedings": "Actas de congreso",
        "ProceedingsArticle": "Ponencia",
        "ProceedingsSeries": "Serie de actas",
        "Report": "Informe",
        "ReportComponent": "Componente de informe",
        "ReportSeries": "Serie de informes",
        "Review": "Revisión",
        "Service": "Servicio",
        "Software": "Software",
        "Sound": "Grabación sonora",
        "Standard": "Norma",
        "StudyRegistration": "Registro de estudio",
        "WebPage": "Página web",
        "Workflow": "Flujo de trabajo",
    },
    "fr": {
        "Audiovisual": "Document audiovisuel",
        "Blog": "Blog",
        "BlogPost": "Billet de blog",
        "BlogVolume": "Volume de blog",
        "Book": "Livre",
        "BookChapter": "Chapitre de livre",
        "BookPart": "Partie de livre",
        "BookSection": "Section de livre",
        "BookSeries": "Collection de livres",
        "BookSet": "Ensemble de livres",
        "Collection": "Collection",
        "Component": "Composant",
        "ComputationalNotebook": "Carnet de calcul",
        "Database": "Base de données",
        "Dataset": "Jeu de données",
        "Dissertation": "Thèse",
        "Document": "Document",
        "Entry": "Entrée",
        "Event": "Événement",
        "Figure": "Figure",
        "Grant": "Financement",
        "Image": "Image",
        "Instrument": "Instrument",
        "InteractiveResource": "Ressource interactive",
        "Journal": "Revue",
        "JournalArticle": "Article de revue",
        "JournalIssue": "Numéro de revue",
        "JournalVolume": "Volume de revue",
        "LegalDocument": "Document juridique",
        "Manuscript": "Manuscrit",
        "Map": "Carte",
        "Model": "Modèle",
        "OutputManagementPlan": "Plan de gestion des données",
        "Patent": "Brevet",
        "PeerReview": "Évaluation par les pairs",
        "Performance": "Performance",
        "PersonalCommunication": "Communication personnelle",
        "PhysicalObject": "Objet physique",
        "Poster": "Affiche",
        "Preprint": "Prépublication",
        "Presentation": "Présentation",
        "Proceedings": "Actes de conférence",
        "ProceedingsArticle": "Communication de conférence",
        "ProceedingsSeries": "Série d'actes",
        "Report": "Rapport",
        "ReportComponent": "Composant de rapport",
        "ReportSeries": "Série de rapports",
        "Review": "Évaluation",
        "Service": "Service",
        "Software": "Logiciel",
        "Sound": "Enregistrement sonore",
        "Standard": "Norme",
        "StudyRegistration": "Enregistrement d'étude",
        "WebPage": "Page web",
        "Workflow": "Flux de travail",
    },
    "it": {
        "Audiovisual": "Materiale audiovisivo",
        "Blog": "Blog",
        "BlogPost": "Articolo di blog",
        "BlogVolume": "Volume di blog",
        "Book": "Libro",
        "BookChapter": "Capitolo di libro",
        "BookPart": "Parte di libro",
        "BookSection": "Sezione di libro",
        "BookSeries": "Collana di libri",
        "BookSet": "Raccolta di libri",
        "Collection": "Raccolta",
        "Component": "Componente",
        "ComputationalNotebook": "Notebook computazionale",
        "Database": "Banca dati",
        "Dataset": "Insieme di dati",
        "Dissertation": "Tesi",
        "Document": "Documento",
        "Entry": "Voce",
        "Event": "Evento",
        "Figure": "Figura",
        "Grant": "Finanziamento",
        "Image": "Immagine",
        "Instrument": "Strumento",
        "InteractiveResource": "Risorsa interattiva",
        "Journal": "Rivista",
        "JournalArticle": "Articolo di rivista",
        "JournalIssue": "Fascicolo di rivista",
        "JournalVolume": "Volume di rivista",
        "LegalDocument": "Documento giuridico",
        "Manuscript": "Manoscritto",
        "Map": "Mappa",
        "Model": "Modello",
        "OutputManagementPlan": "Piano di gestione dei dati",
        "Patent": "Brevetto",
        "PeerReview": "Revisione tra pari",
        "Performance": "Spettacolo",
        "PersonalCommunication": "Comunicazione personale",
        "PhysicalObject": "Oggetto fisico",
        "Poster": "Poster",
        "Preprint": "Preprint",
        "Presentation": "Presentazione",
        "Proceedings": "Atti di convegno",
        "ProceedingsArticle": "Contributo in atti di convegno",
        "ProceedingsSeries": "Serie di atti",
        "Report": "Rapporto",
        "ReportComponent": "Componente di rapporto",
        "ReportSeries": "Serie di rapporti",
        "Review": "Recensione",
        "Service": "Servizio",
        "Software": "Software",
        "Sound": "Registrazione sonora",
        "Standard": "Norma",
        "StudyRegistration": "Registrazione di studio",
        "WebPage": "Pagina web",
        "Workflow": "Flusso di lavoro",
    },
    "pt": {
        "Audiovisual": "Material audiovisual",
        "Blog": "Blogue",
        "BlogPost": "Publicação de blogue",
        "BlogVolume": "Volume de blogue",
        "Book": "Livro",
        "BookChapter": "Capítulo de livro",
        "BookPart": "Parte de livro",
        "BookSection": "Secção de livro",
        "BookSeries": "Série de livros",
        "BookSet": "Coleção de livros",
        "Collection": "Coleção",
        "Component": "Componente",
        "ComputationalNotebook": "Caderno computacional",
        "Database": "Base de dados",
        "Dataset": "Conjunto de dados",
        "Dissertation": "Tese",
        "Document": "Documento",
        "Entry": "Entrada",
        "Event": "Evento",
        "Figure": "Figura",
        "Grant": "Financiamento",
        "Image": "Imagem",
        "Instrument": "Instrumento",
        "InteractiveResource": "Recurso interativo",
        "Journal": "Revista",
        "JournalArticle": "Artigo de revista",
        "JournalIssue": "Número de revista",
        "JournalVolume": "Volume de revista",
        "LegalDocument": "Documento jurídico",
        "Manuscript": "Manuscrito",
        "Map": "Mapa",
        "Model": "Modelo",
        "OutputManagementPlan": "Plano de gestão de dados",
        "Patent": "Patente",
        "PeerReview": "Revisão por pares",
        "Performance": "Espetáculo",
        "PersonalCommunication": "Comunicação pessoal",
        "PhysicalObject": "Objeto físico",
        "Poster": "Cartaz",
        "Preprint": "Preprint",
        "Presentation": "Apresentação",
        "Proceedings": "Atas de conferência",
        "ProceedingsArticle": "Comunicação em conferência",
        "ProceedingsSeries": "Série de atas",
        "Report": "Relatório",
        "ReportComponent": "Componente de relatório",
        "ReportSeries": "Série de relatórios",
        "Review": "Revisão",
        "Service": "Serviço",
        "Software": "Software",
        "Sound": "Gravação sonora",
        "Standard": "Norma",
        "StudyRegistration": "Registo de estudo",
        "WebPage": "Página web",
        "Workflow": "Fluxo de trabalho",
    },
}

#: How a language says what the work is and when it came out. English and
#: German follow the name of the type with a participle; the romance languages
#: name the date instead, which is what keeps the participle from having to
#: agree in gender with each of the fifty-odd nouns above.
PDF_PUBLISHED = {
    "en": "{type} published {date}",
    "de": "{type} veröffentlicht am {date}",
    "es": "{type}, fecha de publicación: {date}",
    "fr": "{type}, date de publication : {date}",
    "it": "{type}, data di pubblicazione: {date}",
    "pt": "{type}, data de publicação: {date}",
}

#: And how it says it of a work that came out in something - the journal or
#: the blog it belongs to. The name of that goes next to the type rather than
#: at the end of the line, which is what keeps the romance sentences readable.
PDF_PUBLISHED_IN = {
    "en": "{type} published {date} in {container}",
    "de": "{type} veröffentlicht am {date} in {container}",
    "es": "{type} en {container}, fecha de publicación: {date}",
    "fr": "{type} dans {container}, date de publication : {date}",
    "it": "{type} in {container}, data di pubblicazione: {date}",
    "pt": "{type} em {container}, data de publicação: {date}",
}

#: What a post calls the reference list it prints itself: the headings the
#: rendition would write, and the ones a blog writes instead.
REFERENCE_HEADINGS = {
    heading.casefold()
    for heading in (
        *PDF_TITLES["references"].values(),
        "Bibliografia",
        "Bibliografía",
        "Bibliographie",
        "Bibliography",
        "Literaturverzeichnis",
        "Reference list",
        "Referenzen",
        "Works cited",
    )
}


def to_pdf_author(contributor: dict) -> str | None:
    """Format a contributor for the pdf byline, given name first"""
    person = contributor.get("person", None) or {}
    name = " ".join(
        n
        for n in (person.get("given_name", None), person.get("family_name", None))
        if n
    )
    return name or (contributor.get("organization", None) or {}).get("name", None)


def to_pdf_authors(metadata: Metadata) -> list:
    """The authors of the post, each with the orcid it has, if it has one."""
    authors = []
    for contributor in wrap(metadata.contributors):
        if "Author" not in wrap(contributor.get("roles", None)):
            continue
        name = to_pdf_author(contributor)
        if not name:
            continue
        person = contributor.get("person", None) or {}
        authors.append({"name": name, "orcid": validate_orcid(person.get("id", None))})
    return authors


def to_pdf_byline(authors: list) -> str:
    """The byline, with each name that has an orcid linking to it.

    The name carries the link and the orcid icon marks it, which is how ORCID
    asks for an iD to be shown next to a name and what the rogue-scholar-api
    template did. The icon is a file next to the stylesheet, so it resolves
    against the same base url the fonts do.

    A name is held together by no-break spaces: a byline that ran to a second
    line broke "Nees Jan van Eck" across it, leaving half a person at the end
    of one line. The comma between two names is where the line breaks instead.
    """
    names = []
    for author in authors:
        # the metadata keeps the ordinary spaces: this is how the name is set,
        # not how it is written
        name = f"<span>{escape(author['name']).replace(' ', NO_BREAK_SPACE)}</span>"
        orcid = author.get("orcid", None)
        if orcid:
            url = f"https://orcid.org/{orcid}"
            name = (
                f'<a href="{url}">{name}'
                f'<img class="orcid" alt="ORCID iD" src="orcid.svg" /></a>'
            )
        names.append(name)
    return f'<p class="author">{", ".join(names)}</p>' if names else ""


def to_pdf_keywords(metadata: Metadata) -> list:
    """The keywords for the title page: the subjects a reader can use.

    Each classification says what kind it is, so a reader can tell it from a
    tag the post gave itself.
    """

    def to_keyword(subject: dict) -> str | None:
        name = subject.get("subject", None)
        if not name:
            return None
        identifier = subject.get("id", None) or ""
        if identifier.startswith(FOS_SUBJECT_PREFIX):
            return None
        for prefix, label in SUBJECT_LABELS:
            if identifier.startswith(prefix):
                return f"{name} ({label})"
        return name

    return unique(
        [
            keyword
            for keyword in (to_keyword(s) for s in wrap(metadata.subjects))
            if keyword
        ]
    )


def strip_emoji(text: str) -> str:
    """Text with its emoji removed, for the page rather than the metadata.

    An emoji is drawn from whatever colour font the machine has - Apple Color
    Emoji on a mac - and the glyph widths such a font declares do not match
    the ones WeasyPrint writes for it, which fails PDF/A (ISO 19005-3
    6.2.11.5) and costs the rendition the archival conformance it is made
    for. A title reading "AIMOS Presentation 🔸 Mindless Transparency" loses
    its diamonds on the page and keeps them in the pdf's own metadata, where
    they are text rather than something to draw.
    """
    # a separator becomes the one space it separated with, and an emoji that
    # sat against a word leaves nothing behind
    return EMOJI.sub(
        lambda match: " " if match.group() != match.group().strip() else "", text
    )


def to_pdf_markup(text: str | None) -> str:
    """A title, description or citation with the inline markup it carries.

    Post titles are html: "The atlas/axis complex of <i>Apatosaurus louisae</i>
    CM 3018" says something the same string with its tags escaped does not, and
    a citation of it says the same in <i>, <sub> and <sup>. Only inline markup
    survives - anything that would lay out, load or run is dropped rather than
    shown as text - and of the attributes only the address a link points at,
    which is worth as much on paper as it is on a page.
    """
    if not text:
        return ""
    return nh3.clean(
        text, tags=PDF_INLINE_TAGS, attributes={"a": {"href"}}, link_rel=None
    )


def to_pdf_text(text: str | None) -> str:
    """The same title or description as plain text, for the pdf's metadata.

    An info dictionary and an XMP packet hold text, not markup, so the tags
    come out and the entities they leave behind are resolved: what a reader's
    viewer shows as the document's title.
    """
    if not text:
        return ""
    return unescape(nh3.clean(text, tags=set()))


def to_pdf_date(date: str | None, language: str) -> str | None:
    """Format a publication date the way a reader writes it, in its language.

    Falls back to the iso date for anything babel cannot make a long date of,
    a partial date such as "2024-10" among them.
    """
    if not date:
        return None
    iso = get_iso8601_date(date)
    try:
        return format_date(date_type.fromisoformat(iso), format="long", locale=language)
    except (ValueError, TypeError, UnknownLocaleError) as error:
        log.warning(f"Cannot format date {date} for the pdf: {error}")
        return iso


def to_pdf_type(type: str | None, language: str) -> str | None:
    """What the record is, named in the language the rendition is written in.

    "Other" names nothing a reader can use, so it is left off the page, and a
    type no language has a name for is called what its camel case says: a
    JournalArticle is a journal article.
    """
    if not type or type == "Other":
        return None
    name = PDF_TYPE_NAMES.get(language, {}).get(type, None)
    if name:
        return name
    return re.sub(r"(?<!^)(?=[A-Z])", " ", type).capitalize()


def to_pdf_container(metadata: Metadata) -> str | None:
    """The journal or blog the work came out in, as the title page names it.

    Set in italics, the way a citation sets it, and named rather than linked:
    the one address a title page points at is the record's own, on the line
    below.
    """
    title = (metadata.container or {}).get("title", None)
    if not title:
        return None
    return f"<i>{to_pdf_markup(title)}</i>"


def to_pdf_published(metadata: Metadata, language: str) -> str | None:
    """The line under the byline: what the record is, when it came out, and
    what it came out in.

    A rendition says "Journal article published May 27, 2026 in <i>Journal of
    Medicinal Chemistry</i>" rather than the date alone, so the reader of a
    loose pdf can tell what they are holding. A record whose type says nothing
    keeps the date on its own, as does one that belongs to nothing.
    """
    date = to_pdf_date(metadata.date_published, language)
    if not date:
        return None
    name = to_pdf_type(metadata.type, language)
    if not name:
        label = PDF_TITLES["published"].get(language, PDF_TITLES["published"]["en"])
        return f"{label} {escape(date)}"
    container = to_pdf_container(metadata)
    if not container:
        template = PDF_PUBLISHED.get(language, PDF_PUBLISHED["en"])
        return template.format(type=escape(name), date=escape(date))
    template = PDF_PUBLISHED_IN.get(language, PDF_PUBLISHED_IN["en"])
    return template.format(type=escape(name), date=escape(date), container=container)


def to_pdf_citation(metadata: Metadata, language: str) -> str | None:
    """How to cite the work, in apa and in the language of the rendition.

    The reader of a loose pdf is one copy-paste away from citing it properly,
    which is the whole point of putting it there. A record the citation
    processor cannot make a citation of gets no such section.
    """
    locale = PDF_CITATION_LOCALES.get(language, "en-US")
    try:
        citation = metadata.write(to="citation", style="apa", locale=locale)
    except Exception as error:  # the citation processor raises what it likes
        log.warning(f"Cannot cite {metadata.id} in the pdf: {error}")
        return None
    if not citation:
        return None
    if isinstance(citation, bytes):
        citation = citation.decode("utf-8")
    # what the writer returns when it cannot cite the record
    if citation.startswith("Error: "):
        log.warning(f"Cannot cite {metadata.id} in the pdf: {citation}")
        return None
    return to_pdf_markup(citation).strip() or None


def to_pdf_rights(metadata: Metadata, authors: list, language: str) -> str | None:
    """Format the copyright line and the terms the PDF is available under."""
    url = (metadata.license or {}).get("url", None)
    identifier = (metadata.license or {}).get("id", None)
    if not url and not identifier:
        return None

    link = f'<a href="{escape(url)}">' if url else "<span>"
    close = "</a>" if url else "</span>"
    if (identifier or "").lower().startswith("cc0"):
        return (
            "This is an open access article, free of all copyright, and may be "
            "freely reproduced, distributed, transmitted, modified, built upon, "
            "or otherwise used by anyone for any lawful purpose. The work is "
            f"made available under the {link}Creative Commons CC0 public domain "
            f"dedication{close}."
        )

    year = (get_iso8601_date(metadata.date_published) or "")[:4]
    holder = authors[0] if authors else ""
    if len(authors) > 1:
        holder += " et al."
    copyright_line = (
        f'Copyright <span class="copyright">&copy;</span> '
        f"{escape(holder)} {year}.".replace("  ", " ")
    )
    if (identifier or "").lower().startswith("cc-by-4.0"):
        return (
            f"{copyright_line} Distributed under the terms of the {link}Creative "
            f"Commons Attribution 4.0 International License{close}, which permits "
            "unrestricted use, distribution, and reproduction in any medium, "
            "provided the original author and source are credited."
        )
    return (
        f"{copyright_line} Distributed under the terms of the "
        f"{link}{escape(str(identifier or url or ''))}{close} license."
    )


def to_pdf_metadata(metadata: Metadata, authors: list) -> list:
    """The meta tags WeasyPrint turns into the pdf's own metadata.

    Each one lands in both the info dictionary and the XMP packet that PDF/A
    requires: author as /Author and dc:creator, description as /Subject and
    dc:description, keywords as /Keywords and pdf:Keywords, the dcterms dates
    as /CreationDate and /ModDate and their xmp counterparts. `read_pdf_metadata`
    reads them back out. The doi and the licence have no meta tag of their own
    and are written afterwards, by `finish_pdf`.
    """
    tags = [
        f'<meta name="author" content="{escape(author["name"])}">' for author in authors
    ]
    description = to_pdf_text(metadata.description)
    if description:
        tags.append(f'<meta name="description" content="{escape(description)}">')
    # the same keywords the title page prints, so the pdf says one thing
    keywords = to_pdf_keywords(metadata)
    if keywords:
        tags.append(f'<meta name="keywords" content="{escape(", ".join(keywords))}">')
    platform = (metadata.container or {}).get("platform", None)
    if platform:
        tags.append(f'<meta name="generator" content="{escape(platform)}">')
    for name, date in (
        ("dcterms.created", metadata.date_published),
        ("dcterms.modified", metadata.date_updated),
    ):
        # W3C-DTF, which is what WeasyPrint parses these as; the iso date is
        # the part of it every record has
        if date:
            tags.append(f'<meta name="{name}" content="{get_iso8601_date(date)}">')
    return tags


def to_data_uri(url: str, what: str = "image") -> str | None:
    """An image fetched and inlined, None when it is not one to be had.

    Fetched here rather than left to WeasyPrint so the image travels inside
    the pdf instead of the pdf depending on a server still serving it. No
    image is worth failing a render for: what cannot be fetched, or comes
    back as something other than an image, is said once and left out.
    """
    try:
        response = http.get(url, timeout=30, headers={"Accept": "image/*,*/*;q=0.8"})
        response.raise_for_status()
    except Exception as error:
        log.warning(f"Cannot embed the {what} {url}: {error}")
        return None

    mime_type = response.headers.get("Content-Type", "").split(";")[0].strip()
    if not mime_type.startswith("image/"):
        log.warning(f"The {what} {url} is {mime_type or 'of unknown type'}")
        return None
    return f"data:{mime_type};base64,{b64encode(response.content).decode('ascii')}"


def embed_image(metadata: Metadata) -> str | None:
    """The feature image as a data uri, None when there is none to be had."""
    url = presence(metadata.image)
    return to_data_uri(str(url), "feature image") if url else None


#: What a PDF/A file has to say before it may carry prism:doi. The standard
#: predefines a handful of schemas - dc, xmp, pdf, pdfaid among them - and any
#: property outside those has to describe itself in the packet, or the file is
#: not PDF/A (ISO 19005-3 6.6.2.3.1). The namespace named here is the one
#: pikepdf writes the prism prefix as, so the description and the property it
#: describes agree.
PRISM_EXTENSION_SCHEMA = (
    '<rdf:Description rdf:about=""'
    ' xmlns:pdfaExtension="http://www.aiim.org/pdfa/ns/extension/"'
    ' xmlns:pdfaSchema="http://www.aiim.org/pdfa/ns/schema#"'
    ' xmlns:pdfaProperty="http://www.aiim.org/pdfa/ns/property#">'
    '<pdfaExtension:schemas><rdf:Bag><rdf:li rdf:parseType="Resource">'
    "<pdfaSchema:schema>PRISM metadata</pdfaSchema:schema>"
    "<pdfaSchema:namespaceURI>"
    "http://prismstandard.org/namespaces/basic/1.0/"
    "</pdfaSchema:namespaceURI>"
    "<pdfaSchema:prefix>prism</pdfaSchema:prefix>"
    '<pdfaSchema:property><rdf:Seq><rdf:li rdf:parseType="Resource">'
    "<pdfaProperty:name>doi</pdfaProperty:name>"
    "<pdfaProperty:valueType>Text</pdfaProperty:valueType>"
    "<pdfaProperty:category>external</pdfaProperty:category>"
    "<pdfaProperty:description>Digital Object Identifier</pdfaProperty:description>"
    "</rdf:li></rdf:Seq></pdfaSchema:property>"
    "</rdf:li></rdf:Bag></pdfaExtension:schemas></rdf:Description>"
)


def finish_pdf(pdf: bytes, metadata: Metadata) -> bytes:
    """Everything the rendition still needs after WeasyPrint has written it.

    The doi and the licence have no slot among the meta tags WeasyPrint
    reads, but each has a standard XMP property - dc:identifier, and dc:rights
    with the licence url as its xmpRights:WebStatement - so pikepdf writes
    them into the packet WeasyPrint produced. Writing them into that same
    packet, as opposed to appending a second rdf:RDF block, is what makes them
    visible to a reader that looks up properties by name. The doi is written a
    second time into the info dictionary, as /DOI, which is what a viewer
    shows as the document's properties.

    The images then lose their /Interpolate key, which WeasyPrint sets on
    every image it draws and PDF/A forbids (ISO 19005-3 6.2.8: present means
    false). It only ever hinted that a viewer may smooth the image when it is
    scaled up, so dropping it costs the rendition nothing and is what makes
    veraPDF pass the file.
    """
    import pikepdf

    identifier = presence(metadata.id)
    doi = doi_from_url(metadata.id)
    license_id = (metadata.license or {}).get("id", None)
    license_url = (metadata.license or {}).get("url", None)

    output = io.BytesIO()
    with pikepdf.open(io.BytesIO(pdf)) as document:
        # update_docinfo would copy these into the info dictionary, where a
        # pdf has no entry for either, and PDF/A wants the two kept in step.
        # set_pikepdf_as_editor would overwrite pdf:Producer, leaving it at
        # odds with the /Producer WeasyPrint wrote, and stamp the current
        # time as xmp:MetadataDate, which would make renditions of the same
        # post differ from each other.
        with document.open_metadata(
            update_docinfo=False, set_pikepdf_as_editor=False
        ) as xmp:
            if identifier:
                xmp["dc:identifier"] = identifier
            if license_id:
                xmp["dc:rights"] = license_id
            if license_url:
                xmp["xmpRights:WebStatement"] = license_url
            if doi:
                # the bare doi, which is what prism:doi holds and what the
                # tools that read a pdf for one expect to find there
                xmp["prism:doi"] = doi

        if doi:
            # prism is not a schema PDF/A knows, so the packet says what it is
            # before it says a word in it. Written here rather than through
            # the metadata api above, which has no way to express the nested
            # bag of structs a schema description is.
            packet = bytes(document.Root.Metadata.read_bytes())
            document.Root.Metadata.write(
                packet.replace(
                    b"</rdf:RDF>",
                    PRISM_EXTENSION_SCHEMA.encode("utf-8") + b"</rdf:RDF>",
                    1,
                )
            )

        # the doi goes in the info dictionary too: that is what a viewer's
        # document properties and `pdfinfo` read, and neither looks in the xmp
        # packet. PDF/A asks the entries it defines to agree with their xmp
        # counterparts, and /DOI is not one of them - veraPDF passes a
        # rendition carrying it.
        if identifier:
            document.docinfo[pikepdf.Name("/DOI")] = identifier

        for obj in document.objects:
            # every object, rather than every page's images: an image can also
            # sit inside a form xobject
            if (
                isinstance(obj, pikepdf.Stream)
                and obj.get("/Subtype", None) == pikepdf.Name.Image
                and "/Interpolate" in obj
            ):
                del obj["/Interpolate"]

        document.save(output, deterministic_id=True)
    return output.getvalue()


def to_pdf_attachment(metadata: Metadata, weasyprint):
    """The post content, embedded in the pdf as the source it was rendered from.

    PDF/A-3 is the variant that allows an arbitrary embedded file, and
    WeasyPrint gives it the /AFRelationship the standard asks for.
    """
    created = to_pdf_datetime(metadata.date_published)
    modified = to_pdf_datetime(metadata.date_updated) or created
    return weasyprint.Attachment(
        string=metadata.content,
        name=f"{Path(pdf_filename(metadata)).stem}.html",
        description="Post content as html (rs:content_html)",
        relationship="Source",
        created=created,
        modified=modified,
    )


def to_pdf_datetime(date: str | None) -> datetime | None:
    """An iso date as the datetime WeasyPrint stamps an attachment with"""
    if not date:
        return None
    try:
        return datetime.fromisoformat(get_iso8601_date(date))
    except (ValueError, TypeError):
        return None


def to_pdf_video(url: str) -> tuple[str, str] | None:
    """The page a video embed points at, and the poster frame to show for it.

    A pdf has no browsing context, so WeasyPrint draws nothing at all for an
    iframe: a post that embeds a video loses it without trace. What it can
    show is the frame the platform publishes as the video's thumbnail, over a
    link to the video itself. YouTube serves one at a known address; Vimeo
    does not, so a vimeo embed becomes the link alone.
    """
    match = re.search(
        r"(?:youtube(?:-nocookie)?\.com/(?:embed|v)/|youtu\.be/)([\w-]{11})", url
    )
    if match:
        video = match.group(1)
        return (
            f"https://youtu.be/{video}",
            f"https://img.youtube.com/vi/{video}/hqdefault.jpg",
        )
    match = re.search(r"player\.vimeo\.com/video/(\d+)", url)
    if match:
        return f"https://vimeo.com/{match.group(1)}", ""
    return None


def to_pdf_videos(soup: BeautifulSoup, label: str) -> bool:
    """Replace each video embed with its poster frame, linked to the video."""
    replaced = False
    for iframe in soup.find_all("iframe"):
        video = to_pdf_video(iframe.get("src", None) or "")
        if video is None:
            continue
        page, poster = video
        data_uri = to_data_uri(poster, "video poster") if poster else None

        figure = soup.new_tag("figure")
        figure["class"] = "video"
        if data_uri:
            link = soup.new_tag("a", href=page)
            image = soup.new_tag("img", src=data_uri, alt=label)
            link.append(image)
            figure.append(link)
        caption = soup.new_tag("figcaption")
        caption_link = soup.new_tag("a", href=page)
        caption_link.string = page
        caption.append(caption_link)
        figure.append(caption)
        iframe.replace_with(figure)
        replaced = True
    return replaced


def find_reference_heading(soup: BeautifulSoup):
    """The heading a post writes over the works it cites, if it writes one.

    What marks it is what it says, in any of the languages a rendition is
    written in - there is no markup that says a list is a reference list.
    """
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        if heading.get_text(" ", strip=True).strip(":. ").casefold() in (
            REFERENCE_HEADINGS
        ):
            return heading
    return None


def to_pdf_content(content: str | None, language: str) -> str:
    """The post content, with an alt description on every image, a poster
    frame where a video was embedded, and its reference list marked."""
    if not content:
        return ""

    soup = BeautifulSoup(content, "html.parser")
    label = PDF_TITLES["image"].get(language, PDF_TITLES["image"]["en"])
    described = to_pdf_videos(
        soup, PDF_TITLES["video"].get(language, PDF_TITLES["video"]["en"])
    )
    heading = find_reference_heading(soup)
    if heading:
        # the works cited begin a page, as they do where the rendition itself
        # writes them: the stylesheet breaks before this class
        heading["class"] = [*(heading.get("class") or []), "references"]
        described = True
    for image in soup.find_all("img"):
        if (image.get("alt") or "").strip():
            continue
        figure = image.find_parent("figure")
        caption = figure.find("figcaption") if figure else None
        image["alt"] = (
            (caption.get_text(" ", strip=True) if caption else "")
            or (image.get("title") or "").strip()
            or label
        )
        described = True
    return str(soup) if described else content


def to_pdf_reference(reference: dict) -> str | None:
    """One entry of the reference list: its citation text, and its identifier.

    The text is the formatted citation the record carries - `reference` in the
    current schema, `unstructured` in the one before it - and the identifier
    follows it as a link, unless the citation already spells it out.
    """
    if not isinstance(reference, dict):
        return None
    text = to_pdf_markup(
        reference.get("reference", None) or reference.get("unstructured", None)
    ).strip()
    identifier = reference.get("id", None)
    if not text and not identifier:
        return None
    link = ""
    if identifier and identifier not in text:
        link = f'<a href="{escape(identifier)}">{escape(identifier)}</a>'
    return f"<li>{' '.join(part for part in (text, link) if part)}</li>"


def has_reference_list(content: str | None) -> bool:
    """Whether the post prints its own list of the works it cites.

    A record's references are often read back out of the post that lists them,
    so the two say the same thing; where the post has the list, the rendition
    prints that one rather than the same works twice. What marks it is the
    heading over it, in any of the languages a rendition is written in.
    """
    if not content:
        return False
    return find_reference_heading(BeautifulSoup(content, "html.parser")) is not None


def to_pdf_references(metadata: Metadata, language: str) -> str:
    """The works the record cites, as a page of their own.

    A rendition closes the way an article does, with the reference list after
    the text; the stylesheet gives the section `break-before`, so it is the
    last page. A record that cites nothing gets no such page, and neither does
    one whose post already prints the list.
    """
    entries = [
        entry
        for entry in (to_pdf_reference(r) for r in wrap(metadata.references))
        if entry
    ]
    if not entries or has_reference_list(metadata.content):
        return ""
    label = PDF_TITLES["references"].get(language, PDF_TITLES["references"]["en"])
    return (
        f'<section class="references"><h2>{label}</h2>'
        f"<ol>{''.join(entries)}</ol></section>"
    )


def to_pdf_running_matter(metadata: Metadata) -> str:
    """What every page but the title page carries, at its head and its foot.

    A page on its own has to say where it came from: the head names what the
    work came out in, in bold, and what it is called, and the foot carries the
    record's own address as a link the reader can follow. Both are taken out
    of the flow by `position: running()`, so they are written once here and
    laid out by the page.
    """
    title = to_pdf_markup(metadata.title)
    container = to_pdf_markup((metadata.container or {}).get("title", None))
    head = f"<b>{container}</b> • {title}" if container else title
    matter = f'<div class="running-head">{head}</div>'
    if metadata.id:
        matter += (
            f'<div class="running-foot"><a href="{escape(metadata.id)}">'
            f"{escape(metadata.id)}</a></div>"
        )
    return matter


def to_pdf_html(metadata: Metadata) -> str:
    """Build the html document the pdf is rendered from.

    The post content is the body, preceded by the front matter that the
    stylesheet styles by class. The licence carries `break-after: always`, so the
    front matter is a title page.
    """
    language = get_language(metadata.language, format="alpha_2") or "en"
    authors = to_pdf_authors(metadata)

    front_matter = [
        f"<h1>{to_pdf_markup(metadata.title)}</h1>",
        to_pdf_running_matter(metadata),
        to_pdf_byline(authors),
    ]
    published = to_pdf_published(metadata, language)
    if published:
        # already markup: the container it names is set in italics and linked
        front_matter.append(f'<div class="date">{published}</div>')
    if metadata.id:
        front_matter.append(
            f'<p class="identifier"><a href="{escape(metadata.id)}">'
            f"{escape(metadata.id)}</a></p>"
        )
    if presence(metadata.description):
        label = PDF_TITLES["abstract"].get(language, PDF_TITLES["abstract"]["en"])
        # the text follows the heading directly, as in the rights block: a <p>
        # would add its own margin on top of the heading's padding
        front_matter.append(
            f'<div class="abstract"><h4>{label}</h4>'
            f"{to_pdf_markup(metadata.description)}</div>"
        )
    keywords = to_pdf_keywords(metadata)
    if keywords:
        label = PDF_TITLES["keywords"].get(language, PDF_TITLES["keywords"]["en"])
        front_matter.append(
            f'<div class="keywords"><h4>{label}</h4>{escape(", ".join(keywords))}</div>'
        )
    image = embed_image(metadata)
    if image:
        front_matter.append(
            f'<img class="feature-image" alt="Feature image" src="{image}" />'
        )
    citation = to_pdf_citation(metadata, language)
    if citation:
        label = PDF_TITLES["citation"].get(language, PDF_TITLES["citation"]["en"])
        # not `citation`: the rogue-scholar stylesheet hides a post's own
        # citation widget by that class
        front_matter.append(
            f'<div class="recommended-citation"><h4>{label}</h4>{citation}</div>'
        )
    rights = to_pdf_rights(metadata, [a["name"] for a in authors], language)
    if rights:
        label = PDF_TITLES["copyright"].get(language, PDF_TITLES["copyright"]["en"])
        front_matter.append(f'<div class="rights"><h4>{label}</h4>{rights}</div>')

    body = (
        f'<section class="front-matter">{"".join(front_matter)}</section>'
        f"{to_pdf_content(metadata.content, language)}"
        f"{to_pdf_references(metadata, language)}"
    )
    head = [
        "<meta charset='utf-8'>",
        f"<title>{escape(to_pdf_text(metadata.title))}</title>",
        *to_pdf_metadata(metadata, authors),
    ]
    return (
        f"<html lang='{escape(language)}'><head>{''.join(head)}</head>"
        # the head keeps its emoji, the page does not: see strip_emoji
        f"<body>{strip_emoji(body)}</body></html>"
    )


#: Where a mac keeps the libraries `brew install pango` puts there, arm64
#: first. dyld searches neither unless DYLD_FALLBACK_LIBRARY_PATH says so.
HOMEBREW_LIB_PATHS = ("/opt/homebrew/lib", "/usr/local/lib")
#: What dyld falls back to when the variable is unset, which setting it drops.
DYLD_DEFAULT_LIB_PATHS = ("~/lib", "/usr/local/lib", "/lib", "/usr/lib")


def find_pango() -> None:
    """Let dyld find a homebrew pango, on the mac where one is installed.

    WeasyPrint dlopens pango, cairo and glib by leaf name, and on macOS dyld
    looks for those only in DYLD_FALLBACK_LIBRARY_PATH - which does not list
    the homebrew directories, and which SIP strips from the environment of a
    protected binary, so exporting it in a shell profile does not reliably
    survive either. Setting it here does, because ctypes reads it when the
    library is actually dlopened.

    Nothing is set on any other platform, where the loader finds the libraries
    on its own, and an existing value is added to rather than replaced.
    """
    if sys.platform != "darwin":
        return
    paths = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "").split(os.pathsep)
    paths += [p for p in HOMEBREW_LIB_PATHS if os.path.isdir(p)]
    paths += list(DYLD_DEFAULT_LIB_PATHS)
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = os.pathsep.join(
        dict.fromkeys(p for p in paths if p)
    )


def load_weasyprint():
    """Import WeasyPrint, None when its native stack is missing.

    Imported here rather than at module level because WeasyPrint binds pango,
    cairo and glib through cffi at import time: on a machine without those
    system libraries the import raises OSError rather than ImportError, and
    only the pdf path should pay for that.
    """
    find_pango()
    try:
        import weasyprint

        return weasyprint
    except (ImportError, OSError) as error:
        log.error(f"Cannot render pdf, weasyprint needs the pango libraries: {error}")
        return None


def write_pdf(metadata: Metadata, file: str) -> bytes:
    """Write the pdf rendition of a record to a file, and return the bytes.

    A pdf is a rendering of a record rather than a metadata format, so it is
    not one of the things `Metadata.write` produces: a caller names a file and
    gets one. A record that carries the html of a post - one read through the
    InvenioRDM reader, today - is rendered whole; any other record gets its
    title page, which is a record of the metadata rather than of the work.

    Raises ValueError where the rendition cannot be made at all, since a
    caller that named a file expects one to be there afterwards.
    """
    pdf = write_pdf_rendition(metadata, file=file)
    if pdf is None:
        raise ValueError(
            "Could not render the pdf. WeasyPrint needs the pango libraries, "
            "and Python 3.10 or newer; the log says which of the two it was."
        )
    return pdf


def pdf_filename(metadata: Metadata, record: dict | None = None) -> str:
    """Name the pdf after the doi of the record or metadata it is attached to.

    Replaces the slash in the doi with a dash, so the filename is valid on every
    filesystem. Falls back to "content.pdf" when there is no doi.
    """
    doi = doi_from_url(dig(record, "doi")) or doi_from_url(metadata.id)
    return f"{doi.replace('/', '-')}.pdf" if doi else "content.pdf"


@lru_cache(maxsize=1)
def pdf_stylesheet() -> tuple:
    """The shipped stylesheet and the font configuration it registers into.

    Parsed once per process: it reads and registers the six bundled font
    faces, which is the expensive part of rendering a post. The same font
    configuration has to reach `write_pdf`, otherwise the @font-face rules are
    dropped and the text falls back to WeasyPrint's default font.
    """
    import weasyprint
    from weasyprint.text.fonts import FontConfiguration

    font_config = FontConfiguration()
    css = weasyprint.CSS(
        filename=str(PDF_RESOURCES / "style.css"), font_config=font_config
    )
    # WeasyPrint's font configuration calls back into its own module when it is
    # finalized, which fails once the interpreter has torn those modules down.
    # Dropping the cache at exit finalizes it while that is still safe.
    atexit.register(pdf_stylesheet.cache_clear)
    return css, font_config


def write_pdf_rendition(
    metadata: Metadata, url_fetcher=None, file: str | None = None, **options
) -> bytes | None:
    """Render a record as a tagged pdf, None when it cannot be rendered at all.

    A record that carries the html of a post - which today is one read through
    the InvenioRDM reader - is rendered whole: the title page, then the post.
    Every other record has its title page and stops there, which is a record
    of the metadata rather than of the work, and is what any input can give.

    ``url_fetcher`` is handed to WeasyPrint for the images the post links, and
    any further ``options`` go to ``write_pdf`` - among them ``pdf_variant``,
    which defaults to PDF/A-3a.

    ``file`` also writes the rendition there, through `write_output`, which
    takes the compression suffixes with it: ``post.pdf.gz`` and ``post.pdf.zst``
    are written compressed. It refuses to overwrite, as every other output
    format does. The bytes are returned either way, since what a caller does
    with a rendition is usually to send it somewhere rather than keep it.
    """
    weasyprint = load_weasyprint()
    if weasyprint is None:
        return None

    css, font_config = pdf_stylesheet()
    # WeasyPrint picks its own fetcher when none is given; naming its default
    # explicitly would go through an api it deprecated in 69.
    fetcher = {"url_fetcher": url_fetcher} if url_fetcher is not None else {}
    options.setdefault("pdf_variant", PDF_VARIANT)
    # nothing to attach when there is no post to attach: the html the pdf was
    # rendered from is the only file it carries
    if presence(metadata.content):
        options.setdefault("attachments", [to_pdf_attachment(metadata, weasyprint)])
    document = weasyprint.HTML(
        string=to_pdf_html(metadata), base_url=str(PDF_RESOURCES), **fetcher
    ).render(stylesheets=[css], font_config=font_config)
    pdf = finish_pdf(document.write_pdf(**options), metadata)
    if file:
        write_output(file, pdf, [".pdf"])
    return pdf


def read_pdf_metadata(pdf: bytes) -> dict:
    """Read a rendition's own metadata back out of the pdf.

    Reads the XMP packet, which is where PDF/A keeps the metadata the
    InvenioRDM writer put there when it rendered the post, the two markers
    that say the pdf is tagged - a structure tree, and a catalog declaring it
    marked - and the names of the embedded files. Anything absent from the pdf
    is absent from the result.

    pikepdf is imported here rather than at module level: it pulls in libqpdf,
    which costs more to import than the rest of this module put together, and
    only the pdf path should pay for it.
    """
    import pikepdf

    metadata = {}
    with pikepdf.open(io.BytesIO(pdf)) as document:
        catalog = document.Root
        metadata["tagged"] = (
            bool(catalog.get("/MarkInfo", {}).get("/Marked", False))
            and "/StructTreeRoot" in catalog
        )
        if "/Lang" in catalog:
            metadata["language"] = str(catalog.Lang)
        attachments = {
            name: document.attachments[name].get_file().mime_type
            for name in document.attachments
        }
        if attachments:
            metadata["attachments"] = attachments

        xmp = document.open_metadata()
        for key, property_ in (
            ("id", "dc:identifier"),
            ("title", "dc:title"),
            ("authors", "dc:creator"),
            ("description", "dc:description"),
            ("license", "dc:rights"),
            ("license_url", "xmpRights:WebStatement"),
            ("keywords", "pdf:Keywords"),
            ("generator", "xmp:CreatorTool"),
            ("created", "xmp:CreateDate"),
            ("modified", "xmp:ModifyDate"),
            ("producer", "pdf:Producer"),
        ):
            value = xmp.get(property_, None)
            if value:
                metadata[key] = value
        # a single string of comma-separated keywords in the pdf, a list here
        if metadata.get("keywords", None):
            metadata["keywords"] = [k.strip() for k in metadata["keywords"].split(",")]
        part = xmp.get("pdfaid:part", None)
        if part:
            level = xmp.get("pdfaid:conformance", "")
            metadata["variant"] = f"PDF/A-{part}{level.lower()}"
    return metadata


def read_pdf_attachment(pdf: bytes, name: str | None = None) -> bytes | None:
    """Read an embedded file back out of the pdf, the first one by default"""
    import pikepdf

    with pikepdf.open(io.BytesIO(pdf)) as document:
        names = list(document.attachments)
        if name is None:
            name = names[0] if names else None
        if name is None or name not in names:
            return None
        return document.attachments[name].get_file().read_bytes()
