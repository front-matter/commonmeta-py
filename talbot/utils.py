import os
import html
import json
import re
import bleach
from urllib.parse import urlparse
import dateparser
from pydash import py_


from .doi_utils import normalize_doi, doi_from_url, get_doi_ra, validate_doi


NORMALIZED_LICENSES = {
    'https://creativecommons.org/licenses/by/1.0': 'https://creativecommons.org/licenses/by/1.0/legalcode',
    'https://creativecommons.org/licenses/by/2.0': 'https://creativecommons.org/licenses/by/2.0/legalcode',
    'https://creativecommons.org/licenses/by/2.5': 'https://creativecommons.org/licenses/by/2.5/legalcode',
    'https://creativecommons.org/licenses/by/3.0': 'https://creativecommons.org/licenses/by/3.0/legalcode',
    'https://creativecommons.org/licenses/by/3.0/us': 'https://creativecommons.org/licenses/by/3.0/legalcode',
    'https://creativecommons.org/licenses/by/4.0': 'https://creativecommons.org/licenses/by/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nc/1.0': 'https://creativecommons.org/licenses/by-nc/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nc/2.0': 'https://creativecommons.org/licenses/by-nc/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nc/2.5': 'https://creativecommons.org/licenses/by-nc/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nc/3.0': 'https://creativecommons.org/licenses/by-nc/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nc/4.0': 'https://creativecommons.org/licenses/by-nc/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/1.0': 'https://creativecommons.org/licenses/by-nd-nc/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/2.0': 'https://creativecommons.org/licenses/by-nd-nc/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/2.5': 'https://creativecommons.org/licenses/by-nd-nc/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/3.0': 'https://creativecommons.org/licenses/by-nd-nc/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/4.0': 'https://creativecommons.org/licenses/by-nd-nc/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/1.0': 'https://creativecommons.org/licenses/by-nc-sa/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/2.0': 'https://creativecommons.org/licenses/by-nc-sa/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/2.5': 'https://creativecommons.org/licenses/by-nc-sa/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/3.0': 'https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/4.0': 'https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nd/1.0': 'https://creativecommons.org/licenses/by-nd/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nd/2.0': 'https://creativecommons.org/licenses/by-nd/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nd/2.5': 'https://creativecommons.org/licenses/by-nd/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nd/3.0': 'https://creativecommons.org/licenses/by-nd/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nd/4.0': 'https://creativecommons.org/licenses/by-nd/2.0/legalcode',
    'https://creativecommons.org/licenses/by-sa/1.0': 'https://creativecommons.org/licenses/by-sa/1.0/legalcode',
    'https://creativecommons.org/licenses/by-sa/2.0': 'https://creativecommons.org/licenses/by-sa/2.0/legalcode',
    'https://creativecommons.org/licenses/by-sa/2.5': 'https://creativecommons.org/licenses/by-sa/2.5/legalcode',
    'https://creativecommons.org/licenses/by-sa/3.0': 'https://creativecommons.org/licenses/by-sa/3.0/legalcode',
    'https://creativecommons.org/licenses/by-sa/4.0': 'https://creativecommons.org/licenses/by-sa/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/1.0': 'https://creativecommons.org/licenses/by-nc-nd/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/2.0': 'https://creativecommons.org/licenses/by-nc-nd/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/2.5': 'https://creativecommons.org/licenses/by-nc-nd/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/3.0': 'https://creativecommons.org/licenses/by-nc-nd/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/4.0': 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode',
    'https://creativecommons.org/licenses/publicdomain': 'https://creativecommons.org/licenses/publicdomain/',
    'https://creativecommons.org/publicdomain/zero/1.0': 'https://creativecommons.org/publicdomain/zero/1.0/legalcode'
}

CR_TO_CP_TRANSLATIONS = {
    'Proceedings': None,
    'ReferenceBook': None,
    'JournalIssue': 'article-journal',
    'ProceedingsArticle': 'paper-conference',
    'Other': None,
    'Dissertation': 'thesis',
    'Dataset': 'dataset',
    'EditedBook': 'book',
    'PostedContent': 'article-journal',
    'JournalArticle': 'article-journal',
    'Journal': None,
    'Report': 'report',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': None,
    'BookSection': 'chapter',
    'BookPart': None,
    'Book': 'book',
    'BookChapter': 'chapter',
    'StandardSeries': None,
    'Monograph': 'book',
    'Component': None,
    'ReferenceEntry': 'entry-dictionary',
    'JournalVolume': None,
    'BookSet': None
}

CR_TO_SO_TRANSLATIONS = {
    'Proceedings': None,
    'ReferenceBook': 'Book',
    'JournalIssue': 'PublicationIssue',
    'ProceedingsArticle': None,
    'Other': 'CreativeWork',
    'Dissertation': 'Thesis',
    'Dataset': 'Dataset',
    'EditedBook': 'Book',
    'JournalArticle': 'ScholarlyArticle',
    'Journal': None,
    'Report': 'Report',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': None,
    'BookSection': None,
    'BookPart': None,
    'Book': 'Book',
    'BookChapter': 'Chapter',
    'StandardSeries': None,
    'Monograph': 'Book',
    'Component': 'CreativeWork',
    'ReferenceEntry': None,
    'JournalVolume': 'PublicationVolume',
    'BookSet': None,
    'PostedContent': 'ScholarlyArticle',
    'PeerReview': 'Review'
}

