import pytest

import cfpq_data

cfg_1 = cfpq_data.cfg_from_text("S -> a S b | a b")
cfg_2 = cfpq_data.cfg_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")

cnf_1 = cfpq_data.cnf_from_text("S -> a S b | a b")
cnf_2 = cfpq_data.cnf_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")


@pytest.mark.parametrize("cfg", [cfg_1, cfg_2])
def test_rsa_from_cfg(cfg):
    rsa = cfpq_data.rsa_from_cfg(cfg)
    cfg_from_rsa = cfpq_data.cfg_from_rsa(rsa)
    for word in cfg.get_words(4):
        assert cfg_from_rsa.contains(word) and cfg.contains(word)


@pytest.mark.parametrize("cnf", [cnf_1, cnf_2])
def test_rsa_from_cnf(cnf):
    rsa = cfpq_data.rsa_from_cnf(cnf)
    cfg_from_rsa = cfpq_data.cfg_from_rsa(rsa)
    for word in cnf.get_words(4):
        assert cfg_from_rsa.contains(word) and cnf.contains(word)
