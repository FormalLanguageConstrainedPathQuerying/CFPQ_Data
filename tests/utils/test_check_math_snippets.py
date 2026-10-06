from pathlib import Path

from check_math_snippets import (
    check_docs,
    extract_math_snippets,
    find_broken_snippets,
    main,
)

DOCS_DIR = Path(__file__).resolve().parents[2] / "docs"


def test_extract_inline_role():
    assert extract_math_snippets("x :math:`a_1` y") == [(1, "a_1")]


def test_extract_multiple_inline_roles_on_one_line():
    assert extract_math_snippets(":math:`a` and :math:`b_2`") == [
        (1, "a"),
        (1, "b_2"),
    ]


def test_extract_multiline_inline_role():
    text = "for :math:`\\{w \\mid\nw \\in L\\}` end"
    assert extract_math_snippets(text) == [(1, "\\{w \\mid w \\in L\\}")]


def test_extract_math_block():
    text = ".. math::\n\n   S \\rightarrow a_1 \\\\\n   V \\rightarrow b_2 \\\\\n"
    assert extract_math_snippets(text) == [
        (1, "S \\rightarrow a_1 \\\\ V \\rightarrow b_2 \\\\")
    ]


def test_extract_indented_math_block():
    assert extract_math_snippets("  .. math::\n\n     x_1\n") == [(1, "x_1")]


def test_extract_math_block_without_body():
    assert extract_math_snippets(".. math::\n\nNext paragraph.\n") == []


def test_extract_skips_code_blocks():
    text = ".. code-block:: latex\n\n   :math:`\\textit{a_b}`\n\nreal :math:`c_d` end\n"
    assert extract_math_snippets(text) == [(5, "c_d")]


def test_extract_code_block_without_body():
    text = ".. code-block:: python\nplain text :math:`a_b`\n"
    assert extract_math_snippets(text) == [(2, "a_b")]


def test_extract_inline_role_inside_math_block_is_not_double_counted():
    text = ".. math::\n\n   :math:`a_b`\n"
    assert extract_math_snippets(text) == [(1, ":math:`a_b`")]


def test_extract_no_math():
    assert extract_math_snippets("plain text\nno math here\n") == []


def test_broken_underscore_in_textit_group():
    snippet = r"\textit{assigment_labels}"
    assert find_broken_snippets([(1, snippet)]) == [(1, snippet)]


def test_valid_subscript_outside_group():
    assert find_broken_snippets([(1, r"\textit{load}_f")]) == []


def test_escaped_underscore_in_group_is_valid():
    assert find_broken_snippets([(1, r"\textit{a\_b}")]) == []


def test_double_backslash_before_underscore_is_broken():
    # A literal backslash (\\) followed by a raw underscore is not escaped.
    snippet = r"\textit{a\\_b}"
    assert find_broken_snippets([(1, snippet)]) == [(1, snippet)]


def test_nested_text_mode_group_is_checked():
    snippet = r"\textit{\mbox{a_b}}"
    assert find_broken_snippets([(1, snippet)]) == [(1, snippet)]


def test_plain_subscript_without_command_is_valid():
    assert find_broken_snippets([(1, r"V_1 \rightarrow a_r")]) == []


def test_all_text_mode_commands_are_checked():
    for cmd in ("text", "textit", "textrm", "textbf", "mbox"):
        snippet = rf"\{cmd}{{a_b}}"
        assert find_broken_snippets([(1, snippet)]) == [(1, snippet)]


def test_unbalanced_group_still_checked():
    snippet = r"\textit{a_b"
    assert find_broken_snippets([(1, snippet)]) == [(1, snippet)]


def test_no_snippets_no_violations():
    assert find_broken_snippets([]) == []


def test_check_docs_reports_violations(tmp_path):
    (tmp_path / "page.rst").write_text(
        "T\n=\n\n:math:`\\textit{a_b}`\n", encoding="utf-8"
    )
    messages = check_docs(tmp_path)
    assert len(messages) == 1
    assert "page.rst:4" in messages[0]
    assert r"\textit{a_b}" in messages[0]


def test_check_docs_is_clean_for_valid_pages(tmp_path):
    (tmp_path / "page.rst").write_text(
        ".. math::\n\n   \\textit{load}_f \\\\\n", encoding="utf-8"
    )
    assert check_docs(tmp_path) == []


def test_check_docs_skips_build_artifacts(tmp_path):
    build = tmp_path / "_build"
    build.mkdir()
    (build / "page.rst").write_text(":math:`\\textit{a_b}`\n", encoding="utf-8")
    assert check_docs(tmp_path) == []


def test_check_docs_empty_dir(tmp_path):
    assert check_docs(tmp_path) == []


def test_main_returns_zero_when_clean(tmp_path, capsys):
    (tmp_path / "page.rst").write_text("no math\n", encoding="utf-8")
    assert main(["--dir", str(tmp_path)]) == 0
    assert "valid" in capsys.readouterr().out


def test_main_returns_one_on_violation(tmp_path, capsys):
    (tmp_path / "page.rst").write_text(":math:`\\textit{a_b}`\n", encoding="utf-8")
    assert main(["--dir", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "page.rst:1" in out


def test_real_docs_tree_is_clean():
    assert check_docs(DOCS_DIR) == []
