#!/usr/bin/env python3
"""Validate the math snippets of the docs pages.

Sphinx passes math content verbatim to MathJax, which renders it in the
browser; a snippet that MathJax cannot parse shows up as an error message on
the deployed page while the Sphinx build stays green (issue #127). This tool
scans every ``.rst`` file under ``docs/`` and rejects the known-broken
pattern: an unescaped underscore inside a text-mode command group (``\\text``,
``\\textit``, ``\\textrm``, ``\\textbf``, ``\\mbox``). Inside such a group the
content is typeset in text mode, where ``_`` is illegal ("'_' allowed only in
math mode"); a subscript outside the group (``\\textit{load}_f``) is valid.

Usage::

    python utils/check_math_snippets.py [--dir docs]
"""

import argparse
import pathlib
import re
import sys
from typing import Optional, Sequence

__all__ = [
    "check_docs",
    "extract_math_snippets",
    "find_broken_snippets",
    "main",
]

#: Commands whose argument is typeset in text mode inside a math environment,
#: where an underscore is illegal.
_TEXT_MODE_RE = re.compile(r"\\(?:text|textit|textrm|textbf|mbox)\s*\{")

_INLINE_MATH_RE = re.compile(r":math:`([^`]+)`", re.DOTALL)
_MATH_BLOCK_RE = re.compile(r"^\s*\.\.\s+math::\s*$")
_CODE_BLOCK_RE = re.compile(r"^\s*\.\.\s+(?:code-block|literalinclude|sourcecode)::")


def _directive_body(lines: list[str], i: int) -> tuple[int, list[str]]:
    """Returns the (end index, body lines) of the indented block after ``lines[i]``.

    The end index is the first line index past the block (trailing blank
    lines are included in the span); body lines are stripped of their
    indentation.
    """
    base = len(lines[i]) - len(lines[i].lstrip())
    j = i + 1
    n = len(lines)
    body_indent: Optional[int] = None
    body: list[str] = []
    while j < n:
        line = lines[j]
        if not line.strip():
            j += 1
            continue
        indent = len(line) - len(line.lstrip())
        if body_indent is None:
            if indent <= base:
                break
            body_indent = indent
        elif indent < body_indent:
            break
        body.append(line.strip())
        j += 1
    return j, body


def _code_block_spans(lines: list[str]) -> list[tuple[int, int]]:
    """Returns the (start, end) line-index spans of code-block directives."""
    spans: list[tuple[int, int]] = []
    i, n = 0, len(lines)
    while i < n:
        if not _CODE_BLOCK_RE.match(lines[i]):
            i += 1
            continue
        j, _ = _directive_body(lines, i)
        spans.append((i, j))
        i = j
    return spans


def _mask_code_blocks(text: str) -> str:
    """Returns the text with code-block directives blanked out.

    The line count is preserved so that the line numbers of the remaining
    content stay valid.
    """
    lines = text.splitlines()
    for start, end in _code_block_spans(lines):
        for k in range(start, end):
            lines[k] = ""
    return "\n".join(lines)


def extract_math_snippets(text: str) -> list[tuple[int, str]]:
    """Returns the (start line, snippet) pairs of every math snippet in an RST text.

    Collects inline ``:math:`` roles (which may span several lines) and the
    bodies of ``.. math::`` directives; code-block directives are ignored.
    Line numbers are 1-based and whitespace inside a snippet is collapsed to
    single spaces.

    Parameters
    ----------
    text : str
        The reStructuredText source to scan.

    Examples
    --------
    >>> extract_math_snippets("a :math:`x_1` b\\n\\n.. math::\\n\\n   y_2\\n")
    [(1, 'x_1'), (3, 'y_2')]

    Returns
    -------
    snippets : list[tuple[int, str]]
        The (start line, snippet) pairs, in document order.
    """
    masked = _mask_code_blocks(text)
    lines = masked.splitlines()

    snippets: list[tuple[int, str]] = []
    block_lines: set[int] = set()
    for i, line in enumerate(lines):
        if not _MATH_BLOCK_RE.match(line):
            continue
        j, body = _directive_body(lines, i)
        block_lines.update(range(i, j))
        if body:
            snippets.append((i + 1, " ".join(body)))

    for match in _INLINE_MATH_RE.finditer(masked):
        line_no = masked.count("\n", 0, match.start()) + 1
        if line_no - 1 in block_lines:
            continue
        snippet = " ".join(match.group(1).split())
        snippets.append((line_no, snippet))

    snippets.sort()
    return snippets


def _has_unescaped_underscore(text: str) -> bool:
    """Returns True if text holds an underscore not escaped by a backslash."""
    for match in re.finditer(r"_", text):
        i = match.start() - 1
        backslashes = 0
        while i >= 0 and text[i] == "\\":
            backslashes += 1
            i -= 1
        if backslashes % 2 == 0:
            return True
    return False


def _text_mode_groups(snippet: str) -> list[str]:
    """Returns the brace-balanced arguments of the text-mode commands in a snippet.

    An unbalanced group extends to the end of the snippet so its content is
    still checked.
    """
    groups: list[str] = []
    for match in _TEXT_MODE_RE.finditer(snippet):
        depth = 1
        j = match.end()
        while j < len(snippet) and depth > 0:
            if snippet[j] == "{":
                depth += 1
            elif snippet[j] == "}":
                depth -= 1
            j += 1
        end = j - 1 if depth == 0 else len(snippet)
        groups.append(snippet[match.end() : end])
    return groups


def find_broken_snippets(snippets: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Returns the (line, snippet) pairs with a raw underscore in a text-mode group.

    Parameters
    ----------
    snippets : list[tuple[int, str]]
        The (start line, snippet) pairs as returned by ``extract_math_snippets``.

    Returns
    -------
    broken : list[tuple[int, str]]
        The violating pairs, in the order of the input.
    """
    broken: list[tuple[int, str]] = []
    for line, snippet in snippets:
        if any(
            _has_unescaped_underscore(group) for group in _text_mode_groups(snippet)
        ):
            broken.append((line, snippet))
    return broken


def check_docs(docs_dir: pathlib.Path) -> list[str]:
    """Returns one message per broken math snippet under docs_dir.

    Parameters
    ----------
    docs_dir : pathlib.Path
        The directory to scan recursively for ``.rst`` pages (``_build``
        directories are skipped).

    Returns
    -------
    messages : list[str]
        One ``path:line: reason`` message per violation, sorted by file.
    """
    messages: list[str] = []
    for path in sorted(pathlib.Path(docs_dir).rglob("*.rst")):
        if "_build" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for line, snippet in find_broken_snippets(extract_math_snippets(text)):
            messages.append(
                f"{path}:{line}: unescaped '_' inside a text-mode group: {snippet}"
            )
    return messages


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Checks all docs pages; returns 0 if clean, 1 on any violation."""
    parser = argparse.ArgumentParser(
        description="Validate the math snippets of the docs pages."
    )
    parser.add_argument(
        "--dir", default="docs", help="directory to scan for .rst pages"
    )
    args = parser.parse_args(argv)

    messages = check_docs(pathlib.Path(args.dir))
    if messages:
        for message in messages:
            print(message)
        print(f"\n{len(messages)} broken math snippet(s) found.")
        return 1
    print("All math snippets are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
