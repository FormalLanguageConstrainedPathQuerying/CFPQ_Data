# Detailed Plan: Task 41 — Move canonical grammar descriptions from graph pages to category pages

## Task

Analyze structure of the site. Looks like better place for canonical grammars
description is category page, not graph. Because grammar canonical for category.

**[USER GUIDANCE]**: "On issue and request teplamtes. If graph for existing
category, then ok. But we can have at least two more options. Graph for new
category. Then grammars should be provided. New grammar for existing category."
/ "Nothing (Recommended)" (graph pages keep no grammar section or pointer) /
"Leave as-is (Recommended)" (docs/old_graphs legacy pages untouched) /
"All 4 grammars (Recommended)" (rdf category page lists the union incl.
broaderTransitive) / "Yes, add it (Recommended)" (Category row in both graph
templates)

## Analysis (verified against the tree, 2026-09-18)

Site layout: `docs/dataset.rst` toctree → `graphs/index` → 8 category pages
(`docs/graphs/<category>.rst`) → 113 graph pages (`docs/graphs/data/*.rst`).
Separately, `docs/grammars/` holds 4 parameterized *template* pages
(nested_parentheses, dyck, c_alias, java_points_to) — different purpose, kept.

7 distinct canonical grammar texts are each repeated on every graph page of
its category:

| Category | Pages | Current duplication |
|---|---|---|
| c_alias_analysis | 20 | identical inline section (incl. `change_edges` note, 2 variants) |
| rdf | 20 | inline; 19 identical + geospecies has a 4th grammar (broaderTransitive) |
| biological_uniprot | 10 | identical inline section |
| java_points_to | 21 | inconsistent: 14 pages inline + 7 via `.. include::` |
| field_sensitive_alias | 10 | `.. include:: grammar_cpu17_field_sensitive_alias.inc` |
| context_sensitive_data_flow | 10 | `.. include:: grammar_cpu17_context_sensitive_data_flow.inc` |
| data_provenance | 18 | `.. include:: grammar_data_provenance.inc` |
| name_resolution | 4 | `.. include:: grammar_name_resolution.inc` |

5 `.inc` files live in `docs/graphs/data/`. No tooling (utils/, tests/,
cfpq_data/) references them. Docs build is nitpicky with a no-warnings policy,
so it catches dangling refs.

## Decisions

- Grammar text moves **verbatim** to the category page, appended after the
  per-category graph table (the table already has one column per grammar
  language — the description belongs with it).
- Section heading normalized to `Canonical grammars` on all 8 category pages
  (sources use "Canonical grammars" / "Canonical Grammar" / "Grammar").
- Graph pages: section removed entirely, nothing left in its place (user
  decision). The category page is the parent in the toctree/nav.
- `docs/old_graphs/` (54 legacy pages, orphan page, no category structure):
  untouched (user decision).
- rdf category page: union of all 4 grammars (3 shared + broaderTransitive),
  keeping the `----` separators (user decision).
- Cross-reference lines to `docs/grammars/` template pages
  (`:ref:`java_points-to``, `:ref:`c_alias``, `:ref:`nested_parentheses``)
  are kept — they tie the concrete canonical grammar to its parameterized
  template.
- Docs-only task: no `.py` changes; code gates (tests/lint/format) skipped,
  docs build gate applies.

## Subtasks

### S1: Record task 41 in the task log and write the detailed plan

**Code:** n/a. Modify `tasks/tasks.md`, `tasks/detailed_plan.md`.
**Tests:** n/a.
**Docs:** n/a (task tracking files).

**Spec:**
- Append Task 41 to `tasks/tasks.md` with the user's description verbatim and
  the `[USER GUIDANCE]` annotations.
- Write this detailed plan.

### S2: Add "Canonical grammars" section to the 5 .inc-based category pages

**Code:** n/a (docs-only). Modify `docs/graphs/java_points_to.rst`,
`docs/graphs/field_sensitive_alias.rst`,
`docs/graphs/context_sensitive_data_flow.rst`,
`docs/graphs/data_provenance.rst`, `docs/graphs/name_resolution.rst`.
**Tests:** n/a — verified by the docs build (S6).
**Docs:** the 5 category pages gain a `Canonical grammars` section after the
graph table, content moved verbatim from `grammar_java_points_to.inc`,
`grammar_cpu17_field_sensitive_alias.inc`,
`grammar_cpu17_context_sensitive_data_flow.inc`,
`grammar_data_provenance.inc`, `grammar_name_resolution.inc` respectively;
headings normalized to `Canonical grammars`; template-page cross-references
kept.

