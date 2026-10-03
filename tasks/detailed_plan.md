# Detailed Plan: Task 146 — strip stored reverse edges from 7 Java points-to archives and fix the checker

Task issue: **#146**. Fully resolves bug **#136**. Branch:
`feature/146-strip-stored-reverses`.

## Context

The 6.0.0 migration (task 48) was supposed to remove stored reverse edges, but
7 of the 21 `java_points_to` archives still bundle `load_r_<n>.mtx` /
`store_r_<n>.mtx`:

- with reverses: commons_io, commons_lang3, gson, guava, jackson, junit5, mockito
- clean: avrora, batik, eclipse, fop, h2, jython, luindex, lusearch, pmd,
  sunflow, tomcat, tradebeans, tradesoap, xalan

The stored reverses are exact transposes of the forward labels (verified on
gson) and are never grammar terminals: `materialize` emits `load_<k>_r`
(derived from forward edges), so the stored `load_r_<k>` are dead weight and
cause `add_reverse_edges()` to double-reverse.

`utils/check_archive_structure.py` Rule 3 ("no stored reverses") only checks
stems ending in `_r`, so it catches `a_r.mtx` but not `load_r_0.mtx`; all 7
archives report `archive structure ok`.

## Design decisions

1. **Checker.** Extend Rule 3 to also flag an indexed reverse `B_r_<n>` when
   the forward `B_<n>` is stored. The unindexed `L_r` branch stays.
2. **Tool.** Add a reusable `utils/strip_reverse_edges.py` maintenance tool
   (archive in, archive out) rather than a one-off script; removing stored
   reverses is now a convention the checker enforces, so the normalizer is
   reusable.
3. **No recomputation of `results.mtx`.** Reachability is unchanged. Proof:
   `temporal_cfpq/run_reference.py:stream_g_file` writes, for every stored
   `.mtx` edge, both the forward token and its reverse. The stored reverse
   files therefore only add duplicate edges and `_r_r_i` tokens that no
   grammar terminal matches; dropping them cannot change the solution.
4. **Docs reflect stored edges.** `docs/graphs/index.rst` says the Edges
   Statistics tables list stored labels only. The 7 per-graph pages and the
   `java_points_to` category table must drop the reverse rows and halves of the
   edge counts; `Size (MB)` follows from `utils/archive_sizes.py --update`.

## Reuse

- `utils/check_archive_structure.py` — the reverse-label regexes
  (`_INDEXED_REV_RE`) and the existing Rule 3 message.
- `utils/upload_to_s3.py` / `check_archive_structure.validate_archive` — the
  upload path already validates archives (used by the tool and by S3).
- `utils/archive_sizes.py --update` — refreshes the `Size (MB)` columns.
- `utils/merge_archive.py` — pattern for a tar-in/tar-out maintenance tool
  (single top-level dir handling, validation, exit codes).
- `temporal_cfpq` (gitignored) — `stream_g_file`/`label_to_tokens` for the
  reachability-invariance argument; not depended on by committed code.

## Subtasks

### S1: Catch indexed stored reverses in the archive checker [done] (caf7af6)

**Code:** `utils/check_archive_structure.py` — extend `_label_problems` Rule 3.
**Tests:** `tests/utils/test_check_archive_structure.py` — new cases.
**Docs:** `docs/utils.rst` — the "Graph" check bullet already covers label
consistency; extend the reverse note to name both stored forms.

**Spec:**
- Keep the existing branch: a stem ending in `_r` whose `stem[:-2]` is stored.
- Add: a stem matching `^(?P<base>.+)_r_(?P<idx>\d+)$` whose
  `f"{base}_{idx}"` is stored is a stored reverse. Report the same message
  ("reversed edge is stored but must be auto-generated from <forward>.mtx").
- No double report: an indexed stem has a numeric suffix, so it is not caught
  by the `_r` branch.
- Tests:
  - stored unindexed reverse (`a.mtx` + `a_r.mtx`) is flagged;
  - stored indexed reverse (`load_0.mtx` + `load_r_0.mtx`) is flagged;
  - an indexed reverse without its forward (`load_r_0.mtx` only) is not
    flagged by Rule 3.

### S2: Add a strip-stored-reverses maintenance tool

**Code:** new `utils/strip_reverse_edges.py`.
**Tests:** new `tests/utils/test_strip_reverse_edges.py`.
**Docs:** `docs/utils.rst` — new "Strip stored reverse edges" section.

**Spec:**
- CLI: `python utils/strip_reverse_edges.py ARCHIVE.tar.gz -o OUT.tar.gz`
  (also accept an unpacked directory for tests).
- A graph `.mtx` stem is a stored reverse when its forward exists (same
  predicate as the fixed Rule 3). Remove those files.
- Rewrite `README.md` "Edges and labels": drop the reverse bullet lines
  (labels ending in `_r`, `_r_i`, or `_r_<i>`) and set the leading
  "N stored edges:" total to the sum of the remaining bullets.
- Preserve the single top-level directory and deterministic (sorted) member
  order; refuse to write an output that fails
  `check_archive_structure.validate_archive`.
- Return/print the number of removed files and the old/new total.
- Tests: a small fixture archive with `a`/`a_r`/`load_0`/`load_r_0`; assert
  the reverse files are gone, the README total recomputed and reverse bullets
  removed, the output validates, and a second run is a no-op.

### S3: Strip and re-upload the 7 archives

**Code:** none in the package; add `utils/reverse_edges_strip_record.json`
(old/new sha256 + removed count per archive).
**Tests:** verification commands (not committed unit tests).
**Docs:** the record JSON is the provenance document.

**Spec:**
- For each of the 7 names: download `6.0.0/graph/<name>.tar.gz`, strip with the
  S2 tool, validate with the S1 checker, upload back to
  `6.0.0/graph/<name>.tar.gz` with `utils/upload_to_s3.py` (credentials from
  the CLI), size-verified by the tool.
- Re-download the 7 and validate; assert no reverse problems and no structural
  problems.
- Confirm the 14 clean archives still validate.
- Record old/new sha256 + removed-file count in the JSON.

### S4: Fix edge statistics in the docs

**Code:** docs only.
**Tests:** none (Sphinx `Num Edges` cells); docs build is part of the gate.
**Docs:** 7 `docs/graphs/data/<name>.rst` and
`docs/graphs/java_points_to.rst`.

**Spec:**
- For each of the 7 per-graph pages: set `Num Edges` to the forward-only
  stored sum and delete the reverse rows (`*_r`, `*_{r\_i}`) from
  "Edges Statistics".
- `docs/graphs/java_points_to.rst`: set the `Num Edges` cells of the 7 rows to
  the same values.

### S5: Refresh sizes and record the change

**Code:** docs only.
**Tests:** `python utils/archive_sizes.py` (check mode) must pass.
**Docs:** `docs/graphs/java_points_to.rst` (`Size (MB)` column, via the tool)
and `CHANGELOG.md` `[Unreleased]`.

**Spec:**
- Run `utils/archive_sizes.py --update` to refresh every `Size (MB)` cell from
  the re-uploaded 6.0.0 objects.
- Add a CHANGELOG `[Unreleased]` entry: 7 java_points_to archives no longer
  store reverse edges; the archive checker now rejects indexed stored reverses.
- Last commit carries `Closes #146` and `Fixes #136`.
