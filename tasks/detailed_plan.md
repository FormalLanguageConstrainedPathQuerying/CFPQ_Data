# Detailed Plan: Task 130 — Reference results for the big graphs (fill the 60 stubs)

Issue #130. The 6.0.0 dataset has 60 graph/grammar pairs whose reference
reachable-pair counts are "not available" in
`flpq_data/dataset/reachable_pairs.csv` and whose in-archive `results.mtx` is
a dimensioned empty stub (v6 migration: reference run >= 30 s or oom/timeout;
list in `temporal_cfpq/results/v6_drift_report.md`). This task computes the
reference results for all 60 pairs with the FastMatrixCFPQ oracle on the
remote machine (`user4ferrum@172.22.241.114`, 24 cores / 124 GB RAM, Docker
28.1.1), using language-equivalent low-memory grammars where they exist
(`c_alias_muravev2024.cnf` / `java_points_to_muravev2024.cnf` — arXiv:2401.11029
optimization 5, shipped in the archives; the muravev-style sparse uniprot
grammar of task 157 for unigraph_8/9/10), fills the stub `results.mtx`,
repacks and re-uploads the affected archives to S3, and syncs
`reachable_pairs.csv`, the docs tables, and `registry.json`.

## Context

**The 60 pairs and the grammar each run uses.** Counts are recorded under the
canonical grammar name (the one `reachable_pairs.csv` tracks); the *run*
grammar is a language-equivalent variant where one exists (verified in task 56
for the muravev2024 pair, task 157 for the sparse uniprot grammar):

| Category | Graphs (count) | Run grammar | Reference for verification |
|---|---|---|---|
| c_alias_analysis | apache, arch, block, crypto, drivers, fs, init, ipc, kernel, lib, mm, net, postgre, security, sound (15) | `c_alias_muravev2024.cnf` (in-archive) | `reference_answers.csv` (all 15) |
| java_points_to | batik, eclipse, fop, h2, jackson, junit5, tomcat, tradebeans, tradesoap, xalan, guava, jython (12) | `java_points_to_muravev2024.cnf` (in-archive) | reference csv (9); external values in `temporal_cfpq/README.md`: guava 26384496, jackson 3108775, jython 561720 |
| uniprot | unigraph_2..unigraph_10 (9) | `unigraph_1_sparse.cnf` (task 157; same terminal set as the in-archive `unigraph_N.cnf`) | reference csv (unigraph_2..7); none for 8/9/10 |
| RDF | enzyme/broaderTransitive, geospecies x3, taxonomy x3, taxonomy_hierarchy x3 (10) | original in-archive `.cnf` | reference csv (all 10) |
| field-sensitive alias | cactus_fsa, imagick_fsa, omnetpp_fsa, parest_fsa, perlbench_fsa, povray_fsa with `vf.cnf` (6) | original in-archive `vf.cnf` | reference csv under the swapped 5.0.0 name `aa.cnf` (see below) |
| context-sensitive data-flow | cactus, omnetpp, perlbench, povray with `aa.cnf` (4) | original in-archive `aa.cnf` | reference csv under the swapped 5.0.0 name `vf.cnf` |
| name resolution | jiaozi, libgdx, shattered_pixel_dungeon (3) | original in-archive `name_resolution.cnf` | reference csv (jiaozi 14435, spd 971998); none for libgdx |
| data provenance | httpx with `prov_derivation.cnf` (1) | original in-archive `.cnf` | reference csv (4408) |

The ten vf/aa rows of `reference_answers.csv` carry the 5.0.0 file names that
were swapped by name (v6 drift report): e.g. reference row
`cactus,vf.cnf = 47806209` verifies v6 pair `cactus,aa.cnf`, and
`cactus_field_sensitive_alias,aa.cnf = 37625324` verifies
`cactus_field_sensitive_alias,vf.cnf`. The verification step must apply this
name mapping.

**Hardware limits (decided with the user).** FastMatrixCFPQ materializes dense
n×n Boolean matrices (~n²/8 bytes each):

- unigraph_10 (2,055,621 nodes): ~527 GB for ONE dense matrix — infeasible on
  the 124 GB machine; its `results.mtx` would also likely exceed the 228G free
  lab disk. **Decision: attempt all; if infeasible, document the limitation in
  the task record, leave the cell "not available", and report to the user at
  the end.**
