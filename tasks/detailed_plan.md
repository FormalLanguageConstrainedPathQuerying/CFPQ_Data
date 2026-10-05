# Detailed Plan: Task 152 — Cache manipulation API

Part of hub #148 (end-user core rework). Design: `docs/flpq.rst` "Cache
manipulation" (#149) + the global plan comment on hub #148.

## Context

The cache from #151 holds one directory per dataset version under the root
(`<root>/<version>/`). This task adds the single documented way to wipe it:
`clear_cache(keep=None)` — remove version directories except `keep`
(`None` removes all), returning the removed paths. `cache_root()` and
`cached_versions()` (read-side manipulation) already exist in #151.

### S1: clear_cache(keep=None) in cache.py + tests + docs

**Code:** `flpq_data/dataset/cache.py` (new `clear_cache`; exported through
the existing star import)
**Tests:** Extended `tests/dataset/test_cache.py` — fake version trees in
`tmp_path` via `FLPQ_DATA_CACHE`, no network
**Docs:** `docs/reference/dataset/index.rst` (autosummary entry), CHANGELOG

**Spec:**
- `clear_cache(keep: str | None = None) -> list[pathlib.Path]`:
  - `root = cache_root()`; when the root does not exist, return `[]`.
  - For every directory under the root whose name differs from `keep`,
    remove it (`shutil.rmtree`) and collect its path; non-directory entries
    are left untouched.
  - Return the removed paths in sorted order (deterministic).
  - numpydoc docstring with an `Examples` block (no network).
- Tests (env override to `tmp_path`, version dirs created by hand):
  - missing root → `[]`.
  - `keep=None` removes every version dir and returns them.
  - `keep="5.0.0"` removes the others, keeps that one.
  - `keep` equal to the current dataset version keeps it.
  - a stray file under the root survives; an unknown `keep` removes all.
- Docs: autosummary entry on the dataset reference page; CHANGELOG
  `[Unreleased]` Added entry for the cache manipulation API
  (`cache_root`, `cached_versions`, `clear_cache`).
