"""Read (and write) a context-free grammar
from (and to) different sources.
"""
from pathlib import Path
from typing import Union

from pyformlang.cfg import Variable, CFG

__all__ = [
    "cfg_from_text",
    "cfg_to_text",
    "cfg_from_txt",
    "cfg_to_txt",
]


def cfg_from_text(source: str, start_symbol: Variable = Variable("S")) -> CFG:
    """Create a context-free grammar [1]_ from text.

    Parameters
    ----------
    source : str
        The text with which
        the context-free grammar
        will be created.

    start_symbol : Variable
        Start symbol of a context-free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_text("S -> a S b S")
    >>> cfpq_data.cfg_to_text(cfg)
    'S -> a S b S\\n'

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    return CFG.from_text(source, start_symbol)


def cfg_to_text(cfg: CFG) -> str:
    """Turns a context-free grammar [1]_
    into its text representation.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_text("S -> a S b S")
    >>> cfpq_data.cfg_to_text(cfg)
    'S -> a S b S\\n'

    Returns
    -------
    text : str
        Context-free grammar
        text representation.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    return cfg.to_text()


def cfg_from_txt(
    source: Union[Path, str], start_symbol: Variable = Variable("S")
) -> CFG:
    """Create a context-free grammar [1]_
    from TXT file.

    Parameters
    ----------
    source : Union[Path, str]
        The path to the TXT file with which
        the context-free grammar will be created.

    start_symbol : Variable
        Start symbol of a context-free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg_1 = cfpq_data.cfg_from_text("S -> a S b S")
    >>> path = cfpq_data.cfg_to_txt(cfg_1, "test.txt")
    >>> cfg = cfpq_data.cfg_from_txt(path)
    >>> cfpq_data.cfg_to_text(cfg)
    'S -> a S b S\\n'

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    with open(source, "r") as fin:
        productions = fin.read()
    return cfg_from_text(productions, start_symbol)


def cfg_to_txt(cfg: CFG, destination: Union[Path, str]) -> Path:
    """Saves a context-free grammar [1]_
    text representation
    into TXT file.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    destination : Union[Path, str]
        The path to the TXT file
        where context-free grammar
        text representation
        will be saved.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_text("S -> a S b S")
    >>> path = cfpq_data.cfg_to_txt(cfg, "test.txt")

    Returns
    -------
    path : Path
        The path to the TXT file
        where context-free grammar
        text representation
        will be saved.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    with open(destination, "w") as fout:
        fout.write(cfg_to_text(cfg))
    return Path(destination).resolve()
