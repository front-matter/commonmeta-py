"""Citation writer for commonmeta-py"""
import json
import re
from pydash import py_
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON
from citeproc_styles import get_style_filepath


def write_citation(metadata):
    """Write citation"""

    def _clean_result(text):
        """Remove double spaces, punctuation."""
        text = re.sub(r"\s\s+", " ", text)
        text = re.sub(r"\.\.+", ".", text)
        return text

    csl = json.loads(metadata.csl())

    # Remove keys that are not supported by citeproc-py.
    csl = py_.omit(csl, "copyright", "categories")

    # Process the JSON data to generate a citeproc-py BibliographySource.
    source = CiteProcJSON([csl])
    style_path = get_style_filepath(metadata.style)
    style = CitationStylesStyle(style_path, locale=metadata.locale)
    bib = CitationStylesBibliography(style, source, formatter.html)
    citation = Citation([CitationItem(metadata.id)])

    # workaround for the issue with the vancouver style and de locale
    try:
        bib.register(citation)
        return _clean_result(str(bib.bibliography()[0]))
    except Exception as e:
        print(e)
        return f"Error: citation not available for style {metadata.style} and locale {metadata.locale}."
