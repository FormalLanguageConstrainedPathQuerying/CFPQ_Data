# Detailed Plan: Task 55 — Data providing mechanism (Google Drive link + partial archives)

## Context

Task 54 extended the archive structure: a query is a directory
`queries/<class>/<query>/` holding its representations plus one
`results.mtx`. Task 55 reworks how new data is provided to the project: a
Google Drive link to an archive prepared per the structure-validation tool
becomes the main way; partial archives (a new query for an existing graph)
are allowed, with the structure preserved so the new data merges into the
existing archive; the issue/PR templates make this way the main one and
point at the tooling.

Existing pieces to build on:

- `utils/check_archive_structure.py` — the structure validator (full mode,
  task 54 layout).
- `utils/upload_to_s3.py` — validates before uploading; `--audit` over the
  bucket.
- `utils/migrate_gdrive_to_s3.py` — `download_from_drive(file_id, dest)`
  handles Drive's large-file confirmation form; `DRIVE_FILE_ID_RE` extracts
  a file ID from a Drive URL.

## User decisions (recorded verbatim in tasks.md)

1. A partial archive contains **queries/ + a README fragment**:
   `<graph>/queries/<class>/<query>/{representations, results.mtx}` plus a
   `queries/README.md` holding only the new `## <class>/<query>` sections —
   everything needed for the merge lives in the archive.
2. **Build `utils/merge_archive.py`** — merges a partial archive into an
   existing one: collision checks, README section append, full re-validation
   of the result.

## Design

### Partial archive format

```
<graph_name>/
└── queries/
    ├── README.md          fragment: the new "## <class>/<query>" sections only
    └── <class>/
        └── <query>/
            ├── <rep>.*    ≥ 1 representation file (.cnf/.rsm, .re/.rsm, .mcfg)
            └── results.mtx
```

- The top-level directory is named after the graph (same rule as full
  archives).
- No `graph/`, no top-level `README.md`.
- The reachable-pair count is derivable: the number of entries in
  `results.mtx` — no separate reference file.

### Validator extension (`check_archive_structure.py --partial`)

- Explicit `--partial` flag; `validate_archive(path, partial=False)`.
- Partial skeleton: a single top-level directory named after the archive,
  containing only `queries/`; `queries/` carries its `README.md` and at
  least one known class directory; each class directory holds query
  directories validated by the existing `_query_dir_problems`.
- Representation files must parse (no label check — there is no graph to
  check against; no `results.mtx` dimension check either).
- The README fragment: every section is non-empty and matches a
  `<class>/<query>` directory present in the partial archive.
- Full mode is unchanged; a missing `graph/` without `--partial` stays an
  error.

### Merge tool (`utils/merge_archive.py`)

```
python utils/merge_archive.py EXISTING.tar.gz PARTIAL.tar.gz -o MERGED.tar.gz
```

- `PARTIAL` may be a local `.tar.gz`, an unpacked directory, or a Google
  Drive URL / file ID (downloaded via `download_from_drive`).
- Validates the existing archive in full mode and the partial one in partial
  mode; both top-level directories must have the same name (same graph).
- Copies the partial's query directories into the existing tree; a
  `<class>/<query>` that already exists is a collision error (all collisions
  reported at once).
- README merge: every section of the partial fragment must correspond to a
  merged-in query directory; sections are appended to the existing
  `queries/README.md`; a section name that already exists is an error.
- Re-validates the merged tree in full mode; on any problem it reports them
  and exits non-zero without writing the output.
- Writes `MERGED.tar.gz` with the graph-named top-level directory.

### Templates (issue + PR, kept in sync)

- **Info table.** "Origin" becomes "Archive": a Google Drive link to
  `<name>.tar.gz`; a new "Target graph" field for partial archives (the
  existing graph the queries are added to).
- **Data format.** Explains full vs partial archives and points at the
  "File structure" section of the Graphs page, the validator (incl.
  `--partial`), and the RSM format in the FLPQ design page.
- **Description document.** Full archive: the eight mandatory questions.
  Partial archive: the `queries/README.md` fragment — one
  `## <class>/<query>` section per new query.
- **Queries.** Updated to the task-54 layout (one directory per query with
  its representations and `results.mtx`); the three canonical-grammar cases
  stay.

### Docs

- `docs/utils.rst`: the "Archive structure" section documents `--partial`;
  a new "Merge partial archives" section documents `merge_archive.py`.
- `.opencode/skills/add-graph/SKILL.md`: pointer update if it states
  providing-workflow details.

## Subtasks

- [x] **S1**: Record the user decisions verbatim in `tasks/tasks.md`; write
      this detailed plan. Commit `docs(55-S1)`.
- [ ] **S2**: Validator `--partial` mode — partial skeleton, parse-only
      representation checks, README-fragment check; tests with fixture
      archives (valid + each failure mode). Commit `feat(55-S2)`.
- [ ] **S3**: `utils/merge_archive.py` — merge, collisions, README append,
      full re-validation, Drive input; tests. Commit `feat(55-S3)`.
- [ ] **S4**: Templates (issue + PR) rework + `docs/utils.rst` sections +
      skill pointer if needed. Commit `docs(55-S4)`.
- [ ] **S5**: Quality gate, code review, mark done in the task log, merge to
      dev.

## Out of scope

- Uploading or migrating any data (the migration of existing archives is
  task 48).
- `reachable_pairs.csv` redesign for per-query rows (task 48).
- New-graph partials (a new graph always ships a full archive) and
  edge/label additions to an existing graph.
