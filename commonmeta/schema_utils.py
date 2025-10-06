"""Schema utils for commonmeta-py"""

from __future__ import annotations

from os import path
from typing import Any

import orjson as json
import xmlschema
from jsonschema import Draft202012Validator, ValidationError


def json_schema_errors(
    instance: dict[str, Any], schema: str = "commonmeta"
) -> str | None:
    """validate against JSON schema

    Returns:
        str: Error message if validation fails
        None: If validation succeeds
    """
    schema_map = {
        "cff": "cff_v1.2.0",
        "commonmeta": "commonmeta_v0.16",
        "crossref": "crossref-v0.2",
        "csl": "csl-data",
        "datacite": "datacite-v4.5",
        "inveniordm": "inveniordm-v0.1",
        "schema_org": "schema_org-v0.1",
    }
    if instance is None:
        raise ValueError("No instance provided")
    try:
        if schema not in schema_map:
            raise ValueError("No schema found")
        file_path = path.join(
            path.dirname(__file__), f"resources/{schema_map[schema]}.json"
        )
        try:
            with open(file_path, encoding="utf-8") as file:
                string = file.read()
                schema_definition = json.loads(string)
        except FileNotFoundError:
            raise ValueError(f"Schema file not found: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in schema file: {file_path}")
        # validate() returns None if valid, raises ValidationError if invalid
        Draft202012Validator(schema_definition).validate(instance)
        return None
    except ValidationError as error:
        return error.message


def xml_schema_errors(
    instance: str | bytes | None, schema: str = "crossref_xml"
) -> str | None:
    """validate against XML schema

    Returns:
        str: Error message if validation fails
        None: If validation succeeds
    """
    schema_map = {
        "crossref_xml": "crossref5.4.0",
    }
    if instance is None:
        raise ValueError("No instance provided")
    try:
        if schema not in schema_map:
            raise ValueError("No schema found")
        base_dir = path.join(path.dirname(__file__), "resources", "crossref")
        schema_path = path.join(base_dir, "crossref5.4.0.xsd")
        try:
            # Load schema with allow="sandbox" to prevent network access
            # and validation="skip" to skip validation of the schema itself
            schema_obj = xmlschema.XMLSchema(
                schema_path, allow="sandbox", validation="skip"
            )
        except FileNotFoundError:
            raise ValueError(f"Schema file not found: {schema_path}")
        except xmlschema.XMLSchemaException as error:
            raise ValueError(f"Invalid XML schema file: {str(error)}")
        # validate() returns None if valid, raises exception if invalid
        schema_obj.validate(instance)
        return None
    except xmlschema.validators.exceptions.XMLSchemaValidationError as error:
        return str(error)
