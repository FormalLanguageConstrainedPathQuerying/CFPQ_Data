.. _contributing_data:

=================
Contributing data
=================

.. only:: html

   :Release: |release|
   :Date: |today|

New data — graphs, queries, grammars — enters the dataset through a single
`"CONTRIBUTE NEW DATA" issue <https://github.com/FormalLanguageConstrainedPathQuerying/FLPQ_Data/blob/dev/.github/ISSUE_TEMPLATE/new-data-template.md>`_:
you prepare one or more archives (one graph each), validate them, publish
them (e.g. to Google Drive), and open the issue with the links, the
validation output, the SHA256 of every archive, and the motivation. The
maintainers upload the archives and merge them into the dataset — no pull
request is needed. Every archive must follow the layout documented in
:ref:`file_structure`.

Contribution cases
------------------

The issue template's "Contribution type" section lists the four contribution
cases — new graph(s) for an existing or a new category, with an existing or
a new grammar, and new queries for existing graph(s) — and what each
requires; its remaining sections carry every required field (statistics,
grammar definitions, category description). A set of graphs for a category
goes into one issue as several archives (one graph per archive).

Validation
----------

Every archive must pass the structure checker before it is shared::

   flpq-check-archive <name>.tar.gz            # full archive
   flpq-check-archive <name>.tar.gz --partial  # partial archive

The issue carries the pasted output of this command per archive, the
archive's SHA256, and the FLPQ_Data version used; the template has the
recipe — ``pip install flpq-data`` installs the checker.

Consistency invariants
----------------------

- No graph without at least one query.
- No query without reference results (``results.mtx``).
- No item without description and motivation: every graph is described in
  its archive ``README.md``, every query in ``queries/README.md``, and the
  issue states why each new graph, grammar, or category is useful to other
  users.

Not accepted via this flow
--------------------------

The issue template's "Not accepted via this flow" section lists the declined
cases: a grammar or query provided outside an archive (without reference
results), updates to an existing graph, a new representation of an existing
query, and more than one graph inside a single archive.

Grammars
--------

Grammars are added together with the data they apply to — the template's
"Queries and grammars" section carries their definitions. A grammar is
accepted only if it is instantiated as at least one query with reference
results in a contributed archive.
