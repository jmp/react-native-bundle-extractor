import zipfile


def extract(zip_path, in_path, out_path):
    with zipfile.ZipFile(zip_path) as z:
        data = z.read(in_path)
        with open(out_path, 'wb') as f:
            f.write(data)


def is_apk(filename):
    return zipfile.is_zipfile(filename)
