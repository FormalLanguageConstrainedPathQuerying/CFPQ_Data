---
name: workflow-management
description: Load first at the start of every session, before doing anything else. Drives the overall working loop for a task or set of tasks: global plan, one task at a time, feature branch, detailed plan, subtask execution, code review, quality gate, merge.
---

# Workflow Management

The top-level loop that orchestrates all other workflow skills. For a
single task, load this skill first; it points to the skills that handle each
step.

## Core Rules

- Log all tasks as GitHub issues with the `task` label (`gh issue create`).
  Use the description exactly as the user provided it — minimal changes, only
  splitting and numbering. The task ID is the issue number.
- Do tasks strictly **one at a time**. Each task gets its own feature branch,
  its own detailed plan, and its own merge to `dev`. Never combine multiple
  tasks in a single feature branch.
- Each decision must be documented before implementation. Documentation must
  be detailed enough to reproduce the project from scratch and understand why
  each decision was made.
- Commit messages must be detailed enough to understand the reasons for
  changes.
- Documentation-only tasks (no `.py` files changed) skip code-specific gates
  (tests, lint, format) but still follow all other workflow rules: one task
  per branch, one commit per subtask, code review.

## Working Loop

0. If the user requests multiple tasks at once, first create one issue per
   task, then create a global plan in `tasks/global_plan.md` referencing the
   issue numbers (see the `planning` skill) before proceeding.
1. Ensure user-defined tasks, the global plan, and project architecture are
   aligned.
2. Choose exactly ONE open `task`-labeled issue that is not yet done: a task
   is done when its subtask commits are on `dev`
   (`git log dev --format=%s | grep -cE '\(<N>-S[0-9]+\):'` > 0, where N is
   the issue number). List candidates with
   `gh issue list --label task --state open`.
3. Create a feature branch from `dev` for this single task (branching model:
   the "Contribution guidelines" section of `docs/developer.rst`; procedure:
   `git-workflow`).
4. Generate a detailed plan in `tasks/detailed_plan.md`, decomposing the task
   into atomic subtasks (see `planning`), then post it as a comment on the
   task issue; the first line of the comment is the marker
   `<!-- detailed-plan -->`.
5. Load the `subtask-loop` skill, then execute each subtask using its cycle.
5a. Verify all subtasks are complete and unblocked. Check
    `tasks/detailed_plan.md`:
    - If any subtask is marked `[blocked]` or `[deferred]`, STOP immediately.
      The task is NOT complete. Do NOT proceed to code review or merge.
      Report blocking subtasks to the user and await guidance.
    - If a subtask was attempted, not committed, and its work reverted, the
      subtask is NOT complete. Do not silently skip it.
5b. When continuing a partially-done task, analyze current state before any
    code changes:
    - Verify `git branch --show-current` is the correct feature branch.
    - Review committed subtasks: `git log --oneline` on the feature branch.
    - Read `tasks/detailed_plan.md` and `tasks/global_plan.md`.
    - Cross-reference committed file changes with planned subtasks:
      `git diff --stat HEAD..dev`.
    - Report status to the user: "S1-S3 committed, S4 pending, ..."
6. After all subtasks are done, perform code review on the entire repo (see
   the `code-review` skill). Iteratively detect and fix problems until zero
   findings.
7. Load the `quality-gates` skill and run the gate. It must show PASS. If
   BLOCKED, do not assess whether failures are pre-existing or unrelated to
   your changes; fix every failure and re-run until PASS. Then merge the
   feature branch to `dev` (see `git-workflow`). Verify
   `git branch --show-current` is `dev`.
8. Verify the last subtask's commit carries `Closes #<N>` (the task's own
   issue) as a standalone line — the issue closes when the release lands on
   `master`. See the Task Completeness Verification in the `subtask-loop`
   skill (the single source of truth for what "done" means).
9. Return to step 2.
