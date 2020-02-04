import re


def is_valid_package_name(string):
    return re.match(
        r'^([a-zA-Z_][a-zA-Z0-9_]*(\\.[a-zA-Z_][a-zA-Z0-9_]*)*)?$',
        string,
    )
