#!/usr/bin/env python -u

import os
import sys
import tempfile

from extractor.adb import (
    check_adb,
    get_packages,
    verify_package_exists,
    find_package_path,
    pull_path,
)
from extractor.apk import is_apk
from extractor.package import is_valid_package_name
from extractor.bundle import beautify
from extractor.apk import extract


DEFAULT_BUNDLE_FILENAME = 'index.android.bundle'


def show_usage():
    print(f'usage: {sys.argv[0]} apk/package [bundle_filename]')


def extract_bundle_from_apk(path, bundle_in_path):
    bundle_out_path = os.path.basename(bundle_in_path)
    extract(path, bundle_in_path, bundle_out_path)
    beautify(bundle_out_path, bundle_out_path)


def pull_apk_from_device(package, out_path):
    packages = get_packages()
    verify_package_exists(package, packages)
    package_path = find_package_path(package)
    pull_path(package_path, out_path)


def extract_bundle_from_device(package, bundle_filename):
    check_adb()
    with tempfile.NamedTemporaryFile(delete=False) as f:
        pull_apk_from_device(package, f.name)
        extract_bundle_from_apk(f.name, bundle_filename)


def get_source(argv):
    try:
        return argv[1]
    except IndexError:
        show_usage()
        sys.exit(1)


def get_bundle_path(argv):
    try:
        return f'assets/{argv[2]}'
    except IndexError:
        return f'assets/{DEFAULT_BUNDLE_FILENAME}'


def run():
    try:
        source = get_source(sys.argv)
        bundle_path = get_bundle_path(sys.argv)
        if is_apk(source):
            extract_bundle_from_apk(source, bundle_path)
        elif is_valid_package_name(source):
            extract_bundle_from_device(source, bundle_path)
        else:
            raise RuntimeError(f'"{source}" is not an APK or a package name.')
    except KeyboardInterrupt:
        sys.exit(1)
    except RuntimeError as e:
        print(e)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    run()
