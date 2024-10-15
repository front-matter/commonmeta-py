"""Schema utils for commonmeta-py"""
from os import path
import orjson as json
from jsonschema import Draft202012Validator, ValidationError


def json_schema_errors(instance, schema: str = "commonmeta"):
    """validate against JSON schema"""
    schema_map = {
        "commonmeta": "commonmeta_v0.15",
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
