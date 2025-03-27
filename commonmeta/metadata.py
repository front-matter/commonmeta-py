"""Metadata"""

from os import path
import orjson as json
from typing import Optional, Union
import yaml
from pydash import py_

from .readers.crossref_reader import (
    get_crossref,
    read_crossref,
)
from .readers.datacite_reader import (
    get_datacite,
    read_datacite,
)
from .readers.datacite_xml_reader import read_datacite_xml
from .readers.crossref_xml_reader import (
    get_crossref_xml,
    read_crossref_xml,
)
from .readers.schema_org_reader import (
    get_schema_org,
    read_schema_org,
)
from .readers.codemeta_reader import (
    get_codemeta,
    read_codemeta,
)
from .readers.csl_reader import read_csl
from .readers.cff_reader import get_cff, read_cff
from .readers.json_feed_reader import get_json_feed_item, read_json_feed_item
from .readers.inveniordm_reader import (
    get_inveniordm,
    read_inveniordm,
)
from .readers.kbase_reader import read_kbase
from .readers.commonmeta_reader import read_commonmeta
from .readers.ris_reader import read_ris
from .writers.datacite_writer import write_datacite
from .writers.bibtex_writer import write_bibtex, write_bibtex_list
from .writers.citation_writer import write_citation, write_citation_list
from .writers.crossref_xml_writer import write_crossref_xml, write_crossref_xml_list
from .writers.csl_writer import write_csl, write_csl_list
from .writers.ris_writer import write_ris, write_ris_list
from .writers.schema_org_writer import write_schema_org
from .writers.commonmeta_writer import write_commonmeta, write_commonmeta_list
from .writers.inveniordm_writer import write_inveniordm
from .utils import normalize_id, find_from_format
from .base_utils import parse_xml, wrap
from .doi_utils import doi_from_url
from .schema_utils import json_schema_errors
from .constants import CM_TO_CR_TRANSLATIONS


# pylint: disable=R0902
class Metadata:
    """Metadata"""

    def __init__(self, string: Optional[Union[str, dict]], **kwargs):
        if string is None or not isinstance(string, (str, dict)):
            raise ValueError("No input found")
        self.via = kwargs.get("via", None)
        if isinstance(string, dict):
            data = string
        elif isinstance(string, str):
            pid = normalize_id(string)
            if pid is not None and self.via is None:
                self.via = find_from_format(pid=pid)
            elif path.exists(string):
                with open(string, encoding="utf-8") as file:
                    string = file.read()
                if self.via is None:
                    self.via = find_from_format(string=string)
            if self.via is None:
                self.via = "commonmeta"
            data = self.get_metadata(pid=pid, string=string)
        meta = self.read_metadata(data=data, **kwargs)

        # required properties
        self.id = meta.get("id")  # pylint: disable=C0103
        self.type = meta.get("type")
        # recommended and optional properties
        self.additional_type = meta.get("additionalType")
        self.archive_locations = meta.get("archiveLocations")
        self.container = meta.get("container")
        self.contributors = meta.get("contributors")
        self.date = meta.get("date")
        self.descriptions = meta.get("descriptions")
        self.files = meta.get("files")
        self.funding_references = meta.get("fundingReferences")
        self.geo_locations = meta.get("geoLocations")
        self.identifiers = meta.get("identifiers")
        self.language = meta.get("language")
        self.license = meta.get("license")
        self.provider = meta.get("provider")
        self.publisher = meta.get("publisher")
        self.references = meta.get("references")
        self.relations = meta.get("relations")
        self.subjects = meta.get("subjects")
        self.titles = meta.get("titles")
        self.url = meta.get("url")
        self.version = meta.get("version")
        self.content = meta.get("content")
        self.image = meta.get("image")
        # other properties
        self.date_created = meta.get("date_created")
        self.date_registered = meta.get("date_registered")
        self.date_published = meta.get("date_published")
        self.date_updated = meta.get("date_updated")
        self.state = meta.get("state")

        # Catch errors in the reader, then validate against JSON schema for Commonmeta
        self.errors = meta.get("errors", None) or json_schema_errors(
            json.loads(self.write())
        )
        self.write_errors = None
        self.is_valid = (
            meta.get("state", None) not in ["not_found", "forbidden", "bad_request"]
            and self.errors is None
            and self.write_errors is None
        )

    def get_metadata(self, pid, string) -> dict:
        via = self.via
        if pid is not None:
            if via == "schema_org":
                return get_schema_org(pid)
            elif via == "datacite":
                return get_datacite(pid)
            elif via in ["crossref", "op"]:
                return get_crossref(pid)
            elif via == "crossref_xml":
                return get_crossref_xml(pid)
            elif via == "codemeta":
                return get_codemeta(pid)
            elif via == "cff":
                return get_cff(pid)
            elif via == "json_feed_item":
                return get_json_feed_item(pid)
            elif via == "inveniordm":
                return get_inveniordm(pid)
        elif string is not None:
            if via == "datacite_xml":
                return parse_xml(string)
            elif via == "crossref_xml":
                return parse_xml(string, dialect="crossref")
            elif via == "cff":
                return yaml.safe_load(string)
            elif via == "bibtex":
                raise ValueError("Bibtex not supported")
            elif via == "ris":
                return string
            elif via in [
                "commonmeta",
                "crossref",
                "datacite",
                "schema_org",
                "csl",
                "json_feed_item",
                "codemeta",
                "kbase",
                "inveniordm",
            ]:
                return json.loads(string)
            else:
                raise ValueError("No input format found")
        else:
            raise ValueError("No metadata found")

    def read_metadata(self, data: dict, **kwargs) -> dict:
        """get_metadata"""
        via = isinstance(data, dict) and data.get("via", None) or self.via
        if via == "commonmeta":
            return read_commonmeta(data, **kwargs)
        elif via == "schema_org":
            return read_schema_org(data)
        elif via == "datacite":
            return read_datacite(data)
        elif via == "datacite_xml":
            return read_datacite_xml(data)
        elif via in ["crossref", "op"]:
            return read_crossref(data)
        elif via == "crossref_xml":
            return read_crossref_xml(data)
        elif via == "csl":
            return read_csl(data, **kwargs)
        elif via == "codemeta":
            return read_codemeta(data)
        elif via == "cff":
            return read_cff(data)
        elif via == "json_feed_item":
            return read_json_feed_item(data, **kwargs)
        elif via == "inveniordm":
            return read_inveniordm(data)
        elif via == "kbase":
            return read_kbase(data)
        elif via == "ris":
            return read_ris(data)
        else:
            raise ValueError("No input format found")

    def write(self, to: str = "commonmeta", **kwargs) -> str:
        """convert metadata into different formats"""
        try:
            if to == "commonmeta":
                return write_commonmeta(self)
            elif to == "bibtex":
                return write_bibtex(self)
            elif to == "csl":
                instance = py_.omit(json.loads(write_csl(self)), [])
                self.errors = json_schema_errors(instance, schema="csl")
                return write_csl(self)
            elif to == "citation":
                self.style = kwargs.get("style", "apa")
                self.locale = kwargs.get("locale", "en-US")
                return write_citation(self)
            elif to == "ris":
                return write_ris(self)
            elif to == "schema_org":
                return write_schema_org(self)
            elif to == "inveniordm":
                return write_inveniordm(self)
            elif to == "datacite":
                instance = json.loads(write_datacite(self))
                self.write_errors = json_schema_errors(instance, schema="datacite")
                print(self.write_errors)
                return write_datacite(self)
            elif to == "crossref_xml":
                doi = doi_from_url(self.id)
                _type = CM_TO_CR_TRANSLATIONS.get(self.type, None)
                url = self.url
                instance = {"doi": doi, "type": _type, "url": url}
                self.depositor = kwargs.get("depositor", None)
                self.email = kwargs.get("email", None)
                self.registrant = kwargs.get("registrant", None)
                self.write_errors = json_schema_errors(instance, schema="crossref")
                return write_crossref_xml(self)
            else:
                raise ValueError("No output format found")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON")


