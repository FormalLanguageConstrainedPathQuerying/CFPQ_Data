import hashlib
import io
import json
import pathlib
from unittest import mock

import pytest

from migrate_gdrive_to_s3 import (
    DRIVE_DOWNLOAD_URL,
    DriveDownloadError,
    MigrationError,
    MigrationItem,
    discover_items,
    download_from_drive,
    is_on_yandex,
    load_mapping,
    main,
    migrate,
    save_mapping,
    sha256_of,
    update_docs,
)


def _rst_page(full_name: str, direct_fid: str, origin_fid: str | None = None) -> str:
    origin = ""
    if origin_fid is not None:
        origin = (
            "   * - Origin\n"
            f"     - `.txt <https://drive.google.com/uc?export=download&id={origin_fid}>`_\n"
        )
    return (
        ".. _page:\n\n"
        f"{full_name}\n"
        f"{'=' * len(full_name)}\n\n"
        "Info\n"
        "----\n\n"
        ".. list-table::\n"
        "   :header-rows: 1\n\n"
        "   * -\n"
        "     -\n"
        "   * - Full Name\n"
        f"     - {full_name}\n"
        "   * - Direct download\n"
        f"     - `.tar.gz <https://drive.google.com/uc?export=download&id={direct_fid}>`_\n"
        f"{origin}"
    )


def test_discover_items_uses_stem_for_dataset_graphs(tmp_path):
    docs = tmp_path / "docs"
    (docs / "old_graphs/data").mkdir(parents=True)
    (docs / "old_graphs/data/skos.rst").write_text(
        _rst_page("skos", "FID_OLD", origin_fid="FID_ORIGIN"), encoding="utf-8"
    )

    items = discover_items(docs)

    assert items == [
        MigrationItem(name="skos", file_id="FID_OLD", source="old_graphs/data/skos.rst")
    ]


def test_discover_items_uses_full_name_for_new_collections(tmp_path):
    docs = tmp_path / "docs"
    (docs / "graphs/data").mkdir(parents=True)
    (docs / "graphs/data/provenance_airflow.rst").write_text(
        _rst_page("airflow", "FID_NEW"), encoding="utf-8"
    )

    items = discover_items(docs)

    assert items == [
        MigrationItem(
            name="airflow",
            file_id="FID_NEW",
            source="graphs/data/provenance_airflow.rst",
        )
    ]


def test_discover_items_ignores_origin_links(tmp_path):
    docs = tmp_path / "docs"
    (docs / "old_graphs/data").mkdir(parents=True)
    (docs / "old_graphs/data/skos.rst").write_text(
        _rst_page("skos", "FID_OLD", origin_fid="FID_ORIGIN"), encoding="utf-8"
    )

    items = discover_items(docs)

    assert [item.file_id for item in items] == ["FID_OLD"]


def test_discover_items_deduplicates_across_directories(tmp_path):
    docs = tmp_path / "docs"
    (docs / "graphs/data").mkdir(parents=True)
    (docs / "old_graphs/data").mkdir(parents=True)
    page = _rst_page("skos", "FID_OLD")
    (docs / "graphs/data/skos.rst").write_text(page, encoding="utf-8")
    (docs / "old_graphs/data/skos.rst").write_text(page, encoding="utf-8")

    items = discover_items(docs)

    assert [item.file_id for item in items] == ["FID_OLD"]
    assert items[0].source == "graphs/data/skos.rst"


def test_discover_items_skips_pages_without_drive_link(tmp_path):
    docs = tmp_path / "docs"
    (docs / "graphs/data").mkdir(parents=True)
    (docs / "graphs/data/migrated.rst").write_text(
        _rst_page("migrated", "NO_DRIVE_HERE").replace(
            "https://drive.google.com/uc?export=download&id=NO_DRIVE_HERE",
            "https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/migrated.tar.gz",
        ),
        encoding="utf-8",
    )

    assert discover_items(docs) == []


def test_discover_items_missing_data_dirs(tmp_path):
    assert discover_items(tmp_path / "docs") == []


