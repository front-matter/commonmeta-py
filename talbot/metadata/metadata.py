"""Metadata"""
from ..readers import (
    get_crossref_json,
    read_crossref_json,
    get_datacite_json,
    read_datacite_json,
    get_schema_org,
    read_schema_org
)
from ..writers import (
    write_bibtex,
    write_citation,
    write_citeproc,
    write_ris,
    write_schema_org,
)
from ..utils import normalize_id

# pylint: disable=R0902
class Metadata:
    """Metadata"""

    def __init__(self, pid, **kwargs):
        pid = normalize_id(pid)

        if pid is None:
            raise ValueError("No PID found")
        via = kwargs.get("via", None)  # or find_from_format(id=id)
        if via == "schema_org":
            data = get_schema_org(pid)
            meta = read_schema_org(data)
        elif via == "datacite_json":
            data = get_datacite_json(pid)
            meta = read_datacite_json(data)
        else:
            data = get_crossref_json(pid)
            meta = read_crossref_json(data)
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
