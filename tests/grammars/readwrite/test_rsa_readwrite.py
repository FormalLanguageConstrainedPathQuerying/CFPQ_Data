import os
import tempfile

import pytest

import cfpq_data

grammar_1 = "S -> a b"
grammar_2 = "S -> a"


@pytest.mark.parametrize(
    "grammar, expected",
    [(grammar_1, ["ab"]), (grammar_2, ["a"])],
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
    ],
)
def test_rsa_to_text(grammar, expected):
    rsa = cfpq_data.rsa_from_text(grammar)

    actual = set(cfpq_data.rsa_to_text(rsa).splitlines())

    assert actual == expected


@pytest.mark.parametrize(
    "grammar",
    [
        grammar_1,
        grammar_2,
    ],
)
def test_rsa_from_and_to_txt(grammar):
    (fd, fname) = tempfile.mkstemp()

    rsa_1 = cfpq_data.rsa_from_text(grammar)

    path = cfpq_data.rsa_to_txt(rsa_1, fname)

    rsa_2 = cfpq_data.rsa_from_txt(path)

    os.close(fd)
    os.unlink(fname)

    assert set(cfpq_data.rsa_to_text(rsa_1).splitlines()) == set(
        cfpq_data.rsa_to_text(rsa_2).splitlines()
    )
