# Detailed Plan: Issue #139 — Fix reachable_pairs CSV packaging and storage

## Context

Issue #139 (task): "reachable_pairs.csv is missing from the 5.0.0 wheel;
documentation link returns 404". `cfpq_data.reachable_pairs("wc", "c_alias.cnf")`
raised `FileNotFoundError` for `cfpq_data/dataset/reachable_pairs.csv` on the
installed 5.0.0 wheel, and the docs CSV link pointed at an unpinned
`raw.githubusercontent.com/.../dev/...` URL that 404s.

User guidance (the design driver for this task):
"store the table in S3. It must be versioned as dataset, so stored in
respective path with version prefix."

## Current state (6.0.0 codebase)

- `flpq_data/dataset/reachable_pairs.csv` exists in the repo (tracked) and is
  included in the wheel built by hatchling (`packages = ["flpq_data"]`).
- `reachable_pairs.py` reads the CSV from
  `pathlib.Path(__file__).parent / "reachable_pairs.csv"` (bundled).
- `docs/reachable_pairs.rst` links the CSV from `raw.githubusercontent.com`
  (`dev` branch, unpinned).
- The graph dataset is served from S3 under `{VERSION[0]}.0.0/graph/`
  (`flpq_data/dataset/data.py`), publicly readable.
- The partial branch work added an S3 URL constant, an S3-download/cache
  routine and changed the docs link, but left the code largely untested
  (coverage gate fails: branch 93.56% < 95%) and made the exported
  `REACHABLE_PAIRS_CSV` point at a cache path that does not exist on a fresh
  checkout (`test_csv_exists` only passed because a stale cache file existed
  locally).

## Design decisions

1. **Keep the CSV bundled in the wheel** (fixes the reported
   `FileNotFoundError`): the repo file `flpq_data/dataset/reachable_pairs.csv`
   stays the single source of truth for the counts and the offline package
   API. `REACHABLE_PAIRS_CSV` points at it and always exists.
2. **Publish the CSV to S3 under the version prefix** at
   `{VERSION[0]}.0.0/reachable_pairs.csv` (sibling of `graph/`) — the table is
   dataset-level metadata, not a graph archive, so it does not belong under
   the archive-validated `graph/` prefix. The key derives from `VERSION`, the
   same single source as `DATASET_KEY_PREFIX`, so it moves with the version
   bump.
3. **Expose the versioned location as `REACHABLE_PAIRS_URL`** and add
   `download_reachable_pairs()`, which fetches the versioned copy into the
   shared local data cache (`flpq_data/config.py::DATA`, the same directory
   graph archives use). This lets an updated table be consumed without a new
   package release.
4. **`reachable_pairs()` prefers the downloaded versioned copy when present,
   else the bundled one.** No implicit network access on every call: the
   download is explicit, so the API stays deterministic and offline-capable.
5. **Fix the documentation link** to the S3 versioned URL (no `dev` branch
   dependency, no 404).

## Subtasks

### S1: Versioned S3 storage for reachable_pairs in the package
**Code:** rewrite `flpq_data/dataset/reachable_pairs.py`: `REACHABLE_PAIRS_FILENAME`,
`REACHABLE_PAIRS_KEY_PREFIX`, `REACHABLE_PAIRS_URL`, bundled `REACHABLE_PAIRS_CSV`,
`download_reachable_pairs()`, and a resolver used by `reachable_pairs()`.
**Tests:** none yet (S2).
**Docs:** none yet (S3).

**Spec:**
- `REACHABLE_PAIRS_KEY_PREFIX = f"{VERSION[0]}.0.0"`.
- `REACHABLE_PAIRS_URL = "https://cfpq-data.storage.yandexcloud.net/6.0.0/reachable_pairs.csv"`.
- `REACHABLE_PAIRS_CSV = Path(__file__).parent / "reachable_pairs.csv"` (bundled, always exists).
- `download_reachable_pairs()` -> writes `DATA / "reachable_pairs.csv"`, returns the path.
- `reachable_pairs()` reads `DATA / "reachable_pairs.csv"` if it exists, else
  `REACHABLE_PAIRS_CSV`; signatures and returned rows unchanged.

### S2: Tests for the versioned storage
**Code:** none.
**Tests:** extend `tests/dataset/test_reachable_pairs.py`.
**Docs:** none.

**Spec:**
- URL constants assert the 6.0.0 prefix and full URL.
- `download_reachable_pairs()` writes the fetched bytes to a monkeypatched
  `DATA` (no network) and returns the destination path.
- The resolver returns the downloaded copy when present and the bundled copy
  otherwise (both branches), with `reachable_pairs()` reading the selected file.

### S3: Documentation for the versioned CSV
**Code:** none.
**Tests:** none.
**Docs:** `docs/reachable_pairs.rst` (S3 link + download API), `CHANGELOG.md`
(Unreleased/Added or Fixed).

**Spec:**
- The "CSV file" link points at `REACHABLE_PAIRS_URL`.
- The Download section documents that the table is shipped with the package
  and that the versioned copy is available from S3 via
  `download_reachable_pairs()`.
- Changelog records the versioned S3 storage and the packaging/link fix.

### S4: Verify the CSV ships in the wheel
**Code:** only if the wheel lacks the file.
**Tests:** none.
**Docs:** none.

**Spec:**
- Build the wheel (`uv build --wheel`) and confirm
  `flpq_data/dataset/reachable_pairs.csv` is present; if absent, add the
  hatch build configuration needed to include it.

### S5: Publish and verify the versioned CSV on S3
**Code:** none.
**Tests:** none.
**Docs:** none.

**Spec:**
- Upload `flpq_data/dataset/reachable_pairs.csv` to
  `s3://cfpq-data/6.0.0/reachable_pairs.csv` with `utils/upload_to_s3.py`
  (credentials from the user).
- Verify the public `REACHABLE_PAIRS_URL` returns 200 and the exact byte
  contents.
- Final subtask: carries `Closes #139`.
