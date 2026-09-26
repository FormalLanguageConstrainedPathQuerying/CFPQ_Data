# Detailed Plan: Issue #132 — Complete the [Unreleased] section of CHANGELOG.md

## Context

The `[Unreleased]` section of `CHANGELOG.md` lags behind dev: user-visible
changes that landed after v5.0.0 (2026-09-16) are not recorded. The issue
lists six entries to add, each of which was verified against the commits and
current state on dev before being written (the "do not claim anything that
has not landed" rule). Nothing in the current `[Unreleased]` section
duplicates these entries.

Verification evidence (all on dev):

1. **MCFG module** — `cfpq_data/grammars/readwrite/mcfg.py` exists;
   `__all__ = [MCFG, MCFGRule, mcfg_from_text, mcfg_from_txt, mcfg_to_text,
   mcfg_to_txt]`; `lark>=1.3.1,<2.0.0` is a dependency in `pyproject.toml`;
   documented in the reference docs (44-S5).
2. **reachable_pairs columns + API** — `cfpq_data/dataset/reachable_pairs.csv`
   header is `graph,grammar,category,query_class,num_reachable_pairs`;
   `reachable_pairs()` takes `category` and `query_class` filters and returns
   rows with those keys (43-S2, 47-S2/S3).
3. **RSM transition-system style** — `cfpq_data/grammars/readwrite/rsa.py`
   parses the transition-system style (`_rsa_from_transition_system`); the
   format and extended archive structure are documented (54-S2/S4).
4. **Partial archives** — `utils/check_archive_structure.py` has a
   `--partial` mode; `utils/merge_archive.py` merges a partial archive into an
   existing one (55-S2/S3).
5. **6.0.0 self-contained layout** — the dataset on S3 is at the
   `6.0.0/graph/` prefix (verified in the consistency audit); the "File
   structure" section of `docs/graphs/index.rst` documents the
   `queries/<class>/<query>/` layout; the site links were re-pointed to it in
   #133.
6. **Removed download APIs** — `download_grammars` / `download_benchmark` are
   absent from `cfpq_data/`, `tests/`, and the docs (the only remaining mention
   is a forward-looking note in the `docs/flpq.rst` design doc, which the issue
   says stays); the separate `grammar/` and `benchmark/` S3 paths were removed
   in 48-S6.

## Subtasks

### S1: Add the four "Added" entries [done] b9dfce3

**Code:** none (changelog only)
**Tests:** skip (no code); docs build green (the changelog is not built by
Sphinx, so this is a formality — run it as part of the gate)
**Docs:** `CHANGELOG.md` — the `### Added` section of `[Unreleased]`

**Spec:**
- Append four bullets to `### Added`, in Keep a Changelog style matching the
  existing entries (imperative, specific, naming the module/column/format):
  - the MCFG readwrite module (`cfpq_data/grammars/readwrite/mcfg.py`): data
    model, lark-based EBNF parsing, validation, `mcfg_from_text` /
    `mcfg_to_text` and the `*_from_txt` / `*_to_txt` file helpers;
  - the `category` and `query_class` columns of `reachable_pairs.csv` and the
    matching filters/fields of the `reachable_pairs()` API;
  - the transition-system description style of the `.rsm` format (a query may
    be a CFG and/or an explicit labelled transition system);
  - partial-archive validation (`--partial`) and `utils/merge_archive.py` for
    merging new queries into an existing graph archive.

### S2: Add the "Changed" and "Removed" entries [done] 776bb34

**Code:** none (changelog only)
**Tests:** skip (no code)
**Docs:** `CHANGELOG.md` — the `### Changed` and `### Removed` sections of
  `[Unreleased]`

**Spec:**
- Append one bullet to `### Changed`: the dataset on object storage moved to
  the 6.0.0 self-contained archive layout — each graph archive carries its
  queries under `queries/<class>/<query>/` (representations + one
  `results.mtx`) instead of a separate top-level `grammar/` directory.
- Append one bullet to `### Removed`: `download_grammars()` and
  `download_benchmark()`; the separate `grammar/` and `benchmark/` S3 paths
  were removed from the bucket, the docs, and the package. Note that benchmark
  data is set aside for now and gets its own rework (#129).
