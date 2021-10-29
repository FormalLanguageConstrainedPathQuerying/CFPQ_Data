"""Read (and write) a context-free grammar from (and to) different sources."""
import logging
import pathlib
from typing import Union

from pyformlang.cfg import Variable, CFG

__all__ = [
    "cfg_from_text",
    "cfg_to_text",
    "cfg_from_txt",
    "cfg_to_txt",
]


def cfg_from_text(text: str, *, start_symbol: Variable = Variable("S")) -> CFG:
    """Create a context-free grammar [1]_ from text.

    Parameters
    ----------
    text : str
        The text with which the context-free grammar will be created.

    start_symbol : Variable
        Start symbol of a context-free grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cfg = cfg_from_text("S -> a S b S")
    >>> cfg_to_text(cfg)
    'S -> a S b S'

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    cfg = CFG.from_text(text=text, start_symbol=start_symbol)

    logging.info(f"Create {cfg=} from {text=}, {start_symbol=}")

    return cfg


def cfg_to_text(cfg: CFG) -> str:
    """Turns a context-free grammar [1]_ into its text representation.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cfg = cfg_from_text("S -> a S b S | epsilon")
    >>> cfg_to_text(cfg)
    'S -> \\nS -> a S b S'

    Returns
    -------
    text : str
        Context-free grammar text representation.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    productions = [
        f"{p.head.value} -> " + " ".join(map(lambda x: x.value, p.body))
        for p in cfg.productions
    ]

    productions.sort(
        key=lambda s: (s.split(" -> ")[0] != cfg.start_symbol.value, s),
    )

    text = "\n".join(productions)

    logging.info(f"Turn {cfg=} into {text=}")

    return text


def cfg_from_txt(
    path: Union[pathlib.Path, str], *, start_symbol: Variable = Variable("S")
) -> CFG:
    """Create a context-free grammar [1]_ from TXT file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the TXT file with which the context-free grammar will be created.

    start_symbol : Variable
        Start symbol of a context-free grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cfg_1 = cfg_from_text("S -> a S b S | epsilon")
    >>> path = cfg_to_txt(cfg_1, "test.txt")
    >>> cfg = cfg_from_txt(path)
    >>> cfg_to_text(cfg)
    'S -> \\nS -> a S b S'

    Returns
    -------
    cfg : CFG
        Context-free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    with open(path, "r") as f:
        productions = f.read()

    cfg = cfg_from_text(productions, start_symbol=start_symbol)

    logging.info(f"Create {cfg=} from {path=}, {start_symbol=}")

    return cfg


def cfg_to_txt(cfg: CFG, path: Union[pathlib.Path, str]) -> pathlib.Path:
    """Saves a context-free grammar [1]_ text representation into TXT file.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    path : Union[Path, str]
        The path to the TXT file where context-free grammar text representation
        will be saved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> cfg = cfg_from_text("S -> a S b S")
    >>> path = cfg_to_txt(cfg, "test.txt")

    Returns
    -------
    path : Path
        The path to the TXT file where context-free grammar text representation
        will be saved.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    with open(path, "w") as f:
        f.write(cfg_to_text(cfg))

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {cfg=} to {dest=}")

    return dest
