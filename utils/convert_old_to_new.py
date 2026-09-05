"""Convert old-format graph archives to the nab-like mtx-per-label format.

The old format stores a whole graph in one CSV file (``<name>/<name>.csv``,
space-separated ``from to label`` lines with CRLF endings). The new format
stores one Boolean MatrixMarket matrix per edge label
(``<name>/graph/<label>.mtx``) plus CNF grammar files
(``<name>/grammar/*.cnf``) and a README.

The tool processes graphs one by one: it downloads a single old-format
archive from the public bucket (``4.0.0/graph/``, where the old archives
stay), converts it locally, verifies the conversion by round-trip, uploads
the new archive under the ``5.0.0/graph/`` key prefix, and removes the local
files. At most one graph is on disk at any time.
"""

import argparse
import datetime
import json
import logging
import os
import pathlib
import re
import shutil
import tarfile
import tempfile
from dataclasses import dataclass, field
from typing import Dict, IO, Iterator, List, Optional, Sequence, Set, Tuple, Union

import requests
from botocore.client import BaseClient

from cfpq_data.dataset import (
    DATASET_KEY_PREFIX,
    DATASET_URL,
    LEGACY_DATASET_URL,
)
from cfpq_data.grammars.generators.c_alias_grammar import c_alias_grammar
from cfpq_data.grammars.generators.nested_parentheses_grammar import (
    nested_parentheses_grammar,
)
from migrate_gdrive_to_s3 import sha256_of
from upload_to_s3 import (
    DEFAULT_BUCKET,
    DEFAULT_ENDPOINT_URL,
    create_s3_client,
    upload_file,
)

__all__ = [
    "MTX_BANNER",
    "MTX_TYPE",
    "GraphStats",
    "iter_edges",
    "scan_csv",
    "convert_csv_to_graph_dir",
    "validate_labels",
    "JAVA_TEMPLATE",
    "JAVA_START",
    "cnf_lite",
    "write_cnf",
    "java_points_to_cnf",
    "c_alias_cnf",
    "rdf_cnf_grammars",
    "instantiate_template",
    "ConversionError",
    "render_readme",
    "build_archive",
    "verify_conversion",
    "make_tarball",
    "SECTIONS",
    "DEFAULT_KEY_PREFIX",
    "download_graph",
    "verify_public_read",
    "load_record",
    "save_record",
    "convert_one",
    "main",
]

MTX_BANNER = "%%MatrixMarket matrix coordinate pattern general"
MTX_TYPE = "%%GraphBLAS type bool"


@dataclass
class GraphStats:
    """Statistics of a graph collected from its edge list.

    Attributes
    ----------
    num_nodes : int
        Number of distinct node IDs occurring in the edges.
    max_node_id : int
        The largest node ID occurring in the edges.
    total_edges : int
        Total number of edges (one per CSV line).
    edges_per_label : dict[str, int]
        Number of edges per label.
    """

    num_nodes: int
    max_node_id: int
    total_edges: int
    edges_per_label: Dict[str, int] = field(default_factory=dict)


def iter_edges(csv_path: Union[pathlib.Path, str]) -> Iterator[Tuple[int, int, str]]:
    """Yield the edges of an old-format graph CSV file.

    Parameters
    ----------
    csv_path : Union[Path, str]
        Path to the CSV file with one edge per line in the format
        ``<from> <to> <label>``. The source files use CRLF line endings;
        both CRLF and LF are accepted. Blank lines are skipped.

    Yields
    ------
    edge : Tuple[int, int, str]
        A triple ``(u, v, label)`` with 0-based integer node IDs.

    Raises
    ------
    ValueError
        If a non-blank line does not have exactly three
        whitespace-separated fields or the node IDs are not integers.
    """
    with open(csv_path, "r") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(
                    f"{csv_path}:{line_no}: expected 3 fields "
                    f"('<from> <to> <label>'), got {len(parts)}: {line!r}"
                )
            u_str, v_str, label = parts
            try:
                u, v = int(u_str), int(v_str)
            except ValueError:
                raise ValueError(
                    f"{csv_path}:{line_no}: node IDs must be integers: {line!r}"
                ) from None
            yield u, v, label


def scan_csv(csv_path: Union[pathlib.Path, str]) -> GraphStats:
    """Collect the statistics of an old-format graph CSV file.

    Parameters
    ----------
    csv_path : Union[Path, str]
        Path to the CSV file (see :func:`iter_edges`).

    Returns
    -------
    stats : GraphStats
        Distinct node count, max node ID, total edge count, and per-label
        edge counts.
    """
    nodes = set()
    edges_per_label: Dict[str, int] = {}
    total_edges = 0
    max_node_id = -1

    for u, v, label in iter_edges(csv_path):
        nodes.add(u)
        nodes.add(v)
        if u > max_node_id:
            max_node_id = u
        if v > max_node_id:
            max_node_id = v
        edges_per_label[label] = edges_per_label.get(label, 0) + 1
        total_edges += 1

    stats = GraphStats(
        num_nodes=len(nodes),
        max_node_id=max_node_id,
        total_edges=total_edges,
        edges_per_label=edges_per_label,
    )

    logging.info(f"Scanned {csv_path=}: {stats=}")
    return stats