- unigraph_9 (475,450 nodes): ~28 GB per dense matrix — the original grammar
  OOMed >100 GiB; the sparse grammar (fewer dense intermediates) may fit under
  a raised container cap (~115 GiB). Same decision as above if it OOMs.
- libgdx (2,274,310 nodes, name_resolution): OOMed >100 GiB in the reference
  run and has NO optimized grammar variant — attempt with the raised cap; same
  decision if it OOMs.

**Remote environment state (checked 2026-10-08).** `/mnt/jblab2-disk/gsv_cfpq/`
holds `repo/` (a stale 5.0.0-era copy: package still named `cfpq_data`, old
`temporal_cfpq/`), `venv/` (Python 3.12.3), `fast_matrix_cfpq.tar.gz` (image,
already loaded into Docker), and the previous retry scripts/logs. The repo copy
must be updated to the current `flpq_data` tree before running (user guidance:
"Use it. Update if necessary.").

**Archive update flow.** Each affected archive gets its stub
`queries/cfpq/<query>/results.mtx` replaced by the filled matrix (same two-line
header + dimension line, `nnz` = pair count, entries `tail head`), is re-tarred
as `<graph>.tar.gz` (single top-level dir named after the graph), validated with
`utils/check_archive_structure.py`, uploaded to `6.0.0/graph/` on S3, and then
`registry.json` is regenerated from S3 (`utils/generate_registry.py`) so the
sha256/size columns follow. The updated `reachable_pairs.csv` is also uploaded
to `6.0.0/reachable_pairs.csv`.

## Decisions (confirmed with the user)

1. Scope: **all 60 pairs** (every "not available" cell).
2. Archive updates: **prepare + upload to S3** — repack the affected archives,
   re-upload them and `reachable_pairs.csv` under the 6.0.0 prefix, sync the
   repo data (CSV, docs tables, registry).
3. Grammar selection per the table above (muravev2024 where it exists — "It is
   faster and requies less memory" — sparse uniprot grammar for unigraph_8/9/10,
   original otherwise); counts recorded under the canonical grammar name.
4. unigraph_10 (and unigraph_9 / libgdx if they OOM): attempt, then document
   the hardware limitation and leave the cell "not available"; report to the
   user at the end.
5. S3 credentials: the user pastes the Yandex Cloud IAM key ID + secret in chat
   when the upload subtask starts; used only for the CLI command, never written
   to files.
6. Reference freshness (2026-10-08): the user confirmed that the old
   `reference_answers.csv` counters for 8 java_points_to pairs are stale
   ("Reference counters were updated some tmes ago") and that the fresh
   computed values are correct ("All these 8 fresh results correct."). The
   fresh values are authoritative: batik 45968, eclipse 21830, fop 76615,
   h2 92038, tomcat 82424, tradebeans 696316, tradesoap 698567, xalan 52382.
   S4 verification for these 8 is user confirmation, not a reference match.

## Subtasks

### S1: temporal_cfpq tooling for results.mtx generation [local, gitignored] [done]

