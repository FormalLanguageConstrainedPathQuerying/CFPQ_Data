---
name: reusing
description: Use before creating any new code, types, functions, or documentation. Run this reuse checklist to find existing material to reuse or generalize instead of duplicating. Enforces the "one source of truth / no duplicates" principle.
---

# Reusing

Before writing new code or docs, search for existing material and reuse or
generalize it. Duplicating an existing function, type, or doc section violates
the project's single-source-of-truth principle.

## Checklist

Run through these before creating new material:

- [ ] **Package code** — search `cfpq_data/` for an existing function or type
      that already does (or nearly does) the job. Prefer generalizing the
      existing one over adding a near-copy.
- [ ] **Graph types** — graphs are `networkx.MultiDiGraph`; use NetworkX
      built-ins (`nx.from_pandas_edgelist`, generators, `nx.MultiDiGraph`) and
      the existing `cfpq_data.graphs` helpers instead of reimplementing.
- [ ] **Grammar types** — grammars are `pyformlang` `CFG` / `CNF` / `RSA` /
      `Regex`; use pyformlang APIs and existing `cfpq_data.grammars` converters
      instead of reimplementing.
- [ ] **Generators** — check `cfpq_data/graphs/generators` and
      `cfpq_data/grammars/generators` for an existing template before adding a
      new one.
- [ ] **Readwrite** — check `readwrite` modules for an existing
      `*_from_text`/`*_to_text` pair before adding new serialization.
- [ ] **Tests** — check `tests/` for existing fixtures, helpers, or patterns to
      extend rather than duplicate.
- [ ] **Docs** — check `docs/reference/` and existing docstrings for a section
      to update rather than add a new page.

## Rules

- If a close match exists, **generalize it** (make it generic enough to cover
  both cases) rather than copy-paste.
- Record what is reused in each subtask's **Code** section of
  `tasks/detailed_plan.md`.
- When in doubt, prefer the existing abstraction; only create new material when
  no reasonable generalization is possible.
