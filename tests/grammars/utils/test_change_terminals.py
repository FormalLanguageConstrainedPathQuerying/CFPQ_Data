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

regex_1 = cfpq_data.regex_from_text("(abc|(d)*)")
exp_regex_1 = cfpq_data.regex_from_text("(bcc|(d)*)")

regex_2 = cfpq_data.regex_from_text("(a (bc|(d)*))")
exp_regex_2 = cfpq_data.regex_from_text("(b (cc|(d)*))")

rsa_1 = cfpq_data.rsa_from_text("S -> a b\n")
exp_rsa_1 = cfpq_data.rsa_from_text("S -> b c\n")

rsa_2 = cfpq_data.rsa_from_text("S -> b a\n")
exp_rsa_2 = cfpq_data.rsa_from_text("S -> c b\n")


@pytest.mark.parametrize(
    "cfg, exp_cfg",
    [
        (cfg_1, exp_cfg_1),
        (cfg_2, exp_cfg_2),
    ],
)
def test_change_terminals_in_cfg(cfg, exp_cfg):
    act_cfg = cfpq_data.change_terminals_in_cfg(cfg, {"a": "b", "b": "c"})
    assert set(cfpq_data.cfg_to_text(exp_cfg).split("\n")) == set(
        cfpq_data.cfg_to_text(act_cfg).split("\n")
    )


@pytest.mark.parametrize(
    "cnf, exp_cnf",
    [
        (cnf_1, exp_cnf_1),
        (cnf_2, exp_cnf_2),
    ],
)
def test_change_terminals_in_cnf(cnf, exp_cnf):
    act_cnf = cfpq_data.change_terminals_in_cnf(cnf, {"a": "b", "b": "c"})
    assert set(cfpq_data.cfg_to_text(exp_cnf).split("\n")) == set(
        cfpq_data.cfg_to_text(act_cnf).split("\n")
    )


@pytest.mark.parametrize(
    "regex, exp_regex",
    [
        (regex_1, exp_regex_1),
        (regex_2, exp_regex_2),
    ],
)
def test_change_terminals_in_reg(regex, exp_regex):
    act_regex = cfpq_data.change_terminals_in_regex(regex, {"a": "b", "b": "c"})
    assert cfpq_data.regex_to_text(exp_regex) == cfpq_data.regex_to_text(act_regex)


@pytest.mark.parametrize(
    "rsa, exp_rsa",
    [
        (rsa_1, exp_rsa_1),
        (rsa_2, exp_rsa_2),
    ],
)
def test_change_terminals_in_rsa(rsa, exp_rsa):
    act_rsa = cfpq_data.change_terminals_in_rsa(rsa, {"a": "b", "b": "c"})
    assert set(cfpq_data.rsa_to_text(exp_rsa).split("\n")) == set(
        cfpq_data.rsa_to_text(act_rsa).split("\n")
    )
