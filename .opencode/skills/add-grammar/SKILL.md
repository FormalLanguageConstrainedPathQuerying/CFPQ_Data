---
name: add-grammar
description: Use when adding a new grammar template to FLPQ_Data. Covers the generator/readwrite/converter module conventions and the issue template.
---

# Add a grammar template

## Source of truth

The required fields and metadata live in the GitHub issue template — do
**not** duplicate them here:

- `.github/ISSUE_TEMPLATE/new-data-template.md` (the "Queries and grammars"
  section; a grammar arrives only together with a data contribution)

Fill in every field in the triangle brackets (`<>`) of that template.

## Where grammars come from

Grammars arrive via cases 2, 3, or 4b of a CONTRIBUTE NEW DATA issue: the
issue carries the grammar definition (LaTeX plus file-format text), and the
same grammar is instantiated as at least one query directory with
`results.mtx` in a contributed archive. When the grammar is parameterized,
implement its generator module under `flpq_data/queries/<class>/generators/`
per the package conventions below; the docs wiring (category page, table
column) follows the "Documentation" section of the `add-graph` skill.

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
