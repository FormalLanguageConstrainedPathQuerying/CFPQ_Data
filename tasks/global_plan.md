# Global Plan: Tasks 14-16

Follow-ups of task 13 (conversion of all 54 old-format graphs to the new
mtx-per-label format, uploaded under `5.0.0/graph/`).

## Tasks

- **Task 15**: Bump VERSION/DATASET_URL to the 5.0.0 prefix and re-point docs
  download links once the conversion (task 13) is complete.
  **[USER GUIDANCE]**: "Keep them at 4.0.0" (the 59 pre-existing new-format
  graphs stay under `4.0.0/graph/`; no data movement).
- **Task 14**: Package support for new-format (mtx-per-label) graphs:
  download() + mtx-per-label readwrite + .cnf template read/write with indexed
  symbols and the _r reversed-edge convention.
  **[USER GUIDANCE]**: "Materialized CFG (Recommended)" / "_i is a placeholder
  for real index" / "file name may be load_i_5.mtx. But label is load_5".
- **Task 16**: Fix stale docs stats (e.g. generations listed as 546 edges vs
  273 stored) and document the label conventions (indexed symbols, _r reversed
  edges) in the format docs.

## Execution order: 15 -> 14 -> 16

1. **Task 15 first** — it finalizes the URL layout (VERSION bump). Task 14's
   `download()` must target the final layout; doing 14 first would force
   hard-coding the future 5.0.0 prefix. Both tasks touch
   `cfpq_data/dataset/data.py`, so they must be sequential.
2. **Task 14 second** — package support against the final layout; also fixes
   the doctests that break when `download()` starts returning new-format
   archives.
3. **Task 16 last** — docs-only. It documents the label conventions that task
   14 implements, and can use task 14's reader to verify the corrected stats.
   It also touches `docs/graphs/index.rst` + data pages, which task 15 already
   modified (links/Version) — sequential order avoids conflicts.

No bucket writes in any of the three tasks (user: keep all existing data where
it is) -> no S3 credentials needed.

## Verified facts (checked against the public bucket, 2026-09-04)

### Bucket state

| Prefix | Contents |
|---|---|
| `4.0.0/graph/` | 113 archives (0.66 GiB): the 54 old-format CSV graphs + 59 pre-existing new-format graphs |
| `5.0.0/graph/` | 54 archives: task-13 converted new-format versions of the 54 old-format graphs |
| `4.0.0/grammar/` | 147 per-graph grammar archives (`.txt`, `->` format) + `example/`; read by existing `cfg_from_txt`/`cnf_from_txt` |
| `5.0.0/grammar/` | empty |
| `4.0.0/benchmark/` | `MS_Reachability.tar.gz` |
| `5.0.0/benchmark/` | empty |

Consequence for task 15: bumping VERSION re-points `DATASET_URL` to
`5.0.0/graph/` (correct), but `GRAMMARS_URL`/`BENCHMARK_URL` must be pinned to
the 4.0.0 prefix — the 5.0.0 ones are empty and the data is not moved
(user guidance).

### New-format archive layout (verified on nab, gson, mockito, junit5,
cactus_field_sensitive_alias, generations, sunflow, avrora)

```
<name>/README.md          # MatrixMarket-style header: stats + format description
<name>/grammar/*.cnf      # one or more CNF template files
<name>/graph/*.mtx        # one Boolean MatrixMarket matrix per edge label
```

Exception: `cactus_field_sensitive_alias.tar.gz` contains a top-level
directory named `cactus/` (collides with `cactus.tar.gz`) -> `download()` must
normalize the extracted directory to the graph name.

### MTX format (verified byte-equivalent to the old CSVs for all 17 labels of
generations)

- Header: `%%MatrixMarket matrix coordinate pattern general`,
  `%%GraphBLAS type bool`.
- Dimensions line `<rows> <cols> <nnz>`, then `<i> <j>` pairs.
- Indices are **0-based** (not the MatrixMarket 1-based default).
- Pattern matrices: no values.

### Label conventions (user-confirmed)

- Real edge labels are either plain (`alloc`, `subClassOf`) or indexed
  `<base>_<k>` (`load_5`, `call_6`).
- `_i` is a **placeholder for the real index**, never part of a label:
  - original-style file `load_i_5.mtx` -> label `load_5`; grammar symbol
    `load_i` matches labels `load_<k>`;
  - converted-style file `load_5.mtx` -> label `load_5`; grammar symbol
    `load` matches labels `load_<k>`.
- `_r` marks a reversed edge (exact transpose of the forward matrix; verified
  on gson `alloc`/`alloc_r`, `load_i_5`/`load_r_i_5`):
  - stored as files in the original java_points_to graphs (gson, mockito,
    junit5: `alloc_r.mtx`, `load_r_i_5.mtx` -> label `load_r_5`);
  - NOT stored in the 54 converted graphs; grammar symbols `S_r` resolve to
    derived labels (`S_r` plain / `S_r_<k>` indexed) obtained by transposing
    the forward family.
- A grammar symbol with no matching stored or derivable label is inert (e.g.
  generations has no `subClassOf` edges, yet its archive ships
  `nested_parentheses_subClassOf.cnf`).

### CNF template format

- Whitespace-separated rules: `<NT> <S1> <S2>` / `<NT> <S1>` / `<NT>`
  (epsilon). Non-terminals are exactly the LHS symbols.
