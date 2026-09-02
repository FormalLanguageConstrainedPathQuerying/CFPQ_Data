"""Upload local files to Yandex Object Storage via the S3 API."""

import argparse
import logging
import pathlib
from typing import Optional, Sequence, Union

import boto3
from botocore.client import BaseClient

__all__ = [
    "DEFAULT_ENDPOINT_URL",
    "DEFAULT_BUCKET",
    "create_s3_client",
    "upload_file",
    "main",
]

DEFAULT_ENDPOINT_URL = "https://s3.ru-central1.storage.yandexcloud.net"
DEFAULT_BUCKET = "cfpq-data"


def create_s3_client(
    access_key_id: str,
    secret_access_key: str,
    endpoint_url: str = DEFAULT_ENDPOINT_URL,
) -> BaseClient:
    """Create a boto3 S3 client for Yandex Object Storage.

    Parameters
    ----------
    access_key_id : str
        Yandex Cloud IAM service account key ID (provided from the CLI).
    secret_access_key : str
        Yandex Cloud IAM service account secret key (provided from the CLI).
    endpoint_url : str, optional
        S3 API endpoint of the bucket's region.
        Default: ``DEFAULT_ENDPOINT_URL`` (ru-central1).

    Returns
    -------
    client : botocore.client.BaseClient
        Configured S3 client.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        endpoint_url=endpoint_url,
    )


def upload_file(
    client: BaseClient,
    local_path: Union[str, pathlib.Path],
    bucket: str,
    key: Optional[str] = None,
) -> str:
    """Upload a local file to an S3 bucket and verify the stored size.

    Parameters
    ----------
    client : botocore.client.BaseClient
        S3 client (see :func:`create_s3_client`).
    local_path : Union[str, Path]
        Path to the local file to upload.
    bucket : str
        Target bucket name.
    key : str, optional
        Object key in the bucket. Default: the file name.

    Returns
    -------
    key : str
        The object key the file was stored under.

    Raises
    ------
    FileNotFoundError
        If ``local_path`` does not exist.
    RuntimeError
        If the stored object size differs from the local file size.
    """
    local_path = pathlib.Path(local_path)
    if not local_path.is_file():
        raise FileNotFoundError(f"No such file: {local_path}")
    if key is None:
        key = local_path.name

    client.upload_file(str(local_path), bucket, key)

    stored_size = client.head_object(Bucket=bucket, Key=key)["ContentLength"]
    local_size = local_path.stat().st_size
    if stored_size != local_size:
        raise RuntimeError(
            f"Upload verification failed for s3://{bucket}/{key}: "
            f"stored size {stored_size} != local size {local_size}"
        )

    logging.info(f"Uploaded {local_path} to s3://{bucket}/{key}")
    return key


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Command-line entry point.

    Usage::

        python utils/upload_to_s3.py FILE \\
            --access-key-id KEY_ID --secret-access-key SECRET \\
            [--endpoint-url URL] [--bucket BUCKET] [--key KEY]

    Credentials are always taken from the command line and are never read
    from environment variables or config files.
    """
    parser = argparse.ArgumentParser(
        description="Upload a local file to Yandex Object Storage (S3 API)."
    )
    parser.add_argument("file", help="path to the local file to upload")
    parser.add_argument(
        "--access-key-id", required=True, help="Yandex Cloud IAM key ID"
    )
    parser.add_argument(
        "--secret-access-key",
        required=True,
        help="Yandex Cloud IAM secret key",
    )
    parser.add_argument(
        "--endpoint-url",
        default=DEFAULT_ENDPOINT_URL,
        help=f"S3 API endpoint (default: {DEFAULT_ENDPOINT_URL})",
    )
    parser.add_argument(
        "--bucket",
        default=DEFAULT_BUCKET,
        help=f"target bucket (default: {DEFAULT_BUCKET})",
    )
    parser.add_argument(
        "--key",
        default=None,
        help="object key in the bucket (default: file name)",
    )
    args = parser.parse_args(argv)

    client = create_s3_client(
        args.access_key_id, args.secret_access_key, args.endpoint_url
    )
    key = upload_file(client, args.file, args.bucket, args.key)
    print(f"Uploaded {args.file} to s3://{args.bucket}/{key}")


if __name__ == "__main__":
    main()