**Code:** New `temporal_cfpq/fill_results.py` — the fill driver. Reuses from
`run_reference.py`: `stream_g_file`, `grammar_terminals`, `start_symbol`,
`run_solver`, `ensure_container`, `docker_available`, `WORK`; `_MTX_HEADER`
from `flpq_data.graphs.readwrite.mtx`. New logic: (a) the 60-pair target table
(graph, query dir, run grammar path, recorded grammar, reference count +
source, with the vf/aa name mapping); (b) a solver invocation variant that
keeps `pairs.txt` (the current `run_solver` deletes the run dir — extend it
with a `keep_pairs=True` flag instead of duplicating the function); (c) a
streaming `pairs.txt -> results.mtx` writer (O(1) memory: header from the
graph's declared dimensions, entries validated in range, `nnz` = line count,
must equal the solver's reported count); (d) archive handling: keep the
downloaded archive (no per-graph delete), replace the stub
`queries/cfpq/<query>/results.mtx`, re-tar as `<graph>.tar.gz` into
`new_archives/`; (e) resumable CSV `results/big_graph_results.csv` with columns
graph, query_dir, run_grammar, recorded_grammar, num_reachable_pairs, status,
elapsed_sec, peak_rss_kib, archive_out. CLI: `--only <graph>` (repeatable),
`--timeout`, `--mem-limit`, `--timeout-big` (longer limit for unigraph/libgdx).
**Tests:** The script's own assertions are the tests plus a local Docker smoke
run on httpx (expect 4408, status ok): the repacked archive must pass
`utils/check_archive_structure.py`, its `results.mtx` must declare nnz=4408
with in-range entries, and the count must equal the reference. The
pairs.txt->mtx writer is tested on a synthetic file (count mismatch must fail).
**Docs:** none (gitignored local tool).

**Spec:**
- ONE `.g` per graph (run grammars share the terminal set with the canonical
  grammar — the archive checker enforces same-terminal-set per query dir); the
  `.g` is streamed once and reused for every grammar of that graph.
- `pairs.txt` format is verified empirically in the S2 smoke run (whitespace
  separated `u v` pairs, 0-based); the writer fails loudly on any other shape.
- Peak RSS via `/usr/bin/time -v` inside the container (the existing
  `measure_memory=True` path), same as task 157.
- Container caps: default 100 GiB; 115 GiB for unigraph_9, unigraph_10,
  libgdx. Timeouts: 21600 s for unigraph_4..10 and libgdx, 7200 s otherwise.
- A pair whose solver run ends oom/timeout/error is recorded with that status
  and NO archive is repacked for it; the run is resumable (skip pairs already
  `ok` in the CSV).

### S2: Sync repo + tooling to the remote, update the venv [remote] [done]

**Code:** rsync the current tree (`flpq_data/`, `temporal_cfpq/`,
`pyproject.toml`, `uv.lock`) into `/mnt/jblab2-disk/gsv_cfpq/repo` (replacing
the stale `cfpq_data` copy), sync the venv (`uv sync --all-groups` in the
existing venv or recreate it), confirm the Docker image is loaded, and run the
S1 smoke target (httpx) end-to-end on the remote: solve, convert, repack,
validate.
**Tests:** Remote smoke run: httpx count == 4408, `check_archive_structure.py`
passes on the repacked archive, CSV row written, `pairs.txt` format confirmed
against the solver output.
**Docs:** none (remote machine state).

**Spec:**
- The remote repo is a working copy for the tool only — no git operations on
  the remote; the local repo stays the source of truth.
- Graphs download from S3 into the remote's `FLPQ_DATA_CACHE` (default
  `~/.cache/flpq-data`) exactly as in the previous remote runs.

**Execution notes (2026-10-08).** The pre-existing remote Docker image
(`fast_matrix_cfpq:1.1.0`, image id d93f4899f092) was kept as-is — it is the
build that produced the reference values in `reference_answers.csv`
(unigraph_4..7), so new runs stay comparable to their references. The stale
5.0.0-era `cfpq_data/` tree was removed; a fresh `.venv` was created with
`uv sync --all-groups` (uv 0.12.23 installed on the remote). Key-based SSH
(`~/.ssh/jblab2_ed25519`) was set up for rsync. Remote smoke: httpx = 4408
pairs, repacked archive validated.

### S3: Run all 60 pairs on the remote [remote, long-running] [done]

**Code:** Launch `fill_results.py` over the full target table under `nohup`
(resumable; log to `fill_run.log`), ordered small-to-large per category so
failures surface early: httpx, RDF, name_resolution (jiaozi, spd), vf/aa,
c_alias, java_points_to, unigraph_2..7, libgdx, unigraph_8, unigraph_9,
unigraph_10. Monitor and resume as needed; keep `new_archives/` and
`results/big_graph_results.csv`.
**Tests:** Every target pair has a CSV row; all rows `ok` except the pairs
documented infeasible under Decision 4 (those carry oom/timeout status).
**Docs:** none (remote machine state).

**Spec:**
- One graph at a time (bounded disk: archive + `.g` + `pairs.txt` + repacked
  archive, peak ~50 GB for unigraph_5/7); `pairs.txt` is deleted right after
  the conversion.
- Repacked archives accumulate in `/mnt/jblab2-disk/gsv_cfpq/new_archives/`
  until the S5 upload; nothing is uploaded before S4 verification.

**Execution notes (2026-10-08/09).**

