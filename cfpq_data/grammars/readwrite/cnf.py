"""Read (and write) a context-free grammar in Chomsky normal form
from (and to) different sources."""
import logging
import pathlib
from typing import Union

from pyformlang.cfg import Variable, CFG

from cfpq_data.grammars.converters.cnf import cnf_from_cfg
from cfpq_data.grammars.readwrite.cfg import cfg_from_text

__all__ = [
    "cnf_from_text",
    "cnf_from_txt",
]


def cnf_from_text(text: str, *, start_symbol: Variable = Variable("S")) -> CFG:
    """Create a context-free grammar in Chomsky normal form [1]_ from text.

    Parameters
    ----------
    text : str
        The text with which the context-free grammar in Chomsky normal form
        will be created.

    start_symbol : Variable
        Start symbol of a context-free grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cnf = cnf_from_text("S -> a b")
    >>> cfg_to_text(cnf)
    'S -> a#CNF# b#CNF#\\na#CNF# -> a\\nb#CNF# -> b'

    Returns
    -------
    cnf : CFG
        Context-free grammar in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    """
    cnf = cnf_from_cfg(cfg_from_text(text, start_symbol=start_symbol))

    logging.info(f"Create {cnf=} from {text=}, {start_symbol=}")

    return cnf


def cnf_from_txt(
    path: Union[pathlib.Path, str], *, start_symbol: Variable = Variable("S")
) -> CFG:
    """Create a context-free grammar in Chomsky normal form [1]_ from TXT file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the TXT file with which the context-free grammar
        in Chomsky normal form will be created.

    start_symbol : Variable
        Start symbol of a context-free grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cnf_1 = cfg_from_text("S -> a b")
    >>> path = cfg_to_txt(cnf_1, "test.txt")
    >>> cnf = cnf_from_txt(path)
    >>> cfg_to_text(cnf)
    'S -> a#CNF# b#CNF#\\na#CNF# -> a\\nb#CNF# -> b'

    Returns
    -------
    cnf : CFG
        Context-free grammar in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    """
    with open(path, "r") as f:
        productions = f.read()

    cnf = cnf_from_text(productions, start_symbol=start_symbol)

    logging.info(f"Create {cnf=} from {path=}, {start_symbol=}")

    return cnf
