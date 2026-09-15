---
name: build-docs
description: Use when building the CFPQ_Data Sphinx documentation. Covers installing doc deps and running the make target.
---

# Build docs

The model (no-warnings policy, CI checks, gh-pages deployment) is documented
in the "Docs build and deploy" section of `docs/developer.rst`; the canonical
local instructions live in `docs/README.md` — do not duplicate them here.
This skill keeps only the commands and the agent-specific notes below.

## Commands

Install doc dependencies (from the repo root):

```bash
poetry install --with docs
```

Build the HTML (from `docs/`):

```bash
make html
```

Output goes to `docs/_build/html/` (git-ignored).

Check all links (from the repo root; full check including external URLs —
network-bound and slower than the html build; exits non-zero on broken or
timed-out links, redirects do not fail it):

```bash
sphinx-build -b linkcheck docs docs/_build/linkcheck
```

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
