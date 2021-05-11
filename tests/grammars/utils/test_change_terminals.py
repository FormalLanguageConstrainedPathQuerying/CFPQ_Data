import pytest

import cfpq_data

cfg_1 = cfpq_data.cfg_from_text("S -> a S b S\nS -> a b\n")
exp_cfg_1 = cfpq_data.cfg_from_text("S -> b S c S\nS -> b c\n")

cfg_2 = cfpq_data.cfg_from_text("S -> a b c d\n")
exp_cfg_2 = cfpq_data.cfg_from_text("S -> b c c d\n")

cnf_1 = cfpq_data.cnf_from_text("S -> a")
exp_cnf_1 = cfpq_data.cnf_from_text("S -> b")

cnf_2 = cfpq_data.cnf_from_text("S -> b")
exp_cnf_2 = cfpq_data.cnf_from_text("S -> c")

rsm_1 = cfpq_data.rsm_from_text("S -> a b\n")
exp_rsm_1 = cfpq_data.rsm_from_text("S -> b c\n")

rsm_2 = cfpq_data.rsm_from_text("S -> b a\n")
exp_rsm_2 = cfpq_data.rsm_from_text("S -> c b\n")


@pytest.mark.parametrize(
    "cfg, exp_cfg",
    [
        (cfg_1, exp_cfg_1),
        (cfg_2, exp_cfg_2),
    ],
)
def test_change_terminals_in_cfg(cfg, exp_cfg):
    act_cfg = cfpq_data.change_terminals_in_cfg(cfg, {"a": "b", "b": "c"})
    assert set(exp_cfg.to_text().split("\n")) == set(act_cfg.to_text().split("\n"))


@pytest.mark.parametrize(
    "cnf, exp_cnf",
    [
        (cnf_1, exp_cnf_1),
        (cnf_2, exp_cnf_2),
    ],
)
def test_change_terminals_in_cnf(cnf, exp_cnf):
    act_cnf = cfpq_data.change_terminals_in_cnf(cnf, {"a": "b", "b": "c"})
    assert set(exp_cnf.to_text().split("\n")) == set(act_cnf.to_text().split("\n"))


@pytest.mark.parametrize(
    "rsm, exp_rsm",
    [
        (rsm_1, exp_rsm_1),
        (rsm_2, exp_rsm_2),
    ],
)
def test_change_terminals_in_rsm(rsm, exp_rsm):
    act_rsm = cfpq_data.change_terminals_in_rsm(rsm, {"a": "b", "b": "c"})
    assert set(exp_rsm.to_text().split("\n")) == set(act_rsm.to_text().split("\n"))
