# Detailed Plan: Task 161 — Remove the Version row from per-graph Info tables

Issue #161. Every per-graph docs page carries a `Version` row in its Info
list-table duplicating the dataset version. On the current pages
(`docs/graphs/data/`, 113 files) it is stale: it says `5.0.0` while the
dataset is `6.0.0` (the 6.0.0 migration re-pointed the download links in
#133 but missed this row). On the historical `old_graphs` pages
(`docs/old_graphs/data/`, 54 files) it says `4.0.0`, consistent with their
URLs but equally redundant.

## Decision: remove, not automate

The version is easily discoverable and is not per-graph information:

- It is the dataset version — one value for all pages — defined once in
  `flpq_data/config.py` (`DATASET_VERSION`).
- The "Direct download" URL on the same page already encodes it
  (`.../6.0.0/graph/<name>.tar.gz`, `.../4.0.0/graph/<name>.tar.gz`).
- Nothing consumes the row: no tool, test, or template reads it from the
  pages. `utils/audit_info_tables.py` and its tests use synthetic field
  names; the "Version" field of the `.github/` contribution templates is
  contribution metadata (which release an archive targets), not a page field.

Per the single-source-of-truth principle, a manually maintained duplicate
that has already gone stale once is removed rather than automated. New
per-graph pages (the add-graph skill says to follow the structure of an
existing page) will no longer carry the row.

## Subtasks

### S1: Remove the Version row from the 113 current per-graph pages [docs] [done] (cc13b4e)

**Code:** none (docs only).
**Files:** `docs/graphs/data/*.rst` — delete the two-line Info-table row
(`* - Version` / `- 5.0.0`) from each page; no other line changes.
**Tests:** skip (no code); verify with `python utils/audit_info_tables.py`
— no `Version` field, shapes reduce to `[Full Name, Direct download]` (50)
and `[Full Name, Direct download, Source]` (63).

### S2: Remove the Version row from the 54 historical old_graphs pages [docs]

**Code:** none (docs only).
**Files:** `docs/old_graphs/data/*.rst` — same deletion (`- 4.0.0` value);
the frozen historical family keeps one uniform page format with the current
one.
**Tests:** skip; verify with
`python utils/audit_info_tables.py --dir docs/old_graphs/data`.

### S3: Record the removal in the changelog [docs]

**Code:** none (docs only).
**Files:** `CHANGELOG.md` — a "Changed" entry under `[6.0.0]`: this task
lands on dev before the release merge, so it ships with 6.0.0.
**Tests:** skip; docs build green.

## Verification

- `python utils/audit_info_tables.py` on both directories: no `Version`
  field in any shape.
- `grep -rn '^\s*\* - Version$' docs/graphs/data docs/old_graphs/data` →
  empty.
- Docs build (quality gate) green, no warnings.
