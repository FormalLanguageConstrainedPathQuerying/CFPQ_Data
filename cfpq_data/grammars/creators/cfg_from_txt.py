"""Create a context free grammar [1]_
from txt file.

References
----------
.. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
"""
import os
from pathlib import Path
from typing import Union

from pyformlang.cfg import Variable, CFG

__all__ = ["cfg_from_txt"]


def cfg_from_txt(
    source: Union[Path, str], start_symbol: Variable = Variable("S")
) -> CFG:
    """Create a context free grammar [1]_
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
    >>> cfg = cfpq_data.cfg_from_txt("S -> a S b S | epsilon")
    >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cfg : CFG
        Context free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    productions = source
    if os.path.isfile(source):
        with open(source, "r") as fin:
            productions = fin.read()

    return CFG.from_text(productions, start_symbol)
