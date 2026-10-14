"""S3 access to the dataset object storage.

The dataset archives live in a Yandex Object Storage bucket reachable via
the S3 API. This module holds the storage endpoint and bucket name and the
client factory used by the maintainer tools (``utils/upload_to_s3.py`` and
the ``--audit`` mode of :mod:`flpq_data.tools.check_archive_structure`).

``boto3`` is imported lazily inside :func:`create_s3_client`, so importing
this module does not require it.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from botocore.client import BaseClient

__all__ = [
    "DEFAULT_ENDPOINT_URL",
    "DEFAULT_BUCKET",
    "create_s3_client",
]

#: The S3 API endpoint of the dataset object storage.
DEFAULT_ENDPOINT_URL = "https://s3.yandexcloud.net"

#: The bucket holding the dataset archives.
DEFAULT_BUCKET = "cfpq-data"


def create_s3_client(
    access_key_id: str,
    secret_access_key: str,
    endpoint_url: str = DEFAULT_ENDPOINT_URL,
) -> "BaseClient":
    """Create a boto3 S3 client for the dataset object storage.

    Parameters
    ----------
    access_key_id : str
        Yandex Cloud IAM service account key ID (provided from the CLI).
    secret_access_key : str
        Yandex Cloud IAM service account secret key (provided from the CLI).
    endpoint_url : str, optional
        S3 API endpoint of the bucket's region.
        Default: ``DEFAULT_ENDPOINT_URL``.

    Returns
    -------
    client : botocore.client.BaseClient
        Configured S3 client.

    Raises
    ------
    ImportError
        If ``boto3`` is not installed (it is a development dependency; the
        callers that need it report a friendly error instead).
    """
    import boto3

    return boto3.client(
        "s3",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        endpoint_url=endpoint_url,
    )
