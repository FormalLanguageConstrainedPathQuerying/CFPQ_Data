# Changelog

All notable changes to CFPQ_Data are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

The changes below make up the upcoming **5.0.0** release.

### Added

- Expanded the graph dataset to **113 labeled directed graphs** across eight
  families: C alias analysis, RDF/OWL, Java points-to, field-sensitive alias,
  context-sensitive data-flow, data provenance, name resolution (stack graphs),
  and biological graphs from UniProt.
- `download_grammars()` to fetch per-graph and example grammars for the
  `c_alias`, `dyck`, `java_points_to`, and `nested_parentheses` templates.
- `download_benchmark()` to fetch benchmark data (e.g. `MS_Reachability`).
- `graph_to_mtx_dir()`, a writer for the per-label MatrixMarket format.

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
