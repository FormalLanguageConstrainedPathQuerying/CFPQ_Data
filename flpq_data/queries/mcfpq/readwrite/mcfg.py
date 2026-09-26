"""Read (and write) a multiple context-free grammar from (and to) different sources."""

import logging
import pathlib
import re
from dataclasses import dataclass
from typing import Union

from lark import Lark, Transformer

__all__ = [
    "MCFG",
    "MCFGRule",
    "mcfg_from_text",
    "mcfg_from_txt",
    "mcfg_to_text",
    "mcfg_to_txt",
]

# Datalog-like syntax for MCFGs (docs/flpq.rst, "MCFG grammar format
# (.mcfg)"): one rule per line; a '#' at the start of a line comments out
# the rest of the line; nonterminals are identifiers starting with an
# uppercase letter; variables are a lowercase letter followed by digits
# (the literature's x^i, y^j notation); 'eps' is the empty string; '<-'
# separates the head from the body. The LALR contextual lexer makes '#'
# context-sensitive: COMMENT is only valid between rules, so inside
# argument lists '#' matches TERMINAL (the spec's examples use it as an
# edge label). EPS/VARIABLE/NONTERMINAL outrank the catch-all TERMINAL, so
# 'eps', 'x1', and uppercase identifiers never lex as terminals; a token
# that merely starts with one of those patterns (e.g. 'x1a') lexes as the
# higher-priority prefix plus the rest — no dataset label has this form.
_MCFG_GRAMMAR = r"""
    start: (COMMENT | rule)*

    rule: basic_rule | production_rule
    basic_rule: NONTERMINAL "(" args ")"
    production_rule: NONTERMINAL "(" args ")" ARROW body

    args: arg ("," arg)*
    arg: (TERMINAL | VARIABLE | EPS)+
    body: atom ("," atom)*
    atom: NONTERMINAL "(" vars ")"
    vars: VARIABLE ("," VARIABLE)*

    COMMENT.3: /#[^\n]*/
    NONTERMINAL.2: /[A-Z]\w*/
    VARIABLE.2: /[a-z][0-9]+/
    EPS.2: /eps/
    TERMINAL.1: /[^ \t\r\n(),<>-]+/
    ARROW: /<-/

    %ignore /[ \t\r\n]/
"""

_PARSER = Lark(_MCFG_GRAMMAR, parser="lalr")


@dataclass(frozen=True)
class MCFGRule:
    """A rule of a multiple context-free grammar.

    A basic rule is a production with an empty body: ``A(eps, eps)`` is
    stored as ``MCFGRule("A", (("eps",), ("eps",)), ())``.
    """

    head: str
    head_args: tuple[tuple[str, ...], ...]
    body: tuple[tuple[str, tuple[str, ...]], ...] = ()


@dataclass(frozen=True)
class MCFG:
    """A multiple context-free grammar in the Datalog-like ``.mcfg`` syntax."""

    rules: tuple[MCFGRule, ...]
    start_symbol: str = "S"

    @property
    def dimension(self) -> int:
        """The maximum arity of a nonterminal (the :math:`d` of
        :math:`d`-MCFG(:math:`r`))."""
        sizes = [len(rule.head_args) for rule in self.rules]
        sizes.extend(len(args) for rule in self.rules for _, args in rule.body)
        return max(sizes, default=0)

    @property
    def rank(self) -> int:
        """The maximum number of body atoms of a rule (the :math:`r` of
        :math:`d`-MCFG(:math:`r`))."""
        return max((len(rule.body) for rule in self.rules), default=0)


_VARIABLE_RE = re.compile(r"[a-z][0-9]+")


def _validate_mcfg(rules: tuple[MCFGRule, ...], start_symbol: str) -> None:
    arities: dict[str, int] = {}
    for rule in rules:
        if rule.head in arities and arities[rule.head] != len(rule.head_args):
            raise ValueError(
                f"The nonterminal {rule.head} has inconsistent arity: "
                f"{arities[rule.head]} and {len(rule.head_args)}"
            )
        arities[rule.head] = len(rule.head_args)
        for head, args in rule.body:
            if head in arities and arities[head] != len(args):
                raise ValueError(
                    f"The nonterminal {head} has inconsistent arity: "
                    f"{arities[head]} and {len(args)}"
                )
            arities.setdefault(head, len(args))

    for rule in rules:
        body_variables = [var for _, args in rule.body for var in args]
        if len(set(body_variables)) != len(body_variables):
            duplicated = sorted(
                {var for var in body_variables if body_variables.count(var) > 1}
            )
            raise ValueError(
                f"The body variables of the rule {rule} are not pairwise "
                f"distinct: {', '.join(duplicated)}"
            )
        head_variables = [
            token
            for arg in rule.head_args
            for token in arg
            if _VARIABLE_RE.fullmatch(token)
        ]
        if sorted(head_variables) != sorted(body_variables):
            raise ValueError(
                f"The rule {rule} has dangling variables: the head uses "
                f"{sorted(set(head_variables))}, the body uses "
                f"{sorted(set(body_variables))}"
            )
        if rule.body and any("eps" in arg for arg in rule.head_args):
            raise ValueError(
                f"The rule {rule} uses 'eps' in a production; 'eps' is only "
                "allowed in basic rules (rules without a body)"
            )

    if start_symbol not in arities:
        raise ValueError(
            f"The start symbol {start_symbol} does not occur in the grammar"
        )
    if arities[start_symbol] != 1:
        raise ValueError(
            f"The start symbol {start_symbol} must have arity 1, "
            f"not {arities[start_symbol]}"
        )


