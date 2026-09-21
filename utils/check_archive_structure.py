"""Validate the structure of a graph archive.

Every graph archive must have the same fixed, self-contained structure
(documented in the "File structure" section of ``docs/graphs/index.rst``):
a description document answering the mandatory questions, one Boolean
MatrixMarket file per stored edge label, and all queries of the graph as
separate files grouped by class and described in a common document.

Usage (from any directory)::

    python utils/check_archive_structure.py ARCHIVE.tar.gz
    python utils/check_archive_structure.py UNPACKED_DIR
"""

import argparse
import pathlib
import re
import shutil
import tarfile
import tempfile
from typing import Optional, Sequence, Union

from pyformlang.cfg import CFG
from pyformlang.regular_expression import Regex

from cfpq_data.grammars.readwrite.mcfg import mcfg_from_text
from cfpq_data.graphs.readwrite.mtx import graph_from_mtx_dir

__all__ = [
    "MANDATORY_README_SECTIONS",
    "QUERY_CLASSES",
    "validate_archive",
    "main",
]

#: The questions the archive ``README.md`` must answer (one ``##`` section each).
MANDATORY_README_SECTIONS = (
    "What is this graph?",
    "Source",
    "Construction",
    "Nodes",
    "Edges and labels",
    "Query classes",
    "License",
    "Caveats",
)

#: Query class -> file extension of the query files in ``queries/<class>/``.
QUERY_CLASSES = {"cfpq": ".cnf", "rpq": ".re", "mcfpq": ".mcfg"}

_VARIABLE = re.compile(r"[a-z][0-9]+")


def _query_terminals(path: pathlib.Path, cls: str) -> set[str]:
    """Return the terminals used by one query file.

    Parameters
    ----------
    path : Path
        The query file to read.
    cls : str
        The query class (a key of ``QUERY_CLASSES``).

    Returns
    -------
    terminals : set[str]
        The edge labels the query uses.

    Raises
    ------
    Exception
        If the file cannot be parsed as a query of class ``cls``.
    """
    text = path.read_text(encoding="utf-8")
    if cls == "cfpq":
        cfg = CFG.from_text(text=text)
        return {symbol.value for symbol in cfg.terminals}
    if cls == "rpq":
        regex = Regex(text)
        nfa = regex.to_epsilon_nfa()
        if nfa is None:
            return set()
        return {symbol.value for symbol in nfa.symbols}
    mcfg = mcfg_from_text(text)
    terminals = set()
    for rule in mcfg.rules:
        for arg in rule.head_args:
            for item in arg:
                if item != "eps" and not _VARIABLE.fullmatch(item):
                    terminals.add(item)
    return terminals


def _skeleton_problems(root: pathlib.Path) -> list[str]:
    """Check the fixed archive skeleton under ``root``."""
    problems = []
    entries = {path.name for path in root.iterdir()}
    expected = {"README.md", "graph", "queries"}
    for name in sorted(entries - expected):
        problems.append(f"unexpected entry {name!r} (expected only {sorted(expected)})")
    for name in sorted(expected - entries):
        problems.append(f"missing entry {name!r}")
    if problems:
        return problems

    graph_dir = root / "graph"
    if not any(
        path.suffix == ".mtx" and path.is_file() for path in graph_dir.iterdir()
    ):
        problems.append("graph/ must contain at least one .mtx file")
    for path in sorted(graph_dir.iterdir()):
        if not path.is_file() or path.suffix != ".mtx":
            problems.append(f"graph/{path.name}: only .mtx files are allowed in graph/")

    queries_dir = root / "queries"
    query_entries = {path.name for path in queries_dir.iterdir()}
    query_expected = {"README.md", *QUERY_CLASSES}
    for name in sorted(query_entries - query_expected):
        problems.append(
            f"queries/{name}: unexpected entry (expected only {sorted(query_expected)})"
        )
    for name in sorted(query_expected - query_entries):
        problems.append(f"queries/{name}: missing")
    for cls, ext in QUERY_CLASSES.items():
        cls_dir = queries_dir / cls
        if not cls_dir.is_dir():
            continue
        for path in sorted(cls_dir.iterdir()):
            if not path.is_file() or path.suffix != ext:
                problems.append(
                    f"queries/{cls}/{path.name}: only {ext} files are allowed"
                )
    return problems


