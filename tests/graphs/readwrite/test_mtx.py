import inspect

import networkx as nx
import pytest

from flpq_data.graphs.readwrite.mtx import (
    filename_to_label,
    graph_from_mtx_dir,
    graph_to_mtx_dir,
    iter_edges_from_mtx_dir,
    label_to_filename,
    mtx_dir_from_edges,
)


@pytest.mark.parametrize(
    "filename,label",
    [
        ("type.mtx", "type"),
        ("alloc_r.mtx", "alloc_r"),
        ("load_5.mtx", "load_5"),
        ("load_i_5.mtx", "load_i_5"),
        ("load_r_i_5.mtx", "load_r_i_5"),
        ("a_i_b.mtx", "a_i_b"),
    ],
)
def test_filename_to_label(filename, label):
    assert filename_to_label(filename) == label


@pytest.mark.parametrize(
    "label,filename",
    [
        ("type", "type.mtx"),
        ("load_5", "load_5.mtx"),
        ("alloc_r", "alloc_r.mtx"),
    ],
)
def test_label_to_filename(label, filename):
    assert label_to_filename(label) == filename
    assert filename_to_label(filename) == label


def _small_graph() -> nx.MultiDiGraph:
    g = nx.MultiDiGraph()
    g.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "a"}),
            (2, 0, {"label": "b_5"}),
            (0, 1, {"label": "a"}),
        ]
    )
    return g


def test_mtx_round_trip(tmp_path):
    g = _small_graph()
    path = graph_to_mtx_dir(g, tmp_path / "graph")

    assert sorted(p.name for p in path.glob("*.mtx")) == ["a.mtx", "b_5.mtx"]

    g2 = graph_from_mtx_dir(path)
    assert sorted((u, v, e["label"]) for u, v, e in g2.edges(data=True)) == sorted(
        (u, v, e["label"]) for u, v, e in g.edges(data=True)
    )


def test_mtx_header_and_pairs(tmp_path):
    graph_to_mtx_dir(_small_graph(), tmp_path / "graph")

    text = (tmp_path / "graph" / "a.mtx").read_text()
    lines = text.splitlines()
    assert lines[0] == "%%MatrixMarket matrix coordinate pattern general"
    assert lines[1] == "%%GraphBLAS type bool"
    assert lines[2] == "3 3 3"
    assert lines[3:] == ["0 1", "0 1", "1 2"]


def test_mtx_reads_file_name_as_literal_label(tmp_path):
    (tmp_path / "load_i_5.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n"
        "3 3 1\n"
        "0 2\n"
    )

    g = graph_from_mtx_dir(tmp_path)
    assert list(g.edges(data=True)) == [(0, 2, {"label": "load_i_5"})]


def test_mtx_rejects_bad_header(tmp_path):
    (tmp_path / "a.mtx").write_text("%%MatrixMarket matrix coordinate real\n1 1 0\n")

    with pytest.raises(ValueError, match="Unexpected header"):
        graph_from_mtx_dir(tmp_path)


def test_mtx_rejects_bad_nnz(tmp_path):
    (tmp_path / "a.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n"
        "3 3 2\n"
        "0 1\n"
    )

    with pytest.raises(ValueError, match="declares 2 entries but has 1"):
        graph_from_mtx_dir(tmp_path)


def test_mtx_rejects_non_integer_nodes(tmp_path):
    g = nx.MultiDiGraph()
    g.add_edge("x", "y", label="a")

    with pytest.raises(TypeError, match="non-negative integers"):
        graph_to_mtx_dir(g, tmp_path / "graph")


def _write_two_label_dir(path):
    (path / "a.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n3 3 2\n0 1\n1 2\n"
    )
    (path / "b_5.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n3 3 1\n2 0\n"
    )


def test_iter_edges_from_mtx_dir(tmp_path):
    _write_two_label_dir(tmp_path)

    assert list(iter_edges_from_mtx_dir(tmp_path)) == [
        (0, "a", 1),
        (1, "a", 2),
        (2, "b_5", 0),
    ]


def test_iter_edges_from_mtx_dir_is_lazy(tmp_path):
    _write_two_label_dir(tmp_path)

    edges = iter_edges_from_mtx_dir(tmp_path)
    assert inspect.isgenerator(edges)
    assert next(edges) == (0, "a", 1)


def test_iter_edges_from_mtx_dir_rejects_bad_header(tmp_path):
    (tmp_path / "a.mtx").write_text("%%MatrixMarket matrix coordinate real\n1 1 0\n")

    with pytest.raises(ValueError, match="Unexpected header"):
        list(iter_edges_from_mtx_dir(tmp_path))


def test_iter_edges_from_mtx_dir_rejects_bad_nnz(tmp_path):
    (tmp_path / "a.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n3 3 2\n0 1\n"
    )

    with pytest.raises(ValueError, match="declares 2 entries but has 1"):
        list(iter_edges_from_mtx_dir(tmp_path))


def test_mtx_dir_from_edges(tmp_path):
    d = mtx_dir_from_edges(
        [(0, "a", 1), (1, "a", 2), (2, "b_5", 0)], tmp_path / "graph"
    )

    assert sorted(p.name for p in d.glob("*.mtx")) == ["a.mtx", "b_5.mtx"]
    assert not list(d.glob("*.tmp"))

    lines = (d / "a.mtx").read_text().splitlines()
    assert lines[:3] == [
        "%%MatrixMarket matrix coordinate pattern general",
        "%%GraphBLAS type bool",
        "3 3 2",
    ]
    assert lines[3:] == ["0 1", "1 2"]


def test_mtx_dir_from_edges_interleaved_labels(tmp_path):
    # The labels interleave arbitrarily: the writer must reopen closed temp
    # files (at most one is open at a time, so the label count is unbounded).
    edges = [(i, f"l{i % 300}", i + 1) for i in range(600)]
    d = mtx_dir_from_edges(edges, tmp_path / "graph")

    files = list(d.glob("*.mtx"))
    assert len(files) == 300
    total = 0
    for p in files:
        lines = p.read_text().splitlines()
        nnz = int(lines[2].split()[2])
        assert len(lines) - 3 == nnz
        total += nnz
    assert total == 600


def test_mtx_dir_from_edges_dimension(tmp_path):
    # An explicit dimension preserves isolated nodes that carry no edges.
    d = mtx_dir_from_edges([(0, "a", 1)], tmp_path / "graph", dimension=5)

    assert (d / "a.mtx").read_text().splitlines()[2] == "5 5 1"


def test_mtx_dir_from_edges_rejects_small_dimension(tmp_path):
    with pytest.raises(ValueError, match="smaller than the largest node index"):
        mtx_dir_from_edges([(0, "a", 4)], tmp_path / "graph", dimension=3)

    assert not list((tmp_path / "graph").glob("*.tmp"))


def test_mtx_dir_from_edges_digit_strings(tmp_path):
    d = mtx_dir_from_edges([("0", "a", "1")], tmp_path / "graph")

    assert (d / "a.mtx").read_text().splitlines()[3:] == ["0 1"]


def test_mtx_dir_from_edges_rejects_non_integer_nodes(tmp_path):
    with pytest.raises(TypeError, match="non-negative integers"):
        mtx_dir_from_edges([(0, "a", 1), ("x", "a", 2)], tmp_path / "graph")

    assert not list((tmp_path / "graph").glob("*.tmp"))


def test_mtx_dir_from_edges_empty(tmp_path):
    d = mtx_dir_from_edges([], tmp_path / "graph")

    assert not list(d.glob("*"))
