"""Create a Recursive State Machine [1]_
from txt file.

References
----------
.. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
   and Semyon Grigorev "Context-Free Path Querying
   by Kronecker Product", ADBIS 2020, pp 49-59, 2020
"""
import os
from pathlib import Path
from typing import Union

from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from cfpq_data.grammars.rsm import RSM

__all__ = ["rsm_from_txt"]


def rsm_from_txt(
    source: Union[Path, str], start_symbol: Variable = Variable("S")
) -> RSM:
    """Create a Recursive State Machine [1]_
    from txt file.

    Parameters
    ----------
    source : Union[Path, str]
        If source is a str, then the graph will be created from a text.
        If source is a Path, then the graph will be created from a txt file.

    start_symbol : Variable
        Start symbol of a context free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_txt("S -> a S b S | epsilon")

    Returns
    -------
    rsm : RSM
        Recursive State Machine.

    References
    ----------
    .. [1] Egor Orachev, Ilya Epelbaum, Rustam Azimov
       and Semyon Grigorev "Context-Free Path Querying
       by Kronecker Product", ADBIS 2020, pp 49-59, 2020
    """
    productions = source
    if os.path.isfile(source):
        with open(source, "r") as fin:
            productions = fin.read()

    boxes = list()

    for production in productions.splitlines():
        if not production:
            continue

        head, body = production.split(" -> ")

        body = body.replace("epsilon", "$").replace("eps", "$")
        if body == "":
            body = "$"

        boxes.append(
            (Variable(head), Regex(body).to_epsilon_nfa().to_deterministic().minimize())
        )

    return RSM(start_symbol, boxes)
