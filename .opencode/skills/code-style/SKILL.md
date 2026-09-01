---
name: code-style
description: Use before committing to format and lint CFPQ_Data. Covers pre-commit and black; the hook list is defined in .pre-commit-config.yaml.
---

# Code style

Formatting and linting run through `pre-commit`. The hook list is the source
of truth in `.pre-commit-config.yaml` (black, plus whitespace/yaml/requirements
fixers) — do not duplicate it.

## Commands

Run once across the whole repo:

```bash
pre-commit run --all-files --color always --verbose --show-diff-on-failure
```

Or rely on the installed git hook (run `pre-commit install` once) to run on
each commit.

Format a single file with black directly:

```bash
black <path>
```

## Notes

- CI runs the full pre-commit pass (`pre-commit run --all-files`) — see
  `.github/workflows/lint.yml`.
- Dev deps are in `requirements/developer.txt` (`black`, `pre-commit`, `pytest`).