def validate_labels(labels) -> None:
    """Validate that labels can be used as MTX file names.

    Parameters
    ----------
    labels : iterable of str
        The edge labels of the graph.

    Raises
    ------
    ValueError
        If a label is empty, starts with ``-``, or contains a slash,
        whitespace, or NUL character.
    """
    for label in labels:
        if (
            not label
            or label.startswith("-")
            or "/" in label
            or "\x00" in label
            or any(c.isspace() for c in label)
        ):
            raise ValueError(f"Label {label!r} is not filesystem-safe")


def convert_csv_to_graph_dir(
    csv_path: Union[pathlib.Path, str],
    graph_dir: Union[pathlib.Path, str],
) -> GraphStats:
    """Convert an old-format graph CSV to per-label MTX files.

    For every distinct label ``L`` the function writes
    ``<graph_dir>/<L>.mtx``::

        %%MatrixMarket matrix coordinate pattern general
        %%GraphBLAS type bool
        <N> <N> <nnz>
        <u> <v>
        ...

    where ``N = max_node_id + 1`` and one entry line follows per edge with
    label ``L``, in the order the edges appear in the CSV. Node IDs are
    written verbatim (0-based). The conversion streams the CSV twice and
    keeps O(1) data in memory, so it works for graphs with tens of millions
    of edges.

    Parameters
    ----------
    csv_path : Union[Path, str]
        Path to the old-format CSV file (see :func:`iter_edges`).
    graph_dir : Union[Path, str]
        Directory where the ``<label>.mtx`` files are written. Created if
        it does not exist.

    Returns
    -------
    stats : GraphStats
        The statistics collected from the CSV (see :func:`scan_csv`).

    Raises
    ------
    ValueError
        If a label is not filesystem-safe (see :func:`validate_labels`).
    """
    stats = scan_csv(csv_path)
    validate_labels(stats.edges_per_label)

    n = stats.max_node_id + 1
    graph_dir = pathlib.Path(graph_dir)
    graph_dir.mkdir(parents=True, exist_ok=True)

    handles: Dict[str, IO[str]] = {}
    try:
        for label, nnz in stats.edges_per_label.items():
            handle = open(graph_dir / f"{label}.mtx", "w")
            handle.write(f"{MTX_BANNER}\n{MTX_TYPE}\n{n} {n} {nnz}\n")
            handles[label] = handle
        for u, v, label in iter_edges(csv_path):
            handles[label].write(f"{u} {v}\n")
    finally:
        for handle in handles.values():
            handle.close()

    logging.info(f"Converted {csv_path=} to {graph_dir=}: {stats=}")
    return stats


# ---------------------------------------------------------------------------
# Grammar generation
# ---------------------------------------------------------------------------

#: The compact Java points-to template shared by all new-format java archives
#: (byte-identical to ``gson/grammar/java_points_to.cnf`` except that the
#: indexed symbols carry no ``_i`` placeholder: the index is not part of the
#: symbol name, it sits in the label — ``load`` matches ``load_<k>``,
#: ``store_r`` matches ``store_<k>_r``). Rule order matches the family file.
JAVA_TEMPLATE: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("PT", ("PTh", "alloc")),
    ("PTh", ("assign", "PTh")),
    ("FT", ("alloc_r", "FTh")),
    ("FTh", ("assign_r", "FTh")),
    ("Al", ("PT", "FT")),
    ("PT", ("alloc",)),
    ("FT", ("alloc_r",)),
    ("PTh", ("assign",)),
    ("FTh", ("assign_r",)),
    ("PTh", ("load", "Al_st_PTh")),
    ("FTh", ("store_r", "Al_ld_r_FTh")),
    ("Al_st_PTh", ("Al", "st_PTh")),
    ("Al_ld_r_FTh", ("Al", "ld_r_FTh")),
    ("st_PTh", ("store", "PTh")),
    ("ld_r_FTh", ("load_r", "FTh")),
    ("PTh", ("load", "Al_store")),
    ("Al_store", ("Al", "store")),
    ("FTh", ("store_r", "Al_load_r")),
    ("Al_load_r", ("Al", "load_r")),
)

JAVA_START = "PT"


def cnf_lite(productions: List[Tuple[str, Tuple[str, ...]]]):
    """Break productions with a right-hand side of more than two symbols.

    The ``.cnf`` format allows at most two symbols on the right-hand side.
    Every longer production ``L -> X1 ... Xn`` is replaced by the chain
    ``L -> X1 N1``, ``N1 -> X2 N2``, ..., ``Nk-1 -> X(n-1) Xn`` with fresh
    auxiliary non-terminals ``N1..Nk-1`` allocated in processing order.
    Productions of length at most two and epsilon productions pass through
    unchanged, so the result generates the same language.

    Parameters
    ----------
    productions : list of (str, tuple of str)
        The productions as ``(lhs, rhs)`` pairs in the desired output order.

    Returns
    -------
    list of (str, tuple of str)
        The productions with every right-hand side of length at most two.
    """
    result: List[Tuple[str, Tuple[str, ...]]] = []
    aux_counter = 0
    for lhs, rhs in productions:
        if len(rhs) <= 2:
            result.append((lhs, rhs))
            continue
        prev = lhs
        for i in range(len(rhs) - 2):
            aux_counter += 1
            aux = f"N{aux_counter}"
            result.append((prev, (rhs[i], aux)))
            prev = aux
        result.append((prev, rhs[-2:]))
    return result


