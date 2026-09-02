from unittest import mock

import pytest

from upload_to_s3 import (
    DEFAULT_BUCKET,
    DEFAULT_ENDPOINT_URL,
    create_s3_client,
    main,
    upload_file,
)


def test_create_s3_client_passes_credentials_and_endpoint(monkeypatch):
    calls = {}

    def fake_client(service, **kwargs):
        calls["service"] = service
        calls.update(kwargs)
        return "client"

    monkeypatch.setattr("upload_to_s3.boto3.client", fake_client)

    client = create_s3_client("key-id", "secret", endpoint_url="https://example.com")

    assert client == "client"
    assert calls == {
        "service": "s3",
        "aws_access_key_id": "key-id",
        "aws_secret_access_key": "secret",
        "endpoint_url": "https://example.com",
    }


def test_create_s3_client_default_endpoint(monkeypatch):
    calls = {}

    def fake_client(service, **kwargs):
        calls.update(kwargs)
        return "client"

    monkeypatch.setattr("upload_to_s3.boto3.client", fake_client)

    create_s3_client("key-id", "secret")

    # Pin the verified working endpoint for the cfpq-data bucket.
    assert calls["endpoint_url"] == DEFAULT_ENDPOINT_URL == "https://s3.yandexcloud.net"


def test_upload_file_uploads_and_returns_key(tmp_path):
    file = tmp_path / "graph.tar.gz"
    file.write_bytes(b"payload")
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": 7}

    key = upload_file(client, file, "cfpq-data", key="4.0.0/graph/graph.tar.gz")

    assert key == "4.0.0/graph/graph.tar.gz"
    client.upload_file.assert_called_once_with(
        str(file), "cfpq-data", "4.0.0/graph/graph.tar.gz"
    )
    client.head_object.assert_called_once_with(
        Bucket="cfpq-data", Key="4.0.0/graph/graph.tar.gz"
    )


def test_upload_file_default_key_is_file_name(tmp_path):
    file = tmp_path / "graph.tar.gz"
    file.write_bytes(b"payload")
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": 7}

    key = upload_file(client, file, "cfpq-data")

    assert key == "graph.tar.gz"


def test_upload_file_missing_local_file(tmp_path):
    client = mock.Mock()

    with pytest.raises(FileNotFoundError):
        upload_file(client, tmp_path / "nope.tar.gz", "cfpq-data")

    client.upload_file.assert_not_called()


def test_upload_file_size_mismatch_raises(tmp_path):
    file = tmp_path / "graph.tar.gz"
    file.write_bytes(b"payload")
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": 3}

    with pytest.raises(RuntimeError, match="verification failed"):
        upload_file(client, file, "cfpq-data")


def test_main_uploads_file(tmp_path, monkeypatch, capsys):
    file = tmp_path / "graph.tar.gz"
    file.write_bytes(b"payload")
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": 7}
    monkeypatch.setattr("upload_to_s3.boto3.client", lambda *args, **kwargs: client)

    main(
        [
            str(file),
            "--access-key-id",
            "key-id",
            "--secret-access-key",
            "secret",
        ]
    )

    out = capsys.readouterr().out
    assert f"Uploaded {file} to s3://{DEFAULT_BUCKET}/graph.tar.gz" in out
    client.upload_file.assert_called_once()


def test_main_requires_credentials(tmp_path):
    file = tmp_path / "graph.tar.gz"
    file.write_bytes(b"payload")

    with pytest.raises(SystemExit):
        main([str(file)])
