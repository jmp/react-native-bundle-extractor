import jsbeautifier

from .decorators import with_logging


@with_logging('Beautifying')
def beautify(in_path, out_path):
    js = jsbeautifier.beautify_file(in_path)
    with open(out_path, 'wt') as f:
        f.write(js)
