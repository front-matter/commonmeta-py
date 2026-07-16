"""Optional Rust backend for commonmeta-py.

The corpus-scale operations - bulk import of annual data files, the local SQLite
store, Parquet and archive output - are implemented in commonmeta-rs and exposed
through its PyO3 module, `commonmeta_rs`. None of them exist in pure Python.

They ship as an optional extra::

    pip install 'commonmeta-py[backend]'      # requires Python 3.14+

`commonmeta_rs` is never imported at module scope by the library: reading and
writing metadata does not need it, and it must stay absent-but-not-broken on
interpreters and installs that don't have it. Call :func:`require_backend` at the
top of anything that does need it.
"""

from __future__ import annotations

import os
import sys
from functools import lru_cache
from typing import Any

from .schema_utils import COMMONMETA_SCHEMA_URI

# Environment override for the local SQLite store, matching commonmeta-rs'
# COMMONMETA_DB. The store holds imported commonmeta works plus ROR organizations
# and ORCID persons, so reads can be served from it offline.
DB_PATH_ENV = "COMMONMETA_DB"

# commonmeta-rs builds against the stable ABI from 3.14 on (abi3-py314), so it
# cannot be installed below that. commonmeta-py itself keeps a 3.9 floor: the
# library serves InvenioRDM, the backend serves operators running corpus-scale
# imports on infrastructure they control. The CLI hides the backend commands
# below this version rather than listing ones the interpreter can never run.
BACKEND_PYTHON_VERSION = (3, 14)
BACKEND_PYTHON_SUPPORTED = sys.version_info >= BACKEND_PYTHON_VERSION

INSTALL_HINT = (
    "This needs the optional Rust backend:\n"
    "    pip install 'commonmeta-py[backend]'   (requires Python 3.14+)"
)


class BackendError(Exception):
    """The Rust backend is unavailable, or a call into it failed."""


@lru_cache(maxsize=1)
def _load() -> Any:
    """Import commonmeta_rs and check it agrees with us on the schema.

    The backend writes commonmeta records into a *persistent* SQLite/Parquet
    store, so a schema mismatch between it and this package doesn't just produce
    a bad conversion - it persists one. Fail at import rather than at read time.
    """
    if not BACKEND_PYTHON_SUPPORTED:
        raise BackendError(
            f"The Rust backend requires Python "
            f"{BACKEND_PYTHON_VERSION[0]}.{BACKEND_PYTHON_VERSION[1]}+; this is "
            f"{sys.version_info[0]}.{sys.version_info[1]}. The rest of "
            "commonmeta-py works here; only bulk import, the local SQLite store "
            "and Parquet output need it."
        )
    try:
        import commonmeta_rs
    except ImportError as error:
        raise BackendError(INSTALL_HINT) from error

    schema_uri = getattr(commonmeta_rs, "__commonmeta_schema__", None)
    if schema_uri is not None and schema_uri != COMMONMETA_SCHEMA_URI:
        raise BackendError(
            "commonmeta-rs targets a different commonmeta schema than "
            f"commonmeta-py: {schema_uri} vs {COMMONMETA_SCHEMA_URI}. Records "
            "written to a shared store would disagree. Align the "
            "commonmeta-schema versions the two packages pin."
        )
    return commonmeta_rs


def _data_dir() -> str:
    """Per-user data directory, matching the Rust `dirs` crate that
    commonmeta-rs uses, so both resolve the same default database path."""
    if sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    elif sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.path.expanduser("~/AppData/Roaming")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(base, "commonmeta")


def resolve_db_path(explicit: str | None = None) -> str:
    """Resolve the local commonmeta SQLite database path.

    Precedence, mirroring commonmeta-rs' ``resolve_db_path``: an explicit path,
    then the ``COMMONMETA_DB`` environment variable, then
    ``<data_dir>/commonmeta/commonmeta.sqlite3``.
    """
    if explicit:
        return explicit
    env = os.environ.get(DB_PATH_ENV)
    if env:
        return env
    return os.path.join(_data_dir(), "commonmeta.sqlite3")


def backend_available() -> bool:
    """Whether the optional Rust backend can be used."""
    try:
        _load()
    except BackendError:
        return False
    return True


def require_backend() -> Any:
    """Return the `commonmeta_rs` module, or raise BackendError explaining how
    to install it."""
    return _load()
