# Detailed Plan: Task 42 — FLPQ design document

Task: design the structure of the site and the project for extending CFPQ_Data
to all classes of formal-language-constrained path queries (FLPQ): regular
(RPQ), context-free (CFPQ, existing), and multiple context-free (MCFPQ).
Docs-only task — no `.py` files change; code-specific gates (tests, lint,
format) are skipped per the workflow rules, but the docs build (no-warnings
policy) and the link check must pass.

Deliverable: `docs/flpq.rst` — the single source of truth for the FLPQ design
(taxonomy, MCFG formalism, `.mcfg` format spec, target site/package/dataset
structure, migration path), linked from the index toctree so team members can
discuss it. Plus the follow-up task list in `tasks/global_plan.md`.

Locked decisions (user guidance, recorded verbatim in `tasks/tasks.md`):
- Package renamed to `flpq_data` / PyPI `flpq-data` at 6.0.0; `cfpq-data`
  becomes a thin deprecation shim.
- Graphs: shared catalog (single source of truth); per-class sections
  cross-link applicable graphs.
- MCFPQ = Seki's multiple context-free languages (a language class wider than
  CFL), NOT a combination of several CFGs; reference application: Conrado et
  al., "Program Analysis via Multiple Context Free Language Reachability"
  (ACM doi 10.1145/3704854).
- MCFGs are specified in a Datalog-like syntax (user requirement); parser
  library: `lark` (verified: no off-the-shelf Datalog/MCFG text parser exists
  — MCFG head templates are not standard Datalog; lark is MIT, maintained,
  zero required deps).
- Reachable pairs: the flat table stays as a downloadable CSV for automatic
  processing; site rendering is split into per-category tables.
- Incremental tasks first (reachable-pairs refactor, MCFG readwrite); NO
  release task is planned — "We must do much more tasks first."

Research facts used by this plan (verified 2026-09-18):
- Seki, Matsumura, Fujii, Kasami, "On multiple context-free grammars",
  Theoretical Computer Science 88(2), 191–229, 1991,
  doi 10.1016/0304-3975(91)90374-B — the d-MCFG(r) formalism: dimension d
  bounds nonterminal arity, rank r bounds RHS nonterminals; CFL = 1-MCFL;
  TAL = 2-MCFL(2); membership in O(n^{d(r+1)}).
- Conrado, Kjelstrøm, Pavlogiannis, van de Pol, "Program Analysis via Multiple
  Context Free Language Reachability", POPL 2025 (arXiv 2411.06383; ACM doi
  10.1145/3704854) — Datalog-like predicate notation for MCFGs
  (`A(x1, ..., xk)` predicates; basic rules `A(s1, ..., sk)`; production rules
  `A0(s1, ..., sk0) <- A1(...), ..., Al(...)` with head templates mixing
  terminals and variables, each variable at most once); reachability semantics:
  an arity-k nonterminal denotes k independent paths, `S[(u,v)]` gives the
  reachable pairs (start symbol always arity 1); O(n^{2d+1}) for r=1,
  O(n^{d(r+1)}) for r>1; no public implementation (private Go tool).
- Current site: one flat ~155-row table in `docs/reachable_pairs.rst`;
  per-category graph tables already carry count columns (task 28); data source
  is `cfpq_data/dataset/reachable_pairs.csv` + `reachable_pairs()` API.

### S1: Create docs/flpq.rst with the FLPQ taxonomy and model

**Code:** none (docs-only task).
**Tests:** docs build must stay warning-free after the change (no-warnings
policy); no pytest impact.
**Docs:** new file `docs/flpq.rst` (skeleton + complete "Query classes" and
"Multiple context-free languages" sections); add `flpq` to the index toctree
in `docs/index.rst` (between `getting_started` and `dataset`) so the page is
not orphaned from the first commit.

**Spec:**
- Page label `.. _flpq:`, title "FLPQ: Formal-Language-Constrained Path
  Querying", standard `.. only:: html` release/date header like other pages.
- Intro paragraph: FLPQ = paths of a labeled graph constrained by a formal
  language; the project currently covers CFPQ and is extended to RPQ and
  MCFPQ; this page records the design decisions (what/why), implementation
  happens in follow-up tasks.
- "Query classes" section: list-table with columns Query class | Language
  class | Formalism | Status in the dataset:
  - RPQ — Regular — regular expressions, NFA/DFA — planned
  - CFPQ — Context-free — CFG/CNF (incl. indexed grammars) — current
  - MCFPQ — Multiple context-free (Seki) — MCFG, d-MCFG(r) — planned
  Plus a paragraph: all classes share the same query pattern (a language L
  constrains graph paths; (u, v) reachable iff some string of L labels a path
  u -> v); they differ only in the language class and its formalism.
