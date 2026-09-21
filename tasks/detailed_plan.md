# Detailed Plan: Task 52 — Self-contained archive structure + validation

Task (user's words, recorded in `tasks/tasks.md`): "Second, let carefully
design archive structure and tool to check this structure. All archives must
have sidentical structure and be self-contained. Each archive: graph as a set
of MTX, description document (let design madatory cestions), all grammars
(qeryes) in separated files with descriptions (in common document). Structure
validation step must be added to upload workflow. Rework FLPQ design document
with respect to this."

User guidance (recorded verbatim): "Do not forget to reflrct structure of
archive in documnet and templates for PR and issue."

Scope decisions (confirmed with the user during planning):
- Graph archives only — benchmark data is out of scope (task 53).
- Example/template queries not tied to a graph are dropped: every query file
  lives inside a graph archive.
- Validation lives in the upload tool: `utils/upload_to_s3.py` validates
  before uploading, plus an audit mode over the bucket.

Verified facts this plan builds on (checked against the repo, 2026-09-21):
- Current layout (`docs/graphs/index.rst` "File structure", the source of
  truth): `<name>.tar.gz` unpacks to `<name>/{README.md, grammar/, graph/}`;
  `graph/` holds one Boolean MatrixMarket pattern file per stored edge label.
- Grammars use reversed labels (`d_r`, `a_r`, `subClassOf_r` in the
  canonical grammars of `docs/graphs/c_alias_analysis.rst` and
  `docs/graphs/rdf.rst`); reversed edges are derived, not stored.
- Query formats and readers already exist: `.cnf` via
  `cnf_from_text` (pyformlang CFG; terminals via `cfg.terminals`), regex text
  via `regex_from_text` (pyformlang `Regex`; symbols via
  `to_epsilon_nfa().symbols`, multi-character tokens stay single symbols —
  matching dataset labels like `subClassOf`), `.mcfg` via `mcfg_from_text`
  (task 44; terminals are the non-`eps`, non-variable items of
  `MCFGRule.head_args`). No RPQ file extension exists yet — this plan
  introduces `.re`.
- `graph_from_mtx_dir` raises `ValueError` on a bad header or an nnz/count
  mismatch — reusable for MTX validation.
- `utils/` scripts import `cfpq_data` (pattern of `audit_archive_names.py`,
  `convert_old_to_new.py`); `tests/utils/test_upload_to_s3.py` mocks the S3
  client with `mock.Mock()` and `monkeypatch` — the pattern for the audit
  tests.
- The required fields/metadata live in the GitHub templates (add-graph skill
  convention): `.github/PULL_REQUEST_TEMPLATE/new_graph.md` and
  `.github/ISSUE_TEMPLATE/graph-add-template.md` share one body (Info, Data
  format, Graph Statistics, Edges Statistics, Canonical grammars); both
  restate the old layout inline.
- `utils/upload_to_s3.py` uploads arbitrary files; today nothing validates
  archive content before upload.

Design (the new identical, self-contained graph-archive structure):

    <name>.tar.gz unpacks to <name>/
    ├── README.md              description document — answers the mandatory
    │                          questions of the contribution templates
    ├── graph/                 one Boolean MatrixMarket pattern file per
    │   └── <label>.mtx        stored edge label (non-empty)
    └── queries/               all queries for this graph, one file each
        ├── README.md          common document describing every query file
        ├── cfpq/              .cnf files (pyformlang CFG format)
        ├── rpq/               .re files (regular expression text)
        └── mcfpq/             .mcfg files (Datalog-like MCFG syntax)

- Fixed skeleton: the three class directories and `queries/README.md` are
  always present (possibly empty); nothing else may appear at any level.
- Mandatory questions of `README.md` (markdown `##` headers, enforced by the
  validator; the templates are the source of truth for the fields):
  "What is this graph?", "Source", "Construction", "Nodes", "Edges and
  labels", "Query classes", "License", "Caveats".
- `queries/README.md`: one `## <class>/<file>` section per query file (path
  relative to `queries/`), each with a non-empty description; the templates
  show the recommended Language/Purpose/Source bullets.
- Label consistency: every terminal used by any query file must be a stored
  label (`graph/<t>.mtx`) or the reverse of one (`<L>_r` with
  `graph/<L>.mtx`).

### S1: Record the guidance and write this plan

**Code:** none.
**Tests:** n/a.
**Docs:** `tasks/tasks.md` (guidance appended — already in the working
tree), `tasks/detailed_plan.md` (this plan).

**Spec:**
- Commit the task-log change together with this plan.

### S2: Design the layout in the docs

**Code:** none.
**Tests:** docs build exits 0 (no-warnings policy).
**Docs:** `docs/graphs/index.rst` "File structure" — replace the old layout
(`README.md, grammar/, graph/`) with the new one above; document the query
file conventions (one file per query, the per-class extensions `.cnf`/`.re`/
`.mcfg`, the fixed skeleton) and the `queries/README.md` common-document
format; point at the contribution templates for the mandatory README
questions (the templates stay the source of truth for the fields, as with
the statistics conventions).

**Spec:**
- The "Indexed labels" and "Reversed edges" subsections stay unchanged.
- No mandatory-question text is duplicated into the docs — only a pointer to
  the templates.

### S3: Update the PR and issue templates

**Code:** none.
**Tests:** n/a (templates); pre-commit passes.
**Docs:** `.github/PULL_REQUEST_TEMPLATE/new_graph.md` and
`.github/ISSUE_TEMPLATE/graph-add-template.md` — "Data format" restates the
new layout; a new "Description document" section lists the eight mandatory
questions (the fields that become the archive `README.md`); "Canonical
grammars" becomes "Queries": the three cases stay, and for new grammars the
contributor provides the file-format text (`.cnf`/`.re`/`.mcfg`) that lands
in `queries/<class>/` of the archive.

**Spec:**
- Both templates keep the same body (they are kept in sync today).
- Every mandatory question appears exactly once per template, in
  `<triangle brackets>` form like the existing fields.

### S4: The structure-validation tool (local mode)

**Code:** new `utils/check_archive_structure.py` (pattern of
`utils/archive_sizes.py`: module docstring with Usage, `__all__`,
`main(argv) -> int`): validates a local `.tar.gz` or an unpacked directory —
skeleton (single top-level dir named after the archive; exactly
`README.md`/`graph/`/`queries/`; `graph/` non-empty with only `*.mtx`;
`queries/` exactly `README.md` + the three class dirs with only the matching
extensions), MTX validity via `graph_from_mtx_dir`, query validity via
`cnf_from_text`/`regex_from_text`/`mcfg_from_text`, label consistency
(stored or reversed), the eight mandatory README headers, and
`queries/README.md` completeness (every file has a section, no orphan
sections). Collects ALL problems and prints them; exit 1 if any.
**Tests:** new `tests/utils/test_check_archive_structure.py` building
synthetic archives in `tmp_path`: a fully valid archive passes; each
violation class is detected (extra top-level entry, missing class dir,
non-mtx file in graph/, malformed MTX, unparseable query, unknown label,
missing mandatory header, orphan/missing queries/README.md section).
**Docs:** `docs/utils.rst` — register the tool like the other `utils/`
scripts (check how `archive_sizes.py` is documented and follow it).

**Spec:**
- The validator imports the existing readers (no re-parsing logic of its
  own); terminal extraction: `cfg.terminals`,
  `Regex(...).to_epsilon_nfa().symbols`, and the non-`eps`/non-variable
  items of `MCFGRule.head_args`.
- A reversed label `<L>_r` is consistent iff `graph/<L>.mtx` exists.

### S5: Audit mode + pre-upload validation

**Code:** `utils/check_archive_structure.py` — `--audit --prefix P` mode:
list the `.tar.gz` objects under the bucket prefix, download each to a temp
dir, validate, report per archive (reuses `upload_to_s3.create_s3_client`,
credentials from CLI like the upload tool). `utils/upload_to_s3.py` — before
uploading any `.tar.gz`, run the structure check on the local file; refuse
the upload and print the problems otherwise.
**Tests:** extend `tests/utils/test_check_coverage.py`-style coverage: new
tests in `tests/utils/test_check_archive_structure.py` for the audit mode
(mocked S3 client listing/downloading a valid and an invalid archive) and in
`tests/utils/test_upload_to_s3.py` for the pre-upload gate (valid tarball
uploads, invalid tarball is refused without any S3 call).
**Docs:** `docs/utils.rst` — the audit mode and the pre-upload behavior.

**Spec:**
- The upload tool validates every `.tar.gz` upload: graph archives are the
  only structured archive kind today (benchmarks are out of scope until
  task 53).
- Audit mode prints one line per archive plus a summary; exit 1 if any
  archive is invalid.

### S6: Rework flpq.rst and the add-graph skill

**Code:** none.
**Tests:** docs build exits 0.
**Docs:** `docs/flpq.rst` — "Dataset layout and migration": the separate
`query/<class>/` prefix disappears; `6.0.0/graph/<name>.tar.gz` is the
self-contained archive (layout documented once in `docs/graphs/index.rst`,
referenced, not duplicated); the migration repackages every graph archive
into the new structure (per-graph grammars move from the legacy grammar
archives into `queries/`, example archives are dropped, READMEs are filled
to the mandatory questions) instead of copying them unchanged; "API
changes": `download(name)` returns the directory with graph AND queries,
`download_grammars` is deprecated (queries come with the graph).
`.opencode/skills/add-graph/SKILL.md` — the "Data format" paragraph's inline
old layout is replaced by a pointer to the updated "File structure" section;
the wiring notes that mention `grammar/` are updated to `queries/`.

**Spec:**
- `flpq.rst` keeps the dataset-level design (prefixes, migration path, API)
  and points at `docs/graphs/index.rst` for the per-archive layout — no
  duplication of the layout.
- The benchmark prefix line stays, marked as reworked in task 53.
