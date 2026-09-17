# Building docs

We use Sphinx for generating the API and reference documentation.

## Instructions

Install the Python packages needed to build the documentation from the uv
`docs` dependency group — the same one the CI workflows install::

    uv sync --only-group docs

in the root directory.

To build the HTML documentation, run from the repository root::

    uv run make -C docs html

This will generate a ``docs/_build/html`` subdirectory containing the built
documentation.

The build runs with the no-warnings policy (``-W --keep-going`` in
``docs/Makefile``): any Sphinx warning — including an unresolved
cross-reference under ``nitpicky = True`` — fails the build and lists every
warning in one run. Fix the warnings; do not suppress them.

## Check links

To check that all links in the documentation resolve (local targets against
the filesystem, external URLs over HTTP), run from the repository root::

    uv run sphinx-build -b linkcheck docs docs/_build/linkcheck

The check runs in full — no URL classes are skipped by default; see
``linkcheck_ignore`` in ``docs/conf.py`` for the two documented exceptions.
It is network-bound and slower than the HTML build. The command exits
non-zero if any link is broken or times out; redirects are reported but do
not fail the check.
