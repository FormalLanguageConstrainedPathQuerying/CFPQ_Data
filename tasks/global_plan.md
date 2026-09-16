# Global Plan: Tasks 34-35 (v5.0.0 release preparation)

## Tasks

- **Task 34**: Add references to the resolved issues (#122, #76, #75, #74,
  #28 sub-items, #26, #16, #2 partial) to the `[Unreleased]` section of
  `CHANGELOG.md`. The resolution analysis is recorded in the detailed plan.
- **Task 35**: Cut the v5.0.0 release per the `release` skill: promote the
  changelog via `utils/bump_version.py 5.0.0`, commit, push `dev`, open a PR
  `dev` -> `master` (reviewed and merged **manually by the user**), then — only
  after the user confirms the merge — fetch origin, tag `v5.0.0` on
  `origin/master`, push the tag, and verify the automated PyPI publish and
  GitHub Release.

## Dependencies

- **34 -> 35**: the changelog must be finalized before `bump_version.py`
  promotes `[Unreleased]` to `[5.0.0]`; otherwise the release notes would miss
  the issue references.

## Verified facts (analysis of 2026-09-16, on `dev`)

### Issue resolution status

| Issue | Status | Evidence |
|---|---|---|
| #122 broken function doc links on the Graphs page | resolved | task 31 (commit 8485b56); explicit `:obj:` roles at `docs/graphs/index.rst:43,62`; systematic prevention: nitpicky + no-warnings build + linkcheck in CI and the quality gate |
| #76 developer docs | resolved | task 33; `docs/developer.rst` covers all five requested areas (pre-commit, test pipeline, docs deploy, package deploy, guidelines); README "For developers" section |
| #75 release pipeline documentation | resolved (nuance) | task 24; `docs/release.rst` + `.github/workflows/publish.yml`; TestPyPI validation is a manual `workflow_dispatch` run, not an automatic per-PR release |
| #74 docs prebuild for PR | resolved | `.github/workflows/docs.yml` on `[push, pull_request]`: no-warnings build + full linkcheck |
| #26 data from "Subgraph Queries by Context-free Grammars" | resolved | `docs/graphs/biological_uniprot.rst` cites exactly that paper; 10 UniProt graphs |
| #16 data for data provenance | resolved | `docs/graphs/data_provenance.rst`: 18 W3C-PROV graphs, cites the issue's first reference |
| #2 static code analysis cases | **partial** | Zheng & Rugina "Demand-driven Alias Analysis for C" -> `c_alias_analysis` category (20 graphs); Vedurada "Batch Alias Analysis" (ASE 2019) -> no trace in the repo |
| #28 umbrella "Make CFPQ_Data better. Again." | **7 of 8 sub-items** | resolved: #27 (networkx generators; GTgraph only a stale `.gitignore` line), PR #24 (merged long ago), #32 (reachable-pair reference values, tasks 26/28), #20 (Num Nodes/Num Edges columns), #30 (six labeled generators), #33 (release process, task 24), #26; open: the Vedurada part of #2 |

### Release mechanics

- Version is already `5.0.0` in `cfpq_data/config.py` and `pyproject.toml`
  (task 15); `utils/bump_version.py 5.0.0` is idempotent for the version
  fields and only promotes `[Unreleased]` -> `## [5.0.0] - <date>`.
- The dataset is already served from the `5.0.0/graph/` prefix (tasks 19/20) —
  a major release needs no re-upload.
- **Trusted Publishing for PyPI was configured by the user** (repository
  `FormalLanguageConstrainedPathQuerying/CFPQ_Data`, workflow `publish.yml`);
  no token needed for the real publish.

## Human gates (task 35)

1. The user reviews and merges the `dev` -> `master` PR manually. Nothing is
   tagged or pushed before the user confirms the merge.
2. The tag is created on `origin/master` after a fresh `git fetch origin`, so
   it points at the merged commit.

## Conflicts / overlapping changes

- Both tasks touch `CHANGELOG.md`: task 34 edits `[Unreleased]`, task 35
  promotes it — strictly sequential, 34 first.
- No other file overlaps; no code changes in either task (task 35 runs the
  existing `bump_version.py`).

## Execution order: 34 -> 35
