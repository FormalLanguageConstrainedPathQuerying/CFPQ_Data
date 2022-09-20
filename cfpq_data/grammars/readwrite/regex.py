"""Read (and write) a regular expression from (and to) different sources."""
import logging
import pathlib
from typing import Union

from pyformlang.regular_expression import Regex

__all__ = [
    "regex_from_text",
    "regex_to_text",
    "regex_from_txt",
    "regex_to_txt",
]


def regex_from_text(text: str) -> Regex:
    """Create a regular expression [1]_ from text.

    Parameters
    ----------
    text : str
        The text with which the regular expression will be created.

    Examples
    --------
    >>> from cfpq_data import *
    >>> regex = regex_from_text("a (bc|d*)")
    >>> regex_to_text(regex)
    '(a (bc|(d)*))'

    Returns
    -------
    regex : Regex
        Regular expression.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Regular_expression#Formal_definition
    """
    regex = Regex(text)

    logging.info(f"Create {regex=} from {text=}")

    return regex


def regex_to_text(regex: Regex) -> str:
    """Turns a regular expression [1]_ into its text representation.

    Parameters
    ----------
    regex : Regex
        Regular expression.

    Examples
    --------
    >>> from cfpq_data import *
    >>> regex = regex_from_text("a (bc|d*)")
    >>> regex_to_text(regex)
    '(a (bc|(d)*))'

    Returns
    -------
    text : str
        Regular expression text representation.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Regular_expression#Formal_definition
    """

    text = str(regex).replace(".", " ")

    logging.info(f"Turn {regex=} into {text=}")

    return text


def regex_from_txt(path: Union[pathlib.Path, str]) -> Regex:
    """Create a regular expression [1]_ from TXT file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the TXT file with which the regular expression will be created.

    Examples
    --------
    >>> from cfpq_data import *
    >>> regex_1 = regex_from_text("a (bc|d*)")
    >>> path = regex_to_txt(regex_1, "test.txt")
    >>> regex = regex_from_txt(path)
    >>> regex_to_text(regex)
    '(a (bc|(d)*))'

    Returns
    -------
    regex : Regex
        Regular expression.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Regular_expression#Formal_definition
    """
    with open(path, "r") as f:
        expression = f.read()

    regex = regex_from_text(expression)

    logging.info(f"Create {regex=} from {path=}")

    return regex


def regex_to_txt(regex: Regex, path: Union[pathlib.Path, str]) -> pathlib.Path:
    """Saves a regular expression [1]_ text representation into TXT file.

    Parameters
    ----------
    regex : Regex
        Regular expression.

    path : Union[Path, str]
        The path to the TXT file where regular expression text representation
        will be saved.

    Examples
    --------
    >>> from cfpq_data import *
    >>> regex = regex_from_text("a (bc|d*)")
    >>> path = regex_to_txt(regex, "test.txt")

    Returns
    -------
    path : Path
        The path to the TXT file where regular expression text representation
        will be saved.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Regular_expression#Formal_definition
    """
    with open(path, "w") as f:
        f.write(regex_to_text(regex))

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {regex=} to {dest=}")

    return dest
