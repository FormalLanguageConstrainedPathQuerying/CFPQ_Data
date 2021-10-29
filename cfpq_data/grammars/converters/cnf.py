"""Create a context-free grammar in Chomsky normal form from different formats."""
import logging

from pyformlang.cfg import CFG, Epsilon
from pyformlang.rsa import RecursiveAutomaton as RSA

from cfpq_data.grammars.converters.cfg import cfg_from_rsa

__all__ = [
    "cnf_from_cfg",
    "cnf_from_rsa",
]


def cnf_from_cfg(cfg: CFG) -> CFG:
    """Create a context-free grammar in Chomsky normal form [1]_
    from given context-free grammar [2]_.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    Examples
    --------
    >>> from cfpq_data import *
    >>> gr = cfg_from_text("S -> a b")
    >>> cnf = cfpq_data.cnf_from_cfg(gr)
    >>> cfg_to_text(cnf)
    'S -> a#CNF# b#CNF#\\na#CNF# -> a\\nb#CNF# -> b'

    Returns
    -------
    cnf : CFG
        Context-free grammar in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    epsilon_productions = set()

    for production in cfg.productions:
        if production.body in ([], [Epsilon]):
            epsilon_productions.add(production)

    cnf = cfg.to_normal_form()

    cnf = CFG(
        variables=cnf.variables,
        terminals=cnf.terminals,
        start_symbol=cnf.start_symbol,
        productions=cnf.productions | epsilon_productions,
    )

    logging.info(f"Create {cnf=} from {cfg=}")

    return cnf


def cnf_from_rsa(rsa: RSA) -> CFG:
    """Create a context-free grammar in Chomsky normal form [1]_
    from Recursive State Automaton [2]_.

    Parameters
    ----------
    rsa : RSA
        Recursive State Automaton.

    Examples
    --------
    >>> from cfpq_data import *
    >>> gr = rsa_from_text("S -> a*")
    >>> cnf = cnf_from_rsa(gr)
    >>> cfg_to_text(cnf)
    'S -> \\nS -> a\\nS -> a#CNF# S\\na#CNF# -> a'

    Returns
    -------
    cnf : CFG
        Context-free grammar in Chomsky normal form.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    cnf = cnf_from_cfg(cfg_from_rsa(rsa=rsa))

    logging.info(f"Create {cnf=} from {rsa=}")

    return cnf
