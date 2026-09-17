# Detailed Plan: Task 40 — Archive sizes on the site + upload tool size computation

## Task

For the site, add archive sizes (size to download) to tables with graphs. Add
one new column to each table (for each category). Choose one unit of measure
for all graphs (Kb, Mb or Gb). Moreover, improve the tool that uploads a new
graph — it should compute the archive size. When a new graph is added, the
table must be updated; the computed size is used for it.

**[USER GUIDANCE]**: "Include old graphs (Recommended)" / "Add a reusable
utils script"

## Decisions (verified against live data, 2026-09-17)

- **Unit: MB** (decimal, 10^6 bytes), one unit for all graphs. All 167
  archives measured via S3 HEAD (`Content-Length`):
  - `5.0.0/graph/` (113 graphs): 2,472 B – 99,645,647 B → 0.002 – 99.65 MB;
  - `4.0.0/graph/` (54 old graphs): 2,078 B – 112,652,191 B → 0.002 – 112.65 MB.
  KB would reach ~110,000; GB would make every value < 0.12.
- **Formatting rule** (single shared function): `< 1` MB → 3 decimals
  (`0.002`, `0.988`); `>= 1` MB → 2 decimals (`1.02`, `57.21`, `99.65`).
- **Column**: header `Size (MB)`, inserted immediately before the existing
  `Download` column in every table.
- **Scope**: all 9 graph tables — the 8 per-category pages
  (`docs/graphs/{c_alias_analysis,rdf,java_points_to,field_sensitive_alias,
  context_sensitive_data_flow,data_provenance,name_resolution,
  biological_uniprot}.rst`) and `docs/old_graphs/index.rst`. The benchmarks
  table is excluded (it lists benchmark archives, not graphs). Per-graph Info
  pages are unchanged.
- **No new state file**: the S3 bucket is the source of truth for archive
  sizes. The upload tool reports the size it verifies at upload time; the
  table tool fetches the same values from S3. Nothing to keep in sync in the
  repo besides the tables themselves.
- **URL keying**: sizes are keyed by full URL, not archive name — the 4.0.0
  and 5.0.0 prefixes contain same-named archives with different content
  (old CSV format vs new mtx-per-label format).

## Reuse analysis (reusing skill)

- `utils/config.py:MAIN_FOLDER` — reused to anchor the docs paths so the tool
  runs from any CWD.
- `utils/audit_info_tables.py` — line-based RST list-table parsing style and
  module layout (docstring + usage, `__all__`, pure functions with numpydoc
  docstrings, `main(argv)` with argparse) reused as the template for
  `archive_sizes.py`.
- `tests/utils/conftest.py` already puts `utils/` on `sys.path`; new tests
  follow `tests/utils/test_upload_to_s3.py` conventions (mocked clients, no
  network in the test suite).
- `upload_file()` in `utils/upload_to_s3.py` already computes and verifies
  the stored size (`head_object` vs local stat) — S5 only surfaces it.
- No existing size-formatting code anywhere (searched `cfpq_data/`,
  `utils/`, `docs/`) — `utils/sizes.py` is genuinely new.

## Subtasks

### S1: Record task, create branch, write this plan

**Code:** none.
**Tests:** none.
**Docs:** `tasks/tasks.md` (task line), `tasks/detailed_plan.md` (this file).

**Spec:**
- Task 40 logged in `tasks/tasks.md` with the user's description verbatim and
  the two Q&A decisions as **[USER GUIDANCE]**.
- Feature branch `feature/40-archive-sizes` created from `dev`.

### S2: Shared size formatting — `utils/sizes.py`

**Code:** New `utils/sizes.py` with `format_size_mb(size_bytes: int) -> str`
implementing the formatting rule above (decimal MB; 3 decimals below 1, 2
decimals from 1 up). numpydoc docstring with doctest-stable `Examples`.
**Tests:** New `tests/utils/test_sizes.py`: boundary values (0 B, 999,999 B →
`0.999`, 1,000,000 B → `1.00`, 1,021,000 B → `1.02`), real archive sizes
(wc 2,472 B → `0.002`; taxonomy_hierarchy 112,652,191 B → `112.65`), and the
doctest examples.
**Docs:** none (maintainer-internal module; documented where used in S3/S5).

**Spec:**
- Pure function, no I/O, no dependencies; importable as top-level `sizes`
  (conftest puts `utils/` on `sys.path`).
- The formatting rule lives here and ONLY here — both `archive_sizes.py` and
  `upload_to_s3.py` import it (single source of truth).

### S3: Table tool — `utils/archive_sizes.py`

**Code:** New `utils/archive_sizes.py`:
- `iter_graph_tables(text: str) -> list[GraphTable]` — line-based parser for
  RST `list-table`s whose header row contains a `Download` cell; returns the
  table's rows (each row = list of `(line_index, cell_text)` pairs) so both
  check and update can operate on it. Tables without a `Download` header are
  skipped (e.g. the Contents table in `docs/graphs/index.rst`).
- `extract_url(cell: str) -> str | None` — pulls the `https://…` target out of
  a `` `name.tar.gz <URL>`_ 📥 `` cell.
- `fetch_sizes(urls: Iterable[str], timeout: float = 30.0, workers: int = 8)
  -> dict[str, int]` — HEAD each unique URL (stdlib `urllib.request`,
  `ThreadPoolExecutor`), one retry per URL, returns `{url: content_length}`;
  raises `RuntimeError` listing the failed URLs so updates are all-or-nothing.
