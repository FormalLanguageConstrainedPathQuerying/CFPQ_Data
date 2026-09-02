# Global Plan

## Tasks

| ID | Task | Branch | Depends on |
|----|------|--------|------------|
| 1 | Analyze existing tooling (deliverable: this plan + `tasks/tasks.md`) | `feature/001-analyze-existing-tooling` | — |
| 2 | Yandex S3 upload CLI tool: uploads a local file; credentials provided by the user from the CLI | `feature/002-yandex-s3-upload-tool` | 1 |
| 3 | Google Drive → Yandex S3 migration tool: one item at a time (download from Drive → upload via Task 2 tool → remove local copy); updates doc links; saves name→URL mapping | `feature/003-gdrive-to-s3-migration` | 2 |

Execution order: 1 → 2 → 3 (strict; Task 3 imports the upload core of Task 2).

## Existing Tooling Analysis (Task 1)

### Dataset download (public, no credentials)

- `cfpq_data/dataset/data.py` — `download`, `download_grammars`,
  `download_benchmark`. Streamed GET via `requests` from the public bucket
  URLs:
  - `DATASET_URL = https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/`
  - `GRAMMARS_URL = https://cfpq-data.storage.yandexcloud.net/4.0.0/grammar/`
  - `BENCHMARK_URL = https://cfpq-data.storage.yandexcloud.net/4.0.0/benchmark/`
- Bucket layout: `<major>.0.0/graph/<name>.tar.gz`,
  `<major>.0.0/grammar/[example/]<template>[_<graph>].tar.gz`,
  `<major>.0.0/benchmark/<name>.tar.gz`. The bucket is publicly readable
  (verified: HTTP 200 for existing objects, 404 for missing ones) — this
  makes upload verification and idempotency checks possible without
  credentials.

### Maintainer scripts (`utils/`, not part of the public API)

- `utils/fetch_dataset.py` — lists bucket objects with boto3 and rewrites the
  dataset table. **Broken as-is**: imports `AWS_ACCESS_KEY_ID`,
  `AWS_SECRET_ACCESS_KEY`, `BUCKET_NAME` from `cfpq_data.config`, where none
  of them exist, and `from config import MAIN_FOLDER` only works when the
  script directory is on `sys.path`. It also hardcodes `Bucket="cfpq-data"`
  while reading `BUCKET_NAME` for `head_object`.
- `utils/update_dataset_tables.py` — regenerates docs CSV tables from
  `DATASET`; same `from config import MAIN_FOLDER` pattern.
- `utils/config.py` — only `MAIN_FOLDER`.
- **boto3 is used but not declared** in `pyproject.toml` (any group). It is
  present in the base conda env (1.18.31) but not in the project venv.

### Google Drive usage

- All Drive links live in graph docs: `docs/graphs/data/*.rst`,
  `docs/old_graphs/data/*.rst`, and the index tables
  (`docs/graphs/index.rst`, `docs/old_graphs/index.rst`). **No grammar is on
  Drive** — all grammars are already on Yandex S3.
- 131 unique Drive file IDs in docs, of which 113 are "Direct download"
  archives (the rest are legacy `.txt`/`.xml.tar.gz` origin files). Per-file
  check against the public bucket (HEAD requests) shows:
  - 54 direct-download archives fully present on Yandex already (old
    collection).
  - **59 direct-download archives are Drive-only** — the migration scope:
    graphs from the new collections (java_points_to, field_sensitive_alias,
    provenance, name_resolution, unigraph).
- Name collisions: `cactus`, `imagick`, `leela`, `nab`, `omnetpp`, `parest`,
  `perlbench`, `povray`, `x264`, `xz` (10 names) each appear in both
  java_points_to and field_sensitive_alias with **different Drive file IDs**
  and different content (verified by SHA-256; resolved per Design Decision 3:
  suffixed keys, keep both).
- Verified Drive download protocol from this network:
  - small files: `GET https://drive.google.com/uc?export=download&id=<fid>`
    returns `application/octet-stream` directly;
  - large files: the same URL returns an HTML page with a form
    (`action=https://drive.usercontent.google.com/download`, hidden inputs
    `id`, `export=download`, `confirm=t`, per-download `uuid`); GETting that
    action with those params streams the file.

### Test/CI infrastructure

- pytest: `testpaths = ["cfpq_data", "tests"]`, `addopts = --doctest-modules`;
  tests mirror the package layout; no `conftest.py` anywhere.
