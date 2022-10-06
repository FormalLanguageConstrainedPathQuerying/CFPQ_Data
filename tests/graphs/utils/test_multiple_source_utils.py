import pytest

import os
import pathlib

import cfpq_data

seed = 42

g1 = cfpq_data.labeled_two_cycles_graph(42, 29)
g2 = cfpq_data.labeled_cycle_graph(42)


@pytest.mark.parametrize(
    "graph",
    [
        g1,
        g2,
    ],
)
@pytest.mark.parametrize(
    "set_size",
    [
        10,
        20,
        30,
    ],
)
def test_generate_multiple_source(graph, set_size):
    actual = cfpq_data.generate_multiple_source(graph, set_size, seed=seed)

    assert len(actual) == set_size

    expected = cfpq_data.generate_multiple_source(graph, set_size, seed=seed)

    assert actual == expected


@pytest.mark.parametrize(
    "incorrect_set_size",
    [
        -1,
        g1.number_of_nodes() + 1,
    ],
)
def test_multiple_source_set_size(incorrect_set_size):
    with pytest.raises(ValueError):
        cfpq_data.generate_multiple_source(g1, incorrect_set_size, seed=seed)


@pytest.mark.parametrize(
    "graph",
    [
        g1,
        g2,
    ],
)
@pytest.mark.parametrize(
    "percent",
    [
        1.0,
        10.0,
        99.9,
    ],
)
def test_generate_multiple_source_percent(graph, percent):
    actual = cfpq_data.generate_multiple_source_percent(graph, percent, seed=seed)

    assert len(actual) == int(percent * graph.number_of_nodes() / 100.0)

    expected = cfpq_data.generate_multiple_source_percent(graph, percent, seed=seed)

    assert actual == expected


@pytest.mark.parametrize(
    "incorrect_percent",
    [
        -1.0,
        101.0,
    ],
)
def test_multiple_source_percent_bounds(incorrect_percent):
    with pytest.raises(ValueError):
        cfpq_data.generate_multiple_source_percent(g1, incorrect_percent, seed=seed)


@pytest.mark.parametrize(
    "graph",
    [
        g1,
        g2,
    ],
)
@pytest.mark.parametrize(
    "percent",
    [
        1.0,
        10.0,
        99.9,
    ],
)
def test_multiple_source_txt(graph, percent):
    source_vertices_expected = cfpq_data.generate_multiple_source_percent(
        graph, percent, seed=seed
    )
    path = cfpq_data.multiple_source_to_txt(source_vertices_expected, "test.txt")
    source_vertices_actual = cfpq_data.multiple_source_from_txt(path)

    os.remove("test.txt")

    assert source_vertices_actual == source_vertices_expected


@pytest.mark.parametrize(
    "incorrect_line",
    [
        "1.5\n",
        "1 2 3\n",
        "abc\n",
    ],
)
def test_multiple_source_txt_format(incorrect_line):
    with open("test.txt", "w") as f:
        f.write(incorrect_line)
        dest = pathlib.Path("test.txt").resolve()

    with pytest.raises(ValueError):
        cfpq_data.multiple_source_from_txt(dest)

    os.remove("test.txt")


@pytest.mark.parametrize(
    "reachable_pairs",
    [
        set(),
        {(1, 1), (1, 3), (2, 2), (3, 1)},
    ],
)
def test_multiple_source_result_txt(reachable_pairs):
    path = cfpq_data.multiple_source_result_to_txt(reachable_pairs, "test.txt")
    reachable_pairs_actual = cfpq_data.multiple_source_result_from_txt(path)

    os.remove("test.txt")

    assert reachable_pairs_actual == reachable_pairs


@pytest.mark.parametrize(
    "incorrect_line",
    [
        "1\n",
        "1 2 3\n",
        "1 abc\n",
    ],
)
def test_multiple_source_result_txt_format(incorrect_line):
    with open("test.txt", "w") as f:
        f.write(incorrect_line)
        dest = pathlib.Path("test.txt").resolve()

    with pytest.raises(ValueError):
        cfpq_data.multiple_source_result_from_txt(dest)

    os.remove("test.txt")
