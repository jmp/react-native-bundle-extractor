import os


def get_relative_path(path):
    return os.path.join(os.path.dirname(__file__), path)


class StringContaining(str):
    def __eq__(self, other):
        return self in other
