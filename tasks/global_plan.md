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
- **Task 46** [done]: RPQ design decision + stubs: document the RPQ query-class
  design in `docs/flpq.rst` (format, parameterized regex templates, placement
  inside self-contained graph archives) and add stub template entries
  (Class = Regular) to the existing Grammars section, until the site
  restructure of task 50 moves them to the RPQ section. No real-world RPQ
  data yet — it will be provided later (user decision).
- **Task 47** [done]: Add a `query_class` column to `reachable_pairs.csv` and the
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
- **Task 54** [done]: Extend the archive structure — several ways to specify one
  language: a query may be specified by different grammars; for CFPQ, by a
  CFG or an RSM (recursive state machine), described either in an EBNF-based
  text format or as an explicit transition system (labelled graph with start
  and final states). Each query carries one results file — a Boolean MTX of
  constrained-reachability facts — identical for all its specifications.
  Investigate RSMs first; design documents + tooling only, no re-upload.
 - **Task 55** [done]: Improve the new-data providing mechanism — the main
   way is a Google Drive link to an archive prepared per the structure-
   validation tool; partial archives are allowed (e.g. a new query for an
   existing graph: query representation + references — pair count, results
   MTX — + README descriptions), with the structure preserved so new data
   merges into the existing archive. Issue/PR templates make this way the
   main one and point at the tooling; extend the tooling if necessary.

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
- 48 is after 46, 52, 54 and 55 (all query data classes in place, the
  migration repackages archives into the final extended structure, and the
  providing mechanism is settled).
- 49 is after 48 and 52 (the download machinery points at the new layout and
  reflects self-contained archives).
- 50 is after 49 (the site references the final package structure).
- 53 is after 50 and 52 (benchmarks are redesigned on top of the final site
  hierarchy and the self-contained archive structure).
- 54 is after 52 (it extends the self-contained archive structure).
- 55 is after 54 (partial archives follow the extended structure, including
  the per-query results files).

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
- **Task 54 extends the task-52 archive structure**: a query is no longer a
  flat file but a directory `queries/<class>/<query>/` holding every
  representation of the language (`.cnf`/`.rsm` for CFPQ, `.re`/`.rsm` for
  RPQ — regular only, `.mcfg` for MCFPQ) plus one representation-independent
  `results.mtx` (Boolean MTX of constrained reachability facts). The RSM
  readwrite (`rsa.py`) and the `cfg_from_rsa` converter already existed and
  are reused; task 54 adds the transition-system description style to the
  `.rsm` format. Existing archives keep the old layout until the migration
  (task 48) repackages them.
- **Task 55 makes the Google Drive link the main data-providing way**: a
  provider shares a Drive link to `<name>.tar.gz` in the issue/PR; the
  archive is either full (a new graph) or partial (new queries for an
  existing graph — only `queries/`: the new query directories plus a
  `README.md` fragment with their sections). The validator gains a
  `--partial` mode (structure + parse checks; label/dimension checks run
  after the merge), and `utils/merge_archive.py` merges a partial archive
  into the existing one (collision checks, README section append, full
   re-validation, Drive-URL input). The reachable-pair count of a new query
   is the number of entries in its `results.mtx` — no separate reference.

## Consistency fixes (issues 131–134)

A consistency audit (dataset on S3 = source of truth) found the site
mid-migration: it describes the 6.0.0 self-contained layout while linking and
serving 5.0.0 artifacts, one grammar page disagrees with its archive, and the
changelog lags behind dev. User decisions: work #131 on the existing issue
(no new one); dev targets v6.0, so all links/references must be consistent
with the 6.0.0 dataset — preparation only, no version bump (that is task 49);
benchmark page related stuff stays removed from dev.

- **#131** [bug]: the FSA canonical grammar on `docs/graphs/field_sensitive_alias.rst`
  does not match the distributed `vf.cnf`/`vf.rsm`: the docs' `a` part
  (`V → A V A | a_r V a`, `A → a M? | ε`) defines a different language than
  the archive's (`V → A_r V | V A`, `A_r → M a_r | a_r | ε`,
  `A → a M | a | ε`). Fix the docs to match the dataset.
- **#132**: complete the `[Unreleased]` section of CHANGELOG.md with the
  post-5.0.0 changes (MCFG module, CSV columns, RSM transition-system style,
  partial archives/merge tooling, 6.0.0 dataset migration, removal of
  download_grammars/download_benchmark).
- **#133**: align the site with the 6.0.0 dataset — re-point all download
  links to `6.0.0/graph/`, refresh `Size (MB)` via `utils/archive_sizes.py`,
  update `docs/utils.rst` prefix references, fix the stale package-layout
  line in AGENTS.md; no benchmark page re-introduction.
- **#134**: remove untracked scratch files (`endpoints`, `test.csv`) and
  gitignore `test.csv`.

### Dependencies

- All four are independent of each other (disjoint file sets, except #132
  and #133 both touch the changelog/docs narrative — #133 first so #132 can
  also record the re-pointing if desired; kept separate to stay atomic).
- Execution order: #131 → #133 → #132 → #134.
