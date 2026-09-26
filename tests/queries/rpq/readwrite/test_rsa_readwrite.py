import pytest

import cfpq_data

grammar_1 = "S -> a b"
grammar_2 = "S -> a"
grammar_3 = "S -> a\nS -> b"
grammar_4 = "S -> \n#comment"

transition_system_1 = "start: S\n[box S]\nstart: 0\nfinal: 2\n0 --a--> 1\n1 --b--> 2"
transition_system_2 = (
    "start: S\n"
    "[box S]\n"
    "start: 0\n"
    "final: 3\n"
    "0 --a--> 1\n"
    "1 --S--> 2\n"
    "2 --b--> 3\n"
    "1 --b--> 3"
)
transition_system_3 = (
    "start: B\n[box S]\nstart: 0\nfinal: 0\n[box B]\nstart: 0\nfinal: 1\n0 --x--> 1"
)


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, ["ab"]),
        (grammar_2, ["a"]),
        (grammar_3, ["a", "b"]),
        (grammar_4, [""]),
    ],
)
def test_rsa_from_text(grammar, expected):
    rsa = cfpq_data.rsa_from_text(grammar)
    cfg_from_rsa = cfpq_data.cfg_from_rsa(rsa)

    for word in expected:
        if word is not None:
            assert cfg_from_rsa.contains(word)


@pytest.mark.parametrize(
    "grammar, expected",
    [
        (grammar_1, {"S -> ($.(a.b))"}),
        (grammar_2, {"S -> ($.a)"}),
        (grammar_3, {"S -> ($.(a|b))", "S -> ($.(b|a))"}),
        (grammar_4, {"S -> $"}),
    ],
)
def test_rsa_to_text(grammar, expected):
    rsa = cfpq_data.rsa_from_text(grammar)

    actual = set(cfpq_data.rsa_to_text(rsa).splitlines())

    assert actual.issubset(expected)


@pytest.mark.parametrize(
    "text, expected",
    [
        (transition_system_1, ["ab"]),
        (transition_system_2, ["ab", "aabb"]),
        (transition_system_3, ["x"]),
    ],
)
def test_rsa_from_text_transition_system(text, expected):
    rsa = cfpq_data.rsa_from_text(text)
    cfg = cfpq_data.cfg_from_rsa(rsa)

    for word in expected:
        assert cfg.contains(word)


@pytest.mark.parametrize(
    "text, rejected",
    [
        (transition_system_1, ["a", "b", "aba"]),
        (transition_system_2, ["aab", "abab", ""]),
        (transition_system_3, ["", "xx"]),
    ],
)
def test_rsa_from_text_transition_system_rejects(text, rejected):
    rsa = cfpq_data.rsa_from_text(text)
    cfg = cfpq_data.cfg_from_rsa(rsa)

    for word in rejected:
        assert not cfg.contains(word)


@pytest.mark.parametrize(
    "text",
    [
        transition_system_1,
        transition_system_2,
        transition_system_3,
    ],
)
def test_rsa_to_text_transition_system_round_trip(text):
    rsa = cfpq_data.rsa_from_text(text)
    canonical = cfpq_data.rsa_to_text(rsa)

    assert cfpq_data.rsa_from_text(canonical) == rsa


@pytest.mark.parametrize(
    "text",
    [
        "[box S]\nstart: 0\nfinal: 0\n[box S]\nstart: 1\nfinal: 1",
        "[box S]\nfinal: 1\n0 --a--> 1",
        "[box S]\nstart: 0\nfinal: 1\n0 --a--> 1\n0 --a--> 2",
        "start: X\n[box S]\nstart: 0\nfinal: 0",
        "garbage\n[box S]\nstart: 0\nfinal: 0",
    ],
)
def test_rsa_from_text_transition_system_errors(text):
    with pytest.raises(ValueError):
        cfpq_data.rsa_from_text(text)


def test_rsa_from_text_start_header():
    rsa = cfpq_data.rsa_from_text("start: B\nB -> x")

    assert rsa.initial_label.value == "B"
