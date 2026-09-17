# Task 38: Issue-closing commit messages

Task (verbatim): We use mechanism to close issues automatically described here: https://github.blog/news-insights/product-news/closing-issues-via-commit-messages/    Improve imstructions to write respective commut message when task is link to issue.

Branch: `feature/38-issue-closing-commit-messages` (from `dev`).
Documentation-only task: no `.py` files change; code-specific gates (tests,
lint, format) are skipped per the workflow rules, docs build + link check still apply.

## Decision record

Decisions made before implementation:

1. **Mechanism** (per the linked GitHub post): GitHub closes an issue when a
   commit whose message contains a closing keyword (`close`, `closes`,
   `closed`, `fixes`, `fixed`) reaches the repository's **default branch**.
   Verified for this repo: the default branch is `master`
   (`git ls-remote --symref origin HEAD` -> `refs/heads/master`).
2. **Closing timing**: our flow merges feature branches to `dev`; only a
   release merges `dev` -> `master`. Therefore a linked issue closes when the
   release containing the task lands on `master`, not when the task merges to
   `dev`. This is documented as intended behavior: an issue stays open until
   the fix is actually released.
3. **Placement**: exactly one commit of a task carries the closing keyword —
   by convention the **first subtask's commit**, as a standalone line in the
   message body. Rationale: a branch merges only after ALL subtasks complete,
   so placement does not affect correctness; the first commit makes validation
   monotonic (0 matches before S1, 1 afterwards) and never requires rewording
   when the plan grows.
4. **Keyword choice**: `Fixes #N` when the task fixes a reported defect,
   `Closes #N` for all other work. One keyword line per fully resolved issue.
5. **Partial resolution**: reference the issue without a closing keyword (bare
   `#N`) — GitHub links it but leaves it open. Consistent with the task 34
   user guidance "Reference partial, no close claim".
6. **Single source of truth**: the model lives in the "Contribution
   guidelines" section of `docs/developer.rst` (new "Issue references"
   subsection); the `git-workflow` skill gains only the operational validation
   and points to the docs. No other skill is touched (`subtask-loop` step 6
   already defers commit rules to `git-workflow`).

## Subtasks

### S1: Record task 38 in the task log and write the detailed plan [done — 3cb5dc3]

**Code:** N/A (documentation-only task)
**Tests:** Skip — no code to test
**Docs:** `tasks/tasks.md` (append the task line, user wording verbatim),
         `tasks/detailed_plan.md` (this plan)

**Spec:**
- Append `- Task 38: <user wording verbatim>` to `tasks/tasks.md`.
- Replace `tasks/detailed_plan.md` with this plan.

### S2: Document the issue-closing commit rules in the developer docs [done — 73581a6]

**Code:** N/A (documentation-only task)
**Tests:** Skip — no code to test
**Docs:** `docs/developer.rst` — "Contribution guidelines" section, new
         "Issue references" subsection right after the "Commits" format text.

**Spec:**
- State the mechanism: GitHub closes an issue once a commit containing a
  closing keyword (`close`, `closes`, `closed`, `fixes`, `fixed`) reaches the
  default branch; link the GitHub blog post as the source.
- Rule 1 (full resolution): exactly one commit of the task carries the
  keyword — by convention the first subtask's commit — as a standalone line
  in the message body: `Fixes #N` for defects, `Closes #N` otherwise; no other
  commit of the task repeats it. Include a short example.
- Rule 2 (partial resolution): bare `#N`, no keyword — linked, not closed.
- Timing note: with the dev -> master release flow, a linked issue closes when
  the release lands on `master`, not at merge to `dev`.

### S3: Add operational validation to the git-workflow skill [done — 1a0a196]

**Code:** N/A (documentation-only task)
**Tests:** Skip — no code to test
**Docs:** `.opencode/skills/git-workflow/SKILL.md` — "Commits" section, extend
         the pre-commit validation.

**Spec:**
- Add an **Issue-closing validation** paragraph: if the task fully resolves a
  linked issue, the first subtask's commit must carry the keyword line and no
  later commit of the task may repeat it.
- Verification command on the feature branch:
  `git log dev..HEAD --format=%B | grep -cE '^(Fixes|Closes) #[0-9]+$'` — must
  print `0` before the first subtask's commit and, afterwards, exactly one
  line per fully resolved issue (no more).
- Partially addressed issues use a bare `#N` reference (no keyword).
- Point to the "Contribution guidelines" section of `docs/developer.rst` for
  the model and closing timing — the skill stays a thin pointer.

### S4: Mark task 38 done in the task log [done — 6704bc3]

**Code:** N/A (documentation-only task)
**Tests:** Skip — no code to test
**Docs:** `tasks/tasks.md` — prepend `[done] ` to the task 38 line.

**Spec:**
- Only prepend `[done] ` to the existing line; never rewrite the task
  description (user-authored, immutable).

### S5: Make the link check deterministic on rate-limited networks

Added 2026-09-17 during the quality gate. The full link check failed with
403 "Too many requests" from `en.wikipedia.org` on two of the four Wikipedia
URLs (pre-existing links in `grammars/data/dyck.rst` and the generated
`cfpq_data.grammars.converters.cfg` page — not introduced by this task).

Root cause (verified empirically): with the configured descriptive
User-Agent, all four URLs answer 200 when requested **sequentially**
(`curl`, 5 s apart), but linkcheck's default parallel worker pool triggers
Wikipedia's per-IP rate limit from this datacenter network — the same
failure mode already documented in `docs/conf.py` for `dl.acm.org` and
`dacapobench.sourceforge.net`, except there the block is persistent while
here it is concurrency-driven. Retrying with delays did not stabilize the
result (different subsets of the four URLs failed per run).

**Code:** N/A (documentation-only task)
**Tests:** Skip — no code to test
**Docs:** `docs/conf.py` — add `linkcheck_workers = 1` next to the other
         linkcheck settings, with the rationale comment.

**Spec:**
- Sequential checking is not an ignore: every URL is still checked in full;
  only the concurrency changes (the check gets slower, never weaker).
- Re-run the full link check; it must report no broken or timed-out links.
