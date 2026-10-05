# Detailed Plan: Task 153 — Streaming graph format conversion

Issue #153. Driven by #138 (MTX→TXT through `nx.MultiDiGraph` peaks at ~4 GiB
for ~100 MB of input). Design decisions are recorded in the issue body and,
from S1 on, in the "Format conversion" section of `docs/graphs/index.rst`.

## Context

Every graph reader/writer in `flpq_data/graphs/readwrite/` uses an in-memory
`nx.MultiDiGraph` as the intermediate representation. For large graphs the nx
per-edge overhead dominates memory. The fix: conversion runs over an **edge
stream** — a lazy `Iterator[(u, label, v)]` in TXT's `FROM LABEL TO` order —
with one streaming reader and one streaming writer per format, composed by a
single dispatcher. NetworkX stays where it earns its place (generators,
adjacency utils, `materialize`, the existing `graph_from_*`/`graph_to_*` API).

Formats: `mtx` (dir of per-label Boolean MatrixMarket files), `txt`
(`FROM LABEL TO` lines), `rdf` (Turtle; fixed to valid RDF 1.1), `g`
(FastMatrixCFPQ `.g` text, dst-only), `graph` (in-memory `nx.MultiDiGraph`,
src-only). **CSV is removed** (redundant with TXT — same line-per-edge format,
only the column order differed; no dataset impact, archives are MTX-only);
the `pandas` dependency drops with it.

