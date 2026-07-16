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

import sys
from functools import lru_cache
from typing import Any

from .schema_utils import COMMONMETA_SCHEMA_URI

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
