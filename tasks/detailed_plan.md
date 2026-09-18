# Detailed Plan: Task 43 — Refactor the reachable-pairs representation on the site

Task (user's words, recorded in `tasks/tasks.md`): "One big flat table for
reachable pairs on the site looks ugly. One table may be usefulf to donload
for automatic processing, but it may be better to slit rendering on the sute
to several tables. Eg. per category."

Scope (per `docs/flpq.rst` "Reachable pair counts" and `tasks/global_plan.md`):
- `docs/reachable_pairs.rst`: the flat ~155-row table is removed; the page
  renders one small table per graph category (columns Graph | Grammar |
  Reachable pairs).
- The flat CSV stays the single source of truth for automatic processing and
  gains a `category` column so it is self-describing.
- A generator script in `utils/` (pattern of `utils/archive_sizes.py`) keeps
  both the per-category tables and the category-page count columns in sync
  with the CSV, so no count is hand-maintained in two places.

Verified facts this plan builds on (checked against the repo, 2026-09-18):
- The CSV has 155 rows / 113 unique graphs; 4 values are empty (libgdx,
  unigraph_8/9/10).
- The graph -> category mapping is NOT in the package (`DATASET` is a flat
  list); it lives in the site: each `docs/graphs/<category>.rst` toctree
  lists its `data/<page>` pages, and the archive name in each data page's
  Yandex download URL equals the CSV graph name exactly (all 113 verified;
  page titles are NOT reliable — `xz_field_sensitive_alias.rst` is titled
  "xz"). Category order = the toctree of `docs/graphs/index.rst`:
  c_alias_analysis, rdf, java_points_to, field_sensitive_alias,
  context_sensitive_data_flow, data_provenance, name_resolution,
  biological_uniprot. Row counts per category: 20/62/21/10/10/18/4/10 = 155.
- Category-page count columns (header -> CSV grammar file):
  c_alias_analysis: `c_alias` -> c_alias.cnf; rdf: `subClassOf` ->
  nested_parentheses_subClassOf.cnf, `subClassOf_type` ->
  nested_parentheses_subClassOf_type.cnf, `type` ->
  nested_parentheses_type.cnf, `broaderTransitive` ->
  nested_parentheses_broaderTransitive.cnf; java_points_to: `java_points_to`
  -> java_points_to.cnf; field_sensitive_alias: `aa` -> aa.cnf;
  context_sensitive_data_flow: `vf` -> vf.cnf; data_provenance:
  `prov_derivation` -> prov_derivation.cnf; name_resolution:
  `name_resolution` -> name_resolution.cnf; biological_uniprot: `grammar` ->
  per-graph `<graph>.cnf` (unigraph_1.cnf ... unigraph_10.cnf).
- Cell semantics on category pages (per docs/graphs/index.rst "Contents"):
  a number = the count; "not available" = in the CSV but not computed yet;
  empty cell = the grammar does not apply to that graph.
- `tests/utils/conftest.py` puts `utils/` on sys.path, so tests import the
  script's modules directly (pattern of `test_archive_sizes.py`).

### S1: Add the category column to the CSV and the API

**Code:** `cfpq_data/dataset/reachable_pairs.csv` — new column order
`graph,grammar,category,num_reachable_pairs`, all 155 rows filled with the
category derived from the site mapping above. `cfpq_data/dataset/
reachable_pairs.py` — each returned row gains the `category` key; a new
optional `category` filter parameter (exact match, like the existing ones);
docstring updated.
**Tests:** update `tests/dataset/test_reachable_pairs.py`: row keys are now
{graph, grammar, category, num_reachable_pairs}; every category is one of
the eight known stems; each graph maps to exactly one category across its
rows; per-category row counts (20/62/21/10/10/18/4/10); `category=` filter
works and composes with the other filters.
**Docs:** update the "Columns:" line of `docs/reachable_pairs.rst` to list
the new column.

**Spec:**
- Category values are the category page stems (e.g. `rdf`,
  `c_alias_analysis`) — the same identifiers the generator and the docs use.
- The CSV keeps one row per (graph, grammar) pair; sorting stays by graph
  then grammar (the current order).
- `reachable_pairs()` keeps its signature backward-compatible: the new
  parameter is optional with default None.

### S2: Add the utils/reachable_pairs_tables.py generator

**Code:** new file `utils/reachable_pairs_tables.py` following the structure
of `utils/archive_sizes.py` (module docstring with usage, `__all__`, data
classes where useful, numpydoc docstrings with Examples, check mode default
+ `--update`, exit code 0/1):
- `category_order(docs_dir)` — the ordered category stems from the toctree
  of `docs/graphs/index.rst`.
- `graph_to_category(docs_dir) -> dict[str, str]` — for each category page:
  parse its toctree (`data/<page>` entries), read the data page, take the
  archive name from the Yandex download URL (regex on
  `https://cfpq-data.storage.yandexcloud.net/<ver>/graph/<name>.tar.gz`);
  raise on a missing link or a graph appearing in two categories.
- `load_rows(csv_path) -> list[dict]` — the CSV rows with
  `num_reachable_pairs` as int or None.
- `render_tables_region(rows, docs_dir) -> str` — the RST between the
  markers: one section per category (in `category_order`, title = the
  category page's title line, `-` underline), each a list-table with header
  Graph | Grammar | Reachable pairs and that category's rows sorted by
  (graph, grammar); None renders as "not available".
- `update_reachable_pairs_page(text, region) -> tuple[str, int]` — replace
  the content between the marker lines `.. reachable-pairs-tables:begin` and
  `.. reachable-pairs-tables:end` (RST comments, invisible in the build);
  return (new_text, changed).
- `GRAMMAR_COLUMNS: dict[str, list[tuple[str, str | None]]]` — per category,
  the ordered (column header, grammar file) pairs; None means the per-graph
  `<graph>.cnf` (biological_uniprot's `grammar` column).
- `update_category_columns(text, rows, page_to_graph) -> tuple[str, int]` —
  for the category table in a single category page: for each row (matched by
  the `:ref:`<page>` cell via `page_to_graph`) and each count column, set
  the cell to the CSV value, "not available" when the row exists with no
  value, or empty (bare `-` line) when the grammar does not apply; lines
  that need no change keep their exact text.
- `main(argv)` — check mode: verify the reachable-pairs region equals the
  rendered one and every category-page count cell matches the CSV, reporting
  problems with file:line and exiting 1 on any; `--update`: rewrite both.

**Tests:** new `tests/utils/test_reachable_pairs_tables.py` (imports the
module directly, like `test_archive_sizes.py`):
- `graph_to_category` on a synthetic mini docs tree in tmp_path (two
  categories, archive-name extraction, duplicate-graph error).
- `render_tables_region`: section order/titles, row order, "not available"
  rendering.
- `update_reachable_pairs_page`: replaces the region, is idempotent (second
  run reports no change), errors clearly when the markers are missing.
- `update_category_columns`: number / "not available" / empty-cell
  semantics, row matching by page ref, unchanged lines keep exact text.
- Integration: running `main()` in check mode on the real repo exits 0
  (after S3 has generated the content; until then this test is added with
  the expectation set in S3 — see S3 spec).

**Spec:**
- The script reads the CSV from
  `MAIN_FOLDER / "cfpq_data" / "dataset" / "reachable_pairs.csv"` (no
  package import, consistent with the other utils scripts) and the docs from
  `MAIN_FOLDER / "docs"`.
- No network access: everything is local files.
- Idempotent by construction: check mode after --update must report zero
  problems.

### S3: Restructure docs/reachable_pairs.rst and sync the category pages

**Code:** none (docs + generated content).
**Tests:** docs build warning-free; `python utils/reachable_pairs_tables.py`
(check mode) exits 0; pytest green (the S2 integration test now passes).
**Docs:** rewrite `docs/reachable_pairs.rst`: keep the title, intro (add one
sentence: the sections follow the graph categories of the Graphs catalog),
note, and Download section (Columns line updated in S1); replace the flat
"Summary" table with the marker region; run
`python utils/reachable_pairs_tables.py --update` to generate the region and
sync every category-page count column; commit whatever the generator
changed.

**Spec:**
- The generated region holds exactly eight sections in `category_order`;
  nothing between the markers is hand-edited (the generator owns it).
- If the generator finds drifted count cells on category pages, fix them via
  --update and include them in this commit (expected: none — the tables were
  kept in sync manually so far; any drift found is a finding to report).

### S4: Document the tool in docs/utils.rst

**Code:** none.
**Tests:** docs build warning-free.
**Docs:** new "Reachable pair counts" section in `docs/utils.rst` (label
`reachable_pairs_tables`, placed after the Archive sizes section), in the
same style as the other tool sections: what it keeps in sync (the
per-category tables of `docs/reachable_pairs.rst` and the count columns of
the eight category pages, from
`cfpq_data/dataset/reachable_pairs.csv`), check/`--update` behavior, the
cell semantics (number / "not available" / empty), and the workflow: after
computing a new count, add the CSV row and run `--update`.

**Spec:**
- Cross-reference :ref:`reachable_pairs` from the new section.
- No other doc changes: the category pages' "Contents" explanation in
  `docs/graphs/index.rst` already describes the cell semantics correctly.
