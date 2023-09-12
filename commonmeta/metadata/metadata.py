"""Metadata"""
import os
import json
from typing import Optional, Any
from functools import cached_property
import yaml
from fastjsonschema import JsonSchemaException, compile
import xmltodict

from ..readers import (
    get_crossref,
    read_crossref,
    get_datacite,
    read_datacite,
    read_datacite_xml,
    get_crossref_xml,
    read_crossref_xml,
    get_schema_org,
    read_schema_org,
    get_codemeta,
    read_codemeta,
    read_csl,
    get_cff,
    read_cff,
    get_json_feed_item,
    read_json_feed_item,
    get_inveniordm,
    read_inveniordm,
    read_kbase,
)
from ..writers import (
    write_datacite,
    write_bibtex,
    write_citation,
    write_csl,
    write_ris,
    write_schema_org,
    write_commonmeta,
)
from ..utils import normalize_id, find_from_format


# pylint: disable=R0902
class Metadata:
    """Metadata"""

    def __init__(self, string: Optional[str], **kwargs):
        if string is None or not isinstance(string, str):
            raise ValueError("No input found")
        pid = normalize_id(string)

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
            elif via == "crossref_xml":
                data = get_crossref_xml(pid)
                meta = read_crossref_xml(data)
            elif via == "codemeta":
                data = get_codemeta(pid)
                meta = read_codemeta(data)
            elif via == "cff":
                data = get_cff(pid)
                meta = read_cff(data)
            elif via == "json_feed_item":
                data = get_json_feed_item(pid)
                meta = read_json_feed_item(data)
            elif via == "inveniordm":
                data = get_inveniordm(pid)
                meta = read_inveniordm(data)
        elif os.path.exists(string):
            with open(string, encoding="utf-8") as file:
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
            elif via == "datacite_xml":
                data = xmltodict.parse(string)
                data = json.loads(str(json.dumps(data)))
                meta = read_datacite_xml(data)
            elif via == "crossref_xml":
                data = xmltodict.parse(string)
                data = json.loads(str(json.dumps(data)))
                meta = read_crossref_xml(data)
            elif via == "csl":
                data = json.loads(string)
                meta = read_csl(data)
            elif via == "codemeta":
                data = json.loads(string)
                meta = read_codemeta(data)
            elif via == "cff":
                data = yaml.safe_load(string)
                meta = read_cff(data)
            elif via == "inveniordm":
                data = json.loads(string)
                meta = read_inveniordm(data)
            elif via == "kbase":
                data = json.loads(string)
                meta = read_kbase(data)
            # elif via == "bibtex":
            #     data = yaml.safe_load(string)
            #     meta = read_bibtex(data)
            else:
                raise ValueError("No input format found")
        else:
            raise ValueError("No metadata found")

        # required properties
        self.id = meta.get("id")  # pylint: disable=C0103
        self.type = meta.get("type")
        self.doi = meta.get("doi")
        self.url = meta.get("url")
        self.contributors = meta.get("contributors")
        self.titles = meta.get("titles")
        self.publisher = meta.get("publisher")
        self.date = meta.get("date")
        # recommended and optional properties
        self.additional_type = meta.get("additional_type")
        self.subjects = meta.get("subjects")
        self.language = meta.get("language")
        self.alternate_identifiers = meta.get("alternate_identifiers")
        self.related_identifiers = meta.get("related_identifiers")
        self.sizes = meta.get("sizes")
        self.formats = meta.get("formats")
        self.version = meta.get("version")
        self.license = meta.get("license")
        self.descriptions = meta.get("descriptions")
        self.geo_locations = meta.get("geo_locations")
        self.funding_references = meta.get("funding_references")
        self.references = meta.get("references")
        # other properties
        self.date_created = meta.get("date_created")
        self.date_registered = meta.get("date_registered")
        self.date_published = meta.get("date_published")
        self.date_updated = meta.get("date_updated")
        self.files = meta.get("files")
        self.container = meta.get("container")
        self.provider = meta.get("provider")
        self.state = meta.get("state")
        self.schema_version = meta.get("schema_version")
        # citation style language options
        self.style = kwargs.get("style", "apa")
        self.locale = kwargs.get("locale", "en-US")

    def is_valid(self) -> Any:
        """validate against JSON schema"""
        try:
            file_path = os.path.join(
                os.path.dirname(__file__), "resources/commonmeta_v0.10.1.json"
            )
            print(file_path)
            with open(file_path, encoding="utf-8") as file:
                schema = json.load(file)
            # validate = compile(schema)
            return file_path
        except JsonSchemaException as error:
            return error

    def commonmeta(self):
        """Commonmeta"""
        return write_commonmeta(self)

    def bibtex(self):
        """Bibtex"""
        return write_bibtex(self)

    def csl(self):
        """CSL-JSON"""
        return write_csl(self)

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
