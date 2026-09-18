import pathlib

import pytest
import reachable_pairs_tables
from reachable_pairs_tables import (
    BEGIN_MARKER,
    END_MARKER,
    category_order,
    graph_to_category,
    page_to_graph,
    render_tables_region,
    update_category_columns,
    update_reachable_pairs_page,
)


def make_docs(tmp_path: pathlib.Path) -> pathlib.Path:
    docs = tmp_path / "docs"
    (docs / "graphs" / "data").mkdir(parents=True)
    (docs / "graphs" / "index.rst").write_text(
        ".. _graphs:\n\nGraphs\n******\n\n"
        ".. toctree::\n   :maxdepth: 1\n\n   cat_a\n   cat_b\n"
    )
    (docs / "graphs" / "cat_a.rst").write_text(
        ".. _graphs_cat_a:\n\nCat A\n*****\n\n"
        ".. toctree::\n   :hidden:\n\n   data/g1\n   data/g2\n"
    )
    (docs / "graphs" / "cat_b.rst").write_text(
        ".. _graphs_cat_b:\n\nCat B\n*****\n\n.. toctree::\n   :hidden:\n\n   data/g3\n"
    )
    for page, name in [("g1", "alpha"), ("g2", "beta"), ("g3", "gamma")]:
        (docs / "graphs" / "data" / f"{page}.rst").write_text(
            f".. _{page}:\n\n{name}\n====\n\n"
            f"- `x.tar.gz <https://cfpq-data.storage.yandexcloud.net/"
            f"5.0.0/graph/{name}.tar.gz>`_\n"
        )
    return docs


def test_category_order(tmp_path):
    assert category_order(make_docs(tmp_path)) == ["cat_a", "cat_b"]


def test_page_to_graph_and_graph_to_category(tmp_path):
    docs = make_docs(tmp_path)
    assert page_to_graph(docs) == {"g1": "alpha", "g2": "beta", "g3": "gamma"}
    assert graph_to_category(docs) == {
        "alpha": "cat_a",
        "beta": "cat_a",
        "gamma": "cat_b",
    }


def test_graph_to_category_duplicate_raises(tmp_path):
    docs = make_docs(tmp_path)
    (docs / "graphs" / "data" / "g3.rst").write_text(
        ".. _g3:\n\ngamma\n=====\n\n"
        "- `x.tar.gz <https://cfpq-data.storage.yandexcloud.net/"
        "5.0.0/graph/alpha.tar.gz>`_\n"
    )
    with pytest.raises(ValueError, match="listed in both"):
        graph_to_category(docs)


def test_page_to_graph_missing_link_raises(tmp_path):
    docs = make_docs(tmp_path)
    (docs / "graphs" / "data" / "g3.rst").write_text(".. _g3:\n\ngamma\n=====\n")
    with pytest.raises(ValueError, match="no Yandex download link"):
        page_to_graph(docs)


ROWS = [
    {
        "graph": "alpha",
        "grammar": "a.cnf",
        "category": "cat_a",
        "num_reachable_pairs": 3,
    },
    {
        "graph": "alpha",
        "grammar": "b.cnf",
        "category": "cat_a",
        "num_reachable_pairs": None,
    },
    {
        "graph": "beta",
        "grammar": "a.cnf",
        "category": "cat_a",
        "num_reachable_pairs": 5,
    },
    {
        "graph": "beta",
        "grammar": "b.cnf",
        "category": "cat_a",
        "num_reachable_pairs": 9,
    },
    {
        "graph": "gamma",
        "grammar": "g.cnf",
        "category": "cat_b",
        "num_reachable_pairs": 7,
    },
]


def test_render_tables_region(tmp_path):
    docs = make_docs(tmp_path)
    region = render_tables_region(ROWS, docs)

    # Sections in category order, titled like the category pages.
    assert region.index("Cat A") < region.index("Cat B")
    assert "Cat A\n-----" in region
    assert "Cat B\n-----" in region

    # Rows sorted by (graph, grammar) within a section.
    cat_a = region[region.index("Cat A") : region.index("Cat B")]
    assert cat_a.index("- a.cnf") < cat_a.index("- b.cnf")
    assert cat_a.index("* - alpha") < cat_a.index("* - beta")

    # A row without a computed value renders as "not available".
    assert "not available" in cat_a
    # The other category's rows do not leak into this section.
    assert "gamma" not in cat_a


def test_render_tables_region_empty_category(tmp_path):
    docs = make_docs(tmp_path)
    region = render_tables_region(ROWS[:4], docs)
    cat_b = region[region.index("Cat B") :]
    assert "No reachable-pair counts have been computed" in cat_b


