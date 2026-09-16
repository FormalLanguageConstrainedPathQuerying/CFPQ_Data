# Task 35: Cut the v5.0.0 release

## Context

Task 34 finalized the `[Unreleased]` changelog section with issue references.
This task cuts the release. The procedure is codified in the `release` skill
and `docs/release.rst` (single source of truth — not re-described here); this
plan records only what is specific to this run.

## Verified facts (2026-09-16, on `dev`)

- Version is already `5.0.0` in `cfpq_data/config.py` and `pyproject.toml`;
  `utils/bump_version.py 5.0.0` only promotes the changelog section.
- The dataset is already served from `5.0.0/graph/` — no re-upload needed.
- Trusted Publishing for PyPI was configured by the user (repository
  `FormalLanguageConstrainedPathQuerying/CFPQ_Data`, workflow `publish.yml`).
- The changelog line "The changes below make up the upcoming **5.0.0**
  release." must be dropped before promotion: after the bump it would sit
  under the released `[5.0.0]` heading and leak into the GitHub Release notes
  (extracted by `publish.yml` from the `## [5.0.0]` section).

## Human gates (user guidance, verbatim in tasks.md)

1. The user reviews and merges the `dev` -> `master` PR manually. No tag is
   created and nothing is pushed to `master` before the user confirms the
   merge.
2. The tag is created on `origin/master` after a fresh `git fetch origin`, so
   it points at the merged commit.

## Subtasks

### S1: Write this detailed plan

**Code:** none (documentation-only)
**Tests:** skip — no code to test
**Docs:** `tasks/detailed_plan.md`

**Spec:** Record context, verified facts, human gates, and subtasks S2-S5.

### S2: Finalize the changelog and promote it to [5.0.0]

**Code:** none (runs the existing `utils/bump_version.py`)
**Tests:** skip — no code changes; the version guard is verified explicitly
**Docs:** `CHANGELOG.md` (drop the "upcoming" line; section promoted by the
         helper)

**Spec:**
- Remove the "The changes below make up the upcoming **5.0.0** release." line.
- Run `python utils/bump_version.py 5.0.0`; it promotes `[Unreleased]` to
  `## [5.0.0] - <today>` and inserts a fresh empty `[Unreleased]`.
- Verify `poetry run pre-commit run check-version-sync --all-files` passes.
- Commit on `dev` with the release-skill message: `chore: release 5.0.0`.

### S3: Push dev and open the release PR (human gate after)

**Code:** none
**Tests:** skip
**Docs:** none

**Spec:**
- `git push origin dev` (release exception to the no-push convention).
- Open a PR `dev` -> `master` via `gh pr create` with a title/body describing
  the v5.0.0 release; do not merge it.
- STOP and ask the user to review and merge the PR manually. Do not proceed
  to S4 before the user confirms the merge.

### S4: Tag the merged commit and push the tag

**Code:** none
**Tests:** skip
**Docs:** none

**Spec:**
- Only after the user confirms the PR is merged: `git fetch origin`.
- `git tag -a v5.0.0 -m "Release v5.0.0" origin/master` — the tag points at
  the merged commit on `origin/master`, never at a local ref.
- `git push origin v5.0.0`. This triggers the `publish` workflow.

### S5: Verify the publish and mark the task done

**Code:** none
**Tests:** skip
**Docs:** `tasks/tasks.md` (mark task 35 done)

**Spec:**
- Watch the `publish` workflow run (tag verification, build, PyPI publish via
  Trusted Publishing, GitHub Release creation).
- Verify the package is live on PyPI and the GitHub Release carries the
  `[5.0.0]` changelog section.
- Prepend `[done] ` to the task 35 line in `tasks/tasks.md` (local commit on
  `dev`; pushed with the next dev push — the release itself is already out).

### S6: Make intersphinx inventory fetches resilient to transient network errors

Added 2026-09-16 at the merge gate (user: "CI report set of warnings ... Fix
it"). The first CI run on `20a181a` failed its Docs build because the runner's
connection to `networkx.org` was reset while fetching the intersphinx
inventory; with the inventory missing, every `nx.MultiDiGraph` cross-reference
went unresolved and failed the build under the no-warnings policy. A second
run of the same commit passed — the failure was a transient network flake, not
a docs defect.

**Code:** `docs/conf.py` (retry wrapper around `sphinx.util.requests.get`)
**Tests:** skip — build configuration only; verified by a clean docs build
**Docs:** `docs/developer.rst` ("Docs build and deploy" section)

**Spec:**
- Retry only transient connection errors (`ConnectionError`, `Timeout`); a
  final failure propagates, so the warning still fires and the build still
  fails — no suppression.
- Note the behavior in the "Docs build and deploy" section of
  `docs/developer.rst`.

### S7: Fix sdist packaging so `python -m build` succeeds

Added 2026-09-16 at the publish gate. The first real `python -m build` run
(publish workflow on tag `v5.0.0`) failed: `setup.py` reads
`requirements/*.txt`, but no MANIFEST.in existed, so the files were missing
from the sdist and the sdist→wheel step raised FileNotFoundError. This is the
first packaging build in the project's history — it was never exercised
before.

**Code:** `MANIFEST.in` (new: `include requirements/*.txt`)
**Tests:** skip — verified with an isolated `python -m build` (clean venv,
same as CI); sdist contains all four requirements files and the wheel builds.
**Docs:** none

### S8: Publish to TestPyPI on every PR targeting master

Added 2026-09-16 at the merge gate (user request: validate publishing
automatically before the human merge). The `publish` workflow gains a
`pull_request: branches: [master]` trigger; the `publish-testpypi` job runs on
PRs with `skip-existing: true` because concurrent PRs share one package
version and TestPyPI rejects re-uploads of existing files.

Final design (after the first PR run failed): TestPyPI uses **OIDC Trusted
Publishing**, not a token — the first run proved the pypi-publish action
silently falls back to OIDC when no token secret exists, and the user prefers
no long-lived secrets (consistent with the PyPI setup). The publisher's
subject claim is `repo:FormalLanguageConstrainedPathQuerying/CFPQ_Data:pull_request`
(the documented sub for pull_request events; confirmed in the failed run's
claims dump). The manual `workflow_dispatch` TestPyPI path was removed: its
sub claim cannot match the PR publisher, and the PR check fully covers
pre-release validation (a tag always points at a merged PR's head).

**Code:** `.github/workflows/publish.yml`
**Tests:** skip — workflow-only; the build step is the check itself
**Docs:** `docs/release.rst` (Package publishing section), `CHANGELOG.md`

### S9: Check out the repo in the publish-pypi job

Added 2026-09-16 at the publish gate. The real tag push published to PyPI
successfully, but "Create GitHub Release" failed with
`awk: fatal: cannot open file 'CHANGELOG.md'`: the `publish-pypi` job never
checked out the repository (it only downloads the dist artifact), so the
changelog was absent from its working directory. Latent bug — the step had
never run before because every earlier attempt died upstream. The v5.0.0
GitHub Release was created manually (same notes + the exact PyPI artifacts as
assets) while this fix lands via PR for future releases.

**Code:** `.github/workflows/publish.yml` (`actions/checkout@v7` in
`publish-pypi`)
**Tests:** skip — workflow-only
**Docs:** none
