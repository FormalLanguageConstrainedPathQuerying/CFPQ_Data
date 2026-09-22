# Detailed Plan: Task 56 — Optimized grammars from arXiv:2401.11029 into the archives

## Context

arXiv:2401.11029 ("Optimization of the Context-Free Language Reachability
Matrix-Based Algorithm", Muravev 2024) presents five optimizations for the
matrix-based CFL-r algorithm. Optimization (5), in Appendix B, gives two
equivalent hand-crafted WCNF grammars that outperform the automatically
normalized ones. Both originals are "taken from CFPQ Data":

| Class | Original in our archives | Optimized (paper) |
|---|---|---|
| Field-sensitive Java points-to (FSJPT) | Fig 1(a) = `java_points_to.cnf` | **Fig 1(b)** |
| Field-insensitive C/C++ alias (FICA) | Fig 2(a) = `c_alias.cnf` | **Fig 2(b)** |

(Figs 3–4 are from POCR/Lei et al., not ours, and are untouched by
optimization 5.) The task: extract the two optimized grammars, add them to
the respective archives (all 21 `java_points_to` + all 20
`c_alias_analysis` graph archives on S3), and verify with `temporal_cfpq`
(FastMatrixCFPQ Docker oracle) that original and optimized return equal
reachable-pair counts on several small graphs.

Language equivalence (checked by hand before implementation):

- FSJPT: Fig 1(b)'s `PT -> LPFS_i PT` with `LPFS_i = load_i PT FT store_i`
  reproduces Fig 1(a)'s `PTH -> load_i Al store_i PTH` (`Al = PT FT`); the
  non-ε trailing `PT` in 1(b) absorbs the terminating `alloc` of 1(a)'s
  `PTH -> ε` case, and symmetrically for `FT`/`SPFL_i` vs `FTH`. Same
  language.
- FICA: Fig 2(a)'s `V = ((ε|M) a_r)* (ε|M) (a (ε|M))*` equals Fig 2(b)'s
  `d_r (a_r | M a_r)* (ε|M) (a | aM)* d` since `(ε|M) a_r = a_r | M a_r` and
  `a (ε|M) = a | aM`. Same language.

## User decisions (recorded verbatim in tasks.md)

1. **Keep old structure** — the live archives are in the legacy layout
   (`README.md`, `grammar/`, `graph/`); the upload CLI gate added by task 52
   enforces the new `queries/` layout and would refuse them. Re-upload the 41
   archives as-is with the new grammar file added, via the `upload_file()`
   API of `utils/upload_to_s3.py` (the gate stays intact for new data). The
   dataset-wide migration to the new layout remains global-plan task 48.
2. **Cite the paper in the name** — the files are
   `java_points_to_muravev2024.cnf` and `c_alias_muravev2024.cnf`.

## The two optimized grammars (POCR `.cnf`, our label conventions)

`java_points_to_muravev2024.cnf` (Fig 1(b); indexed nonterminals share the
field index; start `PT`):

```
PT	alloc
PT	assign	PT
PT	LPFS_i	PT
FT	alloc_r
FT	FT	assign_r
FT	FT	SPFL_i
LPFS_i	LP_i	FS_i
LP_i	load_i	PT
FS_i	FT	store_i
SPFL_i	SP_i	FL_i
SP_i	store_r_i	PT
FL_i	FT	load_r_i

Count:
PT
```

`c_alias_muravev2024.cnf` (Fig 2(b); start `M`):

```
M	N1	N3
M	N2	N3
N1	d_r
N1	N1	a_r
N1	N2	a_r
N2	N1	M
N3	d
N3	a	N3
N3	AM	N3
AM	a	M

Count:
M
```

Both are CNF (≤2 RHS symbols), have no ε-productions, use only the stored
labels of their category (`alloc`, `assign`, `load_i`, `store_i` + reverses;
`a`, `d` + reverses), and the start symbol is not indexed.

## Affected archives

- `java_points_to` (21): gson, sunflow, lusearch, luindex, avrora, mockito,
  commons_io, commons_lang3, eclipse, h2, pmd, xalan, junit5, batik, fop,
  tomcat, guava, jackson, jython, tradebeans, tradesoap.
- `c_alias_analysis` (20): wc, bzip, pr, ls, gzip, apache, init, mm, ipc,
  lib, block, arch, crypto, security, sound, net, fs, drivers, postgre,
  kernel.

## Subtasks

### S1: Record the task and write the detailed plan [done]

**Code:** none (documentation-only subtask).
**Tests:** skipped — no code.
**Docs:** `tasks/tasks.md` (task 56 entry with verbatim user guidance),
`tasks/detailed_plan.md` (this file).

**Spec:**
- Task line recorded verbatim in `tasks/tasks.md` with the two user
  decisions as `[USER GUIDANCE]`.
- This plan written before any implementation.

### S2: Extract and document the two optimized grammars [ ]

**Code:** none in the package. Working `.cnf` files written to
`temporal_cfpq/grammars/` (gitignored local reference copies, alongside the
existing `fsjpt.cnf`/`cscvf.cnf`/`fsca.cnf`):
`java_points_to_muravev2024.cnf`, `c_alias_muravev2024.cnf`.
**Tests:** local validation (no CI code to test): parse both files with the
package's `cnf_template_from_cnf` and with pyformlang `CFG.from_text`; assert
CNF (≤2 RHS), start symbol present and not indexed, terminal set exactly
`{alloc, assign, alloc_r, assign_r, load_i, store_i, load_r_i, store_r_i}`
(FSJPT) / `{a, d, a_r, d_r}` (FICA); assert the terminal set equals that of
the in-archive original grammar (so one `.g` edge list serves both).
**Docs:** `docs/graphs/java_points_to.rst` and
`docs/graphs/c_alias_analysis.rst` — an "Optimized variant" subsection in the
"Canonical grammars" section: the exact `.cnf` content as stored in the
archives (code block, the single source of truth for the productions), the
file name, a citation to arXiv:2401.11029 (Fig 1(b) / Fig 2(b)), and a note
that it generates the same language (verified in S3).

**Spec:**
- Transcribe Fig 1(b) / Fig 2(b) exactly, mapping the paper's barred symbols
  to our `_r` convention (`store_ī` -> `store_r_i`, `d̄` -> `d_r`, ...).
- Tab-separated POCR CNF; last two lines `Count:` + start symbol.
- The docs subsection shows the productions once (no duplication between the
  code block and any math rendering).

### S3: Verify equivalence with temporal_cfpq on small graphs [ ]

**Code:** new local tool `temporal_cfpq/verify_optimized.py` (gitignored,
reuses `run_reference.py`'s `stream_g_file`, `run_solver`,
`grammar_terminals`, `start_symbol`): for each graph, download it, stream one
`.g` edge list (terminal sets of original and optimized are identical), run
the FastMatrixCFPQ solver on the in-archive original `.cnf` and on the
optimized `.cnf`, compare the reachable-pair counts. Results appended to
`temporal_cfpq/results/optimized_grammars_check.csv`.
**Tests:** the check itself is the test: 10 graphs × 2 grammars, all counts
must be equal (original vs optimized) and must match the recorded reference
values in `results/reference_answers.csv`.
**Docs:** record the results table (graph, original count, optimized count,
match) in this file under "Verification results" — the tracked trace of the
check.

**Spec:**
- Graphs: c_alias -> `wc`, `bzip`, `pr`, `ls`, `gzip`; java_points_to ->
  `gson`, `sunflow`, `lusearch`, `luindex`, `avrora` (all previously `ok` in
  the full sweep; seconds to ~25 s per run).
- Run under Docker access (`sg docker -c ...`), container memory cap as in
  `run_reference.py`.
- Any mismatch or solver failure blocks S4 — nothing is uploaded before a
  clean PASS.

### S4: Repack and re-upload the 41 archives [ ]

**Code:** one-off repack script (ad-hoc, task-19 pattern; not committed) +
committed record `utils/optimized_grammars_record.json`.
**Tests:** per archive: the repacked tarball contains exactly the original
members plus the one new `.cnf`; the stored object size after upload equals
the local file size (verified by `upload_file`); a spot-check download of two
archives (one per category) lists the new file.
**Docs:** the JSON record (per archive: name, S3 key, sha256 before/after,
added file, date) following the `filename_unification_record.json` pattern;
`Size (MB)` columns re-synced with `utils/archive_sizes.py --update` (the
archives grow by a few hundred bytes).

**Spec:**
- For each of the 41 graphs: download `5.0.0/graph/<name>.tar.gz`, unpack,
  add `grammar/<x>_muravev2024.cnf` (identical file within a category),
  repack as `<name>.tar.gz` with the same top-level directory name, upload
  via `upload_file()` from `utils/upload_to_s3.py` (credentials from the CLI;
  the CLI structure gate is bypassed deliberately — legacy layout kept per
  the user decision).
- One graph at a time; scratch removed after each.
- The record JSON is committed; the upload itself is a data operation on S3.

### S5: Changelog and task close-out [ ]

**Code:** none (documentation-only subtask).
**Tests:** skipped — no code.
**Docs:** `CHANGELOG.md` ([Unreleased] → Added: optimized grammar variants
for the two categories, verified equivalent); `tasks/tasks.md` (mark task 56
`[done]`).

**Spec:**
- Changelog entry names the paper and both file names.
- Task marked done only after the quality gate passes.

## Verification results

(Filled in by S3.)
