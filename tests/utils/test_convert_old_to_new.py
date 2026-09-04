import pathlib
import random
from collections import Counter

import pytest

from convert_old_to_new import (
    MTX_BANNER,
    MTX_TYPE,
    GraphStats,
    convert_csv_to_graph_dir,
    iter_edges,
    scan_csv,
    validate_labels,
)


def write_csv(path: pathlib.Path, lines) -> pathlib.Path:
    path.write_text("\r\n".join(lines) + "\r\n")
    return path


def parse_mtx(path: pathlib.Path):
    """Parse an MTX file produced by the converter into (header, entries)."""
    with open(path, "r") as f:
        lines = f.read().splitlines()
    assert lines[0] == MTX_BANNER
    assert lines[1] == MTX_TYPE
    rows, cols, nnz = (int(x) for x in lines[2].split())
    entries = [(int(a), int(b)) for a, b in (line.split() for line in lines[3:])]
    return (rows, cols, nnz), entries


def test_iter_edges_crlf_and_lf(tmp_path):
    crlf = write_csv(tmp_path / "crlf.csv", ["0 1 a", "2 3 b"])
    lf = tmp_path / "lf.csv"
    lf.write_text("0 1 a\n2 3 b\n")

    assert list(iter_edges(crlf)) == [(0, 1, "a"), (2, 3, "b")]
    assert list(iter_edges(lf)) == list(iter_edges(crlf))


def test_iter_edges_skips_blank_lines(tmp_path):
    csv = write_csv(tmp_path / "g.csv", ["0 1 a", "", "2 3 b"])
    assert list(iter_edges(csv)) == [(0, 1, "a"), (2, 3, "b")]


@pytest.mark.parametrize(
    "line",
    [
        "0 1",  # too few fields
        "0 1 a b",  # too many fields
        "x 1 a",  # non-integer from
        "0 y a",  # non-integer to
    ],
)
def test_iter_edges_malformed(tmp_path, line):
    csv = write_csv(tmp_path / "g.csv", [line])
    with pytest.raises(ValueError):
        list(iter_edges(csv))


def test_scan_csv_stats(tmp_path):
    csv = write_csv(
        tmp_path / "g.csv",
        ["0 1 a", "1 2 a", "2 0 b", "5 5 a"],
    )
    stats = scan_csv(csv)
    assert isinstance(stats, GraphStats)
    assert stats.num_nodes == 4  # {0, 1, 2, 5}
    assert stats.max_node_id == 5
    assert stats.total_edges == 4
    assert stats.edges_per_label == {"a": 3, "b": 1}


def test_convert_golden_readme_example(tmp_path):
    # The example graph from the new-format README:
    # (0) --[a]-> (1); (2) --[a]-> (1); (0) --[b]-> (2); (2) --[b]-> (3)
    csv = write_csv(
        tmp_path / "g.csv",
        ["0 1 a", "2 1 a", "0 2 b", "2 3 b"],
    )
    graph_dir = tmp_path / "graph"
    stats = convert_csv_to_graph_dir(csv, graph_dir)

    assert sorted(p.name for p in graph_dir.iterdir()) == ["a.mtx", "b.mtx"]
    assert stats.total_edges == 4
    assert stats.edges_per_label == {"a": 2, "b": 2}

    (rows, cols, nnz), entries = parse_mtx(graph_dir / "a.mtx")
    assert (rows, cols, nnz) == (4, 4, 2)
    assert entries == [(0, 1), (2, 1)]

    (rows, cols, nnz), entries = parse_mtx(graph_dir / "b.mtx")
    assert (rows, cols, nnz) == (4, 4, 2)
    assert entries == [(0, 2), (2, 3)]


def test_convert_roundtrip_property(tmp_path):
    rng = random.Random(42)
    edges = [
        (rng.randrange(50), rng.randrange(50), rng.choice(["a", "b_r", "c_x"]))
        for _ in range(2000)
    ]
    csv = tmp_path / "g.csv"
    csv.write_text("\n".join(f"{u} {v} {l}" for u, v, l in edges) + "\n")

    graph_dir = tmp_path / "graph"
    stats = convert_csv_to_graph_dir(csv, graph_dir)

    assert stats.total_edges == len(edges)
    assert Counter(stats.edges_per_label.values()) == Counter(
        Counter(l for _, _, l in edges).values()
    )

    restored = Counter()
    for label, nnz in stats.edges_per_label.items():
        (rows, cols, header_nnz), entries = parse_mtx(graph_dir / f"{label}.mtx")
        assert header_nnz == len(entries) == nnz
        assert rows == cols == stats.max_node_id + 1
        restored.update((u, v, label) for u, v in entries)

    assert restored == Counter(edges)


def test_convert_sparse_node_ids(tmp_path):
    csv = write_csv(tmp_path / "g.csv", ["0 5 a"])
    graph_dir = tmp_path / "graph"
    stats = convert_csv_to_graph_dir(csv, graph_dir)

    (rows, cols, nnz), entries = parse_mtx(graph_dir / "a.mtx")
    assert (rows, cols, nnz) == (6, 6, 1)
    assert entries == [(0, 5)]
    assert stats.num_nodes == 2


def test_convert_preserves_duplicate_edges(tmp_path):
    csv = write_csv(tmp_path / "g.csv", ["0 1 a", "0 1 a", "1 0 a"])
    graph_dir = tmp_path / "graph"
    convert_csv_to_graph_dir(csv, graph_dir)

    (_, _, nnz), entries = parse_mtx(graph_dir / "a.mtx")
    assert nnz == 3
    assert entries == [(0, 1), (0, 1), (1, 0)]


@pytest.mark.parametrize(
    "label",
    ["", "a/b", "a b", "-a", "a\x00b"],
)
def test_validate_labels_rejects_unsafe(label):
    with pytest.raises(ValueError):
        validate_labels([label])


def test_validate_labels_accepts_dataset_labels():
    validate_labels(
        {
            "a",
            "type_r",
            "subClassOf",
            "load_0",
            "store_857_r",
            "default-namespace",
            "created_by",
        }
    )
