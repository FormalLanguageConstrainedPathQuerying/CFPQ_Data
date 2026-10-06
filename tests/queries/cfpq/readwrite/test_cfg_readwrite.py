import os
import tempfile

import pytest

import flpq_data

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
    cfg = flpq_data.cfg_from_text(grammar)

    assert flpq_data.cfg_to_text(cfg) == expected


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, {"S -> a S b S", "S -> "}),
        (grammar_2, {"S -> a S", "S -> "}),
    ],
)
def test_cfg_to_text(grammar, expected):
    cfg = flpq_data.cfg_from_text(grammar)

    actual = set(flpq_data.cfg_to_text(cfg).splitlines())

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

    cfg_1 = flpq_data.cfg_from_text(grammar)

    path = flpq_data.cfg_to_txt(cfg_1, fname)

    cfg_2 = flpq_data.cfg_from_txt(path)

    os.close(fd)
    os.unlink(fname)

    assert set(flpq_data.cfg_to_text(cfg_1).splitlines()) == set(
        flpq_data.cfg_to_text(cfg_2).splitlines()
    )
