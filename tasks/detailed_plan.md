# Detailed Plan: Task 44 — MCFG readwrite module with lark

Task (recorded in `tasks/tasks.md`): "MCFG readwrite module with lark:
`cfpq_data/grammars/readwrite/mcfg.py` (data model, EBNF grammar, validation
per the spec in `docs/flpq.rst`, `mcfg_from_text/to_text/from_txt/to_txt`),
doctests with the paper's examples, reference docs page."

Scope (per `docs/flpq.rst` "MCFG grammar format (.mcfg)" and
`tasks/global_plan.md`): a new formalism-based readwrite module for the
`.mcfg` Datalog-like syntax. The format spec — lexical conventions, rule
forms, validation constraints, and the two literature examples — lives in
`docs/flpq.rst`; this plan does not re-describe it, only the implementation
decisions below.

Verified facts this plan builds on (checked against the repo, 2026-09-21):
- `lark` is NOT a dependency yet; it must be added to `[project]
  dependencies` in `pyproject.toml` (runtime dependency of the reader) via
  `uv add lark`, which also updates `uv.lock`.
- No pyformlang type exists for MCFGs (verified in task 42), so the data
  model is defined in `mcfg.py` itself.
- Module conventions (from `regex.py`/`cnf.py`): module docstring "Read (and
  write) a ... from (and to) different sources."; `__all__`; numpydoc
  docstrings with Parameters/Examples/Returns/References (Examples run as
  doctests via `--doctest-modules`); `logging.info` per public function;
  file paths typed `Union[pathlib.Path, str]`; doctests import via
  `from cfpq_data import *`.
- Invalid input raises `ValueError` with a descriptive f-string (pattern of
  `cnf_template.py`). Syntax errors surface as lark's `UnexpectedInput`.
- Exports: `cfpq_data/grammars/readwrite/__init__.py` re-exports each module
  via `from ... import *` in alphabetical order (cfg, cnf, cnf_template,
  regex, rsa) — `mcfg` slots between `cnf_template` and `regex`. The top
  level (`cfpq_data/__init__.py`) already re-exports the whole chain.
- Tests mirror the package: `tests/grammars/readwrite/test_mcfg_readwrite.py`
  (siblings: test_cfg/cnf/cnf_template/regex/rsa).
- Docs: `docs/reference/grammars/grammars_readwrite.rst` lists the modules
  in an autosummary toctree; the per-module stubs under
  `docs/reference/grammars/generated/` are produced by
  `autosummary_generate = True` at build time and committed (pattern of
  `cfpq_data.grammars.readwrite.regex.rst`).

Design decisions (implementation-level; the format itself is fixed by
`docs/flpq.rst`):

1. **Data model** — two frozen dataclasses in `mcfg.py`:
   - `MCFGRule`: `head: str` (nonterminal), `head_args: tuple[tuple[str,
     ...], ...]` (each argument is a sequence of tokens — terminals,
     variables, or the literal `"eps"`), `body: tuple[tuple[str,
     tuple[str, ...]], ...]` (atoms; empty for basic rules). A *basic rule*
     is a production with an empty body — one representation, no separate
     class.
   - `MCFG`: `rules: tuple[MCFGRule, ...]`, `start_symbol: str`; properties
     `dimension` (max nonterminal arity) and `rank` (max number of body
     atoms) computed from the rules (the file carries no header).
2. **Parser** — lark with `parser="lalr"`. The LALR contextual lexer makes
   `#` context-sensitive without preprocessing: a `COMMENT` token
   (`/#[^\n]*/`) is only valid between rules (top level), while inside
   argument lists `#` matches the catch-all `TERMINAL` token — required by
   the spec's example `S(x1 y1 # y2 x2)`. Token priorities break the other
   ambiguities: `EPS`/`VARIABLE`/`NONTERMINAL` outrank `TERMINAL`, so
   `eps`, `x1`, and uppercase identifiers never lex as terminals.
   `NONTERMINAL: /[A-Z]\w*/`, `VARIABLE: /x[0-9]+/`, `EPS: /eps/`,
   `TERMINAL: /[^ \t\r\n#(),<>-]+/` (structural characters cannot appear in
   terminals — inherent to the chosen syntax). Whitespace is ignored via
   `%ignore /[ \t\r\n]/`; comments are explicit grammar tokens.
