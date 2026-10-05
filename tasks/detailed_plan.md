# Detailed Plan: Task 151 — Machine-global versioned cache + lazy downloads

Part of hub #148 (end-user core rework). Closes #140 (the graph archive was
re-downloaded on every call). Design: `docs/flpq.rst` "Core API: metadata,
lazy access, and cache" (#149) + the global plan comment on hub #148.

## Context

`download_graph()` today re-downloads and re-extracts into the in-package
dir (`config.GRAPHS_DIR`) on every call — no cache, no integrity check, data
written inside the installed package. This task moves downloaded data to a
machine-global, per-user cache keyed by dataset version (mirroring the S3
layout) and makes the accessor lazy: `graph_dir(name)` returns the local
folder and touches the network only on a cache miss or invalidation.

Cache layout (version root = dataset version, so versions coexist)::

   <root>/<version>/
   ├── reachable_pairs.csv
   └── graph/<name>/<name>.tar.gz        plus the unpacked contents in the
                                          same folder (README.md, graph/, queries/)
       <name>.tar.gz.sha256               sidecar digest written at install

`<root>` = `FLPQ_DATA_CACHE` env var, else
`platformdirs.user_cache_dir("flpq-data")`.

### S1: platformdirs dependency + flpq_data/dataset/cache.py [done] (f8c2760)

**Code:** `pyproject.toml` (new `platformdirs` dependency), new
`flpq_data/dataset/cache.py`, `flpq_data/dataset/__init__.py`
**Tests:** New `tests/dataset/test_cache.py` — no network
**Docs:** `docs/reference/dataset/index.rst` (autosummary entries)

**Spec:**
- `pyproject.toml`: add `platformdirs>=4.12.3,<5.0.0` to `[project]
  dependencies`; `uv lock`.
- `flpq_data/dataset/cache.py`:
  - `CACHE_ENV_VAR = "FLPQ_DATA_CACHE"`.
  - `cache_root() -> pathlib.Path` — the env var when set (non-empty), else
    `pathlib.Path(platformdirs.user_cache_dir("flpq-data"))`.
  - `version_dir(version: str | None = None) -> pathlib.Path` —
    `cache_root() / (version or DATASET_VERSION)`; no I/O.
  - `cached_versions() -> list[str]` — sorted names of the directories under
    `cache_root()`; `[]` when the root does not exist (files ignored).
- `dataset/__init__.py`: star-import the new module.
- Tests: env override wins over the OS default; unset env falls back to
  `platformdirs.user_cache_dir` (monkeypatched); `version_dir` defaults to
  the dataset version and honours an explicit one; `cached_versions` on a
  missing root, on a root with version dirs + a stray file.

### S2: Lazy accessor graph_dir(name, verify=False) in data.py [done] (4fbc85e)

**Code:** `flpq_data/dataset/data.py` (reworked)
**Tests:** Reworked `tests/dataset/test_data.py` — real tarballs in
`tmp_path`, monkeypatched `requests.get`, no network
**Docs:** `docs/tutorial.rst` (`graph_dir`), `docs/reference/dataset/index.rst`

**Spec:**
- `data.py`:
  - `graph_dir(name: str, verify: bool = False) -> pathlib.Path` — the
    single data accessor:
    - `info = graph_info(name)` (FileNotFoundError for unknown names).
    - `dest = version_dir() / "graph" / name`; archive =
      `dest / f"{name}.tar.gz"`; sidecar =
      `archive.with_name(archive.name + ".sha256")`.
    - Hit: `dest` and the archive exist, and the digest — re-hashed from the
      archive when `verify=True`, else read from the sidecar (missing sidecar
      is a miss) — equals `info.sha256` → return `dest`, zero network.
    - Miss: download to a temp file in `dest.parent` (`requests.get(stream=
      True)`, `raise_for_status`), streaming sha256; mismatch → ValueError +
      cleanup; unpack into a temp dir; single-top-level-dir check (same
      message as today); remove any existing `dest`; move the extracted dir
      to `dest`, the archive into `dest`, and write the sidecar digest. Any
      failure removes the temp files and leaves `dest` untouched.
    - numpydoc docstring with a live-network doctest:
      `graph_dir("generations")` (replaces the `download_graph` one).
  - `download_graph(name)` — deprecated alias of `graph_dir`
    (`DeprecationWarning`, `.. deprecated:: 6.0.0`).
  - `download(name)` — deprecated alias of `graph_dir` (same warning style,
    message points at `graph_dir`).
