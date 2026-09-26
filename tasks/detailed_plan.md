# Detailed Plan: Issue #131 — FSA canonical grammar does not match the distributed grammar

## Context

The "Canonical grammars" section of `docs/graphs/field_sensitive_alias.rst`
describes the `vf` query language. The dataset (source of truth) ships the
query in every 6.0.0 archive as `queries/cfpq/vf/vf.cnf` + `vf.rsm`. The RSM
block on the page matches `vf.rsm` verbatim, but the CFG math block does not
match `vf.cnf`:

- Docs: `V → A V A | f_r_i V f_i | M | a_r V a | ε`, `A → a M? | ε`
- Archive (`vf.cnf`): `V → A_r V | V A | FV_i f_i | M | ε`,
  `FV_i → f_r_i V`, `A_r → M a_r | a_r | ε`, `A → a M | a | ε`

The two define different languages (verified by CYK membership check on the
short paths): `a_r`, `a a`, and `a_r a_r` are accepted by the archive grammar
and rejected by the docs grammar. The issue (#131) was reported against the
deployed site, where the page had no reverse symbols at all; dev partially
fixed it (commit 06ebf6d added `d_r`/`f_r_i` and the correct RSM block) but
the `a` part is still wrong.

Approved fix (user: work on the existing issue #131, no new one): make the
docs CFG language-identical to the distributed grammar, keeping the page's
existing compressed presentation style (the archive's helper nonterminals
`DV`/`FV_i` are inlined exactly as `M → d_r V d` and `f_r_i V f_i` already
are). The RSM block is already correct and stays untouched.

## Subtasks

### S1: Fix the canonical grammar math block [done] a570f53

**Code:** none (docs-only task)
**Tests:** skip code tests; run `utils/check_math_snippets.py` and the docs
build (quality gate) to prove the new math renders
**Docs:** `docs/graphs/field_sensitive_alias.rst` — the "Canonical grammars"
math block

**Spec:**
- Replace the math block with the productions of the distributed grammar in
  the page's compressed style:
  - `M → d_r V d` (unchanged)
  - `V → A_r V | V A | f_r_i V f_i | M | ε`
  - `A_r → M a_r | a_r | ε`
  - `A → a M | a | ε`
- Keep the surrounding text ("Productions with index i ...", "Reversed edges
  (a_r, d_r, f_r_i) are auto-generated from forward edges.") and the RSM
  block unchanged.
- The commit carries `Fixes #131` as a standalone body line (the task's own
  issue is the bug being fixed).