- Pass 1 (14:0x–22:28 Oct 8): httpx, RDF, name_resolution, vf/aa, c_alias,
  java_points_to, unigraph_2..5 all `ok` (48 reference matches + the 8
  user-confirmed java_points_to values). unigraph_5's repacked archive was
  validated manually after an ENOSPC in `validate_archive`: it unpacks into
  `tempfile.TemporaryDirectory()` = `/tmp` on the 219G root partition (24G
  free), which cannot hold a ~29G extraction. Fixed by running with
  `TMPDIR=/mnt/jblab2-disk/gsv_cfpq/tmp` (lab disk); no code change.
- unigraph_7 (pass 1) and libgdx failed with a masked status: `run_solver`
  ran `docker cp pairs.txt` BEFORE checking the solver exit status, so the
  copy error hid the real outcome. Root cause of the underlying failure:
  `ensure_container` appended `-v <run_dir>:/tmp/cfpq_run` AFTER the image
  name in `docker run`, where docker treats it as a command argument — the
  bind mount never existed, so multi-GB `pairs.txt` was written to the
  container layer on the root partition and hit ENOSPC. Both bugs fixed in
  `temporal_cfpq/run_reference.py` (flag ordering; status determined before
  the copy, copy only on success).
- Pass 2 (07:26–12:0x Oct 9, mount verified via `docker inspect`):
  unigraph_8 `oom` (peak RSS 99.8 GiB at the 100 GiB cap — cgroup overhead
  put it over), libgdx `oom` (peak 114.8 GiB at the 115 GiB cap, still
  growing → infeasible per Decision 4).
- Pass 3 (12:0x–21:3x Oct 9): unigraph_7 `oom` (peak 99.7 GiB at the 100 GiB
  cap), unigraph_9 `oom` (peak 114.8 GiB at the 115 GiB cap → infeasible per
  Decision 4). unigraph_10 died on a download failure: the lab lost external
  network connectivity (~21:3x Oct 9, S3 + all internet unreachable from both
  machines; still down as of 22:45 Oct 9).
- `process_graph` deletes the cache dir even for failed graphs, so the
  unigraph_7/8 retry needs a re-download from S3 — blocked by the outage.
  The archives are small (unigraph_7 3.5 MB / 285,577 nodes; unigraph_8
  5.7 MB / 449,237 nodes; unigraph_10 29 MB / 2,055,882 nodes).
- State at outage: 55/60 `ok`; libgdx + unigraph_9 infeasible (clean oom
  evidence); unigraph_7 + unigraph_8 retryable at the 115 GiB cap; unigraph_10
  not attempted — infeasible by construction (one dense n×n matrix =
  2,055,882²/8 ≈ 529 GB > 124 GB host RAM).
- Network restored Oct 12 ~09:4x (user fixed the lab uplink). The three
  archives were downloaded locally (sha256-verified against the registry),
  rsynced over the lab network, and installed into the remote cache by hand
  (extract + tarball + `.sha256` sidecar; `graph_dir` reports cache hits).
- Retry pass (Oct 12 09:5x–20:3x): unigraph_7 `ok` — 2,320,964,134 pairs,
  MATCHES the reference (peak 100.5 GiB at the 115 GiB cap). unigraph_8
  `oom` at the 115 GiB cap (peak 114.9 GiB) and unigraph_10
  `error(rc=1):graphblas.exceptions.OutOfMemory` after 60 s. Note: the solver
  grows its memory up to whatever cap is given, so "peaked just under the old
  cap" does NOT mean it fits under a higher one — unigraph_8/9 and libgdx all
  consumed the full 115 GiB; they need more than the host's 124 GB and are
  infeasible per Decision 4.
- FINAL: 60/60 pairs have CSV rows — 56 `ok` (48 exact reference matches + the
  8 user-confirmed java_points_to values of Decision 6), 4 infeasible with OOM
  evidence (libgdx, unigraph_8, unigraph_9, unigraph_10). 50 repacked archives
  in `new_archives/`; all validated except enzyme/taxonomy_hierarchy whose
  validation log line was lost to a log truncation — re-validated in S4.

### S4: Verify counts and validate every repacked archive [local] [done]