def test_update_reachable_pairs_page():
    text = f"intro\n{BEGIN_MARKER}\nold content\n{END_MARKER}\noutro\n"
    updated, changed = update_reachable_pairs_page(text, "new content")
    assert changed
    assert updated.splitlines() == [
        "intro",
        BEGIN_MARKER,
        "",
        "new content",
        "",
        END_MARKER,
        "outro",
    ]
    # Idempotent: replacing with the same region changes nothing.
    again, changed_again = update_reachable_pairs_page(updated, "new content")
    assert not changed_again
    assert again == updated


def test_update_reachable_pairs_page_missing_markers():
    with pytest.raises(ValueError, match="not found"):
        update_reachable_pairs_page("no markers here\n", "x")


BASE_URL = "https://cfpq-data.storage.yandexcloud.net/5.0.0/graph"
ALPHA_URL = f"{BASE_URL}/alpha.tar.gz"
BETA_URL = f"{BASE_URL}/beta.tar.gz"
GAMMA_URL = f"{BASE_URL}/gamma.tar.gz"

CATEGORY_TABLE = (
    ".. list-table::\n"
    "   :header-rows: 1\n"
    "\n"
    "   * - Graph\n"
    "     - Num Nodes\n"
    "     - a_col\n"
    "     - b_col\n"
    "     - Download\n"
    "   * - :ref:`g1`\n"
    "     - 10\n"
    "     - 3\n"
    "     -\n"
    f"     - `alpha.tar.gz <{ALPHA_URL}>`_ 📥\n"
    "   * - :ref:`g2`\n"
    "     - 20\n"
    "     - not available\n"
    "     - 9\n"
    f"     - `beta.tar.gz <{BETA_URL}>`_ 📥\n"
    "   * - :ref:`g3`\n"
    "     - 30\n"
    "     -\n"
    "     -\n"
    f"     - `gamma.tar.gz <{GAMMA_URL}>`_ 📥\n"
)

COLUMNS: list[tuple[str, str | None]] = [("a_col", "a.cnf"), ("b_col", "b.cnf")]
PAGES = {"g1": "alpha", "g2": "beta", "g3": "gamma"}


def test_update_category_columns_semantics():
    updated, problems = update_category_columns(
        CATEGORY_TABLE, ROWS, "cat_a", PAGES, columns=COLUMNS
    )

    # alpha/b.cnf: in the CSV without a value -> "not available" (was empty);
    # beta/a.cnf: 5 (was "not available"). Everything else already matches.
    assert len(problems) == 2
    lines = updated.splitlines()
    assert lines[11] == "     - not available"
    assert lines[15] == "     - 5"
    # Unchanged lines keep their exact text, including the empty cells of a
    # graph whose grammars do not apply (gamma).
    assert lines[10] == "     - 3"
    assert lines[20] == "     -"
    assert lines[21] == "     -"

    # Idempotent: the updated text is in sync.
    _, problems_again = update_category_columns(
        updated, ROWS, "cat_a", PAGES, columns=COLUMNS
    )
    assert problems_again == []


def test_update_category_columns_empty_cell_for_missing_grammar():
    # beta has no b.cnf row in the CSV -> its b_col cell must become empty.
    rows = [r for r in ROWS if not (r["graph"] == "beta" and r["grammar"] == "b.cnf")]
    updated, problems = update_category_columns(
        CATEGORY_TABLE, rows, "cat_a", PAGES, columns=COLUMNS
    )
    lines = updated.splitlines()
    assert lines[16] == "     -"
    assert any("beta/b.cnf" in p for p in problems)


def test_update_category_columns_short_row_is_a_problem():
    # The row has cells for Graph and a_col only.
    text = (
        ".. list-table::\n"
        "   :header-rows: 1\n"
        "\n"
        "   * - Graph\n"
        "     - a_col\n"
        "     - b_col\n"
        "     - Download\n"
        "   * - :ref:`g1`\n"
        "     - 3\n"
    )
    updated, problems = update_category_columns(
        text, ROWS, "cat_a", PAGES, columns=COLUMNS
    )
    assert any("has no cell for column b_col" in p for p in problems)


def test_update_category_columns_missing_header_column_is_a_problem():
    # The table has no b_col column at all.
    text = (
        ".. list-table::\n"
        "   :header-rows: 1\n"
        "\n"
        "   * - Graph\n"
        "     - a_col\n"
        "     - Download\n"
        "   * - :ref:`g1`\n"
        "     - 3\n"
        f"     - `alpha.tar.gz <{ALPHA_URL}>`_ 📥\n"
    )
    updated, problems = update_category_columns(
        text, ROWS, "cat_a", PAGES, columns=COLUMNS
    )
    assert any("column b_col is missing from the table header" in p for p in problems)


def test_update_category_columns_unknown_category_raises():
    with pytest.raises(ValueError, match="GRAMMAR_COLUMNS"):
        update_category_columns(CATEGORY_TABLE, ROWS, "cat_a", PAGES)


def test_check_mode_on_the_real_repo_is_in_sync():
    # Guards against drift between the CSV and both renderings.
    assert reachable_pairs_tables.main([]) == 0
