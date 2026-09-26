# Detailed Plan: Issue #135 — Rename/restructure the package to flpq_data at 6.0.0

## Context

The rename step of the FLPQ extension (design source of truth:
`docs/flpq.rst`, "Package structure", "API changes", "Dataset layout and
migration"). The dataset already lives at `6.0.0/graph/` (task 48) and the
site already points there (#133); this task makes the package match:

```
flpq_data/
├── config.py        version, data directories
├── dataset/         download machinery, registries, reachable pairs
├── graphs/          unchanged — class-agnostic I/O, generators, utils
└── queries/         renamed from grammars/
    ├── cfpq/        generators/, readwrite/{cfg,cnf,cnf_template}, converters/, utils/
    ├── rpq/         readwrite/{regex,rsa}
    └── mcfpq/       readwrite/mcfg
```

Verified current state on dev:

- `grammars/` holds exactly the modules listed above; cross-imports are only
  `converters/cnf.py -> converters/cfg.py` and `readwrite/cnf.py ->
  {converters/cnf, readwrite/cfg}` (all CFPQ-side, so they stay inside
  `queries/cfpq/`).
- `DATASET_KEY_PREFIX = f"{VERSION[0]}.0.0/graph"` — bumping VERSION to
  6.0.0 re-points `DATASET_URL` at `6.0.0/graph/` automatically; no separate
  URL change needed.
- `GRAMMAR_TEMPLATES` / `GRAMMARS_URL` / `BENCHMARK_URL` were removed in
  48-S6 — the design's "GRAMMAR_TEMPLATES becomes per-class templates" item
  is stale (nothing to rename).
- `download()` always re-downloads (no cache skip), so the version bump
  cannot be masked by a stale local cache.
- Files referencing the old names: package (~50 .py), tests (146 files),
  docs (232 files, incl. autosummary stubs named after module paths),
  `utils/{audit_archive_names,migrate_gdrive_to_s3,check_archive_structure}.py`,
  `pyproject.toml` (name/packages/coverage/testpaths), `.gitignore`
  (`cfpq_data/data`), `.github/workflows/coverage.yml` (`--cov=cfpq_data`),
  README.rst, AGENTS.md, six skills.

User decision (verbatim on the issue): the cfpq-data PyPI deprecation shim is
split into a follow-up task — not part of this one.

## Subtasks

### S1: Restructure grammars/ into queries/{cfpq,rpq,mcfpq}/ [done] cab6ccb

**Code:** `git mv` inside `cfpq_data/`: `grammars/generators/` ->
`queries/cfpq/generators/`; `grammars/readwrite/{cfg,cnf,cnf_template}.py` ->
`queries/cfpq/readwrite/`; `grammars/readwrite/{regex,rsa}.py` ->
`queries/rpq/readwrite/`; `grammars/readwrite/mcfg.py` ->
`queries/mcfpq/readwrite/`; `grammars/converters/` -> `queries/cfpq/converters/`;
`grammars/utils/` -> `queries/cfpq/utils/`. New `__init__.py`:
`queries/__init__.py` (star-imports the three classes), one per class, and
per-class `readwrite/__init__.py` (cfpq: cfg+cnf+cnf_template; rpq: regex+rsa;
mcfpq: mcfg). Top-level `__init__.py`: `grammars` -> `queries`. Fix the two
cross-imports and any doctests that name module paths.
**Tests:** mirror the move: `tests/grammars/{generators,converters,utils}` ->
`tests/queries/cfpq/...`, `tests/grammars/readwrite/test_{cfg,cnf,cnf_template}.py`
-> `tests/queries/cfpq/readwrite/`, `test_{regex,rsa}_readwrite.py` ->
`tests/queries/rpq/readwrite/`, `test_mcfg_readwrite.py` ->
`tests/queries/mcfpq/readwrite/`; fix imports.
**Docs:** restructure `docs/reference/grammars/` ->
`docs/reference/queries/{cfpq,rpq,mcfpq}/`: rename the autosummary stubs to
the new module paths (`automodule:: cfpq_data.queries.<class>....`), regroup
the four summary pages per class, update `docs/reference/index.rst`.

**Spec:**
- The flat top-level API is preserved: `from cfpq_data import *` still exposes
  every function (star-import chain through `queries/__init__.py`).
- No function names change in this subtask — only module paths.

### S2: Rename the package cfpq_data -> flpq_data [done] b828e58

**Code:** `git mv cfpq_data flpq_data`; update every import (package doctests,
tests, the three utils scripts); `pyproject.toml` (`name = "flpq-data"`,
`packages = ["flpq_data"]`, coverage source, `testpaths`, keywords);
`.gitignore` (`cfpq_data/data` -> `flpq_data/data`);
`.github/workflows/coverage.yml` (`--cov=flpq_data`); the package docstring in
`flpq_data/__init__.py`.
**Tests:** mechanical import update across `tests/` (incl.
`tests/test_py_typed.py`).
**Docs:** every remaining `cfpq_data` mention under `docs/`: reference stubs
(dataset/graphs), `docs/conf.py`, the per-graph load snippets, tutorial, about,
developer guide; the "Until the rename happens" paragraph of `docs/flpq.rst`
is now stale — rewrite it to state the rename has happened.

**Spec:**
- The PyPI distribution name becomes `flpq-data`; the repo/site project name
  stays CFPQ_Data (the site restructure is task 50).

### S3: API renames with deprecated aliases [done] 7456898

**Code:** `flpq_data/dataset/data.py`: `download` -> `download_graph`
(docstring + doctest updated), `DATASET` -> `GRAPHS`; keep `download` as a
wrapper that emits `DeprecationWarning` and delegates to `download_graph`, and
`DATASET = GRAPHS` as a documented alias (a plain constant — no runtime
warning, since a PEP 562 `__getattr__` would fire during the package's own
star import); update `__all__`.
**Tests:** `tests/dataset/test_data.py` switches to `GRAPHS`; new tests:
`download_graph` is the implementation name, the deprecated `download` emits
`DeprecationWarning` and returns the same result, `DATASET is GRAPHS`.
**Docs:** dataset reference stubs renamed to `flpq_data.dataset.GRAPHS.rst` /
`flpq_data.dataset.download_graph.rst`; `docs/reference/dataset/index.rst`
autosummary updated.

**Spec:**
- Importing the package must not emit any warning (warnings only on calling
  the deprecated function).

### S4: Bump VERSION to 6.0.0 and record the rename in the changelog [done] a901566

**Code:** `config.py` `VERSION = "6.0.0"` + `pyproject.toml` `version =
"6.0.0"` (the version-sync guard must pass); `DATASET_KEY_PREFIX` then
derives `6.0.0/graph` and `DATASET_URL` re-points automatically.
**Tests:** the `download_graph` doctest now fetches from `6.0.0/graph/`
(verified to exist for all 113 archives); version-sync pre-commit hook green.
**Docs:** CHANGELOG `[Unreleased]`: a Changed entry (package renamed to
`flpq_data`, distribution `flpq-data`, `grammars/` restructured into
`queries/{cfpq,rpq,mcfpq}/`, `DATASET_URL` now serves the 6.0.0 prefix) and a
Deprecated entry (`download` / `DATASET` aliases for `download_graph` /
`GRAPHS`).

### S5: Update README, AGENTS.md, and the skills [pending]

**Code:** none (meta files only)
**Tests:** skip (no code); docs build green
**Docs:** `README.rst` (install/import examples), `AGENTS.md` ("Package
layout"), `.opencode/skills/{run-tests,add-graph,add-grammar,planning,reusing,
release}/SKILL.md`, and any remaining `cfpq_data`/`cfpq-data` mentions in
tracked meta files.

**Spec:**
- Skills stay thin pointers — update paths/names only, no re-description.
- `tasks/tasks.md` is archived history: untouched.