class MetadataList:
    """MetadataList"""

    def __init__(
        self, dct: Optional[Union[str, dict]] = None, **kwargs
    ) -> Optional[dict]:
        if dct is None or not isinstance(dct, (str, bytes, dict)):
            raise ValueError("No input found")
        if isinstance(dct, dict):
            meta = dct
        elif isinstance(dct, (str, bytes)):
            if path.exists(dct):
                with open(dct, encoding="utf-8") as file:
                    dct = file.read()
            self.via = kwargs.get("via", None) or find_from_format(string=dct)
            meta = self.get_metadata_list(dct)

        self.id = meta.get("id", None)
        self.type = meta.get("type", None)
        self.title = meta.get("title", None)
        self.description = meta.get("description", None)

        # options needed for Crossref DOI registration
        self.depositor = kwargs.get("depositor", None)
        self.email = kwargs.get("email", None)
        self.registrant = kwargs.get("registrant", None)

        self.items = self.read_metadata_list(wrap(meta.get("items", None)), **kwargs)
        self.errors = [i.errors for i in self.items if i.errors is not None]
        self.write_errors = [
            i.write_errors for i in self.items if i.write_errors is not None
        ]
        self.is_valid = all([i.is_valid for i in self.items])

        # other options
        self.jsonlines = kwargs.get("jsonlines", False)
        self.filename = kwargs.get("filename", None)

    def get_metadata_list(self, string) -> list:
        if string is None or not isinstance(string, (str, bytes)):
            raise ValueError("No input found")
        if self.via in [
            "commonmeta",
            "crossref",
            "datacite",
            "schema_org",
            "csl",
            "json_feed_item",
        ]:
            return json.loads(string)
        else:
            raise ValueError("No input format found")

    def read_metadata_list(self, data: list, **kwargs) -> list:
        """read_metadata_list"""
        kwargs["via"] = kwargs.get("via", None) or self.via
        return [Metadata(i, **kwargs) for i in data]

    def write(self, to: str = "commonmeta", **kwargs) -> str:
        """convert metadata list into different formats"""
        if to == "commonmeta":
            return write_commonmeta_list(self)
        elif to == "bibtex":
            return write_bibtex_list(self)
        elif to == "csl":
            return write_csl_list(self)
        elif to == "citation":
            return write_citation_list(self, **kwargs)
        elif to == "ris":
            return write_ris_list(self)
        elif to == "schema_org":
            raise ValueError("Schema.org not supported for metadata lists")
        elif to == "datacite":
            raise ValueError("Datacite not supported for metadata lists")
        elif to == "crossref_xml":
            return write_crossref_xml_list(self)
        else:
            raise ValueError("No output format found")
