"""Metadata"""

from __future__ import annotations

from os import path
from typing import Any

import orjson as json
import yaml

from .base_utils import dig, parse_xml, wrap
from .file_utils import write_output
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
from .readers.jsonfeed_reader import get_jsonfeed, read_jsonfeed
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
from .utils import find_from_format, is_chain_object, normalize_id
from .writers.bibtex_writer import write_bibtex, write_bibtex_list
from .writers.citation_writer import write_citation, write_citation_list
from .writers.commonmeta_writer import write_commonmeta, write_commonmeta_list
from .writers.crossref_xml_writer import (
    push_crossref_xml,
    push_crossref_xml_list,
    write_crossref_xml,
    write_crossref_xml_list,
)
from .writers.csl_writer import write_csl, write_csl_list
from .writers.datacite_writer import write_datacite, write_datacite_list
from .writers.inveniordm_writer import (
    push_inveniordm,
    push_inveniordm_list,
    write_inveniordm,
    write_inveniordm_list,
)
from .writers.ris_writer import write_ris, write_ris_list
from .writers.schema_org_writer import write_schema_org, write_schema_org_list


# pylint: disable=R0902
class Metadata:
    """Metadata"""

    def __init__(self, string: str | dict[str, Any] | None, **kwargs):
        self.via = kwargs.get("via", None)
        if isinstance(string, str):
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
        # if string is an InvenioRDM chain object
        elif is_chain_object(string):
            self.via = "inveniordm"
            data = getattr(string, "_child", None)
            if data is None:
                raise ValueError("No valid input found")
            parent = getattr(string, "_parent", None)
            if parent is not None and hasattr(parent, "pids"):
                kwargs["parent_doi"] = dig(parent.pids, "doi.identifier")
        elif isinstance(string, dict):
            data = string
        else:
            raise ValueError("No valid input found")

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
        self.citations = meta.get("citations")
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

        # options needed for Crossref DOI registration
        self.depositor = kwargs.get("depositor", None)
        self.email = kwargs.get("email", None)
        self.registrant = kwargs.get("registrant", None)
        self.login_id = kwargs.get("login_id", None)
        self.login_passwd = kwargs.get("login_passwd", None)
        self.test_mode = kwargs.get("test_mode", False)

        # options needed for InvenioRDM registration
        self.host = kwargs.get("host", None)
        self.token = kwargs.get("token", None)
        self.legacy_key = kwargs.get("legacy_key", None)

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

    def _get_metadata_from_pid(self, pid, via) -> dict[str, Any]:
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
        elif via == "jsonfeed":
            return get_jsonfeed(pid)
        elif via == "inveniordm":
            return get_inveniordm(pid)
        elif via == "openalex":
            return get_openalex(pid)
        else:
            return {"pid": pid}

    def _get_metadata_from_string(self, string, via) -> dict[str, Any]:
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
                "jsonfeed",
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

    def read_metadata(self, data: dict[str, Any], **kwargs) -> dict[str, Any]:
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
        elif via == "jsonfeed":
            return dict(read_jsonfeed(data, **kwargs))
        elif via == "inveniordm":
            return dict(read_inveniordm(data, **kwargs))
        elif via == "kbase":
            return dict(read_kbase(data))
        elif via == "openalex":
            return dict(read_openalex(data))
        elif via == "ris":
            return dict(read_ris(data["data"] if isinstance(data, dict) else data))
        else:
            raise ValueError("No input format found")

    def write(self, to: str = "commonmeta", **kwargs) -> bytes | None:
        """convert metadata list into different formats"""
        try:
            return self._write_format(to, **kwargs)
        except json.JSONDecodeError as e:
            # More specific error message including the original JSONDecodeError details
            raise ValueError(f"Invalid JSON: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error writing format '{to}': {str(e)}")

    def _write_format(self, to: str, **kwargs) -> bytes | None:
        """Helper method to handle writing to different formats."""
        # JSON-based output formats
        if to in ["commonmeta", "datacite", "inveniordm", "schema_org", "csl"]:
            writer_map = {
                "commonmeta": write_commonmeta,
                "datacite": write_datacite,
                "inveniordm": write_inveniordm,
                "schema_org": write_schema_org,
                "csl": write_csl,
            }
            output = writer_map[to](self)
            self.write_errors = json_schema_errors(output, schema=to)
            if self.write_errors is not None:
                self.is_valid = False
            if output is None:
                return b"{}"
            return json.dumps(output)
        # Text-based output formats
        elif to == "bibtex":
            return write_bibtex(self)
        elif to == "citation":
            self.style = kwargs.get("style", "apa")
            self.locale = kwargs.get("locale", "en-US")
            return write_citation(self)
        elif to == "ris":
            return write_ris(self)
        # XML-based output formats
        elif to == "crossref_xml":
            self.depositor = kwargs.get("depositor", None)
            self.email = kwargs.get("email", None)
            self.registrant = kwargs.get("registrant", None)
            output, self.write_errors = write_crossref_xml(self)
            if self.write_errors is not None:
                self.is_valid = False
            return output
        else:
            raise ValueError(f"Unsupported output format: {to}")

    def push(self, to: str = "commonmeta", **kwargs) -> str | dict:
        """push metadata to external APIs"""

        if to == "crossref_xml":
            response = push_crossref_xml(
                self,
                login_id=self.login_id,
                login_passwd=self.login_passwd,
                test_mode=self.test_mode,
                host=self.host,
                token=self.token,
                legacy_key=self.legacy_key,
            )
            return response
        elif to == "datacite":
            raise ValueError("Datacite not yet supported")
        elif to == "inveniordm":
            kwargs = {"legacy_key": self.legacy_key}
            response = push_inveniordm(self, host=self.host, token=self.token, **kwargs)
            return response
        else:
            raise ValueError("No valid output format found")


