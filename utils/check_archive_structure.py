"""Validate the structure of a graph archive.

Every graph archive must have the same fixed, self-contained structure
(documented in the "File structure" section of ``docs/graphs/index.rst``):
a description document answering the mandatory questions, one Boolean
MatrixMarket file per stored edge label, and all queries of the graph as
directories grouped by class — each query directory holding every
representation of the query plus one ``results.mtx`` with the constrained
reachability facts — described in a common document.

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
from pyformlang.rsa import RecursiveAutomaton as RSA

from cfpq_data.grammars.converters.cfg import cfg_from_rsa
from cfpq_data.grammars.readwrite.mcfg import mcfg_from_text
from cfpq_data.grammars.readwrite.rsa import rsa_from_text
from cfpq_data.graphs.readwrite.mtx import _MTX_HEADER, graph_from_mtx_dir

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

#: Query class -> file extensions of the representation files in a query directory.
QUERY_CLASSES = {"cfpq": (".cnf", ".rsm"), "rpq": (".re", ".rsm"), "mcfpq": (".mcfg",)}

_VARIABLE = re.compile(r"[a-z][0-9]+")


def _query_terminals(path: pathlib.Path) -> set[str]:
    """Return the terminals used by one query representation file.

    Parameters
    ----------
    path : Path
        The representation file to read (its extension selects the format).

    Returns
    -------
    terminals : set[str]
        The edge labels the query uses.

    Raises
    ------
    Exception
        If the file cannot be parsed as a query of its class.
    """
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".cnf":
        cfg = CFG.from_text(text=text)
        return {symbol.value for symbol in cfg.terminals}
    if path.suffix == ".rsm":
        rsa = rsa_from_text(text)
        cfg = cfg_from_rsa(rsa)
        return {symbol.value for symbol in cfg.terminals}
    if path.suffix == ".re":
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
    for cls, exts in QUERY_CLASSES.items():
        cls_dir = queries_dir / cls
        if not cls_dir.is_dir():
            continue
        for path in sorted(cls_dir.iterdir()):
            if not path.is_dir():
                problems.append(
                    f"queries/{cls}/{path.name}: must be a query directory "
                    "(flat query files are no longer allowed)"
                )
                continue
            problems.extend(_query_dir_problems(path, cls, exts))
    return problems


def _query_dir_problems(
    query_dir: pathlib.Path, cls: str, exts: tuple[str, ...]
) -> list[str]:
    """Check one ``queries/<class>/<query>/`` directory."""
    problems = []
    rel = f"queries/{cls}/{query_dir.name}"
    has_representation = False
    for path in sorted(query_dir.iterdir()):
        if not path.is_file():
            problems.append(f"{rel}/{path.name}: only files are allowed")
            continue
        if path.name == "results.mtx":
            continue
        if path.suffix not in exts:
            problems.append(
                f"{rel}/{path.name}: only {' '.join(exts)} representation files "
                "and results.mtx are allowed"
            )
            continue
        has_representation = True
    if not has_representation:
        problems.append(f"{rel}/: no {cls} representation file ({' or '.join(exts)})")
    if not (query_dir / "results.mtx").is_file():
        problems.append(f"{rel}/: missing results.mtx")
    return problems


def _read_mtx(path: pathlib.Path) -> Optional[tuple[int, int, list[tuple[int, int]]]]:
    """Parse one Boolean MatrixMarket file into (rows, cols, entries).

    Returns None when the file does not follow the dataset format (the
    two-line header, a dimension line, and integer entry lines).
    """
    lines = [
        line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    if len(lines) < 3 or tuple(lines[:2]) != _MTX_HEADER:
        return None
    try:
        rows, cols, nnz = (int(value) for value in lines[2].split())
        entries = [(int(line.split()[0]), int(line.split()[1])) for line in lines[3:]]
    except ValueError:
        return None
    if len(entries) != nnz:
        return None
    return rows, cols, entries


def _graph_dimensions(graph_dir: pathlib.Path) -> set[tuple[int, int]]:
    """The declared dimensions of every parseable graph label matrix."""
    dimensions = set()
    for mtx_file in sorted(graph_dir.glob("*.mtx")):
        parsed = _read_mtx(mtx_file)
        if parsed is not None:
            dimensions.add((parsed[0], parsed[1]))
    return dimensions


def _mtx_range_problems(graph_dir: pathlib.Path) -> list[str]:
    """Check that edge endpoints fit the declared matrix dimensions."""
    problems = []
    for mtx_file in sorted(graph_dir.glob("*.mtx")):
        parsed = _read_mtx(mtx_file)
        if parsed is None:
            continue  # a format problem graph_from_mtx_dir already reports
        rows, cols, entries = parsed
        for tail, head in entries:
            if not 0 <= tail < rows or not 0 <= head < cols:
                problems.append(
                    f"graph/{mtx_file.name}: edge ({tail}, {head}) is outside the "
                    f"declared {rows}x{cols} matrix"
                )
                break
    dimensions = _graph_dimensions(graph_dir)
    if len(dimensions) > 1:
        problems.append(
            "graph/: all label matrices must declare the same dimensions "
            f"(found {sorted(dimensions)})"
        )
    return problems


def _results_problems(root: pathlib.Path) -> list[str]:
    """Check every per-query results.mtx against the graph."""
    problems = []
    dimensions = _graph_dimensions(root / "graph")
    if len(dimensions) != 1:
        return problems  # the matrix shape is undefined; already reported
    expected = next(iter(dimensions))

    queries_dir = root / "queries"
    for cls in QUERY_CLASSES:
        cls_dir = queries_dir / cls
        if not cls_dir.is_dir():
            continue
        for query_dir in sorted(cls_dir.iterdir()):
            if not query_dir.is_dir():
                continue
            results = query_dir / "results.mtx"
            rel = f"queries/{cls}/{query_dir.name}/results.mtx"
            parsed = _read_mtx(results)
            if parsed is None:
                problems.append(
                    f"{rel}: cannot be parsed as a Boolean MatrixMarket file"
                )
                continue
            rows, cols, entries = parsed
            if (rows, cols) != expected:
                problems.append(
                    f"{rel}: must be a {expected[0]}x{expected[1]} matrix "
                    f"(the graph declares {expected[0]}x{expected[1]})"
                )
                continue
            for tail, head in entries:
                if not 0 <= tail < rows or not 0 <= head < cols:
                    problems.append(
                        f"{rel}: entry ({tail}, {head}) is outside the declared "
                        f"{rows}x{cols} matrix"
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


def _rsm_recurses(rsa: RSA) -> bool:
    """Whether any box transition is labelled by a nonterminal (box name)."""
    names = {label.value for label in rsa.labels}
    for label in rsa.labels:
        box = rsa.get_box(label)
        if box is not None and any(symbol.value in names for symbol in box.dfa.symbols):
            return True
    return False


def _query_problems(root: pathlib.Path) -> list[str]:
    """Check that queries parse, use only own labels, and are all described."""
    problems = []
    queries_dir = root / "queries"
    stored = {path.stem for path in (root / "graph").glob("*.mtx")}

    existing: dict[str, tuple[str, list[pathlib.Path]]] = {}
    for cls, exts in QUERY_CLASSES.items():
        cls_dir = queries_dir / cls
        if not cls_dir.is_dir():
            continue
        for query_dir in sorted(cls_dir.iterdir()):
            if not query_dir.is_dir():
                continue  # reported by the skeleton check
            representations = [
                path
                for path in sorted(query_dir.iterdir())
                if path.is_file() and path.suffix in exts
            ]
            existing[f"{cls}/{query_dir.name}"] = (cls, representations)

    for rel, (cls, representations) in sorted(existing.items()):
        for path in representations:
            where = f"queries/{rel}/{path.name}"
            try:
                terminals = _query_terminals(path)
            except Exception as error:
                problems.append(f"{where}: cannot be parsed as a {cls} query ({error})")
                continue
            if not terminals:
                problems.append(
                    f"{where}: uses no terminal (an empty query is meaningless)"
                )
            for terminal in sorted(terminals):
                reversed_of = terminal[:-2] if terminal.endswith("_r") else None
                if terminal not in stored and (
                    reversed_of is None or reversed_of not in stored
                ):
                    problems.append(
                        f"{where}: label {terminal!r} is not a stored "
                        "label of this graph"
                    )
            if cls == "rpq" and path.suffix == ".rsm":
                try:
                    rsa = rsa_from_text(path.read_text(encoding="utf-8"))
                except Exception:
                    continue  # already reported above
                if _rsm_recurses(rsa):
                    problems.append(
                        f"{where}: an rpq query must be regular (no box "
                        "transition may be labelled by a nonterminal)"
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
            f"queries/README.md: section {name!r} does not match any query directory"
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
    problems.extend(_results_problems(root))
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
        help=(
            "validate every .tar.gz object under --prefix in the bucket "
            "instead of a local path"
        ),
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
                "error: --access-key-id and --secret-access-key are "
                "required for --audit"
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
