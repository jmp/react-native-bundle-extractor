# noinspection PyUnresolvedReferences
from .fixtures import temporary_path  # noqa: F401
from .helpers import get_relative_path
from extractor.apk import extract


def test_extract(temporary_path):
    zip_path = get_relative_path('fixtures/test_extract.zip')
    in_path = 'some/directory/test.txt'
    extract(zip_path, in_path, temporary_path)
    with open(temporary_path, 'rt') as f:
        assert f.read() == 'This is a test file.'