class FakeResponse:
    def __init__(self, content: bytes = b"", headers: dict | None = None):
        self._content = content
        self.headers = headers or {}
        self.raw = io.BytesIO(content)

    @property
    def content(self) -> bytes:
        return self._content

    def close(self):
        pass


CONFIRM_FORM_HTML = (
    b'<html><body><form action="https://drive.usercontent.google.com/download">'
    b'<input type="hidden" name="id" value="FID1">'
    b'<input type="hidden" name="export" value="download">'
    b'<input type="hidden" name="confirm" value="t">'
    b'<input type="hidden" name="uuid" value="abc-123">'
    b"</form></body></html>"
)


def _patch_session(monkeypatch, session):
    monkeypatch.setattr("migrate_gdrive_to_s3.requests.Session", lambda: session)


def test_download_from_drive_direct_binary(tmp_path, monkeypatch):
    payload = b"archive-bytes"
    dest = tmp_path / "graph.tar.gz"
    session = mock.Mock()
    session.get.return_value = FakeResponse(
        content=payload, headers={"content-type": "application/octet-stream"}
    )
    _patch_session(monkeypatch, session)

    result = download_from_drive("FID1", dest)

    assert result == dest
    assert dest.read_bytes() == payload
    session.get.assert_called_once_with(
        DRIVE_DOWNLOAD_URL.format(file_id="FID1"), stream=True, timeout=300
    )


def test_download_from_drive_confirm_form(tmp_path, monkeypatch):
    payload = b"big-archive-bytes"
    dest = tmp_path / "graph.tar.gz"
    session = mock.Mock()
    session.get.side_effect = [
        FakeResponse(content=CONFIRM_FORM_HTML, headers={"content-type": "text/html"}),
        FakeResponse(
            content=payload, headers={"content-type": "application/octet-stream"}
        ),
    ]
    _patch_session(monkeypatch, session)

    download_from_drive("FID1", dest)

    assert dest.read_bytes() == payload
    session.get.assert_any_call(
        "https://drive.usercontent.google.com/download",
        params={
            "id": "FID1",
            "export": "download",
            "confirm": "t",
            "uuid": "abc-123",
        },
        stream=True,
        timeout=300,
    )


def test_download_from_drive_error_page_without_form(tmp_path, monkeypatch):
    dest = tmp_path / "graph.tar.gz"
    session = mock.Mock()
    session.get.return_value = FakeResponse(
        content=b"<html>File not found</html>", headers={"content-type": "text/html"}
    )
    _patch_session(monkeypatch, session)

    with pytest.raises(DriveDownloadError, match="error page"):
        download_from_drive("FID1", dest)

    assert not dest.exists()


def test_download_from_drive_error_page_after_confirm(tmp_path, monkeypatch):
    dest = tmp_path / "graph.tar.gz"
    session = mock.Mock()
    session.get.side_effect = [
        FakeResponse(content=CONFIRM_FORM_HTML, headers={"content-type": "text/html"}),
        FakeResponse(
            content=b"<html>Quota exceeded</html>",
            headers={"content-type": "text/html"},
        ),
    ]
    _patch_session(monkeypatch, session)

    with pytest.raises(DriveDownloadError, match="error page"):
        download_from_drive("FID1", dest)

    assert not dest.exists()


def test_download_from_drive_empty_file(tmp_path, monkeypatch):
    dest = tmp_path / "graph.tar.gz"
    session = mock.Mock()
    session.get.return_value = FakeResponse(
        content=b"", headers={"content-type": "application/octet-stream"}
    )
    _patch_session(monkeypatch, session)

    with pytest.raises(DriveDownloadError, match="empty file"):
        download_from_drive("FID1", dest)

    assert not dest.exists()


def _make_docs(docs: pathlib.Path, name: str, fid: str) -> None:
    (docs / "graphs/data").mkdir(parents=True, exist_ok=True)
    url = f"https://drive.google.com/uc?export=download&id={fid}"
    (docs / "graphs/data" / f"{name}.rst").write_text(
        f"page\n{url}\n", encoding="utf-8"
    )
    (docs / "graphs" / "index.rst").write_text(f"index\n{url}\n", encoding="utf-8")


