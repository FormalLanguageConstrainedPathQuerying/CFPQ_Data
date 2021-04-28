"""Read (and write) a context-free grammar
in Chomsky normal form
from (and to) different sources.
"""
from pathlib import Path
from typing import Union

from pyformlang.cfg import Variable, CFG

from cfpq_data.grammars.converters.cnf import cnf_from_cfg
from cfpq_data.grammars.readwrite.cfg import cfg_from_txt, cfg_from_text

__all__ = [
    "cnf_from_text",
    "cnf_to_text",
    "cnf_from_txt",
    "cnf_to_txt",
]


def cnf_from_text(source: str, start_symbol: Variable = Variable("S")) -> CFG:
    """Create a context-free grammar
    in Chomsky normal form [1]_
    from text.

    Parameters
    ----------
    source : str
        The text with which
        the context-free grammar
        in Chomsky normal form
        will be created.

    start_symbol : Variable
        Start symbol of a context-free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_text("S -> a S b S | epsilon")
    >>> [cnf.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    """
    cfg = cfg_from_text(source, start_symbol)
    return cnf_from_cfg(cfg)


def cnf_to_text(cnf: CFG) -> str:
    """Turns a context-free grammar
    in Chomsky normal form [1]_
    into its text representation.

    Parameters
    ----------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_text("S -> a")
    >>> cfpq_data.cnf_to_text(cnf)
    'S -> a\\n'

    Returns
    -------
    text : str
        Context-free grammar
        in Chomsky normal form
        text representation.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    """
    return cnf.to_text()


def cnf_from_txt(
    source: Union[Path, str], start_symbol: Variable = Variable("S")
) -> CFG:
    """Create a context-free grammar
    in Chomsky normal form [1]_
    from TXT file.

    Parameters
    ----------
    source : Union[Path, str]
        The path to the TXT file with which
        the context-free grammar
        in Chomsky normal form
        will be created.

    start_symbol : Variable
        Start symbol of a context-free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf_1 = cfpq_data.cnf_from_text("S -> a S b S | epsilon")
    >>> path = cfpq_data.cnf_to_txt(cnf_1, "test.txt")
    >>> cnf = cfpq_data.cnf_from_txt(path)
    >>> [cnf.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    """
    cfg = cfg_from_txt(source, start_symbol)
    return cnf_from_cfg(cfg)


def cnf_to_txt(cnf: CFG, destination: Union[Path, str]) -> Path:
    """Saves a context-free grammar
    in Chomsky normal form [1]_
    text representation
    into TXT file.

    Parameters
    ----------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    destination : Union[Path, str]
        The path to the TXT file
        where context-free grammar
        in Chomsky normal form
        text representation
        will be saved.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_text("S -> a S b S")
    >>> path = cfpq_data.cnf_to_txt(cnf, "test.txt")

    Returns
    -------
    path : Path
        The path to the TXT file
        where context-free grammar
        text representation
        will be saved.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    """
    with open(destination, "w") as fout:
        fout.write(cnf_to_text(cnf))
    return Path(destination).resolve()
