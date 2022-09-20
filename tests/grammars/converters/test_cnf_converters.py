import pytest

import cfpq_data

cfg_1 = cfpq_data.cfg_from_text("S -> a S b | a b")
cfg_2 = cfpq_data.cfg_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")

regex_1 = cfpq_data.regex_from_text("a*")
regex_2 = cfpq_data.regex_from_text("a (bc|d*)")

rsa_1 = cfpq_data.rsa_from_text("S -> a S b | a b")
rsa_2 = cfpq_data.rsa_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")


@pytest.mark.parametrize("cfg", [cfg_1, cfg_2])
def test_cnf_from_cfg(cfg):
    cnf = cfpq_data.cnf_from_cfg(cfg)
    for word in cnf.get_words(4):
        assert cnf.contains(word) and cfg.contains(word)


@pytest.mark.parametrize("regex", [regex_1, regex_2])
def test_cnf_from_regex(regex):
    cnf = cfpq_data.cnf_from_regex(regex)
    for word in cnf.get_words(4):
        regex_word = map(lambda x: x.value, word)
        assert cnf.contains(word) and regex.accepts(regex_word)


@pytest.mark.parametrize("rsa", [rsa_1, rsa_2])
def test_cnf_from_rsa(rsa):
    cnf = cfpq_data.cnf_from_rsa(rsa)
    cfg = cfpq_data.cfg_from_rsa(rsa)
    for word in cnf.get_words(4):
        assert cnf.contains(word) and cfg.contains(word)
