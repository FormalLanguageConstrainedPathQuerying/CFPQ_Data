name: ADD NEW GRAPH
about: Suggest new graph to this project
title: "[NEW GRAPH] <Graph brief description>"
labels: new data
assignees: rustam-azimov, vadyushkins

---

<!-- ⚠ To suggest a new graph, you must fill in all the fields in the triangle brackets(``<>``) ⚠ -->

## Info
| | |
|---|---|
| Type | ``<new graph (full archive) or new queries for an existing graph (partial archive)>`` |
| Full Name | ``<The full name of the graph — for a partial archive, the name of the existing graph being extended>`` |
| Category | ``<Existing category name, or "new: <proposed name>" for a new category (new graphs only)>`` |
| Version | ``<Current version of CFPQ_Data>`` |
| Archive | [link](``<Google Drive link to the archive — <name>.tar.gz, full or partial>``) |

## Data format

The main way to provide data is a **Google Drive link** to an archive prepared per the structure-validation tool. Two kinds of archives exist (both documented in the "File structure" section of the [Graphs page](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html)):

- **Full archive** — a new graph: `<name>.tar.gz` unpacks to a self-contained directory with `README.md`, `graph/` (one Boolean MatrixMarket pattern file per stored edge label), and `queries/` (one directory per query in `cfpq/`, `rpq/`, or `mcfpq/`; each query directory holds every representation of the query — `.cnf`/`.rsm`, `.re`/`.rsm` (regular only), or `.mcfg` — plus one `results.mtx` with the constrained reachability facts).
- **Partial archive** — new queries for an existing graph: `<name>.tar.gz` unpacks to a directory containing only `queries/` — the new query directories (same layout) plus a `README.md` fragment with one `## <class>/<query>` section per new query.

Validate the archive before sharing it:

```
python utils/check_archive_structure.py <name>.tar.gz            # full archive
python utils/check_archive_structure.py <name>.tar.gz --partial  # partial archive
```

A partial archive is merged into the existing graph archive by the maintainer (`python utils/merge_archive.py EXISTING.tar.gz PARTIAL.tar.gz -o <name>.tar.gz`), re-validated, and uploaded. The query file formats — including the recursive state machine (`.rsm`) format — are documented on the [FLPQ design page](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/flpq.html).

## Description document

**Full archive.** The archive's `README.md` must answer all of these questions (one `##` section each):
| | |
|---|---|
| What is this graph? | ``<A short description of the domain and what the graph models>`` |
| Source | ``<Where the data comes from (paper, dataset, tool) and the full citation>`` |
| Construction | ``<How the graph was built, extracted, or generated (method, parameters)>`` |
| Nodes | ``<What a node represents and the total number of nodes>`` |
| Edges and labels | ``<What each label family means and the number of edges per label>`` |
| Query classes | ``<Which of RPQ, CFPQ, MCFPQ apply to this graph and why>`` |
| License | ``<The license of the data>`` |
| Caveats | ``<Known limitations or approximations, or "None">`` |

**Partial archive.** Instead of a full description document, the `queries/README.md` fragment carries one `## <class>/<query>` section per new query, each describing the language (in words and/or in LaTeX) and its purpose on this graph.

*New graphs only — a partial archive adds no nodes or edges.*

## Graph Statistics
| Num Nodes | Num Edges |
|:---:|:---:|
| ``<The number of nodes in the new graph>`` | ``<The number of stored edges in the new graph>`` |

## Edges Statistics
| Edge Label | Num Edge Label |
|---:|---:|
| ``<The type of the edge label of the new graph >`` | ``<The number of edges in the graph of this type>`` |

List the stored labels only (no `_r` reversed-edge rows). A family of indexed labels (e.g. `load_0`, ..., `load_857`) is listed once with a placeholder subscript (e.g. `load_f`) and a note listing the index set.

## Queries

Canonical grammars are documented on the category page, not on the per-graph page. Pick the case that applies:

1. **Graph for an existing category** — name the grammar(s) from the category's "Canonical grammars" section that apply to this graph; they become the table column(s) filled in for the new row. No new grammar text on the site.
2. **New grammar for an existing category** — provide the grammar below; it will be added to the category page and a new column to its table.
3. **Graph for a new category** — provide the canonical grammar(s) below; a new category page will be created with them.

Every query you provide must ship inside the archive (a full archive ships all queries of the graph; a partial archive ships the new ones): one directory per query in `queries/cfpq/`, `queries/rpq/`, or `queries/mcfpq/`, holding every representation of the query (`.cnf`/`.rsm`, `.re`/`.rsm` — regular only, or `.mcfg`) plus one `results.mtx` with the constrained reachability facts (a Boolean pattern matrix with the graph's dimensions; an entry `(i, j)` means some path from node `i` to node `j` satisfies the query). Each query directory is described in a `## <class>/<query>` section of `queries/README.md`. A query may only use labels of this graph.

<LaTeX format of grammar (only for cases 2 and 3)>

<File-format text of the grammar — .cnf, .rsm, .re, or .mcfg (only for cases 2 and 3)>
