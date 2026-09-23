# Detailed Plan: Task 57 — Fix LaTeX error in the C Alias grammar parameters (#127) + prevent recurrence

## Context

Issue #127: on the deployed C Alias page, the Parameter column renders the
MathJax error `'_’ allowed only in math mode` instead of the parameter name.

Root cause: `docs/grammars/data/c_alias.rst` wraps identifiers containing
underscores in `:math:`\textit{...}``. Inside a math environment `\textit`
switches to text mode (MathJax supports it; raw LaTeX does not define
`\textit` in math mode at all); `_` is illegal in text mode, so MathJax
renders the error instead of the formula. 10 occurrences on 7 lines: the
Parameter table (lines 38, 40) and the Example Grammars section (lines 63,
67, 70, 93, 94).

Why CI missed it: the error only occurs at browser runtime. Sphinx passes
math content verbatim to MathJax; `make html -W` + linkcheck + pytest never
validate math snippets.

Why only C Alias breaks: it is the only page with an underscore *inside* a
`\textit{...}` group. Other pages write subscripts outside the group
(`\textit{load}_f`), which is valid math. Verified across `docs/`:
c_alias.rst is the sole offender.

Structural cause: grammar data pages are hand-written transcriptions of
generator signatures/docstrings; c_alias.rst deviates from the PR template
convention (`.github/PULL_REQUEST_TEMPLATE/new_grammar.md` specifies literal
style for parameter names). Nothing validates docs math or cross-checks docs
against code.

## Decisions (user-approved)

- Fix style: parameter names -> literal style (matches the PR template);
  reverse labels in math blocks -> plain subscripts (`a_r`, `d_r`),
  consistent with `V_1`/`V_2`/`V_3` and plain `a`/`d` already on the page.
- Test scope: deterministic targeted rule now (zero new deps); evaluate
  `latex2mathml` against the corpus during S3 and adopt it as an additional
  check only if it rejects the broken snippets and accepts all current ones
  with zero false positives.

## Reuse analysis

- No existing math validation anywhere in the repo (no latex2mathml, no RST
  math extraction) — new material is justified.
- Follows the established `utils/<tool>.py` + `tests/utils/test_<tool>.py`
  pattern (e.g. `check_version_sync.py`, `audit_info_tables.py`); tests
  import the tool module directly (`extraPaths = ["utils"]` is already
  configured for ty and pyright).
- Changelog: extend the existing `[Unreleased]` section (new `### Fixed`
  subsection + one `### Added` entry).

### S1: Record task 57 in the task log and write the detailed plan

**Code:** none
**Tests:** none
**Docs:** `tasks/tasks.md` (task 57 entry), `tasks/detailed_plan.md` (this file)

**Spec:**
- Add the Task 57 entry after task 56 with the user decisions recorded.
- Write this detailed plan.
- The commit carries `Fixes #127` (the task fully resolves the defect).

### S2: Fix the broken math in docs/grammars/data/c_alias.rst

**Code:** none (docs-only change)
**Tests:** verified by the S3 guard once it exists; until then, a search for
an underscore inside a `\textit{...}` group across `docs/` must return no
hits.
**Docs:** `docs/grammars/data/c_alias.rst`

**Spec:**
- Parameter table (lines 38, 40): `:math:`\textit{assigment_labels}`` ->
  `` `assigment_labels` `` and `:math:`\textit{dereference_labels}`` ->
  `` `dereference_labels` `` (literal style per the PR template).
- Line 63 prose: parameter names -> literal; keep the label pairs as math:
  "C Alias grammar with `assigment_labels` = :math:`\{(a, a_r)\}` and
  `dereference_labels` = :math:`\{(d, d_r)\}`."
- Math blocks (lines 67, 70, 93, 94): `\textit{d_r}` -> `d_r`,
  `\textit{a_r}` -> `a_r` (plain subscripts, consistent with `V_1`..`V_3`).
- No other page changes: c_alias.rst is the only file with an underscore
  inside a text-mode command group.

### S3: Add the math-snippet guard

**Code:** new `utils/check_math_snippets.py`:
- `extract_math_snippets(rst_text) -> list[tuple[str, str]]` — returns
  (location, snippet) for every inline `:math:` role and `.. math::` block;
  skips code blocks.
- `find_broken_snippets(snippets) -> list[...]` — flags an unescaped `_`
  inside a text-mode command group (`\text`, `\textit`, `\textrm`,
  `\textbf`, `\mbox`); subscripts outside the group (`\textit{load}_f`) are
  valid and must not be flagged.
- `check_docs(docs_dir) -> list[...]` — walks `docs/**/*.rst`, applies both;
  CLI entry point printing violations (non-zero exit on any).

**Tests:** new `tests/utils/test_check_math_snippets.py`:
- Unit tests on synthetic RST covering: broken inline role, broken math
  block, valid subscript outside the group, escaped underscore inside the
  group, code blocks ignored, file without math.
- A test running `check_docs` over the real `docs/` tree (must pass after S2).

**Docs:** none in this subtask (developer-docs note + changelog in S4).

**Spec:**
- Extraction: inline roles via regex `` :math:`([^`]+)` ``; blocks by parsing
  `.. math::` directives with their indented body (option lines like
  `:label:` skipped). Must not treat `:math:` inside code blocks as math.
- Rule: for each text-mode command group in a snippet, the argument must not
  contain `_` unless escaped (`\_`). Brace-balanced scanning (groups can
  nest).
- Verify the guard fails on the pre-fix c_alias.rst content (run it against
  `git show dev:docs/grammars/data/c_alias.rst` before S2 is committed... i.e.
  against the pre-S2 blob) and passes after S2; record the outcome in the
  commit message.
- latex2mathml evaluation: trial it on every extracted snippet from the
  current corpus (install into the venv temporarily). Adopt as an additional
  check — adding it to the `test` dependency group — only if it (a) rejects
  `\textit{a_b}` and (b) accepts all current snippets with zero false
  positives. Strict-LaTeX semantics would flag all ~100 existing
  `\textit`-in-math usages (undefined in raw LaTeX) — in that case drop it
  and keep the targeted rule only. Record the outcome in a Design Notes
  section of this plan.
- Coverage: all branches of the new module must be covered (95/95 gate).

### S4: Changelog + developer docs

**Code:** none
**Tests:** none
**Docs:** `CHANGELOG.md` — `[Unreleased]`: new `### Fixed` subsection (C
Alias page math error, refs #127) + one `### Added` entry (math-snippet guard
in the test suite). `docs/developer.rst` Test pipeline section — a short note
that the suite also validates docs math snippets.

**Spec:**
- Keep a Changelog ordering: `Fixed` after `Removed`.
- The developer-docs note states what/why: browser-runtime MathJax errors are
  invisible to the Sphinx build; the guard catches them in CI as part of the
  standard suite (no new command).
