# Detailed Plan: Task 164 — External data contribution flow (issue-first)

Issue #164. Redesign the external contribution path so new data enters via a
single issue carrying one or more validated archives (one graph each), with
mandatory motivation and explicit consistency invariants; delete the
standalone grammar path; document the full case matrix; add the
maintainer-side pipeline tooling.

## Confirmed decisions (user guidance, verbatim on the issue)

- One issue may contain **multiple archives** (a set of graphs/queries for a
  category); each archive still unpacks to a single directory named after it
  (one graph per archive — the fixed structure is unchanged).
- **Delete both** specialized PR templates; replace with one generic PR
  template for code contributions.
- **Decline for now**: updates to an existing graph; new representation of an
  existing query. Both are documented as not accepted via this flow.
- **Add the utility** deriving `reachable_pairs.csv` rows from an archive.
- Explicit invariants: every new graph ships at least one query; every query
  ships reference results (`results.mtx`); no item without description and
  motivation. A grammar is a representation of a query — a grammar definition
  is accepted only if the same grammar is instantiated as a query directory
  with `results.mtx` in a contributed archive.

## Contribution cases (the matrix)

| # | Case | Archive(s) | What's new |
|---|------|-----------|-----------|
| 1 | New graph(s), existing category, existing canonical grammar(s) | full | graphs + query instances |
| 2 | New graph(s), existing category, **new grammar** | full | + grammar: new column in the category table, possibly a generator module |
| 3 | New graph(s), **new category**, canonical grammar(s) | full | + category page |
| 4 | **Existing graph(s)**, new queries — any class; sub-case 4b: queries using a **new grammar** | partial | query dirs; + grammar definition if 4b |

Not accepted via this flow: a grammar/query provided outside an archive (no
reference results); updates to an existing graph; a new representation of an
existing query; more than one graph inside a single archive.

---

### S1: Unified "CONTRIBUTE NEW DATA" issue template [done] 4d1c42c

**Code:** Restructure `.github/ISSUE_TEMPLATE/graph-add-template.md` into
`.github/ISSUE_TEMPLATE/new-data-template.md` (rename + rewrite); delete
`.github/ISSUE_TEMPLATE/grammar-add-template.md`. Reuse the existing
template's field definitions and wording where they survive (Info table,
description-document pointer, statistics conventions, data-format bullets) —
restructure, do not reinvent.

**Tests:** none (no `.py` files changed).

**Docs:** the template is the source of truth for the required fields; no
other doc changes in this subtask.

**Spec:**
- Frontmatter: `name: CONTRIBUTE NEW DATA`, `about: Suggest new data
  (graphs, queries, grammars) to this project`, `title: "[NEW DATA] <brief
  description>"`, `labels: new data`, `assignees: rustam-azimov, vadyushkins`.
- **Contribution type** — one of the four cases above; an issue may combine
  several archives of the same case.
- **Info table** — Version (current FLPQ_Data version); Category (existing
  name or `new: <proposed>`; N/A for case 4).
- **Archives** — one entry per archive (a set is allowed): Name, Kind
  (full/partial), Target graph (partial only), Drive link to `<name>.tar.gz`,
  SHA256 of the archive. State that each archive unpacks to a single
  directory named after it (one graph per archive).
- **Validation (mandatory, per archive)** — the exact command
  (`python utils/check_archive_structure.py <name>.tar.gz` or with
  `--partial`) plus the pasted output and the FLPQ_Data version used. Include
  the no-clone recipe: `pip install flpq-data`, download the single script
  from GitHub raw, run it (all imports resolve from the installed package).
- **Motivation (mandatory)** — free text answering why this graph set /
  grammar / category is useful to other users; must cover every new item.
- **Reference results (explicit requirement)** — every query directory must
  contain `results.mtx`; queries without reference results are not accepted;
  every new graph must ship at least one query; every new grammar must be
  instantiated as at least one such query in a contributed archive.
- Keep: the data-format bullets (full vs partial layout), the
  description-document pointer (the archive README answers the 8 mandatory
  questions — not duplicated here), per-graph statistics subsections (new
  graphs only: Graph Statistics + Edges Statistics tables with the existing
  conventions), and the Queries section reorganized around the case matrix:
  which canonical grammar(s) apply (case 1); grammar definition in LaTeX +
  file format plus why no existing canonical grammar covers it (cases 2, 3,
  4b); category name + description (case 3).
- **Not accepted via this flow** — explicit list: a grammar/query provided
  outside an archive (no reference results); updates to an existing graph; a
  new representation of an existing query; more than one graph inside a
  single archive.

### S2: PR template cleanup

**Code:** Delete `.github/PULL_REQUEST_TEMPLATE/new_graph.md` and
`.github/PULL_REQUEST_TEMPLATE/new_grammar.md`; add a generic
`.github/PULL_REQUEST_TEMPLATE/pull_request.md`.

**Tests:** none (no `.py` files changed).

**Docs:** none.