**Code:** Pull `results/big_graph_results.csv`; cross-check every computed
count against its reference (53 rows of `reference_answers.csv` with the vf/aa
name mapping + 3 external values from `temporal_cfpq/README.md`); run
`utils/check_archive_structure.py` on every repacked archive (on the remote,
results pulled back). Produce the verification table (pair, count, reference,
match, status, elapsed_sec, peak_rss_kib) that feeds the S6 record.
**Tests:** 48/56 referenced pairs match their reference exactly; the 8
java_points_to pairs with stale references (Decision 6) carry user-confirmed
fresh values; 0 structure violations across all repacked archives; the 4
unreferenced pairs (libgdx, unigraph_8/9/10) are either computed-and-sanity-checked
or documented infeasible per Decision 4.
**Docs:** none (verification output feeds the S6 record).

**Spec:**
- Any mismatch is a STOP: investigate (grammar selection, `.g` tokenization,
  solver status) before any upload; mismatches are never "explained away" —
  the sole exception is Decision 6 (the 8 user-confirmed stale java_points_to
  references).
- For the unreferenced pairs that do compute, sanity-check the result (pair
  count within the graph's n² bound, density comparable to sibling graphs of
  the same category) and flag them as "no independent reference" in the record.

**Execution notes (2026-10-12).** Cross-check of the final
`results/big_graph_results.csv` (latest row per pair): 48/56 referenced pairs
match their reference exactly (including unigraph_7 = 2,320,964,134); the 8
java_points_to pairs carry the user-confirmed fresh values of Decision 6; the
4 unreferenced pairs are all documented infeasible with OOM evidence (libgdx,
unigraph_8, unigraph_9 consumed the full 115 GiB cap; unigraph_10 raised
`graphblas.exceptions.OutOfMemory` after 60 s — one dense matrix alone is
~529 GB > 124 GB host RAM). All 50 repacked archives pass
`utils/check_archive_structure.py` (50/50 OK, run with `TMPDIR` on the lab
disk; results in `results/archive_validation.txt`) — including enzyme and
taxonomy_hierarchy, whose original validation log line was lost to a log
truncation.

### S5: Upload updated archives + CSV to S3 [remote, needs credentials]

**Code:** With the user-provided IAM keys (Decision 5), run
`utils/upload_to_s3.py` on the remote for every repacked archive under
`6.0.0/graph/<graph>.tar.gz` and for the updated `reachable_pairs.csv` under
`6.0.0/reachable_pairs.csv`.
**Tests:** Post-upload audit: `utils/check_archive_structure.py --audit
--prefix 6.0.0/graph` (or per-object download + validate) reports 0 violations;
sha256 of each uploaded object equals the local repacked file.
**Docs:** none (S3 state).

**Spec:**
- Uploads happen only after S4 is fully green and the user has seen the
  verification table.
- Keys are passed as CLI arguments only; never stored in files, logs, or the
  record.

### S6: Sync the repo data: CSV, docs tables, registry, record [commit]

**Code:** Fill the 60 cells of `flpq_data/dataset/reachable_pairs.csv` (the
infeasible pairs, if any, stay empty per Decision 4); regenerate both doc
renderings with `utils/reachable_pairs_tables.py --update`
(`docs/reachable_pairs.rst` + the count columns of `docs/graphs/*.rst`);
regenerate `flpq_data/dataset/registry.json` with `utils/generate_registry.py`
(post-upload, so sha256/size follow S3); new `utils/stub_results_record.json`
mirroring the `*_record.json` convention: description (what was filled and why),
date, per-pair table (run grammar, count, status, elapsed_sec, peak_rss_kib,
verification source + value, archive sha256 before/after), the vf/aa name
mapping note, and the documented infeasible pairs with the hardware-limitation
rationale. CHANGELOG.md `[Unreleased]` entry.
**Tests:** `utils/reachable_pairs_tables.py` (check mode) exits 0;
`registry.json` parses and its sha256/size columns match the S3 objects for the
changed graphs; the record JSON is valid and its counts equal the CSV cells.
**Docs:** `docs/reachable_pairs.rst`, `docs/graphs/*.rst` (generated),
`CHANGELOG.md`.

**Spec:**
- Single work commit `feat(130-S6): ...` carrying a standalone `Closes #130`;
  a final `docs(130)` commit marks S6 done (the 156 pattern). The plan file is
  committed with the work commit.

## Commit structure

S1–S5 touch only gitignored local tooling, the remote machine, and S3 → no
commits (bounded uncommitted repo work = none until S6). S6's work commit
carries `Closes #130`; a final `docs(130)` commit marks it done.
