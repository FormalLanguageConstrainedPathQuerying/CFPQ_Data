.. _utils:

Maintainer tools
================

.. only:: html

   :Release: |release|
   :Date: |today|

The ``utils/`` directory contains maintainer scripts for managing the dataset
stored on Yandex Object Storage (bucket ``cfpq-data``, S3 API). They are not
part of the public ``cfpq_data`` package.

.. _upload_to_s3:

Upload to Yandex S3
-------------------

``utils/upload_to_s3.py`` uploads a local file to the bucket::

   python utils/upload_to_s3.py FILE \
       --access-key-id KEY_ID --secret-access-key SECRET \
       [--endpoint-url URL] [--bucket BUCKET] [--key KEY]

- ``FILE`` — path to the local file to upload.
- ``--access-key-id``, ``--secret-access-key`` — Yandex Cloud IAM service
  account credentials. They are always taken from the command line and are
  never read from environment variables or config files.
- ``--endpoint-url`` — S3 API endpoint; default
  ``https://s3.yandexcloud.net`` (the verified working endpoint for the
  cfpq-data bucket).
- ``--bucket`` — target bucket; default ``cfpq-data``.
- ``--key`` — object key in the bucket; default is the file name (e.g.
  ``6.0.0/graph/NAME.tar.gz`` to follow the dataset layout).

Before uploading any ``.tar.gz`` the tool validates it as a graph archive
(:ref:`archive_structure`) and refuses an invalid one; after the upload it
verifies that the stored object size equals the local file size and reports
an error otherwise. The verified size is then reported in bytes and
megabytes, with the same MB formatting as the ``Size (MB)`` column of the
graph tables, so a new graph's table row can be
filled directly from the upload output.

.. _archive_sizes:

Archive sizes
-------------

``utils/archive_sizes.py`` keeps the ``Size (MB)`` column of the graph tables
in sync with the stored archives::

   python utils/archive_sizes.py [--update]

