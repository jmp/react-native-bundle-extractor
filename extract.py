#!/usr/bin/env python -u

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
from extractor.args import parse_args
from extractor.package import is_valid_package_name
from extractor.bundle import beautify
from extractor.apk import extract


def extract_bundle_from_apk(path, bundle_in_path, bundle_out_path):
    extract(path, bundle_in_path, bundle_out_path)
    beautify(bundle_out_path, bundle_out_path)


def pull_apk_from_device(package, out_path):
    check_adb()
    packages = get_packages()
    verify_package_exists(package, packages)
    package_path = find_package_path(package)
    pull_path(package_path, out_path)


def extract_bundle_from_device(package, bundle_filename):
    with tempfile.NamedTemporaryFile() as f:
        pull_apk_from_device(package, f.name)
        extract_bundle_from_apk(f.name, bundle_filename)


def run(args):
    try:
        parsed_args = parse_args(args)
        bundle_in_path = f'assets/{parsed_args.bundle}'
        bundle_out_path = parsed_args.out
        if is_apk(parsed_args.source):
            extract_bundle_from_apk(
                parsed_args.source,
                bundle_in_path,
                bundle_out_path,
            )
        elif is_valid_package_name(parsed_args.source):
            extract_bundle_from_device(parsed_args.source, bundle_in_path)
        else:
            raise RuntimeError(f'"{parsed_args.source}" is not an APK or an '
                               f'Android package name.')
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)
    except RuntimeError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    run(sys.argv[1:])
