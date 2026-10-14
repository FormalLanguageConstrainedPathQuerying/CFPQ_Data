import networkx as nx
import pytest

import flpq_data
from flpq_data.graphs.converters import convert_graph


def _graph() -> nx.MultiDiGraph:
    # Multi-label with an indexed label. No duplicate (u, label, v) triples:
    # RDF is a set of triples and cannot represent parallel edges.
    g = nx.MultiDiGraph()
    for u, label, v in [(0, "a", 1), (1, "a", 2), (2, "b_5", 0)]:
        g.add_edge(u, v, label=label)
    return g


def _multi_graph() -> nx.MultiDiGraph:
    g = _graph()
    g.add_edge(0, 1, label="a")
    return g


def _norm(edges):
    return sorted((str(u), label, str(v)) for u, label, v in edges)


def _materialize_source(tmp_path, src_format: str, g: nx.MultiDiGraph):
    if src_format == "graph":
        return g
    if src_format == "mtx":
        path = tmp_path / "src_mtx"
        flpq_data.graph_to_mtx_dir(g, path)
        return path
    if src_format == "txt":
        path = tmp_path / "src.txt"
        flpq_data.graph_to_txt(g, path)
        return path
    path = tmp_path / "src.ttl"
    flpq_data.graph_to_rdf(g, path)
    return path


def _read_back(dst, dst_format: str):
    if dst_format == "mtx":
        return list(flpq_data.iter_edges_from_mtx_dir(dst))
    if dst_format == "txt":
        return list(flpq_data.iter_edges_from_txt(dst))
    return list(flpq_data.iter_edges_from_rdf(dst))


@pytest.mark.parametrize("src_format", ["mtx", "txt", "rdf", "graph"])
@pytest.mark.parametrize("dst_format", ["mtx", "txt", "rdf", "g"])
def test_convert_round_trip(tmp_path, src_format, dst_format):
    g = _graph()
    src = _materialize_source(tmp_path, src_format, g)

    if dst_format == "mtx":
        dst = tmp_path / f"dst_{src_format}_mtx"
    elif dst_format == "g":
        dst = tmp_path / f"dst_{src_format}.g"
    elif dst_format == "rdf":
        dst = tmp_path / f"dst_{src_format}.ttl"
    else:
        dst = tmp_path / f"dst_{src_format}.{dst_format}"

    convert_graph(src, dst, src_format=src_format, dst_format=dst_format)

    if dst_format == "g":
        # g is write-only: cross-check against the independent text path.
        # Line order follows the source (an RDF source yields store order).
        ref = tmp_path / "ref"
        flpq_data.graph_to_mtx_dir(g, ref)
        expected = flpq_data.graph_dir_to_g_text(ref).splitlines()
        assert sorted(dst.read_text().splitlines()) == sorted(expected)
        return

    assert _norm(_read_back(dst, dst_format)) == _norm(
        flpq_data.iter_edges_from_graph(g)
    )


@pytest.mark.parametrize("src_format", ["mtx", "txt", "graph"])
@pytest.mark.parametrize("dst_format", ["mtx", "txt", "g"])
def test_convert_preserves_parallel_edges(tmp_path, src_format, dst_format):
    # Parallel edges survive every format except RDF (a set of triples).
    g = _multi_graph()
    src = _materialize_source(tmp_path, src_format, g)

    if dst_format == "mtx":
        dst = tmp_path / f"dst_{src_format}_mtx"
    elif dst_format == "g":
        dst = tmp_path / f"dst_{src_format}.g"
    else:
        dst = tmp_path / f"dst_{src_format}.{dst_format}"

    convert_graph(src, dst, src_format=src_format, dst_format=dst_format)

    if dst_format == "g":
        ref = tmp_path / "ref"
        flpq_data.graph_to_mtx_dir(g, ref)
        assert dst.read_text() == flpq_data.graph_dir_to_g_text(ref)
        return

    got = _read_back(dst, dst_format)
    assert len(got) == g.number_of_edges()
    assert _norm(got) == _norm(flpq_data.iter_edges_from_graph(g))


def test_convert_writer_options(tmp_path):
    g = _graph()
    src = tmp_path / "src"
    flpq_data.graph_to_mtx_dir(g, src)
    dst = tmp_path / "dst.txt"

    convert_graph(src, dst, src_format="mtx", dst_format="txt", quoting=True)

    assert dst.read_text().splitlines()[0] == "'0' 'a' '1'"


def test_convert_unknown_src_format(tmp_path):
    with pytest.raises(ValueError, match="Unknown src_format"):
        convert_graph("x", tmp_path / "y", src_format="csv", dst_format="txt")


def test_convert_unknown_dst_format(tmp_path):
    with pytest.raises(ValueError, match="Unknown dst_format"):
        convert_graph("x", tmp_path / "y", src_format="mtx", dst_format="csv")


def test_convert_g_is_write_only(tmp_path):
    with pytest.raises(ValueError, match="not a readable format"):
        convert_graph(
            tmp_path / "g.g", tmp_path / "o.txt", src_format="g", dst_format="txt"
        )


def test_convert_graph_is_read_only(tmp_path):
    with pytest.raises(ValueError, match="not a writable format"):
        convert_graph(_graph(), tmp_path / "o", src_format="graph", dst_format="graph")