def write_cnf(
    productions: List[Tuple[str, Tuple[str, ...]]],
    start_symbol: str,
    path: Union[pathlib.Path, str],
) -> None:
    """Write a grammar in the ``.cnf`` format of the new-format archives.

    One production per line, symbols separated by tabs; an epsilon
    production is a bare non-terminal. The last two lines are ``Count:`` and
    the start symbol, preceded by a blank line.

    Parameters
    ----------
    productions : list of (str, tuple of str)
        The productions as ``(lhs, rhs)`` pairs in the desired output order.
    start_symbol : str
        The start non-terminal.
    path : Union[Path, str]
        Where the ``.cnf`` file is written.
    """
    lines = ["\t".join([lhs, *rhs]) for lhs, rhs in productions]
    lines += ["", "Count:", start_symbol]
    pathlib.Path(path).write_text("\n".join(lines) + "\n")


def _cfg_productions(cfg) -> List[Tuple[str, Tuple[str, ...]]]:
    """The productions of a pyformlang CFG as sorted ``(lhs, rhs)`` strings.

    The canonical order (sorted by left-hand side, then right-hand side)
    makes the generated ``.cnf`` files deterministic.
    """
    return sorted(
        (
            (production.head.to_text(), tuple(s.to_text() for s in production.body))
            for production in cfg.productions
        ),
        key=lambda production: (production[0], production[1]),
    )


def java_points_to_cnf(labels) -> Tuple[List[Tuple[str, Tuple[str, ...]]], str]:
    """The compact Java points-to grammar template of the new format.

    The template is fixed and independent of the concrete field indices: the
    indexed symbols ``load``, ``store``, ``load_r``, ``store_r`` (and the six
    auxiliary non-terminals) are resolved against the graph's labels
    ``load_<k>``, ``store_<k>``, ``load_<k>_r``, ``store_<k>_r`` at parse
    time. Reversed (``_r``) edges are not stored in the archive; they are
    derived by reversing the respective forward edges.

    Parameters
    ----------
    labels : iterable of str
        The edge labels of the graph. Must contain at least one ``load_<k>``
        and one ``store_<k>`` label.

    Returns
    -------
    (productions, start_symbol) : (list of (str, tuple of str), str)
        The template productions in family rule order and the start symbol.

    Raises
    ------
    ValueError
        If no ``load_<k>`` or no ``store_<k>`` label is present.
    """
    labels = set(labels)
    if not any(re.fullmatch(r"load_\d+", label) for label in labels):
        raise ValueError("No 'load_<k>' label found; not a java points-to graph")
    if not any(re.fullmatch(r"store_\d+", label) for label in labels):
        raise ValueError("No 'store_<k>' label found; not a java points-to graph")
    return list(JAVA_TEMPLATE), JAVA_START


def c_alias_cnf() -> Tuple[List[Tuple[str, Tuple[str, ...]]], str]:
    """The C alias grammar in the ``.cnf`` format.

    The canonical :func:`c_alias_grammar` (labels ``a``, ``a_r``, ``d``,
    ``d_r``) converted with :func:`cnf_lite`; no indexed symbols.

    Returns
    -------
    (productions, start_symbol) : (list of (str, tuple of str), str)
    """
    cfg = c_alias_grammar()
    return cnf_lite(_cfg_productions(cfg)), cfg.start_symbol.to_text()


#: The three canonical nested-parentheses grammars of every RDF graph page:
#: filename -> opening/closing label pairs (reversed edge first, as on the
#: docs pages).
RDF_GRAMMAR_TYPES = {
    "nested_parentheses_subClassOf_type.cnf": [
        ("subClassOf_r", "subClassOf"),
        ("type_r", "type"),
    ],
    "nested_parentheses_subClassOf.cnf": [("subClassOf_r", "subClassOf")],
    "nested_parentheses_type.cnf": [("type_r", "type")],
}


def rdf_cnf_grammars(
    labels,
) -> Dict[str, Tuple[List[Tuple[str, Tuple[str, ...]]], str]]:
    """The canonical nested-parentheses grammars of an RDF graph.

    The combined subClassOf+type grammar and the two single-type grammars are
    always included; the broaderTransitive grammar is included iff the graph
    has ``broaderTransitive`` edges. Each grammar is
    :func:`nested_parentheses_grammar` with ``eps=False`` converted with
    :func:`cnf_lite`; no indexed symbols.

    Parameters
    ----------
    labels : iterable of str
        The edge labels of the graph.

    Returns
    -------
    dict of str -> (list of (str, tuple of str), str)
        Grammar file name -> (productions, start symbol).
    """
    labels = set(labels)
    grammars: Dict[str, Tuple[List[Tuple[str, Tuple[str, ...]]], str]] = {}
    for filename, types in RDF_GRAMMAR_TYPES.items():
        cfg = nested_parentheses_grammar(types, eps=False)
        grammars[filename] = (
            cnf_lite(_cfg_productions(cfg)),
            cfg.start_symbol.to_text(),
        )
    if "broaderTransitive" in labels:
        cfg = nested_parentheses_grammar(
            [("broaderTransitive", "broaderTransitive_r")], eps=False
        )
        grammars["nested_parentheses_broaderTransitive.cnf"] = (
            cnf_lite(_cfg_productions(cfg)),
            cfg.start_symbol.to_text(),
        )
    return grammars


