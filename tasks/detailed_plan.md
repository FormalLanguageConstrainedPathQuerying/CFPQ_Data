# Detailed Plan: Task 50 (#137) — Restructure the site to the FLPQ hierarchy

Task issue: **#137** (Task 50). Also resolves **#129** (Task 53, benchmark
rework): the benchmark page/category is removed, per user guidance.
Branch: `feature/137-flpq-site-restructure`.

## Context

The FLPQ design (`docs/flpq.rst`, "Site structure") replaces the flat
`Grammars` section with one section per query class under the shared `Dataset`
page, reusing the existing per-class layout:

```text
Dataset
├── Graphs           shared catalog (8 categories, 113 pages) — unchanged
├── CFPQ             grammar templates (4 + indexed grammars) | applicable graphs
├── RPQ              query templates (regular expressions)    | applicable graphs
├── MCFPQ            grammar templates (MCFG)                 | applicable graphs
└── Reachable pairs  per-category tables; flat CSV download
```

Package rename (#135) and the 6.0.0 dataset alignment (#133) are done. The
site still has the flat `docs/grammars/` section and no per-class sections.

User guidance (verbatim): "Benchmark page must be removed
(https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/issues/129)
No separated categoey "benchmarks". You can complete this too if it is aligned
with issue 137 site restructuring." Therefore the design's `benchmarks`
placeholder pages are **not** created; the benchmark category is dropped from
the design doc and the changelog.

## Reuse

- `utils/reachable_pairs_tables.py` — `load_rows`, `category_order`,
  `toctree_entries`, `page_to_graph`, `graph_to_category`, `_section_title`,
  `_validation_problems`, marker-region update pattern; imported by the new
  generator and by `merge_archive`.
- `tests/utils/test_reachable_pairs_tables.py` — test/fixture patterns and the
  real-repo check-mode test to mirror.
- Existing template anchors (`c_alias`, `dyck`, `java_points-to`,
  `nested_parentheses`, `reachability`, `label_star`) and references from
  `docs/graphs/*.rst` / `docs/old_graphs/*.rst` / `docs/tutorial.rst` are
  preserved by moving (not rewriting) the pages.
- `utils/check_archive_structure.py` — `QUERY_CLASSES` (class directory names)
  and archive layout remain the source of truth.

## Design decisions

1. **Class section layout.** Each class gets `docs/queries/<cls>/index.rst`
   (title `CFPQ`/`RPQ`/`MCFPQ`) with the template list-table, a hidden glob
   toctree over `data/*`, and an "Applicable graphs" section. CFPQ additionally
   moves `docs/indexed_grammars.rst` to `docs/queries/cfpq/indexed_grammars.rst`.
   RPQ moves its two regular template pages. MCFPQ has no templates yet
   (arrive with data).
2. **No benchmarks.** No benchmark placeholder pages and no `benchmarks`
   category anywhere. #129 is resolved by removal, not by rework.
3. **Applicable graphs are generated.** A new `utils/applicable_graphs.py`
   renders the per-class "Applicable graphs" sections from
   `flpq_data/dataset/reachable_pairs.csv` (the registry: one row per
   applicable graph×query pair) between the markers
   `.. applicable-graphs:begin` / `.. applicable-graphs:end`, grouped by graph
   category and cross-linking the shared per-graph pages (`:ref:<page>`); no
   graph page is duplicated. It follows the `reachable_pairs_tables.py`
   pattern (check mode default, `--update`, real-repo check-mode test) and
   reuses its helpers.
4. **Registry cannot drift.** `utils/merge_archive.py` requires a CSV row for
   every new query directory it merges: `graph` = the archive's graph,
   `query_class` = the class directory, and `Path(grammar).stem` = the query
   directory name. The registry path is a module constant so tests can inject
   a fixture CSV.
5. **How to add a new grammar** moves to the Dataset page; `navigation_depth
   = 3` already accommodates section → class → template.

## Subtasks

### S1: Restructure the dataset docs into per-class query sections [done] (35513a7)

**Code:** none (docs only).
**Tests:** docs build (`make -C docs html`, part of the gate); no unit tests.
**Docs:**
- new `docs/queries/cfpq/index.rst`, `docs/queries/rpq/index.rst`,
  `docs/queries/mcfpq/index.rst`;
- move `docs/grammars/data/{c_alias,dyck,java_points_to,nested_parentheses}.rst`
  → `docs/queries/cfpq/data/`;
- move `docs/grammars/data/{reachability,label_star}.rst`
  → `docs/queries/rpq/data/`;
- move `docs/indexed_grammars.rst` → `docs/queries/cfpq/indexed_grammars.rst`;
- delete `docs/grammars/`;
- `docs/dataset.rst` — new toctree entries + "How to add a new grammar?"
  pointer moved here from `docs/grammars/index.rst`;
- `docs/tutorial.rst:111` — `:ref:`grammar_templates`` →
  `:ref:`cfpq_queries``;
- `docs/flpq.rst:50,74` — `grammar_templates` refs → `cfpq_queries` /
  `rpq_queries`.

**Spec:**
- Each class index: anchor `_cfpq_queries`/`_rpq_queries`/`_mcfpq_queries`;
  `.. only:: html` release block; one-paragraph class description; a hidden
  `:glob:` toctree over `data/*` (cfpq also `indexed_grammars`); a "Grammar
  templates" list-table (all four context-free templates for CFPQ, both
  regular templates for RPQ, a "templates arrive with data" note for MCFPQ);
  and an "Applicable graphs" section delimited by the `applicable-graphs`
  markers with a one-line placeholder (filled by S2).
