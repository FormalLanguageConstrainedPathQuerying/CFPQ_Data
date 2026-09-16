<!-- ⚠ To suggest a new graph, you must fill in all the fields in the triangle brackets(``<>``) ⚠ -->

## Info
| | |
|---|---|
| Full Name | ``<Specify the full name of the graph>`` |
| Version | ``<Current version of CFPQ_Data>`` |
| Origin | [link](``<Link to download the graph>``) |

## Data format

The archive must follow the standard layout described in the "File structure" section of the [Graphs page](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html): `<name>.tar.gz` unpacks to `<name>/{README.md, grammar/, graph/}`, where `graph/` holds one Boolean MatrixMarket pattern file per edge label.

## Graph Statistics
| Num Nodes | Num Edges |
|:---:|:---:|
| ``<The number of nodes in the new graph>`` | ``<The number of stored edges in the new graph>`` |

## Edges Statistics
| Edge Label | Num Edge Label |
|---:|---:|
| ``<The type of the edge label of the new graph >`` | ``<The number of edges in the new graph of this type>`` |

List the stored labels only (no `_r` reversed-edge rows). A family of indexed labels (e.g. `load_0`, ..., `load_857`) is listed once with a placeholder subscript (e.g. `load_f`) and a note listing the index set.

## Canonical grammars

<LaTeX format of grammar>

<Pyformlang CFG format of grammar>
