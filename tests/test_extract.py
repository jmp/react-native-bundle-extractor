import io
import zipfile
from unittest.mock import patch

from extract import extract_bundle_from_apk, pull_apk_from_device


def test_extract_bundle_from_apk(tmp_path):
    bundle_in_path = 'assets/index.android.bundle'
    bundle_out_path = tmp_path / 'index.android.bundle'
    zip_bytes = io.BytesIO()
    with zipfile.ZipFile(zip_bytes, mode='w') as zf:
        zf.writestr('AndroidManifest.xml', b'')
        zf.writestr('classes.dex', b'')
        zf.writestr(bundle_in_path, b'const a=42 ;')
    apk_path = tmp_path / 'test_extract.apk'
    apk_path.write_bytes(zip_bytes.getvalue())
    extract_bundle_from_apk(apk_path, bundle_in_path, bundle_out_path)
    assert bundle_out_path.exists()
    assert bundle_out_path.read_text() == 'const a = 42;'


@patch('extract.check_adb')
@patch('extract.get_packages')
@patch('extract.verify_package_exists')
@patch('extract.find_package_path')
@patch('extract.pull_path')
def test_pull_apk_from_device(
        mock_pull_path,
        mock_find_package_path,
        mock_verify_package_exists,
        mock_get_packages,
        mock_check_adb,
):
    package = 'com.example.app'
    out_path = '/some/path/app.apk'

    mock_check_adb.return_value = None
    mock_get_packages.return_value = [package]
    mock_verify_package_exists.return_value = None
    mock_find_package_path.return_value = f'/data/app/{package}-RGW6eku5yrzZ' \
                                          f'062ftW4_7Q==/base.apk'
    pull_apk_from_device(package, out_path)
    mock_pull_path.assert_called_with(
        mock_find_package_path.return_value,
        out_path,
    )
