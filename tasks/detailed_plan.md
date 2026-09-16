# Task 34: Add issue references to the v5.0.0 changelog

## Context

The user is preparing the v5.0.0 release and asked to verify whether eight
GitHub issues are resolved and to add references for the resolved ones to the
Changelog. The resolution analysis (2026-09-16, on `dev`) is recorded in
`tasks/global_plan.md` ("Issue resolution status" table). Summary:

- Resolved: #122, #76, #75 (manual-TestPyPI nuance), #74, #26, #16.
- Partial: #2 (Zheng & Rugina C alias data in; Vedurada "Batch Alias Analysis"
  missing) and, consequently, umbrella #28 (7 of 8 sub-items).

User decisions (verbatim, see tasks.md):

- #2: "Reference partial, no close claim".
- #28: "Reference resolved sub-items only".

## Reuse (no duplication)

- The `[Unreleased]` section already describes the 5.0.0 changes; this task
  **amends** those entries with issue references and adds entries for changes
  not yet listed (developer guide, release pipeline, docs prebuild, reference
  values, link fixes). No new changelog sections are invented.
- Keep a Changelog format (Added/Changed/Fixed) as declared in the file header.
- Issue numbers are cited as `(#NNN)` at the end of the entry they describe;
  an entry may carry several references.

## Subtasks

### S1: Record task 34 in the task log and write the plans

**Code:** none (documentation-only task)
**Tests:** skip — no code to test
**Docs:** `tasks/tasks.md` (task 34 + task 35 lines with user guidance),
         `tasks/global_plan.md` (rewritten for tasks 34-35),
         `tasks/detailed_plan.md` (this plan)

**Spec:**
- Append task 34 and task 35 to `tasks/tasks.md` with the user's wording and
  verbatim `[USER GUIDANCE]` annotations.
- Rewrite `tasks/global_plan.md` for tasks 34-35: dependency (34 -> 35),
  verified facts (issue status table, release mechanics, Trusted Publishing
  configured), human gates (manual PR merge; tag on `origin/master` after
  fetch), execution order.
- Write this detailed plan.

### S2: Add issue references to the `[Unreleased]` changelog section

**Code:** none (documentation-only task)
**Tests:** skip — no code to test
**Docs:** `CHANGELOG.md` only

**Spec:**
- Amend the existing "Expanded the graph dataset" entry: cite (#2) on the C
  alias analysis family (noting it comes from "Demand-driven Alias Analysis
  for C"), (#16) on the data provenance family, (#26) on the UniProt biological
  family. No claim that #2 or #28 are closed.
- Add to *Added*:
  - developer guide covering pre-commit, test pipeline, docs build/deploy,
    package deploy, contribution guidelines (#76);
  - release process documentation and the tag-triggered PyPI publish workflow
    (Trusted Publishing) with a manual TestPyPI validation run (#75, #33);
  - docs prebuild for pull requests: no-warnings docs build plus full link
    check on every push and PR (#74);
  - reference reachable-pair counts for graph x grammar pairs exposed via
    `reachable_pairs()` and a downloadable CSV (#32).
- Add to *Changed*: networkx-based labeled graph generators replacing the
  legacy GTgraph ones (#27, #30); node/edge size columns on all per-category
  graph tables (#20).
- Add a *Fixed* section: broken function documentation links on the Graphs
  page; unresolved cross-references now fail the docs build (nitpicky mode,
  no-warnings policy) and the full link check runs in CI and the pre-merge
  quality gate (#122).

### S3: Mark task 34 done in the task log

**Code:** none (documentation-only task)
**Tests:** skip — no code to test
**Docs:** `tasks/tasks.md`

**Spec:**
- Prepend `[done] ` to the task 34 line only; never rewrite the description.

## Post-subtask steps (not subtasks)

- Whole-repo code review per the `code-review` skill (docs-only: focus on
  changelog accuracy against the verified evidence).
- Quality gate per the `quality-gates` skill (docs build + linkcheck; code
  gates skipped for a documentation-only task).
- Merge to `dev` per the `git-workflow` skill (rebase + ff-only), delete the
  feature branch.