- Tests (fake response object as in `test_reachable_pairs.py`; a real
  tarball built in `tmp_path` with one top-level dir; `FLPQ_DATA_CACHE`
  pointed at `tmp_path`; `graph_info` monkeypatched to a `GraphInfo` whose
  `sha256` matches the synthetic archive):
  - miss: downloads, verifies, installs — returned path is
    `<root>/<v>/graph/<name>`, contains the unpacked contents + archive +
    sidecar with the registry digest.
  - hit: a second call returns the same path with `requests.get` patched to
    raise (zero network).
  - tamper: corrupt the stored archive; default call still hits (sidecar
    trusted), `verify=True` re-hashes, misses, and reinstalls from the fake
    response.
  - missing sidecar: default call misses (re-downloads); `verify=True` hits
    via the re-hash with no network.
  - HTTP error: `raise_for_status` raises → propagates, `dest` absent, no
    temp files left in the parent.
  - sha mismatch: wrong bytes → ValueError, `dest` absent, no temp files.
  - unknown name → FileNotFoundError (no monkeypatching of requests).
  - `download_graph`/`download` warn and delegate (unknown name → warning +
    FileNotFoundError).
  - keep the URL-constant tests.
- Docs: tutorial "Load graph archive from Dataset" uses `graph_dir`;
  reference page lists `graph_dir` (and keeps the deprecated aliases).

### S3: reachable_pairs.csv — per-version cache copy [done] (a630af9)

**Code:** `flpq_data/dataset/reachable_pairs.py`
**Tests:** Reworked download/precedence tests in
`tests/dataset/test_reachable_pairs.py`
**Docs:** none beyond the existing reference entry (behaviour note in the
`download_reachable_pairs` docstring)

**Spec:**
- `_csv_path()` — `version_dir() / REACHABLE_PAIRS_FILENAME` when present,
  else the bundled `REACHABLE_PAIRS_CSV`.
- `download_reachable_pairs()` — downloads into `version_dir()` (mkdir
  parents), returns the cache path; docstring updated (no more
  `config.DATA`).
- Drop the `DATA` import.
- Tests: the three tests that monkeypatched `rp.DATA` now set
  `FLPQ_DATA_CACHE` (env) instead — download writes to
  `<root>/<v>/reachable_pairs.csv`; the downloaded copy is preferred; the
  bundled fallback when the cache copy is absent.

### S4: Remove DATA/GRAPHS_DIR from config.py; migrate remaining references

**Code:** `flpq_data/config.py`, `.gitignore`, `LICENSE-DATA.txt`, three
live-network test files, `.opencode/skills/add-graph/SKILL.md`
**Tests:** the live-network tests now call `graph_dir` (they download for
real in CI)
**Docs:** CHANGELOG, add-graph skill

**Spec:**
- `config.py`: remove `DATA` and `GRAPHS_DIR` (and their `__all__` entries);
  keep `VERSION`, `DATASET_VERSION`, `ROOT`.
- `.gitignore`: drop the now-orphaned `flpq_data/data` entry.
- `LICENSE-DATA.txt`: the data path reference becomes the machine-global
  cache (the archives are downloaded from object storage, not shipped).
- Live-network tests switch `download_graph` → `graph_dir`:
  `tests/graphs/utils/test_nodes_to_integers.py`,
  `tests/graphs/readwrite/test_rdf.py`,
  `tests/queries/cfpq/generators/test_java_points_to_grammar.py`.
- `.opencode/skills/add-graph/SKILL.md`: step 1 becomes "regenerate
  `flpq_data/dataset/registry.json` with `utils/generate_registry.py`"
  (`GRAPHS` no longer exists); the loading pointer becomes
  `graph_dir(name)`; frontmatter description updated to match.
- CHANGELOG `[Unreleased]`: fix the stale `graphs()` mentions to
  `graph_names()` (three places, left over from the rename task) and note in
  the cache entry that the root is `FLPQ_DATA_CACHE` or the platformdirs
  default.
