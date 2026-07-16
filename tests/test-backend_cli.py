"""Exercise the commonmeta-rs CLI through the optional backend.

commonmeta_rs.run_cli runs the full Rust clap CLI in-process (the same binary
surface as the standalone `commonmeta` Rust tool), so these check that the
backend extra wires the two implementations together. They skip on a plain
`pip install commonmeta-py` where commonmeta_rs is absent.

Only offline, valid invocations are used on purpose: run_cli parses with clap's
get_matches_from, which calls process::exit on --help/--version or a malformed
command line — that would kill pytest. Application-level failures (e.g. an
--no-network store miss) instead return an error that surfaces as ValueError,
so those are safe to assert on.
"""

import json

import pytest
from conformance_common import fixture_path

from commonmeta.schema_utils import COMMONMETA_SCHEMA_URI

commonmeta_rs = pytest.importorskip("commonmeta_rs")

# argv[0] is the program name (clap's get_matches_from convention).
ARGV0 = "commonmeta"


def test_run_cli_convert_local_file_to_csl(tmp_path):
    """A local commonmeta file converts to CSL, written to --file, offline."""
    out = str(tmp_path / "out.json")
    commonmeta_rs.run_cli(
        [
            ARGV0,
            "convert",
            fixture_path("commonmeta", "blog_post_1.json"),
            "--from",
            "commonmeta",
            "--to",
            "csl",
            "--file",
            out,
        ]
    )
    with open(out, encoding="utf-8") as handle:
        data = json.load(handle)
    assert data.get("type")
    assert data.get("id")


def test_run_cli_convert_to_stdout(capfd):
    """Without --file the CLI writes the record to stdout (fd-level)."""
    commonmeta_rs.run_cli(
        [
            ARGV0,
            "convert",
            fixture_path("commonmeta", "blog_post_1.json"),
            "--from",
            "commonmeta",
            "--to",
            "commonmeta",
        ]
    )
    payload = json.loads(capfd.readouterr().out)
    # commonmeta output is emitted as a JSON array, even for a single record.
    record = payload[0] if isinstance(payload, list) else payload
    assert record["schema_version"].startswith("https://commonmeta.org")


def test_run_cli_convert_from_sqlite_offline(monkeypatch, tmp_path, capfd):
    """A DOI in the local store converts under --no-network, no network.

    The Rust CLI resolves the same COMMONMETA_DB store commonmeta-py reads, so a
    record written via the backend is served back through the CLI offline.
    """
    db = str(tmp_path / "store.sqlite3")
    doi = "https://doi.org/10.5555/rs-cli-offline"
    commonmeta_rs.write_sqlite(
        [
            {
                "id": doi,
                "type": "JournalArticle",
                "schema_version": COMMONMETA_SCHEMA_URI,
            }
        ],
        db,
    )
    monkeypatch.setenv("COMMONMETA_DB", db)

    commonmeta_rs.run_cli([ARGV0, "convert", "10.5555/rs-cli-offline", "--no-network"])
    data = json.loads(capfd.readouterr().out)
    assert data["id"] == doi
    assert data["type"] == "JournalArticle"


def test_run_cli_offline_miss_raises(monkeypatch, tmp_path):
    """--no-network with no database surfaces as a ValueError, not a crash."""
    monkeypatch.setenv("COMMONMETA_DB", str(tmp_path / "absent.sqlite3"))
    with pytest.raises(ValueError):
        commonmeta_rs.run_cli([ARGV0, "convert", "10.5555/absent", "--no-network"])
