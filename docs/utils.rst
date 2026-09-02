.. _utils:

Maintainer tools
================

.. only:: html

   :Release: |release|
   :Date: |today|

The ``utils/`` directory contains maintainer scripts for managing the dataset
stored on Yandex Object Storage (bucket ``cfpq-data``, S3 API). They are not
part of the public ``cfpq_data`` package.

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
- ``--endpoint-url`` — S3 API endpoint of the bucket's region; default
  ``https://s3.ru-central1.storage.yandexcloud.net``.
- ``--bucket`` — target bucket; default ``cfpq-data``.
- ``--key`` — object key in the bucket; default is the file name (e.g.
  ``4.0.0/graph/NAME.tar.gz`` to follow the dataset layout).

After the upload the tool verifies that the stored object size equals the
local file size and reports an error otherwise.
