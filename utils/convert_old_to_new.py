"""Convert old-format graph archives to the nab-like mtx-per-label format.

The old format stores a whole graph in one CSV file (``<name>/<name>.csv``,
space-separated ``from to label`` lines with CRLF endings). The new format
stores one Boolean MatrixMarket matrix per edge label
(``<name>/graph/<label>.mtx``) plus CNF grammar files
(``<name>/grammar/*.cnf``) and a README.

The tool processes graphs one by one: it downloads a single archive from the
public bucket, converts it locally, verifies the conversion by round-trip,
uploads the new archive under the ``5.0.0/graph/`` key prefix, and removes
the local files. At most one graph is on disk at any time.
"""

import logging
import pathlib
import re
from dataclasses import dataclass, field
from typing import Dict, IO, Iterator, List, Set, Tuple, Union

from cfpq_data.grammars.generators.c_alias_grammar import c_alias_grammar
from cfpq_data.grammars.generators.nested_parentheses_grammar import (
    nested_parentheses_grammar,
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