class _MCFGBuilder(Transformer):
    def arg(self, items):
        return tuple(str(item) for item in items)

    def args(self, items):
        return tuple(items)

    def vars(self, items):
        return tuple(str(item) for item in items)

    def atom(self, items):
        return (str(items[0]), items[1])

    def body(self, items):
        return tuple(items)

    def basic_rule(self, items):
        return MCFGRule(head=str(items[0]), head_args=items[1], body=())

    def production_rule(self, items):
        return MCFGRule(head=str(items[0]), head_args=items[1], body=items[3])

    def rule(self, items):
        return items[0]

    def start(self, items):
        return tuple(item for item in items if isinstance(item, MCFGRule))


def mcfg_from_text(text: str, *, start_symbol: str = "S") -> MCFG:
    """Create a multiple context-free grammar [1]_ from text.

    Parameters
    ----------
    text : str
        The text with which the multiple context-free grammar will be created.

    start_symbol : str
        Start symbol of a multiple context-free grammar.

    Examples
    --------
    >>> from flpq_data import *
    >>> text = (
    ...     "A(eps, eps)\\n"
    ...     "A(x1 0, x2 0) <- A(x1, x2)\\n"
    ...     "A(x1 1, x2 1) <- A(x1, x2)\\n"
    ...     "S(x1 y1 # y2 x2) <- A(x1, x2), A(y1, y2)"
    ... )
    >>> mcfg = mcfg_from_text(text)
    >>> len(mcfg.rules)
    4
    >>> mcfg.rules[0]
    MCFGRule(head='A', head_args=(('eps',), ('eps',)), body=())
    >>> mcfg.dimension, mcfg.rank
    (2, 2)

    Returns
    -------
    mcfg : MCFG
        Multiple context-free grammar.

    References
    ----------
    .. [1] https://arxiv.org/abs/2411.06383
    """
    tree = _PARSER.parse(text)
    rules = _MCFGBuilder().transform(tree)

    _validate_mcfg(rules, start_symbol)

    mcfg = MCFG(rules=rules, start_symbol=start_symbol)

    logging.info(f"Create {mcfg=} from {text=}, {start_symbol=}")

    return mcfg


def _render_rule(rule: MCFGRule) -> str:
    head = f"{rule.head}(" + ", ".join(" ".join(arg) for arg in rule.head_args) + ")"
    if not rule.body:
        return head
    body = ", ".join(
        f"{atom_head}(" + ", ".join(atom_vars) + ")"
        for atom_head, atom_vars in rule.body
    )
    return f"{head} <- {body}"


def mcfg_to_text(mcfg: MCFG) -> str:
    """Turns a multiple context-free grammar [1]_ into its text representation.

    The rendering is canonical: one rule per line, argument tokens
    space-joined, so the same model always produces the same text and
    ``mcfg_to_text(mcfg_from_text(text))`` reproduces ``text`` up to
    whitespace and comments.

    Parameters
    ----------
    mcfg : MCFG
        Multiple context-free grammar.

    Examples
    --------
    >>> from flpq_data import *
    >>> text = (
    ...     "A(eps, eps)\\n"
    ...     "A(x1 0, x2 0) <- A(x1, x2)\\n"
    ...     "A(x1 1, x2 1) <- A(x1, x2)\\n"
    ...     "S(x1 y1 # y2 x2) <- A(x1, x2), A(y1, y2)"
    ... )
    >>> mcfg_to_text(mcfg_from_text(text)) == text
    True

    Returns
    -------
    text : str
        Multiple context-free grammar text representation.

    References
    ----------
    .. [1] https://arxiv.org/abs/2411.06383
    """
    text = "\n".join(_render_rule(rule) for rule in mcfg.rules)

    logging.info(f"Turn {mcfg=} into {text=}")

    return text


def mcfg_from_txt(path: Union[pathlib.Path, str], *, start_symbol: str = "S") -> MCFG:
    """Create a multiple context-free grammar [1]_ from an ``.mcfg`` file.

    Parameters
    ----------
    path : Union[Path, str]
        The path to the ``.mcfg`` file with which the multiple context-free
        grammar will be created.

    start_symbol : str
        Start symbol of a multiple context-free grammar.

    Examples
    --------
    >>> from flpq_data import *
    >>> mcfg = mcfg_from_text("A(eps)\\nS(x1) <- A(x1)")
    >>> path = mcfg_to_txt(mcfg, "test.mcfg")
    >>> mcfg_from_txt(path) == mcfg
    True

    Returns
    -------
    mcfg : MCFG
        Multiple context-free grammar.

    References
    ----------
    .. [1] https://arxiv.org/abs/2411.06383
    """
    with open(path, "r") as f:
        text = f.read()

    mcfg = mcfg_from_text(text, start_symbol=start_symbol)

    logging.info(f"Create {mcfg=} from {path=}, {start_symbol=}")

    return mcfg


def mcfg_to_txt(mcfg: MCFG, path: Union[pathlib.Path, str]) -> pathlib.Path:
    """Saves a multiple context-free grammar [1]_ text representation into an
    ``.mcfg`` file.

    Parameters
    ----------
    mcfg : MCFG
        Multiple context-free grammar.

    path : Union[Path, str]
        The path to the ``.mcfg`` file where the multiple context-free
        grammar text representation will be saved.

    Examples
    --------
    >>> from flpq_data import *
    >>> mcfg = mcfg_from_text("A(eps)\\nS(x1) <- A(x1)")
    >>> path = mcfg_to_txt(mcfg, "test.mcfg")

    Returns
    -------
    path : Path
        The path to the ``.mcfg`` file where the text representation will be
        saved.

    References
    ----------
    .. [1] https://arxiv.org/abs/2411.06383
    """
    with open(path, "w") as f:
        f.write(mcfg_to_text(mcfg))

    dest = pathlib.Path(path).resolve()

    logging.info(f"Save {mcfg=} to {dest=}")

    return dest
