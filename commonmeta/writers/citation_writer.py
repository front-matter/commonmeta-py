"""Citation writer for commonmeta-py"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import orjson as json
from citeproc import (
    Citation,
    CitationItem,
    CitationStylesBibliography,
    CitationStylesStyle,
    formatter,
)
from citeproc.source.json import CiteProcJSON
from citeproc_styles import get_style_filepath

from ..base_utils import omit

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


def write_citation(metadata: Metadata) -> bytes | None:
    """Write citation"""
    if metadata is None:
        return None

    # Process the JSON data to generate a citeproc-py BibliographySource.
    item = write_citation_item(metadata)
    if item is None:
        return f"Error: citation not available for {metadata.id}.".encode("utf-8")

    style_path = get_style_filepath(metadata.style)
    style = CitationStylesStyle(style_path, locale=metadata.locale)
    bib = CitationStylesBibliography(style, item, formatter.html)
    citation = Citation([CitationItem(metadata.id)])

    # workaround for the issue with the vancouver style and de locale
    try:
        bib.register(citation)
        return _clean_result(str(bib.bibliography()[0])).encode("utf-8")
    except Exception as e:
        print(e)
        return f"Error: citation not available for style {metadata.style} and locale {metadata.locale}.".encode(
            "utf-8"
        )


def write_citation_item(metadata: Metadata) -> CiteProcJSON | None:
    """Write citation item"""
    if metadata.write_errors is not None:
        return None
    csl_output = metadata.write(to="csl")
    if csl_output is None:
        return None
    csl = json.loads(csl_output)

    # Remove keys that are not supported by citeproc-py.
    csl = omit(csl, "copyright", "categories")
    return CiteProcJSON([csl])


def write_citation_list(metalist: MetadataList | None, **kwargs) -> bytes | None:
    """Write citation list"""
    if metalist is None:
        return None

    style_name = kwargs.get("style", "apa")
    locale = kwargs.get("locale", "en-US")
    style_path = get_style_filepath(style_name)
    style = CitationStylesStyle(style_path, locale=locale)

    def format_citation(index: int, item: CiteProcJSON) -> str:
        bib = CitationStylesBibliography(style, item, formatter.html)
        _id = metalist.items[index].id
        citation = Citation([CitationItem(_id)])
        bib.register(citation)
        return _clean_result(str(bib.bibliography()[0]))

    citations = [write_citation_item(item) for item in metalist.items]
    # Filter out None values
    valid_citations = [c for c in citations if c is not None]
    bibliographies = [
        format_citation(index, item) for index, item in enumerate(valid_citations)
    ]
    return "\n\n".join(bibliographies).encode("utf-8")


def _clean_result(text: str) -> str:
    """Remove double spaces, punctuation."""
    text = re.sub(r"\s\s+", " ", text)
    text = re.sub(r"\.\. ", ". ", text)
    return text
