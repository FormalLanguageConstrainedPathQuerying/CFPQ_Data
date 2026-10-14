#!/usr/bin/env python3
"""Set a PEP 440 developmental version in the package version sources.

Used by the publish workflow on pull requests: each run rewrites the version
to ``<base>.dev<run number>`` on the runner (never committed) so that every
push publishes a distinct artifact to TestPyPI. A literal commit-hash suffix
is not publishable — PEP 440 forbids local version identifiers (``+<hash>``)
on public indices.

Updates ``flpq_data/config.py`` (the canonical ``VERSION``) and
``pyproject.toml``, which must already agree. ``CHANGELOG.md`` is never
touched.

Usage::

    python utils/set_dev_version.py 6.0.0.dev123
"""

import argparse
import pathlib
import re
import sys

from bump_version import set_version_field
from check_version_sync import ROOT, config_version, pyproject_version

__all__ = ["set_dev_version", "main"]

DEV_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+\.dev\d+$")


def set_dev_version(version: str) -> dict[str, str]:
    """Set ``version`` in both version sources; returns path -> new content.

    ``version`` must be a developmental release (``X.Y.Z.devN``). Nothing is
    written until both sources have been read and transformed, so a failure
    leaves the working tree untouched.
    """
    if not DEV_VERSION_RE.match(version):
        raise ValueError(f"not a valid X.Y.Z.devN version: {version!r}")
    if config_version() != pyproject_version():
        raise ValueError(
            "config.py and pyproject.toml versions differ; "
            "resolve the mismatch before setting a dev version"
        )

    changes: dict[str, str] = {}

    config_path = ROOT / "flpq_data" / "config.py"
    changes[str(config_path)] = set_version_field(
        config_path.read_text(encoding="utf-8"), r"^VERSION\s*=\s*", version
    )

    pyproject_path = ROOT / "pyproject.toml"
    changes[str(pyproject_path)] = set_version_field(
        pyproject_path.read_text(encoding="utf-8"), r"^version\s*=\s*", version
    )

    for path, content in changes.items():
        pathlib.Path(path).write_text(content, encoding="utf-8")
    return changes


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point; returns a process exit code."""
    parser = argparse.ArgumentParser(
        description="Set a X.Y.Z.devN version in config.py and pyproject.toml."
    )
    parser.add_argument("version", help="developmental version, e.g. 6.0.0.dev123")
    args = parser.parse_args(argv)
    try:
        set_dev_version(args.version)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"set developmental version {args.version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
