#!/usr/bin/env python

import os
import sys
import subprocess
import tempfile
import zipfile
import jsbeautifier


DEFAULT_BUNDLE_FILENAME = 'index.android.bundle'


def extract(zip_path, in_path, out_path):
    with zipfile.ZipFile(zip_path) as z:
        data = z.read(in_path)
        with open(out_path, 'wb') as f:
            f.write(data)


def beautify_js(in_path, out_path):
    js = jsbeautifier.beautify_file(in_path)
    with open(out_path, 'wt') as f:
        f.write(js)


def list_packages():
    result = subprocess.run(
        'adb shell pm list packages'.split(),
        capture_output=True,
        check=True,
    )
    lines = result.stdout.strip().splitlines()
    return [line.decode('utf-8').replace('package:', '') for line in lines]


def get_package_path(package):
    result = subprocess.run(
        f'adb shell pm path {package}'.split(),
        capture_output=True,
        check=True,
    )
    return result.stdout.decode('utf-8').strip().replace('package:', '')


def pull_path(path, out_path):
    result = subprocess.run(
        f'adb pull {path} {out_path}'.split(),
        capture_output=True,
        check=True,
    )
    return result.stdout.decode('utf-8').strip()


def fetch_apk_from_device(package, out_path):
    print(f'Looking for package...', end='')
    if package not in list_packages():
        print(' FAIL')
        print(f'Package {package} was not found on device!')
        sys.exit(1)
    print(' OK')

    print(f'Getting package path...', end='')
    package_path = get_package_path(package)
    print(' OK')

    print(f'Pulling APK...', end='')
    pull_path(package_path, out_path)
    print(' OK')


def show_usage():
    print(f'usage: {sys.argv[0]} apk/package [bundle_filename]')
    sys.exit(1)


def process_apk(path, bundle_in_path):
    bundle_out_path = os.path.basename(bundle_in_path)
    try:
        print(f'Extracting bundle...', end='')
        extract(path, bundle_in_path, bundle_out_path)
        print(' OK')
    except KeyError:
        print(' FAIL')
        print(f'Bundle {bundle_in_path} was not found in the APK!')
        sys.exit(1)

    print(f'Beautifying bundle...', end='')
    beautify_js(bundle_out_path, bundle_out_path)
    print(' OK')

    sys.exit(0)


def process_package(package, bundle_filename):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        fetch_apk_from_device(package, f.name)
        process_apk(f.name, bundle_filename)
    sys.exit(0)


if __name__ == '__main__':
    if not 1 < len(sys.argv) < 4:
        show_usage()

    apk_or_package = sys.argv[1]
    try:
        bundle_path = f'assets/{sys.argv[2]}'
    except IndexError:
        bundle_path = f'assets/{DEFAULT_BUNDLE_FILENAME}'

    if os.path.exists(apk_or_package):
        process_apk(apk_or_package, bundle_path)
    else:
        process_package(apk_or_package, bundle_path)
