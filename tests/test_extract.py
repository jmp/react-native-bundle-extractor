import os
import pytest
import tempfile

from extract import extract, beautify_js


def _get_relative_path(path):
    return os.path.join(os.path.dirname(__file__), path)


@pytest.fixture
def temporary_path():
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.close()
    assert os.path.exists(tmp_file.name)
    yield tmp_file.name
    os.unlink(tmp_file.name)


def test_extract(temporary_path):
    zip_path = _get_relative_path('fixtures/test_extract.zip')
    in_path = 'some/directory/test.txt'
    extract(zip_path, in_path, temporary_path)
    with open(temporary_path, 'rt') as f:
        assert f.read() == 'This is a test file.'


def test_beautify_js(temporary_path):
    in_path = _get_relative_path('fixtures/test_beautify.js')
    beautify_js(in_path, temporary_path)
    with open(temporary_path, 'rt') as f:
        assert f.read() == '''
const f = () => {
    const a = 42;
    return a;
};
const b = f();
        '''.strip()
