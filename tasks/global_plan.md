# Global Plan: End-user core rework (hub #148)

Rework the package core for end users: dataset utilisation for benchmarks
and statistical analysis. The core (`flpq_data/`) is split from dataset
maintenance utils (repo-only `utils/`). Driven by #140 (cache downloaded
graph datasets) and #147 (expose the dataset category of each graph).

## Decisions (confirmed with the user)

| # | Decision | Choice |
|---|---|---|
| 1 | Metadata storage | New per-graph `registry.json` (bundled + published per S3 version) |
| 2 | Cache layout | Per-graph folder: archive + unpacked contents together; version root mirrors the S3 prefix |
| 3 | Accessor name | `graph_dir(name)`; `download_graph`/`download` become deprecated aliases |
| 4 | Version selection | Current dataset version only (no `version=` param); cache stays version-structured |
| 5 | Loader scope | Metadata + local paths only (no convenience loaders) |

## Target design

**Boundary.** `flpq_data/` = end-user core (lazy dataset access, metadata,
graph/query I/O). `utils/` = maintenance (validation, upload, merge, registry
generation) — repo-only, never installed. `config.DATA`/`GRAPHS_DIR` removed;
the boundary is documented in `docs/flpq.rst` + AGENTS.md.

**Registry schema** (`flpq_data/dataset/registry.json`, published as
`<version>/registry.json` on S3):

```json
{ "version": "6.0.0",
  "graphs": { "skos": { "category": "rdf", "num_nodes": 144, "num_edges": 252,
                        "size_mb": 0.003, "sha256": "…",
                        "queries": [ {"class": "cfpq",
                                      "name": "nested_parentheses_subClassOf",
                                      "representations": ["cnf", "rsm"]} ] } } }
```

**Cache layout.** Root = `FLPQ_DATA_CACHE` env var >
`platformdirs.user_cache_dir("flpq-data")` (new dependency; OS default:
`~/.cache/flpq-data`, `~/Library/Caches/…`, `%LOCALAPPDATA%\…\Cache`).
"Machine-global" = per-user, shared across projects — not tied to a venv or
install dir.

```
<root>/6.0.0/
├── reachable_pairs.csv      # per-version copy (replaces flpq_data/data/)
└── graph/<name>/<name>.tar.gz + README.md, graph/*.mtx, queries/…   (unpacked in the same folder)
```

Multiple dataset versions coexist under `<root>/`.

**Lazy `graph_dir(name)`.** Validate the name against the bundled registry →
if `<root>/<v>/graph/<name>/` exists with an archive whose sha256 matches the
registry → return the path, zero network. Else: download to a temp file →
`raise_for_status` → stream-verify sha256 → extract → single-top-dir check →
atomic move into the cache. Integrity on hit: a sidecar `.sha256` written at
install is compared against the registry (fast path); `verify=True` re-hashes
the archive.

**Metadata API.** `graph_names() -> list[str]` (named to avoid clashing
with the `flpq_data.graphs` subpackage), `graph_info(name) -> GraphInfo`
(frozen dataclass), `categories() -> dict[str, list[str]]` (#147). The
never-released `GRAPHS`/`DATASET` constants are dropped (6.0.0 is pre-release;
the future `cfpq-data` shim maps `DATASET -> graph_names()`).

**Cache manipulation.** `cache_root() -> Path`, `cached_versions() ->
list[str]`, `clear_cache(keep: str | None = None)` — `None` wipes all version
dirs, `keep="6.0.0"` keeps only that one.

## Tasks

- **T1** (#149) [done]: Design doc — record all decisions in `docs/flpq.rst`
  (boundary, registry schema + generation/publication, cache layout/lifecycle/
  integrity, full API incl. deprecations; cite #140/#147); AGENTS.md
  package-layout lines; CHANGELOG `[Unreleased]`. Docs-only task.
- **T2** (#150) [done]: Graph registry + metadata API (closes #147) —
  `utils/generate_registry.py` (maintenance; pattern of
  `utils/archive_sizes.py`), bundled `registry.json`, `GraphInfo`/`graph_names()`/
  `graph_info()`/`categories()`, drop `GRAPHS`/`DATASET`.
- **T3** (#151) [done]: Machine-global versioned cache + lazy downloads
  (closes #140) — `platformdirs` dependency, `cache.py` (`cache_root()` with
  env-var override), lazy `graph_dir()` with checksum verification and atomic
  install, `reachable_pairs.csv` moved into the per-version cache, in-package
  data dir removed.
- **T4** (#152): Cache manipulation API — `clear_cache(keep=None)` + tests +
  docs.

## Dependencies

T1 → T2 → T3 → T4. T2 must precede T3 (the registry carries the checksums T3
verifies and replaces `GRAPHS` for name validation). T4 needs T3's structure.
No file-set conflicts between tasks beyond `data.py`/docs, which are
sequential anyway.

## Notes

- **Execution order**: T1 → T2 → T3 → T4, one feature branch per task, merge
  to `dev` after the quality gate; each subtask commit carries its own
  `<issue>-S<n>` identifier; the last subtask commit of a task carries
  `Closes #<own issue>` plus `Closes #147` (T2) / `Closes #140` (T3).
- **No-network test policy**: download paths are tested with monkeypatched
  `requests.get` and real tarballs built in `tmp_path`; the cache root is
  redirected via `FLPQ_DATA_CACHE`. The registry generator is a local-only
  maintenance script (like `utils/archive_sizes.py`) — CI never runs it.
- **Coverage gate** ≥95% line+branch applies to all new package code.
- **Doctests**: `--doctest-modules` runs over the package; network examples
  follow the existing SKIP convention.
- The in-package `flpq_data/data/` dir (gitignored scratch) is orphaned by T3
  — no migration; users re-download into the new cache.
