# Detailed Plan: Issue #133 — Align the site with the 6.0.0 dataset

## Context

dev works towards v6.0 (user decision: preparation only, no version bump —
that is task 49). The dataset on S3 is at the `6.0.0/graph/` prefix
(self-contained archives), but the site still points at 5.0.0 artifacts: all
226 download links (113 per-graph pages + 113 category-table rows) use
`5.0.0/graph/`, the `Size (MB)` columns reflect 5.0.0 archive sizes, and
`docs/utils.rst` / `AGENTS.md` carry stale references. The 6.0.0 archives
have different sizes (e.g. xz_field_sensitive_alias: 27.7 KB -> 536 KB).

Scope per the issue: re-point links, refresh sizes via the existing tool,
update the two stale reference spots, and keep benchmark page related stuff
removed (no re-introduction; historical changelog entries and flpq.rst design
references stay; LICENSE-DATA.txt keeps "benchmarks" because the
4.0.0/benchmark/ data is still distributed). The old-graphs table links to
`4.0.0/graph/` and stays untouched.

## Subtasks

### S1: Re-point all download links to 6.0.0/graph/ [pending]

**Code:** none (docs-only)
**Tests:** skip (no code); verify with a grep that no `5.0.0/graph` link
remains in docs/graphs/ and that the old-graphs table still points at 4.0.0
**Docs:** `docs/graphs/data/*.rst` (113 "Direct download" links) and
`docs/graphs/*.rst` (8 category tables, 113 "Download" links)

**Spec:**
- Replace every `https://cfpq-data.storage.yandexcloud.net/5.0.0/graph/`
  with `https://cfpq-data.storage.yandexcloud.net/6.0.0/graph/` in the 121
  files (226 links). No other text changes.

### S2: Refresh the Size (MB) columns against the 6.0.0 archives [pending]

**Code:** none (tool-driven docs update)
**Tests:** `utils/archive_sizes.py` check mode must pass after the update
**Docs:** the `Size (MB)` cells of the eight category tables in
`docs/graphs/*.rst` (the tool rewrites only drifted cells)

**Spec:**
- Run `uv run python utils/archive_sizes.py --update` (anonymous HTTP HEAD
  against the public bucket; no credentials).
- Verify with check mode (exit 0) and inspect the diff: only size cells of
  the 6.0.0-re-pointed tables change; the old-graphs (4.0.0) table is
  untouched.

### S3: Update stale prefix references in docs/utils.rst and AGENTS.md [pending]

**Code:** none (docs-only)
**Tests:** skip (no code); docs build green
**Docs:** `docs/utils.rst` (upload key example, archive_sizes coverage
  description, --audit example), `AGENTS.md` ("Package layout")

**Spec:**
- `docs/utils.rst`: current-state references move to `6.0.0/graph/` — the
  upload `--key` example, the archive_sizes coverage sentence ("113 archives
  at the ... prefix"), and the `--audit --prefix` example. The
  migrate_gdrive_to_s3 section describes the historical migration (5.0.0) —
  leave it untouched.
- `AGENTS.md` "Package layout": the `cfpq_data/dataset/` line still lists
  download_grammars/download_benchmark (removed in 48-S6); replace with the
  current API (`download`, `reachable_pairs`).
