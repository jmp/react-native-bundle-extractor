import re

from extractor.decorators import with_logging


@with_logging('Checking package format')
def is_valid_package_name(string):
    return bool(re.match(
        r'^[a-z]\w*(\.[a-z]\w*)+$',
        string,
        re.IGNORECASE,
    ))
