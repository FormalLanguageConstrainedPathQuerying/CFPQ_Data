---
name: quality-gates
description: Use before merging a task to dev. Defines the hard gate that must pass (tests + style + type check + docs build) and how to interpret its result. References docs/developer.rst for the exact commands.
---

# Quality Gates

The hard gate a task must pass before merging. It has exactly two terminal
states: **PASS** or **BLOCKED**. There is no "pass with exceptions".

## What the gate is

The gate is the combination of the test suite, the style/lint checks, the
type check, and the docs build:

- **Tests** — see the "Test pipeline" section of `docs/developer.rst` for
  the exact command. The canonical command includes the coverage check: it
  fails unless both line and branch coverage are at least 95%.
- **Style/lint** — see the "Quality checks" section of `docs/developer.rst`
  for the exact command.
- **Type check** — `uv run ty check` must report no errors; CI additionally
  runs Pyright (see the "Quality checks" section of `docs/developer.rst`).
- **Docs build** — see the "Docs build and deploy" section of
  `docs/developer.rst` (and `docs/README.md`) for the exact command. It must
  exit 0. The build runs under the no-warnings policy (`-W --keep-going`, see
  `docs/Makefile`): any warning — including an unresolved cross-reference
  under `nitpicky = True` — fails the build, so the exit code is sufficient.
  There are no tolerated warnings; fix them instead of suppressing.
- **Link check (CI only)** — not part of the local gate: it is network-bound
  and slow locally (rate-limited retries). The "Check links" step of
  `.github/workflows/docs.yml` must be green for the branch before merge.

The CI workflows are the source of truth for the commands they run (see
the "CI as source of truth" section of `docs/developer.rst`); this skill
only defines the gate semantics.

## Procedure

1. Run the full test suite ("Test pipeline" section of `docs/developer.rst`).
   It must show 0 failures and 0 skipped, and the coverage check must pass
   (line and branch each at least 95%).
2. Run the full style/lint pass ("Quality checks" section of
   `docs/developer.rst`). It must show no errors.
3. Run the type check (`uv run ty check`). It must report no errors.
4. Build the docs ("Docs build and deploy" section of `docs/developer.rst`).
   It must exit 0 (no-warnings policy: any warning fails the build).
5. Confirm the branch's CI link check ("Check links" step of
   `.github/workflows/docs.yml`) is green — it runs in CI only, not locally.
6. Interpret the result:
   - All clean → **PASS**. Proceed to merge (see `git-workflow`).
   - Any failure → **BLOCKED**.

## On BLOCKED

- STOP. Do not merge. Do not mark the task done.
- Do **not** assess whether a failure is pre-existing or unrelated to your
  changes — fix it regardless.
- Do **not** weaken, skip, or comment out failing tests to make the suite green
  (see the Blocked Work Protocol in the `subtask-loop` skill).
- Fix every failure and re-run until **PASS**.
