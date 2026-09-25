# Detailed Plan: Task 128 — Migrate task tracking from tasks.md to GitHub issues

## Context

Task logging and tracking currently lives in `tasks/tasks.md` (numbered task
lines, `[done]` prefix, `**[USER GUIDANCE]**` line annotations). Move it to
GitHub issues via `gh`: every task becomes an issue with the `task` label,
the task ID becomes the issue number, user guidance becomes issue comments,
and completion closes the issue via the existing commit-keyword mechanism.

Approved model (user decisions):

- Task = GitHub issue, label `task`; task ID = issue number → commit scope
  `feat(128-S1)`.
- New task → `gh issue create` (description verbatim); user guidance →
  `gh issue comment` (issue body immutable).
- The detailed plan is posted as a marked comment on the task issue at
  planning time and mirrored after every subtask completes.
- Done → the LAST subtask's commit carries `Closes #<own issue>`; the issue
  auto-closes when the release lands on `master`. A task is "done" for
  selection purposes when its subtask commits are on `dev`.
- `tasks/tasks.md` stays as an immutable archive; open tasks 53 and 58 are
  migrated to issues. `detailed_plan.md` / `global_plan.md` stay local.

## Subtasks

### S1: Introduce issue-based tracking in workflow-management [done] 59b0640

**Code:** `.opencode/skills/workflow-management/SKILL.md`, plus this plan file
**Tests:** skip (docs-only)
**Docs:** the skill file itself

**Spec:**
- Core rule: log all tasks as GitHub issues with the `task` label
  (`gh issue create`); description verbatim; task ID = issue number.
- Step 0: multiple tasks at once → one issue per task first, then the global
  plan in `tasks/global_plan.md` references issue numbers.
- Step 2: choose one open `task` issue with no commits on `dev`
  (`git log dev --format=%s | grep -cE '\(<N>-S[0-9]+\):'` == 0).
- Step 4: after writing `tasks/detailed_plan.md`, post it as a comment on the
  task issue; first line of the comment is the marker `<!-- detailed-plan -->`.
- Step 8: verify the LAST subtask's commit carries `Closes #<N>` (own issue);
  pointer to Task Completeness Verification unchanged.

### S2: Re-point completion semantics in subtask-loop [done] b0e7c93

**Code:** `.opencode/skills/subtask-loop/SKILL.md`
**Tests:** skip (docs-only)
**Docs:** the skill file itself

**Spec:**
- Step 7 Mark Completed: mark `[done]` + commit hash in `detailed_plan.md`,
  then mirror the file onto the marked plan comment of the task issue
  (find by marker, PATCH body). Local file = source of truth; comment =
  pure mirror.
- Blocked Work Protocol: guidance per user-guidance-transfer (issue comment);
  post the block report (Design Notes) as a comment on the task issue.
- Task Completion Verification: "before a task is considered done (its last
  subtask's commit carries `Closes #<N>`, merged to dev), verify: ...".
- Marking Complete: replace the `[done]`-prefix rule — complete = every
  requirement met; the issue closes automatically at release; never edit the
  issue body.

### S3: Re-point task authoring and review references [done] d61e41a

**Code:** `.opencode/skills/planning/SKILL.md`, `.opencode/skills/code-review/SKILL.md`
**Tests:** skip (docs-only)
**Docs:** the skill files themselves

**Spec:**
- planning "Task Authoring Guidelines": "When creating a new task issue
  (`gh issue create`, label `task`)..." — rules apply to the issue body;
  completeness pointer drops the tasks.md wording.
- code-review checklist item 1: "every clause of the task issue (#N) is
  traceable to committed code."

### S4: Rewrite user-guidance-transfer for issues [done] 511704a

**Code:** `.opencode/skills/user-guidance-transfer/SKILL.md`
**Tests:** skip (docs-only)
**Docs:** the skill file itself

**Spec:**
- Procedure: `gh issue comment <N>` with a verbatim `[USER GUIDANCE]` quote;
  never edit the issue body (user-authored, immutable); Design Notes
  cross-reference unchanged; update frontmatter description.

### S5: Update commit/issue model in docs + git-workflow [done] 7375e24

**Code:** `docs/developer.rst`, `.opencode/skills/git-workflow/SKILL.md`
**Tests:** skip (docs-only)
**Docs:** developer.rst is the doc; verify navigation links unaffected

**Spec:**
- developer.rst Commits: "XXX is the task's GitHub issue number."
- developer.rst Issue references: every task IS a GitHub issue (label
  `task`); ALL closing keywords (own issue + fully-resolved linked issues) go
  in exactly one commit — by convention the LAST subtask's commit — as
  standalone body lines; partial work uses bare `#N`; note that an incomplete
  branch therefore carries no keyword and cannot close its issue.
- git-workflow "Issue-closing validation": unconditional for the own issue;
  grep count must be 0 until the last subtask's commit, then exactly K lines.

### S6: Migrate open tasks and archive tasks.md [done] 651b4f4

**Code:** GitHub (issues), `tasks/tasks.md`
**Tests:** skip (docs-only)
**Docs:** archive banner in `tasks/tasks.md`

**Spec:**
- Create issues for Task 53 and Task 58: title keeps the "Task N:" prefix
  (traceability to the archive), body = description verbatim, label `task`,
  existing **[USER GUIDANCE]** quotes posted as the first comment.
- Prepend a one-line archive banner to `tasks/tasks.md`; task lines untouched.
- This subtask's commit carries `Closes #128` (the task's own issue).
