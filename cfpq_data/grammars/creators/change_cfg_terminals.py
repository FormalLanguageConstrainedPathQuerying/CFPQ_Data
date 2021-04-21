"""Change terminals of a context free grammar [1]_.

References
----------
.. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
"""
import re
from typing import Dict

from cfpq_data.grammars.creators.cfg_from_txt import cfg_from_txt
from pyformlang.cfg import CFG

__all__ = ["change_cfg_terminals"]


def change_cfg_terminals(cfg: CFG, spec: Dict[str, str]) -> CFG:
    """Change terminals of a context free grammar [1]_.

    Parameters
    ----------
    cfg : CFG
        Context free grammar.

    spec: Dict
        Terminals mapping.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_txt("S -> a S b S")
    >>> new_cfg = cfpq_data.change_cfg_terminals(cfg, {"a": "b", "b": "c"})
    >>> new_cfg.to_text()
    'S -> b S c S\\n'

    Returns
    -------
    cfg : CFG
        Context free grammar with changed terminals.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    regex = re.compile("|".join(map(re.escape, spec.keys())))
    text = regex.sub(lambda match: spec[match.group(0)], cfg.to_text())
    return cfg_from_txt(text)
