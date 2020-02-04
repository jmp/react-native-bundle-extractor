import re


def is_valid_package_name(string):
    return bool(re.match(
        r'^[a-z]\w*(\.[a-z]\w*)+$',
        string,
        re.IGNORECASE,
    ))
