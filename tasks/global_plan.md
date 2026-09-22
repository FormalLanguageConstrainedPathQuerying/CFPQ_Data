# Global Plan: FLPQ extension (tasks 42-50)

Extending CFPQ_Data from context-free path queries to all classes of
formal-language-constrained path querying (FLPQ): regular (RPQ),
context-free (CFPQ, existing), and multiple context-free (MCFPQ). Design
decisions live in `docs/flpq.rst` (task 42) — the single source of truth
for all follow-up tasks.

## Tasks

- **Task 42** [done]: FLPQ design document (`docs/flpq.rst`): query-
  class taxonomy, MCFG formalism (Seki d-MCFG(r)) + `.mcfg` Datalog-like
  format spec (lark parser), target site/package/dataset structure,
  reachable-pairs rendering design, migration path.
- **Task 43** [done]: Refactor the reachable-pairs representation on the site:
  per-category tables in `docs/reachable_pairs.rst` (the flat table is
  removed), the CSV stays the single source of truth for automatic
  processing and gains a `category` column, and a `utils/` generator script
  (pattern of `utils/archive_sizes.py`) renders both the per-category
  tables and the category-page count columns from the CSV.
- **Task 44** [done]: MCFG readwrite module with lark:
  `cfpq_data/grammars/readwrite/mcfg.py` (data model, EBNF grammar,
  validation per the spec in `docs/flpq.rst`,
  `mcfg_from_text/to_text/from_txt/to_txt`), doctests with the paper's
  examples, reference docs page.
- **Task 45** [done]: Strong code coverage gate + tooling cleanup: enforce line
  and branch coverage >= 95% both in CI (`coverage.yml`) and locally
  (canonical test command), remove the curl/GitHub-API workaround from the
  release skill now that the `gh` CLI is installed, and extend the project
  tooling guidance with a no-workaround rule.
- **Task 46**: RPQ design decision + stubs: document the RPQ query-class
  design in `docs/flpq.rst` (format, parameterized regex templates, placement
  inside self-contained graph archives) and add stub template entries
  (Class = Regular) to the existing Grammars section, until the site
  restructure of task 50 moves them to the RPQ section. No real-world RPQ
  data yet — it will be provided later (user decision).
- **Task 47**: Add a `query_class` column to `reachable_pairs.csv` and the
  `reachable_pairs()` API (+ update the generator from task 43).
- **Task 48**: S3 6.0.0 layout migration + upload tools: copy graph
  archives to `6.0.0/graph/`, move grammar archives to
  `6.0.0/query/cfpq/`, benchmarks to `6.0.0/benchmark/<class>/`; the
  `utils/` upload tools gain the class-aware key layout.
- **Task 49**: Package rename/restructure to `flpq_data`:
  `queries/{cfpq,rpq,mcfpq}`, API renames + deprecated aliases, `cfpq-data`
  deprecation shim, VERSION 6.0.0, re-pointed
  `DATASET_URL`/`GRAMMARS_URL`/`BENCHMARK_URL`.
- **Task 50**: Site restructure to the FLPQ hierarchy: per-class sections
  (CFPQ/RPQ/MCFPQ) with templates/benchmarks/applicable graphs, the shared
  Graphs section, navigation.
- **Task 51** [done]: CI as source of truth for commands: analyze which developer-
  docs and skill content can be replaced with references to the CI workflow
  descriptions; record the per-command decision in the docs; apply it —
  command blocks become references to the workflow file + step, local-only
  commands and policies stay in the docs, and the duplicated CI comments are
  slimmed to pointers.
- **Task 52** [done]: Self-contained archive structure + validation: design the
  identical, self-contained graph-archive layout (graph as a set of MTX
  files, a description document with mandatory questions, all queries as
  separate files described in one common document), the `utils/`
  structure-validation tool, pre-upload validation in `utils/upload_to_s3.py`
  plus an audit mode over the bucket, and rework `docs/flpq.rst` (dataset
  layout, migration, API) to match. Scope: graph archives only — example
  queries not tied to a graph are dropped, benchmark data is out of scope
  (task 53).
- **Task 53**: Rework the benchmark page and the respective benchmark data
  (design comes after the archive structure of task 52 and the site
  restructure of task 50).

## Dependencies

- 43 and 44 are independent of each other (both after 42).
- 45 is independent of the FLPQ tasks (CI/tooling/docs only); scheduled
  right after 44.
- 51 is independent of the FLPQ tasks (process/docs/CI only); scheduled
  right after 45.
- 52 is after 51 (the new upload workflow follows the CI-source-of-truth
  principle).
- 46 is after 52 (new query data must follow the new archive structure).
- 47 is after 43 (the generator must exist to extend).
- 48 is after 46 and 52 (all query data classes in place, and the migration
  repackages archives into the new structure instead of copying them).
- 49 is after 48 and 52 (the download machinery points at the new layout and
  reflects self-contained archives).
- 50 is after 49 (the site references the final package structure).
- 53 is after 50 and 52 (benchmarks are redesigned on top of the final site
  hierarchy and the self-contained archive structure).

## Notes

- **No release task is planned** — user instruction: "Do not plan 6.0
  release as a task. We must do much more tasks first." The 6.0.0 version
  bump happens inside task 49; cutting the release is deferred.
- Incremental tasks (43, 44) deliberately avoid any global rework: they
  work inside the existing `cfpq_data` package and site structure.
- Task 52 supersedes part of the `docs/flpq.rst` dataset design: the
  separate per-query archives (`query/<class>/<template>[_<graph>].tar.gz`)
  are replaced by self-contained graph archives that carry their queries;
  the example query archives (`example/<template>.tar.gz`) are dropped —
  every query file lives inside a graph archive (user decision); the
  migration (task 48) repackages existing archives instead of copying them
  unchanged.
- **Task 46 is design-only**: there is no real-world RPQ data yet — the task
  documents the RPQ design decision and adds stub template entries to the
  Grammars section; real `.re` query files will be provided later and live
  inside graph archives (task 52 structure).