def _mtx_range_problems(graph_dir: pathlib.Path) -> list[str]:
    """Check that edge endpoints fit the declared matrix dimensions."""
    problems = []
    for mtx_file in sorted(graph_dir.glob("*.mtx")):
        lines = [
            line
            for line in mtx_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        dim_index = next(
            (i for i, line in enumerate(lines) if not line.startswith("%%")), None
        )
        if dim_index is None:
            continue  # a header problem graph_from_mtx_dir already reports
        try:
            rows, cols, _nnz = (int(value) for value in lines[dim_index].split())
        except ValueError:
            continue  # reported by graph_from_mtx_dir
        for line in lines[dim_index + 1 :]:
            tail, head = (int(value) for value in line.split()[:2])
            if not 0 <= tail < rows or not 0 <= head < cols:
                problems.append(
                    f"graph/{mtx_file.name}: edge ({tail}, {head}) is outside the "
                    f"declared {rows}x{cols} matrix"
                )
                break
    return problems


def _readme_problems(root: pathlib.Path) -> list[str]:
    """Check that README.md answers all the mandatory questions."""
    text = (root / "README.md").read_text(encoding="utf-8")
    headers = {line[3:].strip() for line in text.splitlines() if line.startswith("## ")}
    return [
        f"README.md: missing mandatory section '## {question}'"
        for question in MANDATORY_README_SECTIONS
        if question not in headers
    ]


def _query_problems(root: pathlib.Path) -> list[str]:
    """Check that queries parse, use only own labels, and are all described."""
    problems = []
    queries_dir = root / "queries"
    stored = {path.stem for path in (root / "graph").glob("*.mtx")}

    existing: dict[str, tuple[pathlib.Path, str]] = {}
    for cls, ext in QUERY_CLASSES.items():
        cls_dir = queries_dir / cls
        if not cls_dir.is_dir():
            continue
        for path in sorted(cls_dir.iterdir()):
            if path.is_file() and path.suffix == ext:
                existing[f"{cls}/{path.name}"] = (path, cls)

    for rel, (path, cls) in sorted(existing.items()):
        try:
            terminals = _query_terminals(path, cls)
        except Exception as error:
            problems.append(
                f"queries/{rel}: cannot be parsed as a {cls} query ({error})"
            )
            continue
        if not terminals:
            problems.append(
                f"queries/{rel}: uses no terminal (an empty query is meaningless)"
            )
        for terminal in sorted(terminals):
            reversed_of = terminal[:-2] if terminal.endswith("_r") else None
            if terminal not in stored and (
                reversed_of is None or reversed_of not in stored
            ):
                problems.append(
                    f"queries/{rel}: label {terminal!r} is not a stored label of this graph"
                )

    doc = (queries_dir / "README.md").read_text(encoding="utf-8")
    sections: dict[str, list[str]] = {}
    current = None
    for line in doc.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    for name in sorted(set(sections) - set(existing)):
        problems.append(
            f"queries/README.md: section {name!r} does not match any query file"
        )
    for name in sorted(set(existing) - set(sections)):
        problems.append(f"queries/README.md: no section describing {name!r}")
    for name, body in sections.items():
        if name in existing and not any(line.strip() for line in body):
            problems.append(f"queries/README.md: the section for {name!r} is empty")
    return problems


def _validate_root(root: pathlib.Path) -> list[str]:
    """Validate the unpacked archive directory ``root``."""
    problems = _skeleton_problems(root)
    if problems:
        return problems  # the deeper checks are meaningless without the skeleton
    try:
        graph_from_mtx_dir(root / "graph")
    except (ValueError, OSError) as error:
        problems.append(f"graph/: {error}")
    problems.extend(_mtx_range_problems(root / "graph"))
    problems.extend(_readme_problems(root))
    problems.extend(_query_problems(root))
    return problems


def validate_archive(path: Union[str, pathlib.Path]) -> list[str]:
    """Validate one graph archive (a ``.tar.gz`` or an unpacked directory).

    Parameters
    ----------
    path : Union[str, Path]
        The archive to validate.

    Returns
    -------
    problems : list[str]
        All structure violations found; an empty list means the archive is
        valid.
    """
    path = pathlib.Path(path)
    if path.is_dir():
        return _validate_root(path)
    try:
        is_tar = tarfile.is_tarfile(path)
    except OSError:
        is_tar = False
    if path.suffix != ".gz" or not is_tar:
        return [f"{path.name}: not a .tar.gz archive or an unpacked directory"]

    with tempfile.TemporaryDirectory() as tmp:
        shutil.unpack_archive(path, tmp)
        entries = list(pathlib.Path(tmp).iterdir())
        if len(entries) != 1 or not entries[0].is_dir():
            return [f"{path.name}: must contain a single top-level directory"]
        root = entries[0]
        problems = []
        expected_name = path.name[: -len(".tar.gz")]
        if root.name != expected_name:
            problems.append(
                f"top-level directory {root.name!r} must be named after the "
                f"archive ({expected_name!r})"
            )
        problems.extend(_validate_root(root))
        return problems


def _audit(client, bucket: str, prefix: str) -> list[str]:
    """Validate every ``.tar.gz`` object stored under the bucket prefix."""
    problems = []
    key_prefix = f"{prefix.rstrip('/')}/" if prefix else ""
    objects = []
    for page in client.get_paginator("list_objects_v2").paginate(
        Bucket=bucket, Prefix=key_prefix
    ):
        objects.extend(
            obj["Key"]
            for obj in page.get("Contents", [])
            if obj["Key"].endswith(".tar.gz")
        )
    if not objects:
        problems.append(f"no .tar.gz objects found under s3://{bucket}/{key_prefix}")
        return problems

    with tempfile.TemporaryDirectory() as tmp:
        for object_key in sorted(objects):
            # A per-key sandbox keeps the original file name, which the
            # top-level-directory check depends on.
            sandbox = pathlib.Path(tmp) / object_key.replace("/", "__")
            sandbox.mkdir()
            local = sandbox / pathlib.Path(object_key).name
            client.download_file(bucket, object_key, str(local))
            problems.extend(
                f"{object_key}: {problem}" for problem in validate_archive(local)
            )
    return problems


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Command-line entry point.

    Validates one local graph archive, or — with ``--audit`` — every
    ``.tar.gz`` object under a bucket prefix, and prints every structure
    violation found.

    Returns
    -------
    status : int
        0 when everything is valid, 1 otherwise.
    """
    parser = argparse.ArgumentParser(
        description="Validate the fixed self-contained structure of a graph archive."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="path to a .tar.gz archive or an unpacked archive directory",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="validate every .tar.gz object under --prefix in the bucket instead of a local path",
    )
    parser.add_argument(
        "--prefix", default="", help="bucket prefix to audit (with --audit)"
    )
    parser.add_argument(
        "--access-key-id", default=None, help="Yandex Cloud IAM key ID (with --audit)"
    )
    parser.add_argument(
        "--secret-access-key",
        default=None,
        help="Yandex Cloud IAM secret key (with --audit)",
    )
    parser.add_argument(
        "--endpoint-url",
        default=None,
        help="S3 API endpoint (with --audit; default: the upload tool's)",
    )
    parser.add_argument(
        "--bucket",
        default=None,
        help="target bucket (with --audit; default: the upload tool's)",
    )
    args = parser.parse_args(argv)

    if args.audit:
        from upload_to_s3 import DEFAULT_BUCKET, DEFAULT_ENDPOINT_URL, create_s3_client

        if not args.access_key_id or not args.secret_access_key:
            print(
                "error: --access-key-id and --secret-access-key are required for --audit"
            )
            return 1
        client = create_s3_client(
            args.access_key_id,
            args.secret_access_key,
            args.endpoint_url or DEFAULT_ENDPOINT_URL,
        )
        problems = _audit(client, args.bucket or DEFAULT_BUCKET, args.prefix)
    elif args.path is None:
        print("error: give a path to validate or use --audit")
        return 1
    else:
        problems = validate_archive(args.path)

    if problems:
        for problem in problems:
            print(f"error: {problem}")
        print(f"{len(problems)} structure violation(s) found")
        return 1
    print("archive structure ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
