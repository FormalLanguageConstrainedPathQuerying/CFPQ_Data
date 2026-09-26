from flpq_data.dataset import REACHABLE_PAIRS_CSV, reachable_pairs


def test_csv_exists():
    assert REACHABLE_PAIRS_CSV.exists()


def test_total_count():
    rows = reachable_pairs()
    assert len(rows) == 155


def test_all_rows_have_keys():
    for row in reachable_pairs():
        assert set(row.keys()) == {
            "graph",
            "grammar",
            "category",
            "query_class",
            "num_reachable_pairs",
        }


def test_query_class_values():
    # All the current counts are CFPQ data.
    assert {r["query_class"] for r in reachable_pairs()} == {"cfpq"}


def test_query_class_filter():
    assert len(reachable_pairs(query_class="cfpq")) == 155
    assert reachable_pairs(query_class="rpq") == []


CATEGORIES = {
    "biological_uniprot": 10,
    "c_alias_analysis": 20,
    "context_sensitive_data_flow": 10,
    "data_provenance": 18,
    "field_sensitive_alias": 10,
    "java_points_to": 21,
    "name_resolution": 4,
    "rdf": 62,
}


def test_categories_are_valid():
    rows = reachable_pairs()
    assert {r["category"] for r in rows} == set(CATEGORIES)


def test_row_counts_per_category():
    for category, count in CATEGORIES.items():
        assert len(reachable_pairs(category=category)) == count


def test_every_graph_has_one_category():
    rows = reachable_pairs()
    by_graph: dict[str, set[str]] = {}
    for row in rows:
        by_graph.setdefault(row["graph"], set()).add(row["category"])
    assert all(len(cats) == 1 for cats in by_graph.values())


def test_available_and_unavailable():
    # A pair has a count iff its results.mtx is computed in the archive;
    # the rest are stubs awaiting the follow-up computation task.
    rows = reachable_pairs()
    available = [r for r in rows if r["num_reachable_pairs"] is not None]
    unavailable = [r for r in rows if r["num_reachable_pairs"] is None]
    assert len(available) == 95
    assert len(unavailable) == 60
    # Spot checks: a computed pair and a stubbed one.
    by_pair = {(r["graph"], r["grammar"]): r for r in rows}
    assert by_pair[("wc", "c_alias.cnf")]["num_reachable_pairs"] == 156
    assert by_pair[("guava", "java_points_to.cnf")]["num_reachable_pairs"] is None


def test_filter_by_graph():
    rows = reachable_pairs(graph="gson")
    assert len(rows) == 1
    assert rows[0]["grammar"] == "java_points_to.cnf"
    assert rows[0]["num_reachable_pairs"] == 56325


def test_filter_by_grammar():
    rows = reachable_pairs(grammar="c_alias.cnf")
    assert len(rows) == 20
    assert all(r["grammar"] == "c_alias.cnf" for r in rows)


def test_filter_by_graph_and_grammar():
    rows = reachable_pairs(graph="wc", grammar="c_alias.cnf")
    assert len(rows) == 1
    assert rows[0]["num_reachable_pairs"] == 156


def test_filter_by_category():
    rows = reachable_pairs(category="rdf")
    assert len(rows) == 62
    assert all(r["category"] == "rdf" for r in rows)


def test_filter_by_category_and_graph():
    rows = reachable_pairs(graph="enzyme", category="rdf")
    assert len(rows) == 4
    assert reachable_pairs(graph="enzyme", category="c_alias_analysis") == []


def test_no_match_returns_empty():
    assert reachable_pairs(graph="nonexistent") == []
    assert reachable_pairs(grammar="nonexistent.cnf") == []
    assert reachable_pairs(category="nonexistent") == []


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
