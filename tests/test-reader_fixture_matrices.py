# pylint: disable=invalid-name
"""Reader fixture matrices ported from commonmeta-rs
(tests/reader_fixture_matrices.rs).

For each reader format, every ``tests/fixtures/<subdir>/<name>.json`` input with
a matching ``tests/fixtures/commonmeta/<name>.json`` expected file is read and
written to commonmeta, then compared. Each pair is a separate parametrized
case: it passes when commonmeta-py matches the commonmeta-rs golden output and
xfails (documenting the diff) when it diverges.
"""

import pytest
from conformance_common import (
    assert_golden_or_xfail,
    canonical_commonmeta_value,
    convert_or_xfail,
    pair_id,
    read_text,
    reader_pairs,
)


def _matrix(format_name, subdir):
    return [
        pytest.param(format_name, pair, id=pair_id(pair))
        for pair in reader_pairs(subdir)
    ]


@pytest.mark.parametrize(
    "format_name,pair",
    _matrix("crossref", "crossref")
    + _matrix("datacite", "datacite_reader")
    + _matrix("schemaorg", "schemaorg")
    + _matrix("jsonfeed", "jsonfeed")
    + _matrix("inveniordm", "inveniordm")
    + _matrix("codemeta", "codemeta"),
)
def test_reader_fixture_matrix(format_name, pair):
    input_path, expected_path = pair
    expected = canonical_commonmeta_value(read_text(expected_path), expected_path)
    actual = convert_or_xfail(format_name, "commonmeta", read_text(input_path))
    assert_golden_or_xfail(expected, actual)
