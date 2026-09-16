"""Audit the per-graph docs pages for Info-table field consistency.

Each page under ``docs/graphs/data/`` has an ``Info`` list-table whose rows
are ``(field, value)`` pairs. This tool reports which field labels appear and
groups the pages by their exact set of fields, so that inconsistent tables can
be normalized.

Usage::

    python utils/audit_info_tables.py [--dir docs/graphs/data]
"""

import argparse
import pathlib
import re
from collections import Counter, defaultdict
from typing import Optional, Sequence

__all__ = [
    "info_fields",
    "main",
]

#: The ``Info`` section heading of a per-graph page.
_INFO_HEADING_RE = re.compile(r"^Info\n[=-]+\n", re.MULTILINE)


def info_fields(text: str) -> list[str]:
    """Returns the field labels of the ``Info`` table in a per-graph page.

    The labels are the non-empty first-column cells of the ``list-table`` that
    follows the ``Info`` heading, in order (the empty header row is skipped).

    Parameters
    ----------
    text : str
        The reStructuredText source of a per-graph page.

    Examples
    --------
    >>> info_fields(
    ...     "Info\\n----\\n\\n.. list-table::\\n   :header-rows: 1\\n\\n"
    ...     "   * -\\n     -\\n   * - Full Name\\n     - wc\\n"
    ...     "   * - Version\\n     - 5.0.0\\n\\nGraph Statistics\\n"
    ... )
    ['Full Name', 'Version']

    Returns
    -------
    fields : list[str]
        The field labels of the Info table, in order.
    """
    match = _INFO_HEADING_RE.search(text)
    if not match:
        return []

    rest = text[match.end() :]
    start = rest.find(".. list-table::")
    if start == -1:
        return []

    fields: list[str] = []
    in_rows = False
    for line in rest[start:].splitlines()[1:]:
        stripped = line.strip()
        if not in_rows:
            if stripped.startswith("* -"):
                in_rows = True
                cell = stripped[3:].strip()
                if cell:
                    fields.append(cell)
        elif stripped == "":
            break
        elif stripped.startswith("* -"):
            cell = stripped[3:].strip()
            if cell:
                fields.append(cell)

    return fields


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Audits the per-graph pages and reports their Info-table shapes."""
    parser = argparse.ArgumentParser(
        description="Report the Info-table field labels of the per-graph docs pages."
    )
    parser.add_argument(
        "--dir", default="docs/graphs/data", help="directory of per-graph .rst pages"
    )
    args = parser.parse_args(argv)

    shapes: Counter = Counter()
    by_shape: dict = defaultdict(list)
    field_counts: Counter = Counter()

    for path in sorted(pathlib.Path(args.dir).glob("*.rst")):
        fields = info_fields(path.read_text(encoding="utf-8"))
        shape = tuple(fields)
        shapes[shape] += 1
        by_shape[shape].append(path.name)
        field_counts.update(fields)

    total = sum(shapes.values())
    print(f"Audited {total} pages in {args.dir}\n")

    print("Field label counts:")
    for field, count in field_counts.most_common():
        print(f"  {count:4d}  {field}")

    print("\nDistinct Info-table shapes (most common first):")
    for shape, count in shapes.most_common():
        print(f"  [{count:3d}] {list(shape)}")


if __name__ == "__main__":
    main()
