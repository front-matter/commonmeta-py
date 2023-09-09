"""JSON Feed reader for commonmeta-py"""
from typing import Optional

from ..utils import compact, normalize_url
from ..date_utils import get_date_from_parts
from ..doi_utils import normalize_doi, doi_from_url
from ..constants import (
    RIS_TO_CM_TRANSLATIONS,
    Commonmeta
)


def get_json_feed_item(pid: str, **kwargs) -> dict:
    """get_json_feed_item"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = crossref_api_url(doi)
    response = requests.get(url, kwargs, timeout=10)
    if response.status_code != 200:
        return {"state": "not_found"}
    return response.json().get("message", {})


def read_json_feed_item(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_json_feed_item"""
    if data is None:
        return {"state": "not_found"}
    meta = data

    # read_options = ActiveSupport::HashWithIndifferentAccess.
    # new(options.except(:doi, :id, :url,
    # :sandbox, :validate, :ra))
    read_options = kwargs or {}

    doi = meta.get("DOI", None)
    id_ = doi_as_url(doi)
    resource_type = meta.get("type", {}).title().replace("-", "")
    type_ = CR_TO_CM_TRANSLATIONS.get(resource_type, "Other")

    if meta.get("author", None):
        contributors = get_authors(from_csl(wrap(meta.get("author"))))
    else:
        contributors = None

    def editor_type(item):
        item["contributorType"] = "Editor"
        return item

    editors = [editor_type(i) for i in wrap(meta.get("editor", None))]
    if editors:
        contributors += get_authors(from_csl(editors))

    url = normalize_url(py_.get(meta, "resource.primary.URL"))
    titles = get_titles(meta)

    member_id = meta.get("member", None)
    # TODO: get publisher from member_id almost always return publisher name, but sometimes does not
    if member_id is not None:
        publisher = get_crossref_member(member_id)
    else:
        publisher = meta.get("publisher", None)

    date: dict = {}
    date["submitted"] = None
    date["accepted"] = py_.get(meta, "accepted.date-time")
    date["published"] = (
        py_.get(meta, "issued.date-time")
        or get_date_from_date_parts(meta.get("issued", None))
        or py_.get(meta, "created.date-time")
    )
    date["updated"] = py_.get(meta, "updated.date-time") or py_.get(
        meta, "deposited.date-time"
    )

    license_ = meta.get("license", None)
    if license_ is not None:
        license_ = normalize_cc_url(license_[0].get("URL", None))
        license_ = dict_to_spdx({"url": license_}) if license_ else None

    container = get_container(meta, resource_type=resource_type)

    references = references = [
        get_reference(i) for i in wrap(meta.get("reference", None))
    ]
    funding_references = from_crossref_funding(wrap(meta.get("funder", None)))

    description = meta.get("abstract", None)
    if description is not None:
        descriptions = [
            {"description": sanitize(description), "descriptionType": "Abstract"}
        ]
    else:
        descriptions = None

    state = "findable" if meta or read_options else "not_found"
    subjects = [{"subject": i} for i in wrap(meta.get("subject", []))]

    return {
        # required properties
        "id": id_,
        "type": type_,
        "url": url,
        "contributors": contributors,
        "titles": presence(titles),
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional properties
        "subjects": presence(subjects),
        "language": meta.get("language", None),
        "alternate_identifiers": None,
        "sizes": None,
        "formats": None,
        "version": meta.get("version", None),
        "license": license_,
        "descriptions": descriptions,
        "geo_locations": None,
        "funding_references": presence(funding_references),
        "references": references,
        # other properties
        "content_url": presence(meta.get("contentUrl", None)),
        "container": presence(container),
        "provider": get_doi_ra(id_),
        "state": state,
        "schema_version": None,
    } | read_options
