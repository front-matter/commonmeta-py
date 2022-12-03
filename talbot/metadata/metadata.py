from talbot import Crossref
from ..utils import (
    get_date_from_date_parts,
    dict_to_spdx, normalize_cc_url,
    wrap, unwrap, compact, from_citeproc,
    presence,
    CR_TO_BIB_TRANSLATIONS,
    CR_TO_SO_TRANSLATIONS,
    CR_TO_CP_TRANSLATIONS,
    CR_TO_RIS_TRANSLATIONS,
    CR_TO_DC_TRANSLATIONS
)
from ..author_utils import get_authors
from ..doi_utils import doi_as_url, get_doi_ra

class Metadata:
    def __init__(self, input):
        
        cr = Crossref() #(mailto: 'info@front-matter.io')
        res = cr.works(ids=input)

        self.id = doi_as_url(res.get('message', {}).get('DOI', None))
        self.resource_type = res.get('message', {}).get('type', {}).title().replace("-", "")
        self.types = {
            'resourceTypeGeneral': CR_TO_DC_TRANSLATIONS[self.resource_type] or 'Text',
            'resourceType': self.resource_type,
            'schemaOrg': CR_TO_SO_TRANSLATIONS.get(self.resource_type, None) or 'CreativeWork',
            'citeproc': CR_TO_CP_TRANSLATIONS.get(self.resource_type, None) or 'article-journal',
            'bibtex': CR_TO_BIB_TRANSLATIONS.get(self.resource_type, None) or 'misc',
            'ris': CR_TO_RIS_TRANSLATIONS.get(self.resource_type, None) or 'GEN',
        }
        if res.get('message', {}).get('author', None):
            self.creators = get_authors(from_citeproc(wrap(res.get('message', {}).get('author'))))
        else:
            self.creators = [{ 'nameType': 'Organizational', 'name': ':(unav)' }]
        self.editors = []
        for editor in wrap(res.get('message', {}).get('editor', None)):
            editor['ContributorType'] = 'Editor'
            self.editors.append(editor)
        self.contributors = presence(get_authors(from_citeproc(self.editors)))

        self.url = res.get('message', {})['resource'].get('primary', {}).get('URL', None)
        self.titles = (res.get('message', {}).get('title', None) or
            res.get('message', {}).get('original-title', None))
        self.publisher = res.get('message', {}).get('publisher', None)

        issued_date = get_date_from_date_parts(res.get('message', {}).get('issued', None))
        issued_date = None if issued_date == 'None' else issued_date
        created_date = get_date_from_date_parts(res.get('message', {}).get('created', None))
        deposited_date = get_date_from_date_parts(res.get('message', {}).get('deposited', None))
        indexed_date = get_date_from_date_parts(res.get('message', {}).get('indexed', None))
        self.published_date = issued_date or created_date 
        self.updated_date = deposited_date or indexed_date
        self.dates = [{ 'date': self.published_date, 'dateType': 'Issued' }]
        self.dates.append({ 'date': self.updated_date, 'dateType': 'Updated' }) if self.updated_date else None
        self.publication_year = self.published_date[0:4] if self.published_date else None
        self.date_registered = get_date_from_date_parts(res.get('message', {}).get('registered', {})) or get_date_from_date_parts(res.get('message', {}).get('created', None))
        
        license = res.get('message', {}).get('license', None)
        if license is not None:
            license = normalize_cc_url(license[0].get('URL', None))
            self.rights_list = [dict_to_spdx({ 'rightsURI': license })] if license else None
        else:
            self.rights_list = None

        issns = res.get('message', {}).get('issn-type', None)
        if issns is not None:
            self.issn = next((item for item in issns if item["type"] == "electronic"), None) or next((item for item in issns if item["type"] == "print"), None) or {}
            self.issn = self.issn['value'] if self.issn else None
        else:
            self.issn = None
        if self.issn is not None:
            self.related_identifiers = [compact({'relationType': 'IsPartOf',
                'relatedIdentifierType': 'ISSN',
                'resourceTypeGeneral': 'Collection',
                'relatedIdentifier': self.issn })]
        else:
            self.related_identifiers = []
        for reference in wrap(res.get('message', {}).get('reference', [])):
            doi = reference.get('DOI', None)
            if doi is None:
                continue # skip references without a DOI
            r = {'relationType': 'References',
                'relatedIdentifierType': 'DOI',
                'relatedIdentifier': doi.lower() }
            self.related_identifiers.append(r)
    
        if self.resource_type == 'JournalArticle':
            container_type = 'Journal'
        elif self.resource_type == 'JournalIssue':
            container_type = 'Journal'
        elif self.resource_type ==  'BookChapter':
            container_type = 'Book'
        elif self.resource_type ==  'Monograph':
            container_type = 'BookSeries'
        else:
            container_type = 'Periodical'
 
        if res.get('message', {}).get('page', None):
            pages = res.get('message', {}).get('page', None).split('-')
            first_page = pages[0]
            last_page = pages[1] if len(pages) > 1 else None
        else:
            first_page = None
            last_page = None

        container_titles = res.get('message', {}).get('container-title', [])
        container_title = container_titles[0] if len(container_titles) > 0 else None
        if container_title is not None:
            self.container = compact({ 
                'type': container_type,
                'title': container_title,
                'identifier': self.issn,
                'identifierType': 'ISSN' if self.issn else None,
                'volume': res.get('message', {}).get('volume', None),
                'issue': res.get('message', {}).get('issue', None),
                'firstPage': first_page,
                'lastPage': last_page})
        else:
            self.container = None

        if self.issn:
            self.related_identifiers = [{ 'relationType': 'IsPartOf',
                                     'relatedIdentifierType': 'ISSN',
                                     'resourceTypeGeneral': 'Collection',
                                     'relatedIdentifier': self.issn }]
        else:
            self.related_identifiers = []
        references = res.get('message', {}).get('reference', [])
        for ref in references:
            doi = ref.get('DOI', None)
            if doi:
                self.related_identifiers.append({ 'relationType': 'References',
                                             'relatedIdentifierType': 'DOI',
                                             'relatedIdentifier': doi.lower() })

        self.funding_references = []
        funding_references = wrap(res.get('message', {}).get('funder', []))
        for funding in funding_references:
            funding_reference = compact({
                'funderName': funding.get('name', None),
                'funderIdentifier': doi_as_url(funding['DOI']) if funding.get('DOI', None) is not None else None,
                'funderIdentifierType': 'Crossref Funder ID' if funding.get('DOI', '').startswith('10.13039') else None
            })
            if funding.get('name', None) is not None and funding.get('award', None) is not None:
                for award in wrap(funding['award']):
                    fund_ref = funding_reference.copy()
                    fund_ref['awardNumber'] = award
                    self.funding_references.append(fund_ref)
        self.funding_references = self.funding_references or None
        description = res.get('message', {}).get('abstract', None)
        if description is not None:
            self.descriptions = [{'description': description,
                                  'descriptionType': 'Abstract' }]
        else:
            self.descriptions = None
        self.subjects = []
        for subject in wrap(res.get('message', {}).get('subject', [])):
            self.subjects.append({ 'subject': subject })
        self.subjects = self.subjects or None
        self.language = res.get('message', {}).get('language', None)
        self.version_info = res.get('message', {}).get('version', None)
        self.agency = get_doi_ra(self.id)