def instantiate_template(
    template: List[Tuple[str, Tuple[str, ...]]],
    index_sets: Dict[str, Set[int]],
) -> List[Tuple[str, Tuple[str, ...]]]:
    """Expand the indexed symbols of a template per concrete index.

    For every production, each symbol present in ``index_sets`` is replaced
    by ``S_<k>`` (or ``S'_<k>_r`` when the symbol ends in ``_r``, so that
    ``load_r`` with ``k=0`` becomes the label ``load_0_r``) for every ``k``
    in the union of the index sets of the production's indexed symbols.
    Productions without indexed symbols pass through unchanged; a production
    referencing a label that does not exist is inert (the family behavior,
    cf. gson with 380 ``load_i_*`` vs 385 ``store_i_*`` labels).

    This helper is used to verify the template against the package grammar
    generators; the ``.cnf`` files store the unexpanded template.

    Parameters
    ----------
    template : list of (str, tuple of str)
        The template productions with placeholder indexed symbols.
    index_sets : dict of str -> set of int
        Indexed symbol -> the concrete indices present in the graph.

    Returns
    -------
    list of (str, tuple of str)
        The expanded productions.
    """
    result: List[Tuple[str, Tuple[str, ...]]] = []
    for lhs, rhs in template:
        indexed = [symbol for symbol in {lhs, *rhs} if symbol in index_sets]
        if not indexed:
            result.append((lhs, rhs))
            continue
        indices = sorted(set().union(*(index_sets[symbol] for symbol in indexed)))

        def instantiate(symbol: str, k: int) -> str:
            if symbol not in index_sets:
                return symbol
            if symbol.endswith("_r"):
                return f"{symbol[:-2]}_{k}_r"
            return f"{symbol}_{k}"

        for k in indices:
            result.append(
                (instantiate(lhs, k), tuple(instantiate(symbol, k) for symbol in rhs))
            )
    return result


# ---------------------------------------------------------------------------
# Archive assembly and verification
# ---------------------------------------------------------------------------


class ConversionError(Exception):
    """The conversion of a graph failed verification."""


#: The README boilerplate of the new-format archives (nab's README), with
#: ``{name}``, ``{year}``, ``{num_nodes}``, ``{num_edges}`` and
#: ``{label_conventions}`` placeholders.
README_TEMPLATE = """\
%%MatrixMarket matrix coordinate pattern general
%-------------------------------------------------------------------------------
% name: {name}
% date: {year}
% fields: title A name date kind
% kind: Context-free path querying
%
% Graph Statistics:
% Num Nodes: {num_nodes}
% Num Edges: {num_edges}
%
% Terminology:
% 1. A Boolean matrix is a matrix whose elements belong to the set {{0, 1}}.
%
% 2. A Boolean decomposition of a graph adjacency matrix is a set of Boolean
% matrices matching the original matrix, where each matrix corresponds to a
% particular label. Thus, each Boolean matrix contains units in those cells where
% the original matrix contains its corresponding label.
% Example:
%
% Graph:
% (0) --[a]-> (1)
%  |           ^
% [b]    [a]--/
%  |  --/
%  v /
% (2) --[b]-> (3)
%
% Adjacency matrix decomposition of this graph consists of:
% * Adjacency matrix for the label a:
%       0   1   2   3
%   0 |   | t |   |   |
%   1 |   |   |   |   |
%   2 |   | t |   |   |
%   3 |   |   |   |   |
% * Adjacency matrix for the label b:
%       0   1   2   3
%   0 |   |   | t |   |
%   1 |   |   |   |   |
%   2 |   |   |   | t |
%   3 |   |   |   |   |
%
% 3. Context-free path query is a query asking for pairs of endpoints in the graph
% that are connected by a path deduced from the start non-terminal.
%
% All files in this directory are Boolean matrices in mtx
% format, with the file name reflecting the label.
% In addition to the graph itself, there is also a grammar in the cnf format
% for this graph in the "grammar" directory.
%
% The cnf grammar file format:
% - Each non-empty line represents a rule, except the last two lines.
% - Complex rules are in the format: <NON_TERMINAL> <SYMBOL_1> <SYMBOL_2>
% - Simple rules are in the format: <NON_TERMINAL> <SYMBOL_1>
% - Epsilon rules are in the format: <NON_TERMINAL>
% - Whitespace characters are used to separate values on one line
% - The last two lines specify the starting non-terminal in the format:
%   Count:
%   <START_NON_TERMINAL>
{label_conventions}
%-------------------------------------------------------------------------------
"""


