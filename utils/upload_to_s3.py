"""Upload local files to Yandex Object Storage via the S3 API."""

import argparse
import logging
import pathlib
from typing import Optional, Sequence, Union

import boto3
from botocore.client import BaseClient
from sizes import format_size_mb

__all__ = [
    "DEFAULT_ENDPOINT_URL",
    "DEFAULT_BUCKET",
    "create_s3_client",
    "upload_file",
    "copy_object",
    "main",
]

DEFAULT_ENDPOINT_URL = "https://s3.yandexcloud.net"
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
        Default: ``DEFAULT_ENDPOINT_URL``.

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
) -> tuple[str, int]:
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
    size : int
        The verified size of the stored object in bytes (equal to the local
        file size; the upload is aborted otherwise). The CLI reports it in
        MB with the same formatting as the ``Size (MB)`` column of the docs
        graph tables.

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

    logging.info(f"Uploaded {local_path} to s3://{bucket}/{key} ({stored_size} bytes)")
    return key, stored_size


def copy_object(
    client: BaseClient,
    bucket: str,
    source_key: str,
    dest_key: Optional[str] = None,
) -> str:
    """Copy an object within a bucket server-side and verify the stored size.

    Parameters
    ----------
    client : S3 client (see :func:`create_s3_client`).
    bucket : Bucket name (source and destination).
    source_key : Key of the existing object to copy.
    dest_key : Destination key. Default: ``source_key``.

    Returns
    -------
    dest_key : str
        The object key the copy was stored under.

    Raises
    ------
    RuntimeError
        If the stored size of the copy differs from the source size.
    """
    if dest_key is None:
        dest_key = source_key

    source_size = client.head_object(Bucket=bucket, Key=source_key)["ContentLength"]
    client.copy_object(
        Bucket=bucket,
        CopySource={"Bucket": bucket, "Key": source_key},
        Key=dest_key,
    )
    stored_size = client.head_object(Bucket=bucket, Key=dest_key)["ContentLength"]
    if stored_size != source_size:
        raise RuntimeError(
            f"Copy verification failed for s3://{bucket}/{dest_key}: "
            f"stored size {stored_size} != source size {source_size}"
        )

    logging.info(f"Copied s3://{bucket}/{source_key} to s3://{bucket}/{dest_key}")
    return dest_key


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Command-line entry point.

    Usage::

        python utils/upload_to_s3.py FILE \\
            --access-key-id KEY_ID --secret-access-key SECRET \\
            [--endpoint-url URL] [--bucket BUCKET] [--key KEY]

    Credentials are always taken from the command line and are never read
    from environment variables or config files. Any ``.tar.gz`` upload is
    first validated as a graph archive (see
    :mod:`check_archive_structure`); an invalid archive is refused.

    Returns
    -------
    status : int
        0 when the file was uploaded, 1 when the upload was refused.
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

    if args.file.endswith(".tar.gz"):
        from check_archive_structure import validate_archive

        problems = validate_archive(args.file)
        if problems:
            for problem in problems:
                print(f"error: {problem}")
            print("upload refused: the archive does not have the required structure")
            return 1

    client = create_s3_client(
        args.access_key_id, args.secret_access_key, args.endpoint_url
    )
    key, size = upload_file(client, args.file, args.bucket, args.key)
    print(
        f"Uploaded {args.file} to s3://{args.bucket}/{key} "
        f"({size} bytes, {format_size_mb(size)} MB)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