**Spec:** The generic template is short: a description of the change, the
linked issue (`Closes #<N>`), and a checklist (quality gate passes; docs
updated per the documentation skill; no secrets). Data contributions do not
use PRs — they use the CONTRIBUTE NEW DATA issue (pointer line in the
template).

### S3: External contribution guide in the docs

**Code:** Rewrite the "How to add a new graph?" section of
`docs/graphs/index.rst` (currently *"Just create a PR"*) into a
"Contributing data" section.

**Tests:** Sphinx build via the quality gate; `utils/check_math_snippets.py`
if any math is added (none planned).

**Docs:** this section becomes the single source of truth for the flow and
the case analysis; field-level details stay in the template (cross-reference,
do not duplicate).

**Spec:**
- Flow overview: build archive(s) → validate each locally → publish to Drive
  → one issue with all archives (link + SHA256 + validation output +
  motivation) → maintainers handle upload/merge/registry/docs.
- The no-clone validation recipe (`pip install flpq-data` + raw script URL).
- The four-case table with what each requires (mirror the matrix above;
  field details point at the template).
- Explicit consistency invariants: no graph without at least one query, no
  query without reference results, no item without description and
  motivation.
- Declined cases with reasons (standalone grammar/query without reference
  results; graph updates; new representation of an existing query; multiple
  graphs per archive).
- Note that a set of graphs for a category goes into one issue as multiple
  archives.

### S4: `utils/add_reachable_pairs.py` — derive CSV rows from an archive

**Code:** New file `utils/add_reachable_pairs.py`. Reuse from
`check_archive_structure.py`: `unpack_single_dir`, `_mtx_header`,
`validate_archive` (and the `QUERY_CLASSES` mapping). No new parsing logic.

**Tests:** New `tests/utils/test_add_reachable_pairs.py`. Reuse the tree
builders from `tests/utils/test_check_archive_structure.py` (`_valid_tree`,
`_partial_tree`, `_tarball`) by importing them from that module (same
directory; pytest prepends it to `sys.path`).

**Docs:** numpydoc docstring with doctest examples on the public function; a
short section in `docs/utils.rst` following the existing per-tool pattern
(`.. _add_reachable_pairs:` anchor, usage line, behavior summary) — the
docstring stays the source of truth for details.

**Spec:**
- CLI: `python utils/add_reachable_pairs.py ARCHIVE.tar.gz --graph NAME
  --category CAT [--partial] [--dry-run]`.
- Validate the archive first (full or partial mode per `--partial`); refuse
  to proceed on any structure problem.
- For each `queries/<class>/<query>/` directory emit one row:
  `(graph, <query>.<ext>, category, class, nnz)` where `<ext>` is the first
  present of `cnf > re > mcfg > rsm` (must be an actual file in the query
  directory; all current rows are `.cnf`) and `nnz` is the declared entry
  count from the `results.mtx` header.
- Write to `flpq_data/dataset/reachable_pairs.csv` preserving the existing
  alphabetical order by graph name (insert, don't resort); refuse a duplicate
  `(graph, query_class, stem)` row; `--dry-run` prints the rows and writes
  nothing.
- Exit non-zero on any problem (invalid archive, duplicate row, missing
  representation file), printing each problem.

### S5: Maintainer acceptance pipeline in the skills

**Code:** Extend `.opencode/skills/add-graph/SKILL.md` with an "Accepting an
external contribution" section; update `.opencode/skills/add-grammar/SKILL.md`
(source-of-truth pointers + the grammar-arrives-with-data rule).

**Tests:** none (markdown only).

**Docs:** skills stay thin pointers to tools/docs — no duplication of tool
docstrings or template fields.

**Spec:**
- `add-graph`: per archive of the issue — download from the Drive link →
  verify SHA256 against the issue → re-run `check_archive_structure.py`
  (full/`--partial`) → name uniqueness vs `registry.json` /
  `reachable_pairs.csv` → add CSV rows via `utils/add_reachable_pairs.py` →
  upload (full) or `merge_archive.py` (partial; re-validates and checks the
  CSV rows). Once per issue — `generate_registry.py` → the existing docs
  wiring steps (per-graph pages, category table(s), canonical grammars, new
  category page) → `reachable_pairs_tables.py --update` +
  `archive_sizes.py --update`.
- `add-grammar`: grammars arrive only together with a data contribution
  (cases 2/3/4b of the CONTRIBUTE NEW DATA issue); pointer to the template;
  the generator-module conventions stay as-is.

### S6: Changelog

**Code:** none. **Tests:** none.

**Docs:** Unreleased entry in `CHANGELOG.md`: issue-first contribution flow
with multi-archive issues, unified CONTRIBUTE NEW DATA template, removed
specialized templates, new `utils/add_reachable_pairs.py`.

---

## Execution order

S1 → S2 → S3 → S4 → S5 → S6. One commit per subtask
(`feat(164-SN)` / `docs(164-SN)`), code review + quality gate before merge to
`dev`; the last subtask's commit carries `Closes #164`.
