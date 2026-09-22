# Detailed Plan: Task 47 — query_class column in reachable pairs

Task (user's words, recorded in `tasks/tasks.md`): "Add a `query_class`
column to `reachable_pairs.csv` and the `reachable_pairs()` API (+ update
the generator from task 43)."

Scope (from `tasks/global_plan.md`; no ambiguity requiring user input — the
class values follow the existing conventions, see Verified facts):
- The CSV gains a `query_class` column; all 155 current rows are CFPQ data.
- `reachable_pairs()` exposes the column as a field and a filter.
- The task-43 generator (`utils/reachable_pairs_tables.py`) stays correct
  with the new column: it validates the value and renders what the site can
  render today (CFPQ only, until the per-class sections of task 50).

Verified facts this plan builds on (checked against the repo, 2026-09-22):
- `cfpq_data/dataset/reachable_pairs.csv`: header
  `graph,grammar,category,num_reachable_pairs`, 155 data rows; every row is
  CFPQ data (`.cnf` grammars).
- `reachable_pairs(graph=None, grammar=None, category=None)` in
  `cfpq_data/dataset/reachable_pairs.py` filters on exact match and returns
  row dicts with the four CSV fields (`num_reachable_pairs` as int or None).
- The generator's `load_rows` parses the same four fields; `main()`
  validates every row (graph known to the site, category agrees, grammar has
  a count column in `GRAMMAR_COLUMNS`) and renders both renderings from all
  rows.
- Query-class names already exist once:
  `QUERY_CLASSES = {"cfpq": ".cnf", "rpq": ".re", "mcfpq": ".mcfg"}` in
  `utils/check_archive_structure.py` (keys = the archive `queries/<class>/`
  directory names, lowercase) — reused as the single source of truth for the
  column values; the CSV's existing values are all lowercase stems.
- The site renders CFPQ counts only today: the per-category tables of
  `docs/reachable_pairs.rst` and the count columns of `docs/graphs/*.rst`
  are keyed by `.cnf` grammar files (`GRAMMAR_COLUMNS`). Per-class sections
  come with task 50.
- `tests/utils/test_reachable_pairs_tables.py` builds row dicts directly
  (a `ROWS` fixture) and runs `main()` on the real repo in check mode;
  `load_rows` is covered by a doctest with inline CSV text.

Reuse (per the reusing skill):
- `QUERY_CLASSES` from `utils/check_archive_structure.py` — no new constant
  for the class names (utils scripts already cross-import: this module
  imports `archive_sizes` and `config`).
- The existing filter pattern of `reachable_pairs()` (exact match, None =
  all) — the new parameter follows it.
- No new docs pages: the CSV column list lives in
  `docs/reachable_pairs.rst`, the tool behavior in `docs/utils.rst`, and the
  design statements in `docs/flpq.rst` — each updated in place.

### S1: Record the task and write this plan

**Code:** none.
**Tests:** none.
**Docs:** `tasks/tasks.md` — add the task 47 entry (tasks 47-50 were only in
the global plan); `tasks/detailed_plan.md` — this plan.

**Spec:**
- The task text is recorded verbatim from the global plan.

### S2: The CSV column and the API

**Code:** `cfpq_data/dataset/reachable_pairs.csv` — new header
`graph,grammar,category,query_class,num_reachable_pairs`; all 155 rows gain
`cfpq` (mechanical rewrite via a one-off Python snippet, verified by row
count and a spot check). `cfpq_data/dataset/reachable_pairs.py` —
`reachable_pairs(graph=None, grammar=None, category=None,
query_class=None)`; the filter follows the existing exact-match pattern; the
row dicts gain `query_class`; docstring updated (the reference docs page is
autosummary-generated from it).

**Tests:** `tests/dataset/test_reachable_pairs.py` — `test_all_rows_have_keys`
gains `query_class`; new tests: every row's `query_class` is `cfpq`;
`reachable_pairs(query_class="cfpq")` returns all 155 rows;
`reachable_pairs(query_class="rpq")` returns `[]`.

**Docs:** the numpydoc docstring (reference docs regenerate from it).

**Spec:**
- Column order: `query_class` sits with the identifier columns, before
  `num_reachable_pairs` (the only value column, which may be empty).
- Values are lowercase (`cfpq`, `rpq`, `mcfpq`) — the same names as the
  `queries/<class>/` archive directories.
- The API does not validate the filter value: an unknown class simply
  matches no row (consistent with the other filters).

### S3: The generator

**Code:** `utils/reachable_pairs_tables.py` —
- `load_rows`: parse `query_class` into the row dicts; doctest updated to
  the new header.
- `from check_archive_structure import QUERY_CLASSES` (reused, not
  redefined).
- a `_rendered_rows(rows)` helper: the rows the current site renders —
  `query_class == "cfpq"` — with a comment that per-class rendering comes
  with the task-50 site restructure; used by both `render_tables_region`
  and `update_category_columns`.
- `main()`: every row's `query_class` must be a key of `QUERY_CLASSES`
  (clear error naming the row); the count-column check applies to cfpq rows
  only — other classes have no site rendering yet, so their grammar files
  are not expected in `GRAMMAR_COLUMNS`.
- module docstring: the CSV is self-describing including `query_class`; the
  renderings cover CFPQ rows until task 50.

**Tests:** `tests/utils/test_reachable_pairs_tables.py` — the `ROWS` fixture
gains `query_class: "cfpq"` on every row; new tests: `load_rows` parses
`query_class` (temp CSV with a mixed-class row); `render_tables_region` and
`update_category_columns` ignore non-cfpq rows; `main()` in check mode
reports an unknown `query_class` value (monkeypatched CSV + docs) and passes
a valid non-cfpq row that has no count column.

**Docs:** `docs/utils.rst` "Reachable pair counts" — the check-mode bullet
gains the unknown-class case; a sentence notes that non-CFPQ rows are
validated but not rendered until the per-class sections exist (task 50);
the "add the row" note mentions the `query_class` value.

**Spec:**
- Rendering behavior is unchanged for the current all-cfpq CSV: check mode
  on the real repo must still report in sync.
- The class-name validation reuses `QUERY_CLASSES`; no second copy of the
  names.

### S4: The site docs

**Code:** none.
**Tests:** docs build exits 0.
**Docs:** `docs/reachable_pairs.rst` — the CSV column list gains
`query_class` (with its values); `docs/flpq.rst` — the "Reachable pair
counts" section: the CSV "gains a category and a query_class column so it
is self-describing"; the API-changes bullet: "reachable_pairs() gains the
category and query_class fields".

**Spec:**
- Each statement is updated in place; no new page, no duplication of the
  column list.

### S5: Mark task 47 done

**Code:** none.
**Tests:** quality gate at merge (canonical test command, pre-commit, ty,
pyright, docs build).
**Docs:** `tasks/tasks.md` — `[done]`; `tasks/global_plan.md` — `[done]`.

**Spec:**
- Marked done only after the quality gate passes; the diff adds no external
  links, so linkcheck is unaffected by this task's changes.