**Spec:**
- Append the section at the end of each page (after the list-table), one
  blank line between the table and the section header.
- Do NOT delete the `.inc` files or touch graph pages yet (S4) — the build
  must stay green at every commit, and includes resolve until removed.

### S3: Add "Canonical grammars" section to c_alias_analysis, biological_uniprot, rdf

**Code:** n/a (docs-only). Modify `docs/graphs/c_alias_analysis.rst`,
`docs/graphs/biological_uniprot.rst`, `docs/graphs/rdf.rst`.
**Tests:** n/a — verified by the docs build (S6).
**Docs:** the 3 category pages gain a `Canonical grammars` section after the
graph table.

**Spec:**
- c_alias_analysis: verbatim from the inline section shared by its 20 graph
  pages (the `.. note::` about `change_edges`, both grammar variants with the
  `----` separator, Pyformlang blocks, `:ref:`c_alias`` cross-reference).
- biological_uniprot: verbatim from the inline section shared by its 10
  unigraph pages ("The grammar file is attached to the archive." + math).
- rdf: union — the 3 grammars shared by 19 pages (combined subClassOf+type,
  subClassOf-only, type-only) plus the broaderTransitive grammar from
  geospecies.rst, in that order, keeping the `----` separators and the
  `:ref:`nested_parentheses`` cross-reference.

### S4: Remove grammar sections from all 113 graph pages; delete the .inc files

**Code:** n/a (docs-only). Modify all 113 `docs/graphs/data/*.rst` pages;
delete `docs/graphs/data/grammar_java_points_to.inc`,
`grammar_cpu17_field_sensitive_alias.inc`,
`grammar_cpu17_context_sensitive_data_flow.inc`,
`grammar_data_provenance.inc`, `grammar_name_resolution.inc`.
**Tests:** n/a — verified by the docs build (S6).
**Docs:** graph pages lose their trailing grammar section; no replacement
text (user decision).

**Spec:**
- 64 pages carry the section inline (header at line start: `Canonical
  grammars` or `Grammar`, section runs to EOF): delete from the header line
  to EOF, leaving the file ending with the Edges Statistics table and a
  single trailing newline.
- 49 pages end with a blank line + `.. include:: grammar_*.inc`: delete both
  lines.
- Verify afterwards: no `include::` left in `docs/graphs/`, no page starts a
  section with `^Canonical|^Grammar`, and the 5 `.inc` files are gone.
- `docs/old_graphs/` untouched.

### S5: Update contribution templates, add-graph skill, graphs index note

**Code:** n/a (docs-only). Modify
`.github/PULL_REQUEST_TEMPLATE/new_graph.md`,
`.github/ISSUE_TEMPLATE/graph-add-template.md`,
`.opencode/skills/add-graph/SKILL.md`, `docs/graphs/index.rst`.
**Tests:** n/a.
**Docs:** templates + skill + index note per spec.

**Spec:**
- Both templates: add a `Category` row to the Info table — value is the
  existing category name, or `new: <proposed name>`.
- Both templates: replace the "Canonical grammars" section with the three-case
  structure: (1) graph for an existing category — name the grammar(s) from
  the category's "Canonical grammars" section that apply; they become the
  table column(s) filled in for the new row; no new grammar text. (2) New
  grammar for an existing category — provide LaTeX + Pyformlang below; it is
  added to the category page and a new column to its table. (3) Graph for a
  new category — provide the canonical grammar(s) below; a new category page
  is created with them. The LaTeX/Pyformlang placeholders apply to cases 2–3
  only.
- add-graph skill Documentation step: per-graph pages no longer carry a
  grammar section; describe the three cases (row under an existing column /
  add grammar + column to the category page / new category page with grammar,
  table, and `docs/graphs/index.rst` registration).
- `docs/graphs/index.rst` "Contents" section: one sentence stating that
  canonical grammars are documented on the category pages.

### S6: Docs build verification

**Code:** n/a.
**Tests:** full Sphinx build per the build-docs skill; zero warnings
(no-warnings policy); no new "not included in any toctree" warnings; spot-check
rendered HTML of the 8 category pages (section present, math rendered) and a
few graph pages (section gone).
**Docs:** n/a.

**Spec:**
- Build must exit clean under the project's no-warnings configuration.
- Grep the build log for `grammar_*.inc` (no unresolved includes) and for
  dangling refs.
