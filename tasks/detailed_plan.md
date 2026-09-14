# Task 32: No-warnings policy for the docs build (fix all Sphinx warnings, no suppressions)

## Context

A clean docs build (`make clean && make html`, Sphinx 9.0.4) produced 247
warnings in 6 classes:

1. 84× `Invalid Babel locale: 'English'` — `language = "English"` is not a
   valid Babel locale code.
2. ~150× `py:class reference target not found: <Name>` for bare type names
   (`Path`, `MultiDiGraph`, `CFG`, `Variable`, `RSA`, `Regex`, `Symbol`,
   `integer`, `random_state`, `default`, ...) in API docstrings, plus one
   `py:exc ... NetworkXError`.
3. ~24× `py:obj reference target not found: <word>` for single-backticked
   prose in docstrings (`path`, `graph`, `range(n)`, `alpha`, `n`, `m`, ...).
4. 1× `py:func reference target not found: cfpq_data.materialize_grammar`
   (docs/indexed_grammars.rst:91 — wrong object path).
5. 1× autosummary ref to `cfpq_data.graphs.readwrite.mtx.MTX_HEADER`.
6. 4× `The topic/note element not yet supported in Markdown` (tutorial.rst,
   from nb2plots' notebook generation).

Additionally `suppress_warnings = ["ref.citation", "ref.footnote"]` hid two
warning classes whose origin had to be established.

## User decisions (verbatim)

"Cool. Yes, fix Babel warnings. Analyze rest warnings. E.g. why you suppress
aernings refs.citations and ref.footnote? Can we fix it and other warnings? I
want to set warings as errors and go to 'no warnings policy'. Without
suppresuins if possible."

"Well. Try to find solution that does not require workarounds or checkers
modification. If site o code refactoring required for this way, propose it to
me. It may be easier to do smoll refactoring, rather than add workaround. If
refactoring improve and simplify site and code, it is better that wotkaround
or tooling patching."

"9 approved. Go." (approval of the proposed plan incl. item 9: replace
tutorial.rst admonitions with plain paragraphs)

## Root causes (verified in Sphinx 9.0.4 / numpydoc 1.10.0 source and doctrees)

- **R1 (class 2):** both `sphinx.ext.napoleon` and `numpydoc` were enabled.
  Napoleon converted each numpy-style docstring to `:param:`/`:type:` fields;
  Sphinx's Python domain registers `type` as a *typed field*
  (`PyTypedField`, typerolename='class') and `rtype` with bodyrolename='class'
  (`sphinx/domains/python/_object.py`), so every type token became a
  `:py:class:` cross-reference. Bare names in docstrings (`Path`, `CFG`, ...)
  are not resolvable objects → warnings. Napoleon's own type conversion
  (`_convert_type_spec`) was not even active (`napoleon_preprocess_types`
  defaults to False) — the refs came from the domain's field handling of
  napoleon's output.
- **R2 (class 3):** single-backticked words in docstring prose are parsed
  with `default_role = "obj"` → `py:obj` references to non-objects.
- **R3 (class 5):** autosummary stubs under `docs/*/generated/` are
  build-generated and git-ignored (`autosummary_generate = True` regenerates
  them from module contents on every build). `MTX_HEADER` is a public-named
  module attribute not in `__all__`, so the generated stub listed it and
  referenced an object autodoc does not document. Editing the .rst is futile
  — the build overwrites it.
- **R4 (class 6):** nb2plots generates the downloadable notebook by
  converting the doctree to Markdown (`nb2plots/doctree2md.py`); its writer
  has no visitors for `topic`/`note` nodes → warning + content silently
  dropped from the notebook. Latest release is 0.7.2 (2023) — no upstream
  fix, so patching/vendoring nb2plots was rejected per user decision.
- **R5 (suppressions):** with napoleon removed and all refs fixed, removing
  `suppress_warnings` resurfaces nothing — the docstring footnote
  definitions (`.. [1]`) and references (`[1]_`) resolve within their own
  docstrings. The suppression was a leftover.

## Design decisions

### D1: Root-cause config fixes, no workarounds (per user decision)

- `language = "en"` (valid Babel code).
- Remove `sphinx.ext.napoleon`: numpydoc alone processes the numpy-style
  docstrings; with its default `numpydoc_xref_param_type = False`, docstring
  types render as plain text and create no references. Signature annotations
  are rendered by autodoc from the real code and still link via the existing
  intersphinx inventories (python, networkx, pyformlang). No alias tables,
  no second source of truth for type names. (An earlier alias-map variant was
  rejected as a workaround and reverted.)
- Remove `suppress_warnings = ["ref.citation", "ref.footnote"]` (R5).

### D2: Content fixes are the fix — no checker modification

Every remaining warning is a real content bug, fixed in place: literal
markup for prose (double backticks), a docstring type line corrected to match
the code, a private constant renamed private, a wrong object path corrected,
and admonitions replaced by plain RST that round-trips through nb2plots.

### D3: No-warnings policy = `-W --keep-going`, enforced by exit code

`docs/Makefile` sets `SPHINXOPTS = -W --keep-going`: any warning (including
unresolved refs under nitpicky) fails the build and all warnings are listed
in one run. CI drops its grep-based log inspection and relies on the exit
code; quality-gates/build-docs skills updated accordingly (no "tolerated
warnings").

## Subtasks

### S1: Fix the Babel locale [done]

`docs/conf.py`: `language = "English"` → `language = "en"`. Removes all 84
`Invalid Babel locale` warnings. Verified by clean rebuild.

### S2: Remove the redundant napoleon extension [done]

`docs/conf.py`: drop `"sphinx.ext.napoleon"` from `extensions`. Napoleon
double-processed every docstring together with numpydoc and its `:type:`
fields are what made the Python domain create ~150 broken `py:class` refs
(R1). With numpydoc alone, docstring types are plain text (its default) and
signature annotations still link via intersphinx. Verified by clean rebuild:
all class-2 warnings gone.

### S3: Remove the leftover warning suppressions [done]

`docs/conf.py`: delete `suppress_warnings = ["ref.citation", "ref.footnote"]`.
Verified by clean rebuild: no citation/footnote warnings resurface (R5) —
docstring footnotes resolve within their own docstrings.

### S4: Fix literal markup and a wrong type line in docstrings [done]

- Double backticks (literal, not cross-reference) for prose words that were
  single-backticked and thus became broken `py:obj` refs under
  `default_role = "obj"`: `cfpq_data/graphs/readwrite/{rdf,mtx,csv}.py`
  (`graph`, `path`), `cfpq_data/grammars/readwrite/cnf_template.py` (`path`),
  `cfpq_data/graphs/generators/labeled_two_cycles_graph.py` and
  `labeled_cycle_graph.py` (`range(n)`), `labeled_scale_free_graph.py`
  (`alpha`, `beta`, `gamma`), `labeled_barabasi_albert_graph.py` (`n`, `m`).
- `labeled_barabasi_albert_graph.py`: docstring said
  `seed : Union[int, RandomState, None]` but the code uses stdlib
  `random.seed(seed)` and the signature is `seed: Union[int, None]` →
  corrected to `seed : int or None`.

### S5: Make MTX_HEADER private [done]

`cfpq_data/graphs/readwrite/mtx.py`: rename `MTX_HEADER` → `_MTX_HEADER`
(definition + 2 uses). It is not in `__all__` — an internal constant. The
autosummary stub (build-generated, git-ignored) listed it because it was
public-named; the private name removes it from the generated reference and
the broken autosummary ref (R3).

### S6: Fix the broken materialize_grammar reference [done]

`docs/indexed_grammars.rst`: `:func:`cfpq_data.materialize_grammar`` →
`:func:`cfpq_data.grammars.readwrite.cnf_template.materialize_grammar``
(the function's real location).

### S7: Replace tutorial admonitions with plain paragraphs [done]

`docs/tutorial.rst`: the 2× `.. topic::` + 1× `.. note::` blocks became plain
paragraphs with bold lead-ins. nb2plots cannot represent admonitions in the
generated notebook's Markdown (R4) — it warned and dropped the content; plain
RST round-trips, so the text now appears in both the HTML page and the
downloadable notebook.

### S8: Enforce the no-warnings policy [done]

- `docs/Makefile`: `SPHINXOPTS = -W --keep-going` (any warning fails the
  build; all warnings reported in one run).
- `.github/workflows/docs.yml`: Build and Check links steps now rely on the
  exit code; the grep-based log inspection is removed.
- `docs/README.md`, `.opencode/skills/build-docs/SKILL.md`,
  `.opencode/skills/quality-gates/SKILL.md`: document the policy — no
  tolerated warnings, fix instead of suppress.

Verified: a deliberately broken `:obj:` ref makes `make html` exit 1; a clean
tree exits 0 with zero warnings.

### S9: Update task records [done]

`tasks/tasks.md` (task logged) and this plan.

## Verification (quality gate, all PASS)

- Tests: `poetry run pytest --doctest-modules -q cfpq_data tests` → 342 passed.
- Style: `pre-commit run --all-files` → all hooks passed.
- Docs build: `make -C docs/ clean && make -C docs/ html` (with `-W
  --keep-going`) → exit 0, zero warnings.
- Link check: `sphinx-build -b linkcheck docs docs/_build/linkcheck` → exit 0,
  no broken links (one transient github.com 504 passed on retry).
