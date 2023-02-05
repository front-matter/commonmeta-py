import requests
from pydash import py_

from ..utils import (
    crossref_api_url,
    get_date_from_date_parts,
    dict_to_spdx, normalize_cc_url,
    wrap, compact, from_citeproc,
    presence, sanitize,
    CR_TO_BIB_TRANSLATIONS,
    CR_TO_SO_TRANSLATIONS,
    CR_TO_CP_TRANSLATIONS,
    CR_TO_RIS_TRANSLATIONS,
    CR_TO_DC_TRANSLATIONS
)
from ..author_utils import get_authors
from ..doi_utils import doi_as_url, get_doi_ra

def get_crossref_json(id=None, **kwargs):
    """get_crossref_json"""
    if id is None:
        return { 'string': None, 'state': 'not_found' } 

    url = crossref_api_url(id)
    response = requests.get(url, kwargs)
    if response.status_code != 200:
        return { 'string': None, 'state': 'not_found' }
    return response.json().get('message', {})

def read_crossref_json(string=None, **kwargs):
    """read_crossref_json"""
    if string is None:
        return { 'meta': None, 'state': 'not_found' }
    meta = string

    id = doi_as_url(meta.get('DOI', None))
    resource_type = meta.get('type', {}).title().replace("-", "")
    types = {
        'resourceTypeGeneral': CR_TO_DC_TRANSLATIONS[resource_type] or 'Text',
        'resourceType': resource_type,
        'schemaOrg': CR_TO_SO_TRANSLATIONS.get(resource_type, None) or 'CreativeWork',
        'citeproc': CR_TO_CP_TRANSLATIONS.get(resource_type, None) or 'article-journal',
        'bibtex': CR_TO_BIB_TRANSLATIONS.get(resource_type, None) or 'misc',
        'ris': CR_TO_RIS_TRANSLATIONS.get(resource_type, None) or 'GEN',
    }
    if meta.get('author', None):
        creators = get_authors(from_citeproc(wrap(meta.get('author'))))
    else:
        creators = [{ 'nameType': 'Organizational', 'name': ':(unav)' }]
    editors = []
    for editor in wrap(meta.get('editor', None)):
        editor['ContributorType'] = 'Editor'
        editors.append(editor)
    contributors = presence(get_authors(from_citeproc(editors)))

    url = py_.get(meta, 'resource.primary.URL', None)
    title = meta.get('title', None) or meta.get('original-title', None)
    if presence(title) is not None:
        titles = [{'title': sanitize(title)}]
    else:
        titles = []
    publisher = meta.get('publisher', None)

    issued_date = get_date_from_date_parts(meta.get('issued', None))
    issued_date = None if issued_date == 'None' else issued_date
    created_date = get_date_from_date_parts(meta.get('created', None))
    deposited_date = get_date_from_date_parts(meta.get('deposited', None))
    indexed_date = get_date_from_date_parts(meta.get('indexed', None))
    published_date = issued_date or created_date 
    updated_date = deposited_date or indexed_date
    dates = [{ 'date': published_date, 'dateType': 'Issued' }]
    if updated_date is not None:
        dates.append({ 'date': updated_date, 'dateType': 'Updated' })
    publication_year = published_date[0:4] if published_date else None
    date_registered = (get_date_from_date_parts(meta.get('registered', {})) 
        or get_date_from_date_parts(meta.get('created', None)))
      
    license = meta.get('license', None)
    if license is not None:
        license = normalize_cc_url(license[0].get('URL', None))
        rights_list = [dict_to_spdx({ 'rightsURI': license })] if license else None
    else:
        rights_list = None

    issns = meta.get('issn-type', None)
    if issns is not None:
        issn = next((item for item in issns if item["type"] == "electronic"), None) or next((item for item in issns if item["type"] == "print"), None) or {}
        issn = issn['value'] if issn else None
    else:
        issn = None
    if issn is not None:
        related_identifiers = [compact({'relationType': 'IsPartOf',
            'relatedIdentifierType': 'ISSN',
            'resourceTypeGeneral': 'Collection',
            'relatedIdentifier': issn })]
    else:
        related_identifiers = []
    for reference in wrap(meta.get('reference', [])):
        doi = reference.get('DOI', None)
        if doi is None:
            continue # skip references without a DOI
        ref = {'relationType': 'References',
            'relatedIdentifierType': 'DOI',
            'relatedIdentifier': doi.lower() }
        related_identifiers.append(ref)
 
    if resource_type == 'JournalArticle':
        container_type = 'Journal'
    elif resource_type == 'JournalIssue':
        container_type = 'Journal'
    elif resource_type ==  'BookChapter':
        container_type = 'Book'
    elif resource_type ==  'Monograph':
        container_type = 'BookSeries'
    else:
        container_type = 'Periodical'

    if meta.get('page', None):
        pages = meta.get('page', None).split('-')
        first_page = pages[0]
        last_page = pages[1] if len(pages) > 1 else None
    else:
        first_page = None
        last_page = None

    container_titles = meta.get('container-title', [])
    container_title = container_titles[0] if len(container_titles) > 0 else None
    if container_title is not None:
        container = compact({ 
            'type': container_type,
            'title': container_title,
            'identifier': issn,
            'identifierType': 'ISSN' if issn else None,
            'volume': meta.get('volume', None),
            'issue': meta.get('issue', None),
            'firstPage': first_page,
            'lastPage': last_page})
    else:
        container = None

    if issn:
        related_identifiers = [{ 'relationType': 'IsPartOf',
            'relatedIdentifierType': 'ISSN',
            'resourceTypeGeneral': 'Collection',
            'relatedIdentifier': issn }]
    else:
        related_identifiers = []
    references = meta.get('reference', [])
    for ref in references:
        doi = ref.get('DOI', None)
        if doi:
            related_identifiers.append({ 'relationType': 'References',
                'relatedIdentifierType': 'DOI',
                'relatedIdentifier': doi.lower() })

    funding_references = []
    for funding in wrap(meta.get('funder', [])):
        funding_reference = compact({
            'funderName': funding.get('name', None),
            'funderIdentifier': doi_as_url(funding['DOI']) if funding.get('DOI', None) is not None else None,
            'funderIdentifierType': 'Crossref Funder ID' if funding.get('DOI', '').startswith('10.13039') else None
        })
        if funding.get('name', None) is not None and funding.get('award', None) is not None:
            for award in wrap(funding['award']):
                fund_ref = funding_reference.copy()
                fund_ref['awardNumber'] = award
                funding_references.append(fund_ref)
    funding_references = funding_references or None

    description = meta.get('abstract', None)
    if description is not None:
        descriptions = [{'description': sanitize(description),
            'descriptionType': 'Abstract' }]
    else:
        descriptions = None

    subjects = []
    for subject in wrap(meta.get('subject', [])):
        subjects.append({ 'subject': subject })
    subjects = subjects or None

    return {
        'id': id,
        'url': url,
        'types': types,
        'creators': creators,
        'contributors': contributors,
        'titles': presence(titles),
        'dates': dates,
        'publication_year': publication_year,
        'date_registered': date_registered,
        'publisher': publisher,
        'rights_list': rights_list,
        'issn': issn,
        'container': container,
        'related_identifiers': related_identifiers,
        'funding_references': funding_references,
        'descriptions': descriptions,
        'subjects': subjects,
        'language': meta.get('language', None),
        'version_info': meta.get('version', None),
        'agency': get_doi_ra(id)
    }
