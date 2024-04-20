"""cff reader for commonmeta-py"""
from typing import Optional
from urllib.parse import urlparse
import httpx
import yaml

from ..utils import (
    normalize_id,
    name_to_fos,
    dict_to_spdx,
    normalize_orcid,
    github_as_cff_url,
    github_as_repo_url,
)
from ..base_utils import compact, wrap, presence, sanitize, parse_attributes
from ..date_utils import get_iso8601_date
from ..constants import Commonmeta


def get_cff(pid: str, **kwargs) -> dict:
    """get_cff"""
    url = github_as_cff_url(pid)
    response = httpx.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    text = response.text
    repo_url = github_as_repo_url(url)
    data = yaml.safe_load(text)

    # collect metadata not included in the CFF file
    if data.get("repository-code", None) is None:
        data["repository-code"] = repo_url

    return data


def read_cff(data: Optional[dict], **kwargs) -> Commonmeta:
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

    _id = normalize_id(kwargs.get("doi", None) or meta.get("doi", None))
    # Array.wrap(meta.fetch('identifiers', nil)).find do |i|
    #                                                     i['type'] == 'doi'
    #                                                   end.fetch('value', nil))
    _type = "Software"
    url = normalize_id(meta.get("repository-code", None))
    contributors = cff_contributors(wrap(meta.get("authors", None)))

    if meta.get("title", None):
        titles = [{"title": meta.get("title", None)}]
    else:
        titles = []

    date = {
        "published": get_iso8601_date(meta.get("date-released"))
        if meta.get("date-released", None)
        else None
    }

    publisher = (
        {"name": "GitHub"} if url and urlparse(url).hostname == "github.com" else None
    )

    if meta.get("abstract", None):
        descriptions = [
            {
                "description": sanitize(meta.get("abstract")),
                "type": "Abstract",
            }
        ]
    else:
        descriptions = []

    subjects = [name_to_fos(i) for i in wrap(meta.get("keywords", None))]

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = dict_to_spdx({"id": meta.get("license")})

    references = cff_references(wrap(meta.get("references", None)))

    state = "findable" if meta or read_options else "not_found"

    return {
        "id": _id,
        "type": _type,
        # 'identifiers' => identifiers,
        "url": url,
        "titles": titles,
        "contributors": presence(contributors),
        "publisher": publisher,
        "references": presence(references),
        "date": date,
        "descriptions": presence(descriptions),
        "license": license_,
        "version": meta.get("version", None),
        "subjects": presence(subjects),
        "provider": "DataCite" if _id else "GitHub",
        "state": state,
    } | read_options


def cff_contributors(contributors):
    """cff_contributors"""

    def format_affiliation(affiliation):
        """format_affiliation"""
        if isinstance(affiliation, str):
            return {"name": affiliation}
        if isinstance(affiliation, dict):
            return compact(affiliation)
        return None
        #         if a.is_a?(Hash)
        #   a
        # elsif a.is_a?(Hash) && a.key?('#text_') && a['#text'].strip.blank?
        #   nil
        # elsif a.is_a?(Hash) && a.key?('#text')
        #   { 'name' => a['#text'] }
        # elsif a.strip.blank

    def format_element(i):
        """format_element"""
        if normalize_orcid(parse_attributes(i.get("orcid", None))):
            _id = normalize_orcid(parse_attributes(i.get("orcid", None)))
        else:
            _id = None
        if i.get("given-names", None) or i.get("family-names", None) or _id:
            given_name = parse_attributes(i.get("given-names", None))
            family_name = parse_attributes(i.get("family-names", None))
            affiliation = compact(
                [format_affiliation(a) for a in wrap(i.get("affiliation", None))]
            )

            return compact(
                {
                    "id": _id,
                    "contributorRoles": ["Author"],
                    "type": "Person",
                    "givenName": given_name,
                    "familyName": family_name,
                    "affiliation": affiliation,
                }
            )
        return {
            "contributorRoles": ["Author"],
            "type": "Organization",
            "name": i.get("name", None) or i.get("#text", None),
        }

    return [format_element(i) for i in contributors]


def cff_references(references):
    """cff_references"""

    def is_reference(i):
        """is_reference"""
        return (
            next(
                (
                    item
                    for item in wrap(i.get("identifers", None))
                    if item.get("type", None) == "doi"
                ),
                None,
            )
            is not None
        )

    def map_reference(i):
        """map_element"""
        identifier = next(
            (
                item
                for item in wrap(i.get("identifers", None))
                if item.get("type", None) == "doi"
            ),
            None,
        )
        return compact(
            {"doi": normalize_id(parse_attributes(identifier.get("value", None)))}
        )

    return [map_reference(i) for i in references if is_reference(i)]
