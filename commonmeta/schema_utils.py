"""Schema utils for commonmeta-py"""

from __future__ import annotations

from importlib.metadata import version as _package_version
from os import path
from typing import Any

import orjson as json
import xmlschema
from commonmeta_schema import schema_path as commonmeta_schema_path
from jsonschema import Draft202012Validator, ValidationError
from jsonschema.exceptions import best_match

from .base_utils import normalize_xml_dict

# Commonmeta JSON Schema version, derived from the installed commonmeta-schema
# package so it tracks the pinned dependency automatically. The version string
# (e.g. "1.0rc4") maps directly to the bundled schema file (commonmeta_v1.0rc4.json);
# commonmeta_schema_path raises FileNotFoundError if the two ever diverge.
COMMONMETA_SCHEMA_VERSION = _package_version("commonmeta-schema")


def json_schema_errors(
    instance: dict[str, Any], schema: str = "commonmeta"
) -> str | None:
    """validate against JSON schema

    Returns:
        str: Error message if validation fails
        None: If validation succeeds
    """
    # The commonmeta schema is provided by the commonmeta-schema package; the
    # remaining schemas are bundled locally under resources/.
    schema_map = {
        "cff": "cff_v1.2.0",
        "crossref_xml": "crossref-v5.5.0",
        "csl": "csl-data",
        "datacite": "datacite-v4.5",
        "inveniordm": "inveniordm-v0.1",
        "schema_org": "schema_org-v0.1",
    }
    if instance is None:
        raise ValueError("No instance provided")
    try:
        if schema != "commonmeta" and schema not in schema_map:
            raise ValueError("No schema found")

        # The Crossref JSON schema uses a normalized representation without
        # xmltodict's special keys ('@…', '#text'). Normalize instances before
        # validation to keep writer output stable while tightening the schema.
        if schema == "crossref_xml":
            instance = normalize_xml_dict(instance)

        if schema == "commonmeta":
            file_path = str(commonmeta_schema_path(COMMONMETA_SCHEMA_VERSION))
        else:
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
        # The commonmeta v1.0 schema validates an array of entities.
        # Wrap a single-record dict in a list so it passes the top-level
        # "type": "array" check.
        if schema == "commonmeta" and isinstance(instance, dict):
            instance = [instance]
        validator = Draft202012Validator(schema_definition)
        errors = list(validator.iter_errors(instance))
        if not errors:
            return None
        # anyOf's default message ("X is not valid under any of the given
        # schemas") hides the actual reason. best_match drills into the most
        # specific sub-error instead.
        error = best_match(errors)
        error_path = "/".join(str(p) for p in error.absolute_path)
        return f"{error.message} (at {error_path})" if error_path else error.message
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
        "crossref_xml": "crossref5.5.0",
    }
    if instance is None:
        raise ValueError("No instance provided")
    try:
        if schema not in schema_map:
            raise ValueError("No schema found")
        base_dir = path.join(path.dirname(__file__), "resources", "crossref")
        schema_path = path.join(base_dir, "crossref5.5.0.xsd")
        # One bundled JATS XSD imports the MathML namespace without a
        # schemaLocation; map it to the local MathML 3 schema so xmlschema
        # doesn't fall back to the (sandbox-blocked) remote URL.
        mathml_path = path.join(base_dir, "standard-modules", "mathml3", "mathml3.xsd")
        locations = {"http://www.w3.org/1998/Math/MathML": mathml_path}
        try:
            # Crossref schema 5.5.0 is XSD 1.1 (uses xsd:assert), so it must be
            # loaded with the XSD 1.1 validator. allow="sandbox" prevents network
            # access; validation="skip" skips validating the schema itself.
            schema_obj = xmlschema.XMLSchema11(
                schema_path,
                base_url=base_dir,
                locations=locations,
                allow="sandbox",
                validation="skip",
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
