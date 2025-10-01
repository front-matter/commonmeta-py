# This file exists for backward compatibility with tools that expect setup.py
# All configuration is in pyproject.toml with hatchling as the build backend.

import sys

if __name__ == "__main__":
    print(
        "This package uses PEP 517/518 with hatchling as the build backend.\n"
        "Please use 'pip install .' or 'python -m build' instead of setup.py",
        file=sys.stderr,
    )
    sys.exit(1)
