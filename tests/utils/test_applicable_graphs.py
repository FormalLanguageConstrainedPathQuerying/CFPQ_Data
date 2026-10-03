import pathlib

import applicable_graphs
from applicable_graphs import (
    BEGIN_MARKER,
    END_MARKER,
    render_class_region,
)
from reachable_pairs_tables import load_rows, replace_marked_region


def make_docs(tmp_path: pathlib.Path) -> pathlib.Path:
    """A minimal docs tree: one real category with two graphs."""
    docs = tmp_path / "docs"
    (docs / "graphs" / "data").mkdir(parents=True)
    (docs / "graphs" / "index.rst").write_text(
        ".. _graphs:\n\nGraphs\n******\n\n"
        ".. toctree::\n   :maxdepth: 1\n\n   c_alias_analysis\n"
    )
    (docs / "graphs" / "c_alias_analysis.rst").write_text(
        ".. _graphs_c_alias_analysis:\n\nC alias analysis\n****************\n\n"
        ".. toctree::\n   :hidden:\n\n   data/g1\n   data/g2\n"
    )
    for page, name in [("g1", "alpha"), ("g2", "beta")]:
        (docs / "graphs" / "data" / f"{page}.rst").write_text(
            f".. _{page}:\n\n{name}\n====\n\n"
            f"- `x.tar.gz <https://cfpq-data.storage.yandexcloud.net/"
            f"6.0.0/graph/{name}.tar.gz>`_\n"
        )
    return docs


def make_class_pages(docs: pathlib.Path) -> dict[str, pathlib.Path]:
    pages: dict[str, pathlib.Path] = {}
    for cls in ("cfpq", "rpq", "mcfpq"):
        page = docs / "queries" / cls / "index.rst"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            f".. _{cls}_queries:\n\n{cls.upper()}\n\n"
            f"{BEGIN_MARKER}\nold\n{END_MARKER}\n"
        )
        pages[cls] = page
    return pages


def make_csv(tmp_path: pathlib.Path) -> pathlib.Path:
    csv = tmp_path / "reachable_pairs.csv"
    csv.write_text(
        "graph,grammar,category,query_class,num_reachable_pairs\n"
        "alpha,c_alias.cnf,c_alias_analysis,cfpq,3\n"
        "beta,c_alias.cnf,c_alias_analysis,cfpq,4\n"
        "alpha,a.re,c_alias_analysis,rpq,\n",
        encoding="utf-8",
    )
    return csv


ROWS = [
    {
        "graph": "alpha",
        "grammar": "c_alias.cnf",
        "category": "c_alias_analysis",
        "query_class": "cfpq",
        "num_reachable_pairs": 3,
    },
    {
        "graph": "beta",
        "grammar": "c_alias.cnf",
        "category": "c_alias_analysis",
        "query_class": "cfpq",
        "num_reachable_pairs": 4,
    },
    {
        "graph": "alpha",
        "grammar": "a.re",
        "category": "c_alias_analysis",
        "query_class": "rpq",
        "num_reachable_pairs": None,
    },
]


def test_render_class_region_groups_and_links(tmp_path):
    region = render_class_region(ROWS, make_docs(tmp_path), "cfpq")
    assert "C alias analysis" in region
    # The ref target is the shared page stem, not the graph name.
    assert ":ref:`g1`" in region and ":ref:`g2`" in region
    assert "alpha" not in region and "beta" not in region


def test_render_class_region_empty_class(tmp_path):
    region = render_class_region(ROWS, make_docs(tmp_path), "mcfpq")
    assert region == "No MCFPQ queries have been added to the graph catalog yet."


def test_render_class_region_only_requested_class(tmp_path):
    region = render_class_region(ROWS, make_docs(tmp_path), "rpq")
    assert region.count(":ref:`g1`") == 1
    assert ":ref:`g2`" not in region


def test_replace_marked_region_round_trip():
    text = f"intro\n{BEGIN_MARKER}\nold\n{END_MARKER}\noutro\n"
    updated, changed = replace_marked_region(text, "new", BEGIN_MARKER, END_MARKER)
    assert changed
    assert updated.splitlines() == [
        "intro",
        BEGIN_MARKER,
        "",
        "new",
        "",
        END_MARKER,
        "outro",
    ]
    again, changed_again = replace_marked_region(
        updated, "new", BEGIN_MARKER, END_MARKER
    )
    assert not changed_again and again == updated


def test_main_check_update_check(tmp_path, monkeypatch, capsys):
    docs = make_docs(tmp_path)
    pages = make_class_pages(docs)
    csv = make_csv(tmp_path)
    monkeypatch.setattr(applicable_graphs, "DOCS_DIR", docs)
    monkeypatch.setattr(applicable_graphs, "CLASS_PAGES", pages)
    monkeypatch.setattr(applicable_graphs, "REACHABLE_PAIRS_CSV", csv)

    # out of sync -> exit 1
    assert applicable_graphs.main([]) == 1
    assert "out of sync" in capsys.readouterr().out

    # --update rewrites the regions
    assert applicable_graphs.main(["--update"]) == 0
    assert ":ref:`g1`" in pages["cfpq"].read_text(encoding="utf-8")
    assert ":ref:`g1`" in pages["rpq"].read_text(encoding="utf-8")
    assert "No MCFPQ queries" in pages["mcfpq"].read_text(encoding="utf-8")
    capsys.readouterr()

    # now in sync
    assert applicable_graphs.main([]) == 0
    assert "in sync" in capsys.readouterr().out


def test_main_missing_marker(tmp_path, monkeypatch, capsys):
    docs = make_docs(tmp_path)
    pages = make_class_pages(docs)
    pages["mcfpq"].write_text("no markers here\n", encoding="utf-8")
    monkeypatch.setattr(applicable_graphs, "DOCS_DIR", docs)
    monkeypatch.setattr(applicable_graphs, "CLASS_PAGES", pages)
    monkeypatch.setattr(applicable_graphs, "REACHABLE_PAIRS_CSV", make_csv(tmp_path))

    assert applicable_graphs.main([]) == 1
    assert "not found" in capsys.readouterr().out


def test_main_unknown_graph_is_reported(tmp_path, monkeypatch, capsys):
    docs = make_docs(tmp_path)
    pages = make_class_pages(docs)
    csv = make_csv(tmp_path)
    csv.write_text(
        csv.read_text(encoding="utf-8") + "ghost,c_alias.cnf,c_alias_analysis,cfpq,1\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(applicable_graphs, "DOCS_DIR", docs)
    monkeypatch.setattr(applicable_graphs, "CLASS_PAGES", pages)
    monkeypatch.setattr(applicable_graphs, "REACHABLE_PAIRS_CSV", csv)

    assert applicable_graphs.main([]) == 1
    assert "not listed in any docs category" in capsys.readouterr().out


def test_load_rows_fixture(tmp_path):
    rows = load_rows(make_csv(tmp_path))
    assert [r["query_class"] for r in rows] == ["cfpq", "cfpq", "rpq"]


def test_check_mode_on_the_real_repo_is_in_sync():
    # Guards against drift between the CSV and the applicable-graphs regions.
    assert applicable_graphs.main([]) == 0
