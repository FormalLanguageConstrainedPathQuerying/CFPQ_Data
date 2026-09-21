---
name: code-style
description: Use before committing to format and lint CFPQ_Data. Thin pointer to the "Quality checks" section of docs/developer.rst, which holds the model and points at the CI workflow step with the exact command; the hook list is defined in .pre-commit-config.yaml.
---

# Code style

What the quality checks enforce (ruff lint/format, ty type check, hygiene
hooks), how CI runs them, and where the exact command lives (the CI workflow
step referenced by the section) are documented in the "Quality checks"
section of `docs/developer.rst`. Read that section before running anything.
The hook list lives in `.pre-commit-config.yaml`.

## Notes

- Dev tools (`ruff`, `ty`, `pyright`, `pre-commit`) live in the `dev`
  dependency group in `pyproject.toml`; run them via `uv run`.
