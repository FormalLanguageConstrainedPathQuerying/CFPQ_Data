# Detailed Plan: Issue #137 — Restructure the site to the FLPQ hierarchy (per-class query sections)

## Context

The site step of the FLPQ extension (design source of truth:
`docs/flpq.rst`, "Site structure"). The package is already `flpq_data` with
`queries/{cfpq,rpq,mcfpq}/` (#135), the dataset lives at `6.0.0/graph/`
(task 48), and the site links/sizes already point there (#133). This task
restructures the Dataset section of the site into the per-class hierarchy:

```text
Dataset
├── Graphs           shared catalog (8 categories, 113 pages) — unchanged
├── CFPQ             grammar templates (4 + indexed grammars) | benchmarks | applicable graphs
├── RPQ              query templates (regular expressions)    | benchmarks | applicable graphs
├── MCFPQ            grammar templates (MCFG)                 | benchmarks | applicable graphs
└── Reachable pairs  per-category tables; flat CSV download
```

Current state: the top-level "Grammars" page (`docs/grammars/index.rst`)
holds one template table with a Class column (4 Context-Free + 2 Regular
rows) and six template pages under `docs/grammars/data/`;
`docs/indexed_grammars.rst` is CFPQ-specific; the reachable-pairs page is
already final (tasks 43/47).

User decision: the per-class "applicable graphs" lists are rendered from
`flpq_data/dataset/reachable_pairs.csv` — the registry where one row exists
per applicable graph×query pair (155 cfpq rows covering all 113 graphs;
rpq/mcfpq rows arrive with data) — following the
`utils/reachable_pairs_tables.py` pattern; `utils/merge_archive.py` requires
a CSV row for every new query directory so the registry cannot drift.

## Subtasks

### S1: Per-class section skeleton (move pages, class indexes, benchmarks placeholders) [pending]

**Code:** none (docs only)
**Tests:** skip (no code); docs build green
**Docs:**
- New `docs/queries/cfpq/index.rst` — "CFPQ" page: intro, template table
  (the 4 CFPQ templates), toctree (`data/*`, `indexed_grammars`,
  `benchmarks`).
- New `docs/queries/rpq/index.rst` — "RPQ" page: intro, template table
  (reachability, label_star), toctree (`data/*`, `benchmarks`).
- New `docs/queries/mcfpq/index.rst` — "MCFPQ" page: note that MCFG
  templates arrive with data (the `.mcfg` format is documented in the
  reference), toctree (`benchmarks`).
- Move `docs/grammars/data/{c_alias,dyck,java_points_to,nested_parentheses}.rst`
  → `docs/queries/cfpq/data/`;
  `{reachability,label_star}.rst` → `docs/queries/rpq/data/`.
- Move `docs/indexed_grammars.rst` → `docs/queries/cfpq/indexed_grammars.rst`.
- New benchmarks placeholder pages `docs/queries/{cfpq,rpq,mcfpq}/benchmarks.rst`.
- `docs/dataset.rst`: toctree becomes `graphs/index`,
  `queries/cfpq/index`, `queries/rpq/index`, `queries/mcfpq/index`,
  `reachable_pairs`; the "How to add a new grammar?" pointer moves here;
  intro wording updated (Context-Free Path Querying → formal-language
  queries).
- Delete `docs/grammars/`.
- Cross-references: `docs/tutorial.rst` ("described on the
  :ref:`grammar_templates` page" → the CFPQ page); `docs/flpq.rst` (the two
  `:ref:`grammar templates <grammar_templates>`` references → the per-class
  sections).

**Spec:**
- Page labels are preserved by the moves (`c_alias`, `dyck`,
  `java_points-to`, `nested_parentheses`, `reachability`, `label_star`,
  `indexed_grammars`) so every existing `:ref:` target keeps working; the
  `grammar_templates` label dies with the old page and its three references
  are updated.
- The class-level template tables drop the now-redundant Class column
  (every row in a section is that class); the per-page Info tables stay
  unchanged.
- The MCFPQ index carries no template entries yet — a documented placeholder
  pointing at the `.mcfg` reference page, not an empty table.
- The benchmarks placeholder pages state that benchmark data arrives with
  the benchmark rework (#129); they are linked from each class toctree so
  the section -> class -> page depth is exercised.
- `navigation_depth = 3` in `docs/conf.py` already accommodates
  section -> class -> template: no conf change.

### S2: Applicable-graphs generator from reachable_pairs.csv [pending]

**Code:** New `utils/applicable_graphs.py` — reuses `load_rows`,
`page_to_graph`, `graph_to_category`, `category_order` from
`utils/reachable_pairs_tables.py` and `QUERY_CLASSES` from
`utils/check_archive_structure.py`. Also: the stale "until the per-class
sections exist (task 50)" note in the `reachable_pairs_tables.py` docstring
is updated (other classes are rendered on the class pages by this tool).
**Tests:** New `tests/utils/test_applicable_graphs.py` — rendering for a
class with rows (cfpq: distinct graphs, category order, graph-page links),
an empty class (rpq/mcfpq → "no queries yet" line), check mode exits
non-zero on drift, `--update` rewrites the region; reuse the tmp docs-tree
fixture pattern of `tests/utils/test_reachable_pairs_tables.py`.
**Docs:** Marked regions on the three class index pages (rendered by
`--update`); a new section in `docs/utils.rst` following the
reachable-pairs section.

**Spec:**
- One list-table per class page between
  `.. applicable-graphs:<class>:begin` / `:end` markers (plain reST
  comments, same convention as `reachable-pairs-tables`): columns Graph
  (`:ref:` link to the shared graph page) and Category; rows are the
  distinct graphs with at least one CSV row of that query_class, sorted by
  category order then graph name.
- A class without rows renders a single italic "no queries yet" line, so
  the RPQ/MCFPQ pages stay clean before data arrives.
- Check mode (default) reports every region disagreeing with the CSV and
  exits non-zero (commit gate); `--update` rewrites the regions.
- The CSV stays the single source of truth: a row exists iff the query
  applies to the graph; this tool only renders, never edits the CSV.

### S3: merge_archive.py requires a CSV row for every new query [pending]

**Code:** `utils/merge_archive.py` — after resolving the partial archive and
before writing anything, verify that every `queries/<class>/<query>`
directory it would add has at least one `reachable_pairs.csv` row matching
(graph, query_class); a missing pair fails the merge with a message naming
the (graph, class) pairs and pointing at the CSV.
**Tests:** Extend `tests/utils/test_merge_archive.py` — a partial archive
with a new query directory and no CSV row fails the merge; the same archive
with the row present succeeds.
**Docs:** The merge-archive section of `docs/utils.rst` mentions the CSV-row
requirement.

**Spec:**
- The check runs before any file is written — the merge stays all-or-nothing
  (consistent with the existing collision/re-validation behavior).
- Matching is on (graph, query_class) only; which representation file name
  goes into the `grammar` column is the contributor's call.
- Existing rows for the graph are untouched; the tool never edits the CSV.
