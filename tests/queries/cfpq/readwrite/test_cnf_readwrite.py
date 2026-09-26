import os
import tempfile

import pytest

import cfpq_data

grammar_1 = "\n".join(["S -> A B", "A -> a", "B -> b", "S -> epsilon"])
grammar_2 = "\n".join(["S -> A S", "A -> A A", "A -> a", "S -> epsilon"])


@pytest.mark.parametrize(
    "grammar",
    [
        grammar_1,
        grammar_2,
    ],
)
def test_cnf_from_and_to_txt(grammar):
    (fd, fname) = tempfile.mkstemp()

    cnf_1 = cfpq_data.cnf_from_text(grammar)

    path = cfpq_data.cfg_to_txt(cnf_1, fname)

    cnf_2 = cfpq_data.cnf_from_txt(path)

    os.close(fd)
    os.unlink(fname)

    assert set(cfpq_data.cfg_to_text(cnf_1).splitlines()) == set(
        cfpq_data.cfg_to_text(cnf_2).splitlines()
    )
