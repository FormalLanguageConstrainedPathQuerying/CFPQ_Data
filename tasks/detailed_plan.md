# Task 37: Migrate project to UV manager

## Context

The project is managed with **Poetry** (`pyproject.toml` `[tool.poetry]` +
`poetry.lock`) on top of a **legacy setuptools layer**: `setup.py` reads
`requirements/*.txt` (via `MANIFEST.in`) to declare the PyPI distribution, and
all five CI workflows install dependencies through Poetry. Quality checking is
limited to `black` (formatting) via pre-commit; there is no linter and no type
checker.

The user requires a **full migration to uv** (https://github.com/astral-sh/uv):
no `requirements.txt`, no other legacy stuff, uv-managed quality tools
(linter, type checker), and updated documentation.

## Decision record

Decisions made before implementation (user-confirmed where noted):

1. **Package manager**: uv 0.12.x. `uv.lock` is committed (the project has
   dependency groups, so a lockfile is required for reproducible dev
   environments). `.python-version` = `3.11` (matches the CI matrix and the
   `requires-python` floor) and is committed; the `.gitignore` entry that
   ignored it is removed.
2. **Project metadata**: PEP 621 `[project]` table in `pyproject.toml`;
   build backend **hatchling** (uv's default recommendation). Flat layout, so
   `[tool.hatch.build.targets.wheel] packages = ["cfpq_data"]`. Distribution
   name is `cfpq-data` (PEP 503-normalized; Poetry used `cfpq_data`). License
   uses the PEP 639 SPDX string `"Apache-2.0 AND CC-BY-4.0"` (fall back to
   `{ text = ... }` if hatchling rejects it; in that case keep the
   `License ::` classifier, otherwise drop it per PEP 639). Classifiers are
   carried over from `setup.py`, with the stale `Python :: 3.9` entry replaced
   by 3.11/3.12/3.13.
3. **Dependencies**: runtime deps converted from Poetry constraints to PEP 508
   (`^3.6.1` → `>=3.6.1,<4.0.0`; `pyformlang = "1.0.1"` → `==1.0.1`).
4. **Dev dependencies**: PEP 735 `[dependency-groups]`:
   - `dev`: `ruff`, `ty`, `pyright`, `pre-commit`, `boto3`
   - `test`: `pytest`, `pytest-cov`
   - `docs`: the Sphinx stack (`sphinx`, `pydata-sphinx-theme`, `numpydoc`,
     `nb2plots`, `sphinx-copybutton`, `ipykernel`, `jupyter-client`)
   - Dropped: `codecov` (the pip CLI is unused — CI uploads via
     `codecov/codecov-action`), `black` (replaced by `ruff format`).
   - The old `setup.py` extras (`developer`, `docs`, `tests`) are dropped:
     dev tools as install extras is the legacy anti-pattern; dependency groups
     replace them.
5. **Quality tools** (user guidance, verbatim in `tasks/tasks.md`):
   - **Linter + formatter**: ruff (lint rules `E,F,W,I`; `ruff format`).
     One-time reformat commit.
   - **Type checker**: **ty for the fast local check; CI runs both ty and
     pyright** (user guidance).
   - **pre-commit is kept** as the commit-time runner, using **official hooks**
     (user asked for official uv pre-commit hooks): `astral-sh/uv-pre-commit`
     (`uv-lock`, keeps `uv.lock` in sync), `astral-sh/ruff-pre-commit`
     (`ruff-check --fix`, `ruff-format`; rev pinned to the locked ruff version
     — both must be bumped together), the existing hygiene hooks, and local
     hooks for the version-sync check and `uv run ty check`. Dropped: the
     `black` hook and `requirements-txt-fixer`.
6. **CI**: all workflows use `astral-sh/setup-uv@v10` (with
   `python-version: "3.11"`); deps via `uv sync --frozen --only-group <g>`;
   commands via `uv run ...`; the publish job builds with `uv build`. The lint
   job runs the pre-commit pass plus `uv run ty check` and `uv run pyright`.
   `uv sync` installs the project itself (editable), so the separate
   `pip install .` steps disappear.
7. **Packaging**: `setup.py`, `MANIFEST.in`, `requirements.txt`,
   `requirements/`, `poetry.lock` are deleted. The hatchling sdist includes
   VCS-tracked files; `cfpq_data/data` stays out (gitignored, downloaded at
   runtime). `uv build` builds the wheel from the source tree (not from the
   sdist as `python -m build` did) — the TestPyPI pre-publish still validates
   the build and metadata; `docs/release.rst` is rewritten accordingly.
8. **Version sync**: `cfpq_data/config.py` stays canonical;
   `utils/check_version_sync.py` and `utils/bump_version.py` work unchanged on
   PEP 621 (their `^version = "..."` regex matches `[project] version`).
9. **Broken legacy scripts** (user decision: delete): `utils/fetch_dataset.py`
   (imports removed `AWS_*`/`BUCKET_NAME` from `cfpq_data.config`, writes a
   non-existent `cfpq_data/dataset.py`) and `utils/update_dataset_tables.py`
   (imports non-existent `graph_from_dataset`). Both fail at import time, have
   no tests, and are referenced by no docs/skill/README.
10. **Type-check scope**: `cfpq_data`, `tests`, `utils`. Tests import the
    `utils/` scripts as top-level modules (via `tests/utils/conftest.py`
    sys.path insertion), so both checkers get `extraPaths = ["utils"]`.

## Probe results (measured on the current code, 2026-09-16)

- ruff (`E,F,W,I`): 130 findings — 41 F403 (star imports in `__init__.py`),
  36 I001 (unsorted imports, auto-fixable), 35 E501 (line too long), 10 F401,
  4 E402, 2 E741, 1 F405, 1 E714; 46 auto-fixable. 34 files need reformatting.
- ty 0.0.81: 74 diagnostics — most are import resolution (pytest not in the
  probe env; `utils` modules), ~10 real errors (regex `.group` on
  `Match | None` in `cfpq_data/grammars/converters/cfg.py` ×2 and
  `utils/fetch_dataset.py` ×1 [deleted], missing members in the two deleted
  scripts, 2× `invalid-argument-type` in tests).
- pyright 1.1.414 (basic mode): 41 errors — 15 reportMissingImports (utils
  modules + deleted scripts), 15 reportArgumentType, 7
  reportOptionalMemberAccess, 4 reportAttributeAccessIssue (deleted scripts).
  After S2 deletions + `extraPaths`, ~26 real errors remain.

## Subtasks

### S1: Record task 37 in the task log and write this detailed plan [done — 2516b06]

**Code:** none (documentation-only)
**Tests:** skip — no code to test
**Docs:** `tasks/tasks.md` (task 37 line with verbatim user guidance),
         `tasks/detailed_plan.md` (this file)

**Spec:**
- Task line recorded verbatim; all three user-guidance items appended
  verbatim (official uv pre-commit hooks; ty fast / ty+pyright in CI; delete
  the two broken scripts).

### S2: Core uv migration — PEP 621 pyproject, lockfile, legacy removal [done — 3f69e99]

**Code:** Rewrite `pyproject.toml` (PEP 621 `[project]`,
          `[dependency-groups]`, hatchling `[build-system]` +
          `[tool.hatch.build.targets.wheel] packages = ["cfpq_data"]`, keep
          `[tool.pytest.ini_options]`); add `.python-version` (`3.11`);
          generate `uv.lock`; delete `poetry.lock`, `setup.py`,
          `MANIFEST.in`, `requirements.txt`, `requirements/`,
          `utils/fetch_dataset.py`, `utils/update_dataset_tables.py`;
          remove the `.python-version` line from `.gitignore`; delete stale
          local build artifacts (`build/`, `dist/`, `cfpq_data.egg-info/`).
**Tests:** `uv sync --all-groups` succeeds; `uv run python -c
          "import cfpq_data"` works; the full suite is green under uv
          (`uv run pytest --doctest-modules -vv -s cfpq_data tests`, 0
          failures); `uv run python utils/check_version_sync.py` exits 0;
          `uv build` produces sdist + wheel with correct metadata (name
          `cfpq-data`, version, deps, license, readme) and the sdist contains
          `cfpq_data/`, `README.rst`, `LICENSE.txt`, `LICENSE-DATA.txt` but no
          `cfpq_data/data`.
**Docs:** `CHANGELOG.md` `[Unreleased]`: Changed (uv migration, PEP 621 +
         hatchling, dependency groups) and Removed (legacy packaging files,
         unused `codecov` dev dep, the two broken scripts).

**Spec:**
- Dependency ranges per decision 3; groups per decision 4.
- If hatchling rejects the SPDX license string, use `{ text = ... }` and keep
  the `License ::` classifier (decision 2 fallback).
- Reuse: `utils/check_version_sync.py` / `utils/bump_version.py` unchanged
  (verified compatible with PEP 621).

### S3: Ruff lint + format config and one-time code pass [done — a3def54]

**Code:** Add `[tool.ruff]` (`target-version = "py311"`),
          `[tool.ruff.lint]` (`select = ["E", "F", "W", "I"]`) and
          `[tool.ruff.lint.per-file-ignores]` to `pyproject.toml`; run
          `uv run ruff check --fix .` and `uv run ruff format .`; manually fix
          the remaining findings (E501 line wraps, E741 ambiguous names,
          E714, F405, any F401 that is an intentional re-export).
**Tests:** Full suite green after reformatting (doctests included);
          `uv run ruff check .` and `uv run ruff format --check .` are clean.
**Docs:** `CHANGELOG.md` `[Unreleased]` Added: ruff as the lint/format gate.

**Spec:**
- Per-file ignores (from the probe): `"__init__.py" = ["F403"]` (star imports
  are the package's public-API re-export pattern);
  `"tests/utils/conftest.py" = ["E402"]` (sys.path insertion must precede the
  utils imports). Any other per-file ignore must be justified in the commit
  message.
- F401 findings are reviewed one by one: genuinely unused imports are removed;
  intentional re-exports keep a `# noqa: F401`.
- `ruff format` must not change doctest output (it does not touch docstrings);
  the suite is the guard.

### S4: Type checking — ty + pyright config and error fixes [done — 5878e10]

**Code:** Add `[tool.ty.environment]` (`extra-paths = ["utils"]`) and
          `[tool.pyright]` (`pythonVersion = "3.11"`, `extraPaths = ["utils"]`)
          to `pyproject.toml`; fix every real ty and pyright error in
          `cfpq_data/`, `tests/`, `utils/` (regex `.group` on `Match | None`
          needs a None guard; argument-type mismatches are fixed at the call
          site or by correcting an over-narrow annotation — whichever matches
          the intended behavior).
**Tests:** `uv run ty check` exits 0; `uv run pyright` exits 0; full suite
          green.
**Docs:** `CHANGELOG.md` `[Unreleased]` Added: type checking (ty locally,
         ty + pyright in CI).

**Spec:**
- No `# type: ignore` / `# ty: ignore` suppressions unless a specific false
  positive is documented in the commit message with the checker and rule.
- ty's `python-version` is auto-detected from `requires-python` (3.11); set it
  explicitly only if detection misbehaves.
- pyright runs in its default `basic` mode; do not lower the mode to get
  green — fix or justify.

### S5: Rewrite .pre-commit-config.yaml with official hooks [done — 2f34ee3]

**Code:** New `.pre-commit-config.yaml`:
          - `pre-commit/pre-commit-hooks` v6.0.0: `check-yaml`,
            `end-of-file-fixer`, `trailing-whitespace` (drop
            `requirements-txt-fixer`)
          - `astral-sh/uv-pre-commit` 0.12.15: `uv-lock`
          - `astral-sh/ruff-pre-commit` v0.16.7: `ruff-check`
            (`args: [--fix]`), `ruff-format`
          - local: `check-version-sync` (unchanged entry), `ty-check`
            (`entry: uv run ty check`, `language: system`,
            `pass_filenames: false`, `files: \.py$`)
          Drop the `black` hook.
**Tests:** `uv run pre-commit run --all-files` — every hook passes (including
          `uv-lock`, both ruff hooks, and the local ty hook).
**Docs:** `docs/developer.rst`: replace the "Pre-commit" section with a
         "Quality checks" section covering the official-hook setup (and the
         rule that the `ruff-pre-commit` rev must match the locked ruff
         version), the local commands (`uv run ruff check .`,
         `uv run ruff format .`, `uv run ty check`), and the fact that CI
         additionally runs pyright; update the "Test pipeline" command to
         `uv run pytest ...`; add type checking to the "Quality gate" list in
         "Contribution guidelines".

**Spec:**
- The hook list in `.pre-commit-config.yaml` stays the single source of truth
  (docs describe it, never duplicate it).
- `uv run ty check` as a local hook requires uv on PATH — that is now a
  project prerequisite (documented in "Development setup").

### S6: Migrate all CI workflows to uv [done — 73eb75d]

**Code:** `.github/workflows/{tests,coverage,docs,deploy_docs,lint,publish}.yml`:
          replace `actions/setup-python` + Poetry with
          `astral-sh/setup-uv@v10` (`python-version: "3.11"`),
          `uv sync --frozen --only-group <g>` (test/docs/dev per job), and
          `uv run ...` commands; drop the `pip install .` steps (uv sync
          installs the project editable); publish job builds with `uv build`;
          lint job gains `uv run ty check` and `uv run pyright` steps.
**Tests:** Every workflow file parses as YAML (`python3 -c
          "import yaml,sys; yaml.safe_load(open(sys.argv[1]))"` per file); no
          `poetry`/`setup-python` references remain (grep). Real CI runs on
          the next push (after merge — noted in the commit message).
**Docs:** `docs/release.rst`: rewrite the "Two packaging constraints" block —
         with PEP 621 + hatchling all build inputs are VCS-tracked, and
         `uv build` builds the wheel from the source tree (not from the sdist);
         the TestPyPI pre-publish still validates build + metadata. Update the
         "Builds the sdist and wheel (`python -m build`)" line to `uv build`.

**Spec:**
- Keep the existing triggers, matrices, permissions, and comments that are
  still true; only the tooling steps change.
- `--frozen` makes CI fail if `uv.lock` is out of sync with `pyproject.toml`
  (the `uv-lock` pre-commit hook is the local guard).

### S7: Update remaining docs and verify the docs build

**Code:** none (documentation-only)
**Tests:** skip — no code to test
**Docs:** `docs/README.md` (Poetry → uv commands); `docs/developer.rst`
         "Development setup" section (uv installation, `uv sync --all-groups`,
         group semantics — replacing the Poetry/package-mode/setup.py/
         requirements paragraphs); `README.rst` developer section (Poetry →
         uv); final consistency pass: grep docs + README for
         `poetry|requirements|setup.py|MANIFEST` and fix stragglers.
**Spec:**
- Verification: `uv run make -C docs html` exits 0 under the no-warnings
  policy; `uv run sphinx-build -b linkcheck docs docs/_build/linkcheck`
  reports no broken links.

### S8: Update the agent skills

**Code:** none (documentation-only)
**Tests:** skip — no code to test
**Docs:** `.opencode/skills/run-tests/SKILL.md` (`poetry run` → `uv run`;
         dependency-group note replaces `requirements/tests.txt`; keep the
         bare-pytest pitfall, updated env name);
         `.opencode/skills/code-style/SKILL.md` (pointer to the new "Quality
         checks" section; ruff/ty via `uv run`; hook list stays in
         `.pre-commit-config.yaml`);
         `.opencode/skills/quality-gates/SKILL.md` (add the type-check step —
         ty locally, CI also runs pyright; update the "Pre-commit" section
         reference to "Quality checks");
         `.opencode/skills/release/SKILL.md` (`poetry run pre-commit run
         check-version-sync --all-files` → `uv run pre-commit run
         check-version-sync --all-files`).

**Spec:**
- Skills stay thin pointers to the docs (main principle); no command
  duplication beyond what the skills already carry.
- Verification: grep `.opencode/skills/` for `poetry` → no matches.

## Post-subtask steps

1. Code review of the whole task diff (`code-review` skill), iterate to zero
   findings.
2. Quality gate (`quality-gates` skill): full test suite, full pre-commit
   pass, `uv run ty check`, docs build, link check — all must PASS. (CI
   additionally runs pyright; it is run locally as well since Node 18 is
   available on this machine.)
3. Merge to `dev` (rebase + ff-only), delete the feature branch, mark task 37
   `[done]`.
