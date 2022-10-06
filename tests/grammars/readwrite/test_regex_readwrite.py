import os
import tempfile

import pytest

import cfpq_data

expression_1 = "abc|d*"
expression_2 = "a (bc|d*)"


@pytest.mark.parametrize(
    "expression, expected, not_expected",
    [
        (expression_1, [["abc"], ["d", "d", "d"], []], [["a"], ["a", "d"]]),
        (
            expression_2,
            [["a"], ["a", "bc"], ["a", "d", "d"]],
            [[], ["bc"], ["a", "bc", "d"]],
        ),
    ],
)
def test_cfg_from_text(expression, expected, not_expected):
    regex = cfpq_data.regex_from_text(expression)

    for word in expected:
        assert regex.accepts(word)

    for word in not_expected:
        assert not regex.accepts(word)


@pytest.mark.parametrize(
    "expression, expected",
    [
        (expression_1, "(abc|(d)*)"),
        (expression_2, "(a (bc|(d)*))"),
    ],
)
def test_regex_to_text(expression, expected):
    regex = cfpq_data.regex_from_text(expression)

    assert cfpq_data.regex_to_text(regex) == expected


@pytest.mark.parametrize(
    "expression",
    [
        expression_1,
        expression_2,
    ],
)
def test_regex_from_and_to_txt(expression):
    (fd, fname) = tempfile.mkstemp()

    regex_1 = cfpq_data.regex_from_text(expression)

    path = cfpq_data.regex_to_txt(regex_1, fname)

    regex_2 = cfpq_data.regex_from_txt(path)

    os.close(fd)
    os.unlink(fname)

    assert cfpq_data.regex_to_text(regex_1) == cfpq_data.regex_to_text(regex_2)
