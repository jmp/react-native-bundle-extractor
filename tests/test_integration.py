import io
import subprocess
import zipfile
from pathlib import Path


def test_extract_bundle_from_apk(tmp_path):
    bundle_name = "index.android.bundle"
    bundle_in_path = f"assets/{bundle_name}"
    bundle_out_path = tmp_path / bundle_name
    zip_bytes = io.BytesIO()
    with zipfile.ZipFile(zip_bytes, mode="w") as zf:
        zf.writestr("AndroidManifest.xml", b"")
        zf.writestr("classes.dex", b"")
        zf.writestr(bundle_in_path, b"const a=100 ;")
    apk_path = tmp_path / "test_extract.apk"
    apk_path.write_bytes(zip_bytes.getvalue())
    script_path = Path(__file__).parent.parent / "extract.py"
    subprocess.run(
        [script_path, "--bundle", bundle_name, apk_path, "--out", bundle_out_path]
    )
    assert bundle_out_path.exists()
    assert bundle_out_path.read_text() == "const a = 100;"
