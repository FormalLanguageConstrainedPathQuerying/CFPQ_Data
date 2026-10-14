import flpq_data
from flpq_data.graphs.utils.to_g_text import g_text_from_edges, graph_dir_to_g_text


def _mtx_dir(tmp_path):
    d = tmp_path / "graph"
    d.mkdir()
    (d / "a.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n3 3 1\n0 1\n"
    )
    (d / "b_5.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        "%%GraphBLAS type bool\n3 3 1\n2 0\n"
    )
    return d


def test_g_text_from_edges(tmp_path):
    p = tmp_path / "g.g"
    g_text_from_edges([(0, "a", 1)], p)

    assert p.read_text() == "0 1 a\n1 0 a_r\n"


def test_g_text_from_edges_indexed(tmp_path):
    p = tmp_path / "g.g"
    g_text_from_edges([(2, "b_5", 0)], p)

    assert p.read_text() == "2 0 b_i 5\n0 2 b_r_i 5\n"


def test_g_text_matches_dir_text(tmp_path):
    # The file writer and the text generator agree on the same input.
    d = _mtx_dir(tmp_path)
    p = tmp_path / "g.g"
    g_text_from_edges(flpq_data.iter_edges_from_mtx_dir(d), p)

    assert p.read_text() == graph_dir_to_g_text(d)


def test_graph_dir_to_g_text_empty(tmp_path):
    d = tmp_path / "graph"
    d.mkdir()

    assert graph_dir_to_g_text(d) == ""