2a. **Variable pattern correction** — `docs/flpq.rst` says variables are "``x``
   followed by one or more digits", but its own literature example uses
   ``y1``/``y2`` as body variables (`S(x1 y1 # y2 x2) <- A(x1, x2),
   A(y1, y2)`), which is unparseable under the strict `x\d+` pattern. The
   pattern is implemented as **one lowercase letter followed by one or more
   digits** (`[a-z][0-9]+`) — exactly the literature's `x^i`, `y^j`
   notation — and the spec line in `docs/flpq.rst` is corrected to match.
   No dataset label collides: the terminal vocabularies are `0`/`1`/`#`,
   `a`/`a_r`/`d`/`d_r`, `load_*`/`store_*`, `subClassOf`-style words — none
   matches `[a-z][0-9]+`.
3. **Validation** (semantic, on the parsed model; syntax errors are lark's):
   - arity consistency across every occurrence of a nonterminal;
   - body variables pairwise distinct per rule;
   - no dangling variables in both directions: the set of head-template
     variables equals the set of body variables, and each appears exactly
     once across the head templates (the strict form every published
     example satisfies);
   - `eps` only in basic rules (empty body) — production templates mix
     terminals and variables, and `eps` is neither;
   - a "terminal" matching `x\d+` can never be one: it lexes as a variable,
     so such a label is rejected wherever a variable is not allowed (basic
     rules) or leaves the rule dangling-variable-inconsistent;
   - the start symbol (default `"S"`, overridable via keyword parameter like
     the `cnf`/`cfg`/`rsa` readers) must occur in the grammar with arity 1.
   All violations raise `ValueError` naming the offending rule/symbol.
4. **Canonical rendering** (`mcfg_to_text`): one rule per line, basic rules
   as `A(eps, eps)`, productions as `S(x1 y1 # y2 x2) <- A(x1, x2),
   A(y1, y2)`; argument tokens space-joined, empty argument list rendered
   `()`. Round-trip: `mcfg_to_text(mcfg_from_text(t))` reproduces `t` up to
   whitespace/comment normalization.

### S1: Record the task and add the lark dependency

**Code:** `pyproject.toml` + `uv.lock` via `uv add lark` (runtime
dependency). No package code yet.
**Tests:** none new — the existing suite must stay green under `uv sync`
with the new lock; `uv run python -c "import lark"` resolves.
**Docs:** `tasks/tasks.md` (task 44 recorded with user guidance),
`tasks/global_plan.md` (coverage task added as task 45, tasks 45-49
renumbered to 46-50, dependencies updated).

**Spec:**
- `lark` lands in `[project] dependencies` (not a dev/test group — the
  reader imports it at runtime), version-pinned like the other dependencies.
- `uv.lock` regenerated; `uv sync --frozen` passes (the CI check).

### S2: Data model, lark EBNF grammar, and syntax-level parsing

**Code:** new `cfpq_data/grammars/readwrite/mcfg.py`: the `MCFGRule` and
`MCFG` frozen dataclasses (decision 1), the lark EBNF grammar as a module
constant (decisions 2/2a), and `mcfg_from_text(text: str) -> MCFG` parsing
to the model. `__all__ = ["MCFG", "MCFGRule", "mcfg_from_text"]`.
`cfpq_data/grammars/readwrite/__init__.py` gains the `mcfg` re-export in
alphabetical position (the module is part of the package from birth, so
doctests can use `from cfpq_data import *` immediately).
**Tests:** new `tests/grammars/readwrite/test_mcfg_readwrite.py`: both
literature examples from `docs/flpq.rst` parse into the expected models
(rule count, head/args/body structure, start symbol default); comments and
blank lines are ignored; a `#` terminal inside arguments parses; `y1`-style
variables parse (decision 2a); malformed syntax (missing arrow, unbalanced
parens, lowercase "nonterminal" head, dangling comma) raises lark's
`UnexpectedInput`.
**Docs:** numpydoc docstrings with `Examples` for the public names (the
paper's 2-MCFG(2) example); `docs/flpq.rst` variable line corrected per
decision 2a; no reference page yet (S5).

**Spec:**
- The grammar constant is the executable documentation of the syntax
  (decisions 2/2a); it accepts exactly the spec's lexical conventions.
- `mcfg_from_text` performs NO semantic validation in this subtask — a
  syntactically valid but semantically broken rule set parses fine (S3
  adds the checks). Tests assert that explicitly.

### S3: Semantic validation, start symbol, dimension and rank

**Code:** extend `mcfg.py`: validation pass (decision 3) invoked by
`mcfg_from_text`, now with signature `mcfg_from_text(text: str, *,
start_symbol: str = "S") -> MCFG`; `MCFG.dimension` / `MCFG.rank`
properties; `logging.info` reporting the created grammar with its
dimension/rank (pattern of the other readers).
**Tests:** extend `test_mcfg_readwrite.py`: each constraint violated in
turn raises `ValueError` with a message naming the offender — arity
mismatch, duplicate body variable, body variable missing from the head,
head variable missing from the body, a body variable twice in the head,
`eps` in a production template, start symbol absent, start symbol of
wrong arity, custom `start_symbol=` accepted; both literature examples
report dimension/rank (2-MCFG(2): d=2, r=2; the dimension-1 example:
d=1, r=2).
**Docs:** docstrings updated for the new parameter and properties.

**Spec:**
- Validation runs after parsing, before the `MCFG` is constructed; on
  failure nothing but the `ValueError` escapes.
- `dimension`/`rank` are computed from the rules (no stored header), per
  the spec: d = max nonterminal arity, r = max number of body atoms.

### S4: Writers — to_text / from_txt / to_txt and round-trips

**Code:** extend `mcfg.py`: `mcfg_to_text(mcfg: MCFG) -> str` (canonical
rendering, decision 4), `mcfg_from_txt(path, *, start_symbol="S") -> MCFG`,
`mcfg_to_txt(mcfg, path) -> pathlib.Path`; `__all__` completed.
**Tests:** extend `test_mcfg_readwrite.py`: round-trip
`mcfg_to_text(mcfg_from_text(t)) == t` for both literature examples (and a
grammar exercising `()`, multi-token arguments, and `#`); `from_txt`/
`to_txt` via `tmp_path` (pattern of the regex tests); doctests in the
docstrings use the paper's examples end to end.
**Docs:** docstrings with `Examples` for all four public functions.

**Spec:**
- The rendering is canonical: the same model always produces the same text,
  so round-trips are stable and diffs are meaningful.
- `mcfg_to_txt` returns the resolved `pathlib.Path` (pattern of
  `regex_to_txt`).

### S5: Reference docs page

**Code:** none (the module was exported from S2).
**Tests:** the full suite green, including all mcfg doctests discovered via
`--doctest-modules`; `from cfpq_data import *` exposes `MCFG`, `MCFGRule`,
and the four functions (asserted in a test).
**Docs:** `docs/reference/grammars/grammars_readwrite.rst` — add `mcfg` to
the autosummary list; run the docs build so the per-module stub
`docs/reference/grammars/generated/cfpq_data.grammars.readwrite.mcfg.rst`
is generated (the `generated/` stubs are gitignored and regenerated on
every build — only the hand-written `.rst` files are tracked).

**Spec:**
- The docs build passes under `-W --keep-going` with zero warnings
  (nitpicky: every cross-reference in the new docstrings resolves).
