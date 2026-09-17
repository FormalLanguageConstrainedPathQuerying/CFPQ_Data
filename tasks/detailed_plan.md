# Task 39: Add the PEP 561 `py.typed` marker (issue #94)

Task (verbatim): Fix https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/issues/94

Branch: `feature/39-py-typed-marker` (from `dev`).

## Decision record

Decisions made before implementation:

1. **The issue is still open work, not stale.** Issue #94 asks for the PEP 561
   `py.typed` marker. Inline type annotations (added in task 37) are necessary
   but not sufficient: per PEP 561, a type checker (mypy, pyright) ignores the
   inline types of an *installed* package unless the package ships a
   `py.typed` marker file. Without it, downstream users get no type
   information from `cfpq_data` at all.
2. **The issue's `setup.py` snippet is obsolete.** Packaging migrated from
   Poetry + setuptools to PEP 621 + hatchling in task 37 (no `setup.py`
   exists). The fix is therefore: create the marker file and confirm the
   hatchling build ships it — no `package_data` configuration needed.
3. **Marker location**: `cfpq_data/py.typed`, empty file, tracked in git.
   This is the PEP 561 convention for inline-typed packages (no separate
   `.pyi` stubs).
4. **Packaging inclusion (to be verified empirically in S2)**: the hatchling
   wheel target `packages = ["cfpq_data"]` includes every VCS-tracked file
   under the package directory by default, so a git-tracked `py.typed` is
   expected to land in the wheel with no `pyproject.toml` change. The sdist
   target's `include = ["cfpq_data", ...]` covers it as well. S2 verifies
   both by building and inspecting the artifacts; if the wheel misses the
   marker, add an explicit hatchling `force-include`/`artifacts` entry.
5. **Regression guard**: a pytest test asserts the marker exists inside the
   installed package (`importlib.resources`), so deleting or untracking the
   file fails the suite. The built-wheel check is a one-off verification in
   S2 (the published artifact is what the issue is about); the test guards
   the source of truth.
6. **Docs**: one sentence in the "Quality checks" section of
   `docs/developer.rst` — the section that already documents ty/pyright —
   stating that the package ships `py.typed` per PEP 561 so downstream type
   checkers use the inline annotations. No new doc page (single source of
   truth, no duplication).
7. **Issue closing**: the task fully resolves #94, so the first subtask's
   commit carries `Closes #94` as a standalone body line (per the
   "Issue references" rules in `docs/developer.rst`). The issue closes when
   the release containing this task lands on `master`.

## Subtasks

### S1: Record task 39 in the task log and write the detailed plan [ ]

**Code:** N/A (documentation-only subtask)
**Tests:** Skip — no code to test
**Docs:** `tasks/tasks.md` (append the task line), `tasks/detailed_plan.md`
         (this plan)

**Spec:**
- Append `- [ ] Task 39: Fix https://github.com/.../issues/94` to
  `tasks/tasks.md`.
- Replace `tasks/detailed_plan.md` with this plan.
- Commit message body carries the standalone line `Closes #94`.

### S2: Add `cfpq_data/py.typed` and verify the built wheel ships it [ ]

**Code:** New empty file `cfpq_data/py.typed` (PEP 561 marker, git-tracked).
         No `pyproject.toml` change expected (decision 4); add a hatchling
         entry only if the empirical check fails.
**Tests:** New `tests/test_py_typed.py`: assert
         `importlib.resources.files("cfpq_data") / "py.typed"` exists —
         guards the marker against deletion/untracking in both editable and
         real installs.
**Docs:** N/A for this subtask (the developer-docs note is S3).

**Spec:**
- Create the empty `cfpq_data/py.typed` file.
- Add the regression test (style: plain pytest, no fixtures needed).
- Verify empirically: `uv build --wheel` and `uv build --sdist`, then inspect
  both artifacts (`unzip -l` / `tar -tzf`) and confirm `cfpq_data/py.typed`
  is present in each. Clean up `dist/` afterwards (build output, not source).
- Run the test suite for the new test.

### S3: Document the PEP 561 marker in the developer docs [ ]

**Code:** N/A (documentation-only subtask)
**Tests:** Skip — no code to test
**Docs:** `docs/developer.rst`, "Quality checks" section — one sentence after
         the ty/pyright paragraph: the package ships a PEP 561 `py.typed`
         marker, so type checkers in downstream projects use the inline
         annotations.

**Spec:**
- Add the sentence; keep it to the "what/why" (no build instructions — the
  packaging config in `pyproject.toml` is the source of truth for "how").
- Verify the docs build passes under the no-warnings policy.
