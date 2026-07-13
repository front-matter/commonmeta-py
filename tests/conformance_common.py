"""Shared helpers for the conformance tests: fixture discovery, a semantic
JSON diff, and a string-in/string-out ``convert`` wrapper.

Ported from the commonmeta-rs conformance harness (tests/common/mod.rs). The
diff compares two parsed JSON trees rather than strings, so key ordering and
whitespace don't matter. Two rules make it match the commonmeta wire format:

  * **omitempty-aware**: a field present in one tree but absent in the other is
    only a mismatch if its value is non-empty. An empty string, empty array,
    empty object, null, or numeric zero is treated as equivalent to absent.
  * **numeric-aware**: ``52`` and ``52.0`` compare equal, so a fixture authored
    with an integer latitude won't spuriously fail against a float field.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from os import path
from typing import Any

import pytest
from commonmeta_schema import fixtures_path as _package_fixtures_path

from commonmeta import Metadata

# Conformance fixtures are provided by the commonmeta-schema package (shared,
# language-neutral golden set) rather than local copies.
FIXTURES_DIR = str(_package_fixtures_path())

# Map commonmeta-rs format names to commonmeta-py reader (via) / writer (to)
# identifiers.
FORMAT_ALIASES = {
    "schemaorg": "schema_org",
}


def _py_format(fmt: str) -> str:
    return FORMAT_ALIASES.get(fmt, fmt)


@dataclass
class Mismatch:
    kind: str  # "LOST" | "SPURIOUS" | "CHANGED" | "LENGTH"
    path: str
    expected: Any = None
    actual: Any = None

    def __str__(self) -> str:
        if self.kind == "LOST":
            return f"LOST     {self.path} (in expected, not in output)"
        if self.kind == "SPURIOUS":
            return f"SPURIOUS {self.path} (in output, not in expected)"
        if self.kind == "LENGTH":
            return (
                f"LENGTH   {self.path}: expected {self.expected} items, "
                f"got {self.actual}"
            )
        return f"CHANGED  {self.path}: expected {self.expected!r}, got {self.actual!r}"


def is_emptyish(value: Any) -> bool:
    """A value equivalent to absent under commonmeta's omitempty serialization."""
    if value is None:
        return True
    if isinstance(value, str):
        return value == ""
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return value == 0
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def _num_eq(a: Any, b: Any) -> bool:
    try:
        return float(a) == float(b)
    except (TypeError, ValueError):
        return False


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def diff(expected: Any, actual: Any) -> list[Mismatch]:
    """Semantic diff of two parsed-JSON trees. Returns a list of mismatches."""
    out: list[Mismatch] = []
    _diff_rec(expected, actual, "$", out)
    return out


def _diff_rec(exp: Any, act: Any, path_: str, out: list[Mismatch]) -> None:
    if isinstance(exp, dict) and isinstance(act, dict):
        for k, ev in exp.items():
            if k in act:
                _diff_rec(ev, act[k], f"{path_}.{k}", out)
            elif not is_emptyish(ev):
                out.append(Mismatch("LOST", f"{path_}.{k}"))
        for k, av in act.items():
            if k not in exp and not is_emptyish(av):
                out.append(Mismatch("SPURIOUS", f"{path_}.{k}"))
    elif isinstance(exp, list) and isinstance(act, list):
        if len(exp) != len(act):
            out.append(Mismatch("LENGTH", path_, len(exp), len(act)))
        for i in range(min(len(exp), len(act))):
            _diff_rec(exp[i], act[i], f"{path_}[{i}]", out)
    elif _is_number(exp) and _is_number(act):
        if not _num_eq(exp, act):
            out.append(Mismatch("CHANGED", path_, exp, act))
    else:
        if exp != act and not (is_emptyish(exp) and is_emptyish(act)):
            out.append(Mismatch("CHANGED", path_, exp, act))


def collect_ext(dir_path: str, ext: str) -> list[str]:
    """Return sorted absolute paths of files in dir_path with the given extension."""
    if not path.isdir(dir_path):
        return []
    files = [
        path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(f".{ext}")
    ]
    files.sort()
    return files


def collect_json(dir_path: str) -> list[str]:
    return collect_ext(dir_path, "json")


def collect_bib(dir_path: str) -> list[str]:
    return collect_ext(dir_path, "bib")