CR_TO_BIB_TRANSLATIONS = {
    'Proceedings': 'proceedings',
    'ReferenceBook': 'book',
    'JournalIssue': None,
    'ProceedingsArticle': None,
    'Other': None,
    'Dissertation': 'phdthesis',
    'Dataset': None,
    'EditedBook': 'book',
    'JournalArticle': 'article',
    'Journal': None,
    'Report': 'techreport',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': None,
    'BookSection': 'inbook',
    'BookPart': None,
    'Book': 'book',
    'BookChapter': 'inbook',
    'StandardSeries': None,
    'Monograph': 'book',
    'Component': None,
    'ReferenceEntry': None,
    'JournalVolume': None,
    'BookSet': None,
    'PostedContent': 'article'
}

CR_TO_RIS_TRANSLATIONS = {
    'Proceedings': 'CONF',
    'PostedContent': 'JOUR',
    'ReferenceBook': 'BOOK',
    'JournalIssue': 'JOUR',
    'ProceedingsArticle': 'CPAPER',
    'Other': 'GEN',
    'Dissertation': 'THES',
    'Dataset': 'DATA',
    'EditedBook': 'BOOK',
    'JournalArticle': 'JOUR',
    'Journal': None,
    'Report': 'RPRT',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': 'STAND',
    'BookSection': 'CHAP',
    'BookPart': 'CHAP',
    'Book': 'BOOK',
    'BookChapter': 'CHAP',
    'StandardSeries': None,
    'Monograph': 'BOOK',
    'Component': None,
    'ReferenceEntry': 'DICT',
    'JournalVolume': None,
    'BookSet': None
}

CR_TO_DC_TRANSLATIONS = {
    'Proceedings': None,
    'ReferenceBook': None,
    'JournalIssue': 'Text',
    'ProceedingsArticle': 'ConferencePaper',
    'Other': 'Other',
    'Dissertation': 'Dissertation',
    'Dataset': 'Dataset',
    'EditedBook': 'Book',
    'JournalArticle': 'JournalArticle',
    'Journal': 'Journal',
    'Report': 'Report',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': 'Standard',
    'BookSection': 'BookChapter',
    'BookPart': None,
    'Book': 'Book',
    'BookChapter': 'BookChapter',
    'SaComponent': 'Text',
    'StandardSeries': 'Standard',
    'Monograph': 'Book',
    'Component': None,
    'ReferenceEntry': None,
    'JournalVolume': None,
    'BookSet': None,
    'PostedContent': 'Preprint',
    'PeerReview': 'PeerReview'
}

DC_TO_SO_TRANSLATIONS = {
    'Audiovisual': 'MediaObject',
    'Book': 'Book',
    'BookChapter': 'Chapter',
    'Collection': 'Collection',
    'ComputationalNotebook': 'SoftwareSourceCode',
    'ConferencePaper': 'Article',
    'ConferenceProceeding': 'Periodical',
    'DataPaper': 'Article',
    'Dataset': 'Dataset',
    'Dissertation': 'Thesis',
    'Event': 'Event',
    'Image': 'ImageObject',
    'InteractiveResource': None,
    'Journal': 'Periodical',
    'JournalArticle': 'ScholarlyArticle',
    'Model': None,
    'OutputManagementPlan': None,
    'PeerReview': 'Review',
    'PhysicalObject': None,
    'Preprint': None,
    'Report': 'Report',
    'Service': 'Service',
    'Software': 'SoftwareSourceCode',
    'Sound': 'AudioObject',
    'Standard': None,
    'Text': 'ScholarlyArticle',
    'Workflow': None,
    'Other': 'CreativeWork',
    # not part of DataCite schema, but used internally
    'Periodical': 'Periodical',
    'DataCatalog': 'DataCatalog'
}

SO_TO_BIB_TRANSLATIONS = {
    'Article': 'article',
    'AudioObject': 'misc',
    'Thesis': 'phdthesis',
    'Blog': 'misc',
    'BlogPosting': 'article',
    'Collection': 'misc',
    'CreativeWork': 'misc',
    'DataCatalog': 'misc',
    'Dataset': 'misc',
    'Event': 'misc',
    'ImageObject': 'misc',
    'Movie': 'misc',
    'PublicationIssue': 'misc',
    'ScholarlyArticle': 'article',
    'Service': 'misc',
    'SoftwareSourceCode': 'misc',
    'VideoObject': 'misc',
    'WebPage': 'misc',
    'WebSite': 'misc'
}

