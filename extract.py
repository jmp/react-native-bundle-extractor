#!/usr/bin/env python

import zipfile
import jsbeautifier


DEFAULT_BUNDLE_FILENAME = 'index.android.bundle'


def extract(zip_path, in_path, out_path):
    with zipfile.ZipFile(zip_path) as z:
        with open(out_path, 'wb') as f:
            f.write(z.read(in_path))


def beautify_js(in_path, out_path):
    js = jsbeautifier.beautify_file(in_path)
    with open(out_path, 'wt') as f:
        f.write(js)


if __name__ == '__main__':
    bundle_in_path = f'assets/{DEFAULT_BUNDLE_FILENAME}'
    bundle_out_path = DEFAULT_BUNDLE_FILENAME

    print(f'Extracting bundle...', end='')
    extract('app.apk', bundle_in_path, bundle_out_path)
    print(' DONE')

    print(f'Beautifying bundle...', end='')
    beautify_js(bundle_out_path, bundle_out_path)
    print(' DONE')
