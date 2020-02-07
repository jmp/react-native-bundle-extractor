import io
import zipfile

import pytest

from extractor.apk import extract, is_apk, BundleNotFoundError


def test_extract_path_exists(tmp_path):
    zip_bytes = io.BytesIO()
    txt_file_path = 'some/directory/test.txt'
    with zipfile.ZipFile(zip_bytes, mode='w') as zf:
        zf.writestr(txt_file_path, b'This is a test file.')
    zip_path = tmp_path / 'test_extract.zip'
    zip_path.write_bytes(zip_bytes.getvalue())
    out_path = tmp_path / 'test.txt'
    extract(zip_path, txt_file_path, out_path)
    with out_path.open('rt') as f:
        assert f.read() == 'This is a test file.'


def test_extract_path_does_not_exist(tmp_path):
    zip_bytes = io.BytesIO()
    with zipfile.ZipFile(zip_bytes, mode='w'):
        pass
    zip_path = tmp_path / 'test_extract.zip'
    zip_path.write_bytes(zip_bytes.getvalue())
    with pytest.raises(BundleNotFoundError):
        extract(zip_path, 'this/does/not/exist', tmp_path / 'tmp.txt')


def test_is_apk_succeeds_with_manifest_and_classes(tmp_path):
    zip_bytes = io.BytesIO()
    with zipfile.ZipFile(zip_bytes, mode='w') as zf:
        zf.writestr('AndroidManifest.xml', b'')
        zf.writestr('classes.dex', b'')
    apk_path = tmp_path / 'valid_apk.apk'
    apk_path.write_bytes(zip_bytes.getvalue())
    assert is_apk(apk_path)


def test_is_apk_fails_with_invalid_apk(tmp_path):
    zip_bytes = io.BytesIO()
    with zipfile.ZipFile(zip_bytes, mode='w') as zf:
        zf.writestr('AndroidManifest.xml', b'')
    apk_path = tmp_path / 'invalid_apk.apk'
    assert not is_apk(apk_path)


def test_is_apk_fails_with_non_zip_file(tmp_path):
    non_zip_path = tmp_path / 'invalid_zip.zip'
    non_zip_path.write_text('This is a test.')
    assert not is_apk(non_zip_path)


def test_is_apk_fails_with_non_existent_file(tmp_path):
    assert not is_apk(tmp_path / 'this_file_does_not_exist')
