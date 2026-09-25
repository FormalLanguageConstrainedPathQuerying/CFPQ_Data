# Detailed Plan: Task 48 — S3 6.0.0 self-contained archive migration

## Context

Migrate all 113 graph archives from the 5.0.0 flat `grammar/` layout to the
6.0.0 self-contained `queries/cfpq/<query>/` structure (designed in tasks 52,
54). Fix naming inconsistencies (aa/vf swap, java_points_to load→load_i,
stored reverses with old "bar" naming). Compute `results.mtx` via the
FastMatrixCFPQ Docker oracle for fast pairs (< 30s); stub empty files for
slow/OOM pairs. Verify reachable-pair counts against
`temporal_cfpq/results/reference_answers.csv` and report all drift. Upload to
S3 `6.0.0/graph/`. Remove separate grammar/ and benchmark/ paths from S3,
docs, and package code.

## Subtasks

### S1: Extend check_archive_structure.py with naming rules [done]

- Add `_label_problems(graph_dir)`: no `bar`/`rev` components; indexed-reversed
  order must be `<base>_r_<N>`; no stored reverses (if `L.mtx` exists,
  `L_r.mtx` must not).
- Add `_terminal_coverage_problems(graph_dir, queries_dir)`: every query
  terminal must map to a stored label, its `_r` reverse, or an indexed form
  `<base>_i` where `<base>_<N>.mtx` exists.
- Add `_same_dir_consistency_problems(queries_dir)`: all representations in
  one query directory must use the same terminal set.
- Relax class-dir requirement: at least one of {cfpq, rpq, mcfpq} present;
  any individual one may be absent.
- Wire `_naming_problems` into `_validate_root`.
- Fix the LSP error (None-safe regex group access).
- Verify: run checker on a local archive (bzip) — should pass structure,
  flag naming issues if any.

### S2: Fix local CNF naming [done]

