from talbot import Crossref
from ..utils import (
    get_date_from_date_parts,
    dict_to_spdx, normalize_cc_url,
    CR_TO_BIB_TRANSLATIONS,
    CR_TO_SO_TRANSLATIONS,
    CR_TO_CP_TRANSLATIONS,
    CR_TO_RIS_TRANSLATIONS,
    CR_TO_DC_TRANSLATIONS
)
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
            'schemaOrg': CR_TO_SO_TRANSLATIONS[self.resource_type] or 'CreativeWork',
            'citeproc': CR_TO_CP_TRANSLATIONS[self.resource_type] or 'article-journal',
            'bibtex': CR_TO_BIB_TRANSLATIONS[self.resource_type] or 'misc',
            'ris': CR_TO_RIS_TRANSLATIONS[self.resource_type] or 'GEN',
        }
        self.url = res.get('message', {})['resource'].get('primary', {}).get('URL', None)
        self.titles = res.get('message', {}).get('title', [])
        self.publisher = res.get('message', {}).get('publisher', None)

        self.published_date = get_date_from_date_parts(res.get('message', {}).get('issued', None)) or get_date_from_date_parts(res.get('message', {}).get('created', None))
        self.updated_date = get_date_from_date_parts(res.get('message', {}).get('deposited', None)) or get_date_from_date_parts(res.get('message', {}).get('indexed', None))
        self.dates = [{ 'date': self.published_date, 'dateType': 'Issued' }]
        self.dates.append({ 'date': self.updated_date, 'dateType': 'Updated' }) if self.updated_date else None
        self.publication_year = self.published_date[0:4] if self.published_date else None
        self.date_registered = get_date_from_date_parts(res.get('message', {}).get('registered', {})) or get_date_from_date_parts(res.get('message', {}).get('created', None))
        
        licenses = res.get('message', {}).get('license', [])
        license = normalize_cc_url(next(item for item in licenses if item["content-version"] == "vor").get('URL', None))
        self.rights_list = [dict_to_spdx({ 'rightsURI': license })] if license else None
        
        issns = res.get('message', {}).get('issn-type', [])
        self.issn = next(item for item in issns if item["type"] == "electronic") or next(item for item in issns if item["type"] == "print") or {}
        self.issn = self.issn['value'] if self.issn else None


        #   related_identifiers += Array.wrap(meta.fetch('reference', nil)).map do |ref|
        #     doi = ref.fetch('DOI', nil)
        #     next unless doi.present?

        #     { 'relationType' => 'References',
        #       'relatedIdentifierType' => 'DOI',
        #       'relatedIdentifier' => doi.downcase }
        #   end.compact
        container_title = res.get('message', {}).get('container-title', [])[0]
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
            first_page = res.get('message', {}).get('page').split('-')[0]
            last_page = res.get('message', {}).get('page').split('-')[-1]
        else:
            first_page = None
            last_page = None
  
        container = { 
            'type': container_type,
            'title': container_title,
            'identifier': self.issn,
            'identifierType': 'ISSN' if self.issn else None,
            'volume': res.get('message', {}).get('volume', None),
            'issue': res.get('message', {}).get('issue', None),
            'firstPage': first_page,
            'lastPage': last_page }
        self.container = { k: v for k, v in container.items() if v is not None }

        if container_title and self.issn:
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
        self.related_identifiers = self.related_identifiers or None
        
        self.abstract = res.get('message', {}).get('abstract', None)
        self.agency = get_doi_ra(self.id)
