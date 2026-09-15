.. _developer:

Developer guide
===============

.. only:: html

   :Release: |release|
   :Date: |today|

How to set up a development environment, run the checks that continuous
integration runs, and contribute to CFPQ_Data. If you only want to *use* the
package, start with :doc:`/getting_started` instead.

.. _developer-setup:

Development setup
-----------------

CFPQ_Data requires Python 3.11–3.13 (``pyproject.toml`` declares
``>=3.11,<3.14``). The canonical development environment is **Poetry** — all
CI workflows install their dependencies through it:

.. code-block:: bash

   poetry install --with dev,test,docs
   poetry run pip install .

- ``--with dev,test,docs`` pulls the three dependency groups from
  ``pyproject.toml``: developer tools (``black``, ``pre-commit``, ``pytest``,
  ``boto3``), test extras (``pytest-cov``, ``codecov``), and the Sphinx docs
  stack.
- The project is declared with ``package-mode = false``, so Poetry installs
  only the dependencies; ``poetry run pip install .`` then installs
  ``cfpq_data`` itself from :file:`setup.py`.
- ``requirements/*.txt`` hold pinned lists for pip-only installs; the Poetry
  groups in ``pyproject.toml`` are the source of truth.

.. _developer-precommit:

Pre-commit
----------

Formatting and hygiene checks run through ``pre-commit``. The hook list —
black formatting plus whitespace, YAML, and requirements-file fixers, and a
version-sync check that fails when :file:`cfpq_data/config.py` and
:file:`pyproject.toml` declare different versions — is defined in
:file:`.pre-commit-config.yaml`, which is the source of truth; do not
maintain a copy of it elsewhere.

Install the git hook once so the checks run on every commit::

   pre-commit install

Run the full pass manually (this is what CI does)::

   pre-commit run --all-files --color always --verbose --show-diff-on-failure

CI runs this full pass on every push and pull request
(:file:`.github/workflows/lint.yml`).

.. _developer-tests:

Test pipeline
-------------

The test suite is ``pytest`` with **doctests enabled**: the ``Examples``
sections of public docstrings are executed as tests, so the documented
behavior and the tested behavior are the same code. The canonical local
command (the one CI runs)::

   poetry run pytest --doctest-modules -vv -s cfpq_data tests

- Doctest discovery and test paths are configured in ``pyproject.toml``
  (``[tool.pytest.ini_options]``).
- ``tests/`` mirrors the package layout (e.g. ``tests/graphs/generators/``
  for ``cfpq_data/graphs/generators/``).

Continuous integration:

- :file:`.github/workflows/tests.yml` — runs the suite on every push and pull
  request across a matrix of Linux, macOS, and Windows with Python 3.11.
- :file:`.github/workflows/coverage.yml` — runs the same suite with
  ``--cov=cfpq_data`` and uploads the report to Codecov.

.. _developer-docs:

Docs build and deploy
---------------------

The documentation is built with Sphinx from the :file:`docs/` directory; the
canonical local instructions (installing the docs dependencies, building the
HTML, checking links) live in :file:`docs/README.md`. Two policies matter:

- **No-warnings policy.** The build runs with ``-W --keep-going`` (set in
  :file:`docs/Makefile`), so any Sphinx warning — including an unresolved
  cross-reference under ``nitpicky = True`` — fails the build. Fix warnings;
  do not suppress them.
- **Full link check.** ``sphinx-build -b linkcheck`` verifies every local
  target and external URL (two documented exceptions in
  :file:`docs/conf.py`); it exits non-zero on broken or timed-out links.

Both the build and the link check run in CI on every push and pull request
(:file:`.github/workflows/docs.yml`).

**Deployment.** Pushing to ``master`` deploys the site:
:file:`.github/workflows/deploy_docs.yml` builds the HTML and publishes
:file:`docs/_build/html` to the ``gh-pages`` branch, which GitHub serves as
the project website (https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data).
The workflow skips forks — it runs only for the owning repository.

.. _developer-release:

Package deploy
--------------

Cutting a release — version bump, changelog, ``vX.Y.Z`` tag, and the
automated PyPI publish (Trusted Publishing) plus dataset publishing — is
documented in :doc:`release`.

.. _developer-guidelines:

Contribution guidelines
-----------------------

Branching model
~~~~~~~~~~~~~~~

- ``dev`` — the stable development branch; all work merges here first.
- ``master`` — the protected release branch. A release merges ``dev`` into
  ``master`` via a pull request and then pushes a ``vX.Y.Z`` tag matching the
  package version (see :doc:`release`).
- ``feature/XXX-short-description`` — one feature branch per task; never
  combine multiple tasks in a single branch.

Commits
~~~~~~~

Conventional Commits with exactly one subtask identifier, one commit per
atomic subtask::

   feat(XXX-SN): description
   fix(XXX-SN): description
   docs(XXX-SN): description

``XXX`` is the task ID and ``SN`` a single subtask identifier (ranges or
lists are not allowed). Commit messages must explain *why* the change was
made, not only what it does.

Quality gate
~~~~~~~~~~~~

Before a feature branch merges to ``dev``, all of the following must pass —
no exceptions:

1. The full test suite: 0 failures, 0 skipped.
2. The full pre-commit pass: no errors.
3. The docs build: exit 0 under the no-warnings policy.
4. The link check: no broken or timed-out links.

Merge strategy
~~~~~~~~~~~~~~

Rebase the feature branch onto ``dev`` and fast-forward ``dev`` to it —
linear history, no squash, so every subtask commit keeps its own message.

Adding graphs and grammars
~~~~~~~~~~~~~~~~~~~~~~~~~~

New dataset entries follow the contribution templates in :file:`.github/`
(issue and pull-request templates for graphs and grammars); see the "How to
add a new graph?" section of the README.
