# Detailed Plan: Task 156 — Rename project CFPQ_Data to FLPQ_Data

Issue #156. The GitHub repository was renamed to
`FormalLanguageConstrainedPathQuerying/FLPQ_Data` and the PyPI distribution is
`flpq-data`; the project scope grew from Context-Free Path Querying (CFPQ) to
Formal Language constrained Path Querying (FLPQ). All remaining `CFPQ_Data`
branding and the "Context-Free Path Querying" description must become
`FLPQ_Data` / "Formal Language constrained Path Querying".

## Context

- The package was already renamed `cfpq_data` → `flpq_data` (task 49, issue
  #135); `pyproject.toml` already declares `name = "flpq-data"` and all site
  URLs in the repo already use `.../FLPQ_Data`. Only the project *branding*
  (name + description) lags behind.
- `flpq-data` is not on PyPI yet; the first publish under the new name is the
  6.0.0 release, so the citation in `docs/about.rst` is updated now.

## Decisions (confirmed with the user)

1. Target name: **FLPQ_Data** (matches the renamed GitHub repo and the
   `flpq-data` PyPI name).
2. **Keep** the S3 bucket name `cfpq-data.storage.yandexcloud.net` — no data
   migration, no URL changes.
3. The `cfpq-data` PyPI deprecation shim is a **separate task**.
4. `CHANGELOG.md`: update **only the header line**; past entries stay as-is.

## Out of scope (verified by full-repo scan)

- Query-class names `cfpq`/`mcfpq`/`rpq`: module tree
  `flpq_data/queries/cfpq/**`, `docs/queries/cfpq/**`,
  `docs/reference/queries/cfpq/**`, `tests/queries/cfpq/**`,
  `registry.json` class values, and all prose using "CFPQ" as the query class.
- S3 bucket URLs: `flpq_data/dataset/data.py`, `reachable_pairs.py`,
  `graphs_list.md`, ~150 `docs/graphs/**` pages, `utils/migration_mapping.json`,
  `docs/release.rst`, `docs/reachable_pairs.rst`, 6 test files.
- History: `tasks/tasks.md`, `tasks/global_plan.md`, past `CHANGELOG.md`
  entries, `utils/optimized_grammars_record.json`, old issue URLs (GitHub
  redirects).
- External names: FastMatrixCFPQ tool, paper titles ("Context-Free Path
  Queries on RDF Graphs", ...), gitignored `temporal_cfpq/` oracle.
- Build artifacts: `docs/_build/`, `.venv/`, `.pytest_cache/`, `coverage.json`.

## Subtasks

### S1: Rename in packaging metadata and top-level files [done] (7248e21)

**Code:** `pyproject.toml` (description, keywords), `README.rst`, `AGENTS.md`,
`LICENSE.txt`, `LICENSE-DATA.txt`, `graphs_list.md`, `CHANGELOG.md` (header
line only).
**Tests:** full test suite (no code changes; guards against any assertion on
the old strings) + pre-commit.
**Docs:** `README.rst` is the sdist readme — updated in place.

**Spec:**
- `pyproject.toml:4`: description → "Python package containing Graphs and
  Grammars for experimental analysis of Formal Language constrained Path
  Querying algorithms".
- `pyproject.toml:12`: keywords — replace `"context-free"` with
  `"formal-language"` (keep `"flpq-data"`).
- `README.rst`: title (line 1) and every `CFPQ_Data` mention (lines 22, 45,
  73, 99) → `FLPQ_Data`; line 24 description → "Formal Language constrained
  Path Querying algorithms".
- `AGENTS.md:3–4`: `CFPQ_Data` → `FLPQ_Data`; "Context-Free Path Querying
  (CFPQ)" → "Formal Language constrained Path Querying (FLPQ)".
- `LICENSE.txt:4`, `LICENSE-DATA.txt:4`: `CFPQ_Data` → `FLPQ_Data`.
- `graphs_list.md:3`: "CFPQ dataset" → "FLPQ dataset".
- `CHANGELOG.md:3`: header line → "All notable changes to FLPQ_Data are
  documented in this file." Nothing else in the changelog changes.

### S2: Rename in docs content [ ]

**Code:** `docs/conf.py` (`project`, linkcheck UA, `htmlhelp_basename`,
`man_pages`).
**Tests:** docs build (Sphinx with no-warnings policy) + full test suite.
**Docs:** `docs/index.rst`, `about.rst`, `install.rst`, `developer.rst`,
`license.rst`, `tutorial.rst`, `getting_started.rst`, `flpq.rst`,
`_templates/layout.html`.

**Spec:**
- `docs/index.rst`: page title → "Data for Formal Language constrained Path
  Querying Evaluation"; lines 6, 10 `CFPQ_Data` → `FLPQ_Data`; line 8
  description reworded as in S1.
- `docs/about.rst`: lines 11, 65 → `FLPQ_Data`; BibTeX title (line 70) →
  `FLPQ\_Data: Graphs and Grammars for Formal Language constrained Path
  Querying`.
- `docs/install.rst:11`, `developer.rst:12,37`, `license.rst:11`,
  `tutorial.rst:13`, `getting_started.rst:12`, `flpq.rst:13`: `CFPQ_Data` →
  `FLPQ_Data`. (`developer.rst:103` quotes the CI step name and is updated in
  S4 together with the workflow it describes.)
- `docs/conf.py`: `project = "FLPQ_Data"` (line 35); linkcheck UA prefix
  `"FLPQ_Data-docs-linkcheck "` (line 99); `htmlhelp_basename = "FLPQ_Data"`
  (line 247); `man_pages` description `"FLPQ_Data Documentation"` (line 253).
- `docs/_templates/layout.html`: schema.org `Dataset.name` → `"FLPQ_Data"`
  (line 9); `description` → "Dataset contains graphs and grammars for Formal
  Language constrained Path-Querying algorithms evaluation." (line 10);
  keywords: `"CONTEXT-FREE"` → `"FORMAL-LANGUAGE"` (line 13).

### S3: Rename the logo file [ ]

**Code:** `git mv docs/_static/img/CFPQDataLogo.svg
docs/_static/img/FLPQDataLogo.svg`; `docs/conf.py:210` `html_logo` path.
**Tests:** docs build (the logo is referenced from `conf.py`).
**Docs:** the SVG itself contains no "CFPQ" text (verified) — content
unchanged, filename only.

**Spec:**
- Rename via `git mv` to preserve history.
- Update `html_logo = "_static/img/FLPQDataLogo.svg"`.

### S4: Rename in CI workflows and GitHub templates [ ]

**Code:** `.github/workflows/tests.yml`, `.github/workflows/coverage.yml`,
`.github/ISSUE_TEMPLATE/graph-add-template.md`,
`grammar-add-template.md`, `bug_report.md`,
`.github/PULL_REQUEST_TEMPLATE/new_graph.md`, `new_grammar.md`.
**Tests:** pre-commit `check-yaml` on the workflow files; full test suite.
**Docs:** none (templates are contribution scaffolding).

**Spec:**
- `tests.yml:31`: step name → "Test FLPQ_Data".
- `coverage.yml:28`: step name → "Test FLPQ_Data with coverage (line and
  branch >= 95%)"; update the matching reference in `docs/developer.rst:103`
  if it quotes the old step name (it does — "Test CFPQ_Data with coverage").
- Templates: every "Current version of CFPQ_Data" field → "Current version of
  FLPQ_Data". The "Which of RPQ, CFPQ, MCFPQ apply" fields are query-class
  names and stay.

### S5: Rename in skill descriptions [ ]

**Code:** `.opencode/skills/add-grammar/SKILL.md`, `add-graph/SKILL.md`,
`build-docs/SKILL.md`, `code-style/SKILL.md`, `release/SKILL.md`,
`run-tests/SKILL.md` (line 3 `description:` of each).
**Tests:** pre-commit; full test suite.
**Docs:** none.

**Spec:**
- In each `description:` line, "CFPQ_Data" → "FLPQ_Data". No other skill
  content changes (module paths like `flpq_data/queries/cfpq` are query-class
  names and stay).
- This is the last subtask: the commit carries `Closes #156` as a standalone
  line.

## Verification

1. Per subtask: pre-commit + full test suite; S2/S3 additionally the docs
   build (`uv run make -C docs html`).
2. Residual scan after S5 (must return only out-of-scope hits):
   `grep -rn "CFPQ_Data" --exclude-dir=.git --exclude-dir=.venv
   --exclude-dir=_build --exclude-dir=.pytest_cache .` → expected: none in
   live files; `cfpq-data.storage` URLs and history files remain by decision.
3. Quality gate on the feature branch (tests + style + type check + docs
   build) must PASS before merge to `dev`.

## Post-merge (outside the repo, reported to the user)

- `git remote set-url origin
  git@github.com:FormalLanguageConstrainedPathQuerying/FLPQ_Data.git`
  (the old URL still works via GitHub redirect).
- Rename the local checkout directory `/home/gsv/Projects/CFPQ_Data` →
  `FLPQ_Data` after the session ends.
