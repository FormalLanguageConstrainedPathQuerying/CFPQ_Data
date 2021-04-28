import os
import tempfile

import pytest

import cfpq_data

grammar_1 = "S -> a b"
grammar_2 = "S -> a"


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, ["ab"]),
        (grammar_2, ["a"]),
    ],
)
def test_rsm_from_text(grammar, expected):
    rsm = cfpq_data.rsm_from_text(grammar)

    for word in expected:
        assert rsm.contains(word)


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, {"S -> ($.(a.b))"}),
        (grammar_2, {"S -> ($.a)"}),
    ],
)
def test_rsm_to_text(grammar, expected):
    rsm = cfpq_data.rsm_from_text(grammar)

    actual = set(cfpq_data.rsm_to_text(rsm).splitlines())

    assert actual == expected


@pytest.mark.parametrize(
    "grammar",
    [
        grammar_1,
        grammar_2,
    ],
)
def test_rsm_from_and_to_txt(grammar):
    (fd, fname) = tempfile.mkstemp()

    rsm_1 = cfpq_data.rsm_from_text(grammar)

    path = cfpq_data.rsm_to_txt(rsm_1, fname)

    rsm_2 = cfpq_data.rsm_from_txt(path)

    os.close(fd)
    os.unlink(fname)

    assert set(cfpq_data.rsm_to_text(rsm_1).splitlines()) == set(
        cfpq_data.rsm_to_text(rsm_2).splitlines()
    )