SO_TO_CP_TRANSLATIONS = {
    'Article': 'article-newspaper',
    'AudioObject': 'song',
    'Blog': 'report',
    'BlogPosting': 'post-weblog',
    'Collection': None,
    'CreativeWork': None,
    'DataCatalog': 'dataset',
    'Dataset': 'dataset',
    'Event': None,
    'ImageObject': 'graphic',
    'Movie': 'motion_picture',
    'PublicationIssue': None,
    'Report': 'report',
    'ScholarlyArticle': 'article-journal',
    'Service': None,
    'Thesis': 'thesis',
    'VideoObject': 'broadcast',
    'WebPage': 'webpage',
    'WebSite': 'webpage'
}

SO_TO_DC_TRANSLATIONS = {
    'Article': 'Preprint',
    'AudioObject': 'Sound',
    'Blog': 'Text',
    'BlogPosting': 'Preprint',
    'Book': 'Book',
    'Chapter': 'BookChapter',
    'Collection': 'Collection',
    'CreativeWork': 'Text',
    'DataCatalog': 'Dataset',
    'Dataset': 'Dataset',
    'Event': 'Event',
    'ImageObject': 'Image',
    'Movie': 'Audiovisual',
    'PublicationIssue': 'Text',
    'Report': 'Report',
    'ScholarlyArticle': 'Text',
    'Thesis': 'Text',
    'Service': 'Service',
    'Review': 'PeerReview',
    'SoftwareSourceCode': 'Software',
    'VideoObject': 'Audiovisual',
    'WebPage': 'Text',
    'WebSite': 'Text'
}

SO_TO_RIS_TRANSLATIONS = {
    'Article': 'GEN',
    'AudioObject': None,
    'Blog': None,
    'BlogPosting': 'BLOG',
    'Collection': None,
    'CreativeWork': 'GEN',
    'DataCatalog': 'CTLG',
    'Dataset': 'DATA',
    'Event': None,
    'ImageObject': 'FIGURE',
    'Movie': 'MPCT',
    'Report': 'RPRT',
    'PublicationIssue': None,
    'ScholarlyArticle': 'JOUR',
    'Service': None,
    'SoftwareSourceCode': 'COMP',
    'VideoObject': 'VIDEO',
    'WebPage': 'ELEC',
    'WebSite': None
}

SO_TO_DC_RELATION_TYPES = {
    'citation': 'References',
    'isBasedOn': 'IsSupplementedBy',
    'sameAs': 'IsIdenticalTo',
    'isPartOf': 'IsPartOf',
    'hasPart': 'HasPart',
    'isPredecessor': 'IsPreviousVersionOf',
    'isSuccessor': 'IsNewVersionOf'
}

SO_TO_DC_REVERSE_RELATION_TYPES = {
    'citation': 'IsReferencedBy',
    'isBasedOn': 'IsSupplementTo',
    'sameAs': 'IsIdenticalTo',
    'isPartOf': 'HasPart',
    'hasPart': 'IsPartOf',
    'isPredecessor': 'IsNewVersionOf',
    'isSuccessor': 'IsPreviousVersionOf'
}

UNKNOWN_INFORMATION = {
    ':unac':  'temporarily inaccessible',
    ':unal':  'unallowed, suppressed intentionally',
    ':unap':  'not applicable, makes no sense',
    ':unas':  'value unassigned (e.g., Untitled)',
    ':unav':  'value unavailable, possibly unknown',
    ':unkn':  'known to be unknown (e.g., Anonymous, Inconnue)',
    ':none':  'never had a value, never will',
    ':null':  'explicitly and meaningfully empty',
    ':tba':  'to be assigned or announced later',
    ':etal':  'too numerous to list (et alia)'
}

MONTH_NAMES = {
    '01': 'jan',
    '02': 'feb',
    '03': 'mar',
    '04': 'apr',
    '05': 'may',
    '06': 'jun',
    '07': 'jul',
    '08': 'aug',
    '09': 'sep',
    '10': 'oct',
    '11': 'nov',
    '12': 'dec'
}


def get_iso8601_date(date):
    """Get ISO 8601 date"""
    if date is None:
        return None
    if isinstance(date, str):
        return dateparser.parse(date).isoformat()

    return None


def get_date(dates, date_type='Issued', date_only=False):
    """Get date"""
    dd = py_.find(wrap(dates), lambda x: x['dateType'] == date_type) or {}
    if dd is None:
        return None
    if date_only:
        return dd.get('date', '')[0:10]
    return dd.get('date', None)


def get_date_parts(iso8601_time):
    """Get date parts"""
    if iso8601_time is None:
        return {'date-parts': [[]]}

    # add 0s to the end of the date if it is incomplete
    if len(iso8601_time) < 10:
        iso8601_time = iso8601_time.ljust(10, '0')

    year = int(iso8601_time[0:4])
    month = int(iso8601_time[5:7])
    day = int(iso8601_time[8:10])

    date_parts = py_.reject([year, month, day], lambda x: x == 0)
    return {'date-parts': [date_parts]}


