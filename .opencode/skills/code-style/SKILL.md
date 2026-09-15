---
name: code-style
description: Use before committing to format and lint CFPQ_Data. Covers pre-commit and black; the hook list is defined in .pre-commit-config.yaml.
---

# Code style

What pre-commit enforces and how CI runs it is documented in the "Pre-commit"
section of `docs/developer.rst` (single source of truth). The hook list lives
in `.pre-commit-config.yaml`. This skill keeps only the local commands.

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

- Dev deps are in `requirements/developer.txt` (`black`, `pre-commit`, `pytest`).
