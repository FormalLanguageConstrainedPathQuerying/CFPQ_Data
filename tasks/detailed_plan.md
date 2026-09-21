# Detailed Plan: Task 45 — Strong code coverage gate + tooling cleanup

Task (user's words, recorded in `tasks/tasks.md`): "set strong code coverage
checking both in CI and locally. Set both instructionand branch coverage up
to 95%. Moreover, gh is installed. remove workarounds from documentation and
instructions. Extend tooling skill: no workaround for regular tasks. If there
is a tool for regular task it must be installed and configured appropriately."

Scope (per `tasks/global_plan.md`): enforce line and branch coverage >= 95%
both in CI (`coverage.yml`) and locally (canonical test command); remove the
curl/GitHub-API workaround from the release skill now that the `gh` CLI is
installed; extend the project tooling guidance with a no-workaround rule.

Verified facts this plan builds on (checked against the repo, 2026-09-21):
- Current coverage: line 1062/1066 = 99.6%, branch 264/274 = 96.3% — both
  already >= 95, so the gate passes from day one; the task is enforcement,
  not writing tests.
- `pytest-cov --cov-fail-under` and `coverage.py fail_under` check only the
  combined TOTAL (statements + branches together) — they cannot enforce each
  metric separately (line 94% + branch 100% could pass a combined 95). No
  existing tool enforces per-metric thresholds locally, so a small `utils/`
  script is the tool (pattern of `utils/archive_sizes.py`).
- `coverage.json` "totals" carries `covered_lines`/`num_statements` always
  and `covered_branches`/`num_branches` only when branch coverage is on.
- `.github/workflows/coverage.yml` runs `uv run pytest --cov=cfpq_data` and
  uploads to Codecov; no branch coverage, no threshold. `tests.yml` (the
  cross-OS suite) runs bare `uv run pytest` and stays that way.
- No `[tool.coverage]` configuration exists in `pyproject.toml`.
- The only gh workaround is `.opencode/skills/release/SKILL.md` "Recovery"
  (GH_TOKEN extraction + curl to api.github.com for release creation and
  asset upload). `gh` 2.45.0 is installed and authenticated on this machine
  (verified 2026-09-21). No other curl/api.github workarounds exist in
  `docs/` or `.opencode/` (grep-verified).
- The tooling guidance lives in the "Tools, not instructions" bullet of the
  Main Principles in `AGENTS.md`.
- The canonical local test command is documented in the "Test pipeline"
  section of `docs/developer.rst`; the `quality-gates` skill defines gate
  semantics and points at `docs/developer.rst` for commands.

Design decisions:

1. `[tool.coverage.run] branch = true` in `pyproject.toml` — every `--cov`
   run includes branches; no caller needs to remember `--cov-branch`.
2. `utils/check_coverage.py` reads `coverage.json`, computes line % and
   branch % separately from "totals", prints both, and exits non-zero if
   either is below the threshold (default 95.0, overridable with
   `--threshold`). Missing branch data is an explicit error (the report must
   be generated with branch coverage); zero branches counts as 100%.
3. Canonical local command:
   `uv run pytest --cov=cfpq_data --cov-report=json && uv run python
   utils/check_coverage.py` — documented in the "Test pipeline" section; the
   quality gate treats a threshold failure as a gate failure.
4. CI: `coverage.yml` runs the same two steps (plus `term-missing` for the
   log); the Codecov upload is unchanged.
5. The release skill's Recovery is rewritten with the `gh` CLI (`gh release
   create` / `gh release upload`); the GH_TOKEN extraction and curl payload
   machinery are removed; the awk changelog extraction stays (it builds the
   notes file that `gh release create --notes-file` also needs).
6. The "Tools, not instructions" bullet in `AGENTS.md` is extended with the
   user's verbatim no-workaround rule.

### S1: Coverage config, check script, and the local gate

**Code:** `pyproject.toml` — `[tool.coverage.run] branch = true`. New
`utils/check_coverage.py`: argparse (`--threshold` default 95.0, positional
report path default `coverage.json`), reads "totals", prints line % and
branch %, exits 1 if either is below the threshold with a message naming the
metric; explicit error when branch data is missing from the report.
**Tests:** new `tests/utils/test_check_coverage.py` with synthetic
`coverage.json` fixtures in `tmp_path`: both metrics pass (exit 0), line
below threshold (exit 1, message names line), branch below (exit 1, names
branch), `--threshold` override, missing branch fields (clear error), zero
branches (treated as 100).
**Docs:** `docs/developer.rst` "Test pipeline" — the canonical command gains
the coverage step and the 95/95 policy is stated; `quality-gates` skill —
the test-suite step notes that a coverage threshold failure fails the gate.

**Spec:**
- The script uses only the standard library (json, argparse, pathlib, sys)
  so it runs in any environment where the report exists.
- Percentages are computed from the raw counts (covered/total), not from the
  rounded `percent_covered` fields.
- The canonical command is one line: pytest (which writes `coverage.json`)
  and then the check; a failing suite short-circuits before the check runs.

### S2: Enforce the gate in CI

**Code:** `.github/workflows/coverage.yml` — the test step becomes
`uv run pytest --cov=cfpq_data --cov-report=term-missing --cov-report=json &&
uv run python utils/check_coverage.py`, with a comment explaining that both
metrics are enforced separately (the combined `--cov-fail-under` cannot).
**Tests:** pre-commit's check-yaml hook passes; the CI job itself is the
verification.
**Docs:** `docs/developer.rst` "Test pipeline" CI bullet — `coverage.yml`
enforces the 95/95 gate and uploads to Codecov.

**Spec:**
- `tests.yml` (the cross-OS suite) keeps running bare `uv run pytest` —
  coverage stays in the dedicated job, as today.
- The Codecov upload step is unchanged (it reads the `.coverage` data that
  pytest-cov always writes).

### S3: Remove the gh workaround from the release skill

**Code:** none.
**Tests:** n/a (skill documentation); `gh --version` and `gh auth status`
verified on this machine during planning.
**Docs:** `.opencode/skills/release/SKILL.md` — the "Recovery" section is
rewritten around the `gh` CLI: create the release with
`gh release create vX.Y.Z --notes-file release_notes.md`, upload the dist
artifacts with `gh release upload vX.Y.Z <whl> <tar.gz>`; the GH_TOKEN
extraction, the python3 JSON payload, and the curl commands (including the
per-release `upload_url` note) are removed; the awk changelog extraction and
the PyPI-delete constraint stay.

**Spec:**
- No curl/api.github.com invocation remains anywhere in `.opencode/` or
  `docs/` (grep-verified after the change).
- The skill stays a thin pointer: procedure only, no duplication of
  `docs/release.rst`.

### S4: The no-workaround tooling rule in AGENTS.md

**Code:** none.
**Tests:** n/a.
**Docs:** `AGENTS.md` Main Principles — the "Tools, not instructions" bullet
is extended with the user's verbatim rule: "No workaround for regular tasks.
If there is a tool for regular task it must be installed and configured
appropriately."

**Spec:**
- The rule is recorded verbatim (user guidance), appended to the existing
  bullet so the tooling policy stays in one place.
