# Changelog

All notable changes to CFPQ_Data are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
