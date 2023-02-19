"""cff reader for Talbot"""
from typing import Optional
import requests
import yaml

from ..utils import (normalize_id, from_schema_org_creators,
                     name_to_fos, dict_to_spdx, normalize_orcid,
                     github_as_cff_url, github_as_repo_url)
from ..base_utils import compact, wrap, presence, sanitize, parse_attributes
from ..date_utils import get_iso8601_date
from ..doi_utils import doi_from_url
from ..constants import (
    TalbotMeta,
    SO_TO_DC_TRANSLATIONS,
    SO_TO_CP_TRANSLATIONS,
    SO_TO_BIB_TRANSLATIONS,
    SO_TO_RIS_TRANSLATIONS)


def get_cff(pid: str, **kwargs) -> dict:
    """get_cff"""
    url = github_as_cff_url(pid)
    response = requests.get(url, kwargs, timeout=5)
    if response.status_code != 200:
        return {"state": "not_found"}
    text = response.text
    repo_url = github_as_repo_url(url)
    data = yaml.safe_load(text)

    # collect metadata not included in the CFF file
    if data.get('repository-code', None) is None:
        data['repository-code'] = repo_url

    return data


def read_cff(data: Optional[dict], **kwargs) -> TalbotMeta:
    """read_cff"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    read_options = kwargs or {}

    # read_options = ActiveSupport::HashWithIndifferentAccess.new(options.except(:doi, :id, :url, :sandbox, :validate, :ra))

    # identifiers = Array.wrap(meta.fetch('identifiers', nil)).map do |r|
    #   r = normalize_id(r) if r.is_a?(String)
    #   if r.is_a?(String) && URI(r).host != 'doi.org'
    #     { 'identifierType' => 'URL', 'identifier' => r }
    #   elsif r.is_a?(Hash)
    #     { 'identifierType' => get_identifier_type(r['propertyID']), 'identifier' => r['value'] }
    #   end
    # end.compact.uniq

    pid = normalize_id(kwargs.get('doi', None) or meta.get('doi', None))
    # Array.wrap(meta.fetch('identifiers', nil)).find do |i|
    #                                                     i['type'] == 'doi'
    #                                                   end.fetch('value', nil))
    url = normalize_id(meta.get('repository-code', None))
    creators = cff_creators(wrap(meta.get('authors', None)))

    if meta.get('title', None):
        titles = [{'title': meta.get('title', None)}]
    else:
        titles = []

    dates = []
    if meta.get('date-released', None):
        released_date = get_iso8601_date(meta.get('date-released'))
        dates = [{'date': released_date, 'dateType': 'Issued'}]
        publication_year = int(released_date[0:4])
    else:
        dates = []
        publication_year = None

    publisher = 'GitHub' if url and url.startswith('https://github.com') else None

    types = compact({
        'resourceTypeGeneral': 'Software',
        'resourceType': None,
        'schemaOrg': 'SoftwareSourceCode',
        'citeproc': 'article-journal',
        'bibtex': 'misc',
        'ris': 'COMP'
    })

    if meta.get('abstract', None):
        descriptions = [{ 'description': sanitize(meta.get('abstract')),
                          'descriptionType': 'Abstract' }]
    else:
        descriptions = []

    subjects = [name_to_fos(i) for i in wrap(meta.get('keywords', None))]

    if meta.get('licenseId', None):
        rights = [dict_to_spdx({'rightsIdentifier': meta.get('licenseId')})]
    else:
        rights = None

    related_items = cff_references(wrap(meta.get('references', None)))

    state = 'findable' if meta or read_options else 'not_found'

    return {
        'pid': pid,
        'types': types,
        # 'identifiers' => identifiers,
        'doi': doi_from_url(pid) if pid else None,
        'url': url,
        'titles': titles,
        'creators': creators,
        'publisher': publisher,
        'related_identifiers': related_items,
        'dates': dates,
        'publication_year': publication_year,
        'descriptions': presence(descriptions),
        'rights': rights,
        'version': meta.get('version', None),
        'subjects': presence(subjects),
        'state': state} | read_options


def cff_creators(creators):
    """cff_creators"""
    def format_affiliation(affiliation):
        """format_affiliation"""
        if isinstance(affiliation, str):
            return {'name': affiliation}
        if isinstance(affiliation, dict):
            return compact(affiliation)
        return None
        #         if a.is_a?(Hash)
        #   a
        # elsif a.is_a?(Hash) && a.key?('__content__') && a['__content__'].strip.blank?
        #   nil
        # elsif a.is_a?(Hash) && a.key?('__content__')
        #   { 'name' => a['__content__'] }
        # elsif a.strip.blank

    def format_element(i):
        """format_element"""
        if normalize_orcid(parse_attributes(i.get('orcid', None))):
            name_identifiers = [{
                'nameIdentifier': normalize_orcid(parse_attributes(i.get('orcid', None))),
                'nameIdentifierScheme': 'ORCID',
                'schemeUri': 'https://orcid.org'
            }]
        else:
            name_identifiers = None
        if i.get('given-names', None) or i.get('family-names', None) or name_identifiers:
            given_name = parse_attributes(i.get('given-names', None))
            family_name = parse_attributes(i.get('family-names', None))
            affiliation = compact([format_affiliation(
                a) for a in wrap(i.get('affiliation', None))])

            return compact({'nameType': 'Personal',
                            'nameIdentifiers': name_identifiers,
                            'givenName': given_name,
                            'familyName': family_name,
                            'affiliation': affiliation})
        return {'nameType': 'Organizational', 'name': i.get('name', None) or i.get('__content__', None)}

    return [format_element(i) for i in creators]


def cff_references(references):
    """cff_references"""
    def format_element(i):
        """format_element"""
        identifier = next((item for item in wrap(
            i.get('identifers', None)) if item.get("type", None) == "doi"), None)
        if identifier is None:
            return None
        return compact({'relatedItemIdentifier': normalize_id(parse_attributes(identifier.get('value', None))),
                        'relationType': 'References',
                        'relatedItemIdentifierType': 'DOI'})

    return [format_element(i) for i in references]