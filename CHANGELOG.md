# Changelog

All notable changes to CFPQ_Data are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Optimized WCNF grammar variants for the `java_points_to` and
  `c_alias_analysis` categories, taken from "Optimization of the Context-Free
  Language Reachability Matrix-Based Algorithm" (arXiv:2401.11029,
  optimization 5): every archive of the two categories now carries
  `java_points_to_muravev2024.cnf` / `c_alias_muravev2024.cnf` alongside the
  original grammar. Each variant follows the label convention of its archive
  (indexed `load_i` form or bare `load` family form) and was verified to
  return identical reachable-pair counts to the original with FastMatrixCFPQ
  on small graphs.
- The graph tables on the website now list the download size of every
  archive in a `Size (MB)` column — one unit (MB) for all graphs, from the
  smallest (0.002 MB) to the largest (112.65 MB) archive.
- `utils/upload_to_s3.py` reports the verified archive size (bytes and MB)
  after each upload, and the new `utils/archive_sizes.py` checks or updates
  the `Size (MB)` column of the docs graph tables against the stored
  archives on Yandex S3.
- The publish workflow now runs on every pull request targeting `master`: it
  builds the sdist and wheel and publishes them to TestPyPI (`skip-existing`),
  validating packaging before a release tag is cut.
- Ruff as the linting and formatting gate (rules `E`, `F`, `W`, `I` plus
  `ruff format`), replacing black; the codebase was brought in line in a
  one-time pass.
- Type checking with [ty](https://docs.astral.sh/ty/) for fast local checks
  and Pyright in CI; the package, tests, and utility scripts are now fully
  type-checked.
- A math-snippet guard in the test suite (`utils/check_math_snippets.py`): it
  scans every docs page and rejects math that MathJax cannot render — an
  unescaped underscore inside a text-mode command group (e.g.
  `\textit{a_b}`) — which previously surfaced only as an error on the
  deployed site while the Sphinx build stayed green.
- The MCFG readwrite module `cfpq_data/grammars/readwrite/mcfg.py`: a data
  model for multiple context-free grammars, lark-based parsing of the
  Datalog-like `.mcfg` format specified in `docs/flpq.rst`, semantic
  validation (start symbol, dimension and rank), and `mcfg_from_text` /
  `mcfg_to_text` with round-trip guarantees plus `mcfg_from_txt` /
  `mcfg_to_txt` for file I/O.
- The `category` and `query_class` columns of `reachable_pairs.csv` and the
  matching filters and row fields of the `reachable_pairs()` API: reference
  counts are now keyed per graph category and query class (`cfpq`, `rpq`,
  `mcfpq`).
- The transition-system description style of the `.rsm` format: a query may
  be written as an explicit labelled transition system in addition to the
  CFG (EBNF) style, and `rsa_from_text` accepts both.
- Partial graph archives: `utils/check_archive_structure.py --partial`
  validates an archive that carries only new queries for an existing graph,
  and `utils/merge_archive.py` merges such a partial archive into the
  existing full one.

### Changed

- Development tooling migrated from Poetry to [uv](https://docs.astral.sh/uv/):
  PEP 621 project metadata with hatchling as the build backend, PEP 735
  dependency groups (`dev`, `test`, `docs`) instead of Poetry groups and the
  `setup.py` extras, a committed `uv.lock`, and all CI workflows on
  `astral-sh/setup-uv`.
- The labeled graph generators type their `labels` parameter as
  `Sequence[str]`, correctly accepting both a single label string and a
  sequence of labels (previously annotated `List[str]` despite the string
  default).

### Removed

- The legacy packaging layer: `setup.py`, `MANIFEST.in`, `requirements.txt`,
  and `requirements/` (dependencies now live in `pyproject.toml`).
- The unused `codecov` dev dependency (CI uploads coverage via the Codecov
  GitHub Action).
- The broken utility scripts `utils/fetch_dataset.py` and
  `utils/update_dataset_tables.py` (both failed at import time against the
  5.0.0 package layout).

### Fixed

- The C Alias grammar page rendered the MathJax error "'_' allowed only in
  math mode" instead of the parameter names and the example grammars: the
  page wrapped identifiers containing underscores in `\textit{...}` inside
  math, where an underscore is illegal. Parameter names now use the literal
  style and the reverse labels are plain subscripts (#127).

## [5.0.0] - 2026-09-16

### Added

- Expanded the graph dataset to **113 labeled directed graphs** across eight
  families: C alias analysis (from "Demand-driven Alias Analysis for C", #2),
  RDF/OWL, Java points-to, field-sensitive alias, context-sensitive data-flow,
  data provenance (#16), name resolution (stack graphs), and biological graphs
  from UniProt for subgraph queries by context-free grammars (#26).
- `download_grammars()` to fetch per-graph and example grammars for the
  `c_alias`, `dyck`, `java_points_to`, and `nested_parentheses` templates.
- `download_benchmark()` to fetch benchmark data (e.g. `MS_Reachability`).
- `graph_to_mtx_dir()`, a writer for the per-label MatrixMarket format.
- A developer guide covering pre-commit, the test pipeline, docs build and
  deploy, package deploy, and contribution guidelines (#76).
- Release process documentation and a tag-triggered PyPI publish workflow
  (Trusted Publishing) with a manual TestPyPI validation run (#75, #33).
- A docs prebuild for pull requests: the no-warnings docs build and the full
  link check now run in CI on every push and PR (#74).
- Reference reachable-pair counts for graph × grammar pairs, computed with the
  FastMatrixCFPQ reference implementation and exposed via `reachable_pairs()`
  and a downloadable CSV (#32).

### Changed

- **Breaking:** graph archives are now distributed in the **mtx-per-label**
  format (one Boolean MatrixMarket file per edge label) instead of CSV.
  `download(name)` returns a directory; load a graph with
  `graph_from_mtx_dir(path / "graph")`.
- **Breaking:** the minimum Python version is now **3.11** (was 3.8).
- The whole dataset is served from a single versioned prefix (`5.0.0/graph/`);
  indexed-label files use the bare `<label>.mtx` name.
- Updated dependencies: networkx 3.6, pandas 2.3, rdflib 7.6, pyformlang 1.0.1,
  requests 2.33.

### Fixed

- Broken function documentation links on the Graphs page; unresolved
  cross-references now fail the docs build (nitpicky mode, no-warnings policy),
  and the full link check runs in CI and the pre-merge quality gate (#122).

### Notes

- This release completes most of the long-standing "Make CFPQ_Data better"
  backlog (#28): its earlier sub-items (networkx-based graph generators #27,
  updated synthetic graphs #30, graph size information #20) shipped in previous
  releases and remain in effect. The static-analysis data item (#2) is only
  partially complete: the "Demand-driven Alias Analysis for C" graphs are now
  documented with their source, while the "Batch Alias Analysis" data is still
  missing.
