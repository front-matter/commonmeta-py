"""Citation writer for commonmeta-py"""
import orjson as json
import re
from pydash import py_
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON
from citeproc_styles import get_style_filepath


def write_citation(metadata):
    """Write citation"""

    # Process the JSON data to generate a citeproc-py BibliographySource.
    item = write_citation_item(metadata)
    style_path = get_style_filepath(metadata.style)
    style = CitationStylesStyle(style_path, locale=metadata.locale)
    bib = CitationStylesBibliography(style, item, formatter.html)
    citation = Citation([CitationItem(metadata.id)])

    # workaround for the issue with the vancouver style and de locale
    try:
        bib.register(citation)
        return _clean_result(str(bib.bibliography()[0]))
    except Exception as e:
        print(e)
        return f"Error: citation not available for style {metadata.style} and locale {metadata.locale}."


def write_citation_item(metadata):
    """Write citation item"""
    if metadata.write_errors is not None:
        return None
    csl = json.loads(metadata.write(to="csl"))

    # Remove keys that are not supported by citeproc-py.
    csl = py_.omit(csl, "copyright", "categories")
    return CiteProcJSON([csl])


def write_citation_list(metalist, **kwargs):
    """Write citation list"""
    if metalist is None:
        return None

    style = kwargs.get("style", "apa")
    locale = kwargs.get("locale", "en-US")
    style_path = get_style_filepath(style)
    style = CitationStylesStyle(style_path, locale=locale)  #

    def format_citation(index, item):
        bib = CitationStylesBibliography(style, item, formatter.html)
        _id = metalist.items[index].id
        citation = Citation([CitationItem(_id)])
        bib.register(citation)
        return _clean_result(str(bib.bibliography()[0]))

    citations = [write_citation_item(item) for item in metalist.items]
    bibliographies = [
        format_citation(index, item) for index, item in enumerate(citations)
    ]
    return "\n\n".join(bibliographies)


def _clean_result(text):
    """Remove double spaces, punctuation."""
    text = re.sub(r"\s\s+", " ", text)
    text = re.sub(r"\.\.+", ".", text)
    return text