class MetadataList:
    """MetadataList"""

    def __init__(
        self, dct: str | bytes | dict[str, Any] | None = None, **kwargs
    ) -> None:
        if dct is None or not isinstance(dct, (str, bytes, dict)):
            raise ValueError("No input found")
        if isinstance(dct, dict):
            meta = dct
        elif isinstance(dct, list):
            meta = {"items": dct}
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
        self.login_id = kwargs.get("login_id", None)
        self.login_passwd = kwargs.get("login_passwd", None)
        self.test_mode = kwargs.get("test_mode", False)

        # options needed for InvenioRDM registration
        self.host = kwargs.get("host", None)
        self.token = kwargs.get("token", None)
        self.legacy_key = kwargs.get("legacy_key", None)

        self.items = self.read_metadata_list(wrap(meta.get("items", None)), **kwargs)
        self.errors = [i.errors for i in self.items if i.errors is not None]
        self.write_errors = [
            i.write_errors for i in self.items if i.write_errors is not None
        ]
        self.is_valid = all([i.is_valid for i in self.items])

        # other options
        self.file = kwargs.get("file", None)

    def get_metadata_list(self, string) -> dict:
        if string is None or not isinstance(string, (str, bytes)):
            raise ValueError("No input found")
        if self.via in [
            "inveniordm",
        ]:
            return {"items": json.loads(string)}
        if self.via in [
            "commonmeta",
            "crossref",
            "csl",
            "datacite",
            "jsonfeed",
            "openalex",
            "schema_org",
        ]:
            return json.loads(string)
        else:
            raise ValueError("No input format found")

    def read_metadata_list(self, items, **kwargs) -> list[Metadata]:
        """read_metadata_list"""
        kwargs["via"] = kwargs.get("via", None) or self.via
        return [Metadata(i, **kwargs) for i in items]

    def write(self, to: str = "commonmeta", **kwargs) -> str | bytes | None:
        """convert metadata list into different formats"""
        if to == "bibtex":
            output = write_bibtex_list(self)
            if self.file and output is not None:
                return write_output(self.file, output, [".bib"])
            else:
                return output
        elif to == "citation":
            output = write_citation_list(self, **kwargs)
            if self.file and output is not None:
                return write_output(self.file, output, [".html"])
            else:
                return output
        elif to == "commonmeta":
            output = json.dumps(write_commonmeta_list(self))
            if self.file:
                return write_output(self.file, output, [".json", ".jsonl"])
            else:
                return output
        elif to == "crossref_xml":
            output, self.write_errors = write_crossref_xml_list(self)
            if self.file and output is not None and self.write_errors is None:
                return write_output(self.file, output, [".xml"])
            else:
                return output
        elif to == "csl":
            output = json.dumps(write_csl_list(self))
            if self.file:
                return write_output(self.file, output, [".json"])
            else:
                return output
        elif to == "datacite":
            output = json.dumps(write_datacite_list(self))
            if self.file:
                return write_output(self.file, output, [".json"])
            else:
                return output
        elif to == "inveniordm":
            output = json.dumps(write_inveniordm_list(self))
            if self.file:
                return write_output(self.file, output, [".json"])
            else:
                return output
        elif to == "ris":
            output = write_ris_list(self)
            if self.file and output is not None:
                return write_output(self.file, output, [".ris"])
            else:
                return output
        elif to == "schema_org":
            output = json.dumps(write_schema_org_list(self))
            if self.file:
                return write_output(self.file, output, [".json"])
            else:
                return output
        else:
            raise ValueError("No valid output format found")

    def push(self, to: str = "commonmeta", **kwargs) -> bytes | None:
        """push metadata list to external APIs"""

        if to == "crossref_xml":
            response = push_crossref_xml_list(
                self,
                login_id=self.login_id,
                login_passwd=self.login_passwd,
                test_mode=self.test_mode,
                host=self.host,
                token=self.token,
                legacy_key=self.legacy_key,
            )
            return response
        elif to == "datacite":
            raise ValueError("Datacite not yet supported for metadata lists")
        elif to == "inveniordm":
            kwargs = {"legacy_key": self.legacy_key}
            response = push_inveniordm_list(
                self, host=self.host, token=self.token, **kwargs
            )
            return response
        else:
            raise ValueError("No valid output format found")
