import json
from citeproc import (Citation, CitationItem, CitationStylesBibliography,
                      CitationStylesStyle, formatter)
from citeproc.source.json import CiteProcJSON
from citeproc_styles import get_style_filepath

from ..utils import (compact, pages_as_string, get_date, get_date_parts, wrap,
     to_citeproc, normalize_doi, get_date, parse_attributes,
     presence)
from ..author_utils import authors_as_string
from ..doi_utils import doi_from_url, normalize_doi


def write_citeproc(metadata):
    """Write citeproc"""
    if len(wrap(metadata.creators)) == 1 and wrap(metadata.creators)[0].get('name', None) == ':(unav)':
        author = None
    else:
        author = to_citeproc(metadata.creators)

    if metadata.types.get('resourceTypeGeneral', None) == 'Software' and metadata.version_info is not None:
        type = 'book'
    else:
        type = metadata.types.get('citeproc', 'article')

    dictionary = compact({
      'type': type,
      'id': metadata.id,
      'DOI': doi_from_url(metadata.id),
      'URL': metadata.url,
      'categories': presence(parse_attributes(wrap(metadata.subjects), content='subject', first=False)),
      'language': metadata.language,
      'author': author,
      'contributor': to_citeproc(metadata.contributors),
      'issued': get_date_parts(get_date(metadata.dates, 'Issued') or str(metadata.publication_year)),
      'submitted': get_date(metadata.dates, 'Submitted'),
      'abstract': parse_attributes(metadata.descriptions, content='description', first=True),
      'container-title': metadata.container.get('title', None),
      'volume': metadata.container.get('volume', None),
      'issue': metadata.container.get('issue', None),
      'page': pages_as_string(metadata.container),
      'publisher': metadata.publisher,
      'title': parse_attributes(metadata.titles, content='title', first=True),
      'copyright': metadata.rights_list[0].get('rights', None) if metadata.rights_list else None,
      'version': metadata.version_info
    })
    return json.dumps(dictionary, indent = 4)