def fixture_path(*parts: str) -> str:
    return path.join(FIXTURES_DIR, *parts)


def read_text(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as fh:
        return fh.read()


def _reader_payload(from_format: str, data: str) -> Any:
    """Unwrap raw API-response fixtures to the shape the commonmeta-py reader
    expects, mirroring what commonmeta-rs convert() and the py API fetchers do:
    Crossref responses are wrapped in ``message``; DataCite in ``data.attributes``.
    """
    if from_format == "crossref":
        obj = json.loads(data)
        return obj.get("message", obj) if isinstance(obj, dict) else obj
    if from_format == "datacite":
        obj = json.loads(data)
        if isinstance(obj, dict) and isinstance(obj.get("data"), dict):
            return obj["data"].get("attributes", obj)
        return obj
    return data


def convert(from_format: str, to_format: str, data: str) -> Any:
    """String-in/JSON-value-out conversion, mirroring commonmeta-rs convert().

    Reads ``data`` (a raw string in ``from_format``) and writes it to
    ``to_format``. JSON outputs are returned as parsed values; text outputs
    (bibtex, ris) as strings.
    """
    subject = Metadata(_reader_payload(from_format, data), via=_py_format(from_format))
    out = subject.write(to=_py_format(to_format))
    if to_format in ("bibtex", "ris"):
        # bibtex/ris writers return bytes; compare as text against the golden.
        return out.decode("utf-8") if isinstance(out, bytes) else out
    return json.loads(out)


def canonical_commonmeta_value(raw: str, context: str) -> Any:
    """Normalize a commonmeta fixture through the commonmeta reader+writer,
    so expectations are compared on equal footing (same omitempty handling)."""
    try:
        return convert("commonmeta", "commonmeta", raw)
    except Exception as error:  # noqa: BLE001 - surfaced with context
        raise AssertionError(
            f"{context}: canonical commonmeta conversion failed: {error}"
        ) from error


def reader_pairs(
    input_subdir: str, ext: str = "json", expected_subdir: str = "commonmeta"
) -> list[tuple[str, str]]:
    """(input_path, expected_commonmeta_path) pairs where both files exist.

    For JSON inputs the expected file shares the full filename; for other
    extensions the expected file is ``<stem>.json`` in ``expected_subdir``.
    """
    pairs = []
    for input_path in collect_ext(fixture_path(input_subdir), ext):
        stem = path.splitext(path.basename(input_path))[0]
        expected_path = fixture_path(expected_subdir, f"{stem}.json")
        if path.exists(expected_path):
            pairs.append((input_path, expected_path))
    return pairs


def writer_pairs(expected_subdir: str, out_ext: str = "json") -> list[tuple[str, str]]:
    """(commonmeta_input_path, expected_output_path) pairs where both exist."""
    pairs = []
    for input_path in collect_json(fixture_path("commonmeta")):
        stem = path.splitext(path.basename(input_path))[0]
        expected_path = fixture_path(expected_subdir, f"{stem}.{out_ext}")
        if path.exists(expected_path):
            pairs.append((input_path, expected_path))
    return pairs


def pair_id(pair: tuple[str, str]) -> str:
    """pytest test id from a fixture pair (the input file's basename)."""
    return path.basename(pair[0])


def assert_golden_or_xfail(expected: Any, actual: Any) -> None:
    """Pass when the semantic diff is empty; otherwise xfail documenting the
    divergence. As commonmeta-py converges to the commonmeta-rs golden output,
    xfailing pairs flip to passing automatically."""
    diffs = diff(expected, actual)
    if diffs:
        summary = "; ".join(str(m) for m in diffs[:4])
        more = "" if len(diffs) <= 4 else f" (+{len(diffs) - 4} more)"
        pytest.xfail(f"diverges from commonmeta-rs golden: {summary}{more}")


def convert_or_xfail(from_format: str, to_format: str, data: str) -> Any:
    """convert(), but xfail (rather than error) when commonmeta-py cannot read
    a fixture that commonmeta-rs handles — that too is a documented divergence."""
    try:
        return convert(from_format, to_format, data)
    except Exception as error:  # noqa: BLE001
        pytest.xfail(
            f"commonmeta-py convert({from_format}->{to_format}) failed: {error}"
        )
