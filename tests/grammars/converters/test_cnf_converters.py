import pytest

import cfpq_data

cfg_1 = cfpq_data.cfg_from_text("S -> a S b | a b")
cfg_2 = cfpq_data.cfg_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")

rsm_1 = cfpq_data.rsm_from_text("S -> a S b | a b")
rsm_2 = cfpq_data.rsm_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")


@pytest.mark.parametrize("cfg", [cfg_1, cfg_2])
def test_cnf_from_cfg(cfg):
    cnf = cfpq_data.cnf_from_cfg(cfg)
    for word in cnf.get_words(4):
        assert cnf.contains(word) and cfg.contains(word)


@pytest.mark.parametrize("rsm", [rsm_1, rsm_2])
def test_cnf_from_rsm(rsm):
    cnf = cfpq_data.cnf_from_rsm(rsm)
    for word in cnf.get_words(4):
        assert cnf.contains(word) and rsm.contains(word)