def render_readme(
    name: str,
    num_nodes: int,
    num_edges: int,
    *,
    has_reversed_labels: bool = False,
    indexed_symbols: Sequence[str] = (),
) -> str:
    """Render the README of a new-format graph archive.

    The nab boilerplate with the graph statistics filled in, plus a
    "Label conventions" section with only the lines that apply: the indexed
    symbol line when ``indexed_symbols`` is non-empty and the ``_r``
    reversed-edge line when ``has_reversed_labels`` is set.

    Parameters
    ----------
    name : str
        The graph name.
    num_nodes : int
        The number of distinct node IDs (README "Num Nodes").
    num_edges : int
        The number of stored edges (README "Num Edges"; reversed ``_r``
        edges are not stored and not counted).
    has_reversed_labels : bool, optional
        Whether the grammars reference ``_r`` terminals whose edges are
        derived by reversing the respective forward edges.
    indexed_symbols : Sequence[str], optional
        The indexed symbols of the grammars (e.g. ``load``, ``store_r``).

    Returns
    -------
    str
        The README text.
    """
    lines: List[str] = []
    if indexed_symbols:
        patterns = [
            f"{symbol[:-2]}_<k>_r" if symbol.endswith("_r") else f"{symbol}_<k>"
            for symbol in indexed_symbols
        ]
        lines.append(
            "% - Indexed symbols " + ", ".join(indexed_symbols) + " match the labels"
        )
        lines.append("%   " + ", ".join(patterns) + " for each index k.")
    if has_reversed_labels:
        lines.append("% - Edges with the _r suffix are not stored; they are derived by")
        lines.append("%   reversing the respective edges without the suffix.")
    label_conventions = "\n% Label conventions:\n" + "\n".join(lines) if lines else ""
    return README_TEMPLATE.format(
        name=name,
        year=datetime.date.today().year,
        num_nodes=num_nodes,
        num_edges=num_edges,
        label_conventions=label_conventions,
    )


def _section_grammars(
    section: str, labels: Set[str]
) -> Tuple[Dict[str, Tuple[List[Tuple[str, Tuple[str, ...]]], str]], List[str]]:
    """The grammar files and indexed symbols of a graph section.

    Returns
    -------
    (grammars, indexed_symbols) :
        file name -> (productions, start symbol), and the indexed symbols
        referenced by the grammars.
    """
    if section == "java_points_to":
        return (
            {"java_points_to.cnf": java_points_to_cnf(labels)},
            ["load", "store", "load_r", "store_r"],
        )
    if section == "c_alias":
        return {"c_alias.cnf": c_alias_cnf()}, []
    if section == "rdf":
        return rdf_cnf_grammars(labels), []
    raise ValueError(f"Unknown section {section!r}")


def build_archive(
    name: str,
    section: str,
    csv_path: Union[pathlib.Path, str],
    workdir: Union[pathlib.Path, str],
) -> Tuple[pathlib.Path, GraphStats]:
    """Assemble the new-format archive tree of one graph.

    Creates ``<workdir>/<name>/`` with ``README.md``, ``grammar/*.cnf`` (the
    section's canonical grammars) and ``graph/<label>.mtx`` (one Boolean
    matrix per stored edge label). An existing tree is replaced.

    Parameters
    ----------
    name : str
        The graph name (top-level directory of the archive).
    section : str
        One of ``java_points_to``, ``c_alias``, ``rdf`` — selects the
        grammar files.
    csv_path : Union[Path, str]
        The old-format CSV file of the graph.
    workdir : Union[Path, str]
        The directory where the tree is created.

    Returns
    -------
    (tree_dir, stats) : (Path, GraphStats)
        The tree directory and the statistics collected from the CSV.
    """
    tree_dir = pathlib.Path(workdir) / name
    if tree_dir.exists():
        shutil.rmtree(tree_dir)
    tree_dir.mkdir(parents=True)

    stats = convert_csv_to_graph_dir(csv_path, tree_dir / "graph")

    labels = set(stats.edges_per_label)
    grammars, indexed_symbols = _section_grammars(section, labels)
    grammar_dir = tree_dir / "grammar"
    grammar_dir.mkdir()
    for filename, (productions, start_symbol) in grammars.items():
        write_cnf(productions, start_symbol, grammar_dir / filename)

    has_reversed_labels = any(
        symbol.endswith("_r")
        for productions, _ in grammars.values()
        for lhs, rhs in productions
        for symbol in [lhs, *rhs]
    )
    (tree_dir / "README.md").write_text(
        render_readme(
            name,
            stats.num_nodes,
            stats.total_edges,
            has_reversed_labels=has_reversed_labels,
            indexed_symbols=indexed_symbols,
        )
    )

    logging.info(f"Built archive tree {tree_dir=} for {name=}: {stats=}")
    return tree_dir, stats


