---
name: build-docs
description: Use when building the CFPQ_Data Sphinx documentation. Covers installing doc deps and running the make target.
---

# Build docs

Docs are built with Sphinx from the `docs/` directory. See `docs/README.md`
for the canonical instructions — do not duplicate them.

## Commands

Install doc dependencies (from the repo root):

```bash
pip install -r requirements/docs.txt
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

- No-warnings policy: the build runs with `-W --keep-going` (set in
  `docs/Makefile`), so any Sphinx warning — including an unresolved
  cross-reference under `nitpicky = True` — fails the build and every
  warning is listed in one run. Fix warnings; do not suppress them
  (`suppress_warnings`) or weaken the flag.
- A config-only change (e.g. enabling `nitpicky`) does not re-resolve
  references in documents whose content is unchanged — their doctrees are
  reused from the cache, so unresolved-reference warnings stay hidden until
  those pages are next edited. After changing reference-related config, do a
  clean rebuild (`make clean && make html`) before trusting the warning log.
- API reference pages use `.. automodule::` / `.. autosummary::`; generated
  stub files land under `docs/*/generated/` and are git-ignored.
- Add new public functions to the matching `docs/reference/<sub>/...rst`
  autosummary list when extending the API.