- `update_table(text: str, sizes: dict[str, int]) -> tuple[str, int]` —
  rewrites every graph table in the text: inserts a `Size (MB)` header cell
  before `Download` where missing and fills/fixes each row's size cell with
  `format_size_mb`; returns the new text and the number of changed rows.
- `main(argv) -> int` — default **check mode**: parse
  `docs/graphs/*.rst` + `docs/old_graphs/index.rst` (anchored at
  `utils.config.MAIN_FOLDER`), fetch sizes, report every row whose cell
  disagrees with the stored object (or is missing), exit code 1 on any
  problem; `--update`: fetch all sizes first, then rewrite the files and
  print what changed.

**Tests:** New `tests/utils/test_archive_sizes.py` — synthetic RST strings
only, no network: parser finds graph tables and skips non-graph tables;
`extract_url`; `update_table` inserts the column into a table that lacks it
and fixes wrong values in one that has it (idempotent second pass → 0
changes); row/URL alignment on a multi-grammar table (3 grammar columns, like
`rdf.rst`). `fetch_sizes` tested with a local `http.server` serving HEAD
responses (or monkeypatched `_head_size`) — no external network.
**Docs:** none yet (the tool's docs page section lands in S6, together with
the populated tables it documents).

**Spec:**
- RST cell insertion preserves the exact indentation of the file
  (`   * - ` row starts, `      - ` continuation cells); the no-warnings docs
  build is the safety net for malformed tables.
- Check mode output: one line per problem
  (`<file>:<line>: <graph>: table says X, stored is Y`), then a summary;
  exit 0 only when every row of every graph table matches S3.
- Update mode writes a file only if it changed; all fetches happen before any
  write (a failed HEAD aborts the run with nothing written).

### S4: Populate the Size (MB) column in all 9 tables

**Code:** none (the change is produced by running the new tool — dogfooding).
**Tests:** `python utils/archive_sizes.py` (check mode) must report all 9
tables in sync (167 rows) against live S3.
**Docs:** The 8 per-category tables + `docs/old_graphs/index.rst` gain the
`Size (MB)` column; one sentence added to the "Contents" section of
`docs/graphs/index.rst` describing the column (the download size of the
`<name>.tar.gz` archive, in MB).

**Spec:**
- Run `python utils/archive_sizes.py --update` from the repo root; inspect
  the diff: exactly one new header cell and one new cell per row in each of
  the 9 tables, values matching the live S3 sizes fetched during planning.
- Re-run check mode → clean. Build the docs (no-warnings) to validate the
  RST.

### S5: Upload tool reports the computed size

**Code:** `utils/upload_to_s3.py`:
- `upload_file()` — extend the existing `logging.info` with the verified size
  in bytes; return type unchanged (`key`), so `migrate_gdrive_to_s3.py` is
  untouched.
- `main()` — print the size in both units using `sizes.format_size_mb`:
  `Uploaded FILE to s3://BUCKET/KEY (12345678 bytes, 11.79 MB)`.
**Tests:** Extend `tests/utils/test_upload_to_s3.py`: `test_main_uploads_file`
asserts the byte count and the formatted MB value in the output; a small-file
case exercises the `< 1 MB` formatting branch (`0.000 MB`).
**Docs:** `docs/utils.rst`, "Upload to Yandex S3" section — extend the
verification paragraph: the tool reports the verified size (bytes and MB),
which is the value for the `Size (MB)` column of the graph tables.

**Spec:**
- The reported size is the *verified* stored size (the `head_object`
  `ContentLength` that already must equal the local file size) — the same
  number `archive_sizes.py` reads back from S3, so a new-graph row filled
  from the upload output always matches check mode.

### S6: Document the tool and the new-graph flow

**Code:** none.
**Tests:** none (docs-only; docs build in S7).
**Docs:**
- `docs/utils.rst` — new "Archive sizes" section for `utils/archive_sizes.py`
  (usage, check vs `--update`, what it covers: the 9 graph tables, URL keying,
  all-or-nothing updates), placed after "Upload to Yandex S3".
- `.opencode/skills/add-graph/SKILL.md` — Documentation section gains the size
  step: the upload tool reports the archive size; add the category-table row
  with that `Size (MB)` value; run `python utils/archive_sizes.py --update`
  before committing so every table row (including the new one) matches S3.
- `CHANGELOG.md` `[Unreleased] → Added`: one bullet for the `Size (MB)` column
  in the website graph tables, one for the tooling (`upload_to_s3.py` reports
  the verified size; new `utils/archive_sizes.py` keeps the column in sync).

**Spec:**
- The skill stays a thin pointer: it names the step and the command, the
  model (column semantics, formatting rule) lives in the docs.

### S7: Quality gate, review, merge

**Code:** none (fixes only if the gate finds problems).
**Tests:** full quality gate per the `quality-gates` skill: `uv run pytest`,
ruff (check + format), `uv run ty check`, no-warnings docs build, linkcheck.
**Docs:** `tasks/tasks.md` — mark Task 40 `[done]` after the merge.

**Spec:**
- Whole-repo code review per the `code-review` skill first; iterate to zero
  findings.
- Rebase onto `dev`, fast-forward merge, delete the feature branch (per
  `git-workflow`). No pushes.
