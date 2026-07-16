"""Schema utils for commonmeta-py"""

from __future__ import annotations

from functools import lru_cache
from os import path
from typing import Any

import orjson as json

from .base_utils import normalize_xml_dict

# jsonschema and xmlschema are imported inside the functions that use them, not
# at module scope: between them they cost ~0.7s of `import commonmeta` (jsonschema
# alone is 607ms, most of it rfc3987_syntax), and neither is needed to read or
# write metadata - only to validate it. Python caches modules in sys.modules, so
# the in-function import is a dict lookup after the first call.

# The Commonmeta JSON Schema version this package targets. This is the *schema*
# version, not the version of the commonmeta-schema distribution that publishes
# it: that distribution is on a release train (1.0rc8) while the schema it
# encodes is 1.0. Every snapshot pins `schema_version` to the stable const
# "https://commonmeta.org/commonmeta_v1.0.json", so records declare 1.0
# regardless of which rc shipped them - which is why this is a fixed "1.0"
# rather than derived from the installed distribution version, where it would
# churn on every rc bump.
COMMONMETA_SCHEMA_VERSION = "1.0"

# The `schema_version` value stamped onto every work written as commonmeta, and
# the const the schema pins that property to. Only works carry it: the person
# and organization definitions don't define the property, and set
# additionalProperties: false.
COMMONMETA_SCHEMA_URI = (
    f"https://commonmeta.org/commonmeta_v{COMMONMETA_SCHEMA_VERSION}.json"
)


# JSON schemas bundled under resources/, by the format name callers pass.
# commonmeta_v1.0.json is a copy of the canonical schema published by the
# commonmeta-schema package; test-schema_utils.py asserts the two are identical,
# so a bump of the pinned commonmeta-schema that isn't mirrored here fails CI
# rather than drifting silently.
_SCHEMA_MAP = {
    "commonmeta": f"commonmeta_v{COMMONMETA_SCHEMA_VERSION}",
    "cff": "cff_v1.2.0",
    "crossref_xml": "crossref-v5.5.0",
    "csl": "csl-data",
    "datacite": "datacite-v4.5",
    "inveniordm": "inveniordm-v0.1",
    "schema_org": "schema_org-v0.1",
}


def schema_file_path(schema: str) -> str:
    """The path to a bundled JSON schema file."""
    return path.join(path.dirname(__file__), f"resources/{_SCHEMA_MAP[schema]}.json")


@lru_cache(maxsize=None)
def _schema_definition(schema: str) -> dict:
    """Read, parse and cache the JSON Schema definition for `schema`.

    Without this the schema file is re-read and re-parsed for every record
    validated.
    """
    file_path = schema_file_path(schema)
    try:
        with open(file_path, encoding="utf-8") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        raise ValueError(f"Schema file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in schema file: {file_path}")


@lru_cache(maxsize=1)
def _use_jsonschema_rs() -> bool:
    """Whether the Rust-backed validator is available.

    jsonschema-rs requires Python 3.10+, so it is a conditional dependency and
    3.9 falls back to the pure-Python jsonschema. It wraps the same Rust crate
    commonmeta-rs validates with, and is ~56x faster on the commonmeta schema —
    a top-level oneOf over work/person/organization with heavy $ref nesting is
    close to the worst case for a pure-Python validator.
    """
    try:
        import jsonschema_rs  # noqa: F401
    except ImportError:
        return False
    return True


@lru_cache(maxsize=None)
def _json_validator(schema: str):
    """Build and cache the validator for `schema`.

    Both validators are stateless, so one per schema lasts the process.
    """
    schema_definition = _schema_definition(schema)
    if _use_jsonschema_rs():
        import jsonschema_rs

        return jsonschema_rs.validator_for(schema_definition)
    from jsonschema import Draft202012Validator

    return Draft202012Validator(schema_definition)


def json_schema_errors(
    instance: dict[str, Any], schema: str = "commonmeta"
) -> str | None:
    """validate against JSON schema

    Returns:
        str: Error message if validation fails
        None: If validation succeeds
    """
    if instance is None:
        raise ValueError("No instance provided")
    if schema not in _SCHEMA_MAP:
        raise ValueError("No schema found")

    # The Crossref JSON schema uses a normalized representation without
    # xmltodict's special keys ('@…', '#text'). Normalize instances before
    # validation to keep writer output stable while tightening the schema.
    if schema == "crossref_xml":
        instance = normalize_xml_dict(instance)

    # The commonmeta v1.0 schema validates an array of entities.
    # Wrap a single-record dict in a list so it passes the top-level
    # "type": "array" check.
    if schema == "commonmeta" and isinstance(instance, dict):
        instance = [instance]

    validator = _json_validator(schema)
    if _use_jsonschema_rs():
        # is_valid() short-circuits on the first failure and skips building the
        # error, which is the common (valid) path.
        if validator.is_valid(instance):
            return None
        error = next(iter(validator.iter_errors(instance)), None)
        if error is None:
            return None
        error_path = "/".join(str(p) for p in error.instance_path)
        return f"{error.message} (at {error_path})" if error_path else error.message

    from jsonschema import ValidationError
    from jsonschema.exceptions import best_match

    try:
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


@lru_cache(maxsize=None)
def _xml_schema(schema: str):
    """Build and cache the XSD validator for `schema`.

    Constructing an XMLSchema11 parses the Crossref XSD and everything it
    imports (JATS, MathML), which takes ~1.1s. It is immutable once built and
    xmlschema's validate() is stateless, so the object is cached for the life of
    the process: a batch deposit paid that cost per record before this.
    """
    import xmlschema

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
        return xmlschema.XMLSchema11(
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


def xml_schema_errors(
    instance: str | bytes | None, schema: str = "crossref_xml"
) -> str | None:
    """validate against XML schema

    Returns:
        str: Error message if validation fails
        None: If validation succeeds
    """
    import xmlschema

    schema_map = {
        "crossref_xml": "crossref5.5.0",
    }
    if instance is None:
        raise ValueError("No instance provided")
    try:
        if schema not in schema_map:
            raise ValueError("No schema found")
        schema_obj = _xml_schema(schema)
        # validate() returns None if valid, raises exception if invalid
        schema_obj.validate(instance)
        return None
    except xmlschema.validators.exceptions.XMLSchemaValidationError as error:
        return str(error)