- "Multiple context-free languages" section: definition of d-MCFG(r) in the
  predicate notation (nonterminal = predicate A(x1, ..., xk), arity k <= d;
  basic rules A(s1, ..., sk) with terminal strings incl. epsilon; production
  rules A0(s1, ..., sk0) <- A1(...), ..., Al(...) with l <= r, head templates
  over terminals + variables, each variable at most once; start symbol arity
  1); hierarchy facts (CFL = 1-MCFL, TAL = 2-MCFL(2), mildly context-sensitive,
  decidable membership O(n^{d(r+1)})); reachability semantics (arity-k
  nonterminal = k independent paths; reachable pairs via the arity-1 start
  symbol; complexity O(n^{2d+1}) for r=1 / O(n^{d(r+1)}) for r>1) and the
  static-analysis application (underapproximating interleaved Dyck
  reachability). Use :math: roles for the notation.

### S2: Add the .mcfg grammar format spec section

**Code:** none.
**Tests:** docs build warning-free.
**Docs:** extend `docs/flpq.rst` with a "MCFG grammar format (.mcfg)" section.

**Spec:**
- State the design decision: Datalog-like syntax per Conrado et al.'s
  predicate notation (user requirement); rationale for the parser choice —
  verified that no off-the-shelf library parses this syntax (PyPI `datalog` is
  a hardware ADC lib; `pyDatalog` is an engine without a documented text
  parser and standard Datalog heads cannot express MCFG head templates; no
  MCFG/MCFL library exists) — therefore `lark` (MIT, maintained, zero
  required deps) with the EBNF grammar doubling as executable format
  documentation.
- Lexical conventions (one rule per line; blank lines and `#` comments
  ignored): nonterminals = identifiers starting with an uppercase letter;
  terminals = edge labels verbatim; variables = `x` followed by digits
  (x1, x2, ...), a terminal must never match this pattern; epsilon = the
  token `eps`; arrow = `<-`.
- Rule forms: basic rule `A(s1, ..., sk)` (arguments are space-separated
  terminal tokens or `eps`); production rule
  `A0(s1, ..., sk0) <- A1(x...), ..., Al(x...)` (body atoms carry variables
  only).
- Validation constraints enforced by the reader: arity consistency per
  nonterminal; all body variables pairwise distinct; each body variable
  appears exactly once across the head templates (no dangling variables —
  stricter than the minimal definition, satisfied by all published examples);
  start symbol defaults to `S`, must have arity 1, overridable via an API
  parameter (consistent with the existing cnf/cfg/rsa readers).
- Dimension d and rank r are computed from the rules (max arity / max body
  atoms) and reported by the reader — no header to keep in sync.