def _fake_download(payloads: dict) -> mock.Mock:
    def fake(file_id, dest_path):
        dest = pathlib.Path(dest_path)
        dest.write_bytes(payloads[file_id])
        return dest

    return mock.Mock(side_effect=fake)


NEW_AIRFLOW_URL = "https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/airflow.tar.gz"


def test_migrate_uploads_new_item(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    _make_docs(docs, "airflow", "FID_A")
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    client = mock.Mock()
    monkeypatch.setattr(
        "migrate_gdrive_to_s3.download_from_drive",
        _fake_download({"FID_A": b"payload-a"}),
    )
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: False)
    uploaded = {}

    def fake_upload(client_, local_path, bucket, key=None):
        uploaded["key"] = key
        return key

    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", fake_upload)

    items = [MigrationItem(name="airflow", file_id="FID_A", source="s.rst")]
    summary = migrate(items, client, "cfpq-data", docs, workdir, mapping_path)

    assert summary == {"uploaded": 1, "skipped_existing": 0, "skipped_duplicate": 0}
    assert uploaded["key"] == "airflow.tar.gz"
    assert not (workdir / "airflow.tar.gz").exists()
    for rst in (docs / "graphs/data/airflow.rst", docs / "graphs/index.rst"):
        text = rst.read_text(encoding="utf-8")
        assert NEW_AIRFLOW_URL in text
        assert "FID_A" not in text
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    assert mapping["airflow"] == {
        "url": NEW_AIRFLOW_URL,
        "drive_file_id": "FID_A",
        "sha256": hashlib.sha256(b"payload-a").hexdigest(),
    }


def test_migrate_skips_item_already_on_yandex(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    _make_docs(docs, "airflow", "FID_A")
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    download = _fake_download({"FID_A": b"payload-a"})
    upload = mock.Mock()
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: True)
    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", upload)

    items = [MigrationItem(name="airflow", file_id="FID_A", source="s.rst")]
    summary = migrate(items, mock.Mock(), "cfpq-data", docs, workdir, mapping_path)

    assert summary == {"uploaded": 0, "skipped_existing": 1, "skipped_duplicate": 0}
    download.assert_not_called()
    upload.assert_not_called()
    text = (docs / "graphs/data/airflow.rst").read_text(encoding="utf-8")
    assert NEW_AIRFLOW_URL in text
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    assert mapping["airflow"]["sha256"] is None


NEW_CACTUS_URL = "https://cfpq-data.storage.yandexcloud.net/4.0.0/graph/cactus.tar.gz"


def test_migrate_shared_name_keeps_both_under_distinct_keys(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    _make_docs(docs, "cactus", "FID_1")
    (docs / "graphs/data/cactus_field_sensitive_alias.rst").write_text(
        "page\nhttps://drive.google.com/uc?export=download&id=FID_2\n",
        encoding="utf-8",
    )
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    download = _fake_download({"FID_1": b"points-to", "FID_2": b"field-sensitive"})
    upload = mock.Mock()
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: False)
    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", upload)

    items = [
        MigrationItem(name="cactus", file_id="FID_1", source="graphs/data/cactus.rst"),
        MigrationItem(
            name="cactus",
            file_id="FID_2",
            source="graphs/data/cactus_field_sensitive_alias.rst",
        ),
    ]
    summary = migrate(items, mock.Mock(), "cfpq-data", docs, workdir, mapping_path)

    assert summary == {"uploaded": 2, "skipped_existing": 0, "skipped_duplicate": 0}
    keys = [call.kwargs["key"] for call in upload.call_args_list]
    assert keys == ["cactus.tar.gz", "cactus_field_sensitive_alias.tar.gz"]
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    assert set(mapping) == {"cactus", "cactus_field_sensitive_alias"}
    assert mapping["cactus"]["drive_file_id"] == "FID_1"
    assert mapping["cactus_field_sensitive_alias"]["drive_file_id"] == "FID_2"


