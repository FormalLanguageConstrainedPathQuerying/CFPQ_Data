"""Enforce the line and branch coverage thresholds on a coverage report.

pytest-cov's ``--cov-fail-under`` (and coverage.py's ``fail_under``) check
only the combined total of statements and branches, so they cannot enforce
each metric separately: with line at 94% and branch at 100%, the combined
total could still pass a 95% gate. This tool reads the JSON report that
pytest-cov writes (``--cov-report=json``) and fails unless **both** line and
branch coverage are at least the threshold (default 95%).

Usage (from any directory)::

    python utils/check_coverage.py [coverage.json] [--threshold 95.0]
"""

import argparse
import json
import pathlib
from typing import Optional, Sequence

__all__ = ["main"]


def _percent(covered: int, total: int) -> float:
    return 100.0 if total == 0 else 100.0 * covered / total


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Command-line entry point.

    Reads the coverage.py JSON report, prints the line and branch
    percentages computed from the raw counts, and fails if either is below
    the threshold.

    Returns
    -------
    status : int
        0 when both metrics are at or above the threshold, 1 otherwise (or
        when the report cannot be read or lacks branch data).
    """
    parser = argparse.ArgumentParser(
        description=(
            "Fail unless both line and branch coverage in a coverage.py JSON "
            "report are at least the threshold."
        )
    )
    parser.add_argument(
        "report",
        nargs="?",
        default="coverage.json",
        type=pathlib.Path,
        help="path to the coverage.py JSON report (default: coverage.json)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=95.0,
        help="minimum percentage for each metric (default: 95.0)",
    )
    args = parser.parse_args(argv)

    try:
        data = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: cannot read coverage report {args.report}: {error}")
        return 1

    try:
        totals = data["totals"]
        line_percent = _percent(totals["covered_lines"], totals["num_statements"])
    except (KeyError, TypeError) as error:
        print(
            f"error: {args.report} does not look like a coverage.py JSON "
            f"report ({error})"
        )
        return 1

    if "num_branches" not in totals:
        print(
            "error: the report has no branch data; generate it with branch "
            "coverage enabled ([tool.coverage.run] branch = true)"
        )
        return 1
    branch_percent = _percent(totals["covered_branches"], totals["num_branches"])

    print(
        f"line coverage:   {line_percent:.2f}% "
        f"({totals['covered_lines']}/{totals['num_statements']})"
    )
    print(
        f"branch coverage: {branch_percent:.2f}% "
        f"({totals['covered_branches']}/{totals['num_branches']})"
    )

    failed = []
    if line_percent < args.threshold:
        failed.append(f"line ({line_percent:.2f}%)")
    if branch_percent < args.threshold:
        failed.append(f"branch ({branch_percent:.2f}%)")
    if failed:
        print(
            f"error: {' and '.join(failed)} below the {args.threshold:.1f}% threshold"
        )
        return 1

    print(f"coverage ok (threshold {args.threshold:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
