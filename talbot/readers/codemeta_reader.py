"""codemeta reader for Talbot"""
import requests
from typing import Optional

from ..utils import (normalize_url, normalize_id, from_schema_org_creators,
                     name_to_fos, dict_to_spdx,
                     doi_from_url)
from ..base_utils import compact, wrap, presence, sanitize
from ..author_utils import get_authors
from ..constants import (
    TalbotMeta,
    SO_TO_DC_TRANSLATIONS,
    SO_TO_CP_TRANSLATIONS,
    SO_TO_BIB_TRANSLATIONS,
    SO_TO_RIS_TRANSLATIONS)


def get_codemeta(pid: str, **kwargs) -> dict:
    """get_codemeta"""
    url = pid
    response = requests.get(url, kwargs, timeout=5)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json()
    # response = Maremma.get(github_as_codemeta_url(id), accept: 'json', raw: true)
    # string = response.body.get('data', None)


def read_codemeta(data: Optional[dict], **kwargs) -> TalbotMeta:
    """read_codemeta"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    read_options = kwargs or {}
    # ActiveSupport: : HashWithIndifferentAccess.new(options.except(: doi, : id, : url,
    # : sandbox, : validate, : ra)

    pid = normalize_id(meta.get('pid', None) or meta.get('identifier', None))
    # id = normalize_id(options[:doi] | | meta.get('@id', None) | | meta.get('identifier', None))
    # identifiers = Array.wrap(meta.get('identifier', None)).map do | r|
    #   r = normalize_id(r) if r.is_a?(String)
    #   if r.is_a?(String) & & URI(r) != 'doi.org'
    #     {'identifierType': 'URL', 'identifier': r}
    #   elsif r.is_a?(Hash)
    #     {'identifierType': get_identifier_type(
    #         r['propertyID']), 'identifier': r['value']}
    #   end
    # end.compact.uniq

    has_agents = meta.get('agents', None)
    authors = meta.get('authors', None) if has_agents is None else has_agents
    creators = get_authors(from_schema_org_creators(wrap(authors)))
    contributors = get_authors(
        from_schema_org_creators(wrap(meta.get('editor', None))))
    dates = []
    if meta.get('datePublished', None):
        dates.append({'date': meta.get('datePublished'), 'dateType': 'Issued'})
        publication_year = int(meta.get('datePublished')[0:4])
    if meta.get('dateCreated', None):
        dates.append({'date': meta.get('dateCreated'), 'dateType': 'Created'})
    if meta.get('dateModified', None):
        dates.append({'date': meta.get('dateModified'), 'dateType': 'Updated'})

    publisher = meta.get('publisher', None)

    if meta.get('description', None):
        descriptions = [{'description': sanitize(meta.get('description')),
                         'descriptionType': 'Abstract'}]
    else:
        descriptions = None

    schema_org = meta.get('@type', None)
    types = compact({
        'resourceTypeGeneral': SO_TO_DC_TRANSLATIONS.get(schema_org, None),
        'resourceType': meta.get('additionalType', None),
        'schemaOrg': schema_org,
        'citeproc': SO_TO_CP_TRANSLATIONS.get(schema_org, None) or 'article-journal',
        'bibtex': SO_TO_BIB_TRANSLATIONS.get(schema_org, None) or 'misc',
        'ris': SO_TO_RIS_TRANSLATIONS.get(schema_org, None) or 'GEN'
    })

    subjects = [name_to_fos(i) for i in wrap(meta.get('keywords', None))]

    has_title = meta.get('title', None)
    if has_title is None:
        titles = [{'title': meta.get('name', None)}]
    else:
        titles = [{'title': has_title}]

    if meta.get('licenseId', None):
        rights = [dict_to_spdx({'rightsIdentifier': meta.get('licenseId')})]
    else:
        rights = None

    state = 'findable' if meta or read_options else 'not_found'

    return {
        'pid': pid,
        'doi': doi_from_url(pid),
        'url': normalize_id(meta.get('codeRepository', None)),
        'types': types,
        'identifiers': None,
        'titles': titles,
        'creators': creators,
        'contributors': contributors,
        'publisher': publisher,
        'dates': dates,
        'publication_year': publication_year,
        'descriptions': descriptions,
        'rights': rights,
        'version': meta.get('version', None),
        'subjects': subjects,
        'state': state
    } | read_options
