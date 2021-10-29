import os
import tempfile

import pytest

import cfpq_data

grammar_1 = "S -> a b"
grammar_2 = "S -> a"
grammar_3 = "S -> a\nS -> b"
grammar_4 = "S -> \n#comment"


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, ["ab"]),
        (grammar_2, ["a"]),
        (grammar_3, ["a", "b"]),
        (grammar_4, [""]),
    ],
)
def test_rsa_from_text(grammar, expected):
    rsa = cfpq_data.rsa_from_text(grammar)
    cfg_from_rsa = cfpq_data.cfg_from_rsa(rsa)

    for word in expected:
        if word is not None:
            assert cfg_from_rsa.contains(word)


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, {"S -> ($.(a.b))"}),
        (grammar_2, {"S -> ($.a)"}),
        (grammar_3, {"S -> ($.(a|b))", "S -> ($.(b|a))"}),
        (grammar_4, {"S -> $"}),
    ],
)
def test_rsa_to_text(grammar, expected):
    rsa = cfpq_data.rsa_from_text(grammar)

    actual = set(cfpq_data.rsa_to_text(rsa).splitlines())

    assert actual.issubset(expected)
