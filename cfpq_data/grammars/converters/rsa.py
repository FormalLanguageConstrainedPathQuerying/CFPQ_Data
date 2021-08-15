"""Create a Recursive State Automaton
from different formats.
"""
from pyformlang.cfg import CFG
from pyformlang.rsa import RecursiveAutomaton as RSA

__all__ = [
    "rsa_from_cfg",
    "rsa_from_cnf",
]


def rsa_from_cfg(cfg: CFG) -> RSA:
    """Create a Recursive State Automaton [2]_
    from context-free grammar [1]_.

    Parameters
    ----------
    cfg : CFG
        Context-free grammar.

    Examples
    --------
    >>> import cfpq_data
    >>> cfg = cfpq_data.cfg_from_text("S -> a S b S | a b")
    >>> rsa = cfpq_data.rsa_from_cfg(cfg)

    Returns
    -------
    rsa : RSA
        Recursive State Automaton.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    .. [2] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    return RSA.from_cfg(cfg)


def rsa_from_cnf(cnf: CFG) -> RSA:
    """Create a Recursive State Automaton [2]_
    from context-free grammar
    in Chomsky normal form [1]_.

    Parameters
    ----------
    cnf : CFG
        Context-free grammar
        in Chomsky normal form.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_text("S -> a S b S | a b")
    >>> rsa = cfpq_data.rsa_from_cnf(cnf)

    Returns
    -------
    rsa : RSA
        Recursive State Automaton.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    return rsa_from_cfg(cnf)
