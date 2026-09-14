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

- API reference pages use `.. automodule::` / `.. autosummary::`; generated
  stub files land under `docs/*/generated/` and are git-ignored.
- Add new public functions to the matching `docs/reference/<sub>/...rst`
  autosummary list when extending the API.
