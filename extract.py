#!/usr/bin/env python -u

import os
import sys
import tempfile

from extractor.adb import pull_apk, check_adb
from extractor.apk import is_apk
from extractor.package import is_valid_package_name
from extractor.bundle import beautify
from extractor.apk import extract


DEFAULT_BUNDLE_FILENAME = 'index.android.bundle'


def show_usage():
    print(f'usage: {sys.argv[0]} apk/package [bundle_filename]')


def process_apk(path, bundle_in_path):
    bundle_out_path = os.path.basename(bundle_in_path)
    extract(path, bundle_in_path, bundle_out_path)
    beautify(bundle_out_path, bundle_out_path)


def process_package(package, bundle_filename):
    check_adb()
    with tempfile.NamedTemporaryFile(delete=False) as f:
        pull_apk(package, f.name)
        process_apk(f.name, bundle_filename)


if __name__ == '__main__':
    if not 1 < len(sys.argv) < 4:
        show_usage()
        sys.exit(1)
    try:
        try:
            bundle_path = f'assets/{sys.argv[2]}'
        except IndexError:
            bundle_path = f'assets/{DEFAULT_BUNDLE_FILENAME}'
        apk_or_package = sys.argv[1]
        if is_apk(apk_or_package):
            process_apk(apk_or_package, bundle_path)
        elif is_valid_package_name(apk_or_package):
            process_package(apk_or_package, bundle_path)
        else:
            print(f'"{apk_or_package}" is not an APK or a valid package name!')
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)
    except RuntimeError as e:
        print(e)
        sys.exit(1)
