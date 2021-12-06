import os
import subprocess
import zipfile
from pathlib import Path

script_path = Path(__file__).parent.parent / "extract.py"


def test_extract_bundle_from_apk(tmp_path):
    bundle_out_path = tmp_path / "index.android.bundle"
    apk_path = tmp_path / "test_extract.apk"
    with zipfile.ZipFile(apk_path, mode="w") as zf:
        zf.writestr("AndroidManifest.xml", b"")
        zf.writestr("classes.dex", b"")
        zf.writestr(f"assets/index.android.bundle", b"const a=100 ;")
    subprocess.run([script_path, apk_path, "--out", bundle_out_path])
    assert bundle_out_path.exists()
    assert bundle_out_path.read_text() == "const a = 100;"


def test_extract_bundle_from_device(tmp_path):
    package = "com.example.app"
    adb_path = Path(__file__).parent / "bin"
    bundle_out_path = tmp_path / "index.android.bundle.out"
    subprocess.run(
        [script_path, package, "--out", bundle_out_path],
        env={"PATH": f"{adb_path}{os.pathsep}{os.environ['PATH']}"},
    )
    assert bundle_out_path.exists()
    assert bundle_out_path.read_text() == "const a = 100;"
