"""Create a Recursive State Machine
from different formats.
"""
from pyformlang.cfg import CFG

from cfpq_data.grammars.readwrite.rsm import rsm_from_text
from cfpq_data.grammars.rsm import RSM

__all__ = [
    "rsm_from_cfg",
    "rsm_from_cnf",
]


def rsm_from_cfg(cfg: CFG) -> RSM:
    """Create a Recursive State Machine [2]_
    from context-free grammar [1]_.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_text("S -> a S b S | epsilon")
    >>> rsm = cfpq_data.rsm_from_cfg(cfg)
    >>> [rsm.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    rsm : RSM
        Recursive State Machine.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    .. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    return rsm_from_text(cfg.to_text(), cfg.start_symbol)


def rsm_from_cnf(cnf: CFG) -> RSM:
    """Create a Recursive State Machine [2]_
    from context-free grammar
    in Chomsky normal form [1]_.

    Parameters
    ----------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_text("S -> a S b S | epsilon")
    >>> rsm = cfpq_data.rsm_from_cnf(cnf)
    >>> [rsm.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    rsm : RSM
        Recursive State Machine.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    return rsm_from_text(cnf.to_text(), cnf.start_symbol)