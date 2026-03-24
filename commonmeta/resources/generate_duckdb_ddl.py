#!/usr/bin/env python3
"""
generate_duckdb_ddl.py — Emit DuckDB CREATE TABLE statements from commonmeta JSON Schema.

Reads x-clickhouse annotations (column names, types) and maps ClickHouse types
to DuckDB equivalents. Produces one CREATE TABLE block per table (works + child
tables from $defs), plus CREATE SEQUENCE and CREATE VIEW statements.

Usage:
    python generate_duckdb_ddl.py                        # prints to stdout
    python generate_duckdb_ddl.py --out schema_duckdb.sql
    python generate_duckdb_ddl.py --check schema_duckdb.sql   # CI diff check
    python generate_duckdb_ddl.py --schema path/to/schema.json
    python generate_duckdb_ddl.py --no-comments          # omit COMMENT clauses
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
# ClickHouse → DuckDB type mapping
# ---------------------------------------------------------------------------

# DuckDB does not have LowCardinality, CODEC, bloom_filter, ReplacingMergeTree,
# PARTITION BY, or LowCardinality. It does have VARCHAR, BOOLEAN, HUGEINT,
# UINTEGER, DATE, FLOAT, DOUBLE, and full SQL NULL semantics (every column
# nullable unless NOT NULL is specified).
#
# Key differences from ClickHouse:
#   - DuckDB columns are nullable by default; we add NOT NULL only for required
#     fields identified by the schema's "required" array.
#   - LowCardinality(String) → VARCHAR  (DuckDB has dictionary encoding built-in)
#   - Bool → BOOLEAN
#   - UInt8/UInt16/UInt32 → UTINYINT / USMALLINT / UINTEGER
#   - Nullable(X) → just X  (DuckDB is nullable by default)
#   - CODEC(...) → ignored  (DuckDB manages compression internally)

CH_TO_DUCKDB: dict[str, str] = {
    # Strings
    "String": "VARCHAR",
    "LowCardinality(String)": "VARCHAR",
    # Booleans
    "Bool": "BOOLEAN",
    # Unsigned integers
    "UInt8": "UTINYINT",
    "UInt16": "USMALLINT",
    "UInt32": "UINTEGER",
    "UInt64": "UBIGINT",
    # Signed integers
    "Int8": "TINYINT",
    "Int16": "SMALLINT",
    "Int32": "INTEGER",
    "Int64": "BIGINT",
    # Floats
    "Float32": "FLOAT",
    "Float64": "DOUBLE",
    # Nullable variants — strip Nullable() wrapper, DuckDB is nullable by default
    "Nullable(Date)": "DATE",
    "Nullable(Float32)": "FLOAT",
    "Nullable(Float64)": "DOUBLE",
    "Nullable(UInt16)": "USMALLINT",
    "Nullable(UInt32)": "UINTEGER",
    # Dates
    "Date": "DATE",
    "DateTime": "TIMESTAMP",
    "DateTime64(3)": "TIMESTAMP",
}


def ch_type_to_duckdb(ch_type: str) -> str:
    """Map a ClickHouse type string to a DuckDB type string."""
    # Strip CODEC annotation if it somehow appears in the type field
    if " CODEC(" in ch_type:
        ch_type = ch_type[: ch_type.index(" CODEC(")]
    mapped = CH_TO_DUCKDB.get(ch_type)
    if mapped:
        return mapped
    # Fallback: warn and use VARCHAR
    print(
        f"warning: unknown ClickHouse type '{ch_type}', defaulting to VARCHAR",
        file=sys.stderr,
    )
    return "VARCHAR"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class ColumnDef:
    name: str
    duckdb_type: str
    not_null: bool = False
    comment: str | None = None


@dataclass
class IndexDef:
    name: str
    table: str
    columns: list[str]
    unique: bool = False


@dataclass
class TableDef:
    name: str
    columns: list[ColumnDef] = field(default_factory=list)
    indexes: list[IndexDef] = field(default_factory=list)
    comment: str | None = None
    # Foreign key info for documentation purposes (DuckDB supports FK constraints)
    foreign_keys: list[tuple[str, str, str]] = field(default_factory=list)
    # (fk_column, ref_table, ref_column)


# ---------------------------------------------------------------------------
# Schema parsing
# ---------------------------------------------------------------------------


def collect_columns(
    properties: dict[str, Any],
    required_fields: list[str],
) -> list[ColumnDef]:
    cols = []
    for prop_name, prop_schema in properties.items():
        ch = prop_schema.get("x-clickhouse")
        if not ch:
            continue
        if "child_table" in ch or "table" in ch:
            continue

        col_name = ch["column"]
        duckdb_type = ch_type_to_duckdb(ch.get("type", "String"))
        not_null = col_name in required_fields or prop_name in required_fields

        comment = ch.get("note") or prop_schema.get("description")
        if comment:
            comment = comment.replace("'", "''")[:120]

        cols.append(
            ColumnDef(
                name=col_name,
                duckdb_type=duckdb_type,
                not_null=not_null,
                comment=comment,
            )
        )
    return cols


def resolve_required_columns(
    properties: dict[str, Any],
    required_props: list[str],
) -> list[str]:
    """Map required JSON Schema property names to their ClickHouse column names."""
    col_names = []
    for prop_name in required_props:
        prop = properties.get(prop_name, {})
        ch = prop.get("x-clickhouse", {})
        if "column" in ch:
            col_names.append(ch["column"])
        else:
            col_names.append(prop_name)
    return col_names


def extract_tables(schema: dict) -> list[TableDef]:
    tables: list[TableDef] = []

    # ---- Top-level works table ----
    top_ch = schema.get("x-clickhouse", {})
    props = schema.get("properties", {})
    required_props = schema.get("required", [])
    required_cols = resolve_required_columns(props, required_props)

    top_indexes = []
    for ix in top_ch.get("indexes", []):
        top_indexes.append(
            IndexDef(
                name=ix["name"],
                table=top_ch["table"],
                columns=[ix["expr"]],
            )
        )

    tables.append(
        TableDef(
            name=top_ch["table"],
            columns=collect_columns(props, required_cols),
            indexes=top_indexes,
            comment=top_ch.get("note"),
        )
    )

    # ---- Child tables from $defs ----
    for def_name, def_schema in schema.get("$defs", {}).items():
        ch = def_schema.get("x-clickhouse")
        if not ch:
            continue

        table_name = ch["table"]
        def_props = def_schema.get("properties", {})
        def_required = def_schema.get("required", [])
        def_required_cols = resolve_required_columns(def_props, def_required)
        cols = collect_columns(def_props, def_required_cols)

        # Build indexes from x-clickhouse.indexes on the $def
        def_indexes = []
        for ix in ch.get("indexes", []):
            def_indexes.append(
                IndexDef(
                    name=ix["name"],
                    table=table_name,
                    columns=[ix["expr"]],
                )
            )

        # Detect foreign key columns by role annotation
        fks = []
        for _pn, ps in def_props.items():
            c = ps.get("x-clickhouse", {})
            if c.get("role") == "foreign_key":
                fks.append((c["column"], "works", "doi"))

        tables.append(
            TableDef(
                name=table_name,
                columns=cols,
                indexes=def_indexes,
                comment=ch.get("note") or def_schema.get("description"),
                foreign_keys=fks,
            )
        )

    return tables


# ---------------------------------------------------------------------------
# DDL rendering
# ---------------------------------------------------------------------------


def render_column(col: ColumnDef, max_name_len: int, include_comments: bool) -> str:
    pad = " " * (max_name_len - len(col.name) + 1)
    line = f"    {col.name}{pad}{col.duckdb_type}"
    if col.not_null:
        line += " NOT NULL"
    if col.comment and include_comments:
        line += f" -- {col.comment}"
    return line


def render_table(t: TableDef, include_comments: bool) -> str:
    lines: list[str] = []

    if t.comment and include_comments:
        for ln in t.comment.splitlines():
            lines.append(f"-- {ln}")

    lines.append(f"CREATE TABLE IF NOT EXISTS {t.name}")
    lines.append("(")

    max_name = max((len(c.name) for c in t.columns), default=0)
    col_lines = [render_column(c, max_name, include_comments) for c in t.columns]

    # Foreign key constraints
    fk_lines = []
    for fk_col, ref_table, ref_col in t.foreign_keys:
        fk_lines.append(f"    FOREIGN KEY ({fk_col}) REFERENCES {ref_table}({ref_col})")

    all_lines = col_lines + fk_lines
    lines.append(",\n".join(all_lines))
    lines.append(");")

    # Indexes as separate CREATE INDEX statements
    for ix in t.indexes:
        col_expr = ", ".join(ix.columns)
        unique = "UNIQUE " if ix.unique else ""
        lines.append(
            f"\nCREATE {unique}INDEX IF NOT EXISTS {ix.name}"
            f"\n    ON {ix.table} ({col_expr});"
        )

    return "\n".join(lines)


def render_views(tables: list[TableDef]) -> str:
    """
    Emit a small set of useful analytical views.
    These illustrate common join patterns and serve as query starting points.
    """
    lines = [
        "-- ---------------------------------------------------------------------------",
        "-- Analytical views",
        "-- ---------------------------------------------------------------------------",
        "",
        "-- works_full: works joined with creator list as JSON aggregate",
        "CREATE OR REPLACE VIEW works_full AS",
        "SELECT",
        "    w.*,",
        "    (SELECT json_group_array(json_object(",
        "        'position',         c.position,",
        "        'name',             c.name,",
        "        'given_name',       c.given_name,",
        "        'family_name',      c.family_name,",
        "        'orcid',            c.orcid,",
        "        'institution_id',   c.institution_id,",
        "        'institution_name', c.institution_name,",
        "        'country_code',     c.country_code",
        "    ) ORDER BY c.position)",
        "     FROM works_creators c",
        "     WHERE c.doi = w.doi AND c.source = w.source",
        "    ) AS creators_json",
        "FROM works w;",
        "",
        "-- citation_graph: resolved citation edges (both sides have a DOI in works)",
        "CREATE OR REPLACE VIEW citation_graph AS",
        "SELECT",
        "    r.citing_doi,",
        "    r.ref_doi         AS cited_doi,",
        "    r.source,",
        "    w_citing.publication_year AS citing_year,",
        "    w_cited.publication_year  AS cited_year,",
        "    w_cited.type              AS cited_type",
        "FROM works_references r",
        "JOIN works w_citing ON w_citing.doi = r.citing_doi AND w_citing.source = r.source",
        "JOIN works w_cited  ON w_cited.doi  = r.ref_doi",
        "WHERE r.ref_doi IS NOT NULL AND r.ref_doi != '';",
        "",
        "-- works_oa: open access works with best available URL",
        "CREATE OR REPLACE VIEW works_oa AS",
        "SELECT doi, source, title, publication_year, type,",
        "       oa_status, oa_url, license_id",
        "FROM works",
        "WHERE is_oa = true;",
    ]
    return "\n".join(lines)


def render_all(
    tables: list[TableDef], schema_path: Path, include_comments: bool
) -> str:
    header = "\n".join(
        [
            "-- Auto-generated by generate_duckdb_ddl.py",
            f"-- Source: {schema_path.name}",
            "-- Edit the JSON Schema, not this file.",
            "--",
            "-- Compatibility: DuckDB 0.9+",
            "-- Notable differences from ClickHouse DDL:",
            "--   * No PARTITION BY (DuckDB manages data layout internally)",
            "--   * No ReplacingMergeTree — use INSERT OR REPLACE or deduplicate in queries",
            "--   * LowCardinality → VARCHAR (DuckDB uses dictionary encoding automatically)",
            "--   * CODEC annotations ignored (DuckDB handles compression internally)",
            "--   * Nullable columns are the default — NOT NULL added only for required fields",
            "--   * Indexes are advisory for DuckDB; it relies primarily on zone maps",
            "",
        ]
    )

    table_blocks = [render_table(t, include_comments) for t in tables]
    views = render_views(tables)

    sep = "\n\n" + "-- " + "-" * 75 + "\n\n"
    return header + sep.join(table_blocks) + "\n\n\n" + views + "\n"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate(schema: dict, tables: list[TableDef]) -> list[str]:
    warnings = []
    for t in tables:
        if not t.columns:
            warnings.append(
                f"{t.name}: no columns found — check x-clickhouse annotations"
            )
    for def_name, def_schema in schema.get("$defs", {}).items():
        if not def_schema.get("x-clickhouse"):
            warnings.append(
                f"$defs.{def_name}: missing x-clickhouse block — table skipped"
            )
    return warnings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--check", type=Path, default=None, metavar="FILE")
    parser.add_argument("--no-comments", action="store_true", dest="no_comments")
    args = parser.parse_args()

    if not args.schema.exists():
        print(f"error: schema not found: {args.schema}", file=sys.stderr)
        sys.exit(1)

    schema = json.loads(args.schema.read_text())
    tables = extract_tables(schema)

    for w in validate(schema, tables):
        print(f"warning: {w}", file=sys.stderr)

    output = render_all(tables, args.schema, include_comments=not args.no_comments)

    if args.check:
        existing = args.check.read_text() if args.check.exists() else ""
        if output != existing:
            print(
                f"error: {args.check} is out of date. Run with --out {args.check} to update.",
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
