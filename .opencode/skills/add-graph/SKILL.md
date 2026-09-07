---
name: add-graph
description: Use when adding a new graph to CFPQ_Data. Covers the mtx-per-label archive format, the download()/DATASET wiring, and the PR/issue templates.
---

# Add a graph to the dataset

## Source of truth

The required fields and metadata live in the GitHub templates — do **not**
duplicate them here:

- `.github/PULL_REQUEST_TEMPLATE/new_graph.md`
- `.github/ISSUE_TEMPLATE/graph-add-template.md`

Fill in every field in the triangle brackets (`<>`) of those templates.

## Data format

The archive layout and the label conventions are documented once in the
"File structure" section of `docs/graphs/index.rst` — follow it exactly:
`<name>.tar.gz` unpacks to `<name>/{README.md, grammar/, graph/}`, where
`graph/` holds one Boolean MatrixMarket pattern file per edge label.

## Wiring a new graph into the code

1. Add the graph name to `MIGRATED_DATASET` in `cfpq_data/dataset/data.py`
   (the graphs served from `DATASET_URL`, the current version prefix).
2. The graph archive must be uploaded under the dataset URL
   `https://cfpq-data.storage.yandexcloud.net/{VERSION[0]}.0.0/graph/<name>.tar.gz`.
3. Loading happens via `download(name)` (which returns the graph directory)
   and `graph_from_mtx_dir(path / "graph")`
   (`cfpq_data/graphs/readwrite/mtx.py`).

See also `.opencode/skills/run-tests` to verify, and the Graphs page of the
docs for the full list of names.
