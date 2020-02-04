# noinspection PyUnresolvedReferences
from .fixtures import temporary_path  # noqa: F401
from .helpers import get_relative_path
from extractor.apk import extract, is_apk


def test_extract(temporary_path):  # noqa: F811
    zip_path = get_relative_path('fixtures/test_extract.zip')
    in_path = 'some/directory/test.txt'
    extract(zip_path, in_path, temporary_path)
    with open(temporary_path, 'rt') as f:
        assert f.read() == 'This is a test file.'


def test_is_apk_succeeds_with_valid_apk():
    apk_path = get_relative_path('fixtures/test_valid_apk.apk')
    assert is_apk(apk_path)


def test_is_apk_fails_with_invalid_apk():
    apk_path = get_relative_path('fixtures/test_invalid_apk.apk')
    assert not is_apk(apk_path)
