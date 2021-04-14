"""Create a Recursive State Machine [2]_
from context free grammar [1]_.

References
----------
.. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
.. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
   and Semyon Grigorev "Context-Free Path Querying
   by Kronecker Product", ADBIS 2020, pp 49-59, 2020
"""
from pyformlang.cfg import CFG

from cfpq_data.grammars.creators.rsm_from_txt import rsm_from_txt
from cfpq_data.grammars.rsm import RSM

__all__ = ["rsm_from_cfg"]


def rsm_from_cfg(cfg: CFG) -> RSM:
    """Create a Recursive State Machine [2]_
    from context free grammar [1]_.

    Parameters
    ----------
    cfg : CFG
        Context free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_txt("S -> a S b S | epsilon")
    >>> rsm = cfpq_data.rsm_from_cfg(cfg)

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
    return rsm_from_txt(cfg.to_text(), cfg.start_symbol)
