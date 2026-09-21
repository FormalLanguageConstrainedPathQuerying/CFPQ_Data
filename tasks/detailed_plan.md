# Detailed Plan: Task 51 — CI as source of truth for commands

Task (user's words, recorded in `tasks/tasks.md`): "First, analyze whether
it is possible to replace some parts of developer docs and skills with refs
to CI workwlow description. I think, CI must be source of thruth for some
commands and knolage."

Scope: analyze which developer-doc/skill content duplicates the CI
workflows, record the decision as a documented rule, apply it — command
blocks become references to the workflow file + step name — and remove the
duplicated knowledge from the CI comments (pointers instead).

Verified facts this plan builds on (checked against the repo, 2026-09-21):
- Six non-trivial commands are restated in docs while CI runs them verbatim:
  - pre-commit full pass — `docs/developer.rst` "Quality checks" and the
    "Run pre-commit" step of `.github/workflows/lint.yml`;
  - canonical test command (pytest + coverage check) — `docs/developer.rst`
    "Test pipeline" and the "Test CFPQ_Data with coverage (line and branch
    >= 95%)" step of `.github/workflows/coverage.yml` (CI adds
    `--cov-report=term-missing`, so local and CI statements already differ);
  - docs build — `docs/README.md` and the "Build" steps of
    `.github/workflows/docs.yml` / `deploy_docs.yml`;
  - link check — `docs/README.md` and the "Check links" step of
    `.github/workflows/docs.yml`.
- Local-only commands (no CI counterpart, stay in docs): `uv sync
  --all-groups`, `uv run pre-commit install`, single-module pytest,
  `uv sync --only-group docs`, individual tool runs (`uv run ruff check .`
  etc.), the single-hook `pre-commit run check-version-sync` in the release
  skill.
- The same 3-line comment explaining `--frozen`/`--all-groups` is
  copy-pasted into five workflows (coverage, deploy_docs, docs, lint,
  tests); `publish.yml` has no sync step. Two more policy comments in
  `docs.yml` (no-warnings, linkcheck exit code) and one in `coverage.yml`
  (per-metric gate rationale) restate policies that `docs/developer.rst`
  already documents.
- The skills (`run-tests`, `code-style`, `build-docs`, `quality-gates`) are
  thin pointers to `docs/developer.rst` sections; none restates a command
  block, but their "exact commands ... the single source of truth" phrasing
  must follow the new model.
- The docs already reference workflow files with `:file:` roles, so
  references are an established pattern.

Decision (recorded in the docs by S2):

1. For every command CI runs verbatim, the CI workflow is the source of
   truth: docs and skills reference the workflow file + step name instead
   of restating the command, so a command changes in exactly one place.
2. Granularity: commands with non-trivial arguments (flags, paths,
   multi-part pipelines) become references; bare tool invocations (`uv run
   ty check`, `uv run pyright`) stay inline where they name the gate step,
   because they carry no drift risk.
3. What stays in docs: local-only commands and the policies behind the
   checks (no-warnings build, 95/95 coverage gate, doctests as tests,
   lockfile pinning).
4. CI comments that restate documented policy become one-line pointers to
   the docs section; workflow-specific operational notes stay.

### S1: Record the task and write this plan

**Code:** none.
**Tests:** n/a.
**Docs:** `tasks/tasks.md` (task 51 recorded — already in the working tree),
`tasks/global_plan.md` (tasks 51–53 + dependencies — already in the working
tree), `tasks/detailed_plan.md` (this plan).

**Spec:**
- Commit the already-recorded task-log and global-plan changes together with
  this plan; no new task text is added.

### S2: Record the decision in developer.rst

**Code:** none.
**Tests:** docs build (`make -C docs html` under the no-warnings policy)
must exit 0.
**Docs:** `docs/developer.rst` — a new "CI as source of truth" section right
after the intro stating the rule of decision 1–3 (workflow file + step name
is the reference form; local-only commands and policies stay in docs); the
"Development setup" bullets absorb the `--frozen`/`--all-groups` rationale
currently carried by the CI comments (lockfile pinning, every dependency
group installed so checks that import from any group resolve).

**Spec:**
- The rule is stated exactly once (this section); later sections apply it
  without re-stating it.
- The Development setup text must carry the full rationale so S5's pointer
  comments do not dangle: `--frozen` fails on a lockfile out of sync with
  `pyproject.toml`; `--all-groups` installs every dependency group because
  checks import from any of them (ty/pyright type-check `tests/`,
  `docs/conf.py` and `utils/`, which import pytest, sphinx and boto3).

### S3: Turn the doc command blocks into references

**Code:** none.
**Tests:** docs build must exit 0 (no-warnings policy).
**Docs:** `docs/developer.rst` — "Quality checks": the full-pass command
block becomes a reference to the "Run pre-commit" step of
`.github/workflows/lint.yml`; "Test pipeline": the canonical command block
becomes a reference to the "Test CFPQ_Data with coverage (line and branch
>= 95%)" step of `.github/workflows/coverage.yml"; "Docs build and deploy":
the build and link-check commands are referenced from the "Build" and
"Check links" steps of `.github/workflows/docs.yml`, and the pointer to
`docs/README.md` is adjusted (it keeps only the local-only setup command).
`docs/README.md` — the build and link-check command blocks become
references to the same `docs.yml` steps; the `uv sync --only-group docs`
block and all policy prose stay.

**Spec:**
- Local-only command blocks survive untouched: single-module pytest,
  individual tool runs, `uv run pre-commit install`, `uv sync --all-groups`,
  `uv sync --only-group docs`.
- The coverage-policy prose (95/95, why the checker script exists) stays in
  "Test pipeline"; only the command block is replaced.
- No command with non-trivial arguments is restated anywhere in `docs/`
  after this subtask (grep-verified).

### S4: Update the skill pointers to the new model

**Code:** none.
**Tests:** n/a (skill documentation); docs build still exits 0.
**Docs:** `.opencode/skills/quality-gates/SKILL.md` — the "single source of
truth for the commands" sentence becomes the new model (CI workflows are
the source of truth for the commands they run; `docs/developer.rst` holds
policies and local-only commands and points at the workflow steps).
`.opencode/skills/run-tests/SKILL.md`, `code-style/SKILL.md`,
`build-docs/SKILL.md` — description and intro phrasing "the exact commands
are documented in ... the single source of truth" becomes "the exact
commands live in the CI workflow steps referenced by ...".

**Spec:**
- Skills stay thin pointers: they gain no command blocks.
- The bare `uv run ty check` mentions in `quality-gates` stay inline
  (decision 2).

### S5: Slim the duplicated CI comments to pointers

**Code:** `.github/workflows/coverage.yml`, `deploy_docs.yml`, `docs.yml`,
`lint.yml`, `tests.yml` — the copy-pasted 3-line dependency comment becomes
a one-line pointer at "Development setup" in `docs/developer.rst`;
`docs.yml` — the no-warnings and linkcheck comments become pointers at
"Docs build and deploy"; `coverage.yml` — the per-metric gate rationale
becomes a pointer at "Test pipeline", keeping the workflow-specific
`term-missing` note.
**Tests:** pre-commit passes (check-yaml validates every touched workflow).
**Docs:** n/a — the knowledge already lives in `docs/developer.rst` since
S2/S3.

**Spec:**
- No policy rationale is restated in a workflow comment after this subtask;
  each slimmed comment names the docs section it points at.
- Workflow-specific operational notes (the `term-missing` log note, the
  lint.yml type-check explanation, publish.yml comments) are untouched.
