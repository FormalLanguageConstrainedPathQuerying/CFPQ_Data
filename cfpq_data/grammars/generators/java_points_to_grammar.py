"""Returns a Java Points-to grammar that generates a language for the field-sensitive analysis of Java programs."""
import logging
from typing import List
from pyformlang.cfg import CFG, Production, Variable, Terminal

import networkx as nx
import re

__all__ = ["java_points_to_grammar", "java_points_to_grammar_from_graph"]


def java_points_to_grammar(
    fields: List[str],
    *,
    start_symbol: Variable = Variable("S"),
) -> CFG:
    """Returns a Java Points-to grammar that generates a language for the field-sensitive analysis of Java programs [1]_
    with given fields labels.

    Parameters
    ----------
    fields : List[str]
        List of labels that represent the fields used in Java program.

    start_symbol : Variable
        Start symbol of the grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cfg = java_points_to_grammar(["0", "1"])
    >>> len(cfg.productions)
    11

    Returns
    -------
    cfg : CFG
        Java Points-to context-free grammar.

    References
    ----------
    .. [1] https://dl.acm.org/doi/10.1145/2858965.2814307
    """
    PTh = Variable("PTh")
    Al = Variable("Al")
    FT = Variable("FT")
    FTh = Variable("FTh")

    alloc = Terminal("alloc")
    alloc_r = Terminal("alloc_r")
    assign = Terminal("assign")
    assign_r = Terminal("assign_r")

    variables = {start_symbol, PTh, Al, FT, FTh}
    productions = set()
    terminals = {alloc, alloc_r, assign, assign_r}

    for f in fields:
        terminals.update(
            [
                Terminal("load_" + f),
                Terminal("load_" + f + "_r"),
                Terminal("store_" + f),
                Terminal("store_" + f + "_r"),
            ]
        )

    productions.update(
        [
            Production(start_symbol, [PTh, alloc]),
            Production(PTh, []),
            Production(PTh, [assign, PTh]),
        ]
    )

    for f in fields:
        productions.add(
            Production(PTh, [Terminal("load_" + f), Al, Terminal("store_" + f), PTh])
        )
        terminals.update([Terminal("load_" + f), Terminal("store_" + f)])

    productions.update(
        [
            Production(FT, [alloc_r, FTh]),
            Production(FTh, []),
            Production(FTh, [assign_r, FTh]),
        ]
    )

    for f in fields:
        productions.add(
            Production(
                FTh,
                [Terminal("store_" + f + "_r"), Al, Terminal("load_" + f + "_r"), FTh],
            )
        )
        terminals.update([Terminal("store_" + f + "_r"), Terminal("load_" + f + "_r")])

    productions.add(Production(Al, [start_symbol, FT]))

    cfg = CFG(
        variables=variables,
        terminals=terminals,
        productions=productions,
        start_symbol=start_symbol,
    )

    logging.info(f"Create a Java Points-to {cfg=} with {fields=}")

    return cfg


def java_points_to_grammar_from_graph(
    graph: nx.MultiDiGraph,
    *,
    start_symbol: Variable = Variable("S"),
) -> CFG:
    """Returns a Java Points-to grammar that generates a language for the field-sensitive analysis of Java programs [1]_
    with fields corresponding to the load and store edge labels of the given graph.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        The graph to be analyzed using the grammar.

    start_symbol : Variable
        Start symbol of the grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> path = download("avrora")
    >>> g = cfpq_data.graph_from_csv(path)
    >>> cfg = java_points_to_grammar_from_graph(g)
    >>> len(cfg.productions)
    1723

    Returns
    -------
    cfg : CFG
        Java Points-to context-free grammar.

    References
    ----------
    .. [1] https://dl.acm.org/doi/10.1145/2858965.2814307
    """
    fields = []
    load_pattern = "(^load_[^r].*)|(^load_r.+)"
    store_pattern = "(^store_[^r].*)|(^store_r.+)"

    for u, v, edge_labels in graph.edges(data=True):
        for key, value in edge_labels.items():
            field = ""

            if re.match(load_pattern, value):
                field = re.sub("load_", "", value, count=1)
            elif re.match(store_pattern, value):
                field = re.sub("store_", "", value, count=1)

            if field and field not in fields:
                fields.append(field)

    cfg = java_points_to_grammar(fields, start_symbol=start_symbol)

    logging.info(f"Create a Java Points-to {cfg=} for {graph=}")

    return cfg
