---
name: add-grammar
description: Use when adding a new grammar template to CFPQ_Data. Covers the generator/readwrite/converter module conventions and the PR/issue templates.
---

# Add a grammar template

## Source of truth

The required fields and metadata live in the GitHub templates — do **not**
duplicate them here:

- `.github/PULL_REQUEST_TEMPLATE/new_grammar.md`
- `.github/ISSUE_TEMPLATE/grammar-add-template.md`

Fill in every field in the triangle brackets (`<>`) of those templates.

## Package conventions

Grammar code lives in `cfpq_data/grammars/`:

- `generators/` — template factories (e.g. `dyck_grammar`, `c_alias_grammar`).
- `readwrite/` — (de)serialization (`cfg_*`, `cnf_*`, `rsa_*`, `regex_*`).
- `converters/` — conversions between formalisms (`cfg_from_cnf`, ...).
- `utils/` — helpers (e.g. `change_terminals_in_cfg`).

Each new module must:

1. Define `__all__` listing its public functions.
2. Export it from the relevant `__init__.py`
   (`generators/__init__.py`, `readwrite/__init__.py`, etc.).
3. Provide numpydoc docstrings with `Examples` (these are run as doctests).
4. Add a mirroring test under `tests/grammars/<submodule>/test_*.py`.
5. Add the template name to `GRAMMAR_TEMPLATES` in
   `cfpq_data/dataset/data.py` if it should be downloadable.

Use `pyformlang` types (`CFG`, `CNF`, `RSA`, `Regex`) as the interchange
format. See `.opencode/skills/run-tests` to verify.
