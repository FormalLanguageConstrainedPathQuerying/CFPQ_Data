.. _release:

Release process
===============

.. only:: html

   :Release: |release|
   :Date: |today|

A release publishes two things: the ``cfpq-data`` **package** on PyPI and the
**dataset** served from Yandex Object Storage. This page describes the model;
the step-by-step procedure lives in the ``release`` skill.

Versioning
----------

- Versions follow `Semantic Versioning <https://semver.org/>`_.
- The canonical version is ``VERSION`` in :file:`cfpq_data/config.py`.
  ``pyproject.toml`` must declare the same value; a pre-commit hook
  (``check-version-sync``) and CI fail on a mismatch.
- Releases are tagged ``vX.Y.Z`` (e.g. ``v5.0.0``). The tag must match the
  package version — the publish workflow verifies this before building.
- Notable changes are recorded in :file:`CHANGELOG.md` (Keep a Changelog).

Package publishing (automated)
------------------------------

The ``publish`` workflow (``.github/workflows/publish.yml``) runs when a
``v*`` tag is pushed:

1. Verifies the tag matches the package version.
2. Builds the sdist and wheel (``python -m build``).
3. Publishes to PyPI via **Trusted Publishing** (OIDC) — no stored token; a
   ``PYPI_API_TOKEN`` secret is supported as a fallback.
4. Creates a GitHub Release with the matching changelog section.

A manual **TestPyPI** run is available from *Actions → Publish → Run workflow*
(uses a ``TEST_PYPI_API_TOKEN`` secret) to validate before a real release.

Prerequisites (one-time, owner action)
--------------------------------------

Publishing requires PyPI access. The ``cfpq-data`` project owners must either:

- configure **Trusted Publishing** on PyPI for this repository and the
  ``publish.yml`` workflow (recommended — no long-lived secret), or
- add the releasing user as an owner / provide a ``PYPI_API_TOKEN``.

Releasing also means pushing: a release merges ``dev`` into the protected
``master`` branch via a pull request, then pushes the version tag. This is the
deliberate exception to the normal "no push" development convention.

Dataset publishing
------------------

The dataset is versioned by the package **major** version and served from
``https://cfpq-data.storage.yandexcloud.net/<major>.0.0/graph/``.

- A **minor/patch** release does not change the dataset prefix — nothing to do.
- A **major** release changes the prefix, so all graph archives must be
  uploaded (or copied server-side) to the new ``<major>.0.0/graph/`` prefix
  using :file:`utils/upload_to_s3.py` before the tag is pushed.
