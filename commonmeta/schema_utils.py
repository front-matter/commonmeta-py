"""Schema utils for commonmeta-py"""

from os import path
from typing import Any, Dict, Optional, Union

import orjson as json
import xmlschema
from jsonschema import Draft202012Validator, ValidationError


def json_schema_errors(
    instance: Dict[str, Any], schema: str = "commonmeta"
) -> Optional[str]:
    """validate against JSON schema"""
    schema_map = {
        "commonmeta": "commonmeta_v0.16",
        "datacite": "datacite-v4.5",
        "crossref": "crossref-v0.2",
        "csl": "csl-data",
        "cff": "cff_v1.2.0",
    }
    try:
        if schema not in schema_map.keys():
            raise ValueError("No schema found")
        file_path = path.join(
            path.dirname(__file__), f"resources/{schema_map[schema]}.json"
        )
        with open(file_path, encoding="utf-8") as file:
            string = file.read()
            schema = json.loads(string)
        return Draft202012Validator(schema).validate(instance)
    except ValidationError as error:
        return error.message


def xml_schema_errors(
    instance: Union[str, bytes], schema: str = "crossref_xml"
) -> Optional[Union[bool, Exception]]:
    """validate against XML schema"""
    schema_map = {
        "crossref_xml": "crossref5.4.0",
    }
    try:
        if schema not in schema_map.keys():
            raise ValueError("No schema found")
        base_dir = path.join(path.dirname(__file__), "resources", "crossref")
        schema_path = path.join(base_dir, "crossref5.4.0.xsd")
        schema_obj = xmlschema.XMLSchema(schema_path)
        return schema_obj.validate(instance)
    except xmlschema.validators.exceptions.XMLSchemaValidationError as error:
        print(error)
        return error
    # except xmlschema.exceptions.XMLSchemaException as error:
    #     print(error)
    #     print(instance)
    #     return error
    # except Exception as error:
    #     print(error)
    #     return error
