---
name: add-graph
description: Use when adding a new graph to the CFPQ_Data dataset. Covers the CSV data format, the download()/DATASET wiring, and the PR/issue templates.
---

# Add a graph to the dataset

## Source of truth

The required fields and metadata live in the GitHub templates — do **not**
duplicate them here:

- `.github/PULL_REQUEST_TEMPLATE/new_graph.md`
- `.github/ISSUE_TEMPLATE/graph-add-template.md`

Fill in every field in the triangle brackets (`<>`) of those templates.

## Data format

A graph is a 3-column space-separated CSV with **no header**:

| Column | Type | Meaning |
|:---:|:---:|---|
| 1 | int | tail of the edge |
| 2 | int | head of the edge |
| 3 | str | label of the edge |

## Wiring a new graph into the code

1. Add the graph name to `DATASET` in `cfpq_data/dataset/data.py`.
2. The graph archive must be uploaded under the dataset URL
   `https://cfpq-data.storage.yandexcloud.net/{VERSION[0]}.0.0/graph/<name>.tar.gz`
   containing `<name>/<name>.csv`.
3. Loading happens via `download(name)` -> `graph_from_csv(path)`
   (`cfpq_data/graphs/readwrite/csv.py`).

See also `.opencode/skills/run-tests` to verify, and the `README.rst`
"Dataset content" section for the full list of names.
