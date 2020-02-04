import zipfile


def extract(zip_path, in_path, out_path):
    with zipfile.ZipFile(zip_path) as z:
        data = z.read(in_path)
        with open(out_path, 'wb') as f:
            f.write(data)


def zip_contains(zip_file, name):
    return any(x == name for x in zip_file.namelist())


def is_apk(filename):
    if not zipfile.is_zipfile(filename):
        return False
    with zipfile.ZipFile(filename, 'r') as z:
        return all([
            zip_contains(z, 'classes.dex') and
            zip_contains(z, 'AndroidManifest.xml')
        ])
