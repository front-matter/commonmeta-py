"""Metadata"""

from os import path
from typing import Optional, Union

import orjson as json
import yaml
from pydash import py_

from .base_utils import parse_xml, wrap
from .constants import CM_TO_CR_TRANSLATIONS
from .doi_utils import doi_from_url
from .readers.cff_reader import get_cff, read_cff
from .readers.codemeta_reader import (
    get_codemeta,
    read_codemeta,
)
from .readers.commonmeta_reader import read_commonmeta
from .readers.crossref_reader import (
    get_crossref,
    read_crossref,
)
from .readers.crossref_xml_reader import (
    get_crossref_xml,
    read_crossref_xml,
)
from .readers.csl_reader import read_csl
from .readers.datacite_reader import (
    get_datacite,
    read_datacite,
)
from .readers.datacite_xml_reader import read_datacite_xml
from .readers.inveniordm_reader import (
    get_inveniordm,
    read_inveniordm,
)
from .readers.json_feed_reader import get_json_feed_item, read_json_feed_item
from .readers.kbase_reader import read_kbase
from .readers.openalex_reader import (
    get_openalex,
    read_openalex,
)
from .readers.ris_reader import read_ris
from .readers.schema_org_reader import (
    get_schema_org,
    read_schema_org,
)
from .schema_utils import json_schema_errors
from .utils import find_from_format, normalize_id
from .writers.bibtex_writer import write_bibtex, write_bibtex_list
from .writers.citation_writer import write_citation, write_citation_list
from .writers.commonmeta_writer import write_commonmeta, write_commonmeta_list
from .writers.crossref_xml_writer import write_crossref_xml, write_crossref_xml_list
from .writers.csl_writer import write_csl, write_csl_list
from .writers.datacite_writer import write_datacite
from .writers.inveniordm_writer import write_inveniordm
from .writers.ris_writer import write_ris, write_ris_list
from .writers.schema_org_writer import write_schema_org


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
        """Get metadata from various sources based on pid or string input."""
        via = self.via

        # Handle pid-based metadata retrieval
        if pid is not None:
            return self._get_metadata_from_pid(pid, via)
        # Handle string-based metadata parsing
        elif string is not None:
            return self._get_metadata_from_string(string, via)

        # Default fallback
        raise ValueError("No metadata found")

    def _get_metadata_from_pid(self, pid, via) -> dict:
        """Helper method to get metadata from a PID."""
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
        elif via == "openalex":
            return get_openalex(pid)
        else:
            return {"pid": pid}

    def _get_metadata_from_string(self, string, via) -> dict:
        """Helper method to get metadata from a string."""
        try:
            # XML formats
            if via == "datacite_xml":
                result = parse_xml(string)
                if isinstance(result, (dict, list)):
                    return (
                        dict(result) if isinstance(result, dict) else {"items": result}
                    )
                return {}
            elif via == "crossref_xml":
                result = parse_xml(string, dialect="crossref")
                if isinstance(result, (dict, list)):
                    return (
                        dict(result) if isinstance(result, dict) else {"items": result}
                    )
                return {}
            # YAML and other plain text formats
            elif via == "cff":
                return dict(yaml.safe_load(string) or {})
            elif via == "bibtex":
                raise ValueError("Bibtex not supported")
            elif via == "ris":
                return {"data": string}
            # JSON-based formats
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
                "openalex",
            ]:
                return json.loads(string)
            else:
                raise ValueError("No input format found")
        except (TypeError, json.JSONDecodeError) as error:
            return {"error": str(error)}

    def read_metadata(self, data: dict, **kwargs) -> dict:
        """Read and parse metadata from various formats."""
        via = (isinstance(data, dict) and data.get("via")) or self.via

        # All these reader methods should return a dict,
        # even though some may return Commonmeta objects that can be treated as dicts
        if via == "commonmeta":
            return dict(read_commonmeta(data, **kwargs))
        elif via == "schema_org":
            return dict(read_schema_org(data))
        elif via == "datacite":
            return dict(read_datacite(data))
        elif via == "datacite_xml":
            return dict(read_datacite_xml(data))
        elif via in ["crossref", "op"]:
            return dict(read_crossref(data))
        elif via == "crossref_xml":
            return dict(read_crossref_xml(data))
        elif via == "csl":
            return dict(read_csl(data, **kwargs))
        elif via == "codemeta":
            return dict(read_codemeta(data))
        elif via == "cff":
            return dict(read_cff(data))
        elif via == "json_feed_item":
            return dict(read_json_feed_item(data, **kwargs))
        elif via == "inveniordm":
            return dict(read_inveniordm(data))
        elif via == "kbase":
            return dict(read_kbase(data))
        elif via == "openalex":
            return dict(read_openalex(data))
        elif via == "ris":
            return dict(read_ris(data["data"] if isinstance(data, dict) else data))
        else:
            raise ValueError("No input format found")

    def write(self, to: str = "commonmeta", **kwargs) -> str:
        """Convert metadata into different formats."""
        try:
            result = self._write_format(to, **kwargs)
            if result is None or result == "":
                return "{}"
            return result
        except json.JSONDecodeError as e:
            # More specific error message including the original JSONDecodeError details
            raise ValueError(f"Invalid JSON: {str(e)}")

    def _write_format(self, to: str, **kwargs) -> str:
        """Helper method to handle writing to different formats."""
        # Split the format handling into multiple methods to reduce cyclomatic complexity
        if to in ["commonmeta", "datacite", "inveniordm", "schema_org"]:
            return self._write_json_format(to)
        elif to in ["bibtex", "csl", "citation", "ris"]:
            return self._write_text_format(to, **kwargs)
        elif to in ["crossref_xml"]:
            return self._write_xml_format(to, **kwargs)
        else:
            raise ValueError("No output format found")

    def _write_json_format(self, to: str) -> str:
        """Handle JSON-based output formats."""
        if to == "commonmeta":
            result = write_commonmeta(self)
        elif to == "datacite":
            result = write_datacite(self)
        elif to == "inveniordm":
            result = write_inveniordm(self)
        elif to == "schema_org":
            result = write_schema_org(self)
        else:
            return "{}"

        if isinstance(result, str):
            # Verify it's valid JSON
            try:
                json.loads(result)
                return result
            except json.JSONDecodeError:
                return "{}"
        elif result is not None:
            try:
                decoded = result.decode("utf-8")
                # Verify it's valid JSON
                json.loads(decoded)
                return decoded
            except (json.JSONDecodeError, UnicodeDecodeError):
                return "{}"
        return "{}"

    def _write_text_format(self, to: str, **kwargs) -> str:
        """Handle text-based output formats."""
        if to == "bibtex":
            return write_bibtex(self)
        elif to == "csl":
            return self._write_csl(**kwargs)
        elif to == "citation":
            self.style = kwargs.get("style", "apa")
            self.locale = kwargs.get("locale", "en-US")
            return write_citation(self)
        elif to == "ris":
            return write_ris(self)
        return ""

    def _write_xml_format(self, to: str, **kwargs) -> str:
        """Handle XML-based output formats."""
        if to == "crossref_xml":
            return self._write_crossref_xml(**kwargs)
        return ""

    def _write_csl(self, **kwargs) -> str:
        """Write in CSL format with error checking."""
        csl_output = write_csl(self)
        if csl_output:
            instance = py_.omit(json.loads(csl_output), [])
            self.errors = json_schema_errors(instance, schema="csl")
            return csl_output
        return ""

    def _write_datacite(self) -> str:
        """Write in DataCite format with error checking."""
        datacite_output = write_datacite(self)
        if not datacite_output:
            return ""
        try:
            instance = json.loads(datacite_output)
            self.write_errors = json_schema_errors(instance, schema="datacite")
            return str(datacite_output)
        except (json.JSONDecodeError, TypeError):
            return "{}" if not datacite_output else str(datacite_output)

    def _write_crossref_xml(self, **kwargs) -> str:
        """Write in Crossref XML format with error checking."""
        doi = doi_from_url(self.id)
        _type = CM_TO_CR_TRANSLATIONS.get(str(self.type or ""), None)
        url = self.url
        instance = {"doi": doi, "type": _type, "url": url}
        self.depositor = kwargs.get("depositor", None)
        self.email = kwargs.get("email", None)
        self.registrant = kwargs.get("registrant", None)
        self.write_errors = json_schema_errors(instance, schema="crossref")
        result = write_crossref_xml(self)
        return result if result is not None else ""


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
            "openalex",
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
        elif to == "openalex":
            raise ValueError("OpenAlex not supported for metadata lists")
        elif to == "crossref_xml":
            return write_crossref_xml_list(self)
        else:
            raise ValueError("No output format found")
