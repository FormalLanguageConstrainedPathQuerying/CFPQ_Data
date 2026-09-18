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

1. Add the graph name to `DATASET` in `cfpq_data/dataset/data.py`.
2. The graph archive must be uploaded under the dataset URL
   `https://cfpq-data.storage.yandexcloud.net/{VERSION[0]}.0.0/graph/<name>.tar.gz`.
3. Loading happens via `download(name)` (which returns the graph directory)
   and `graph_from_mtx_dir(path / "graph")`
   (`cfpq_data/graphs/readwrite/mtx.py`).

## Documentation

1. Create the per-graph page `docs/graphs/data/<name>.rst`, following the
   structure of an existing page (description, statistics tables). The page
   carries **no** grammar section: canonical grammars are documented once on
   the category page. Statistics conventions: the PR template is the source
   of truth.
2. Handle the grammar case from the PR template's "Canonical grammars"
   section:
   - *existing category, existing grammar(s)* — nothing to add; the new table
     row fills in the matching column(s);
   - *new grammar for an existing category* — append the grammar to the
     category page's "Canonical grammars" section and add a column to its
     table;
   - *new category* — create `docs/graphs/<category>.rst` with the category
     description, the graph table (one column per grammar), and the
     "Canonical grammars" section.
3. Register it **twice**: a row in the per-category table of its source area
   (`docs/graphs/<category>.rst`) and an entry in the matching captioned
   toctree of `docs/graphs/index.rst` (the left navigation bar is generated
   from those toctrees). Keep both in the same order, and bump the category's
   graph count in the Contents table of `docs/graphs/index.rst`. For a new
   category, also add its page to the `docs/graphs/index.rst` toctree and a
   row to the Contents table.
 4. Fill the new row's `Size (MB)` cell with the size the upload tool
   reported, then run `python utils/archive_sizes.py --update` before
   committing so every table row — including the new one — matches S3 (see
   the "Archive sizes" section of `docs/utils.rst`).

Note: a `data/*.rst` page missing from all toctrees produces only a Sphinx
*warning*, not an error, so the docs quality gate will not catch it — check
the build log for "not included in any toctree".

See also `.opencode/skills/run-tests` to verify, and the Graphs page of the
docs for the full list of names.
