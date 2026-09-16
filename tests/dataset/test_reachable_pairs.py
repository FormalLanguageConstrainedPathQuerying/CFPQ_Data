from cfpq_data.dataset import REACHABLE_PAIRS_CSV, reachable_pairs


def test_csv_exists():
    assert REACHABLE_PAIRS_CSV.exists()


def test_total_count():
    rows = reachable_pairs()
    assert len(rows) == 155


def test_all_rows_have_keys():
    for row in reachable_pairs():
        assert set(row.keys()) == {"graph", "grammar", "num_reachable_pairs"}


def test_available_and_unavailable():
    rows = reachable_pairs()
    available = [r for r in rows if r["num_reachable_pairs"] is not None]
    unavailable = [r for r in rows if r["num_reachable_pairs"] is None]
    assert len(available) == 151
    assert len(unavailable) == 4
    unavailable_graphs = {r["graph"] for r in unavailable}
    assert unavailable_graphs == {"libgdx", "unigraph_8", "unigraph_9", "unigraph_10"}


def test_filter_by_graph():
    rows = reachable_pairs(graph="guava")
    assert len(rows) == 1
    assert rows[0]["grammar"] == "java_points_to.cnf"
    assert rows[0]["num_reachable_pairs"] == 26384496


def test_filter_by_grammar():
    rows = reachable_pairs(grammar="c_alias.cnf")
    assert len(rows) == 20
    assert all(r["grammar"] == "c_alias.cnf" for r in rows)


def test_filter_by_graph_and_grammar():
    rows = reachable_pairs(graph="wc", grammar="c_alias.cnf")
    assert len(rows) == 1
    assert rows[0]["num_reachable_pairs"] == 156


def test_no_match_returns_empty():
    assert reachable_pairs(graph="nonexistent") == []
    assert reachable_pairs(grammar="nonexistent.cnf") == []


def test_rdf_graph_has_multiple_grammars():
    rows = reachable_pairs(graph="generations")
    assert len(rows) == 3
    grammars = {r["grammar"] for r in rows}
    assert grammars == {
        "nested_parentheses_subClassOf.cnf",
        "nested_parentheses_subClassOf_type.cnf",
        "nested_parentheses_type.cnf",
    }


def test_enzyme_has_broader_transitive():
    rows = reachable_pairs(graph="enzyme")
    assert len(rows) == 4
    grammars = {r["grammar"] for r in rows}
    assert "nested_parentheses_broaderTransitive.cnf" in grammars


def test_values_are_positive_ints():
    for row in reachable_pairs():
        val = row["num_reachable_pairs"]
        if val is not None:
            assert isinstance(val, int)
            assert val >= 0
