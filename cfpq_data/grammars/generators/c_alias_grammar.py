"""Returns a C Alias grammar that generates a language for the flow-insensitive alias analysis of C programs."""
import logging
from typing import Tuple
from pyformlang.cfg import CFG, Variable

import cfpq_data

__all__ = ["c_alias_grammar"]


def c_alias_grammar(
    *,
    assigment_labels: Tuple[str, str] = ("a", "a_r"),
    dereference_labels: Tuple[str, str] = ("d", "d_r"),
    start_symbol: Variable = Variable("S"),
) -> CFG:
    """Returns a C Alias grammar that generates a language for the flow-insensitive alias analysis of C programs [1]_.

    Parameters
    ----------
    assigment_labels : Tuple[str, str]
        Pair $(a, a_r)$ where label $a$ represents the assignment operation and $a_r$ is reverse to it.

    dereference_labels : Tuple[str, str]
        Pair $(d, d_r)$ where label $d$ represents pointer dereference relation and $d_r$ is reverse to it.

    start_symbol : Variable
        Start symbol of the grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cfg = c_alias_grammar()
    >>> cfg_to_text(cfg)
    'S -> d_r V d\\nV -> V1 V2 V3\\nV1 -> \\nV1 -> V2 a_r V1\\nV2 -> \\nV2 -> S\\nV3 -> \\nV3 -> a V2 V3'

    Returns
    -------
    cfg : CFG
        C Alias context-free grammar.

    References
    ----------
    .. [1] https://dl.acm.org/doi/10.1145/1328897.1328464
    """
    a, a_r = assigment_labels
    d, d_r = dereference_labels

    grammar_text = f"""{start_symbol.to_text()} -> {d_r} V {d}
    V -> V1 V2 V3
    V1 -> epsilon
    V1 -> V2 {a_r} V1
    V2 -> epsilon
    V2 -> S
    V3 -> epsilon
    V3 -> {a} V2 V3"""

    cfg = cfpq_data.cfg_from_text(grammar_text)

    logging.info(
        f"Create a C Alias {cfg=} with {assigment_labels=}, {dereference_labels=}"
    )

    return cfg
