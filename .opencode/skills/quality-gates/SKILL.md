---
name: quality-gates
description: Use before merging a task to dev. Defines the hard gate that must pass (tests + style + docs build) and how to interpret its result. References the run-tests, code-style, and build-docs skills for the exact commands.
---

# Quality Gates

The hard gate a task must pass before merging. It has exactly two terminal
states: **PASS** or **BLOCKED**. There is no "pass with exceptions".

## What the gate is

The gate is the combination of the test suite, the style/lint checks, and
the docs build:

- **Tests** — see the `run-tests` skill for the exact command.
- **Style/lint** — see the `code-style` skill for the exact command.
- **Docs build** — see the `build-docs` skill for the exact command. It must
  exit 0 and print no `ERROR:` lines (Sphinx errors do not fail the build on
  their own, so check the log, not just the exit code). The pre-existing
  warnings are tolerated.

`run-tests`, `code-style`, and `build-docs` are the single source of truth
for the commands; this skill only defines the gate semantics.

## Procedure

1. Run the full test suite (`run-tests`). It must show 0 failures and 0 skipped.
2. Run the full style/lint pass (`code-style`). It must show no errors.
3. Build the docs (`build-docs`). It must exit 0 with no `ERROR:` lines.
4. Interpret the result:
   - All clean → **PASS**. Proceed to merge (see `git-workflow`).
   - Any failure → **BLOCKED**.

## On BLOCKED

- STOP. Do not merge. Do not mark the task done.
- Do **not** assess whether a failure is pre-existing or unrelated to your
  changes — fix it regardless.
- Do **not** weaken, skip, or comment out failing tests to make the suite green
  (see the Blocked Work Protocol in the `subtask-loop` skill).
- Fix every failure and re-run until **PASS**.
