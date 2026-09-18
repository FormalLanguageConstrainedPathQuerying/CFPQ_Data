# Global Plan: FLPQ extension (tasks 42-49)

Extending CFPQ_Data from context-free path queries to all classes of
formal-language-constrained path querying (FLPQ): regular (RPQ),
context-free (CFPQ, existing), and multiple context-free (MCFPQ). Design
decisions live in `docs/flpq.rst` (task 42) — the single source of truth
for all follow-up tasks.

## Tasks

- **Task 42** [in progress]: FLPQ design document (`docs/flpq.rst`): query-
  class taxonomy, MCFG formalism (Seki d-MCFG(r)) + `.mcfg` Datalog-like
  format spec (lark parser), target site/package/dataset structure,
  reachable-pairs rendering design, migration path.
- **Task 43**: Refactor the reachable-pairs representation on the site:
  per-category tables in `docs/reachable_pairs.rst` (the flat table is
  removed), the CSV stays the single source of truth for automatic
  processing and gains a `category` column, and a `utils/` generator script
  (pattern of `utils/archive_sizes.py`) renders both the per-category
  tables and the category-page count columns from the CSV.
- **Task 44**: MCFG readwrite module with lark:
  `cfpq_data/grammars/readwrite/mcfg.py` (data model, EBNF grammar,
  validation per the spec in `docs/flpq.rst`,
  `mcfg_from_text/to_text/from_txt/to_txt`), doctests with the paper's
  examples, reference docs page.
- **Task 45**: RPQ query templates + seed data: first-class RPQ content —
  regex template entries in the existing Grammars section (Class = Regular)
  plus example archives, until the site restructure of task 49 moves them
  to the RPQ section.
- **Task 46**: Add a `query_class` column to `reachable_pairs.csv` and the
  `reachable_pairs()` API (+ update the generator from task 43).
- **Task 47**: S3 6.0.0 layout migration + upload tools: copy graph
  archives to `6.0.0/graph/`, move grammar archives to
  `6.0.0/query/cfpq/`, benchmarks to `6.0.0/benchmark/<class>/`; the
  `utils/` upload tools gain the class-aware key layout.
- **Task 48**: Package rename/restructure to `flpq_data`:
  `queries/{cfpq,rpq,mcfpq}`, API renames + deprecated aliases, `cfpq-data`
  deprecation shim, VERSION 6.0.0, re-pointed
  `DATASET_URL`/`GRAMMARS_URL`/`BENCHMARK_URL`.
- **Task 49**: Site restructure to the FLPQ hierarchy: per-class sections
  (CFPQ/RPQ/MCFPQ) with templates/benchmarks/applicable graphs, the shared
  Graphs section, navigation.

## Dependencies

- 43 and 44 are independent of each other (both after 42).
- 46 is after 43 (the generator must exist to extend).
- 47 is after 45 (all query data classes in place before the migration).
- 48 is after 47 (the download machinery points at the new layout).
- 49 is after 48 (the site references the final package structure).

## Notes

- **No release task is planned** — user instruction: "Do not plan 6.0
  release as a task. We must do much more tasks first." The 6.0.0 version
  bump happens inside task 48; cutting the release is deferred.
- Incremental tasks (43, 44) deliberately avoid any global rework: they
  work inside the existing `cfpq_data` package and site structure.
