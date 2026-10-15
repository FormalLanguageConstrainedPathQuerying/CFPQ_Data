# Detailed Plan: Task 167 — Single contribution page under the Dataset root

Issue #167. The data-contribution process is documented in four scattered
places: the "Contributing data" section of the Graphs page
(`docs/graphs/index.rst`), a stranded "How to add a new grammar?" section on
the Dataset root (`docs/dataset.rst`), a stale pointer in the developer guide
(`docs/developer.rst`, referencing a README section that does not exist under
that name), and the README. Consolidate it into one page under the Dataset
root, and elevate the "File structure" archive-layout reference (currently on
the Graphs page) to its own dataset-level page.

## Confirmed decisions (user guidance)

- Placement: **flat file + toctree** — new pages are siblings of
  `dataset.rst`, listed in its toctree, so they appear as subpages under
  Dataset in the navigation. No existing public URL changes (no directory
  restructure).
- File structure: **own dataset-level page** — it describes the full archive
  layout and is a neutral format reference used by contributors *and* end
  users (tutorial, issue template); it does not live inside the contribution
  page.
- No-duplication: every fact keeps exactly one home; all other mentions become
  cross-references re-pointed to the new locations.

## Reuse analysis

- No package code changes (docs-only task).
- All new-page content is **moved verbatim** from existing sections — nothing
  is re-described: "Contributing data" (`docs/graphs/index.rst:12-63`),
  "How to add a new grammar?" (`docs/dataset.rst:26-29`), "File structure"
  (`docs/graphs/index.rst:65-152`).
- The issue template (`.github/ISSUE_TEMPLATE/new-data-template.md`) remains
  the single source of truth for required fields; the pages keep pointing at
  it instead of restating its content.
- Page header pattern (`.. only:: html` + `:Release:` / `:Date:`) reused from
  existing pages; label `contributing_data` reused on the new page;
  `graph_file_structure` renamed to `file_structure` (all four `:ref:` uses
  updated in the same commit).

---

### S1: Move "File structure" to its own dataset-level page [done] 202952d

**Code:** none (docs/templates/skills only).

**Tests:** fresh docs build under the no-warnings policy (orphan-document and
duplicate-label checks included).

**Docs:**
- New `docs/file_structure.rst` — title "File structure", label
  `.. _file_structure:` (renamed from `graph_file_structure`), standard page
  header; content moved verbatim from `docs/graphs/index.rst:65-152` (archive
  layout, partial archives, MTX format, "Indexed labels" and "Reversed edges"
  subsections demoted one level).
- `docs/dataset.rst`: add `file_structure` to the toctree (same commit — an
  unwired document is an orphan warning under the no-warnings policy).
- `docs/graphs/index.rst`: remove the "File structure" section.
- Re-point every reference to the old location:
  - `:ref:`graph_file_structure`` → `:ref:`file_structure``:
    `docs/tutorial.rst` (2×), `docs/queries/rpq/index.rst`.
  - Prose "the 'File structure' section of the :ref:`graphs` page" → the new
    page: `docs/flpq.rst` (2×), `docs/queries/rpq/data/reachability.rst`,
    `docs/queries/rpq/data/label_star.rst`,
    `docs/reference/tools/index.rst`.
  - `.github/ISSUE_TEMPLATE/new-data-template.md`: the "Data format" link
    `.../graphs/index.html` → `.../file_structure.html`.
  - `.opencode/skills/add-graph/SKILL.md`: "File structure section of
    `docs/graphs/index.rst`" → `docs/file_structure.rst`.
  - Discovered during implementation (different phrasing, caught by the
    build + grep sweep): `docs/flpq.rst` RSM "Placement" paragraph and the
    `flpq_data/tools/check_archive_structure.py` module docstring — both
    re-pointed to the new page (docstring-only change; the module's 80 tests
    pass).

**Spec:**
- The moved text is verbatim except heading levels; no sentence is rewritten
  or dropped.
- After the commit, no file in the repo references `graph_file_structure` or
  describes the archive layout outside `docs/file_structure.rst`.
- The Graphs page keeps "Format conversion", "Contents", and the category
  tables untouched.

### S2: Create the "Contributing data" page; remove the old sections [ ]

**Code:** none (docs only).

**Tests:** fresh docs build under the no-warnings policy.

**Docs:**
- New `docs/contributing_data.rst` — title "Contributing data", label
  `.. _contributing_data:` (moved from the Graphs page), standard page header.
  Sections, in order:
  - Intro (from `docs/graphs/index.rst:17-23`): all new data enters through
    the single CONTRIBUTE NEW DATA issue; prepare → validate → publish → open
    issue; maintainers upload and merge; no PR needed. Plus one sentence
    pointing to :ref:`file_structure` for the archive layout every
    contribution must follow.
  - "Contribution cases" (from `docs/graphs/index.rst:25-33`).
  - "Validation" (from `docs/graphs/index.rst:35-45`).
  - "Consistency invariants" (from `docs/graphs/index.rst:47-55`).
  - "Not accepted via this flow" (from `docs/graphs/index.rst:57-63`).
  - "Grammars" (from `docs/dataset.rst:26-29`, condensed to avoid repeating
    the intro's issue-creation sentence): grammars arrive with the data they
    apply to (template's "Queries and grammars" section); accepted only if
    instantiated as at least one query with reference results in a
    contributed archive.
- `docs/dataset.rst`: remove the "How to add a new grammar?" section; add
  `contributing_data` to the toctree (before `file_structure`); extend the
  intro by one sentence naming the two new subpages.
- `docs/graphs/index.rst`: remove the "Contributing data" section (the page
  becomes a pure catalog: intro, Format conversion, Contents, tables).

**Spec:**
- The issue-template link appears exactly once on the new page (in the
  intro); the grammar section references the template's section name without
  repeating the full link.
- After the commit, "Contributing data" content exists only in
  `docs/contributing_data.rst`; the label `contributing_data` resolves to the
  new page.

### S3: Re-point external pointers; changelog [ ]

**Code:** none (README/docs/changelog only).

**Tests:** fresh docs build under the no-warnings policy.

**Docs:**
- `README.rst` "How to contribute new data?": "the full contribution guide is
  on the Graphs page" → the Contributing data page
  (`.../FLPQ_Data/contributing_data.html`).
- `docs/developer.rst` "Adding graphs and grammars": replace the stale
  pointer (it references a README section titled "How to add a new graph?"
  that does not exist) with :doc:`/contributing_data`.
- `CHANGELOG.md` Unreleased → Changed: contribution documentation
  consolidated under the Dataset section — new "Contributing data" and
  "File structure" pages; both sections removed from the Graphs page and the
  Dataset root.

**Spec:**
- No file references the old locations of either section (verified by grep
  for "How to add a new graph", "How to add a new grammar", and the two old
  section headings).
- The last subtask's commit carries `Closes #167`.

---

## Execution order

S1 → S2 → S3. One commit per subtask (`docs(167-SN)`); docs-only task — code
gates (tests, lint, format) are skipped per the workflow rules, but each
subtask must leave a green fresh docs build; code review + quality gate
(docs build, CI linkcheck) before merge to `dev`.
