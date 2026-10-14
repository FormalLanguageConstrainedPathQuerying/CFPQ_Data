"""Builders for graph-archive trees shared by the archive-related tests."""

import pathlib
import tarfile

README = """# g

## What is this graph?
A test graph.

## Source
A test source.

## Construction
Generated.

## Nodes
Two nodes.

## Edges and labels
Label a: one edge.

## Query classes
CFPQ applies.

## License
Apache-2.0.

## Caveats
None.
"""

RESULTS = (
    "%%MatrixMarket matrix coordinate pattern general\n"
    "%%GraphBLAS type bool\n2 2 1\n0 1\n"
)


def _query_dir(
    tree: pathlib.Path, cls: str, name: str, representation: str
) -> pathlib.Path:
    query = tree / "queries" / cls / name
    query.mkdir(parents=True)
    (query / f"{name}{representation}").write_text(
        {
            ".cnf": "S\ta\tN1\nN1\ta\n\nCount:\nS",
            ".rsm": "S -> a*",
            ".re": "a*",
            ".mcfg": "A(a)\nS(x1) <- A(x1)",
        }[representation]
    )
    (query / "results.mtx").write_text(RESULTS)
    return query


def _valid_tree(root: pathlib.Path, name: str = "g") -> pathlib.Path:
    d = root / name
    (d / "graph").mkdir(parents=True)
    for cls in ("cfpq", "rpq", "mcfpq"):
        (d / "queries" / cls).mkdir(parents=True)
    (d / "README.md").write_text(README)
    (d / "graph" / "a.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n2 2 1\n0 1\n"
    )
    _query_dir(d, "cfpq", "s", ".cnf")
    (d / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n- Purpose: test.\n"
    )
    return d


def _partial_tree(root: pathlib.Path, name: str = "g") -> pathlib.Path:
    d = root / name
    _query_dir(d, "cfpq", "s", ".cnf")
    (d / "queries" / "README.md").write_text(
        "# Queries for g\n\n## cfpq/s\n- Language: a*.\n- Purpose: test.\n"
    )
    return d


def _tarball(tree: pathlib.Path, dest: pathlib.Path) -> pathlib.Path:
    with tarfile.open(dest, "w:gz") as tarball:
        tarball.add(tree, arcname=tree.name)
    return dest
