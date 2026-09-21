"""Read (and write) a multiple context-free grammar from (and to) different sources."""

import logging
from dataclasses import dataclass

from lark import Lark, Transformer

__all__ = [
    "MCFG",
    "MCFGRule",
    "mcfg_from_text",
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


def mcfg_from_text(text: str) -> MCFG:
    """Create a multiple context-free grammar [1]_ from text.

    Parameters
    ----------
    text : str
        The text with which the multiple context-free grammar will be created.

    Examples
    --------
    >>> from cfpq_data import *
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
    >>> mcfg.rules[3].head
    'S'

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

    mcfg = MCFG(rules=rules, start_symbol="S")

    logging.info(f"Create {mcfg=} from {text=}")

    return mcfg
