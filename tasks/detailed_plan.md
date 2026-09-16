# Task 36: Document the release experience (global → docs, local → skill)

## Context

Task 35 cut v5.0.0 and surfaced a series of release-flow incidents (intersphinx
network flake, missing MANIFEST.in, TestPyPI PR check via OIDC Trusted
Publishing, the `/legacy/` TestPyPI upload URL, the missing checkout in the
`publish-pypi` job). The user asks that all experience and knowledge on
releases be documented so the next release is fast and smooth, and requires a
strict split:

- **Global knowledge** — useful for all developers — lives in `docs/`
  (the model: "What" and "Why").
- **Local knowledge** — agent-specific operational details (commands,
  pitfalls, procedures) — lives in the `release` skill (the "How"), which
  stays a thin pointer to the docs.

## Knowledge split (decision record)

Global → `docs/release.rst` (facts any developer of the project needs):

- The sdist-completeness constraint: `python -m build` builds the wheel from
  the sdist, so the sdist must contain everything `setup.py` reads at build
  time (`requirements/*.txt`, included via `MANIFEST.in`).
- PyPI and TestPyPI reject re-uploads of files that already exist for a
  version; the PR check uses `skip-existing`; if a tag push reaches PyPI and
  then fails, an owner must delete the release before the tag can be
  re-pushed.
- Merging a pull request into `master` never publishes: the workflow runs
  only on `v*` tag pushes (the merge does redeploy the docs site).

Local → `.opencode/skills/release/SKILL.md` (agent operations only):

- Pre-tag gate: wait for the PR's Publish check (TestPyPI pre-publish) to pass
  before asking the user to merge and before tagging.
- Human merge gate: the user reviews and merges the PR manually; tag + push
  only after the user confirms the merge (tag on `origin/master` after a fresh
  `git fetch origin`).
- Verification of both PyPI and the GitHub Release page (changelog notes +
  dist assets).
- Recovery procedures: workflow failure before the PyPI publish (delete the
  tag, fix, merge, re-tag) and after it (an owner deletes the PyPI release
  first — the fact lives in the docs; create the GitHub Release manually via
  the API, including the `upload_url` asset-upload quirk).
- Machine notes: no `gh` CLI on this machine — use curl + the GitHub API with
  the token extracted from the remote URL (never echoed).

Not documented here (implementation details readable in
`.github/workflows/publish.yml` itself): the checkout step of `publish-pypi`,
the `/legacy/` TestPyPI repository URL, action versions.

## Subtasks

### S1: Record task 36 in the task log and write this detailed plan

**Code:** none (documentation-only)
**Tests:** skip — no code to test
**Docs:** `tasks/tasks.md` (task 36 line; the session's user guidance appended
         verbatim to the task 35 line), `tasks/detailed_plan.md`

**Spec:**
- Add the task 36 line with the user's exact wording and the split
  instruction as `[USER GUIDANCE]`.
- Append, verbatim, the five user-guidance quotes given during task 35
  (actions update, CI warning fix, TestPyPI-on-PR request, trusted-publisher
  question, safe-to-merge question) to the task 35 line.
- Replace `tasks/detailed_plan.md` with this plan.

### S2: Record the global release knowledge in docs/release.rst

**Code:** none
**Tests:** skip — docs only; verified by the clean docs build and link check
         in the quality gate
**Docs:** `docs/release.rst` ("Package publishing (automated)" section)

**Spec:**
- Commit the drafted additions already present in the working tree: the two
  packaging constraints (sdist completeness via `MANIFEST.in`; re-upload
  rejection and its consequence for re-pushing a tag) and the "merging never
  publishes" paragraph.
- Review them against the actual `publish.yml` behavior before committing; do
  not restate agent procedures here — those belong to the skill.

### S3: Record the local release knowledge in the release skill

**Code:** none
**Tests:** skip — skill only
**Docs:** `.opencode/skills/release/SKILL.md`

**Spec:**
- Procedure: step 4 gains the pre-tag gate (the PR's Publish check must pass)
  and the human merge gate (the user merges manually; proceed only after
  confirmation); step 6's verification extends to the GitHub Release page
  (changelog notes + dist assets), not just PyPI.
- New "Recovery" section: (a) workflow failure before the PyPI publish —
  delete the tag, fix, merge the fix, re-tag on the new `origin/master`;
  (b) failure after the PyPI publish — an owner deletes the PyPI release
  first (reference `docs/release.rst` for the fact, do not re-describe it),
  then create the GitHub Release manually via the API with the exact working
  commands: token from the remote URL (never echoed), `awk` extraction of the
  `[X.Y.Z]` changelog section, `POST /releases`, asset upload via the
  created release's `upload_url` (`uploads.github.com`) — posting to
  `api.github.com/.../releases/{id}/assets` returns 404.
- Notes: the `gh` CLI is not installed on this machine — use curl + the
  GitHub API.
- Keep the skill a thin pointer: facts already in `docs/release.rst` are
  referenced, never re-described.

### S4: Mark task 36 done in the task log

**Code:** none
**Tests:** skip
**Docs:** `tasks/tasks.md`

**Spec:** After code review, the quality gate, and the merge to `dev`,
prepend `[done] ` to the task 36 line (commit on `dev`).
