# Detailed Plan: Task 157 — Transform the uniprot grammar to minimize dense intermediate matrices

Issue #157. The uniprot (unigraph) CFPQ grammar materializes very dense
intermediate n×n matrices (the `Seq` closure and dense×medium products), which
makes FastMatrixCFPQ OOM on unigraph_9/10 and take 67 min–4.8 h on
unigraph_4–8. This task applies the muravev-style restructuring
(arXiv:2401.11029, optimization 5 — the same idea behind
`java_points_to_muravev2024.cnf` / `c_alias_muravev2024.cnf`) to the uniprot
grammar: restructure the WCNF so that dense nonterminals are never standalone
factors in binary productions, while preserving the language. Language
preservation is checked first — equality of reachable pairs on small graphs via
the FastMatrixCFPQ oracle (`temporal_cfpq`).

## Context

**The muravev pattern.** In both published transformations the dense
nonterminal appears only multiplied by terminal-anchored (sparse) matrices:

- c_alias: original `M -> d̄·V·d` with `V2 -> ε|M` (dense standalone factor;
  dense×dense products in `V1·V2`, `V2·V3`) becomes
  `M -> N1·N3 | N2·N3` with `N1`/`N3` terminal-anchored runs and `M` only via
  `N2 -> N1·M`, `AM -> a·M`.
- java_points_to: original materializes dense `Al = PT·FT` as a factor
  (`PTH -> load_i·Al·store_i·PTH`); the optimized grammar uses
  `LP_i -> load_i·PT`, `FS_i -> FT·store_i`, `LPFS_i -> LP_i·FS_i`.

**The uniprot grammar** (in-archive `unigraph_N.cnf`, identical language for
all 10 graphs). With `X = IsSimilar`, `R = refers_to·refers_to_r`,
`cf = codes_for`:

```
S = Seq · R · X,   Seq = X | X·cf·X,
X = ε | has·X·has_r | iso·X·iso_r·X | bt·X·bt_r | pi·X·pi_r
```

`X` is a *nested balanced* (Dyck-like) language. The original WCNF
materializes dense `M_Seq ≈ M_X ∪ M_X·cf·M_X` and does dense×medium products
(`S -> Seq·S_1`, `Seq -> X·Seq_1`).

**Pitfall found while prototyping.** A flat "run of steps" restructuring
(`Lp -> Step·Lp | ...`) is NOT equivalent: `X` is nested, not a Kleene star —
the prototype accepted 480556 pairs on unigraph_1 vs the correct 376578. The
correct fact: non-ε `X` = exactly ONE outermost step
(`X⁺ = St1∪St2∪St3∪St4`).

## Transformed grammar (design)

```
S -> N3 | Lp·N3,   N3 = IsAssociated·IsSimilar        (refers_to-anchored)
Lp = St1|St2|St3|St4 | CfX | StCf1|StCf2|StCf3|StCf4  (terminal-prefixed)
StCfi = St_i·CfX,   CfX = codes_for·IsSimilar
St1 = has·X·has_r, St2 = iso·X·iso_r·X, St3 = bt·X·bt_r, St4 = pi·X·pi_r
```

**Equivalence.** `L(S) = X·(ε|cf·X)·R·X = R·X ∪ X⁺·R·X ∪ cf·X·R·X ∪
X⁺·cf·X·R·X` — exactly the language of the transformed grammar. Verified by
in-memory brute force on unigraph_1: pair sets identical (376578, matches the
recorded reference).

**Sparsity.** The dense `M_Seq` matrix is eliminated; every multiplication of
dense `X` is terminal×dense or dense×terminal; the top-level product `Lp·N3`
pairs two terminal-anchored (edge-count-bounded) matrices.

## Decisions (confirmed with the user)

1. Scope: **experiment only** — no archive/S3 changes, no package code changes.
2. Verification graphs: **unigraph_1 + unigraph_2 + unigraph_3** (small).
3. File name: `unigraph_1_sparse.cnf`.
4. User guidance (verbatim): "In report provide difference for both time and
   memory consumption between original and modified grammars."

## Subtasks

### S1: Update temporal_cfpq tooling for flpq_data 6.0.0 [local, gitignored] [done]

