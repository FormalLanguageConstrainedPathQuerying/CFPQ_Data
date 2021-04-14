"""Create a Recursive State Machine [2]_
from context free grammar
in Chomsky normal form [1]_.

References
----------
.. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
.. [2] Egor Orachev, Ilya Epelbaum, Rustam Azimov
   and Semyon Grigorev "Context-Free Path Querying
   by Kronecker Product", ADBIS 2020, pp 49-59, 2020
"""
from pyformlang.cfg import CFG

from cfpq_data.grammars.creators.rsm_from_txt import rsm_from_txt
from cfpq_data.grammars.rsm import RSM

__all__ = ["rsm_from_cnf"]


def rsm_from_cnf(cnf: CFG) -> RSM:
    """Create a Recursive State Machine [2]_
    from context free grammar
    in Chomsky normal form [1]_.

    Parameters
    ----------
    cnf : CFG
        Context free grammar in Chomsky normal form.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_txt("S -> a S b S | epsilon")
    >>> rsm = cfpq_data.rsm_from_cfg(cnf)

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
    return rsm_from_txt(cnf.to_text(), cnf.start_symbol)