def verify_conversion(
    csv_path: Union[pathlib.Path, str],
    tree_dir: Union[pathlib.Path, str],
) -> None:
    """Verify that a converted archive tree matches its source CSV.

    Checks, with O(1) memory (streaming passes over the CSV):

    - the ``.mtx`` file set equals the CSV label set;
    - every ``.mtx`` file has the family banner and type line, a header
      ``<N> <N> <nnz>`` with ``N = max_node_id + 1`` and ``nnz`` equal to
      the number of edges of that label;
    - the entries of every ``.mtx`` file equal the CSV edges of that label,
      in order (duplicates included);
    - no ``.mtx`` file has extra entries.

    Parameters
    ----------
    csv_path : Union[Path, str]
        The old-format CSV file the tree was converted from.
    tree_dir : Union[Path, str]
        The archive tree to verify (``<name>/graph/*.mtx``).

    Raises
    ------
    ConversionError
        If any check fails, with a message naming the offending label and
        the mismatch.
    """
    graph_dir = pathlib.Path(tree_dir) / "graph"
    stats = scan_csv(csv_path)
    n = stats.max_node_id + 1

    mtx_files = {path.stem for path in graph_dir.glob("*.mtx")}
    if set(stats.edges_per_label) != mtx_files:
        raise ConversionError(
            f"MTX file set {sorted(mtx_files)} != label set "
            f"{sorted(stats.edges_per_label)}"
        )

    handles: Dict[str, IO[str]] = {}
    try:
        for label, nnz in stats.edges_per_label.items():
            handle = open(graph_dir / f"{label}.mtx")
            if (banner := handle.readline().rstrip("\n")) != MTX_BANNER:
                raise ConversionError(f"{label}: bad banner line {banner!r}")
            if (type_line := handle.readline().rstrip("\n")) != MTX_TYPE:
                raise ConversionError(f"{label}: bad type line {type_line!r}")
            parts = handle.readline().split()
            if len(parts) != 3:
                raise ConversionError(f"{label}: bad header line")
            rows, cols, header_nnz = (int(part) for part in parts)
            if (rows, cols) != (n, n):
                raise ConversionError(
                    f"{label}: matrix dimension {rows}x{cols} != {n}x{n}"
                )
            if header_nnz != nnz:
                raise ConversionError(
                    f"{label}: header nnz {header_nnz} != {nnz} edges"
                )
            handles[label] = handle

        for u, v, label in iter_edges(csv_path):
            line = handles[label].readline()
            if not line:
                raise ConversionError(f"{label}: entry ({u}, {v}) missing")
            entry_u, entry_v = (int(part) for part in line.split())
            if (entry_u, entry_v) != (u, v):
                raise ConversionError(
                    f"{label}: entry ({entry_u}, {entry_v}) != CSV edge ({u}, {v})"
                )

        for label, handle in handles.items():
            if extra := handle.readline():
                raise ConversionError(f"{label}: extra entries after {extra!r}")
    finally:
        for handle in handles.values():
            handle.close()

    logging.info(f"Verified conversion of {csv_path=} to {tree_dir=}")


def make_tarball(
    tree_dir: Union[pathlib.Path, str], dest_path: Union[pathlib.Path, str]
) -> pathlib.Path:
    """Pack an archive tree into a ``.tar.gz`` with the family layout.

    The top-level entry is the tree's own directory name (as in the bucket
    archives); directory and file members are added in sorted order for a
    deterministic layout.

    Parameters
    ----------
    tree_dir : Union[Path, str]
        The archive tree to pack (``<name>/README.md``, ...).
    dest_path : Union[Path, str]
        Where the ``.tar.gz`` file is written.

    Returns
    -------
    Path
        The path of the written tarball.
    """
    tree_dir = pathlib.Path(tree_dir)
    members: List[pathlib.Path] = [tree_dir]
    for dirpath, dirnames, filenames in os.walk(tree_dir):
        dirnames.sort()
        for dirname in dirnames:
            members.append(pathlib.Path(dirpath) / dirname)
        for filename in sorted(filenames):
            members.append(pathlib.Path(dirpath) / filename)

    dest_path = pathlib.Path(dest_path)
    with tarfile.open(dest_path, "w:gz") as tarball:
        for member in members:
            tarball.add(
                member,
                arcname=member.relative_to(tree_dir.parent).as_posix(),
                recursive=False,
            )

    logging.info(f"Packed {tree_dir=} into {dest_path=}")
    return dest_path


# ---------------------------------------------------------------------------
# S3 pipeline and CLI
# ---------------------------------------------------------------------------

#: The key prefix the converted archives are uploaded under (the new dataset
#: version; the old archives stay under ``4.0.0/graph/``).
DEFAULT_KEY_PREFIX = "5.0.0/graph"

#: The base URL of the public bucket (derived from DATASET_URL, the single
#: source of truth for the bucket host).
STORAGE_BASE_URL = DATASET_URL[: DATASET_URL.index(DATASET_KEY_PREFIX)]

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
DEFAULT_RECORD_PATH = SCRIPT_DIR / "conversion_record.json"

#: The graphs to convert, by section (verified against the 4.0.0 bucket:
#: exactly these archives are still in the old format).
SECTIONS: Dict[str, List[str]] = {
    "rdf": [
        "generations",
        "travel",
        "skos",
        "univ",
        "foaf",
        "atom",
        "people",
        "biomedical",
        "pizza",
        "wine",
        "funding",
        "core",
        "pathways",
        "go_hierarchy",
        "enzyme",
        "geospecies",
        "go",
        "eclass",
        "taxonomy_hierarchy",
        "taxonomy",
    ],
    "c_alias": [
        "wc",
        "bzip",
        "pr",
        "ls",
        "gzip",
        "apache",
        "init",
        "mm",
        "ipc",
        "lib",
        "block",
        "arch",
        "crypto",
        "security",
        "sound",
        "net",
        "fs",
        "drivers",
        "postgre",
        "kernel",
    ],
    "java_points_to": [
        "sunflow",
        "lusearch",
        "luindex",
        "avrora",
        "eclipse",
        "h2",
        "pmd",
        "xalan",
        "batik",
        "fop",
        "tomcat",
        "jython",
        "tradebeans",
        "tradesoap",
    ],
}

