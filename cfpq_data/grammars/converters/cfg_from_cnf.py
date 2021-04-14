"""Create a context free grammar [2]_
from given context free grammar
in Chomsky normal form [1]_.

References
----------
.. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
.. [2] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
"""
from pyformlang.cfg import CFG

__all__ = ["cfg_from_cnf"]


def cfg_from_cnf(cnf: CFG) -> CFG:
    """Create a context free grammar [2]_
    from given context free grammar
    in Chomsky normal form [1]_.

    Parameters
    ----------
    cnf : CFG
        Context free grammar in Chomsky normal form.

    Examples
    --------
    >>> import cfpq_data
    >>> cnf = cfpq_data.cnf_from_txt("S -> a S b S | epsilon")
    >>> cfg = cfpq_data.cfg_from_cnf(cnf)
    >>> [cfg.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    cfg : CFG
        Context free grammar.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chomsky_normal_form
    .. [2] https://en.wikipedia.org/wiki/Context-free_grammar#Formal_definitions
    """
    return CFG.from_text(cnf.to_text(), cnf.start_symbol)
