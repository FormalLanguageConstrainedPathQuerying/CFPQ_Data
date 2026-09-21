---
name: run-tests
description: Use when running the CFPQ_Data test suite (pytest). Thin pointer to the "Test pipeline" section of docs/developer.rst, which holds the model and points at the CI workflow step with the exact command; keeps the machine-specific pitfalls (bare pytest, partial venv after uv add).
---

# Run tests

What the test pipeline is (doctest-enabled suite, CI matrix, coverage gate)
and where the exact command lives (the CI workflow step referenced by the
section) are documented in the "Test pipeline" section of `docs/developer.rst`.
Read that section before running anything. This skill keeps only the
machine-specific pitfalls below.

## Do not run bare pytest

Never run `pytest` or `python -m pytest` with the system interpreter. The
system Python on this machine has networkx 2.6.2, while the project pins
`networkx ^3.6.1` (`pyproject.toml`). The edge-count assertions in
`tests/graphs/generators/test_fast_labeled_binomial_graph.py` and the doctest
in `cfpq_data/graphs/generators/fast_labeled_binomial_graph.py` depend on
networkx's version-specific RNG behavior and fail spuriously under 2.6.2
(91 != 85, 182 != 177, 722 != 711). If a bare-pytest run shows exactly those
failures, re-run under `uv run` before investigating — the suite is green in
the uv project environment (networkx 3.6.1).

## Re-sync after `uv add` / `uv remove`

`uv add <package>` syncs only part of the dependency set and can leave the
venv missing packages from the other groups (`test`, `docs`) — observed
2026-09-21: after `uv add lark`, the venv had no pytest, and `uv run pytest`
silently resolved to the system pytest 8.0.1 (networkx 2.6.2), producing
exactly the bare-pytest failure signature above. After any `uv add` or
`uv remove`, restore the full environment before running anything:

    uv sync --all-groups

## Notes

- Test deps: `pytest`, `pytest-cov` (the `test` dependency group in
  `pyproject.toml`).
