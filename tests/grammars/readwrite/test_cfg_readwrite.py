import os
import tempfile

import pytest

import cfpq_data

grammar_1 = "S -> a S b S\nS -> \n"
grammar_2 = "S -> a S\nS -> \n"


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, "S -> \nS -> a S b S"),
        (grammar_2, "S -> \nS -> a S"),
    ],
)
def test_cfg_from_text(grammar, expected):
    cfg = cfpq_data.cfg_from_text(grammar)

    assert cfpq_data.cfg_to_text(cfg) == expected


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, {"S -> a S b S", "S -> "}),
        (grammar_2, {"S -> a S", "S -> "}),
    ],
)
def test_cfg_to_text(grammar, expected):
    cfg = cfpq_data.cfg_from_text(grammar)

    actual = set(cfpq_data.cfg_to_text(cfg).splitlines())

    assert actual == expected


@pytest.mark.parametrize(
    "grammar",
    [
        grammar_1,
        grammar_2,
    ],
)
def test_cfg_from_and_to_txt(grammar):
    (fd, fname) = tempfile.mkstemp()

    cfg_1 = cfpq_data.cfg_from_text(grammar)

    path = cfpq_data.cfg_to_txt(cfg_1, fname)

    cfg_2 = cfpq_data.cfg_from_txt(path)

    os.close(fd)
    os.unlink(fname)

    assert set(cfpq_data.cfg_to_text(cfg_1).splitlines()) == set(
        cfpq_data.cfg_to_text(cfg_2).splitlines()
    )
