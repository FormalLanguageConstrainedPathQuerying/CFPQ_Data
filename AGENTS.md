# AGENTS.md

CFPQ_Data is a Python package (`cfpq_data`, Apache-2.0) providing Graphs and
Grammars for experimental analysis of Context-Free Path Querying (CFPQ)
algorithms. This file is an entrypoint/TOC only — details live in the skills
linked below.

## Package layout

- `cfpq_data/config.py` — version, data directories.
- `cfpq_data/dataset/` — dataset download (`download`, `download_grammars`,
  `download_benchmark`).
- `cfpq_data/graphs/` — `generators`, `readwrite`, `utils`.
- `cfpq_data/grammars/` — `generators`, `readwrite`, `converters`, `utils`.
- `tests/` mirrors the package structure (pytest + doctests).

## Skills

| Skill | When to use |
|---|---|
| `.opencode/skills/run-tests` | Running the test suite |
| `.opencode/skills/add-graph` | Adding a new graph to the dataset |
| `.opencode/skills/add-grammar` | Adding a new grammar template |
| `.opencode/skills/build-docs` | Building the Sphinx docs |
| `.opencode/skills/code-style` | Formatting / linting before commit |

Contribution templates (graphs/grammars) live under `.github/` and are the
source of truth for the required fields.
