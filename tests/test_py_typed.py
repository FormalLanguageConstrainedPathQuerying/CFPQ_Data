from importlib.resources import files


def test_py_typed_marker_present():
    # PEP 561: without the marker, type checkers ignore the inline
    # annotations of an installed package.
    assert (files("flpq_data") / "py.typed").is_file()
