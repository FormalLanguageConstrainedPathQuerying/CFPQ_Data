"""Change terminals
of a context-free grammar
in different formats.
"""
import re
from typing import Dict

from pyformlang.cfg import CFG

from cfpq_data.grammars.readwrite.cfg import cfg_from_text
from cfpq_data.grammars.readwrite.cnf import cnf_from_text
from cfpq_data.grammars.readwrite.rsm import rsm_from_text
from cfpq_data.grammars.rsm import RSM

__all__ = [
    "change_terminals_in_cfg",
    "change_terminals_in_cnf",
    "change_terminals_in_rsm",
]


def change_terminals_in_cfg(cfg: CFG, spec: Dict[str, str]) -> CFG:
    """Change terminals of
    a context-free grammar [1]_.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    spec: Dict
        Terminals mapping.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_text("S -> a S b S")
    >>> new_cfg = cfpq_data.change_terminals_in_cfg(cfg, {"a": "b", "b": "c"})
    >>> new_cfg.to_text()
    'S -> b S c S\\n'

    Returns
    -------
    cfg : CFG
        Context-free grammar with changed terminals.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    regex = re.compile("|".join(map(re.escape, spec.keys())))
    text = regex.sub(lambda match: spec[match.group(0)], cfg.to_text())
    return cfg_from_text(text)


def change_terminals_in_cnf(cnf: CFG, spec: Dict[str, str]) -> CFG:
    """Change terminals of
    a context-free grammar [1]_
    in Chomsky normal form.

    Parameters
    ----------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    spec: Dict
        Terminals mapping.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_text("S -> a S b S | epsilon")
    >>> new_cnf = cfpq_data.change_terminals_in_cnf(cnf, {"a": "b", "b": "c"})
    >>> [new_cnf.contains(word) for word in ["", "bc", "bbcc"]]
    [True, True, True]

    Returns
    -------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form
        with changed terminals.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    """
    regex = re.compile("|".join(map(re.escape, spec.keys())))
    text = regex.sub(lambda match: spec[match.group(0)], cnf.to_text())
    return cnf_from_text(text)


def change_terminals_in_rsm(rsm: RSM, spec: Dict[str, str]) -> RSM:
    """Change terminals of
    a Recursive State Machine [1]_.

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    spec: Dict
        Terminals mapping.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
    >>> new_rsm = cfpq_data.change_terminals_in_rsm(rsm, {"a": "b", "b": "c"})
    >>> [new_rsm.contains(word) for word in ["", "bc", "bbcc"]]
    [True, True, True]

    Returns
    -------
    rsm : RSM
        Recursive State Machine
        with changed terminals.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
       Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    regex = re.compile("|".join(map(re.escape, spec.keys())))
    text = regex.sub(lambda match: spec[match.group(0)], rsm.to_text())
    return rsm_from_text(text)
