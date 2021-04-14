"""Create a context free grammar
in Chomsky normal form [1]_
from txt file.

References
----------
.. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
"""
from pathlib import Path
from typing import Union

from pyformlang.cfg import Variable, CFG

from cfpq_data.grammars.creators.cfg_from_txt import cfg_from_txt
from cfpq_data.grammars.converters.cnf_from_cfg import cnf_from_cfg

__all__ = ["cnf_from_txt"]


def cnf_from_txt(
    source: Union[Path, str], start_symbol: Variable = Variable("S")
) -> CFG:
    """Create a context free grammar
    in Chomsky normal form [1]_
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
    >>> cnf = cfpq_data.cnf_from_txt("S -> a S b S | epsilon")
    >>> [cnf.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context free grammar in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    """
    cfg = cfg_from_txt(source, start_symbol)

    return cnf_from_cfg(cfg)
