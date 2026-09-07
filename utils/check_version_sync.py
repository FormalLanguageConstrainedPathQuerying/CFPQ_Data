#!/usr/bin/env python3
"""Check that the package version is consistent across its sources.

The canonical version lives in ``cfpq_data/config.py`` (``VERSION``);
``pyproject.toml`` must declare the same value. This tool exits non-zero on a
mismatch so it can be wired into pre-commit and CI.

Usage::

    python utils/check_version_sync.py
"""

import pathlib
import re
import sys

__all__ = [
    "config_version",
    "pyproject_version",
    "main",
]

ROOT = pathlib.Path(__file__).resolve().parent.parent


def config_version() -> str:
    """Returns the ``VERSION`` declared in ``cfpq_data/config.py``."""
    text = (ROOT / "cfpq_data" / "config.py").read_text(encoding="utf-8")
    match = re.search(r'^VERSION\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    if not match:
        raise ValueError("Could not find VERSION in cfpq_data/config.py")
    return match.group(1)


def pyproject_version() -> str:
    """Returns the ``version`` declared in ``pyproject.toml``."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def main() -> int:
    """Compares the two version sources; returns 0 on match, 1 on mismatch."""
    config = config_version()
    pyproject = pyproject_version()
    if config != pyproject:
        print(f"Version mismatch: config.py={config!r} pyproject.toml={pyproject!r}")
        return 1
    print(f"Version consistent: {config}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
