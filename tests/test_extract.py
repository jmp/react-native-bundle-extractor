import io
import zipfile

from extract import extract_bundle_from_apk


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
