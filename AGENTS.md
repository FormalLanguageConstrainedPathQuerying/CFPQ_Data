# AGENTS.md

FLPQ_Data is a Python package (`flpq_data`, Apache-2.0) providing Graphs and
Grammars for experimental analysis of Formal Language constrained Path
Querying (FLPQ) algorithms. It is both the dataset and the tools to support
and use it — extend, modify, validate.
This file is an entrypoint/TOC only — details live in the skills
linked below.

## Start here

At the start of every session, load the `workflow-management` skill
(`.opencode/skills/workflow-management/SKILL.md`) first, before doing anything
else. It drives the loop: plan → feature branch → subtasks → review → quality
gate → merge, and points to the other workflow skills below.

## Main Principles

* Documentation is about "What" and "Why". Skills are about "How".
* This file is a short entry point for fast cold errors-free start.
* Only one source of truth. No duplicates. Each thing (in both code, issues, pull request descriptions, and documentation) described exactly once. Use generalization (especially for code), cross-references, links, other similar techniques to avoid duplicates and reuse staff. Find what you can to reuse before creating new one.
* Source-of-truth hierarchy: code, scripts, CI configs > docs. If a fact can
  be extracted from code or scripts (e.g., CI configs), it is not duplicated
  in docs. Docs hold only what cannot be unambiguously reconstructed from
  code: design decisions, non-trivial constraints. Skills stay thin pointers
  to docs, code, or CI — they never re-describe them.
* Data archives are self-contained and must align with the checker
  (`flpq_data/tools/check_archive_structure.py`, console command
  `flpq-check-archive`) — the source of truth for any data structure.
* Tools, not instructions. If you can do something with existing tool --- do it. No thinking, no long instructions, no manual analysis. Do you want to analyze code coverage? Just run coverage tool and analyze report. No workaround for regular tasks. If there is a tool for regular task it must be installed and configured appropriately.
* Always learn, never forget — encode patterns before session ends
* Issues, pull requests, and their comments are a knowledge base of technical
  details. Log task-related findings and inspirations in the descriptions or
  comments of the respective issues/PRs. When faced with a problem, check
  whether a similar problem was solved or described previously — look for the
  solution in existing issues, PRs, and their comments first.

## Package layout

- `flpq_data/config.py` — version.
- `flpq_data/dataset/` — graph registry + metadata API, machine-global cache
  with lazy access (`graph_dir`), reachable-pair counts (`reachable_pairs`).
- `flpq_data/graphs/` — `generators`, `readwrite`, `converters`, `utils`.
- `flpq_data/queries/` — per-class query modules: `cfpq/` (`generators`,
  `readwrite`, `converters`, `utils`), `rpq/` (`readwrite`), `mcfpq/`
  (`readwrite`).
- `flpq_data/tools/` — the archive structure checker (console command
  `flpq-check-archive`).
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
| `.opencode/skills/release` | Cutting a release: version bump, changelog, tag, PyPI publish |

Contribution templates (graphs/grammars) live under `.github/` and are the
source of truth for the required fields.
