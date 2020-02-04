# noinspection PyUnresolvedReferences
from .fixtures import temporary_path  # noqa: F401
from .helpers import get_relative_path
from extractor.bundle import beautify


def test_beautify(temporary_path):
    in_path = get_relative_path('fixtures/test_beautify.js')
    beautify(in_path, temporary_path)
    with open(temporary_path, 'rt') as f:
        assert f.read() == '''
const f = () => {
    const a = 42;
    return a;
};
const b = f();
        '''.strip()
