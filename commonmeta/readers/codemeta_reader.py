"""codemeta reader for commonmeta-py"""
from typing import Optional
from collections import defaultdict
import httpx

from ..utils import (
    normalize_id,
    from_schema_org_creators,
    name_to_fos,
    dict_to_spdx,
    github_as_codemeta_url,
    github_as_repo_url,
    doi_from_url,
)
from ..base_utils import wrap, presence, compact, sanitize
from ..author_utils import get_authors
from ..constants import (
    Commonmeta,
    SO_TO_CM_TRANSLATIONS,
)


def get_codemeta(pid: str, **kwargs) -> dict:
    """get_codemeta"""
    url = str(github_as_codemeta_url(pid))
    response = httpx.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    data = response.json()
    if data.get("codeRepository", None) is None:
        data["codeRepository"] = github_as_repo_url(url)

    return data


def read_codemeta(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_codemeta"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    read_options = kwargs or {}
    # ActiveSupport: : HashWithIndifferentAccess.new(options.except(: doi, : id, : url,
    # : sandbox, : validate, : ra)

    _id = normalize_id(meta.get("id", None) or meta.get("identifier", None))
    # id = normalize_id(options[:doi] | | meta.get('@id', None) | | meta.get('identifier', None))
    _type = SO_TO_CM_TRANSLATIONS.get(meta.get("@type", "Software"))
    # identifiers = Array.wrap(meta.get('identifier', None)).map do | r|
    #   r = normalize_id(r) if r.is_a?(String)
    #   if r.is_a?(String) & & URI(r) != 'doi.org'
    #     {'identifierType': 'URL', 'identifier': r}
    #   elsif r.is_a?(Hash)
    #     {'identifierType': get_identifier_type(
    #         r['propertyID']), 'identifier': r['value']}
    #   end
    # end.compact.uniq

    has_agents = meta.get("agents", None)
    authors = meta.get("authors", None) if has_agents is None else has_agents
    contributors = get_authors(from_schema_org_creators(wrap(authors)))
    contrib = get_authors(from_schema_org_creators(wrap(meta.get("editor", None))))
    if contrib:
        contributors += contrib
    date: dict = defaultdict(list)
    date["created"] = meta.get("dateCreated", None)
    date["published"] = meta.get("datePublished", None)
    date["updated"] = meta.get("dateModified", None)

    publisher = {"name": meta.get("publisher", None)}

    if meta.get("description", None):
        descriptions = [
            {
                "description": sanitize(str(meta.get("description"))),
                "descriptionType": "Abstract",
            }
        ]
    else:
        descriptions = None

    subjects = [name_to_fos(i) for i in wrap(meta.get("keywords", None))]

    has_title = meta.get("title", None)
    if has_title is None:
        titles = [{"title": meta.get("name", None)}]
    else:
        titles = [{"title": has_title}]

    license_ = meta.get("licenseId", None)
    if license_:
        license_ = dict_to_spdx({"id": meta.get("licenseId")})

    provider = "DataCite" if doi_from_url(_id) else "GitHub"
    state = "findable" if meta or read_options else "not_found"

    return {
        "id": _id,
        "type": _type,
        "url": normalize_id(meta.get("codeRepository", None)),
        "identifiers": None,
        "titles": titles,
        "contributors": presence(contributors),
        "publisher": publisher,
        "date": compact(date),
        "descriptions": descriptions,
        "license": license_,
        "version": meta.get("version", None),
        "subjects": presence(subjects),
        "provider": provider,
        "state": state,
    } | read_options
