#!/usr/bin/env python3
"""
generate_ddl.py — Emit ClickHouse CREATE TABLE statements from commonmeta JSON Schema.

Reads x-clickhouse annotations on every field and produces one CREATE TABLE
block per table (works + all child tables defined in $defs).

Usage:
    python generate_ddl.py                          # prints to stdout
    python generate_ddl.py --out schema.sql         # writes to file
    python generate_ddl.py --check schema.sql       # exits 1 if output differs (CI use)
    python generate_ddl.py --schema path/to/schema  # use non-default schema file
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_SCHEMA = Path(__file__).parent / "commonmeta-work.schema.json"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class ColumnDef:
    name: str
    ch_type: str
    codec: str | None = None
    comment: str | None = None


@dataclass
class IndexDef:
    name: str
    expr: str
    index_type: str
    granularity: int = 4


@dataclass
class TableDef:
    name: str
    engine: str
    order_by: list[str]
    partition_by: str | None = None
    settings: dict[str, Any] = field(default_factory=dict)
    columns: list[ColumnDef] = field(default_factory=list)
    indexes: list[IndexDef] = field(default_factory=list)
    comment: str | None = None


# ---------------------------------------------------------------------------
# Schema parsing
# ---------------------------------------------------------------------------


def parse_indexes(raw: list[dict]) -> list[IndexDef]:
    out = []
    for ix in raw:
        out.append(
            IndexDef(
                name=ix["name"],
                expr=ix["expr"],
                index_type=ix["type"],
                granularity=ix.get("granularity", 4),
            )
        )
    return out


def parse_table_meta(
    ch: dict,
) -> tuple[str, str, list[str], str | None, dict, list[IndexDef], str | None]:
    """Extract table-level ClickHouse metadata from an x-clickhouse block."""
    table = ch["table"]
    engine = ch.get("engine", "MergeTree()")
    order_by = ch.get("order_by", [])
    partition_by = ch.get("partition_by")
    settings = ch.get("settings", {})
    indexes = parse_indexes(ch.get("indexes", []))
    comment = ch.get("note")
    return table, engine, order_by, partition_by, settings, indexes, comment


def collect_columns(properties: dict[str, Any]) -> list[ColumnDef]:
    cols = []
    for _prop_name, prop_schema in properties.items():
        ch = prop_schema.get("x-clickhouse")
        if not ch:
            continue
        # Skip properties that describe a child table rather than a column
        if "child_table" in ch or "table" in ch:
            continue
        col = ColumnDef(
            name=ch["column"],
            ch_type=ch["type"],
            codec=ch.get("codec"),
            comment=ch.get("note") or prop_schema.get("description"),
        )
        cols.append(col)
    return cols


def extract_tables(schema: dict) -> list[TableDef]:
    tables: list[TableDef] = []

    # ---- Top-level works table ----
    top_ch = schema.get("x-clickhouse", {})
    table, engine, order_by, partition_by, settings, indexes, comment = (
        parse_table_meta(top_ch)
    )
    cols = collect_columns(schema.get("properties", {}))
    tables.append(
        TableDef(
            name=table,
            engine=engine,
            order_by=order_by,
            partition_by=partition_by,
            settings=settings,
            columns=cols,
            indexes=indexes,
            comment=comment,
        )
    )

    # ---- Child tables from $defs ----
    for def_name, def_schema in schema.get("$defs", {}).items():
        ch = def_schema.get("x-clickhouse")
        if not ch:
            continue
        table, engine, order_by, partition_by, settings, indexes, comment = (
            parse_table_meta(ch)
        )
        cols = collect_columns(def_schema.get("properties", {}))
        tables.append(
            TableDef(
                name=table,
                engine=engine,
                order_by=order_by,
                partition_by=partition_by,
                settings=settings,
                columns=cols,
                indexes=indexes,
                comment=comment or def_schema.get("description"),
            )
        )

    return tables


# ---------------------------------------------------------------------------
# DDL rendering
# ---------------------------------------------------------------------------


def render_column(col: ColumnDef, max_name_len: int) -> str:
    padding = " " * (max_name_len - len(col.name) + 1)
    line = f"    {col.name}{padding}{col.ch_type}"
    if col.codec:
        line += f" CODEC({col.codec})"
    if col.comment:
        # Truncate long comments; full detail lives in the schema file
        short = col.comment[:80].replace("'", "\\'")
        if len(col.comment) > 80:
            short += "..."
        line += f" COMMENT '{short}'"
    return line


def render_table(t: TableDef) -> str:
    lines: list[str] = []

    if t.comment:
        for ln in t.comment.splitlines():
            lines.append(f"-- {ln}")

    lines.append(f"CREATE TABLE IF NOT EXISTS {t.name}")
    lines.append("(")

    max_name = max((len(c.name) for c in t.columns), default=0)
    col_lines = [render_column(c, max_name) for c in t.columns]
    lines.append(",\n".join(col_lines))

    lines.append(")")
    lines.append(f"ENGINE = {t.engine}")

    if t.partition_by:
        lines.append(f"PARTITION BY {t.partition_by}")

    if t.order_by:
        order_expr = ", ".join(t.order_by)
        lines.append(f"ORDER BY ({order_expr})")

    if t.settings:
        settings_expr = ", ".join(f"{k} = {v}" for k, v in t.settings.items())
        lines.append(f"SETTINGS {settings_expr}")

    lines.append(";")

    # Indexes are separate statements in ClickHouse
    for ix in t.indexes:
        lines.append(
            f"\nALTER TABLE {t.name} ADD INDEX IF NOT EXISTS {ix.name} "
            f"({ix.expr}) TYPE {ix.index_type} GRANULARITY {ix.granularity};"
        )

    return "\n".join(lines)


def render_all(tables: list[TableDef], schema_path: Path) -> str:
    header = (
        f"-- Auto-generated by generate_ddl.py\n"
        f"-- Source: {schema_path.name}\n"
        f"-- Edit the JSON Schema, not this file.\n"
    )
    blocks = [render_table(t) for t in tables]
    return header + "\n\n" + "\n\n".join(blocks) + "\n"


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def validate_schema(schema: dict, tables: list[TableDef]) -> list[str]:
    """
    Basic sanity checks. Returns a list of warning strings.
    Does not raise — warnings are printed to stderr.
    """
    warnings: list[str] = []

    for def_name, def_schema in schema.get("$defs", {}).items():
        ch = def_schema.get("x-clickhouse", {})
        if not ch:
            warnings.append(
                f"$defs.{def_name}: missing x-clickhouse block — table will not be generated"
            )
            continue
        order_by = ch.get("order_by", [])
        props = def_schema.get("properties", {})
        col_names = {
            v["x-clickhouse"]["column"]
            for v in props.values()
            if "x-clickhouse" in v and "column" in v["x-clickhouse"]
        }
        for ob_col in order_by:
            if ob_col not in col_names:
                warnings.append(
                    f"{ch.get('table', def_name)}: ORDER BY column '{ob_col}' not found in properties"
                )

    for t in tables:
        if not t.order_by:
            warnings.append(
                f"{t.name}: no ORDER BY — MergeTree tables require an ORDER BY"
            )
        if not t.columns:
            warnings.append(
                f"{t.name}: no columns found — check x-clickhouse annotations"
            )

    return warnings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--schema", type=Path, default=DEFAULT_SCHEMA, help="Path to JSON Schema file"
    )
    parser.add_argument(
        "--out", type=Path, default=None, help="Write output to file instead of stdout"
    )
    parser.add_argument(
        "--check",
        type=Path,
        default=None,
        metavar="FILE",
        help="Diff against FILE and exit 1 if different (for CI)",
    )
    args = parser.parse_args()

    schema_path: Path = args.schema
    if not schema_path.exists():
        print(f"error: schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)

    schema = json.loads(schema_path.read_text())
    tables = extract_tables(schema)

    warnings = validate_schema(schema, tables)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)

    output = render_all(tables, schema_path)

    if args.check:
        existing = args.check.read_text() if args.check.exists() else ""
        if output != existing:
            print(
                f"error: {args.check} is out of date. Run generate_ddl.py --out {args.check} to update.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"ok: {args.check} is up to date")
        return

    if args.out:
        args.out.write_text(output)
        print(f"wrote {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
