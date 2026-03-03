from commonmeta.jsonschema_generator import generate_jsonschema


def test_generate_jsonschema_crossref_xml():
    schema = generate_jsonschema("crossref_xml")
    assert schema["$schema"].startswith("http")
    assert schema["$ref"] == "#/definitions/CrossrefXMLSchema"
    assert "definitions" in schema
    assert "CrossrefXMLSchema" in schema["definitions"]

    root = schema["definitions"]["CrossrefXMLSchema"]
    assert root["type"] == "object"
    assert "properties" in root
    # spot-check a few known Crossref writer keys
    assert "journal" in root["properties"]
    assert "posted_content" in root["properties"]