def test_migrate_rerun_uploaded_item_skips_upload(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    _make_docs(docs, "cactus", "FID_1")
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    save_mapping(
        mapping_path,
        {
            "cactus": {
                "url": NEW_CACTUS_URL,
                "drive_file_id": "FID_1",
                "sha256": hashlib.sha256(b"points-to").hexdigest(),
            }
        },
    )
    download = _fake_download({"FID_1": b"points-to"})
    upload = mock.Mock()
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: False)
    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", upload)

    items = [
        MigrationItem(name="cactus", file_id="FID_1", source="graphs/data/cactus.rst")
    ]
    summary = migrate(items, mock.Mock(), "cfpq-data", docs, workdir, mapping_path)

    assert summary == {"uploaded": 0, "skipped_existing": 0, "skipped_duplicate": 1}
    download.assert_called_once()
    upload.assert_not_called()


def test_migrate_rerun_twin_stored_under_stem_key(tmp_path, monkeypatch):
    # Re-run after the first item was migrated: only the twin's Drive link
    # remains in the docs, while the mapping still records the name entry.
    docs = tmp_path / "docs"
    (docs / "graphs/data").mkdir(parents=True)
    (docs / "graphs/data/cactus_field_sensitive_alias.rst").write_text(
        "page\nhttps://drive.google.com/uc?export=download&id=FID_2\n",
        encoding="utf-8",
    )
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    save_mapping(
        mapping_path,
        {
            "cactus": {
                "url": NEW_CACTUS_URL,
                "drive_file_id": "FID_1",
                "sha256": hashlib.sha256(b"points-to").hexdigest(),
            }
        },
    )
    download = _fake_download({"FID_2": b"field-sensitive"})
    upload = mock.Mock()
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: False)
    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", upload)

    items = [
        MigrationItem(
            name="cactus",
            file_id="FID_2",
            source="graphs/data/cactus_field_sensitive_alias.rst",
        )
    ]
    summary = migrate(items, mock.Mock(), "cfpq-data", docs, workdir, mapping_path)

    assert summary == {"uploaded": 1, "skipped_existing": 0, "skipped_duplicate": 0}
    upload.assert_called_once()
    assert upload.call_args.kwargs["key"] == "cactus_field_sensitive_alias.tar.gz"
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    assert set(mapping) == {"cactus", "cactus_field_sensitive_alias"}


def test_migrate_same_name_and_stem_cannot_disambiguate(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    _make_docs(docs, "cactus", "FID_1")
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    download = _fake_download({"FID_1": b"a", "FID_2": b"b"})
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: False)
    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", mock.Mock())

    items = [
        MigrationItem(name="cactus", file_id="FID_1", source="graphs/data/cactus.rst"),
        MigrationItem(name="cactus", file_id="FID_2", source="graphs/data/cactus.rst"),
    ]
    with pytest.raises(MigrationError, match="Cannot disambiguate"):
        migrate(items, mock.Mock(), "cfpq-data", docs, workdir, mapping_path)

    download.assert_not_called()


def test_migrate_rerun_hashless_entry_still_on_yandex(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    _make_docs(docs, "airflow", "FID_A")
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    save_mapping(
        mapping_path,
        {
            "airflow": {
                "url": NEW_AIRFLOW_URL,
                "drive_file_id": "FID_A",
                "sha256": None,
            }
        },
    )
    download = _fake_download({"FID_A": b"payload-a"})
    upload = mock.Mock()
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: True)
    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", upload)

    items = [MigrationItem(name="airflow", file_id="FID_A", source="s.rst")]
    summary = migrate(items, mock.Mock(), "cfpq-data", docs, workdir, mapping_path)

    assert summary == {"uploaded": 0, "skipped_existing": 1, "skipped_duplicate": 0}
    download.assert_not_called()
    upload.assert_not_called()


