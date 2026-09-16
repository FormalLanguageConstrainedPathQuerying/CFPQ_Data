from audit_info_tables import info_fields


def _page(*fields: str) -> str:
    rows = "   * -\n     -\n" + "".join(
        f"   * - {field}\n     - value\n" for field in fields
    )
    return (
        "wc\n==\n\nInfo\n----\n\n.. list-table::\n   :header-rows: 1\n\n"
        f"{rows}\n\nGraph Statistics\n----------------\n\n.. list-table::\n"
        "   :header-rows: 1\n\n   * - Num Nodes\n      - Num Edges\n"
    )


def test_info_fields_returns_labels_in_order():
    assert info_fields(_page("Full Name", "Version", "Direct download")) == [
        "Full Name",
        "Version",
        "Direct download",
    ]


def test_info_fields_skips_empty_header_row():
    assert info_fields(_page("Full Name")) == ["Full Name"]


def test_info_fields_stops_at_next_section():
    text = _page("Full Name", "Version")
    # A second list-table (Graph Statistics) must not leak into the result.
    assert info_fields(text) == ["Full Name", "Version"]


def test_info_fields_returns_empty_without_info_section():
    assert info_fields("Graph Statistics\n----------------\n\n.. list-table::\n") == []