- `docs/dataset.rst` toctree becomes: `graphs/index`, `queries/cfpq/index`,
  `queries/rpq/index`, `queries/mcfpq/index`, `reachable_pairs`; keep the
  existing intro, append the "How to add a new grammar?" section with the PR
  template link from `docs/grammars/index.rst`.
- The moved pages keep their anchors and content unchanged, so every
  `:ref:` to a template keeps resolving.

### S2: Generate the per-class applicable-graphs lists from the CSV [done] (5869cdc)

**Code:** new `utils/applicable_graphs.py`; reuse `load_rows`, `category_order`,
`page_to_graph`, `graph_to_category`, `_section_title`, `_validation_problems`
from `reachable_pairs_tables`.
**Tests:** new `tests/utils/test_applicable_graphs.py` (render per class, empty
class, marker round-trip, unknown-graph validation, real-repo check mode).
**Docs:** `docs/utils.rst` — new "Applicable graphs" section; fill the three
class index regions.

**Spec:**
- CLI `python utils/applicable_graphs.py [--update]`; check mode (default)
  exits 1 on any drift and prints the drifted pages; `--update` rewrites.
- Class → page map: `{cfpq: docs/queries/cfpq/index.rst, rpq: …, mcfpq: …}`.
- For each class, take its CSV rows, collect distinct graphs, map each to its
  shared page via the inverse of `page_to_graph`, group by `category_order`
  (category title from `_section_title`), and render, per category, a
  `^^^^` subsection with a sorted bullet list of `:ref:`<page>``. An empty
  class renders a single sentence ("No `<class>` queries have been added to
  the graph catalog yet."). Output is deterministic.
- Validate the CSV with `_validation_problems(rows, graph_to_category(docs))`
  before any update (all-or-nothing), like `reachable_pairs_tables.py`.
- Marker region replaced by the shared two-marker update helper; idempotent.

### S3: Enforce the CSV registry when merging partial archives

**Code:** `utils/merge_archive.py` — add `REGISTRY_CSV` constant and a registry
check for every new query directory.
**Tests:** `tests/utils/test_merge_archive.py` — autouse fixture injecting a
fixture CSV; cases for a registered new query (pass), an unregistered one
(problem), and a class mismatch (problem).
**Docs:** `docs/utils.rst` — note the registry check in the "Merge partial
archives" section.

**Spec:**
- `REGISTRY_CSV = MAIN_FOLDER / "flpq_data" / "dataset" / "reachable_pairs.csv"`
  (import `MAIN_FOLDER` from `config`); read rows with `load_rows`.
- After the collision/name checks, when the merge is otherwise viable, for
  each new `(cls, query_dir)` require a row with `graph == existing_root.name`,
  `query_class == cls`, and `pathlib.Path(row["grammar"]).stem == query_dir.name`.
  Report `queries/<cls>/<name>: no flpq_data/dataset/reachable_pairs.csv row
  for graph '<graph>' (query_class <cls>)` and abort the merge.
- Add a `test_merge.py`-style autouse fixture that monkeypatches
  `merge_archive.REGISTRY_CSV` to a tmp CSV so the existing graph `g` /
  query `t` fixtures remain valid.

### S4: Design doc + changelog: drop benchmarks, reflect the site hierarchy

**Code:** none (docs/process only).
**Tests:** none (docs build is the gate).
**Docs:** `docs/flpq.rst` (Site structure + Dataset layout/migration),
`CHANGELOG.md` `[Unreleased]`, `tasks/global_plan.md`.

**Spec:**
- `docs/flpq.rst` Site structure: remove `| benchmarks` from all three class
  lines; describe the CFPQ/RPQ/MCFPQ sections and the generated applicable
  graphs; state explicitly that there is no separate benchmarks section.
- `docs/flpq.rst` Dataset layout: drop the `benchmark/<class>/<name>.tar.gz`
  line; migration path drops `BENCHMARK_URL`.
- `CHANGELOG.md` `[Unreleased]`: under Added/Changed, record the per-class
  query sections and the generated applicable-graphs lists; under Removed,
  record that the benchmark page/category was removed (#129); update the
  existing `#129` reference from "gets its own rework" to removed.
- `tasks/global_plan.md`: mark Task 50 (#137) and Task 53 (#129) done with a
  one-line note.
- Last commit carries `Closes #137` and `Closes #129` as standalone lines.
