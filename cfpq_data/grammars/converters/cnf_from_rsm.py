"""Create a context free grammar
in Chomsky normal form [1]_
from Recursive State Machine [2]_.

References
----------
.. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
.. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
   and Semyon Grigorev "Context-Free Path Querying
   by Kronecker Product", ADBIS 2020, pp 49-59, 2020
"""
from pyformlang.cfg import CFG

from cfpq_data.grammars.converters.cfg_from_rsm import cfg_from_rsm
from cfpq_data.grammars.converters.cnf_from_cfg import cnf_from_cfg
from cfpq_data.grammars.rsm import RSM

__all__ = ["cnf_from_rsm"]


def cnf_from_rsm(rsm: RSM) -> CFG:
    """Create a context free grammar
    in Chomsky normal form [1]_
    from Recursive State Machine [2]_.

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_txt("S -> a S* b S* | epsilon")
    >>> cnf = cfpq_data.cnf_from_rsm(rsm)
    >>> [cnf.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context free grammar in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    return cnf_from_cfg(cfg_from_rsm(rsm))
