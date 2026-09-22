# Detailed Plan: Task 54 — Archive structure extension (multiple specifications per query + per-query results)

## Context

Task 52 introduced the self-contained graph-archive layout with flat query
files (`queries/<class>/<name>.<ext>`). Task 54 extends it: one query may be
specified in several ways (different grammars; for CFPQ — a CFG or an RSM),
and every query carries one results file that is independent of the
specification. Design documents + tooling only — no data re-upload (the
migration happens in task 48).

### RSM investigation result (done)

- **Formalism** (Alur, Etessami, Yannakakis, CAV 2001; applied to CFPQ in
  Abzalov et al., "GLL-based Context-Free Path Querying for Neo4j",
  arXiv:2312.11925 — which evaluates on CFPQ_Data itself): an RSM is a set of
  **boxes**; each box is a DFA without ε-transitions over the union alphabet
  of terminals and nonterminals (start states of other boxes), with a start
  state and final states. No stack in the representation — the stack appears
  only during computation, which makes the machine "recursive". A grammar in
  EBNF (productions `N -> E` where `E` is a regular expression over
  terminals ∪ nonterminals) maps to an RSM with one box per production.
- **pyformlang support**: `pyformlang.rsa` — `RecursiveAutomaton` + `Box`
  (a box wraps an epsilon-NFA; `.dfa` determinizes it).
- **Already in the repo** (doctests pass, reuse — do not duplicate):
  - `cfpq_data/grammars/readwrite/rsa.py`: `rsa_from_text/to_text/from_txt/
    to_txt` — the EBNF-style text format (one box per production line, RHS
    parsed as a regex over terminals + nonterminals).
  - `cfpq_data/grammars/converters/cfg.py`: `cfg_from_rsa` — RSM → CFG
    (each NFA state becomes a nonterminal, each transition a production).

### User decisions (recorded verbatim in tasks.md)

1. `.rsm` specification files are allowed in **both** `cfpq/` and `rpq/`.
   In `rpq/` the RSM must be regular: no transition label may be a
   nonterminal (box name) — i.e. no recursion.
2. Each query is a **directory**: `queries/<class>/<query>/` containing all
   representations of the language plus one `results.mtx`. The result is
   independent of the representation; it depends on the language (the query).

## Design

### New archive layout

```
<name>/
├── README.md                 (unchanged: 8 mandatory questions)
├── graph/
│   └── <label>.mtx ...       (unchanged)
└── queries/
    ├── README.md             (one section per query directory)
    ├── cfpq/
    │   └── <query>/
    │       ├── <rep_1>.cnf   ┐ ≥ 1 representation file,
    │       ├── <rep_2>.rsm   ┘ allowed extensions per class:
    │       └── results.mtx       cfpq: .cnf .rsm
    ├── rpq/                    rpq:  .re .rsm (regular only)
    │   └── <query>/            mcfpq: .mcfg
    │       ├── <rep>.re / <rep>.rsm
    │       └── results.mtx
    └── mcfpq/
        └── <query>/
            ├── <rep>.mcfg
            └── results.mtx
```

- Representation file names are author-chosen; the extension selects the
  format. `results.mtx` is reserved. No other files inside a query directory
  (per-query descriptions live in `queries/README.md`).
- **`results.mtx`**: MatrixMarket pattern matrix, `|V| × |V|` of the graph;
  entry `(i, j)` present iff some path from node `i` to node `j` satisfies
  the query language. Identical for all representations of the query by
  construction (author responsibility — equivalence of CFLs is undecidable,
  so validation is structural only).

### `.rsm` file format — two description styles

Discriminator: a `[box <name>]` section header. Present → transition-system
style; absent → EBNF style (existing format, unchanged).

**Style A — EBNF** (existing `rsa_from_text`): one production per line,
RHS is a regular expression over terminals + nonterminals; start symbol is
`S` unless a `start: <N>` header line is given.

```
start: S
S -> a* b S c
B -> (x | y)+
```

**Style B — transition system** (new): explicit boxes as labelled graphs
with start and final states.

```
start: S
[box S]
start: 0
final: 2, 3
0 --a--> 1
1 --b--> 2
1 --c--> 3
[box B]
start: 0
final: 1
0 --x--> 1
```

- `start: <N>` — the start box (required in style B; optional in both styles,
  default `S`).
- States are arbitrary tokens, defined implicitly by use (start/final/
  transitions).
- Transition lists may be nondeterministic (NFA-style sugar; boxes are
  conceptually DFAs per the formal definition and are determinized
  internally by pyformlang).
- Labels are terminals or box names (nonterminals); multi-character labels
  are allowed.
- `rsa_to_text` keeps emitting style A — the canonical form; a style-B file
  round-trips to style-A text (documented).

### Validator rules (`utils/check_archive_structure.py`)

- `queries/<class>/` entries must be query directories (flat files are
  errors — the old layout is superseded).
- Per query directory: ≥ 1 representation file with a class-allowed
  extension; exactly one `results.mtx`; no other files.
- Representation files must parse (`cfg_from_text`, `rsa_from_text`,
  `regex_from_text`, `mcfg_from_text`) and use only labels present in the
  graph (for `.rsm`: box alphabets minus nonterminals).
- `rpq/*.rsm` regularity: no transition label equals a box name.
- `results.mtx`: MatrixMarket pattern matrix, dimensions equal to the graph
  node count, indices in range.
- `queries/README.md`: one section per query directory (existing check
  adapted from files to directories).
- Audit mode applies the same rules to the bucket.

### Docs

- `docs/graphs/index.rst` "File structure": new layout + `results.mtx`
  semantics.
- `docs/flpq.rst`: new "Recursive state machines" section — formalism
  (boxes, union alphabet, no stack; references: Alur et al. CAV 2001,
  arXiv:2312.11925), EBNF definition, CFG equivalence via `cfg_from_rsa`,
  the `.rsm` format spec (both styles), where `.rsm` is allowed + the
  regularity rule for `rpq/`.
- `docs/utils.rst`: validator rules updated.
- `.opencode/skills/add-graph/SKILL.md`: pointer update if it states layout
  details.

## Subtasks

- [x] **S1**: Record the user decisions verbatim in `tasks/tasks.md`; write
      this detailed plan. Commit `docs(54-S1)`.
- [ ] **S2**: Transition-system style for `.rsm` — extend
      `cfpq_data/grammars/readwrite/rsa.py`: `start:` header support,
      `[box]` dispatch in `rsa_from_text`, new `_rsa_from_transition_system`
      parser; doctests for both styles + round-trip; unit tests in
      `tests/grammars/test_rsa.py`. Commit `feat(54-S2)`.
- [ ] **S3**: Validator extension — query directories, representation rules
      per class, `results.mtx` checks, `rpq/*.rsm` regularity, README
      sections ↔ directories, audit mode; tests with fixture archives (valid
      + each failure mode). Commit `feat(54-S3)`.
- [ ] **S4**: Docs — File structure (`docs/graphs/index.rst`), RSM section +
      `.rsm` format spec (`docs/flpq.rst`), validator rules
      (`docs/utils.rst`), add-graph skill pointer. Commit `docs(54-S4)`.
- [ ] **S5**: Quality gate (canonical test command + coverage, pre-commit,
      ty, pyright, docs build), code review, mark done in the task log,
      merge to dev.

## Out of scope

- Re-uploading or migrating existing archives (task 48).
- `reachable_pairs.csv` redesign for per-query rows (task 48 — the unit
  becomes the query directory; documented here as the target state).
- A CFPQ solver / language-equivalence checking (structural checks only).
- Google Drive providing mechanism + templates (task 55).
