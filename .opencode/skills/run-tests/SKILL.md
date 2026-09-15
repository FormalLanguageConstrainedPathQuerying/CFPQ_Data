---
name: run-tests
description: Use when running the CFPQ_Data test suite (pytest). Thin pointer to the "Test pipeline" section of docs/developer.rst, which holds the model and the exact commands; keeps the machine-specific bare-pytest pitfall.
---

# Run tests

What the test pipeline is (doctest-enabled suite, CI matrix, coverage upload)
and the exact local commands are documented in the "Test pipeline" section of
`docs/developer.rst` — the single source of truth. Read that section before
running anything. This skill keeps only the machine-specific pitfall below.

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

- Test deps: `pytest`, `pytest-cov`, `codecov` (`requirements/tests.txt`).
