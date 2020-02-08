import io
import zipfile
from unittest.mock import patch, Mock

from extractor.extractor import (
    pull_apk_from_device,
    extract_bundle_from_apk,
    extract_bundle_from_device,
    run,
)
from .helpers import StringContaining


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


@patch('extractor.extractor.check_adb')
@patch('extractor.extractor.get_packages')
@patch('extractor.extractor.verify_package_exists')
@patch('extractor.extractor.find_package_path')
@patch('extractor.extractor.pull_path')
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


@patch('tempfile.NamedTemporaryFile')
@patch('extractor.extractor.pull_apk_from_device')
@patch('extractor.extractor.extract_bundle_from_apk')
def test_extract_bundle_from_device(
        mock_extract_bundle_from_apk,
        mock_pull_apk_from_device,
        mock_tmp,
):
    package = 'com.example.app'
    bundle = 'index.android.bundle'
    tmp_filename = 'temporary_file'
    mock_tmp.return_value.__enter__.return_value.name = tmp_filename
    extract_bundle_from_device(package, bundle)
    mock_pull_apk_from_device.assert_called_with(package, tmp_filename)
    mock_extract_bundle_from_apk.assert_called_with(tmp_filename, bundle)


@patch('sys.exit')
@patch('sys.stderr.write')
@patch('extractor.extractor.is_apk', Mock())
@patch('extractor.extractor.extract_bundle_from_apk', Mock())
@patch('extractor.extractor.extract_bundle_from_device', Mock())
def test_run_prints_usage_when_run_without_arguments(mock_write, mock_exit):
    run([])
    mock_write.assert_any_call(StringContaining('usage:'))
    mock_exit.assert_called_with(0)


@patch('sys.exit', Mock())
@patch('extractor.extractor.is_apk', Mock(return_value=True))
@patch('extractor.extractor.extract_bundle_from_apk')
def test_run_with_existing_apk(mock_extract_bundle_from_apk):
    apk_path = 'app.apk'
    run([apk_path])
    mock_extract_bundle_from_apk.assert_called_with(
        apk_path,
        'assets/index.android.bundle',
        'index.android.bundle',
    )


@patch('sys.exit', Mock())
@patch('extractor.extractor.extract_bundle_from_device')
def test_run_with_package(mock_extract_bundle_from_device):
    package = 'com.example.app'
    run([package])
    mock_extract_bundle_from_device.assert_called_with(
        package,
        'assets/index.android.bundle',
    )


@patch('sys.exit')
def test_run_with_invalid_package(mock_exit):
    run(['test'])
    mock_exit.assert_called_with(1)


@patch('sys.exit')
@patch('extractor.extractor.parse_args')
def test_run_with_keyboard_interrupt(mock_parse_args, mock_exit):
    mock_parse_args.side_effect = KeyboardInterrupt
    run([])
    mock_exit.assert_called_with(1)


@patch('sys.exit')
@patch('extractor.extractor.parse_args')
def test_run_exits_with_runtime_error(mock_parse_args, mock_exit):
    mock_parse_args.side_effect = RuntimeError
    run([])
    mock_exit.assert_called_with(1)
