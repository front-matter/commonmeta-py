"""Metadata"""
from os import path
import json
from typing import Optional
from ..readers import (
    get_crossref,
    read_crossref,
    get_datacite,
    read_datacite,
    get_schema_org,
    read_schema_org,
    read_citeproc,
    read_codemeta,
)
from ..writers import (
    write_datacite,
    write_bibtex,
    write_citation,
    write_citeproc,
    write_ris,
    write_schema_org,
)
from ..utils import normalize_id, find_from_format

# pylint: disable=R0902
class Metadata:
    """Metadata"""

    def __init__(self, data: Optional[str], **kwargs):
        if data is None or not isinstance(data, str):
            raise ValueError("No metadata found")
        pid = normalize_id(data)

        if pid is not None:
            via = kwargs.get("via", None) or find_from_format(pid=pid)
            if via == "schema_org":
                data = get_schema_org(pid)
                meta = read_schema_org(data)
            elif via == "datacite":
                data = get_datacite(pid)
                meta = read_datacite(data)
            elif via == "crossref":
                data = get_crossref(pid)
                meta = read_crossref(data)
        elif path.exists(data):
            with open(data, encoding='utf-8') as file:
                string = file.read()
            via = kwargs.get("via", None) or find_from_format(string=string)
            if via == "schema_org":
                data = json.loads(string)
                meta = read_schema_org(data)
            elif via == "datacite":
                data = json.loads(string)
                meta = read_datacite(data)
            elif via == "crossref":
                data = json.loads(string)
                meta = read_crossref(data)
            elif via == "citeproc":
                data = json.loads(string)
                meta = read_citeproc(data)
            elif via == "codemeta":
                data = json.loads(string)
                meta = read_codemeta(data)
            else:
                raise ValueError("No input format found")
        else:
            raise ValueError("No metadata found")

        # required properties
        self.pid = meta.get("pid")
        self.doi = meta.get("doi")
        self.url = meta.get("url")
        self.creators = meta.get("creators")
        self.titles = meta.get("titles")
        self.publisher = meta.get("publisher")
        self.publication_year = meta.get("publication_year")
        self.types = meta.get("types")
        # recommended and optional properties
        self.subjects = meta.get("subjects")
        self.contributors = meta.get("contributors")
        self.dates = meta.get("dates")
        self.language = meta.get("language")
        self.alternate_identifiers = meta.get("alternate_identifiers")
        self.sizes = meta.get("sizes")
        self.formats = meta.get("formats")
        self.version = meta.get("version")
        self.rights = meta.get("rights")
        self.descriptions = meta.get("descriptions")
        self.geo_locations = meta.get("geo_locations")
        self.funding_references = meta.get("funding_references")
        self.related_items = meta.get("related_items")
        # other properties
        self.date_created = meta.get("date_created")
        self.date_registered = meta.get("date_registered")
        self.date_published = meta.get("date_published")
        self.date_updated = meta.get("date_updated")
        self.content_url = meta.get("content_url")
        self.container = meta.get("container")
        self.agency = meta.get("agency")
        self.state = meta.get("state")
        self.schema_version = meta.get("schema_version")
        # citation style language options
        self.style = kwargs.get("style", "apa")
        self.locale = kwargs.get("locale", "en-US")

    def bibtex(self):
        """Bibtex"""
        return write_bibtex(self)

    def citeproc(self):
        """Citeproc"""
        return write_citeproc(self)

    def citation(self):
        """Citation"""
        return write_citation(self)

    def ris(self):
        """RIS"""
        return write_ris(self)

    def schema_org(self):
        """Schema.org"""
        return write_schema_org(self)

    def datacite(self):
        """Datacite"""
        return write_datacite(self)
