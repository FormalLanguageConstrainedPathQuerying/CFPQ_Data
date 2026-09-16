---
name: git-workflow
description: Use when doing git operations: committing, merging, rebasing. Covers the operational procedure (commit validation, merge to dev, pre-merge checks); the branching/commit model lives in docs/developer.rst.
---

# Git Workflow

The model (branching scheme, commit message format, merge strategy, quality
gate) is documented in the "Contribution guidelines" section of
`docs/developer.rst` (single source of truth). This skill keeps only the
operational procedure.

## Commits

**Pre-commit validation**: before running `git commit`, verify the prepared
message follows the format from the docs — Conventional Commits with exactly
one subtask identifier (`feat(XXX-SN): ...`; ranges, lists, or commas are
forbidden). If the message mentions multiple subtask identifiers, STOP —
split the changes into individual commits. One commit per completed atomic
subtask.

### Pre-commit checklist

1. Run commit gate: code-style, all tests, linters.

### Commit scope

- Each commit is a self-contained, compilable, testable increment
- Commit messages must be detailed enough to understand why changes were required

## Merging to dev

### Pre-merge checks

Run the quality gate (see the `quality-gates` skill). All checks MUST pass
before merging. **This is absolute — no exceptions, no self-assessment.**

### Merge strategy

Rebase the feature branch onto `dev`, then fast-forward `dev` to it. The
individual subtask commits are preserved and the history of `dev` stays
linear. Never squash: squashing destroys the per-subtask commit structure
that the commit message format is built around (each commit already carries
its own detailed message, so no combined merge message is needed).

```bash
git checkout dev
# only if dev has new commits since the branch was created:
git checkout feature/XXX-short-description && git rebase dev && git checkout dev
git merge --ff-only feature/XXX-short-description
git branch -d feature/XXX-short-description
```

If `dev` has not moved, skip the rebase — the fast-forward alone is enough.
Delete the merged feature branch (safe delete only).

## Rules

- No emergency fixes
- All work is local, no `push`-es
