import zipfile

from .decorators import log
from .exceptions import FileNotFoundInAPKError

MANIFEST_FILENAME = "AndroidManifest.xml"
CLASSES_FILENAME = "classes.dex"


@log("Extracting file")
def extract_file(zip_path, in_path, out_path):
    try:
        with zipfile.ZipFile(zip_path) as z:
            data = z.read(in_path)
            with open(out_path, "wb") as f:
                f.write(data)
    except KeyError:
        raise FileNotFoundInAPKError(f'Bundle file "{in_path}" not found')


@log("Checking if APK exists")
def is_apk(filename):
    def zip_contains(zip_file, name):
        return any(x == name for x in zip_file.namelist())

    if not zipfile.is_zipfile(filename):
        return False
    with zipfile.ZipFile(filename, "r") as z:
        return zip_contains(z, CLASSES_FILENAME) and zip_contains(z, MANIFEST_FILENAME)