def test_migrate_rerun_hashless_entry_gone_from_bucket(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    _make_docs(docs, "airflow", "FID_A")
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    save_mapping(
        mapping_path,
        {
            "airflow": {
                "url": NEW_AIRFLOW_URL,
                "drive_file_id": "FID_A",
                "sha256": None,
            }
        },
    )
    download = _fake_download({"FID_A": b"payload-a"})
    upload = mock.Mock()
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: False)
    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", upload)

    items = [MigrationItem(name="airflow", file_id="FID_A", source="s.rst")]
    summary = migrate(items, mock.Mock(), "cfpq-data", docs, workdir, mapping_path)

    assert summary == {"uploaded": 1, "skipped_existing": 0, "skipped_duplicate": 0}
    upload.assert_called_once()
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    assert mapping["airflow"]["sha256"] == hashlib.sha256(b"payload-a").hexdigest()


def test_migrate_limit_stops_after_n_items(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    _make_docs(docs, "airflow", "FID_A")
    _make_docs(docs, "celery", "FID_C")
    workdir = tmp_path / "work"
    mapping_path = tmp_path / "mapping.json"
    download = _fake_download({"FID_A": b"a", "FID_C": b"c"})
    upload = mock.Mock()
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: False)
    monkeypatch.setattr("migrate_gdrive_to_s3.upload_file", upload)

    items = [
        MigrationItem(name="airflow", file_id="FID_A", source="s1.rst"),
        MigrationItem(name="celery", file_id="FID_C", source="s2.rst"),
    ]
    summary = migrate(
        items, mock.Mock(), "cfpq-data", docs, workdir, mapping_path, limit=1
    )

    assert summary == {"uploaded": 1, "skipped_existing": 0, "skipped_duplicate": 0}
    upload.assert_called_once()
    assert "FID_C" in (docs / "graphs/data/celery.rst").read_text(encoding="utf-8")


def test_update_docs_replaces_both_forms_and_skips_build(tmp_path):
    docs = tmp_path / "docs"
    (docs / "_build").mkdir(parents=True)
    form_a = "x https://drive.google.com/uc?export=download&id=FID y\n"
    form_b = "x https://drive.google.com/file/d/FID/view?usp=sharing y\n"
    (docs / "a.rst").write_text(form_a, encoding="utf-8")
    (docs / "b.rst").write_text(form_b, encoding="utf-8")
    (docs / "_build" / "a.rst").write_text(form_a, encoding="utf-8")

    changed = update_docs(docs, "FID", "NEW_URL")

    assert changed == 2
    assert "NEW_URL" in (docs / "a.rst").read_text(encoding="utf-8")
    assert "NEW_URL" in (docs / "b.rst").read_text(encoding="utf-8")
    assert "FID" in (docs / "_build" / "a.rst").read_text(encoding="utf-8")


def test_mapping_roundtrip(tmp_path):
    path = tmp_path / "mapping.json"
    assert load_mapping(path) == {}
    mapping = {"airflow": {"url": "U", "drive_file_id": "F", "sha256": None}}
    save_mapping(path, mapping)
    assert load_mapping(path) == mapping


def test_sha256_of(tmp_path):
    file = tmp_path / "f.bin"
    file.write_bytes(b"payload")
    assert sha256_of(file) == hashlib.sha256(b"payload").hexdigest()


def test_main_dry_run_has_no_side_effects(tmp_path, monkeypatch, capsys):
    docs = tmp_path / "docs"
    (docs / "graphs/data").mkdir(parents=True)
    (docs / "graphs/data/provenance_airflow.rst").write_text(
        _rst_page("airflow", "FID_A"), encoding="utf-8"
    )
    mapping_path = tmp_path / "mapping.json"
    download = mock.Mock()
    monkeypatch.setattr("migrate_gdrive_to_s3.download_from_drive", download)
    monkeypatch.setattr("migrate_gdrive_to_s3.is_on_yandex", lambda name: False)

    main(
        [
            "--access-key-id",
            "key-id",
            "--secret-access-key",
            "secret",
            "--docs-dir",
            str(docs),
            "--mapping",
            str(mapping_path),
            "--dry-run",
        ]
    )

    out = capsys.readouterr().out
    assert "airflow: upload" in out
    download.assert_not_called()
    assert not mapping_path.exists()
    assert "FID_A" in (docs / "graphs/data/provenance_airflow.rst").read_text(
        encoding="utf-8"
    )


def test_main_requires_credentials():
    with pytest.raises(SystemExit):
        main([])