Conversion matrix (RAM): mtx-dir→txt/g = O(1) stream (the #138 case);
any→mtx = single pass + one temp file per label (O(1) RAM, O(E) disk);
rdf-as-source = materialized (rdflib has no streaming parser — documented).

### S1: Design doc — "Format conversion" section + AGENTS.md layout line [done] (f084360)

**Code:** none (docs-only subtask)
**Tests:** n/a
**Docs:** `docs/graphs/index.rst` (new "Format conversion" section after
"File structure"), `AGENTS.md` (package-layout line for `flpq_data/graphs/`)

**Spec:**
- The section records, with rationale: the edge-stream IR and its tuple
  convention `(u, label, v)`; the formats table (mtx/txt/rdf/g + the in-memory
  graph object) — the single source of truth for what each format is; the
  conversion matrix with RAM characteristics; the RDF encoding spec (new
  valid-RDF form `urn:flpq:node:<id>` / `urn:flpq:label:<label>`, streamed,
  one triple per line; legacy Literal-predicate files remain readable); `.g`
  as dst-only; the NetworkX boundary (generators, adjacency utils,
  `materialize`, `graph_from_*`/`graph_to_*` stay nx-based); the CSV removal
  rationale.
- AGENTS.md: the `flpq_data/graphs/` line gains `converters`.

### S2: Streaming edge readers [done] (ceeb631)

**Code:** `flpq_data/graphs/readwrite/mtx.py` (`iter_edges_from_mtx_dir`),
`txt.py` (`iter_edges_from_text`, `iter_edges_from_txt`), `rdf.py`
(`iter_edges_from_rdf` + private `_node_id`/`_label` dual-encoding helpers);
exports via the existing star import in `readwrite/__init__.py`. Reuse:
`_MTX_HEADER` constant (mtx.py), the line-streaming pattern of
`utils/check_archive_structure.py::_mtx_entries` (repo-only, so re-implemented
in-package rather than imported), shlex parsing of `graph_from_text`.
**Tests:** Extend `tests/graphs/readwrite/test_mtx.py`, `test_txt.py`,
`test_rdf.py`; doctests in the new functions.
**Docs:** numpydoc docstrings with `Examples`.

**Spec:**
- All readers are lazy generators yielding `(u, label, v)`; node ids keep
  their parsed type (`int` from MTX, `str` from TXT/RDF).
- `iter_edges_from_mtx_dir(path)`: for each sorted `*.mtx`, stream line by
  line (no whole-file read — the current `graph_from_mtx_dir` reads each file
  into a list; the reader must not); validate the two-line header and the
  dimension line, yield one tuple per entry, raise `ValueError` when the
  entry count differs from the declared nnz (same messages as today).
- `iter_edges_from_text(text)` / `iter_edges_from_txt(path)`: `shlex.split`
  per line, same `ValueError` message as the current `graph_from_text`.
- `iter_edges_from_rdf(path)`: `rdflib.Graph().parse()` (materialized — no
  streaming parser exists; documented in the docstring); for each triple
  yield `(_node_id(s), _label(p), _node_id(o))` where `_label` returns
  `str(pred)` for a legacy `Literal` predicate and the suffix after
  `urn:flpq:label:` for an IRI predicate; `_node_id` returns the bnode
  identifier for a legacy blank node and the suffix after `urn:flpq:node:`
  for an IRI.

### S3: Streaming edge writers [done] (89ba9ab)

**Code:** `txt.py` (`txt_from_edges`), `mtx.py` (`mtx_dir_from_edges` +
private `_node_index`), `rdf.py` (`rdf_from_edges` + private `_iri`; the S2
reader helpers now percent-decode so writer/reader round-trip);
`flpq_data/graphs/utils/to_g_text.py` (the `.g` line logic extracted into a
private `_g_lines` emitter shared by `graph_dir_to_g_text` and the new
`g_text_from_edges` file writer — reuse of its `_INDEXED_RE` /
`_reverse_label`). Reuse: `_MTX_HEADER`, `label_to_filename`, the line format
of `graph_to_text`.
**Tests:** Extend `tests/graphs/readwrite/test_mtx.py`, `test_txt.py`; new
RDF writer tests (rdflib re-parse: every predicate is a `URIRef`; escaping of
labels containing spaces, unicode, and `<>"{}|^`\`#`; round-trip through
`iter_edges_from_rdf`); golden check of the `.g` emitter against the current
`graph_dir_to_g_text` output (its doctest stays green).
**Docs:** numpydoc docstrings with `Examples`.

**Spec:**
- All writers consume an edge iterator and run in O(1) RAM.
- `txt_from_edges(edges, path, *, quoting=False) -> Path`: one line per edge,
  identical formatting to the current `graph_to_text`.
- `mtx_dir_from_edges(edges, path, *, dimension=None) -> Path`: single pass;
  accepts `int` or digit-string node ids (else `TypeError`, same message as
  the current `graph_to_mtx_dir`); tracks the max endpoint; each label's edges
  are appended to its own temp file in the destination directory (a suffix
  that is not `.mtx`, so a concurrent reader never sees it) with **at most
  one temp file open at a time** — close-on-switch, reopen on return: the
  dataset graphs carry up to ~1600 labels (avrora), so one handle per label
  would exhaust the fd limit; on exhaustion every label file is finalized
  with the three-line header — dimension `dimension` when given, else max
  endpoint + 1 (`ValueError` if the given dimension is too small) — by
  streaming the body from the temp file, which is then removed. Temp files
  are cleaned up if the stream raises. A label with zero edges produces no
  file (as today).
- `rdf_from_edges(edges, path) -> Path`: streams valid Turtle, one line per
  edge: `<urn:flpq:node:<id>> <urn:flpq:label:<label>> <urn:flpq:node:<id>> .`
  with the variable IRI components percent-encoded (`urllib.parse.quote`,
  `safe=""`); no rdflib on the write path.
- `.g` emitter: for each `(u, label, v)` yield the forward line and the
  auto-reversed line; indexed labels (`X_N`) collapse to `X_i` with the index
  as a fourth column — byte-identical to today's `graph_dir_to_g_text`.

### S4: Drop CSV; reimplement `graph_from_*`/`graph_to_*` on streams [done] (20d46de)

**Code:** delete `flpq_data/graphs/readwrite/csv.py` and its import line in
`readwrite/__init__.py`; drop `pandas` from `pyproject.toml` (its only user)
and re-sync the env; `mtx.py` (`graph_from_mtx_dir` builds the graph from
`iter_edges_from_mtx_dir`; `graph_to_mtx_dir` routes through
`mtx_dir_from_edges` with `dimension = max(graph.nodes(), default=-1) + 1` to
preserve isolated-node behavior exactly); `txt.py` (`graph_from_text/txt`
from the readers; `graph_to_text` yields one line per edge using
`data["label"]`; `graph_to_txt` via `txt_from_edges`; the line format is a
shared private `_text_line` used by both); `rdf.py` (`graph_from_rdf` from
`iter_edges_from_rdf`; `graph_to_rdf` via `rdf_from_edges` — output is now
the valid encoding, doctests updated to use `graph_from_text` for the sample
graph); new `readwrite/graph.py` with `iter_edges_from_graph(graph)` yielding
`(u, data["label"], v)` per edge key (kept out of converters.py to avoid an
import cycle — converters imports the readwrite modules).
**Tests:** existing suite green; `rdf.py` doctests updated (new encoding +
`graph_from_text` sample); no `test_csv.py` exists to delete.
**Docs:** docstring updates where internals are described.

**Spec:**
- Equivalence: same public signatures, same error types and messages for the
  MTX/TXT readers; `graph_to_mtx_dir` output byte-identical for graphs whose
  nodes all have edges (isolated-node dimension preserved via the explicit
  `dimension` argument).
- `graph_to_text` alignment: one line per edge with `data["label"]` — matches
  `graph_to_mtx_dir`, which already requires the key; documented in S1.
- CSV removal is final (no deprecation shim): `flpq_data.graph_from_csv` /
  `graph_to_csv` disappear at 6.0.0 (pre-release).

### S5: `convert_graph` dispatcher + `to_g_text` refactor [done] (ca721c5)

**Code:** `flpq_data/graphs/converters.py` (`convert_graph`, the format
registry, public exports; the `.g` writer is composed from
`to_g_text.g_text_from_edges`, which S3 already refactored over the shared
emitter); export chain in `flpq_data/graphs/__init__.py`.
**Tests:** new `tests/graphs/test_converters.py`: all-pairs round-trip
(src ∈ {mtx, txt, rdf, graph} × dst ∈ {mtx, txt, rdf, g}) on a small
multi-label graph with parallel edges and an indexed label; error cases
(unknown format, `g` as src, `graph` as dst); an MTX→TXT doctest mirroring
the #138 scenario.
**Docs:** numpydoc docstring with `Examples` for `convert_graph`.

**Spec:**
- `convert_graph(src, dst, *, src_format, dst_format, **writer_options) ->
  Path`; formats are explicit strings (no extension guessing — an MTX
  directory is ambiguous with a single `results.mtx` file); the registry maps
  each format to its reader/writer: `mtx`, `txt`, `rdf` bidirectional; `g`
  dst-only; `graph` src-only (`src` is then an `nx.MultiDiGraph`, not a
  path). `ValueError` for an unknown format or an unsupported direction,
  listing the supported formats. `writer_options` are forwarded to the writer
  (e.g. `quoting` for txt).

### S6: Docs completion — reference, tutorial, CHANGELOG [ ]

**Code:** none (docs-only subtask)
**Tests:** docs build gate
**Docs:** new `docs/reference/graphs/graphs_converters.rst` + toctree entry in
`docs/reference/graphs/index.rst`; autosummary entries for the new functions
on the readwrite reference page; remove `csv` from
`docs/reference/graphs/graphs_readwrite.rst` and delete
`docs/reference/graphs/generated/flpq_data.graphs.readwrite.csv.rst`; new
"Convert graph format" section in `docs/tutorial.rst` (MTX→TXT example — the
#138 use case); CHANGELOG `[Unreleased]`: Added (streaming readers/writers,
`convert_graph`, valid-RDF encoding), Removed (`graph_from_csv` /
`graph_to_csv`, the `pandas` dependency), Changed (RDF output is now valid
RDF 1.1 — legacy files remain readable; `graph_to_text` emits one line per
edge via `data["label"]`).

**Spec:** follow the `documentation` skill mapping; no fact duplicated that
the S1 section already holds (reference pages and tutorial cross-link it).

## Notes

- **Execution order**: S1 → S2 → S3 → S4 → S5 → S6, one commit per subtask
  (`<type>(153-SN): …`); the last subtask's commit carries `Closes #153` and
  `Closes #138` as standalone lines.
- **No-network test policy**: all tests use `tmp_path` fixtures; no dataset
  downloads (the existing `test_rdf.py::test_rdf` already downloads — it must
  keep passing, but new tests do not add network dependence).
- **Coverage gate** ≥95% line+branch applies to all new package code.
- **Doctests**: `--doctest-modules` runs over the package; new functions carry
  runnable Examples.
- **Known duplication (out of scope)**: `utils/check_archive_structure.py`
  keeps its private `_mtx_header`/`_mtx_entries` — maintenance tooling with
  different validation semantics; a follow-up may point it at
  `iter_edges_from_mtx_dir`.
- **Verification of #138 (done in S5, pre-merge)**: `convert_graph` on the
  `fs` graph (3,609,373 edges, MTX dir → TXT and → `.g`) peaks at **0.06 GiB**
  RSS (vs ~4 GiB through an in-memory MultiDiGraph) in ~3–6 s; edge counts
  match the registry exactly. The reporter's repro
  (`homka122/cfpq-fs-memory-repro`) can be re-run post-merge for the record.
- **RDF multiedge limitation (format-inherent)**: RDF is a set of triples, so
  parallel edges with identical `(u, label, v)` collapse on write — the same
  limitation the legacy form had. Documented in S6; the round-trip tests use
  duplicate-free graphs for the rdf pairs and cover parallel edges for all
  other formats.