#: Graph name -> section (inverse of :data:`SECTIONS`).
NAME_SECTIONS: Dict[str, str] = {
    name: section for section, names in SECTIONS.items() for name in names
}


def download_graph(name: str, dest_path: Union[pathlib.Path, str]) -> pathlib.Path:
    """Download the old-format archive of a graph from the public bucket.

    Parameters
    ----------
    name : str
        The graph name (the archive is ``4.0.0/graph/<name>.tar.gz``; the old
        archives stay under the legacy prefix).
    dest_path : Union[Path, str]
        Where the archive is written (parent directories created if needed).

    Returns
    -------
    Path
        The path of the downloaded archive.

    Raises
    ------
    ConversionError
        If the bucket has no such archive or the download fails.
    """
    url = LEGACY_DATASET_URL + f"{name}.tar.gz"
    dest_path = pathlib.Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, timeout=600) as response:
        if response.status_code == 404:
            raise ConversionError(f"No archive for graph {name!r} at {url}")
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(response.raw, f)

    logging.info(f"Downloaded {url} to {dest_path=}")
    return dest_path


def verify_public_read(key: str) -> None:
    """Check that a bucket object is anonymously readable.

    Streams the whole object from the public URL and discards it; this
    confirms the bucket policy covers the key (the new ``5.0.0/graph/``
    prefix inherits the public-read policy of ``4.0.0/graph/``).

    Parameters
    ----------
    key : str
        The object key in the bucket (e.g. ``5.0.0/graph/generations.tar.gz``).

    Raises
    ------
    ConversionError
        If the object cannot be read anonymously or the body is empty.
    """
    url = STORAGE_BASE_URL + key
    with requests.get(url, stream=True, timeout=600) as response:
        if response.status_code != 200:
            raise ConversionError(
                f"Object {url} is not publicly readable "
                f"(HTTP {response.status_code})"
            )
        total = 0
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            total += len(chunk)
    if total == 0:
        raise ConversionError(f"Object {url} is empty")

    logging.info(f"Verified public read of {url} ({total} bytes)")


def load_record(path: Union[pathlib.Path, str]) -> Dict[str, dict]:
    """Load the conversion record (``{}`` if the file does not exist)."""
    path = pathlib.Path(path)
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_record(path: Union[pathlib.Path, str], record: Dict[str, dict]) -> None:
    """Persist the conversion record after every graph (resumable runs)."""
    path = pathlib.Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, sort_keys=True)
        f.write("\n")


