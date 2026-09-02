# AGENTS.md

CFPQ_Data is a Python package (`cfpq_data`, Apache-2.0) providing Graphs and
Grammars for experimental analysis of Context-Free Path Querying (CFPQ)
algorithms. This file is an entrypoint/TOC only — details live in the skills
linked below.

## Start here

At the start of every session, load the `workflow-management` skill
(`.opencode/skills/workflow-management/SKILL.md`) first, before doing anything
else. It drives the loop: plan → feature branch → subtasks → review → quality
gate → merge, and points to the other workflow skills below.

## Main Principles

* Documentation is about "What" and "Why". Skills are about "How".
* This file is a short entry point for fast cold errors-free start.
* Only one source of truth. No duplicates. Each thing (in doth code and documentation) described exactly once. Use generalization (especially for code), cross-references, links, other similar techniques to avoid duplicates and reuse staff.
* Tools, not instructions. If you can do something with existing tool --- do it. No thinking, no long instructions, no manual analysis. You want to analyze code coverage? Just run coverage tool and analyze report.
* Always learn, never forget — encode patterns before session ends

## Package layout

- `cfpq_data/config.py` — version, data directories.
- `cfpq_data/dataset/` — dataset download (`download`, `download_grammars`,
  `download_benchmark`).
- `cfpq_data/graphs/` — `generators`, `readwrite`, `utils`.
- `cfpq_data/grammars/` — `generators`, `readwrite`, `converters`, `utils`.
- `tests/` mirrors the package structure (pytest + doctests).

## Skills

### Domain

| Skill | When to use |
|---|---|
| `.opencode/skills/run-tests` | Running the test suite |
| `.opencode/skills/add-graph` | Adding a new graph to the dataset |
| `.opencode/skills/add-grammar` | Adding a new grammar template |
| `.opencode/skills/build-docs` | Building the Sphinx docs |
| `.opencode/skills/code-style` | Formatting / linting before commit |

### Workflow / process

| Skill | When to use |
|---|---|
| `.opencode/skills/workflow-management` | Driving the overall task loop |
| `.opencode/skills/planning` | Global plans, atomic subtasks, task authoring |
| `.opencode/skills/subtask-loop` | Executing one atomic subtask |
| `.opencode/skills/git-workflow` | Branching, commits, merging |
| `.opencode/skills/reusing` | Finding existing code/docs to reuse, not duplicate |
| `.opencode/skills/user-guidance-transfer` | Recording user guidance verbatim |
| `.opencode/skills/documentation` | Mapping code changes to doc updates |
| `.opencode/skills/quality-gates` | The pre-merge gate that must pass |
| `.opencode/skills/code-review` | Whole-repo review before merge |

Contribution templates (graphs/grammars) live under `.github/` and are the
source of truth for the required fields.
