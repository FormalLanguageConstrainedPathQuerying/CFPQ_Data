<!-- ⚠ To suggest a new graph, you must fill in all the fields in the triangle brackets(``<>``) ⚠ -->

## Info
| | |
|---|---|
| Full Name | ``<Specify the full name of the graph>`` |
| Category | ``<Existing category name, or "new: <proposed name>" for a new category>`` |
| Version | ``<Current version of CFPQ_Data>`` |
| Origin | [link](``<Link to download the graph>``) |

## Data format

The archive must follow the standard layout described in the "File structure" section of the [Graphs page](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html): `<name>.tar.gz` unpacks to a self-contained directory with `README.md`, `graph/` (one Boolean MatrixMarket pattern file per stored edge label), and `queries/` (one file per query in `cfpq/`, `rpq/`, or `mcfpq/`, each described in `queries/README.md`).

## Description document

The archive's `README.md` must answer all of these questions (one `##` section each):
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

## Graph Statistics
| Num Nodes | Num Edges |
|:---:|:---:|
| ``<The number of nodes in the new graph>`` | ``<The number of stored edges in the new graph>`` |

## Edges Statistics
| Edge Label | Num Edge Label |
|---:|---:|
| ``<The type of the edge label of the new graph >`` | ``<The number of edges in the new graph of this type>`` |

List the stored labels only (no `_r` reversed-edge rows). A family of indexed labels (e.g. `load_0`, ..., `load_857`) is listed once with a placeholder subscript (e.g. `load_f`) and a note listing the index set.

## Queries

Canonical grammars are documented on the category page, not on the per-graph page. Pick the case that applies:

1. **Graph for an existing category** — name the grammar(s) from the category's "Canonical grammars" section that apply to this graph; they become the table column(s) filled in for the new row. No new grammar text on the site.
2. **New grammar for an existing category** — provide the grammar below; it will be added to the category page and a new column to its table.
3. **Graph for a new category** — provide the canonical grammar(s) below; a new category page will be created with them.

Every query that applies to this graph must also ship inside the archive: one file per query in `queries/cfpq/` (`.cnf`), `queries/rpq/` (`.re`), or `queries/mcfpq/` (`.mcfg`), each described in a `## <class>/<file>` section of `queries/README.md`. A query may only use labels of this graph.

<LaTeX format of grammar (only for cases 2 and 3)>

<File-format text of the grammar — .cnf, .re, or .mcfg (only for cases 2 and 3)>
