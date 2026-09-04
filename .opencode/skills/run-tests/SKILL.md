---
name: run-tests
description: Use when running the CFPQ_Data test suite (pytest). Covers the exact pytest invocation in the Poetry environment, doctest coverage, and how tests mirror the package layout.
---

# Run tests

The suite is `pytest` with **doctests enabled** for both the package and the
`tests/` directory.

## Commands

Always run tests inside the Poetry environment (as CI does):

```bash
poetry run pytest --doctest-modules -vv -s cfpq_data tests
```

A single module/function:

```bash
poetry run pytest tests/graphs/utils/test_add_reverse_edges.py
```

## Do not run bare pytest

Never run `pytest` or `python -m pytest` with the system interpreter. The
system Python on this machine has networkx 2.6.2, while the project pins
`networkx ^3.6.1` (`pyproject.toml`). The edge-count assertions in
`tests/graphs/generators/test_fast_labeled_binomial_graph.py` and the doctest
in `cfpq_data/graphs/generators/fast_labeled_binomial_graph.py` depend on
networkx's version-specific RNG behavior and fail spuriously under 2.6.2
(91 != 85, 182 != 177, 722 != 711). If a bare-pytest run shows exactly those
failures, re-run under `poetry run` before investigating — the suite is green
in the Poetry environment (networkx 3.6.1).

## Notes

- `testpaths` and `--doctest-modules` are configured in `pyproject.toml`
  (`[tool.pytest.ini_options]`); the command above is the canonical CI command
  (see `.github/workflows/tests.yml`).
- `tests/` mirrors `cfpq_data/` (e.g., `tests/graphs/generators/`,
  `tests/grammars/readwrite/`).
- Doctests live in the docstrings of the public functions in `cfpq_data/`.
- Test deps: `pytest`, `pytest-cov`, `codecov` (`requirements/tests.txt`).