**Code:** `temporal_cfpq/run_reference.py`, `temporal_cfpq/verify_bf.py`,
`temporal_cfpq/verify_optimized.py`: imports `cfpq_data.*` → `flpq_data.*`
(`dataset.data.download` → `graph_dir`; `grammars.readwrite.cnf_template` →
`queries.cfpq.readwrite.cnf_template`; drop removed `config.GRAPHS_DIR`);
in-archive grammar path `path/"grammar"/*.cnf` →
`path/"queries/cfpq/<query>"/*.cnf`.
**Tests:** import check of all three scripts; `stream_g_file` +
`grammar_terminals` smoke run on the cached `unigraph_1` unpacked archive.
**Docs:** none (gitignored local tool).

**Spec:**
- Keep the CLI behavior and CSV schemas unchanged.
- `graph_dir(name)` replaces `download(name)` (same return: unpacked dir).
- Grammar discovery helper returns the query dir(s) under `queries/cfpq/`;
  scripts that glob `grammar/*.cnf` must instead glob
  `queries/cfpq/*/*.cnf`.

### S2: Add unigraph_1_sparse.cnf + verification script; run on unigraph_1 [local, gitignored] [done]

**Code:** New `temporal_cfpq/grammars/unigraph_1_sparse.cnf` (38 productions,
WCNF, same terminal set as the original, start `S` — content fixed by the
design above). New `temporal_cfpq/verify_uniprot_sparse.py` modeled on
`verify_optimized.py`: for each graph in CASES = unigraph_1/2/3, stream ONE
`.g` (terminal sets are identical), run the solver once per grammar
(original in-archive `.cnf` vs `unigraph_1_sparse.cnf`), compare counts
pairwise AND against the recorded references in
`results/reference_answers.csv`; append rows to
`results/uniprot_sparse_check.csv`; exit non-zero on any mismatch or solver
failure.
**Tests:** The script's own assertions ARE the tests: unigraph_1 must give
original == sparse == 376578, status ok for both runs.
**Docs:** none (gitignored local tool).

**Spec:**
- Reuse `run_reference.py` helpers (`stream_g_file`, `run_solver`,
  `ensure_container`, `docker_available`) — no duplicated logic.
- The sparse `.cnf` must parse with `cnf_template_from_cnf`.
- Reference counts: unigraph_1 = 376578, unigraph_2 = 39888347,
  unigraph_3 = 52471840 (from `results/reference_answers.csv`).

### S3: Run on unigraph_2 + unigraph_3; collect time AND memory [local, gitignored] [done]

**Code:** Extend the solver invocation in `verify_uniprot_sparse.py` to wrap
the CLI with `/usr/bin/time -v` inside the container and record
`Maximum resident set size (kbytes)` per run (peak RSS of the solver process);
CSV gains a `peak_rss_kib` column. Run CASES unigraph_2, unigraph_3
(unigraph_1 re-run for a complete table).
**Tests:** All three graphs: original == sparse == recorded reference, status
ok; CSV contains elapsed_sec and peak_rss_kib for all 6 runs.
**Docs:** none (gitignored local tool).

**Spec:**
- Memory = peak RSS of the solver process via `/usr/bin/time -v` (available in
  the image), NOT container-level `docker stats` sampling.
- Same container memory cap (10 GiB) and timeout (600 s) for both grammars —
  fair comparison.
- Report (printed + CSV): per graph, original vs sparse: elapsed time, peak
  RSS, reachable pairs; plus the absolute and relative differences.

### S4: Record the experiment in the repo [commit] [done] (b51918a)

**Code:** New `utils/uniprot_sparse_record.json` — mirrors the
`optimized_grammars_record.json` convention: description (what was transformed
and why), date, the full transformed `.cnf` text, the equivalence rationale
(including the nested-vs-flat pitfall), and the verification table (graph ×
grammar: pairs, status, elapsed_sec, peak_rss_kib) with the time/memory
differences.
**Tests:** `python3 -m json.tool` validity; the embedded `.cnf` parses via
`cnf_template_from_text`; the pairs column matches
`results/uniprot_sparse_check.csv`.
**Docs:** none (no package code, no shipped grammar — experiment record only).

**Spec:**
- Single commit `docs(157-S4): ...` with a standalone `Closes #157` line.
- The record is the durable artifact: temporal_cfpq/ is gitignored and
  machine-local.

## Commit structure

S1–S3 touch only gitignored local tooling → no commits (bounded uncommitted
work = none; the repo stays clean until S4). S4's work commit (`docs(157-S4)`)
carries `Closes #157` and commits the plan file together with the record; a
final `docs(157)` commit marks S4 done (the 156 pattern).