- `avrora/grammar/java_points_to.cnf`: replace bare `load`→`load_i`,
  `store`→`store_i`, `load_r`→`load_r_i`, `store_r`→`store_r_i`; update
  nonterminal names to indexed form (match gson's correct CNF from 5.0.0).
- Same for `eclipse/grammar/java_points_to.cnf`.
- Verify all other local .cnf/.rsm files use unified naming.

### S3: Build rebuild script + restructure all 113 archives [done]

Script logic (per graph):
1. Download `5.0.0/graph/<name>.tar.gz` from S3.
2. Unpack to temp dir.
3. Strip stored reverses from `graph/`: remove `X_r.mtx` where `X.mtx`
   exists; remove any `*bar*.mtx`.
4. Create `queries/cfpq/<query_name>/` per category:
   - C Alias (20): `c_alias/` with c_alias.cnf + _muravev2024.cnf + c_alias.rsm
   - RDF standard (18): 3 dirs (subClassOf, type, subClassOf_type) each with
     .cnf + shared .rsm in subClassOf_type dir
   - RDF enzyme+geospecies (2): above 3 + broaderTransitive/
   - Java Points-To (21): `java_points_to/` with .cnf + _muravev2024.cnf + .rsm
   - Field-Sensitive Alias (10): `vf/` with vf.cnf + vf.rsm
   - Context-Sensitive Data-Flow (10): `aa/` with aa.cnf + aa.rsm
   - Data Provenance (18): `prov_derivation/` with .cnf (no RSM yet)
   - Name Resolution (4): `name_resolution/` with .cnf (no RSM yet)
   - Biological UniProt (10): `unigraph_N/` per-graph with .cnf (no RSM yet)
5. Write `queries/README.md` with `## cfpq/<query>` sections.
6. Ensure top-level `README.md` has mandatory sections.
7. Remove old `grammar/` directory.
8. Validate with extended checker.
9. Pack as `<name>.tar.gz`.

### S4: Compute results.mtx via oracle (< 30s pairs) [done]

For each graph×query pair in reference with elapsed < 30s AND status=ok:
1. Build `.g` file (forward + auto-reverse, indexed label expansion).
2. Materialize CNF template → concrete CNF.
3. Run FastMatrixCFPQ Docker oracle.
4. Write `results.mtx` (Boolean pattern matrix).
5. Assert pair count matches reference.

For pairs >= 30s or status != ok: write stub results.mtx (header, 0 entries).

### S5: Drift report [done]

Compare all computed counts against reference_answers.csv. Output
`drift_report.csv`: graph, query, ref_count, new_count, delta, explanation.
Expected drift: 20 swap-fix pairs + 2 java_points_to pairs. Flag any
unexpected drift.

### S6: Upload to S3 + cleanup [done]

1. Upload all 113 .tar.gz to `s3://cfpq-data/6.0.0/graph/`.
2. Delete `6.0.0/grammar/` and `6.0.0/benchmark/` objects.
3. Package code: remove GRAMMAR_TEMPLATES, BENCHMARKS, download_grammars(),
   download_benchmark(), GRAMMARS_URL, BENCHMARK_URL, LEGACY_VERSION_PREFIX;
   update DATASET_KEY_PREFIX to "6.0.0/graph".
4. Config: remove GRAMMARS_DIR, BENCHMARKS_DIR.
5. Docs: remove grammar example links, benchmark refs; update URLs to 6.0.0.

### S7: [FOLLOW-UP — separate task] Fill results.mtx for big graphs [moved to Task 58]

All stub pairs (elapsed >= 30s or OOM/timeout). May need increased Docker
memory, parallel execution, or algorithm changes.

## Reference data

- `temporal_cfpq/results/reference_answers.csv`: 155 pairs (148 ok, 7 OOM,
  1 timeout). Columns: graph, grammar, start_symbol, num_nodes, num_edges,
  num_reachable_pairs, status, elapsed_sec.
- Docker container: `fast_matrix_cfpq` (image `fast_matrix_cfpq:1.1.0`).
- S3: bucket `cfpq-data`, endpoint `https://s3.yandexcloud.net`.
- Local RSM templates: `/tmp/opencode/rsm_templates.py` (c_alias, java_points_to,
  vf, aa, nested_parentheses).

## Category → grammar mapping

| Category | Graphs | Query dir(s) | .cnf | .rsm |
|----------|--------|-------------|------|------|
| C Alias | wc,bzip,pr,ls,gzip,apache,init,mm,ipc,lib,block,arch,crypto,security,sound,net,fs,drivers,postgre,kernel (20) | c_alias/ | c_alias.cnf, _muravev2024.cnf | c_alias.rsm |
| RDF std | skos,generations,travel,univ,foaf,atom,people,biomedical,pizza,wine,funding,core,pathways,go_hierarchy,go,eclass,taxonomy,taxonomy_hierarchy (18) | nested_parentheses_subClassOf/, _type/, _subClassOf_type/ | 3 variants | _subClassOf_type.rsm |
| RDF ext | enzyme, geospecies (2) | above 3 + _broaderTransitive/ | 4 variants | (Task S7+) |
| Java PT | gson,sunflow,lusearch,luindex,avrora,mockito,commons_io,commons_lang3,eclipse,h2,pmd,xalan,junit5,batik,fop,tomcat,guava,jackson,jython,tradebeans,tradesoap (21) | java_points_to/ | .cnf, _muravev2024.cnf | .rsm |
| FS Alias | xz_fsa,nab_fsa,leela_fsa,povray_fsa,x264_fsa,cactus_fsa,parest_fsa,perlbench_fsa,imagick_fsa,omnetpp_fsa (10) | vf/ | vf.cnf | vf.rsm |
| CS DataFlow | xz,nab,leela,x264,parest,imagick,povray,cactus,omnetpp,perlbench (10) | aa/ | aa.cnf | aa.rsm |
| Provenance | sampleproject,wikipedia-provenance,pluggy,itsdangerous,requests,httpx,click,jinja,flask,fastapi,celery,scikit-learn,sphinx,pandas,django,zulip,superset,airflow (18) | prov_derivation/ | .cnf | (S7+) |
| Name Res | jiaozi,jsonpath,shattered_pixel_dungeon,libgdx (4) | name_resolution/ | .cnf | (S7+) |
| UniProt | unigraph_1..10 (10) | unigraph_N/ per-graph | .cnf | (S7+) |
