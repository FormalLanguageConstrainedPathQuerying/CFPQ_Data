from typing import cast

import pytest
from pyformlang.cfg import Terminal

import flpq_data

cnf_1 = flpq_data.cnf_from_text("S -> a S b | a b")
cnf_2 = flpq_data.cnf_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")

regex_1 = flpq_data.regex_from_text("a*")
regex_2 = flpq_data.regex_from_text("a (bc|d*)")

rsa_1 = flpq_data.rsa_from_text("S -> a S b | a b")
rsa_2 = flpq_data.rsa_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")


@pytest.mark.parametrize("cnf", [cnf_1, cnf_2])
def test_cfg_from_cnf(cnf):
    cfg = flpq_data.cfg_from_cnf(cnf)
    for word in cfg.get_words(4):
        word = cast("list[Terminal]", word)
        assert cfg.contains(word) and cnf.contains(word)


@pytest.mark.parametrize("regex", [regex_1, regex_2])
def test_cfg_from_regex(regex):
    cfg = flpq_data.cfg_from_regex(regex)
    for word in cfg.get_words(4):
        word = cast("list[Terminal]", word)
        regex_word = map(lambda x: x.value, word)
        assert cfg.contains(word) and regex.accepts(regex_word)


@pytest.mark.parametrize("rsa", [rsa_1, rsa_2])
def test_cfg_from_rsa(rsa):
    cfg = flpq_data.cfg_from_rsa(rsa)
    cnf = flpq_data.cnf_from_rsa(rsa)
    for word in cfg.get_words(4):
        word = cast("list[Terminal]", word)
        assert cfg.contains(word) and cnf.contains(word)
