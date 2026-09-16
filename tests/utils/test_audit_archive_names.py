from audit_archive_names import find_indexed_names


def test_find_indexed_names_returns_placeholder_style_names():
    members = [
        "g/load_5.mtx",
        "g/load_i_5.mtx",
        "g/load_r_i_5.mtx",
        "g/alloc.mtx",
        "README.md",
    ]

    assert find_indexed_names(members) == ["g/load_i_5.mtx", "g/load_r_i_5.mtx"]


def test_find_indexed_names_ignores_non_placeholder_names():
    members = ["g/a.mtx", "g/b_5.mtx", "g/c_i_x.mtx", "g/d_i.mtx"]

    assert find_indexed_names(members) == []
