---
name: code-style
description: Use before committing to format and lint CFPQ_Data. Thin pointer to the "Pre-commit" section of docs/developer.rst, which holds the model and the exact commands; the hook list is defined in .pre-commit-config.yaml.
---

# Code style

What pre-commit enforces, how CI runs it, and the exact local commands are
documented in the "Pre-commit" section of `docs/developer.rst` — the single
source of truth. Read that section before running anything. The hook list
lives in `.pre-commit-config.yaml`.

## Notes

- Dev deps are in `requirements/developer.txt` (`black`, `pre-commit`, `pytest`).
