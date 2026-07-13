"""codemeta reader for commonmeta-py"""

from __future__ import annotations

import requests

from ..author_utils import get_authors
from ..base_utils import compact, presence, sanitize, wrap
from ..constants import (
    SO_TO_CM_TRANSLATIONS,
    Commonmeta,
)
from ..utils import (
    dict_to_spdx,
    from_schema_org_creators,
    github_as_codemeta_url,
    github_as_repo_url,
    name_to_fos,
    normalize_id,
)


def get_codemeta(pid: str, **kwargs) -> dict:
    """get_codemeta"""
    url = str(github_as_codemeta_url(pid))
    response = requests.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    data = response.json()
    if data.get("codeRepository", None) is None:
        data["codeRepository"] = github_as_repo_url(url)

    return data


def read_codemeta(data: dict | None, **kwargs) -> Commonmeta:
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

    date_published = meta.get("datePublished", None)
    date_updated = meta.get("dateModified", None)
    dates = compact({"created": meta.get("dateCreated", None)})

    publisher = {"name": meta.get("publisher", None)}

    description = (
        sanitize(str(meta.get("description")))
        if meta.get("description", None)
        else None
    )

    subjects = [name_to_fos(i) for i in wrap(meta.get("keywords", None))]

    title = meta.get("title", None) or meta.get("name", None)

    license_ = meta.get("licenseId", None)
    if license_:
        license_ = dict_to_spdx({"id": meta.get("licenseId")})

    state = "findable" if meta or read_options else "not_found"

    return {
        **{
            "id": _id,
            "type": _type,
            "contributors": presence(contributors),
            "date_published": date_published,
            "date_updated": date_updated,
            "dates": presence(dates),
            "description": description,
            "identifiers": None,
            "license": license_,
            "publisher": publisher,
            "state": state,
            "subjects": presence(subjects),
            "title": title,
            "url": normalize_id(meta.get("codeRepository", None)),
            "version": meta.get("version", None),
        },
        **read_options,
    }