def get_date_from_date_parts(date_as_parts):
    """Get date from date parts"""
    if date_as_parts is None:
        return None
    date_parts = date_as_parts.get('date-parts', [])
    if len(date_parts) == 0:
        return None
    date_parts = date_parts[0]
    year = date_parts[0] if len(date_parts) > 0 else 0
    month = date_parts[1] if len(date_parts) > 1 else 0
    day = date_parts[2] if len(date_parts) > 2 else 0
    return get_date_from_parts(year, month, day)


def get_date_from_parts(year=0, month=0, day=0):
    """Get date from parts"""
    arr = [str(year).rjust(4, '0'), str(
        month).rjust(2, '0'), str(day).rjust(2, '0')]
    arr = [e for i, e in enumerate(arr) if not (e == '00' or e == '0000')]
    return None if len(arr) == 0 else '-'.join(arr)


def get_month_from_date(date):
    """Get month from date"""
    if date is None:
        return None
    if isinstance(date, dict):
        date = get_date_from_parts(date)
    if isinstance(date, str):
        date = date.split('-')
    return MONTH_NAMES.get(date[1], None) if len(date) > 1 else None


def wrap(item):
    """Turn None, dict, or list into list"""
    if item is None:
        return []
    if isinstance(item, list):
        return item
    return [item]


def unwrap(list):
    """Turn list into dict or None, depending on list size"""
    if len(list) == 0:
        return None
    if len(list) == 1:
        return list[0]
    return list


def presence(item):
    """Turn empty list, dict or str into None"""
    return None if len(item) == 0 else item


def compact(dict_or_list):
    """Remove None from dict or list"""
    if type(dict_or_list) in [None, str]:
        return dict_or_list
    if isinstance(dict_or_list, dict):
        return {k: v for k, v in dict_or_list.items() if v is not None}
    if isinstance(dict_or_list, list):
        arr = (list(map(lambda x: compact(x), dict_or_list)))
        return None if len(arr) == 0 else arr


def parse_attributes(element, **kwargs):
    """extract attributes from a string, dict or list"""
    content = kwargs.get('content', '__content__')

    if isinstance(element, str) and kwargs.get('content', None) is None:
        return html.unescape(element)
    if isinstance(element, dict):
        return element.get(html.unescape(content), None)
    if isinstance(element, list):
        arr = list(map(lambda x: x.get(html.unescape(content), None)
                       if isinstance(x, dict) else x, element))
        arr = arr[0] if kwargs.get('first') else unwrap(arr)
        return arr


def normalize_id(id, **kwargs):
    """Check for valid DOI or HTTP(S) URL"""
    if id is None:
        return None

    # check for valid DOI
    doi = normalize_doi(id, **kwargs)
    if doi is not None:
        return doi

    # check for valid HTTP uri
    uri = urlparse(id)
    if not uri.netloc or uri.scheme not in ['http', 'https']:
        return None
    # make id lowercase
    id = id.lower()
    # remove trailing slash
    if id.endswith('/'):
        id = id.strip('/')
    # ensure https
    if id.startswith('http://'):
        id = id.replace('http://', 'https://')
    # decode utf-8
    # id = id.encode("utf-8")
    return id


def normalize_ids(ids=None, relation_type=None):
    """Normalize identifiers"""
    formatted_ids = []
    for idx in wrap(ids):
        if idx.get('@id', None) is not None:
            id = normalize_id(idx['@id'])
            related_identifier_type = 'DOI' if doi_from_url(
                id) is not None else 'URL'
            id = doi_from_url(id) or id
            type = idx.get('@type') if isinstance(idx.get('@type',
                                                          None), str) else wrap(idx.get('@type', None))[0]
            formatted_ids.append(compact({'relatedIdentifier': id,
                                          'relationType': relation_type,
                                          'relatedIdentifierType': related_identifier_type,
                                          'resourceTypeGeneral': SO_TO_DC_TRANSLATIONS.get(type, None)}))
    return formatted_ids


def crossref_api_url(doi):
    """Return the Crossref API URL for a given DOI"""
    return 'https://api.crossref.org/works/' + doi


def normalize_url(url, secure=False):
    """Normalize URL"""
    if url is None:
        return None
    if url.endswith('/'):
        url = url.strip('/')
    if secure is True and url.startswith('http://'):
        url = url.replace('http://', 'https://')
    return url.lower()


def normalize_cc_url(url):
    """Normalize Creative Commons URL"""
    if url is None:
        return None
    url = normalize_url(url, secure=True)
    return NORMALIZED_LICENSES.get(url, url)


def normalize_orcid(orcid):
    """Normalize ORCID"""
    orcid = validate_orcid(orcid)
    if orcid is None:
        return None
    return 'https://orcid.org/' + orcid


def validate_orcid(orcid):
    """Validate ORCID"""
    match = re.search(
        r"\A(?:(?:http|https)://(?:(?:www|sandbox)?\.)?orcid\.org/)?(\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{3}[0-9X]+)\Z", orcid)
    if match is None:
        return None
    orcid = re.sub(' ', '-', match.group(1))
    return orcid