- Two worked examples in code blocks: the paper's 2-MCFG(2) for
  L = {w1 w2 # w2 w1 | w1, w2 in {0,1}*} (A(eps, eps); A(x1 0, x2 0) <-
  A(x1, x2); A(x1 1, x2 1) <- A(x1, x2); S(x1 y1 # y2 x2) <- A(x1, x2),
  A(y1, y2)) and a d=1 CFG embedding for {0^n 1^n 1^m 0^m} showing the format
  subsumes CFGs.
- Relationship to existing formats: CFPQ data stays `.cnf` (pyformlang
  ecosystem, no re-upload); MCFPQ uses `.mcfg`; a `.cnf <-> .mcfg` converter
  is a follow-up task; RPQ keeps regex text files.

### S3: Add the site structure design section

**Code:** none.
**Tests:** docs build warning-free.
**Docs:** extend `docs/flpq.rst` with a "Site structure" section.

**Spec:**
- Target hierarchy (code block): Dataset -> Graphs (shared catalog, 8
  categories, unchanged) + one section per query class (CFPQ / RPQ / MCFPQ),
  each with its Grammars/Queries templates page, Benchmarks, and a list of
  applicable graphs (cross-links, no duplication); Reachable pairs page at
  the Dataset level. Note the navigation depth: conf.py `navigation_depth` is
  3, which accommodates section -> class -> template pages.
- Reachable-pairs rendering design: the flat table is removed from
  `docs/reachable_pairs.rst`; the page renders one table per graph category
  (columns Graph | Grammar | Reachable pairs); the CSV remains the single
  source of truth for automatic processing and gains a `category` column; a
  utils generator script (pattern of `utils/archive_sizes.py`) renders both
  the per-category tables and the category-page count columns from the CSV so
  no numbers are hand-maintained in two places.

### S4: Add the package structure and API design section

**Code:** none.
**Tests:** docs build warning-free.
**Docs:** extend `docs/flpq.rst` with a "Package structure" section.

**Spec:**
- Target layout (code block): `flpq_data/` with `config.py`, `dataset/`
  (download machinery + per-class registries + reachable_pairs), `graphs/`
  (unchanged, class-agnostic I/O), and `queries/` (renamed from `grammars/`)
  containing `cfpq/` (existing generators/readwrite{cfg,cnf,cnf_template}/
  converters/utils), `rpq/` (regex + rsa readwrite moved here; new
  regex-template generators), `mcfpq/` (new lark-based mcfg readwrite;
  generators).
- Interim placement before the rename: MCFG readwrite lands in
  `cfpq_data/grammars/readwrite/mcfg.py` (formalism-based module convention,
  alongside `regex.py` and `rsa.py`) so no global rework is needed to start.
- API changes: `download(name)` -> `download_graph(name)`;
  `download_grammars(template, graph_name=None)` ->
  `download_query(query_class, template, graph_name=None)`; old names kept as
  deprecated aliases; registries `DATASET` -> `GRAPHS`,
  `GRAMMAR_TEMPLATES` -> per-class `CFPQ_TEMPLATES` / `RPQ_TEMPLATES` /
  `MCFPQ_TEMPLATES`; `reachable_pairs()` gains the category field.
- Distribution: new PyPI project `flpq-data` at 6.0.0; `cfpq-data` 6.0.0 is a
  thin shim depending on `flpq-data`, re-exporting the old names with
  DeprecationWarning.

### S5: Add the dataset layout + migration path; write the follow-up task list

**Code:** none.
**Tests:** docs build warning-free.
**Docs:** extend `docs/flpq.rst` with a "Dataset layout and migration"
section; rewrite `tasks/global_plan.md` with the follow-up task list.

**Spec:**
- Target S3 layout under the 6.0.0 prefix (code block):
  `graph/<name>.tar.gz` (shared, copied from 5.0.0);
  `query/{cfpq,rpq,mcfpq}/<template>[_<graph>].tar.gz` (cfpq migrated from
  the legacy 4.0.0/grammar prefix); `benchmark/<class>/<name>.tar.gz`
  (MS_Reachability -> cfpq/). Rationale: graphs are big and class-agnostic —
  one shared prefix; queries are class-specific.
- Migration path bullets: copy graph archives to the 6.0.0 prefix; move
  grammar archives under query/cfpq/; re-point DATASET_URL/GRAMMARS_URL via
  the version bump (part of the rename task); upload tools in `utils/` gain
  the class-aware key layout.
- `tasks/global_plan.md`: follow-up tasks in execution order with
  dependencies — Task 43 reachable-pairs site refactor (per-category tables,
  CSV + category column, generator util); Task 44 MCFG readwrite module with
  lark (`cfpq_data/grammars/readwrite/mcfg.py`, format per docs/flpq.rst,
  doctests with the paper's examples); Task 45 RPQ query templates + seed
  data; Task 46 reachable_pairs query_class column (+ generator update);
  Task 47 S3 6.0.0 layout migration + upload tools; Task 48 package
  rename/restructure to flpq_data (queries/{cfpq,rpq,mcfpq}, API renames,
  cfpq-data shim, VERSION 6.0.0); Task 49 site restructure to the FLPQ
  hierarchy. Dependencies: 43 and 44 independent after 42; 46 after 43; 47
  after 45; 48 after 47; 49 after 48. Explicitly note: NO release task is
  planned — the user deferred it ("We must do much more tasks first").

### S6: Final verification of the docs build and link check

**Code:** none.
**Tests:** full docs build (`make -C docs html` per docs/README.md, no-
  warnings policy) must exit 0; `sphinx-build -b linkcheck` must report no
  broken or timed-out links (the two documented conf.py exceptions apply).
**Docs:** fix any warning/link issue found; record the verification outcome
  in this plan.

**Spec:**
- Run the docs build and the link check exactly as the quality gate defines
  them (docs/developer.rst "Docs build and deploy").
- Verify `docs/flpq.rst` is reachable from the index toctree and renders all
  six sections; verify no orphan/duplicate-label warnings.
- Record PASS/BLOCKED outcome here before code review.

**S6 outcome: PASS (with a linkcheck robustness fix).**

The first link-check runs failed on Wikipedia URLs with 403 "Too many
requests" — transient rate limiting of datacenter IPs, not broken links
(identical direct requests answered 200 seconds apart; sphinx dedupes URLs
per run, so it was not duplicate checking). Fixed in `docs/conf.py`,
extending the retry infrastructure already present for intersphinx:

- `_Session.request` (the path both linkcheck and intersphinx go through)
  now retries transient failures — connection errors/timeouts and HTTP
  403/429 — with the existing backoff before a response is reported; a
  persistent block still reports broken after the retries. Verified with a
  direct test (2 simulated 403s -> retry -> 200).
- `linkcheck_retries = 5` adds outer attempts on top, because Wikipedia's
  limit window can outlast one backoff cycle (observed: one URL answered
  403 to every attempt of a run while identical direct requests passed).

Final gate result: 363 tests passed; pre-commit clean (ruff check/format,
version sync, ty); docs build exit 0 with zero warnings; link check exit 0
with no broken or timed-out links. All four new external links verified:
arxiv.org/abs/2411.06383 ok, doi.org/10.1016/0304-3975(91)90374-B redirect
to Elsevier (reported, not failing), github.com/lark-parser/lark ok,
dl.acm.org/doi/10.1145/3704854 ignored (documented exception).
