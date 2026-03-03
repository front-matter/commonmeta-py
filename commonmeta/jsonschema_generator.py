"""Generate JSON Schema documents for Marshmallow schemas.

We keep this isolated from the core library logic: Commonmeta already ships
hand-authored JSON Schemas under `commonmeta/resources/` for validation.

Note: `marshmallow-jsonschema` (0.13.0) imports `pkg_resources` at import time.
`pkg_resources` (from setuptools) is deprecated and may be absent in modern
environments. To avoid adding setuptools just for this, we install a minimal
runtime shim for `pkg_resources.get_distribution` before importing the library.
"""

from __future__ import annotations

import importlib.metadata
import sys
import types
from typing import Any

from marshmallow import Schema


def _install_pkg_resources_shim() -> None:
    """Install a minimal `pkg_resources` shim into `sys.modules`.

    `marshmallow-jsonschema` only uses `pkg_resources.get_distribution(...).version`
    to populate `__version__`.
    """

    if "pkg_resources" in sys.modules:
        return

    shim = types.ModuleType("pkg_resources")

    def get_distribution(dist_name: str):
        try:
            version = importlib.metadata.version(dist_name)
        except importlib.metadata.PackageNotFoundError:
            version = "0.0.0"
        return types.SimpleNamespace(version=version)

    shim.get_distribution = get_distribution  # type: ignore[attr-defined]
    sys.modules["pkg_resources"] = shim


def marshmallow_to_jsonschema(schema: Schema) -> dict[str, Any]:
    """Convert a Marshmallow `Schema` instance to a JSON Schema dict."""

    _install_pkg_resources_shim()

    from marshmallow_jsonschema import JSONSchema

    base: dict[str, Any] = JSONSchema().dump(schema)
    # marshmallow-jsonschema doesn't add the $schema keyword; add it for clarity.
    return {"$schema": "http://json-schema.org/draft-07/schema#", **base}


def generate_jsonschema(name: str) -> dict[str, Any]:
    """Generate a JSON Schema by symbolic name.

    Currently supported:
    - `crossref_xml`: the pre-serialization Crossref writer dict.
    """

    if name == "crossref_xml":
        from .writers.crossref_xml_writer import CrossrefXMLSchema

        schema = marshmallow_to_jsonschema(CrossrefXMLSchema())
        # Match existing resource naming and intent.
        schema["$id"] = "crossref-v5.4.0.json"
        schema["title"] = "Crossref XML Writer v5.4.0"
        schema["description"] = (
            "JSON Schema for validating output before converting to Crossref XML."
        )
        return schema

    raise ValueError(f"Unknown schema: {name}")
