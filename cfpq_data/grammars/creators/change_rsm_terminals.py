"""Change terminals of a Recursive State Machine [1]_.

References
----------
.. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
   and Semyon Grigorev "Context-Free Path Querying
   by Kronecker Product", ADBIS 2020, pp 49-59, 2020
"""
import re
from typing import Dict

from cfpq_data.grammars.creators.rsm_from_txt import rsm_from_txt
from cfpq_data.grammars.rsm import RSM

__all__ = ["change_rsm_terminals"]


def change_rsm_terminals(rsm: RSM, spec: Dict[str, str]) -> RSM:
    """Change terminals of a Recursive State Machine [1]_.

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    spec: Dict
        Terminals mapping.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_txt("S -> a S b S | epsilon")
    >>> new_rsm = cfpq_data.change_rsm_terminals(rsm, {"a": "b", "b": "c"})

    Returns
    -------
    rsm : RSM
        Recursive State Machine with changed terminals.

    References
    ----------
    .. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    regex = re.compile("|".join(map(re.escape, spec.keys())))
    text = regex.sub(lambda match: spec[match.group(0)], rsm.to_text())
    return rsm_from_txt(text)
