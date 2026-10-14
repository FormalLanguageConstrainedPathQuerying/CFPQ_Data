# Detailed Plan: Task 165 — Package the archive checker as `flpq-check-archive`

Issue #165. Move the archive structure checker from `utils/` into the
`flpq_data` package and expose it as a console entry point, so external
contributors validate archives with `pip install flpq-data` alone — no
manual script download.

## Confirmed decisions (user guidance, verbatim on the issue)

- Scope: **checker only**. The other utils are repo-bound maintainer tools
  (S3 credentials, in-repo CSV/docs paths) that would fail outside a
  checkout.
- Entry point name: **`flpq-check-archive`** (e.g.
  `flpq-check-archive my_graph.tar.gz --partial`).

## Design notes

- The checker imports only from `flpq_data.*` + `pyformlang` — no
  repo-bound paths — so it moves cleanly into the package.
- boto3 is a dev-only dependency; the `--audit` subcommand (S3 audit) is
  maintainer-side. `create_s3_client` + `DEFAULT_BUCKET` /
  `DEFAULT_ENDPOINT_URL` move to `flpq_data/dataset/s3.py` with boto3
  imported lazily inside the function, so the package imports without
  boto3; `--audit` reports a clean "boto3 required" error when it is
  missing.
- The wheel build (`packages = ["flpq_data"]`) picks up the new submodule
  automatically; `[project.scripts]` registers the entry point; uv installs
  the project itself, so the command works in-repo too.
- Coverage: the moved lines now count toward the 95% flpq_data gate; the
  existing tests cover the module (incl. mock-tested `_audit`); one new
  branch (missing boto3) gets a test.

---

### S1: Move the checker into the package + console entry point

One atomic increment — moving the module without its tests would break the
suite, so code and tests move together.

**Code:**
- `git mv utils/check_archive_structure.py` →
  `flpq_data/tools/check_archive_structure.py`; update the module docstring
  Usage block to `flpq-check-archive ...`.
- New `flpq_data/tools/__init__.py` — star import of the checker module,
  following the `flpq_data/dataset/__init__.py` pattern.
- New `flpq_data/dataset/s3.py`: `DEFAULT_ENDPOINT_URL`, `DEFAULT_BUCKET`,
  `create_s3_client` (moved from `utils/upload_to_s3.py`; boto3 imported
  lazily inside the function body; numpydoc docstring with doctest-safe
  examples). Star-imported from `flpq_data/dataset/__init__.py`.
- `pyproject.toml`: `[project.scripts]` with
  `flpq-check-archive = "flpq_data.tools.check_archive_structure:main"`.
- Checker's `--audit` branch: import the S3 helpers from
  `flpq_data.dataset.s3`; wrap client creation so a missing boto3 prints
  `error: --audit requires boto3 (pip install boto3)` and returns 1.
- Utils importers updated to the package path: `merge_archive.py`,
  `add_reachable_pairs.py`, `reachable_pairs_tables.py`,
  `strip_reverse_edges.py`, `generate_registry.py`; `upload_to_s3.py` drops
  its own constant/client definitions (imports them from the package; its
  `__all__` keeps re-exporting them so existing imports keep working) and
  its lazy `validate_archive` import points at the package module.

**Tests:**
- Move `tests/utils/test_check_archive_structure.py` →
  `tests/tools/test_check_archive_structure.py`; imports from
  `flpq_data.tools.check_archive_structure`.
- Extract the shared tree builders (`README`, `RESULTS`, `_query_dir`,
  `_valid_tree`, `_partial_tree`, `_tarball`) into `tests/archive_helpers.py`;
  new root `tests/conftest.py` inserting `tests/` on `sys.path` (the four
  utils test files — `test_merge_archive`, `test_add_reachable_pairs`,
  `test_strip_reverse_edges`, `test_upload_to_s3` — import those helpers;
  their import lines point at `archive_helpers`).
- New tests: the missing-boto3 `--audit` branch (mocked import failure);
  the declared console entry point via `importlib.metadata` (name
  `flpq-check-archive`, value `flpq_data.tools.check_archive_structure:main`).

**Docs:** none in this subtask beyond the moved module's docstring (the
docs sweep is S2).

**Spec:**
- The public API and behavior are unchanged — this is a move, not a rewrite;
  `validate_archive`, `unpack_single_dir`, `stored_reverse_forward`,
  `parse_readme_sections`, `QUERY_CLASSES`, `MANDATORY_README_SECTIONS` keep
  their signatures.
- `flpq_data/dataset/s3.py` must import cleanly without boto3 installed
  (lazy import inside `create_s3_client` only).
- After the move, no file outside `tests/` may import the bare
  `check_archive_structure` module name; all in-repo consumers use
  `flpq_data.tools.check_archive_structure`.
- Verify: full suite + coverage gate green (canonical command from
  `docs/developer.rst`).

### S2: Docs and flow sweep

**Code:** none (docs/templates/skills only).

**Tests:** fresh docs build under the no-warnings policy.

**Docs:**
- New reference page `docs/reference/tools/index.rst` following the
  `docs/reference/dataset/index.rst` pattern (`.. automodule::` +
  autosummary of the checker's public API, `generated/` toctree); it carries
  the existing `.. _archive_structure:` anchor (so `:ref:`archive_structure`
  from `docs/flpq.rst` and `docs/utils.rst` keeps resolving); add
  `tools/index` to the `docs/reference/index.rst` toctree.
- Remove the "Archive structure checker" section from `docs/utils.rst` (the
  tool is no longer a repo util).
- `docs/flpq.rst`: update the checker path mention in the migration-path
  note.
- `.github/ISSUE_TEMPLATE/new-data-template.md` "Validation" section: the
  recipe becomes `pip install flpq-data` +
  `flpq-check-archive <name>.tar.gz [--partial]` — no raw-URL script
  download.
- `docs/graphs/index.rst`: "Contributing data" → Validation subsection and
  the "File structure" partial-validation command mention use the console
  command.
- `.opencode/skills/add-graph/SKILL.md`: the two checker invocations use the
  console command.
- `AGENTS.md`: the checker path in the data-archives principle line and a
  `flpq_data/tools/` line in the package layout.
- `CHANGELOG.md` Unreleased: Added — `flpq-check-archive` console command,
  validation with `pip install flpq-data` alone; Changed — checker moved
  from `utils/` to `flpq_data/tools/`, S3 client helpers moved to
  `flpq_data.dataset.s3`.

**Spec:**
- Every remaining mention of `utils/check_archive_structure.py` in
  docs/templates/skills/AGENTS.md is updated (the historical CHANGELOG entry
  stays as-is).
- The contributor flow documented end-to-end: `pip install flpq-data`, then
  `flpq-check-archive <name>.tar.gz [--partial]`.

---

## Execution order

S1 → S2. One commit per subtask (`feat(165-SN)` / `docs(165-SN)`), code
review + quality gate before merge to `dev`; the last subtask's commit
carries `Closes #165`. Final verification includes a one-off `uv build`
wheel inspection (module present, entry point registered).
