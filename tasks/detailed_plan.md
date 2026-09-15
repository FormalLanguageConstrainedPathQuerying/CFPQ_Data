# Task 33: Developer documentation for issue #76 + README developer section

## Context

Issue #76 ([FEATURE] Developer docs) asks for developer documentation covering
five items: **Pre-commit, Test pipeline, Docs deploy, Package deploy,
Guideline**. The user also asked to verify the README carries the necessary
parts.

Gap analysis on `dev` (before this task):

| Issue item | Where it was documented | Gap |
|---|---|---|
| Pre-commit | `.pre-commit-config.yaml` (hook list), CI `lint.yml`, agent skill `code-style` | No human-facing page; no README mention |
| Test pipeline | CI `tests.yml` (3 OS × py3.11), `coverage.yml` (→ Codecov), agent skill `run-tests` | No human-facing page; no README mention |
| Docs deploy | `deploy_docs.yml` (push to `master` → gh-pages); `docs/README.md` covers the *local* build only | Deployment mechanism undocumented anywhere for humans |
| Package deploy | `publish.yml`, `docs/release.rst` (versioning, Trusted Publishing, TestPyPI, dataset publishing) | Already documented — cross-links only |
| Guideline | Agent skills `git-workflow`, `quality-gates`; `AGENTS.md` (agent-facing) | No human-facing contribution guidelines anywhere |

## User decisions (verbatim)

"Let use docs as the source of truth, skills as thin pointers. Add this to
main pronciples for future skills design and update."

Scope decisions confirmed with the user:

- Contribution guideline lives in the docs page + README only — **no**
  root-level `CONTRIBUTING.md`.
- The stale `docs/install.rst` ("Python 3.7 or later" while
  `pyproject.toml`/`setup.py` require >=3.11) is fixed as part of this task.

## Reuse (no duplication)

- Package deploy: cross-reference existing `docs/release.rst` — do not
  duplicate its content.
- Local docs build: cross-reference existing `docs/README.md` (canonical for
  the local build) — do not duplicate.
- Pre-commit hook list: reference `.pre-commit-config.yaml` as the source of
  truth — do not enumerate hooks in prose.
- pytest configuration: reference `[tool.pytest.ini_options]` in
  `pyproject.toml`.
- CI facts: reference the workflow files under `.github/workflows/` by name;
  the files are the source of truth for exact versions/flags.
- Skills `code-style`, `run-tests`, `build-docs`, `git-workflow`: slim to thin
  pointers to the new page (same pattern as the `release` skill →
  `docs/release.rst`): keep agent-specific operational details (commands,
  pitfalls), drop re-descriptions of the model.
- New material: `docs/developer.rst` (no existing page covers these topics),
  README "For developers" section, `install.rst` fix, `AGENTS.md` principle.

## Division of labor (docs vs skills)

Per the new Main Principle: docs hold the **what/why** (model: what each
pipeline does, what CI enforces, how deployment works, contribution rules);
skills hold the **how** for agents (exact commands, agent/machine-specific
pitfalls, operational procedures) and point at the docs page instead of
re-describing the model.

---

### S1: Record task 33 and write this detailed plan

**Code:** N/A (no code).
**Tests:** N/A (docs-only task; verified by the docs build + linkcheck gate).
**Docs:** `tasks/tasks.md` (append task 33 line, user text verbatim + USER
GUIDANCE), `tasks/detailed_plan.md` (this file).

**Spec:**
- Task line uses the user's description verbatim plus the verbatim USER
  GUIDANCE annotation.
- Branch `feature/33-developer-docs` created from `dev`.

### S2: Create docs/developer.rst covering all five issue items

**Code:** N/A (no code).
**Tests:** N/A (docs-only; the no-warnings docs build + linkcheck are the
verification — every cross-reference and external URL must resolve).
**Docs:** New `docs/developer.rst`; add it to the toctree in
`docs/project.rst` (after `about`) and extend that page's intro line.

**Spec:**
- Page label `.. _developer:`, title "Developer guide", standard
  `.. only:: html` Release/Date block, sections underlined with `-`.