def dict_to_spdx(dict):
    """Convert a dict to SPDX"""
    dict.update({'rightsURI': normalize_cc_url(dict.get('rightsURI', None))})
    file_path = os.path.join(os.path.dirname(
        __file__), 'resources/spdx/licenses.json')
    with open(file_path) as json_file:
        spdx = json.load(json_file).get('licenses')
    license = next((l for l in spdx if l['licenseId'].lower() == dict.get(
        'rightsIdentifier', None) or l['seeAlso'][0] == dict.get('rightsURI', None)), None)
    if license is None:
        return dict
    #   license = spdx.find do |l|
    #     l['licenseId'].casecmp?(hsh['rightsIdentifier']) || l['seeAlso'].first == normalize_cc_url(hsh['rightsURI']) || l['name'] == hsh['rights'] || l['seeAlso'].first == normalize_cc_url(hsh['rights'])
    #   end
    return compact({
        'rights': license['name'],
        'rightsURI': license['seeAlso'][0],
        'rightsIdentifier': license['licenseId'].lower(),
        'rightsIdentifierScheme': 'SPDX',
        'schemeUri': 'https://spdx.org/licenses/',
        'lang': dict.get('lang', None)
    })

    #   else
    #     {
    #       'rights': hsh['__content__'] || hsh['rights'],
    #       'rightsUri': hsh['rightsURI'] || hsh['rightsUri'],
    #       'rightsIdentifier': hsh['rightsIdentifier'].present? ? hsh['rightsIdentifier'].downcase : None,
    #       'rightsIdentifierScheme': hsh['rightsIdentifierScheme'],
    #       'schemeUri': hsh['schemeUri'],
    #       'lang': hsh['lang']
    #     }.compact
    #   end
    # end


def from_citeproc(element):
    """Convert a citeproc element to CSL"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        if elem.get('literal', None) is not None:
            el['@type'] = 'Organization'
            el['name'] = el['literal']
        elif elem.get('name', None) is not None:
            el['@type'] = 'Organization'
            el['name'] = elem.get('name')
        else:
            el['@type'] = 'Person'
            el['name'] = ' '.join(
                compact([elem.get('given', None), elem.get('family', None)]))
        el['givenName'] = elem.get('given', None)
        el['familyName'] = elem.get('family', None)
        el['affiliation'] = elem.get('affiliation', None)
        formatted_element.append(compact(el))
    return formatted_element


def to_citeproc(element):
    """Convert a CSL element to citeproc"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        el['family'] = elem.get('familyName', None)
        el['given'] = elem.get('givenName', None)
        el['literal'] = elem.get('name', None) if elem.get(
            'familyName', None) is None else None
        formatted_element.append(compact(el))
    return formatted_element


def to_ris(element):
    """Convert a CSL element to RIS"""
    formatted_element = []
    for elem in wrap(element):
        if elem['familyName'] is not None:
            el = ', '.join([elem['familyName'], elem['givenName']])
        else:
            el = elem['name']
        formatted_element.append(el)
    return formatted_element


def to_schema_org(element):
    """Convert a CSL element to Schema.org"""
    mapping = {'type': '@type', 'id': '@id', 'title': 'name'}
    for key, value in mapping.items():
        if element.get(key, None) is not None:
            element[value] = element.pop(key)
    return element


def to_schema_org_creators(element):
    """Convert CSL creators to Schema.org creators"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        # el['affiliation'] = wrap(element['affiliation']).map do |a|
        #   if a.is_a?(String)
        #     name = a
        #     affiliation_identifier = nil
        #   else
        #     name = a['name']
        #     affiliation_identifier = a['affiliationIdentifier']
        #   end

        #   { '@type' => 'Organization', '@id' => affiliation_identifier, 'name' => name }.compact
        # end.unwrap
        el['@type'] = elem['nameType'][0:-
            3] if elem.get('nameType', None) else None
        # el['@id']= vwrap(c['nameIdentifiers']).first.to_h.fetch('nameIdentifier', nil)
        el['name'] = ' '.join([elem['givenName'], elem['familyName']]
                              ) if elem['familyName'] else elem.get('name', None)
        # c.except('nameIdentifiers', 'nameType').compact
        formatted_element.append(compact(el))
    return unwrap(formatted_element)


def to_schema_org_contributors(element):
    """Convert CSL contributors to Schema.org contributors"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        # c['affiliation'] = Array.wrap(c['affiliation']).map do |a|
        #   if a.is_a?(String)
        #     name = a
        #     affiliation_identifier = nil
        #   else
        #     name = a['name']
        #     affiliation_identifier = a['affiliationIdentifier']
        #   end

        #   { '@type' => 'Organization', '@id' => affiliation_identifier, 'name' => name }.compact
        # end.unwrap
        el['@type'] = elem['nameType'][0:-
            3] if elem.get('nameType', None) else None
        # el['@id']=# vwrap(c['nameIdentifiers']).first.to_h.fetch('nameIdentifier', nil)
        el['name'] = ' '.join([elem['givenName'], elem['familyName']]
                              ) if elem['familyName'] else elem.get('name', None)
        # c.except('nameIdentifiers', 'nameType').compact
        formatted_element.append(compact(el))
    return unwrap(formatted_element)


