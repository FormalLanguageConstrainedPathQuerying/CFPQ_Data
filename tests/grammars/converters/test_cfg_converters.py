import pytest

import cfpq_data

cnf_1 = cfpq_data.cnf_from_text("S -> a S b | a b")
cnf_2 = cfpq_data.cnf_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")

rsm_1 = cfpq_data.rsm_from_text("S -> a S b | a b")
rsm_2 = cfpq_data.rsm_from_text("S -> sco_r S sco | t_r S t | sco_r sco | t_r t")


@pytest.mark.parametrize("cnf", [cnf_1, cnf_2])
def test_cfg_from_cnf(cnf):
    cfg = cfpq_data.cfg_from_cnf(cnf)
    for word in cfg.get_words(4):
        assert cfg.contains(word) and cnf.contains(word)


@pytest.mark.parametrize("rsm", [rsm_1, rsm_2])
def test_cfg_from_rsm(rsm):
    cfg = cfpq_data.cfg_from_rsm(rsm)
    for word in cfg.get_words(4):
        assert cfg.contains(word) and rsm.contains(word)