- Sections, in order:
  1. *Development setup* — Python 3.11–3.13 (per `pyproject.toml`
     `>=3.11,<3.14`); Poetry is the canonical environment (what all CI
     workflows use): `poetry install --with dev,test,docs` then
     `pip install .` (`package-mode = false`, so the package itself is
     installed via `setup.py`); note that `requirements/*.txt` are pip-only
     fallbacks.
  2. *Pre-commit* — what it enforces (formatting + hygiene + version sync),
     hook list referenced from `.pre-commit-config.yaml` (not enumerated);
     `pre-commit install` for the git hook; manual full run command; CI
     enforcement via `lint.yml` on every push/PR.
  3. *Test pipeline* — local canonical command
     `poetry run pytest --doctest-modules -vv -s cfpq_data tests`; doctests in
     docstrings are part of the suite (`--doctest-modules`, `testpaths` in
     `pyproject.toml`); `tests/` mirrors `cfpq_data/`; CI: `tests.yml` matrix
     (ubuntu/macos/windows × Python 3.11) on push/PR, `coverage.yml`
     (pytest-cov → Codecov).
  4. *Docs build and deploy* — local build cross-referenced to
     `docs/README.md` (canonical; no-warnings policy `-W --keep-going` in
     `docs/Makefile`; linkcheck command); **new content**: deployment — push
     to `master` triggers `deploy_docs.yml`, which builds the HTML and deploys
     `docs/_build/html` to the `gh-pages` branch (GitHub Pages) via
     `JamesIves/github-pages-deploy-action`; forks are skipped
     (`repository_owner` guard); site URL.
  5. *Package deploy* — one short paragraph cross-referencing
     `:doc:`release`` (versioning, tag-triggered PyPI publish via Trusted
     Publishing, TestPyPI dry run, dataset publishing). No duplication.
  6. *Contribution guidelines* — branching model (`dev` stable development
     branch; `master` protected release branch; releases merge `dev` →
     `master` via PR then push a `vX.Y.Z` tag matching the package version);
     one task per `feature/XXX-short-description` branch, never combine tasks;
     Conventional Commits with exactly one subtask identifier
     (`feat(XXX-SN): ...`), one commit per atomic subtask; pre-merge quality
     gate — all of: full test suite (0 failures, 0 skipped), full pre-commit
     pass, docs build exit 0 under the no-warnings policy, linkcheck with no
     broken/timed-out links; merge strategy rebase + fast-forward (linear
     history, no squash); pointer to the graph/grammar contribution templates
     in `.github/` (reuse, do not duplicate).
- All cross-references must resolve under `nitpicky = True`; all external
  URLs must pass linkcheck.

### S3: Add "For developers" section to README.rst

**Code:** N/A.
**Tests:** N/A (README is RST rendered on GitHub/PyPI; no doctests added —
keep existing examples untouched).
**Docs:** `README.rst` — new "For developers" section between "Examples" and
"How to add a new graph?".

**Spec:**
- Content: dev setup (Poetry, two commands), the three local checks CI
  enforces (tests / pre-commit / docs build) with their one-line commands,
  and a link to the full developer guide page
  (`https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/developer.html`)
  naming what it covers (setup, pre-commit, test pipeline, docs build and
  deployment, package release, contribution guidelines).
- Keep it short — the docs page is the source of truth; the README section
  must not re-describe the model.

### S4: Fix stale install instructions

**Code:** N/A.
**Tests:** N/A (docs-only).
**Docs:** `docs/install.rst`; `docs/README.md` (install line only).

**Spec:**
- `docs/install.rst`: "requires Python 3.7 or later" → Python 3.11–3.13
  (matching `pyproject.toml` `>=3.11,<3.14` and the README); pip commands use
  the PyPI distribution name `cfpq-data` (consistent with the README), while
  prose about the importable module keeps `cfpq_data`.
- `docs/README.md`: the install instruction points at
  `requirements/docs.txt`, which pins sphinx 7.2.6 while the canonical Poetry
  docs group (used by CI and by the no-warnings validation) allows sphinx
  ^9.0.4 — re-point it to the Poetry docs group (`poetry install --with docs`)
  so the canonical instructions match what CI and the quality gate use.

### S5: Slim overlapping skills to thin pointers

**Code:** N/A (skill markdown only).
**Tests:** N/A.
**Docs:** `.opencode/skills/code-style/SKILL.md`,
`.opencode/skills/run-tests/SKILL.md`,
`.opencode/skills/build-docs/SKILL.md`,
`.opencode/skills/git-workflow/SKILL.md`.

**Spec (same pattern as the `release` skill → `docs/release.rst`):**
- Each skill: one pointer line at the top — the model is documented in the
  named section of `docs/developer.rst` (single source of truth, do not
  duplicate) — then keep only agent-specific operational content.
- `code-style`: drop the inline hook-list description (it re-describes the
  config file); keep the commands (`pre-commit run --all-files ...`,
  `pre-commit install`, `black <path>`) and the `requirements/developer.txt`
  note.
- `run-tests`: keep the canonical command, the single-module example, and the
  bare-pytest/networkx pitfall (machine-specific, agent-only); drop the
  re-description of CI coverage in favor of the pointer.
- `build-docs`: keep local build + linkcheck commands and the cached-doctree
  pitfall; add the pointer for the deployment model (new docs section).
- `git-workflow`: keep the operational merge procedure (rebase +
  `--ff-only`), the pre-commit message validation step, and the no-push rule;
  point at the docs Guidelines section for the branching/commit model instead
  of re-stating it.
- Do not touch `quality-gates` (it references the command skills, which stay
  command-bearing) or `release` (already a thin pointer).

### S6: Add the docs-as-source-of-truth principle to AGENTS.md

**Code:** N/A.
**Tests:** N/A.
**Docs:** `AGENTS.md` — Main Principles list.

**Spec:**
- New bullet right after "Documentation is about 'What' and 'Why'. Skills are
  about 'How'.": docs are the source of truth for the project model; skills
  are thin pointers that keep only agent-specific operational details and
  reference the docs page instead of re-describing it.

---

## Post-subtask gate (task level)

Docs-only task: code-specific gates (tests, lint, format) are skipped per the
workflow rules. The quality gate for this task is: docs build exit 0 under
the no-warnings policy (`make clean && make html`) + linkcheck with no broken
or timed-out links. Then whole-repo code review, merge to `dev` (rebase +
fast-forward), mark the task `[done]`.