def to_schema_org_container(element, **kwargs):
    """Convert CSL container to Schema.org container"""
    if isinstance(element, dict) or (element is None and kwargs.get('container_title', None)):
        return None

    return compact({
        '@id': element.get('identifier', None),
        '@type': 'DataCatalog' if kwargs.get('type', None) == 'Dataset' else 'Periodical',
        'name': element['title'] or kwargs.get('container_title', None)
    })


def to_schema_org_identifiers(element, **kwargs):
    """Convert CSL identifiers to Schema.org identifiers"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        el['@type'] = 'PropertyValue'
        el['propertyID'] = elem.get('identifierType', None)
        el['value'] = elem.get('identifier', None)
        formatted_element.append(compact(el))
    return unwrap(formatted_element)


def to_schema_org_relation(related_identifiers=None, relation_type=None):
    """Convert CSL related identifiers to Schema.org relations"""
    if related_identifiers is None or relation_type is None:
        return None

    # consolidate different relation types
    if relation_type == 'References':
        relation_type = ['References', 'Cites']
    else:
        relation_type = [relation_type]

    related_identifiers = py_.filter(
        wrap(related_identifiers), lambda ri: ri['relationType'] in relation_type)

    formatted_identifiers = []
    for r in related_identifiers:
        if r['relatedIdentifierType'] == 'ISSN' and r['relationType'] == 'IsPartOf':
            formatted_identifiers.append(
                compact({'@type': 'Periodical', 'issn': r['relatedIdentifier']}))
        else:
            formatted_identifiers.append(compact({
                '@id': normalize_id(r['relatedIdentifier']),
                '@type': DC_TO_SO_TRANSLATIONS.get(r['resourceTypeGeneral'], 'CreativeWork')}))
    return unwrap(formatted_identifiers)

def find_from_format(id=None, string=None, ext=None, filename=None):
    """Find reader from format"""
    if id is not None:
        return find_from_format_by_id(id)
    if string is not None and ext is not None:
        return find_from_format_by_ext(string, ext=ext)
    if string is not None:
        return find_from_format_by_string(string)
    if filename is not None:
        return find_from_format_by_filename(filename)
    return 'datacite'


def find_from_format_by_id(id):
    """Find reader from format by id"""
    doi=validate_doi(id)
    if doi and (ra := get_doi_ra(doi)) is not None:
        return ra.lower()
    if re.match(r"\A(?:(http|https):/(/)?orcid\.org/)?(\d{4}-\d{4}-\d{4}-\d{3}[0-9X]+)\Z", id) is not None:
        return 'orcid'
    if re.match(r"\A(http|https):/(/)?github\.com/(.+)/package.json\Z", id) is not None:
        return 'npm'
    if re.match(r"\A(http|https):/(/)?github\.com/(.+)/codemeta.json\Z", id) is not None:
        return 'codemeta'
    if re.match(r"\A(http|https):/(/)?github\.com/(.+)/CITATION.cff\Z", id) is not None:
        return 'cff'
    if re.match(r"\A(http|https):/(/)?github\.com/(.+)\Z", id) is not None:
        return 'cff'
    return 'schema_org'


def find_from_format_by_ext(string, ext=None):
    """Find reader from format by ext"""


def find_from_format_by_string(string):
    """Find reader from format by string"""
    try:
        if json.loads(string).get('@context', None) == 'http://schema.org':
            return 'schema_org'
        if json.loads(string).get('schema-version', '').beginswith('http://datacite.org/schema/kernel'):
            return 'datacite_json'
        if json.loads(string).get('source', None) == 'Crossref':
            return 'crossref_json'
        if py_.get(json.loads(string), 'issued.date-parts', None) is not None:
            return 'citeproc'
        if string.startswith('TY  - '):
            return 'ris'
        return 'datacite'
    except NameError:
        return 'datacite'
    # if Maremma.from_xml(string).to_h.dig('crossref_result', 'query_result', 'body', 'query',
    #                                        'doi_record', 'crossref').present?
    #     'crossref'
    #   elsif Nokogiri::XML(string, None, 'UTF-8', &:noblanks).collect_namespaces.find do |_k, v|
    #           v.start_with?('http://datacite.org/schema/kernel')
    # #         end
    #     'datacite'
    #   elsif URI(Maremma.from_json(string).to_h.fetch('@context', '')).host == 'schema.org'
    #     'schema_org'
    #   elsif Maremma.from_json(string).to_h.dig('@context') == ('https://raw.githubusercontent.com/codemeta/codemeta/master/codemeta.jsonld')
    #     'codemeta'
    #   elsif Maremma.from_json(string).to_h.dig('schema-version').to_s.start_with?('http://datacite.org/schema/kernel')
    #     'datacite_json'
    #   elsif Maremma.from_json(string).to_h.dig('source') == ('Crossref')
    #     'crossref_json'
    #   elsif Maremma.from_json(string).to_h.dig('types').present? && Maremma.from_json(string).to_h.dig('publication_year').present?
    #     'crosscite'
    #   elsif Maremma.from_json(string).to_h.dig('issued', 'date-parts').present?
    #     'citeproc'

    #   elsif YAML.load(string).to_h.fetch('cff-version', None).present?
    #     'cff'


def find_from_format_by_filename(filename):
    """Find reader from format by filename"""
    if filename == 'package.json':
        return 'npm'
    if filename == 'CITATION.cff':
        return 'cff'
    return None


def camel_case(text):
    """Convert text to camel case"""
    s=text.replace("-", " ").replace("_", " ")
    s=s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])


def from_schema_org(element):
    """Convert schema.org to DataCite"""
    if element is None:
        return None
    element['type']=element.get('@type', None)
    element['id']=element.get('@id', None)
    return compact(py_.omit(element, ['@type', '@id']))


def from_schema_org_creators(element):
    """Convert schema.org creators to DataCite"""
    formatted_element=[]
    for elem in wrap(element):
        if isinstance(elem.get('affiliation', None), str):
            elem['affiliation']={'name': elem['affiliation']}
            affiliation_identifier_scheme=None
            scheme_uri=None
        elif py_.get(elem, 'affiliation.@id', '').startswith('https://ror.org'):
            affiliation_identifier_scheme='ROR'
            scheme_uri='https://ror.org/'
        elif elem.get('affiliation.@id', '').startswith('https://isni.org'):
            affiliation_identifier_scheme='ISNI'
            scheme_uri='https://isni.org/isni/'
        else:
            affiliation_identifier_scheme=None
            scheme_uri=None

        # alternatively find the nameIdentifier in the identifer attribute
        # if elem.get('identifier', None) is not None and elem.get('@id', None) is not None:
        #    elem['@id'] = elem['identifier']
        # alternatively find the nameIdentifier in the sameAs attribute
        # elem['@id'] = py_.find(wrap(elem.get('sameAs', None)), lambda x: x == 'orcid.org')

        if elem.get('@id', None) is not None:
            # elem['@id'] = normalize_orcid(elem.get('@id'))
            identifier_scheme='ORCID'
            scheme_uri='https://orcid.org/'
        elem['nameIdentifier']=[
            {'__content__': elem.get('@id', None),
             'nameIdentifierScheme': 'ORCID',
             'schemeUri': 'https://orcid.org'}]

        if isinstance(elem.get('@type', None), list):
            elem['@type']=py_.find(elem['@type'],
                                   lambda x: x in ['Person', 'Organization'])
        elem['creatorName']=compact({'nameType': elem['@type'].title() + 'al' if elem.get('@type', None) is not None else None,
                                       '__content__': elem['name']})
        elem['affiliation']=compact({'__content__': py_.get(elem, 'affiliation.name', None),
                                       'affiliationIdentifier': py_.get(elem, 'affiliation.@id', None),
                                       'affiliationIdentifierScheme': affiliation_identifier_scheme,
                                       'schemeUri': scheme_uri})
        formatted_element.append(py_.omit(elem, '@id', '@type', 'name'))
    return formatted_element


def from_schema_org_contributors(element):
    """Parse contributors from schema.org"""
    formatted_element=[]
    for elem in wrap(element):
        if isinstance(elem.get('affiliation', None), str):
            elem['affiliation']={'name': elem['affiliation']}
            affiliation_identifier_scheme=None
            scheme_uri=None
        elif py_.get(elem, 'affiliation.@id', '').startswith('https://ror.org'):
            affiliation_identifier_scheme='ROR'
            scheme_uri='https://ror.org/'
        elif py_.get(elem, 'affiliation.@id', '').startswith('https://isni.org'):
            affiliation_identifier_scheme='ISNI'
            scheme_uri='https://isni.org/isni/'
        else:
            affiliation_identifier_scheme=None
            scheme_uri=None

        if normalize_orcid(elem.get('@id', None)) is not None:
            elem['nameIdentifier']=[{'__content__': elem['@id'],
                                       'nameIdentifierScheme': 'ORCID',
                                       'schemeUri': 'https://orcid.org'}]
        elem['contributorName']=compact({'nameType': elem['@type'].titleize + 'al' if elem.get('@type', None) is not None else None,
                                           '__content__': elem['name']})
        elem['affiliation']=compact({'__content__': py_.get(elem, 'affiliation.name', None),
                                       'affiliationIdentifier': py_.get(elem, 'affiliation.@id', None),
                                       'affiliationIdentifierScheme': affiliation_identifier_scheme,
                                       'schemeUri': scheme_uri})
        formatted_element.append(py_.omit(elem, '@id', '@type', 'name'))
    return formatted_element


def pages_as_string(container, page_range_separator='-'):
    """Parse pages for BibTeX"""
    if container is None:
        return None
    if container.get('firstPage', None) is None:
        return None
    if container.get('lastPage', None) is None:
        return container.get('firstPage', None)

    return page_range_separator.join(compact([container.get('firstPage'), container.get('lastPage', None)]))


def subjects_as_string(subjects):
    """convert subject list to string, e.g. for bibtex"""
    if subjects is None:
        return None

    keywords=[]
    for subject in wrap(subjects):
        keywords.append(subject.get('subject', None))
    return ', '.join(keywords)


# def reverse():
#       return { 'citation': wrap(related_identifiers).select do |ri|
#                         ri['relationType'] == 'IsReferencedBy'
#                       end.map do |r|
#                         { '@id': normalize_doi(r['relatedIdentifier']),
#                           '@type': r['resourceTypeGeneral'] validate_orcid 'ScholarlyArticle',
#                           'identifier' => r['relatedIdentifierType'] == 'DOI' ? nil : to_identifier(r) }.compact
#                       end.unwrap,
#         'isBasedOn': wrap(related_identifiers).select do |ri|
#                          ri['relationType'] == 'IsSupplementTo'
#                        end.map do |r|
#                          { '@id': normalize_doi(r['relatedIdentifier']),
#                            '@type': r['resourceTypeGeneral'] or 'ScholarlyArticle',
#                            'identifier': r['relatedIdentifierType'] == 'DOI' ? nil : to_identifier(r) }.compact
#                        end.unwrap }.compact

def name_to_fos(name):
    """Convert name to Fields of Science (OECD) subject"""
    #   # first find subject in Fields of Science (OECD)
    #   fos = JSON.load(File.read(File.expand_path('../../resources/oecd/fos-mappings.json',
    #                                              __dir__))).fetch('fosFields')

    #   subject = fos.find { |l| l['fosLabel'] == name || 'FOS: ' + l['fosLabel'] == name }

    #   if subject
    #     return [{
    #       'subject' => sanitize(name).downcase
    #     },
    #             {
    #               'subject' => 'FOS: ' + subject['fosLabel'],
    #               'subjectScheme' => 'Fields of Science and Technology (FOS)',
    #               'schemeUri' => 'http://www.oecd.org/science/inno/38235147.pdf'
    #             }]
    #   end

    #   # if not found, look in Fields of Research (Australian and New Zealand Standard Research Classification)
    #   # and map to Fields of Science. Add an extra entry for the latter
    #   fores = JSON.load(File.read(File.expand_path('../../resources/oecd/for-mappings.json',
    #                                                __dir__)))
    #   for_fields = fores.fetch('forFields')
    #   for_disciplines = fores.fetch('forDisciplines')

    #   subject = for_fields.find { |l| l['forLabel'] == name } ||
    #             for_disciplines.find { |l| l['forLabel'] == name }

    #   if subject
    #     [{
    #       'subject' => sanitize(name).downcase
    #     },
    #      {
    #        'subject' => 'FOS: ' + subject['fosLabel'],
    #        'subjectScheme' => 'Fields of Science and Technology (FOS)',
    #        'schemeUri' => 'http://www.oecd.org/science/inno/38235147.pdf'
    #      }]
    #   else
    return [{'subject': name.lower()}]


def strip_milliseconds(iso8601_time):
    """strip milliseconds if there is a time, as it interferes with edtc parsing"""
    if iso8601_time is None:
        return None
    elif ' ' in iso8601_time:
        return iso8601_time.split(' ')[0]
    elif 'T00:00:00' in iso8601_time:
        return iso8601_time.split('T')[0]
    elif '+00:00' in iso8601_time:
        return iso8601_time.split('+')[0] + 'Z'
    elif '.' in iso8601_time:
        return iso8601_time.split('.')[0] + 'Z'

    return iso8601_time

def sanitize(text, **kwargs):
    """Sanitize text"""
    tags=kwargs.get('tags', None) or frozenset(
        {'b', 'br', 'code', 'em', 'i', 'sub', 'sup', 'strong'})
    content=kwargs.get('content', None) or '__content__'
    first=kwargs.get('first', True)
    strip=kwargs.get('strip', True)

    if isinstance(text, str):
        string=bleach.clean(text, tags=tags, strip=strip)
        # remove excessive internal whitespace
        return " ".join(re.split(r"\s+", string, flags=re.UNICODE))
        # return re.sub(r'\\s\\s+', ' ', string)
    elif isinstance(text, dict):
        return sanitize(text.get(content, None))
    elif isinstance(text, list):
        if len(text) == 0:
            return None

        lst=[]
        for e in text:
            lst.append(sanitize(e.get(content, None))
                       if isinstance(e, dict) else sanitize(e))  # uniq
        return lst[0] if first else unwrap(lst)
