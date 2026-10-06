# Detailed Plan: Task 154 — Publish unique dev versions to TestPyPI from PRs

Issue #154. Every PR targeting `master` builds `flpq-data==6.0.0` and publishes
to TestPyPI with `skip-existing: true`, so only the first push produces an
artifact and later iterations are silently skipped. This task makes each PR
run publish a distinct, automatically derived developmental version.

## Context

- PyPI/TestPyPI **cannot** accept local version identifiers (`6.0.0+<hash>`):
  PEP 440 states the index "MUST NOT allow the use of local version
  identifiers". Hashes are also unorderable. The compliant substitute is a
  developmental release `.devN`.
- The version must change **only on the TestPyPI path**. Committed sources and
  the tag/PyPI release path stay byte-identical.
- `config.DATASET_VERSION = f"{VERSION[0]}.0.0"` is independent of the suffix
  (`6.0.0` either way), so dataset URLs are unaffected.

## Decisions (confirmed with the user)

| # | Decision | Choice |
|---|---|---|
| 1 | Suffix scheme | `github.run_number` (globally unique, monotonic) |
| 2 | Commit traceability | Committed SHA printed to `$GITHUB_STEP_SUMMARY` |
| 3 | Scope | PR path only; tag/PyPI build untouched; committed files untouched |
| 4 | `skip-existing` | Kept as a safety net; stale rationale comment updated |

## Reuse analysis

- `utils/bump_version.py::_set_version` already performs the quoted-version
  transform for both sources — reused (exposed as `set_version_field`).
- `utils/check_version_sync.py` exposes `ROOT`, `config_version()`,
  `pyproject_version()` — reused.
- Test fixture pattern from `tests/utils/test_bump_version.py` (throwaway repo
  under `tmp_path`, monkeypatched `ROOT`) — reused.
- Existing `build` job in `.github/workflows/publish.yml` — extended, no new
  workflow.

### S1: `utils/set_dev_version.py` + tests [ ]

**Code:** New `utils/set_dev_version.py` with `set_dev_version(version)` and
`main(argv)`; `utils/bump_version.py` — rename `_set_version` →
`set_version_field` and export it in `__all__`.
**Tests:** New `tests/utils/test_set_dev_version.py`.
**Docs:** none beyond the numpydoc docstring (behaviour documented in S3).

**Spec:**
- `set_dev_version(version)` validates `^\d+\.\d+\.\d+\.dev\d+$`, refuses when
  `config_version() != pyproject_version()`, then rewrites `flpq_data/config.py`
  (`^VERSION\s*=\s*`) and `pyproject.toml` (`^version\s*=\s*`) via
  `set_version_field`, writing only after both transforms succeed. It never
  touches `CHANGELOG.md`.
- `main` prints the new version and returns 0; returns 1 on `ValueError`.

### S2: Wire the dev version into the publish workflow (PR path only) [ ]

**Code:** `.github/workflows/publish.yml` — add a `Set TestPyPI dev version`
step in the `build` job, guarded by `if: github.event_name == 'pull_request'`,
between "Set up uv" and "Build distributions"; update the top-of-file and
`skip-existing` comments.
**Tests:** none (Actions YAML); `check-yaml` pre-commit hook validates shape.
**Docs:** S3.

**Spec:**
```yaml
      - name: Set TestPyPI dev version
        if: github.event_name == 'pull_request'
        id: dev-version
        run: |
          set -euo pipefail
          base="$(uv version --short)"
          dev="${base}.dev${{ github.run_number }}"
          python utils/set_dev_version.py "$dev"
          {
            echo "### TestPyPI pre-publish"
            echo ""
            echo "- version: \`${dev}\`"
            echo "- commit: \`${{ github.sha }}\`"
          } >> "$GITHUB_STEP_SUMMARY"
```
- The `if` guard is event-based, so tag builds are untouched (no-op).
- `uv version --short` reads the committed `6.0.0` before the rewrite.

### S3: Document the behaviour and record it in the changelog [ ]

**Code:** none.
**Tests:** `pre-commit` only.
**Docs:** `docs/release.rst` ("Package publishing (automated)"),
`CHANGELOG.md` (`[Unreleased]` → `Changed`).

**Spec:**
- Describe the PR-only `.dev<run_number>` rewrite, the PEP 440 limitation on
  local versions, the SHA in the step summary, the `--pre`/exact-pin install
  requirement, and reword the `skip-existing` paragraph (no longer "concurrent
  PRs share a version"). Fix the stale OIDC subject repo name
  (`CFPQ_Data` → `FLPQ_Data`) in the same paragraph.

## Verification

1. Quality gate on the feature branch: coverage test suite, `pre-commit`
   (ruff/format/ty/check-version-sync), docs build.
2. Post-merge acceptance (operational): a PR to `master` publishes
   `<base>.dev<N>`; a second push yields a new version; the run summary shows
   the SHA. The tag path is unchanged.

## Prerequisite outside this task (blocks the first publish)

- The GitHub repository was renamed to
  `FormalLanguageConstrainedPathQuerying/FLPQ_Data`; the TestPyPI pending
  publisher's subject claim must use the new repository name.
- `dev` and `master` have diverged (11 commits on `master` from obsolete
  Dependabot bumps; conflicts in `poetry.lock` and `requirements/*`, deleted
  in `dev`). A `dev → master` PR is currently not mergeable, so no
  `pull_request` workflow runs until they are reconciled. Resolved by merging
  `origin/master` into `dev` and keeping `dev`'s deletions. Tracked separately
  from the code subtasks.
