---
name: release
description: Use when cutting a CFPQ_Data release — bumping the version, finalizing the changelog, tagging, and publishing to PyPI. Covers the procedure and the automated publish workflow.
---

# Release

Cut a release of the `cfpq-data` package. The model, versioning policy, and
prerequisites are documented in `docs/release.rst` — do not duplicate them here.
Publishing is automated by `.github/workflows/publish.yml` (runs on a `v*` tag
push).

## Procedure

1. Bump the version and finalize the changelog:

   ```bash
   python utils/bump_version.py X.Y.Z
   ```

   Sets `config.py` + `pyproject.toml` to `X.Y.Z` and promotes the
   `[Unreleased]` changelog section to `## [X.Y.Z] - <today>`.
2. Verify the version guard passes:

   ```bash
   poetry run pre-commit run check-version-sync --all-files
   ```
3. Commit the bump (message: `chore: release X.Y.Z`).
4. Merge `dev` into `master` via a pull request (`master` is protected; do not
   squash). This also deploys the docs.
5. Tag the merged commit and push the tag:

   ```bash
   git fetch origin
   git tag -a vX.Y.Z -m "Release vX.Y.Z" origin/master
   git push origin vX.Y.Z
   ```
6. The `publish` workflow builds, publishes to PyPI (Trusted Publishing), and
   creates the GitHub Release. Verify on <https://pypi.org/project/cfpq-data/>.

## Notes

- **Major version bumps** also move the dataset prefix (`<major>.0.0/graph/`):
  upload/copy all archives with `utils/upload_to_s3.py` before pushing the tag.
  Minor/patch releases do not touch the dataset.
- Releasing is the deliberate exception to the "no push" convention (it merges
  to `master` and pushes a tag).
- First-time publishing needs PyPI access set up by an owner (Trusted
  Publishing or a token) — see `docs/release.rst`.
