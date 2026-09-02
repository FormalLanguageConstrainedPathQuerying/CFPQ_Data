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
  ``4.0.0/graph/NAME.tar.gz`` to follow the dataset layout).

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
verified upload from :ref:`upload_to_s3` (``4.0.0/graph/<name>.tar.gz``),
removes the local copy, and replaces the Drive link(s) in the docs with the
new Yandex URL. At most one item is on disk at any time.

Behavior:

- **Idempotent.** Before downloading, the tool checks the public bucket URL;
  items already on Yandex are skipped. Re-running after an interruption
  resumes where it stopped.
- **Name collisions.** A graph name identifies the graph uniquely, so a name
  is never stored twice. If two Drive files share a name, their contents are
  compared by SHA-256: identical content is uploaded once, differing content
  stops the run (the local copy is kept for inspection).
- **Mapping.** After every item the tool saves
  ``utils/migration_mapping.json`` with the mapping graph name → new Yandex
  URL (plus the Drive file ID and SHA-256) so the migration record survives
  interruptions.
- **Conservative.** Any per-item error stops the run; fix the cause and
  re-run.

Use ``--dry-run`` to preview which items would be uploaded without any
side effects, and ``--limit N`` to migrate only the first N items (for
testing).
