#!/usr/bin/env python3
"""Bump the package version across all sources and promote the changelog.

Updates, atomically (all files are validated and transformed before any of
them is written):

* ``cfpq_data/config.py`` -- the canonical ``VERSION``
* ``pyproject.toml``      -- the declared ``version``
* ``CHANGELOG.md``        -- promotes ``## [Unreleased]`` to a dated release
  section (``## [X.Y.Z] - <date>``) and inserts a fresh empty
  ``## [Unreleased]`` above it

The two version sources must already agree (see ``check_version_sync.py``);
this tool refuses to run otherwise.

Usage::

    python utils/bump_version.py 5.1.0 [--date 2026-09-08]
"""

import argparse
import datetime
import pathlib
import re
import sys

from check_version_sync import ROOT, config_version, pyproject_version

__all__ = ["bump", "main"]

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def _set_version(text: str, field_pattern: str, new_version: str) -> str:
    """Replace the version value following ``field_pattern``.

    ``field_pattern`` must match the line prefix (e.g. ``^VERSION\\s*=\\s*``);
    the quoted value that follows it is replaced with ``new_version``.
    """
    new_text, count = re.subn(
        rf"({field_pattern})[\"']([^\"']+)[\"']",
        rf'\g<1>"{new_version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError(f"could not locate version field matching {field_pattern!r}")
    return new_text


def bump(new_version: str, date: str | None = None) -> dict[str, str]:
    """Apply the version bump; returns a mapping of path -> new content.

    Nothing is written until every file has been read, validated, and
    transformed, so a failure leaves the working tree untouched.
    """
    if not SEMVER_RE.match(new_version):
        raise ValueError(f"not a valid X.Y.Z version: {new_version!r}")
    if config_version() != pyproject_version():
        raise ValueError(
            "config.py and pyproject.toml versions differ; "
            "resolve the mismatch before bumping"
        )

    date = date or datetime.date.today().isoformat()

    changes: dict[str, str] = {}

    config_path = ROOT / "cfpq_data" / "config.py"
    changes[str(config_path)] = _set_version(
        config_path.read_text(encoding="utf-8"), r"^VERSION\s*=\s*", new_version
    )

    pyproject_path = ROOT / "pyproject.toml"
    changes[str(pyproject_path)] = _set_version(
        pyproject_path.read_text(encoding="utf-8"), r"^version\s*=\s*", new_version
    )

    changelog_path = ROOT / "CHANGELOG.md"
    promoted, count = re.subn(
        r"^## \[Unreleased\]\s*$",
        f"## [Unreleased]\n\n## [{new_version}] - {date}",
        changelog_path.read_text(encoding="utf-8"),
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError("CHANGELOG.md has no '## [Unreleased]' section to promote")
    changes[str(changelog_path)] = promoted

    for path, content in changes.items():
        pathlib.Path(path).write_text(content, encoding="utf-8")
    return changes


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point; returns a process exit code."""
    parser = argparse.ArgumentParser(
        description="Bump the version in config.py, pyproject.toml, and CHANGELOG.md."
    )
    parser.add_argument("version", help="new version, e.g. 5.1.0")
    parser.add_argument(
        "--date",
        default=None,
        help="release date (YYYY-MM-DD); defaults to today",
    )
    args = parser.parse_args(argv)
    try:
        changes = bump(args.version, args.date)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for path in changes:
        print(f"updated {path}")
    print(f"bumped to {args.version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
