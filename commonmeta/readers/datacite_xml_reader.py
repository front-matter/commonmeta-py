"""datacite_xml reader for Commonmeta"""
import requests
from pydash import py_

from ..doi_utils import doi_from_url, datacite_api_url
from ..constants import Commonmeta


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
