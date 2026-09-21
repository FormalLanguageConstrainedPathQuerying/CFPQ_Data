---
name: build-docs
description: Use when building the CFPQ_Data Sphinx documentation. Thin pointer to the "Docs build and deploy" section of docs/developer.rst and docs/README.md, which hold the model and point at the CI workflow steps with the exact commands; keeps the agent-specific notes.
---

# Build docs

The model (no-warnings policy, CI checks, gh-pages deployment) and where the
exact commands live (the CI workflow steps referenced by the section; the
local setup command in `docs/README.md`) are documented in the "Docs build
and deploy" section of `docs/developer.rst` — do not duplicate them here.
Read those before running anything. This skill keeps only the
agent-specific notes below.

## Notes

- No-warnings policy (see the docs page): any Sphinx warning fails the build
  — fix it, do not suppress it (`suppress_warnings`) or weaken the flag.
- A config-only change (e.g. enabling `nitpicky`) does not re-resolve
  references in documents whose content is unchanged — their doctrees are
  reused from the cache, so unresolved-reference warnings stay hidden until
  those pages are next edited. After changing reference-related config, do a
  clean rebuild (`make clean && make html`) before trusting the warning log.
- API reference pages use `.. automodule::` / `.. autosummary::`; generated
  stub files land under `docs/*/generated/` and are git-ignored.
- Add new public functions to the matching `docs/reference/<sub>/...rst`
  autosummary list when extending the API.
