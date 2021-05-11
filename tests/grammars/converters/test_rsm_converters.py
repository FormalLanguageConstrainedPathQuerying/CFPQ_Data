import pytest

import cfpq_data

cfg_1 = cfpq_data.cfg_from_text("S -> a S b | a b")
cfg_2 = cfpq_data.cfg_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")

cnf_1 = cfpq_data.cnf_from_text("S -> a S b | a b")
cnf_2 = cfpq_data.cnf_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")


@pytest.mark.parametrize("cfg", [cfg_1, cfg_2])
def test_rsm_from_cfg(cfg):
    rsm = cfpq_data.rsm_from_cfg(cfg)
    for word in cfg.get_words(4):
        assert rsm.contains(word) and cfg.contains(word)


@pytest.mark.parametrize("cnf", [cnf_1, cnf_2])
def test_rsm_from_cnf(cnf):
    rsm = cfpq_data.rsm_from_cnf(cnf)
    for word in cnf.get_words(4):
        assert rsm.contains(word) and cnf.contains(word)
