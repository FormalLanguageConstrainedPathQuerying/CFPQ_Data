"""Read (and write) a Recursive State Automaton
from (and to) different sources.
"""
from pathlib import Path
from typing import Union

from pyformlang.cfg import Epsilon, Variable
from pyformlang.finite_automaton.finite_automaton import to_symbol
from pyformlang.regular_expression import Regex
from pyformlang.rsa import Box, RecursiveAutomaton as RSA

__all__ = [
    "rsa_from_text",
    "rsa_to_text",
    "rsa_from_txt",
    "rsa_to_txt",
]


def rsa_from_text(source: str, start_symbol: Variable = Variable("S")) -> RSA:
    """Create a Recursive State Automaton [1]_ from text.

    Parameters
    ----------
    source : str
        The text with which
        the Recursive State Machine
        will be created.

    start_symbol : Variable
        Start symbol of a Recursive State Machine.

    Examples
    --------
    >>> import cfpq_data
    >>> rsa = cfpq_data.rsa_from_text("S -> (a S* b S*)*")

    Returns
    -------
    rsa : RSA
        Recursive State Automaton.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    productions = dict()
    boxes = set()
    labels = set()

    for production in source.splitlines():
        if " -> " not in production:
            continue

        head, body = production.split(" -> ")
        labels.add(to_symbol(head))

        if body == "":
            body = Epsilon().to_text()

        if head in productions:
            productions[head] += " | " + body
        else:
            productions[head] = body

    for head, body in productions.items():
        boxes.add(Box(Regex(body).to_epsilon_nfa().minimize(), to_symbol(head)))

    return RSA(labels, to_symbol(start_symbol), boxes)


def rsa_to_text(rsa: RSA) -> str:
    """Turns a Recursive State Automaton [1]_
    into its text representation.

    Parameters
    ----------
    rsa : RSA
        Recursive State Automaton.

    Examples
    --------
    >>> import cfpq_data
    >>> rsa = cfpq_data.rsa_from_text("S -> (a S* b S*)*")
    >>> text = cfpq_data.rsa_to_text(rsa)

    Returns
    -------
    text : str
        Recursive State Automaton text representation.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    productions = list()
    for symbol in rsa.labels:
        box = rsa.get_box(symbol)
        productions.append(f"{box.label.value} -> {box.dfa.to_regex()}")
    return "\n".join(productions)


def rsa_from_txt(
    source: Union[Path, str], start_symbol: Variable = Variable("S")
) -> RSA:
    """Create a Recursive State Automaton [1]_
    from TXT file.

    Parameters
    ----------
    source : Union[Path, str]
        The path to the TXT file with which
        the Recursive State Machine
        will be created.

    start_symbol : Variable
        Start symbol of a Recursive State Machine.

    Examples
    --------
    >>> import cfpq_data
    >>> rsa_1 = cfpq_data.rsa_from_text("S -> (a S* b S*)*")
    >>> path = cfpq_data.rsa_to_txt(rsa_1, "test.txt")
    >>> rsa = cfpq_data.rsa_from_txt(path)

    Returns
    -------
    rsa : RSA
        Recursive State Automaton.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    with open(source, "r") as fin:
        productions = fin.read()
    return rsa_from_text(productions, start_symbol)


def rsa_to_txt(rsa: RSA, destination: Union[Path, str]) -> Path:
    """Saves a Recursive State Automaton
    text representation
    into TXT file.

    Parameters
    ----------
    rsa : RSA
        Recursive State Automaton.

    destination : Union[Path, str]
        The path to the TXT file
        where Recursive State Machine
        text representation
        will be saved.

    Examples
    --------
    >>> import cfpq_data
    >>> rsa = cfpq_data.rsa_from_text("S -> (a S* b S*)*")
    >>> path = cfpq_data.rsa_to_txt(rsa, "test.txt")

    Returns
    -------
    path : Path
        The path to the TXT file
        where Recursive State Automaton
        text representation
        will be saved.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines.
       In: Berry G., Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    with open(destination, "w") as fout:
        fout.write(rsa_to_text(rsa))
    return Path(destination).resolve()
