import zipfile

from .decorators import with_logging


@with_logging('Extracting bundle')
def extract(zip_path, in_path, out_path):
    try:
        with zipfile.ZipFile(zip_path) as z:
            data = z.read(in_path)
            with open(out_path, 'wb') as f:
                f.write(data)
    except KeyError:
        raise RuntimeError(f'Bundle file "{in_path}" not found')


@with_logging('Checking if APK exists')
def is_apk(filename):
    def zip_contains(zip_file, name):
        return any(x == name for x in zip_file.namelist())
    if not zipfile.is_zipfile(filename):
        return False
    with zipfile.ZipFile(filename, 'r') as z:
        return all([
            zip_contains(z, 'classes.dex') and
            zip_contains(z, 'AndroidManifest.xml')
        ])
