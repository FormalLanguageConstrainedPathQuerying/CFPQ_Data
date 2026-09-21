import pathlib
from unittest import mock

import pytest
from test_check_archive_structure import README, _tarball, _valid_tree
from upload_to_s3 import (
    DEFAULT_BUCKET,
    DEFAULT_ENDPOINT_URL,
    copy_object,
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


def test_upload_file_uploads_and_returns_key_and_size(tmp_path):
    file = tmp_path / "graph.tar.gz"
    file.write_bytes(b"payload")
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": 7}

    key, size = upload_file(client, file, "cfpq-data", key="4.0.0/graph/graph.tar.gz")

    assert key == "4.0.0/graph/graph.tar.gz"
    assert size == 7
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

    key, size = upload_file(client, file, "cfpq-data")

    assert key == "graph.tar.gz"
    assert size == 7


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


def test_copy_object_copies_and_returns_dest_key():
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": 7}

    key = copy_object(
        client, "cfpq-data", "4.0.0/graph/g.tar.gz", "5.0.0/graph/g.tar.gz"
    )

    assert key == "5.0.0/graph/g.tar.gz"
    client.copy_object.assert_called_once_with(
        Bucket="cfpq-data",
        CopySource={"Bucket": "cfpq-data", "Key": "4.0.0/graph/g.tar.gz"},
        Key="5.0.0/graph/g.tar.gz",
    )


def test_copy_object_default_dest_key_is_source_key():
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": 7}

    key = copy_object(client, "cfpq-data", "4.0.0/graph/g.tar.gz")

    assert key == "4.0.0/graph/g.tar.gz"


def test_copy_object_size_mismatch_raises():
    client = mock.Mock()
    client.head_object.side_effect = [{"ContentLength": 7}, {"ContentLength": 3}]

    with pytest.raises(RuntimeError, match="verification failed"):
        copy_object(client, "cfpq-data", "a.tar.gz", "b.tar.gz")


def _valid_tarball(tmp_path) -> pathlib.Path:
    tree = _valid_tree(tmp_path)
    return _tarball(tree, tmp_path / "g.tar.gz")


def test_main_uploads_valid_archive_and_reports_size(tmp_path, monkeypatch, capsys):
    file = _valid_tarball(tmp_path)
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": file.stat().st_size}
    monkeypatch.setattr("upload_to_s3.boto3.client", lambda *args, **kwargs: client)

    status = main(
        [
            str(file),
            "--access-key-id",
            "key-id",
            "--secret-access-key",
            "secret",
        ]
    )

    assert status == 0
    out = capsys.readouterr().out
    assert f"Uploaded {file} to s3://{DEFAULT_BUCKET}/g.tar.gz" in out
    client.upload_file.assert_called_once()


def test_main_reports_size_above_one_megabyte(tmp_path, monkeypatch, capsys):
    tree = _valid_tree(tmp_path)
    nodes = 5000
    pairs = [f"{i} {j}" for i in range(nodes) for j in range(i, min(i + 46, nodes))]
    (tree / "graph" / "a.mtx").write_text(
        "%%MatrixMarket matrix coordinate pattern general\n"
        f"%%GraphBLAS type bool\n{nodes} {nodes} {len(pairs)}\n"
        + "\n".join(pairs)
        + "\n"
    )
    file = _tarball(tree, tmp_path / "g.tar.gz")
    client = mock.Mock()
    client.head_object.return_value = {"ContentLength": file.stat().st_size}
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
    assert f"({file.stat().st_size} bytes, " in out and " MB)" in out


def test_main_refuses_invalid_archive_without_uploading(tmp_path, monkeypatch, capsys):
    tree = _valid_tree(tmp_path)
    (tree / "README.md").write_text(README.replace("## License\nApache-2.0.\n", ""))
    file = _tarball(tree, tmp_path / "g.tar.gz")
    client = mock.Mock()
    monkeypatch.setattr("upload_to_s3.boto3.client", lambda *args, **kwargs: client)

    status = main(
        [
            str(file),
            "--access-key-id",
            "key-id",
            "--secret-access-key",
            "secret",
        ]
    )

    assert status == 1
    out = capsys.readouterr().out
    assert "upload refused" in out and "'## License'" in out
    client.upload_file.assert_not_called()


def test_main_requires_credentials(tmp_path):
    file = tmp_path / "graph.tar.gz"
    file.write_bytes(b"payload")

    with pytest.raises(SystemExit):
        main([str(file)])
