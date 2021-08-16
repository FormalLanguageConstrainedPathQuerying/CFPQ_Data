"""Read (and write) a Recursive State Machine
from (and to) different sources.
"""
from pathlib import Path
from typing import Union

from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from cfpq_data.grammars.rsm import RSM

__all__ = [
    "rsm_from_text",
    "rsm_to_text",
    "rsm_from_txt",
    "rsm_to_txt",
]


# TODO: Remove in cfpq_data 2.0.0
def rsm_from_text(source: str, start_symbol: Variable = Variable("S")) -> RSM:
    """Create a Recursive State Machine [1]_ from text.

    .. deprecated:: 2.0.0

       The function `rsm_from_text` will be replaced
       with function `rsa_from_text`

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
    >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
    >>> [rsm.contains(word) for word in ["", "ab", "aabb"]]
    [True, True, True]

    Returns
    -------
    rsm : RSM
        Recursive State Machine.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
       Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    import warnings

    msg = (
        "\nThe function `rsm_from_text` will be replaced "
        "with function `rsa_from_text` in "
        "cfpq_data 2.0.0\n"
    )

    warnings.warn(msg, FutureWarning, stacklevel=2)

    boxes = list()

    for production in source.splitlines():
        if " -> " not in production:
            continue

        head, body = production.split(" -> ")

        body = body.replace("epsilon", "$").replace("eps", "$")
        if body == "":
            body = "$"

        boxes.append(
            (Variable(head), Regex(body).to_epsilon_nfa().to_deterministic().minimize())
        )

    return RSM(start_symbol, boxes)


# TODO: Remove in cfpq_data 2.0.0
def rsm_to_text(rsm: RSM) -> str:
    """Turns a Recursive State Machine [1]_
    into its text representation.

    .. deprecated:: 2.0.0

       The function `rsm_to_text` will be replaced
       with function `rsa_to_text`

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
    >>> text = cfpq_data.rsm_to_text(rsm)

    Returns
    -------
    text : str
        Recursive State Machine text representation.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
       Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    import warnings

    msg = (
        "\nThe function `rsm_to_text` will be replaced "
        "with function `rsa_to_text` in "
        "cfpq_data 2.0.0\n"
    )

    warnings.warn(msg, FutureWarning, stacklevel=2)

    return rsm.to_text()


# TODO: Remove in cfpq_data 2.0.0
def rsm_from_txt(
    source: Union[Path, str], start_symbol: Variable = Variable("S")
) -> RSM:
    """Create a Recursive State Machine [1]_
    from TXT file.

    .. deprecated:: 2.0.0

       The function `rsm_from_txt` will be replaced
       with function `rsa_from_txt`

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
    >>> rsm_1 = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
    >>> path = cfpq_data.rsm_to_txt(rsm_1, "test.txt")
    >>> rsm = cfpq_data.rsm_from_txt(path)

    Returns
    -------
    rsm : RSM
        Recursive State Machine.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
       Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    import warnings

    msg = (
        "\nThe function `rsm_from_txt` will be replaced "
        "with function `rsa_from_txt` in "
        "cfpq_data 2.0.0\n"
    )

    warnings.warn(msg, FutureWarning, stacklevel=2)

    with open(source, "r") as fin:
        productions = fin.read()
    return rsm_from_text(productions, start_symbol)


# TODO: Remove in cfpq_data 2.0.0
def rsm_to_txt(rsm: RSM, destination: Union[Path, str]) -> Path:
    """Saves a Recursive State Machine
    text representation
    into TXT file.

    .. deprecated:: 2.0.0

       The function `rsm_to_txt` will be replaced
       with function `rsa_to_txt`

    Parameters
    ----------
    rsm : RSM
        Recursive State Machine.

    destination : Union[Path, str]
        The path to the TXT file
        where Recursive State Machine
        text representation
        will be saved.

    Examples
    --------
    >>> import cfpq_data
    >>> rsm = cfpq_data.rsm_from_text("S -> (a S* b S*)*")
    >>> path = cfpq_data.rsm_to_txt(rsm, "test.txt")

    Returns
    -------
    path : Path
        The path to the TXT file
        where Recursive State Machine
        text representation
        will be saved.

    References
    ----------
    .. [1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of Recursive State Machines. In: Berry G.,
       Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
       Lecture Notes in Computer Science, vol 2102.
       Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
    """
    import warnings

    msg = (
        "\nThe function `rsm_to_txt` will be replaced "
        "with function `rsa_to_txt` in "
        "cfpq_data 2.0.0\n"
    )

    warnings.warn(msg, FutureWarning, stacklevel=2)

    with open(destination, "w") as fout:
        fout.write(rsm_to_text(rsm))
    return Path(destination).resolve()
