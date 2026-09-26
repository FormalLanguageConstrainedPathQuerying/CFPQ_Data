import networkx as nx
import pytest

from flpq_data.graphs.readwrite.mtx import (
    filename_to_label,
    graph_from_mtx_dir,
    graph_to_mtx_dir,
    label_to_filename,
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
