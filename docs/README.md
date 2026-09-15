# Building docs

We use Sphinx for generating the API and reference documentation.

## Instructions

Install the Python packages needed to build the documentation from the
Poetry docs group — the same one the CI workflows use::

    poetry install --with docs

in the root directory. (`requirements/docs.txt` is a pinned pip-only
fallback; the Poetry groups in `pyproject.toml` are the source of truth.)

To build the HTML documentation, enter::

    make html

in the ``doc/`` directory.  This will generate a ``build/html`` subdirectory
containing the built documentation.

The build runs with the no-warnings policy (``-W --keep-going`` in
``docs/Makefile``): any Sphinx warning — including an unresolved
cross-reference under ``nitpicky = True`` — fails the build and lists every
warning in one run. Fix the warnings; do not suppress them.

## Check links

To check that all links in the documentation resolve (local targets against
the filesystem, external URLs over HTTP), run from the repository root::

    sphinx-build -b linkcheck docs docs/_build/linkcheck

The check runs in full — no URL classes are skipped by default; see
``linkcheck_ignore`` in ``docs/conf.py`` for the two documented exceptions.
It is network-bound and slower than the HTML build. The command exits
non-zero if any link is broken or times out; redirects are reported but do
not fail the check.