The tool covers every list-table with a ``Download`` column in
``docs/graphs/*.rst`` and ``docs/old_graphs/index.rst`` — currently the eight
per-category tables (113 archives at the ``6.0.0/graph/`` prefix) and the
old-graphs table (54 archives at the ``4.0.0/graph/`` prefix). For every
referenced archive it issues an S3 ``HEAD`` request and compares the
``Content-Length`` with the table cell, formatted in MB (three decimals below
one megabyte, two from one up — the rule lives in ``utils/sizes.py`` and is
shared with :ref:`upload_to_s3`).

Behavior:

- **Check mode (default).** Reports every row whose size cell disagrees with
  the stored object (or a missing column or link) and exits non-zero, so it
  can gate a commit.
- **``--update``.** Fetches all sizes first, then rewrites the tables —
  inserting the ``Size (MB)`` column before ``Download`` where it is missing
  and fixing drifted cells. All-or-nothing: if any archive cannot be fetched,
  nothing is written.
- **URL keying.** Sizes are keyed by full URL, not archive name: the
  ``4.0.0``, ``5.0.0``, and ``6.0.0`` prefixes hold same-named archives with
  different content.

When adding a new graph, upload it first (:ref:`upload_to_s3` prints the
verified size), add the table row with that value, and run this tool before
committing so every row — including the new one — matches S3.

.. _archive_structure:

Archive structure
-----------------

``utils/check_archive_structure.py`` validates that a graph archive has the
fixed self-contained structure documented in the "File structure" section of
the :ref:`graphs` page::

   python utils/check_archive_structure.py ARCHIVE.tar.gz
   python utils/check_archive_structure.py UNPACKED_DIR
   python utils/check_archive_structure.py PARTIAL.tar.gz --partial
   python utils/check_archive_structure.py --audit --prefix 6.0.0/graph/ \
       --access-key-id KEY_ID --secret-access-key SECRET

A **partial archive** provides new queries for an existing graph: it contains
only ``queries/`` — the new query directories plus a ``README.md`` fragment
with their sections. With ``--partial`` the tool checks that skeleton, that
every representation file parses (the label and dimension checks are skipped
— there is no graph to check against), and that the fragment describes
exactly the query directories it contains.

The checks:

- **Skeleton.** A single top-level directory named after the archive,
  containing exactly ``README.md``, ``graph/`` (non-empty, only ``.mtx``
  files), and ``queries/`` with its ``README.md`` and the three class
  directories. Each class directory holds query directories only (flat query
  files are rejected); each query directory contains at least one
  representation file with a class extension (``.cnf``/``.rsm`` for CFPQ,
  ``.re``/``.rsm`` for RPQ, ``.mcfg`` for MCFPQ) and exactly one
  ``results.mtx``.
- **Graph.** Every MTX file parses as a Boolean pattern matrix, every edge
  endpoint fits the declared dimensions, and all label matrices declare the
  same dimensions.
- **Results.** Every ``results.mtx`` parses as a Boolean pattern matrix with
  the graph's dimensions and in-range entries.
- **Queries.** Every representation file parses with its class reader (an
  ``.rsm`` via :obj:`rsa_from_text <cfpq_data.grammars.readwrite.rsa.rsa_from_text>`),
  uses at least one terminal, and uses only labels of its own graph (stored
  or reversed). An ``.rsm`` in ``rpq/`` must be regular — no box transition
  labelled by a nonterminal.
- **Description.** ``README.md`` answers all mandatory questions of the
  contribution templates; ``queries/README.md`` describes exactly the query
  directories that exist, each with a non-empty section.

The tool collects every violation and exits non-zero if any is found, so it
can gate a commit. With ``--audit`` it downloads and validates every
``.tar.gz`` object under the bucket prefix (credentials from the command
line, like :ref:`upload_to_s3`). :ref:`upload_to_s3` runs the same check
before uploading any ``.tar.gz`` and refuses an invalid archive.

.. _merge_archive:

Merge partial archives
----------------------

``utils/merge_archive.py`` merges a partial archive into the existing graph
archive it extends::

   python utils/merge_archive.py EXISTING.tar.gz PARTIAL.tar.gz -o MERGED.tar.gz

The partial source may also be an unpacked directory or a Google Drive URL /
file ID (the archive is downloaded first). The tool validates both inputs
(full mode for the existing archive, ``--partial`` mode for the partial
one), copies the new query directories into the existing tree, appends the
fragment's sections to the existing ``queries/README.md``, re-validates the
merged tree in full mode, and writes the result. Any problem — a query that
already exists, a section already described, a top-level directory named
after another graph, or a failed re-validation — is reported and the output
is not written; both inputs are left untouched.

The output file must be named after the graph (``<graph>.tar.gz``): the
upload tool stores it under that name, replacing the previous archive.

.. _reachable_pairs_tables:

Reachable pair counts
---------------------

``utils/reachable_pairs_tables.py`` keeps the reachable-pairs renderings in
sync with ``cfpq_data/dataset/reachable_pairs.csv``, the single source of
truth for the reference counts (:ref:`reachable_pairs`)::

   python utils/reachable_pairs_tables.py [--update]

The tool covers two renderings: the per-category tables of
``docs/reachable_pairs.rst`` (one section per graph category, between the
``reachable-pairs-tables`` markers) and the count columns of the eight
per-category graph tables in ``docs/graphs/*.rst``. The graph-to-category
mapping is derived from the site itself: each category page's toctree lists
its data pages, and the archive name in a data page's download URL is the
graph name (page titles are not reliable).

Behavior:

- **Check mode (default).** Reports every drifted cell or table region —
  plus CSV rows with an unknown ``query_class``, whose graph is unknown,
  whose category disagrees with the docs, or which has no count column in
  its category — and exits non-zero, so it can gate a commit. The
  count-column check applies to CFPQ rows only: the site renders CFPQ
  counts, and rows of other query classes are validated but not rendered
  until the per-class sections exist (task 50).
- **``--update``.** Rewrites the reachable-pairs region and fixes the
  drifted cells in place; lines that need no change keep their exact text.

On the category pages a cell is a number (the count), ``not available``
(a pair without a computed value yet), or empty (the grammar does not apply
to that graph) — the convention explained on the :ref:`graphs` page.

When a new count is computed, add the row to the CSV with the graph's
category and query class and run this tool with ``--update`` before
committing.

.. _migrate_gdrive_to_s3:

Migrate from Google Drive
-------------------------

``utils/migrate_gdrive_to_s3.py`` moves graph archives from Google Drive to
the bucket, one item at a time::

   python utils/migrate_gdrive_to_s3.py \
       --access-key-id KEY_ID --secret-access-key SECRET \
       [--endpoint-url URL] [--bucket BUCKET] \
       [--docs-dir DIR] [--workdir DIR] [--mapping FILE] \
       [--limit N] [--dry-run]

The item list is discovered from the docs: every "Direct download" link in
``docs/graphs/data/*.rst`` and ``docs/old_graphs/data/*.rst`` that points to
Google Drive becomes a migration item (the object key name is the graph
name). For each item the tool downloads the archive, uploads it with the
verified upload from :ref:`upload_to_s3` (``5.0.0/graph/<name>.tar.gz``),
removes the local copy, and replaces the Drive link(s) in the docs with the
new Yandex URL. At most one item is on disk at any time.

Behavior:

- **Idempotent.** Before downloading, the tool checks the public bucket URL;
  items already on Yandex are skipped. Re-running after an interruption
  resumes where it stopped.
- **Name collisions.** Ten graph names appear in two collections with
  different content, so both archives are kept: the item whose docs page stem
  equals the name keeps ``<name>.tar.gz``, the other is stored under its docs
  page stem (e.g. ``cactus_field_sensitive_alias.tar.gz``). If two items
  resolve to the same key the run stops with an error. Re-uploading an
  existing key is guarded by a SHA-256 comparison of the downloaded bytes; a
  mismatch stops the run and keeps the local copy for inspection.
- **Mapping.** After every item the tool saves
  ``utils/migration_mapping.json`` with the mapping graph name → new Yandex
  URL (plus the Drive file ID and SHA-256) so the migration record survives
  interruptions.
- **Conservative.** Any per-item error stops the run; fix the cause and
  re-run.

Use ``--dry-run`` to preview which items would be uploaded without any
side effects, and ``--limit N`` to migrate only the first N items (for
testing).
