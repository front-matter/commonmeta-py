from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from ..utils import compact, pages_as_string, get_month_from_date, get_date
from ..author_utils import authors_as_string
from ..doi_utils import doi_from_url


def write_bibtex(metadata):
    """Write bibtex"""
    container = metadata.container or {}
    print(container)
    db = BibDatabase()
    db.entries = [
        compact({'ID': metadata.id,
                 'ENTRYTYPE': 'article',
                 'abstract': metadata.descriptions[0].get('description', None),
                 'author': authors_as_string(metadata.creators),
                 'copyright': str(metadata.rights_list[0].get('rightsURI', None)),
                 'doi': doi_from_url(metadata.id),
                 'issn': metadata.issn,
                 'issue': container.get('issue', None),
                 'journal': container.get('title', None),
                 'language': metadata.language,
                 'month': get_month_from_date(metadata.dates[0].get('date', None)),
                 'pages': pages_as_string(container),
                 'title': metadata.titles[0].get('title', None),
                 'url': metadata.url,
                 'urldate': get_date(metadata.dates, date_only=True),
                 'year': metadata.publication_year})]
    writer = BibTexWriter()
    writer.indent = '    '
    bibtex_str = writer.write(db)
    return bibtex_str
