"""Read (and write) grammar templates in the ``.cnf`` format of the new-format
graph archives, and materialize them over a concrete graph."""
import logging
import pathlib
from typing import List, Optional, Set, Tuple, Union

import networkx as nx
from pyformlang.cfg import CFG, Production, Terminal, Variable

__all__ = [
    "cnf_template_from_text",
    "cnf_template_to_text",
    "cnf_template_from_cnf",
    "cnf_template_to_cnf",
    "materialize",
    "materialize_grammar",
]


def _parse_template(text: str) -> Tuple[List[Tuple[str, Tuple[str, ...]]], str]:
    """Parse the ``.cnf`` template text into productions and a start symbol.

    One production per non-empty line (symbols separated by whitespace, the
    left-hand side first); the last two lines are ``Count:`` and the start
    symbol.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    count_index = lines.index("Count:")
    productions = [
        (parts[0], tuple(parts[1:]))
        for parts in (line.split() for line in lines[:count_index])
    ]
    start_symbol = lines[count_index + 1]

    return productions, start_symbol


def cnf_template_from_text(text: str) -> CFG:
    """Create a grammar template from ``.cnf`` format text.

    The template is a context-free grammar whose left-hand-side symbols are
    the non-terminals and all other symbols (including the indexed placeholder
    symbols such as ``load_i`` or ``load_r``) are terminals; the start symbol
    is given by the ``Count:`` trailer.

    Parameters
    ----------
    text : str
        The text with which the grammar template will be created.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cfg = cnf_template_from_text("S\\ta\\tN1\\nN1\\tS\\tb\\n\\nCount:\\nS")
    >>> cfg.start_symbol.value
    'S'
    >>> len(cfg.productions)
    2

    Returns
    -------
    cfg : CFG
        Grammar template.
    """
    productions, start_symbol = _parse_template(text)

    cfg = _cfg_from_productions(productions, start_symbol)

    logging.info(f"Create {cfg=} from {text=}")

    return cfg


def cnf_template_to_text(cfg: CFG) -> str:
    """Turns a grammar template into its ``.cnf`` format text representation.

    One production per line, symbols separated by tabs (an epsilon production
    is a bare non-terminal), sorted by the left-hand side and then the
    right-hand side; the last two lines are ``Count:`` and the start symbol.

    Parameters
    ----------
    cfg : CFG
        Grammar template to convert.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cfg = cnf_template_from_text("S\\ta\\tN1\\nN1\\tS\\tb\\n\\nCount:\\nS")
    >>> cnf_template_to_text(cfg)
    'N1\\tS\\tb\\nS\\ta\\tN1\\n\\nCount:\\nS'

    Returns
    -------
    text : str
        Grammar template text representation.
    """
    productions = sorted(
        (
            production.head.value,
            tuple(symbol.value for symbol in production.body),
        )
        for production in cfg.productions
    )

    lines = ["\t".join([lhs, *rhs]) for lhs, rhs in productions]
    lines += ["", "Count:", cfg.start_symbol.value]
    text = "\n".join(lines)

    logging.info(f"Turn {cfg=} into {text=}")

    return text


def cnf_template_from_cnf(path: Union[pathlib.Path, str]) -> CFG:
    """Create a grammar template from a ``.cnf`` file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the ``.cnf`` file with which the grammar template will be
        created.

    Examples
    --------
    >>> from cfpq_data import *
    >>> import pathlib, tempfile
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "g.cnf"
    >>> _ = p.write_text("S\\ta\\tN1\\nN1\\tS\\tb\\n\\nCount:\\nS")
    >>> cfg = cnf_template_from_cnf(p)
    >>> len(cfg.productions)
    2

    Returns
    -------
    cfg : CFG
        Grammar template.
    """
    with open(path, "r") as f:
        text = f.read()

    cfg = cnf_template_from_text(text)

    logging.info(f"Create {cfg=} from {path=}")

    return cfg


def cnf_template_to_cnf(cfg: CFG, path: Union[pathlib.Path, str]) -> pathlib.Path:
    """Saves a grammar template to a ``.cnf`` file by `path`.

    Parameters
    ----------
    cfg : CFG
        Grammar template to save.

    path : Union[Path, str]
        The path to the ``.cnf`` file where the grammar template will be saved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> import pathlib, tempfile
    >>> cfg = cnf_template_from_text("S\\ta\\tN1\\nN1\\tS\\tb\\n\\nCount:\\nS")
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "g.cnf"
    >>> path = cnf_template_to_cnf(cfg, p)
    >>> cnf_template_from_cnf(path).start_symbol.value
    'S'

    Returns
    -------
    path : Path
        The path to the ``.cnf`` file where the grammar template will be saved.
    """
    pathlib.Path(path).write_text(cnf_template_to_text(cfg) + "\n")

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {cfg=} to {dest=}")

    return dest


def _index_set(base: str, available: Set[str], *, reversed_: bool) -> Set[int]:
    """The indices k for which the label of base and k is in `available`.

    The label is ``<base>_<k>`` or, when `reversed_`, ``<base>_<k>_r``.
    """
    prefix = f"{base}_"
    suffix = "_r" if reversed_ else ""
    indices: Set[int] = set()
    for label in available:
        if not (label.startswith(prefix) and label.endswith(suffix)):
            continue
        middle = label[len(prefix) : len(label) - len(suffix)]
        if middle.isdigit():
            indices.add(int(middle))
    return indices


def materialize(cfg: CFG, graph: nx.MultiDiGraph) -> CFG:
    """Materialize a grammar template over the edge labels of a graph.

    Returns a context-free grammar whose terminals are the concrete edge
    labels: an indexed symbol is expanded per index present in the graph (the
    ``_i`` placeholder style, e.g. ``load_i`` -> ``load_5``, and the bare
    style, e.g. ``load`` -> ``load_5`` and ``load_r`` -> ``load_5_r``), and a
    symbol with no matching label is kept as an inert terminal. Reversed
    labels (the ``_r`` suffix) resolve to the stored labels or to the labels
    derived by reversing the respective forward edges (see
    :func:`cfpq_data.graphs.utils.add_reverse_edges`); the returned grammar
    does not add the reversed edges to the graph itself.

    Parameters
    ----------
    cfg : CFG
        Grammar template (e.g. from :func:`cnf_template_from_cnf`).

    graph : MultiDiGraph
        The graph whose edge labels (the ``label`` edge attribute) the
        template is materialized over.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = nx.MultiDiGraph()
    >>> _ = g.add_edges_from(
    ...     [(0, 1, {"label": "load_0"}), (1, 2, {"label": "store_0"}),
    ...      (0, 2, {"label": "alloc"}), (2, 3, {"label": "assign"})]
    ... )
    >>> template = cnf_template_from_text(
    ...     "PT\\tPTh\\talloc\\nPTh\\tassign\\nPTh\\tload\\tAl_st_PTh\\n"
    ...     "Al_st_PTh\\tAl\\tst_PTh\\nst_PTh\\tstore\\tPTh\\nAl\\tPT\\n\\nCount:\\nPT"
    ... )
    >>> cfg = materialize(template, g)
    >>> sorted(symbol.value for symbol in cfg.terminals)
    ['alloc', 'assign', 'load_0', 'store_0']

    Returns
    -------
    cfg : CFG
        Materialized context-free grammar.
    """
    stored = {data["label"] for _, _, data in graph.edges(data=True)}
    available = stored | {f"{label}_r" for label in stored}

    productions, start_symbol = _template_productions(cfg)

    if start_symbol in _indexed_symbols(productions, available):
        raise ValueError(f"The start symbol {start_symbol=} must not be indexed")

    terminal_index_sets = _terminal_index_sets(productions, available)
    indexed = _indexed_symbols(productions, available, terminal_index_sets)
    index_sets = _nonterminal_index_sets(productions, terminal_index_sets, indexed)

    materialized: List[Tuple[str, Tuple[str, ...]]] = []
    for lhs, rhs in productions:
        production_indices = [symbol for symbol in (lhs, *rhs) if symbol in indexed]
        if not production_indices:
            materialized.append((lhs, rhs))
            continue

        indices = sorted(
            set().union(*(index_sets[symbol] for symbol in production_indices))
        )
        for k in indices:
            materialized.append(
                (
                    _instantiate(lhs, k, index_sets),
                    tuple(_instantiate(symbol, k, index_sets) for symbol in rhs),
                )
            )

    result = _cfg_from_productions(materialized, start_symbol)

    logging.info(f"Materialize {cfg=} over {graph=} to {result=}")

    return result


def materialize_grammar(
    cnf_path: Union[pathlib.Path, str], graph: nx.MultiDiGraph
) -> CFG:
    """Load a ``.cnf`` grammar template and materialize it over a graph.

    A convenience wrapper over :func:`cnf_template_from_cnf` +
    :func:`materialize`: expands indexed symbols (e.g. ``load_i`` ->
    ``load_0``, ``load_1``, ...) into explicit productions for each index
    present in the graph edge labels. Non-indexed grammars pass through
    unchanged.

    Parameters
    ----------
    cnf_path : Union[Path, str]
        Path to the ``.cnf`` grammar template file.
    graph : MultiDiGraph
        The graph whose edge labels determine which indices are instantiated.

    Examples
    --------
    >>> from cfpq_data import *
    >>> g = nx.MultiDiGraph()
    >>> _ = g.add_edges_from(
    ...     [(0, 1, {"label": "load_0"}), (1, 2, {"label": "store_0"}),
    ...      (0, 3, {"label": "load_1"}), (3, 2, {"label": "store_1"}),
    ...      (0, 4, {"label": "alloc"})]
    ... )
    >>> import pathlib, tempfile
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "g.cnf"
    >>> _ = p.write_text(
    ...     "PT\\tPTh\\talloc\\nPTh\\tassign\\n"
    ...     "PTh\\tload_i\\tAl_st_PTh_i\\nAl_st_PTh_i\\tAl\\tst_PTh_i\\n"
    ...     "st_PTh_i\\tstore_i\\tPTh\\nAl\\tPT\\n\\nCount:\\nPT"
    ... )
    >>> cfg = materialize_grammar(p, g)
    >>> sorted(s.value for s in cfg.terminals)
    ['alloc', 'assign', 'load_0', 'load_1', 'store_0', 'store_1']

    Returns
    -------
    cfg : CFG
        The explicitly-instantiated context-free grammar.
    """
    template = cnf_template_from_cnf(cnf_path)
    return materialize(template, graph)


def _cfg_from_productions(
    productions: List[Tuple[str, Tuple[str, ...]]], start_symbol: str
) -> CFG:
    """Build a CFG from (lhs, rhs) string productions: the left-hand-side
    symbols are the variables, all other symbols are terminals."""
    lhs_symbols = {lhs for lhs, _ in productions}
    all_symbols = {symbol for lhs, rhs in productions for symbol in (lhs, *rhs)}

    return CFG(
        variables={Variable(symbol) for symbol in lhs_symbols},
        terminals={Terminal(symbol) for symbol in all_symbols - lhs_symbols},
        productions={
            Production(
                Variable(lhs),
                [
                    Variable(symbol) if symbol in lhs_symbols else Terminal(symbol)
                    for symbol in rhs
                ],
            )
            for lhs, rhs in productions
        },
        start_symbol=Variable(start_symbol),
    )


def _template_productions(cfg: CFG) -> Tuple[List[Tuple[str, Tuple[str, ...]]], str]:
    """The productions of a template as (lhs, rhs) string pairs + start symbol."""
    return (
        [
            (production.head.value, tuple(symbol.value for symbol in production.body))
            for production in cfg.productions
        ],
        cfg.start_symbol.value,
    )


def _terminal_index_sets(
    productions: List[Tuple[str, Tuple[str, ...]]], available: Set[str]
) -> dict:
    """The index set of every indexed terminal symbol ({} for inert ones)."""
    terminals = {
        symbol
        for lhs, rhs in productions
        for symbol in (lhs, *rhs)
        if symbol not in {left for left, _ in productions}
    }

    index_sets: dict = {}
    for symbol in terminals:
        if symbol.endswith("_r_i"):
            base = symbol[:-4]
            indices = _index_set(base, available, reversed_=True)
            indices |= _index_set(base + "_r", available, reversed_=False)
            index_sets[symbol] = indices
        elif symbol.endswith("_i"):
            index_sets[symbol] = _index_set(symbol[:-2], available, reversed_=False)
        elif symbol.endswith("_r") and symbol not in available:
            index_sets[symbol] = _index_set(symbol[:-2], available, reversed_=True)
        elif not symbol.endswith("_r") and symbol not in available:
            index_sets[symbol] = _index_set(symbol, available, reversed_=False)

    return index_sets


def _indexed_symbols(
    productions: List[Tuple[str, Tuple[str, ...]]],
    available: Set[str],
    terminal_index_sets: Optional[dict] = None,
) -> Set[str]:
    """The indexed symbols of a template (terminals and non-terminals).

    A terminal is indexed when its index set is non-empty. A non-terminal is
    indexed when it ends in ``_i`` or when every production with it on the
    left-hand side contains an indexed symbol (fixpoint).
    """
    lhs_symbols = {lhs for lhs, _ in productions}

    if terminal_index_sets is None:
        terminal_index_sets = _terminal_index_sets(productions, available)

    indexed = {symbol for symbol, indices in terminal_index_sets.items() if indices}
    indexed |= {symbol for symbol in lhs_symbols if symbol.endswith("_i")}

    changed = True
    while changed:
        changed = False
        for symbol in sorted(lhs_symbols - indexed):
            own_rhs = [rhs for lhs, rhs in productions if lhs == symbol]
            if own_rhs and all(any(part in indexed for part in rhs) for rhs in own_rhs):
                indexed.add(symbol)
                changed = True

    return indexed


def _nonterminal_index_sets(
    productions: List[Tuple[str, Tuple[str, ...]]],
    terminal_index_sets: dict,
    indexed: Set[str],
) -> dict:
    """The index set of every indexed non-terminal (fixpoint over co-occurrence)."""
    index_sets = dict(terminal_index_sets)

    changed = True
    while changed:
        changed = False
        for symbol in indexed:
            own = index_sets.get(symbol, set())
            for lhs, rhs in productions:
                if symbol not in (lhs, *rhs):
                    continue
                co_occurring = {
                    part
                    for part in (lhs, *rhs)
                    if part != symbol and part in index_sets
                }
                union = own | set().union(*(index_sets[part] for part in co_occurring))
                if union - own:
                    index_sets[symbol] = union
                    changed = True

    return index_sets


def _instantiate(symbol: str, k: int, index_sets: dict) -> str:
    """The concrete symbol of an indexed symbol at index k (else unchanged)."""
    if symbol not in index_sets:
        return symbol
    if symbol.endswith("_r_i"):
        return f"{symbol[:-4]}_{k}_r"
    if symbol.endswith("_i"):
        return f"{symbol[:-2]}_{k}"
    if symbol.endswith("_r"):
        return f"{symbol[:-2]}_{k}_r"
    return f"{symbol}_{k}"
