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
  ``5.0.0/graph/NAME.tar.gz`` to follow the dataset layout).

After the upload the tool verifies that the stored object size equals the
local file size and reports an error otherwise.

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

.. _convert_old_to_new:

Convert old-format graphs
-------------------------

``utils/convert_old_to_new.py`` converts graph archives from the old format
(``<name>/<name>.csv`` + ``README.md``, one space-separated ``from to label``
line per edge) to the new mtx-per-label format (``<name>/README.md`` +
``<name>/grammar/*.cnf`` + one Boolean MatrixMarket matrix per edge label in
``<name>/graph/``), one graph at a time::

   python utils/convert_old_to_new.py [NAME|SECTION]... \
       [--access-key-id KEY_ID --secret-access-key SECRET] \
       [--endpoint-url URL] [--bucket BUCKET] [--key-prefix PREFIX] \
       [--record FILE] [--workdir DIR] [--dry-run] [--force] \
       [--report FILE]

Each ``NAME|SECTION`` argument is a graph name or a section key (``rdf``,
``c_alias``, ``java_points_to``) expanding to all its graphs — the 54 old-
format archives of the dataset (20 RDF, 20 C alias analysis, 14 Java
points-to). For each graph the tool downloads a single archive from the
public bucket, converts it locally, verifies the conversion by round-trip
(the per-label matrices must reproduce the CSV edge multiset in order, with
matching headers), packs the new archive, uploads it under the ``5.0.0/graph/``
key prefix (verified upload via :ref:`upload_to_s3`), checks that the object
is anonymously readable, and removes the local files. At most one graph is on
disk at any time, so graphs with tens of millions of edges convert with O(1)
memory.

Grammar files: the java points-to archives get the compact 19-rule template
shared by all new-format java archives (indexed symbols ``load``, ``store``,
``load_r``, ``store_r`` match the labels ``load_<k>``, ``store_<k>``,
``load_<k>_r``, ``store_<k>_r``); the C alias and RDF archives get the
package canonical grammars
(:func:`cfpq_data.grammars.generators.c_alias_grammar`,
:func:`cfpq_data.grammars.generators.nested_parentheses_grammar` with
``eps=False`` — for RDF the three canonical grammars of the graph's docs
page, plus broaderTransitive if the graph has such edges). Reversed ``_r``
edges are not stored; the README documents that they are derived by
reversing the respective forward edges.

Behavior:

- **Idempotent.** After every graph the tool saves
  ``utils/conversion_record.json`` (old/new SHA-256, key, date); recorded
  graphs whose object is publicly readable are skipped on re-run.
  ``--force`` re-converts them.
- **Conservative.** Any per-graph error stops the run and keeps the local
  files under the workdir for inspection; fix the cause and re-run.
- Credentials are always taken from the command line (required unless
  ``--dry-run``) and are never persisted.

Use ``--dry-run`` to convert and verify all graphs locally without uploading
or recording anything, and ``--report FILE`` to write the per-graph results
to a JSON file.
