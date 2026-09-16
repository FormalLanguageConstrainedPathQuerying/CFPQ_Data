---
name: documentation
description: Use when determining which docs to update for a code change. Maps source changes to required documentation actions and defines documentation completeness verification. The single source of truth for doc conventions in this project.
---

# Documentation

Sphinx docs live in `docs/`; the API reference mirrors the package under
`docs/reference/` (`graphs/`, `grammars/`, `dataset/`). This skill is the
single source of truth for what docs to update when code changes.

## Mapping: source change -> doc action

| Source change | Required doc action |
|---|---|
| New public function/class | Add to the matching `autosummary` list in `docs/reference/<sub>/<module>.rst` (e.g. `graphs_generators.rst`, `grammars_readwrite.rst`); write a numpydoc docstring with `Examples` |
| Changed public function | Update its numpydoc docstring (params, returns, `Examples`) |
| New module | Add a `*.rst` page and add it to the parent `index.rst` toctree |
| Removed/renamed API | Update the autosummary list and any docstrings/links referencing it |
| New dataset graph/grammar | Update the dataset lists in `docs/` and the README examples if applicable |

## Docstring conventions

- numpydoc style: `Parameters`, `Returns`, `Examples` sections.
- `Examples` are run as **doctests** (`--doctest-modules`) — keep them
  self-contained and output-stable.

## Completeness verification

A documentation update is complete when:

- [ ] At least one doc file was created or updated for the change.
- [ ] New public APIs appear in the correct autosummary list.
- [ ] Navigation (toctrees in `docs/reference/index.rst` and sub-index pages)
      is updated for any new page.
- [ ] Docstrings follow numpydoc and their `Examples` pass as doctests.

To build and check the docs, see the `build-docs` skill.
