"""datacite_xml reader for Commonmeta"""
import requests
from pydash import py_

from ..base_utils import compact, wrap, presence
from ..author_utils import get_authors
from ..date_utils import strip_milliseconds
from ..doi_utils import doi_from_url, doi_as_url, datacite_api_url
from ..utils import normalize_url
from ..constants import DC_TO_CM_TRANSLATIONS, Commonmeta


def get_datacite_xml(pid: str, **kwargs) -> dict:
    """get_datacite_xml"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = datacite_api_url(doi)
    response = requests.get(url, kwargs, timeout=5)
    if response.status_code != 200:
        return {"state": "not_found"}
    return py_.get(response.json(), "data.attributes", {})


def read_datacite_xml(data: dict, **kwargs) -> Commonmeta:
    """read_datacite_xml"""

    read_options = kwargs or {}

    meta = data

    id_ = doi_as_url(meta.get("doi", None))
    resource_type_general = py_.get(meta, "types.resourceTypeGeneral")
    type_ = DC_TO_CM_TRANSLATIONS.get(resource_type_general, 'Other')
    references = wrap(meta.get("relatedItems", None) + meta.get("relatedIdentifiers", None))

    return {
        # required properties
        "id": id_,
        "type": type_,
        "doi": doi_from_url(id_) if id_ else None,
        "url": normalize_url(meta.get("url", None)),
        "creators": get_authors(wrap(meta.get("creators", None))),
        "titles": compact(meta.get("titles", None)),
        "publisher": meta.get("publisher", None),
        "publication_year": int(meta.get("publicationYear", None)),
        # recommended and optional properties
        "subjects": presence(meta.get("subjects", None)),
        "contributors": get_authors(wrap(meta.get("contributors", None))),
        "dates": presence(meta.get("dates", None))
        or [{"date": meta.get("publicationYear", None), "dateType": "Issued"}],
        "language": meta.get("language", None),
        "alternate_identifiers": presence(meta.get("alternateIdentifiers", None)),
        "sizes": presence(meta.get("sizes", None)),
        "formats": presence(meta.get("formats", None)),
        "version": meta.get("version", None),
        "rights": presence(meta.get("rights", None),),
        "descriptions": meta.get("descriptions", None),
        "geo_locations": wrap(meta.get("geoLocations", None)),
        "funding_references": meta.get("fundingReferences", None),
        "references": presence(references),
        # other properties
        "date_created": strip_milliseconds(meta.get("created", None)),
        "date_registered": strip_milliseconds(meta.get("registered", None)),
        "date_published": strip_milliseconds(meta.get("published", None)),
        "date_updated": strip_milliseconds(meta.get("updated", None)),
        "content_url": presence(meta.get("contentUrl", None)),
        "container": presence(meta.get("container", None)),
        "agency": "DataCite",
        "state": "findable",
        "schema_version": meta.get("schemaVersion", None),
    } | read_options
