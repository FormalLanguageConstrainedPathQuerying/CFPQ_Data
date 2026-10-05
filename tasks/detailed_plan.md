# Detailed Plan: Task 149 — Design doc: record the core rework decisions in docs/flpq.rst

Part of hub #148 (end-user core rework; global plan comment on the hub).
Docs-only task: no `.py` changes — code-specific gates (tests, lint, format)
are skipped per the workflow rules; the docs build gate still applies.

## Context

The core rework decisions (hub #148 body + confirmed user decisions) must be
documented before any implementation (workflow rule). This task records them
in `docs/flpq.rst` — the persistent design record — and aligns the two
layout pointers (AGENTS.md, CHANGELOG). It cites #140 (cache) and #147
(category exposure) as the drivers.

### S1: Record the core rework design in docs/flpq.rst [done] (45bd1aa)

**Code:** none (docs-only subtask)
**Tests:** n/a — no code; the docs build gate applies at merge time
**Docs:** `docs/flpq.rst` — update the "Package structure" tree (`config.py`
line: drop "data directories"; `dataset/` line: registry + metadata API,
machine-global cache, lazy access); add a new top-level section "Core API:
metadata, lazy access, and cache" after "Dataset layout and migration"

**Spec:**
- New section content, in this order:
  - Intro paragraph: the core is for end users (dataset utilisation for
    benchmarks and statistical analysis); dataset maintenance (archive
    validation, upload, merge, registry generation) lives in repo-only
    `utils/` scripts, never installed with the wheel; cite #140 and #147 as
    the drivers.
  - "Graph registry" subsection: the `flpq_data/dataset/registry.json`
    schema (version + per-graph records: category, num_nodes, num_edges,
    size_mb, sha256, queries[{class, name, representations}]) with a JSON
    example; the source of each field (category/graph list from
    `reachable_pairs.csv`, nodes/edges from MTX headers, size from the
    stored object, sha256 of the `.tar.gz`, queries from the archive's
    `queries/` tree); generation by repo-only `utils/generate_registry.py`
    (pattern of `utils/archive_sizes.py`, local-only, never in CI);
    publication to S3 as `<version>/registry.json`; bundling in the wheel.
  - Metadata API: `graphs() -> list[str]`, `graph_info(name) -> GraphInfo`
    (frozen dataclass mirroring one registry record), `categories() ->
    dict[str, list[str]]` (the #147 mapping); the metadata path never
    touches the network; the never-released `GRAPHS`/`DATASET` constants are
    dropped and the future `cfpq-data` shim maps `DATASET -> graphs()`.
  - "Machine-global cache" subsection: root = `FLPQ_DATA_CACHE` env var >
    `platformdirs.user_cache_dir("flpq-data")` with the per-OS defaults
    (Linux `~/.cache/flpq-data`, macOS `~/Library/Caches/flpq-data`,
    Windows `%LOCALAPPDATA%\flpq-data\Cache`); per-user and shared across
    projects, not tied to a venv or install dir; the in-package data dir
    (`config.DATA`/`GRAPHS_DIR`) is removed.
  - Cache layout: mirrors the dataset, version root, several versions
    coexist — the tree `<root>/<version>/reachable_pairs.csv` and
    `<root>/<version>/graph/<name>/<name>.tar.gz` plus the unpacked contents
    in the same folder.
  - "Lazy access" subsection: `graph_dir(name)` is the single data accessor;
    name validated against the bundled registry; hit = folder present +
    archive sha256 (sidecar `.sha256` written at install) matches the
    registry -> return the path with zero network, `verify=True` re-hashes;
    miss = download to a temp file with `raise_for_status`, stream-verify
    sha256, extract, single-top-dir check, atomic move into the cache, any
    failure leaves the cache untouched; `download_graph`/`download` remain
    deprecated aliases; `reachable_pairs.csv` resolves to the per-version
    cache copy when present else the bundled file.
  - "Cache manipulation" subsection: `cache_root() -> Path`,
    `cached_versions() -> list[str]`, `clear_cache(keep: str | None = None)`
    (removes version dirs under the root except `keep`; `None` removes all;
    returns the removed paths).
- "Package structure" tree update: `config.py` line becomes "version"; the
  `dataset/` line becomes "registry + metadata API, machine-global cache
  with lazy access (`graph_dir`), reachable pairs".

### S2: Update AGENTS.md package layout and CHANGELOG [done] (fb6985c)

**Code:** none (docs-only subtask)
**Tests:** n/a — no code; the docs build gate applies at merge time
**Docs:** `AGENTS.md` (package-layout bullets for `config.py` and
`dataset/`), `CHANGELOG.md` (`[Unreleased]` entry for the design decision),
`tasks/global_plan.md` (mark T1 done)

**Spec:**
- AGENTS.md: `flpq_data/config.py` bullet becomes "version"; the
  `flpq_data/dataset/` bullet becomes "graph registry + metadata API,
  machine-global cache with lazy access (`graph_dir`), reachable-pair counts
  (`reachable_pairs`)".
- CHANGELOG `[Unreleased]`: add an entry recording that the core rework
  design (end-user core vs repo-only maintenance utils, per-graph registry,
  machine-global versioned cache, lazy `graph_dir`, cache manipulation API)
  is documented in `docs/flpq.rst` — implementation follows in #150–#152.
- Global plan: mark T1 (#149) done.
- This is the last subtask: the commit carries `Closes #149` as a standalone
  line.
