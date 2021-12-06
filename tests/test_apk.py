import io
import zipfile

import pytest

from extractor.apk import (
    CLASSES_FILENAME,
    MANIFEST_FILENAME,
    BundleNotFoundError,
    extract,
    is_apk,
)


def create_zip(filenames):
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, mode="w") as zf:
        for filename in filenames:
            zf.writestr(filename, f"this is {filename}")
    return zip_io.getvalue()


def test_extract_path_exists(tmp_path):
    txt_file_path = "some/directory/test.txt"
    zip_path = tmp_path / "test_extract.zip"
    zip_path.write_bytes(create_zip([txt_file_path]))
    out_path = tmp_path / "test.txt"
    extract(zip_path, txt_file_path, out_path)
    with out_path.open("rt") as f:
        assert f.read() == f"this is {txt_file_path}"


def test_extract_path_does_not_exist(tmp_path):
    zip_path = tmp_path / "test_extract.zip"
    zip_path.write_bytes(create_zip([]))
    with pytest.raises(BundleNotFoundError):
        extract(zip_path, "this/does/not/exist", tmp_path / "tmp.txt")


def test_is_apk_succeeds_with_manifest_and_classes(tmp_path):
    apk_path = tmp_path / "with_manifest_and_classes.apk"
    apk_path.write_bytes(create_zip([MANIFEST_FILENAME, CLASSES_FILENAME]))
    assert is_apk(apk_path)


def test_is_apk_fails_with_manifest_only(tmp_path):
    apk_path = tmp_path / "with_manifest.apk"
    apk_path.write_bytes(create_zip([MANIFEST_FILENAME]))
    assert not is_apk(apk_path)


def test_is_apk_fails_with_classes_only(tmp_path):
    apk_path = tmp_path / "with_classes.apk"
    apk_path.write_bytes(create_zip([CLASSES_FILENAME]))
    assert not is_apk(apk_path)


def test_is_apk_fails_without_manifest_or_classes(tmp_path):
    apk_path = tmp_path / "without_manifest_or_classes.apk"
    apk_path.write_bytes(create_zip([]))
    assert not is_apk(apk_path)


def test_is_apk_fails_with_non_zip_file(tmp_path):
    non_zip_path = tmp_path / "invalid_zip.zip"
    non_zip_path.write_text("This is a test.")
    assert not is_apk(non_zip_path)


def test_is_apk_fails_with_non_existent_file(tmp_path):
    assert not is_apk(tmp_path / "this_file_does_not_exist")
