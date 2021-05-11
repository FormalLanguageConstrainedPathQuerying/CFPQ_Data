"""Create a context-free grammar
from different formats.
"""
from pyformlang.cfg import CFG

from cfpq_data.grammars.rsm import RSM

__all__ = [
    "cfg_from_cnf",
    "cfg_from_rsm",
]


def cfg_from_cnf(cnf: CFG) -> CFG:
    """Create a context-free grammar [2]_
    from given context-free grammar
    in Chomsky normal form [1]_.

    Parameters
    ----------
    cnf : CFG
        Context free grammar
        in Chomsky normal form.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_text("S -> a S b S | epsilon")
    >>> cfg = cfpq_data.cfg_from_cnf(cnf)
    >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    return CFG.from_text(cnf.to_text(), cnf.start_symbol)


def cfg_from_rsm(rsm: RSM) -> CFG:
    """Create a context-free grammar [1]_
    from given Recursive State Machine [2]_.

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
    >>> cfg = cfpq_data.cfg_from_rsm(rsm)
    >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    .. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    return rsm.to_cfg()
