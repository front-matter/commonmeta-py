# pylint: disable=invalid-name
"""Test schema_utils"""

import json

import pytest
from commonmeta_schema import schema_path

from commonmeta.schema_utils import (
    _SCHEMA_MAP,
    COMMONMETA_SCHEMA_URI,
    COMMONMETA_SCHEMA_VERSION,
    json_schema_errors,
    schema_file_path,
)


def test_bundled_commonmeta_schema_matches_canonical():
    """The copy under resources/ must match the schema published by the pinned
    commonmeta-schema package.

    The copy exists so the code reads every schema the same way, out of
    resources/. That is only safe if drift is caught: without this test, bumping
    commonmeta-schema would silently leave commonmeta-py validating against the
    old schema.
    """
    bundled = json.loads(open(schema_file_path("commonmeta"), encoding="utf-8").read())
    canonical = json.loads(
        open(schema_path(COMMONMETA_SCHEMA_VERSION), encoding="utf-8").read()
    )
    assert bundled == canonical, (
        "commonmeta/resources/commonmeta_v1.0.json is out of date with the "
        "pinned commonmeta-schema package. Re-copy it from "
        f"{schema_path(COMMONMETA_SCHEMA_VERSION)}"
    )


def test_schema_uri_matches_bundled_schema():
    """The stamped schema_version must be the const the schema pins it to."""
    bundled = json.loads(open(schema_file_path("commonmeta"), encoding="utf-8").read())
    const = bundled["$defs"]["work"]["properties"]["schema_version"]["const"]
    assert const == COMMONMETA_SCHEMA_URI
    assert bundled["$id"] == COMMONMETA_SCHEMA_URI


@pytest.mark.parametrize("schema", sorted(_SCHEMA_MAP))
def test_every_mapped_schema_is_bundled(schema):
    """Every schema the map names resolves to a file that parses."""
    definition = json.loads(open(schema_file_path(schema), encoding="utf-8").read())
    assert isinstance(definition, dict)


def test_unknown_schema_rejected():
    """An unmapped schema name is an error, not a missing-file traceback."""
    with pytest.raises(ValueError, match="No schema found"):
        json_schema_errors({"id": "https://doi.org/10.5555/x"}, "nonesuch")


def test_no_instance_rejected():
    with pytest.raises(ValueError, match="No instance provided"):
        json_schema_errors(None)


def test_crossref_body_schema_names_the_field():
    """The Crossref 5.5.0 deposit body schema takes xmltodict's '@' attributes
    and '#text', and its error names the field rather than the anyOf around
    every element."""
    body = {
        "journal": {
            "journal_metadata": {"full_title": "eLife"},
            "journal_article": {
                "titles": {"title": {"#text": "A Title"}},
                "publication_date": {"year": "2024"},
                "archive_locations": [{"archive": {"@name": "CLOCKSS"}}],
                "doi_data": {"doi": "10.5555/x", "resource": "https://example.org"},
            },
        }
    }
    errors = json_schema_errors(body, schema="crossref_xml")
    assert errors == (
        "[{'archive': {'@name': 'CLOCKSS'}}] is not of type 'object' "
        "(at journal/journal_article/archive_locations)"
    )
    body["journal"]["journal_article"]["archive_locations"] = {
        "archive": [{"@name": "CLOCKSS"}, {"@name": "Portico"}]
    }
    assert json_schema_errors(body, schema="crossref_xml") is None
    # text is '#text' (DOM, xmltodict), not quick-xml's '$text'
    body["journal"]["journal_article"]["titles"] = {"title": {"$text": "A Title"}}
    assert json_schema_errors(body, schema="crossref_xml") is not None


@pytest.mark.parametrize(
    "publisher,valid",
    [
        ({"name": "Example Press"}, True),
        (
            {
                "name": "Example Press",
                "publisherIdentifier": "https://ror.org/04wxnsj81",
                "publisherIdentifierScheme": "ROR",
                "schemeUri": "https://ror.org/",
            },
            True,
        ),
        ({"name": "Example Press", "geo_locations": [{"place": "Cham"}]}, False),
    ],
)
def test_datacite_4_7_publisher(publisher, valid):
    record = {
        "doi": "10.5555/x",
        "creators": [{"name": "Example Institute"}],
        "titles": [{"title": "A Title"}],
        "publisher": publisher,
        "publicationYear": "2024",
        "types": {"resourceTypeGeneral": "Report"},
    }
    assert (json_schema_errors(record, schema="datacite") is None) is valid