- CI (`coverage.yml`): `poetry install --with dev,test`, `pip install .`,
  `pytest --cov=cfpq_data --doctest-modules cfpq_data tests`.
- Baseline on `dev`: **190 passed**.
- Pre-commit: black + pre-commit-hooks (end-of-file-fixer,
  trailing-whitespace, check-yaml, requirements-txt-fixer).

## Design Decisions

From user guidance (verbatim in `tasks/tasks.md`) and verified facts:

1. **S3 endpoint**: `https://s3.yandexcloud.net` (bucket: `cfpq-data`). The
   user answered "ru-central1" for the region, but the regional hostname form
   `s3.ru-central1.storage.yandexcloud.net` fails TLS validation from this
   network (certificate SANs cover `s3.yandexcloud.net`,
   `*.s3.yandexcloud.net`, `*.storage.yandexcloud.net` — no
   `s3.<region>.storage.yandexcloud.net`). Verified working: anonymous
   ListBucket and authenticated head_object against `https://s3.yandexcloud.net`
   (task 4). `--endpoint-url` remains overridable.
2. **Key layout**: flat, same as existing objects —
   `4.0.0/graph/<name>.tar.gz`. No per-collection subdirectories.
3. **Name collisions** (user): "Name is an unique identifier. If names are
   equal, graphs are the same. It must not be stored twice." Verified by
   SHA-256 of the downloaded archives: all 10 colliding names are different
   graphs (java_points_to vs field_sensitive_alias), so the assumption does
   not hold. User decision: "Suffixed keys, keep both (Recommended)" — the
   item whose docs page stem equals the name keeps `<name>.tar.gz`, the twin
   is stored under its docs page stem (`<name>_field_sensitive_alias.tar.gz`).
   The per-key SHA-256 check still guards re-uploads of an existing key.
4. **Scope**: only the 59 `.tar.gz` files (the 15 legacy `.txt` origin files
   are out of scope).
5. **Docs update is part of the migration**: after each successful upload the
   tool rewrites that item's `drive.google.com` links in the docs to the new
   Yandex URL, and saves the mapping graph name → new URL (with Drive file ID
   and SHA-256 for audit) to `utils/migration_mapping.json`.
6. **Credentials**: always from the CLI (`--access-key-id`,
   `--secret-access-key`), never stored in the repo or read from env/config.
7. **One item at a time**: download → (hash/dedup) → upload → verify → remove
   local copy → update docs/mapping. Never more than one item on disk.
8. **Idempotency**: before downloading, HEAD the public Yandex URL; if 200 the
   item is skipped (already migrated). Re-running the tool is safe.

## Shared Infrastructure

- `utils/upload_to_s3.py` (Task 2) exposes the importable core used by Task 3:
  - `create_s3_client(access_key_id, secret_access_key, endpoint_url)`
  - `upload_file(client, local_path, bucket, key)`
  - CLI entry point (`main`).
- Task 3 imports that core instead of duplicating S3 logic.
- `boto3` is declared once (Task 2) as a dev-group dependency and reused by
  both tools.

## Reuse Analysis (per `reusing` skill)

- Streaming-download pattern: reuse the approach of
  `cfpq_data/dataset/data.py` (`requests` + `shutil.copyfileobj`) for the
  Drive downloader; no new HTTP library.
- Name mapping for old-collection graphs: reuse `DATASET` from
  `cfpq_data.dataset` (rst stem ∈ DATASET ⇒ short key name); new collections
  use the "Full Name" field of the rst Info table.
- Item discovery source of truth: the docs themselves (single source of
  truth — no separate hardcoded item list).
- S3 access: reuse boto3 already used by `utils/fetch_dataset.py`; do not
  reimplement S3 signing with raw HTTP.
- No existing upload/migration code exists in `cfpq_data/` or `utils/` to
  generalize — new modules are justified.

## Conflicts / Overlaps

- Task 2 and Task 3 both touch `pyproject.toml` only in Task 2 (boto3);
  Task 3 adds no dependencies (`requests` already present).
- Task 3 rewrites `docs/**/*.rst` links **at runtime** (when the user runs
  the migration with credentials), not as repo changes committed by the tool
  itself; the committed repo state contains only the tool, its tests, and its
  docs page.

## Out of Scope / Follow-ups (not requested)

- Migrating the 15 legacy `.txt` origin files.
- Replacing stale Drive links of old-collection graphs that already exist on
  Yandex (their doc links predate the earlier migration).
- Fixing `utils/fetch_dataset.py` (broken imports) — separate task if wanted.
