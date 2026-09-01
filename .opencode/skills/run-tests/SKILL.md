---
name: run-tests
description: Use when running the CFPQ_Data test suite (pytest). Covers the exact pytest invocation, doctest coverage, and how tests mirror the package layout.
---

# Run tests

The suite is `pytest` with **doctests enabled** for both the package and the
`tests/` directory.

## Commands

```bash
pytest --doctest-modules -vv -s cfpq_data tests
```

Using Poetry (as CI does):

```bash
poetry run pytest --doctest-modules -vv -s cfpq_data tests
```

A single module/function:

```bash
pytest tests/graphs/utils/test_add_reverse_edges.py
```

## Notes

- `testpaths` and `--doctest-modules` are configured in `pyproject.toml`
  (`[tool.pytest.ini_options]`); the command above is the canonical CI command
  (see `.github/workflows/tests.yml`).
- `tests/` mirrors `cfpq_data/` (e.g. `tests/graphs/generators/`,
  `tests/grammars/readwrite/`).
- Doctests live in the docstrings of the public functions in `cfpq_data/`.
- Test deps: `pytest`, `pytest-cov`, `codecov` (`requirements/tests.txt`).