- Trailer: `Count:` line + start symbol line.
- Distinct from the old per-graph grammar archives (`4.0.0/grammar/`, `.txt`,
  `->` format) read by the existing `cfg_from_txt`/`cnf_from_txt`.

### Docs state (task 16 scope, verified programmatically)

- `docs/graphs/index.rst`: 113 graphs in 8 sections; all links point to
  `4.0.0/graph/`; **all 54 converted entries have node counts that match but
  edge counts exactly doubled** (the tables were generated when `_r` matrices
  were still stored, e.g. generations 546 = 2 x 273).
- `docs/graphs/data/*.rst`: 113 graph pages; the 54 converted ones carry the
  same stale totals and per-label tables that include `_r` rows (e.g. wc:
  `d: 156, d_r: 156, a: 113, a_r: 113`); each page has a `Version` field and a
  download link.
- `docs/old_graphs/`: the 54 old-format graphs with correct stored-only stats
  and valid 4.0.0 links (archives remain) — untouched by tasks 15/16.
- `utils/conversion_report.json`: true `num_nodes`/`num_edges` for all 54
  converted graphs; per-label counts are recoverable from the MTX headers
  (`nnz`) of the 5.0.0 archives.

## Conflicts / overlapping changes

- Tasks 15 and 14 both modify `cfpq_data/dataset/data.py` (URL constants vs
  download()/DATASET) -> sequential, 15 first.
- Tasks 15 and 16 both modify `docs/graphs/index.rst` + the 54 data pages
  (links/Version vs stats/conventions) -> sequential, 15 first.
- Task 14 modifies doctests in `cfpq_data/graphs/readwrite/csv.py`,
  `cfpq_data/grammars/generators/java_points_to_grammar.py` and possibly other
  modules that call `download()` — find them all by grep before starting.

## Shared infrastructure

- Label-convention logic (filename <-> label mapping with the `_i`
  placeholder, `_r` derivation rule) is implemented **once** in
  `cfpq_data/graphs/readwrite/mtx.py` (task 14) and documented **once** in the
  format docs (task 16).
- The 113-name dataset list and per-graph prefix resolution live in
  `cfpq_data/dataset/data.py` (tasks 15+14).

## Reuse analysis

- `download()`: generalize the existing function (requests + copyfileobj +
  unpack_archive idiom from `data.py`), do not add a new downloader.
- `graph_from_csv`/`graph_to_csv`: pattern template for the new MTX readwrite
  (logging, resolved-path return, MultiDiGraph with `label` edge attribute).
- Grammar types: pyformlang `CFG`/`Production`/`Variable`/`Terminal` as in the
  existing generators; the new template module is separate from `cnf.py`
  because the on-disk formats are incompatible (no reasonable generalization).
- Tests: extend `tests/dataset/test_data.py`; add
  `tests/graphs/readwrite/test_mtx.py` and
  `tests/grammars/readwrite/test_cnf_template.py` mirroring existing patterns.
- Docs: autosummary entries in `docs/reference/{dataset,graphs,grammars}`;
  the label-convention section goes into `docs/graphs/index.rst` (task 16).
- `utils/conversion_report.json` + MTX headers as the stats source for task 16.

## Per-task sketch (detailed plans per task in tasks/detailed_plan.md)

### Task 15 — bump VERSION/DATASET_URL to 5.0.0, re-point docs links

- S1: `config.py` VERSION -> "5.0.0", `pyproject.toml` version -> "5.0.0";
  pin `GRAMMARS_URL`/`BENCHMARK_URL` to the 4.0.0 prefix (data not migrated);
  `DATASET_KEY_PREFIX`/`DATASET_URL` derive `5.0.0/graph/`.
- S2: Re-point the 54 converted graphs' download links + Version fields in
  `docs/graphs/index.rst` and `docs/graphs/data/*.rst` to 5.0.0 (scripted,
  diff-reviewed); the other 59 pages and all `docs/old_graphs/` stay 4.0.0.

### Task 14 — package support for new-format graphs

- S1: MTX readwrite module (`graph_from_mtx_dir` / `graph_to_mtx_dir` +
  filename<->label mapping helpers, 0-based indices).
- S2: CNF template readwrite (template from/to text, `Count:` trailer) +
  `materialize(cfg, graph)` producing a CFG whose terminals are real labels
  (indexed expansion, `_r` resolution, inert symbols kept).
- S3: Reversed-edge derivation helper (add missing `_r` edges by transpose,
  skip labels already stored).
- S4: `download()` generalization: DATASET -> all 113 names, per-graph prefix
  (54 -> `DATASET_URL`, 59 -> legacy 4.0.0), extraction normalized to
  `GRAPHS_DIR/<name>/` (fixes the cactus collision), returns the graph
  directory.
- S5: Fix all doctests broken by the new `download()` contract.
- S6: Reference docs autosummary entries for the new functions.

### Task 16 — stale docs stats + label conventions

- S1: Correct the 54 converted entries in `docs/graphs/index.rst` (edge
  counts) and the 54 data pages (totals + per-label tables without `_r`
  rows), values taken from MTX headers of the 5.0.0 archives and cross-checked
  against `utils/conversion_report.json`.
- S2: Document the label conventions (indexed symbols with the `_i`
  placeholder, `_r` reversed edges, both file styles, 0-based MTX) in the
  format docs (`docs/graphs/index.rst`).
