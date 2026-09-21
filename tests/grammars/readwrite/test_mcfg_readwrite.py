from lark.exceptions import UnexpectedInput

import cfpq_data
from cfpq_data import MCFG, MCFGRule

# The 2-MCFG(2) for {w1 w2 # w2 w1 | w1, w2 in {0, 1}*} from the
# literature (docs/flpq.rst, "MCFG grammar format (.mcfg)").
dyck_2_mcfg = (
    "A(eps, eps)\n"
    "A(x1 0, x2 0) <- A(x1, x2)\n"
    "A(x1 1, x2 1) <- A(x1, x2)\n"
    "S(x1 y1 # y2 x2) <- A(x1, x2), A(y1, y2)"
)

# The dimension-1 grammar for {0^n 1^n 1^m 0^m | n, m >= 0}.
dimension_1_mcfg = (
    "A(eps)\nB(eps)\nA(0 x1 1) <- A(x1)\nB(1 x2 0) <- B(x2)\nS(x1 x2) <- A(x1), B(x2)"
)


def test_dyck_2_mcfg_from_text():
    mcfg = cfpq_data.mcfg_from_text(dyck_2_mcfg)

    assert isinstance(mcfg, MCFG)
    assert mcfg.start_symbol == "S"
    assert len(mcfg.rules) == 4
    assert mcfg.rules[0] == MCFGRule(head="A", head_args=(("eps",), ("eps",)), body=())
    assert mcfg.rules[1] == MCFGRule(
        head="A",
        head_args=(("x1", "0"), ("x2", "0")),
        body=(("A", ("x1", "x2")),),
    )
    assert mcfg.rules[3] == MCFGRule(
        head="S",
        head_args=(("x1", "y1", "#", "y2", "x2"),),
        body=(("A", ("x1", "x2")), ("A", ("y1", "y2"))),
    )


def test_dimension_1_mcfg_from_text():
    mcfg = cfpq_data.mcfg_from_text(dimension_1_mcfg)

    assert len(mcfg.rules) == 5
    assert mcfg.rules[0] == MCFGRule(head="A", head_args=(("eps",),), body=())
    assert mcfg.rules[4] == MCFGRule(
        head="S",
        head_args=(("x1", "x2"),),
        body=(("A", ("x1",)), ("B", ("x2",))),
    )


def test_comments_and_blank_lines_are_ignored():
    text = "# a comment\n\nA(eps)\n   # an indented comment\n\nS(x1) <- A(x1)\n"

    mcfg = cfpq_data.mcfg_from_text(text)

    assert len(mcfg.rules) == 2
    assert mcfg.rules[0] == MCFGRule(head="A", head_args=(("eps",),), body=())


def test_hash_terminal_in_arguments():
    mcfg = cfpq_data.mcfg_from_text("S(x1 # x2) <- A(x1, x2)")

    assert mcfg.rules[0] == MCFGRule(
        head="S",
        head_args=(("x1", "#", "x2"),),
        body=(("A", ("x1", "x2")),),
    )


def test_lowercase_letter_variables():
    mcfg = cfpq_data.mcfg_from_text("S(x1 y2 z10) <- A(x1, y2, z10)")

    assert mcfg.rules[0] == MCFGRule(
        head="S",
        head_args=(("x1", "y2", "z10"),),
        body=(("A", ("x1", "y2", "z10")),),
    )


def test_no_semantic_validation_yet():
    # Syntactically valid but semantically broken rule sets parse fine;
    # the semantic checks are added on top of this parser.
    mcfg = cfpq_data.mcfg_from_text("A(x1) <- B(x2)\nB(eps eps)")

    assert len(mcfg.rules) == 2


def test_empty_text():
    mcfg = cfpq_data.mcfg_from_text("")

    assert mcfg.rules == ()


def test_malformed_syntax_raises():
    for text in (
        "A(eps",  # unbalanced parenthesis
        "s(x1) <- A(x1)",  # lowercase head
        "A(eps,)",  # dangling comma
        "S(x1) <- A(a)",  # terminal in the body
        "foo",  # stray terminal at the top level
    ):
        try:
            cfpq_data.mcfg_from_text(text)
        except UnexpectedInput:
            pass
        else:
            raise AssertionError(f"{text!r} should raise UnexpectedInput")