def convert_one(
    name: str,
    section: str,
    *,
    client: Optional[BaseClient],
    bucket: str,
    key_prefix: str,
    record: Dict[str, dict],
    record_path: Union[pathlib.Path, str],
    workdir: Union[pathlib.Path, str],
    dry_run: bool = False,
    force: bool = False,
) -> dict:
    """Convert one graph from the old format to the new one.

    Pipeline (at most one graph on disk at any time): skip if already
    recorded and publicly readable (unless ``force``); download the old
    archive; validate its old-format layout; build the new archive tree;
    verify the conversion by round-trip; pack the tarball; then, unless
    ``dry_run``, upload it under ``<key_prefix>/<name>.tar.gz`` (verified
    upload), check anonymous public read, and record
    ``{old_sha256, new_sha256, key, date}``. Local files are removed on
    success and kept for inspection on error.

    Parameters
    ----------
    name : str
        The graph name.
    section : str
        One of the :data:`SECTIONS` keys — selects the grammar files.
    client : BaseClient or None
        S3 client for the upload (ignored in ``dry_run``).
    bucket : str
        Target bucket name.
    key_prefix : str
        The object key prefix (default ``5.0.0/graph``).
    record : dict of str -> dict
        The conversion record (shared across graphs of one run).
    record_path : Union[Path, str]
        Where the record is persisted after each graph.
    workdir : Union[Path, str]
        The directory for temporary files.
    dry_run : bool, optional
        Stop after verification: no upload, no record update.
    force : bool, optional
        Re-convert even if the graph is already recorded.

    Returns
    -------
    dict
        ``{"name", "status"}`` plus, for converted graphs, ``num_nodes``,
        ``num_edges``, ``num_labels`` and the new tarball ``sha256``.

    Raises
    ------
    ConversionError
        If any step fails; local files are kept for inspection.
    """
    workdir = pathlib.Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    key = f"{key_prefix}/{name}.tar.gz"

    if not force and name in record:
        verify_public_read(record[name]["key"])
        logging.info(f"{name}: already recorded and publicly readable, skipping")
        return {"name": name, "status": "skipped"}

    archive_path = download_graph(name, workdir / f"{name}_old.tar.gz")
    extract_dir = workdir / f"{name}_extracted"
    tree_dir = workdir / name
    tarball_path = workdir / f"{name}.tar.gz"
    succeeded = False

    try:
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        shutil.unpack_archive(archive_path, extract_dir)
        csv_path = extract_dir / name / f"{name}.csv"
        if not csv_path.is_file() or not (extract_dir / name / "README.md").is_file():
            raise ConversionError(
                f"Archive of {name!r} is not in the old format "
                f"(expected {name}/{name}.csv and {name}/README.md)"
            )

        _, stats = build_archive(name, section, csv_path, workdir)
        verify_conversion(csv_path, tree_dir)
        make_tarball(tree_dir, tarball_path)

        result = {
            "name": name,
            "num_nodes": stats.num_nodes,
            "num_edges": stats.total_edges,
            "num_labels": len(stats.edges_per_label),
            "sha256": sha256_of(tarball_path),
        }

        if dry_run:
            result["status"] = "dry_run"
            logging.info(f"{name}: dry run, skipping upload")
            succeeded = True
            return result

        if client is None:
            raise ConversionError("No S3 client provided for the upload")
        upload_file(client, tarball_path, bucket, key=key)
        verify_public_read(key)

        record[name] = {
            "old_sha256": sha256_of(archive_path),
            "new_sha256": result["sha256"],
            "key": key,
            "date": datetime.date.today().isoformat(),
        }
        save_record(record_path, record)
        result["status"] = "uploaded"
        succeeded = True
        return result
    except Exception:
        logging.error(
            f"{name}: conversion failed; keeping local files under {workdir} "
            f"for inspection"
        )
        raise
    finally:
        if succeeded:
            for path in (archive_path, extract_dir, tree_dir, tarball_path):
                if path.is_dir():
                    shutil.rmtree(path)
                elif path.exists():
                    path.unlink()
            logging.info(f"{name}: removed local files")


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Command-line entry point.

    Usage::

        python utils/convert_old_to_new.py [NAME|SECTION]... \\
            [--access-key-id KEY_ID --secret-access-key SECRET] \\
            [--endpoint-url URL] [--bucket BUCKET] [--key-prefix PREFIX] \\
            [--record FILE] [--workdir DIR] [--dry-run] [--force] \\
            [--report FILE]

    Each ``NAME|SECTION`` argument is a graph name or a section key
    (``rdf``, ``c_alias``, ``java_points_to``) expanding to all its graphs.
    Credentials are always taken from the command line and are never read
    from environment variables or config files; they are required unless
    ``--dry-run`` is set.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Convert old-format graph archives to the nab-like "
            "mtx-per-label format, one graph at a time."
        )
    )
    parser.add_argument(
        "names_or_sections",
        nargs="+",
        help="graph names or section keys (rdf, c_alias, java_points_to)",
    )
    parser.add_argument("--access-key-id", default=None, help="Yandex Cloud IAM key ID")
    parser.add_argument(
        "--secret-access-key", default=None, help="Yandex Cloud IAM secret key"
    )
    parser.add_argument(
        "--endpoint-url",
        default=DEFAULT_ENDPOINT_URL,
        help=f"S3 API endpoint (default: {DEFAULT_ENDPOINT_URL})",
    )
    parser.add_argument(
        "--bucket",
        default=DEFAULT_BUCKET,
        help=f"target bucket (default: {DEFAULT_BUCKET})",
    )
    parser.add_argument(
        "--key-prefix",
        default=DEFAULT_KEY_PREFIX,
        help=f"object key prefix (default: {DEFAULT_KEY_PREFIX})",
    )
    parser.add_argument(
        "--record",
        default=str(DEFAULT_RECORD_PATH),
        help=f"conversion record file (default: {DEFAULT_RECORD_PATH})",
    )
    parser.add_argument(
        "--workdir",
        default=None,
        help="directory for temporary files (default: a new temp dir)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="convert and verify locally without uploading or recording",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="re-convert graphs that are already in the record",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="write the per-graph results to this JSON file",
    )
    args = parser.parse_args(argv)

    names: List[str] = []
    for token in args.names_or_sections:
        if token in SECTIONS:
            names.extend(SECTIONS[token])
        elif token in NAME_SECTIONS:
            names.append(token)
        else:
            parser.error(
                f"unknown graph or section {token!r}; use one of the sections "
                f"{sorted(SECTIONS)} or a graph name from them"
            )

    if not args.dry_run and (
        args.access_key_id is None or args.secret_access_key is None
    ):
        parser.error(
            "--access-key-id and --secret-access-key are required "
            "unless --dry-run is set"
        )

    workdir = (
        pathlib.Path(args.workdir)
        if args.workdir
        else pathlib.Path(tempfile.mkdtemp(prefix="cfpq_convert_"))
    )
    record = load_record(args.record)
    client = None
    if not args.dry_run:
        client = create_s3_client(
            args.access_key_id, args.secret_access_key, args.endpoint_url
        )

    summary = {"uploaded": 0, "dry_run": 0, "skipped": 0}
    results: List[dict] = []
    for name in names:
        result = convert_one(
            name,
            NAME_SECTIONS[name],
            client=client,
            bucket=args.bucket,
            key_prefix=args.key_prefix,
            record=record,
            record_path=args.record,
            workdir=workdir,
            dry_run=args.dry_run,
            force=args.force,
        )
        results.append(result)
        summary[result["status"]] += 1
        print(
            f"{name}: {result['status']}"
            + (
                f" ({result['num_nodes']} nodes, {result['num_edges']} edges,"
                f" {result['num_labels']} labels)"
                if result["status"] in ("uploaded", "dry_run")
                else ""
            )
        )

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, sort_keys=True)
            f.write("\n")

    print(
        f"Done: {summary['uploaded']} uploaded, {summary['dry_run']} dry run, "
        f"{summary['skipped']} skipped."
    )


if __name__ == "__main__":
    main()
