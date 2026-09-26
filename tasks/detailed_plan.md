# Detailed Plan: Issue #134 — Remove untracked scratch files and ignore test.csv

## Context

The working tree carries two untracked scratch files that are not ignored:
`endpoints` (a Yandex Cloud endpoint dump from local tooling) and `test.csv`
(a leftover from an older csv doctest; current doctests write to temp dirs).
Neither is part of the package, docs, or tests. The fix removes both and adds
`test.csv` to the "# Doctest files" section of `.gitignore` so a regenerated
scratch file cannot be committed by accident.

Verified on dev: `git status --short` shows exactly these two untracked files;
the "# Doctest files" section of `.gitignore` currently lists `test.mcfg`,
`test.txt`, and `test.xml` (no `test.csv`).

## Subtasks

### S1: Delete the scratch files and ignore test.csv [pending]

**Code:** none (working-tree cleanup + `.gitignore`)
**Tests:** skip (no code); confirm `git status --short` is clean afterwards
**Docs:** `.gitignore` — the "# Doctest files" section

**Spec:**
- Delete the untracked files `endpoints` and `test.csv` from the working tree.
- Add `test.csv` to the "# Doctest files" section of `.gitignore`, alongside
  `test.mcfg` / `test.txt` / `test.xml` (keep the block's existing order/style).
- The commit carries only the `.gitignore` change; the deletions are
  working-tree cleanup of untracked files (nothing to stage).
