# pylint: disable=invalid-name
"""Schema-validation conformance ported from commonmeta-rs
(tests/schema_utils_conformance.rs).

Selected commonmeta fixtures are validated against the commonmeta JSON schema.
"""

import json

import pytest
from conformance_common import fixture_path, read_text

from commonmeta.schema_utils import json_schema_errors

CASES = [
    ("journal_article.json", True),
    ("blog_post_1.json", True),
]


@pytest.mark.parametrize("name,should_validate", CASES)
def test_commonmeta_schema_validation_fixture_matrix(name, should_validate):
    doc = json.loads(read_text(fixture_path("commonmeta", name)))
    result = json_schema_errors(doc, "commonmeta")

    if should_validate:
        assert (
            result is None
        ), f"schema validation unexpectedly failed for {name}: {result}"
    else:
        assert result is not None, f"schema validation unexpectedly passed for {name}"
