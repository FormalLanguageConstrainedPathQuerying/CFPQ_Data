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

Query code lives under `flpq_data/queries/<class>/` (`cfpq`, `rpq`, `mcfpq`):

- `cfpq/generators/` — template factories (e.g. `dyck_grammar`, `c_alias_grammar`).
- `cfpq/readwrite/` — (de)serialization (`cfg_*`, `cnf_*`).
- `cfpq/converters/` — conversions between formalisms (`cfg_from_cnf`, ...).
- `cfpq/utils/` — helpers (e.g. `change_terminals_in_cfg`).
- `rpq/readwrite/` — `regex_*`, `rsa_*`.
- `mcfpq/readwrite/` — lark-based `mcfg_*`.

Each new module must:

1. Define `__all__` listing its public functions.
2. Export it from the relevant `__init__.py` files up the chain
   (e.g. `queries/cfpq/readwrite/__init__.py`, then `queries/cfpq/__init__.py`).
3. Provide numpydoc docstrings with `Examples` (these are run as doctests).
4. Add a mirroring test under `tests/queries/<class>/<submodule>/test_*.py`.

Templates are not downloadable on their own — the query files they generate
ship inside each graph archive's `queries/<class>/<query>/` directory.

Use `pyformlang` types (`CFG`, `CNF`, `RSA`, `Regex`) as the interchange
format. See `.opencode/skills/run-tests` to verify.
