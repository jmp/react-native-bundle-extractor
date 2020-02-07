from .helpers import get_relative_path
from extractor.bundle import beautify


def test_beautify(tmp_path):  # noqa: F811
    in_path = get_relative_path('fixtures/test_beautify.js')
    out_path = tmp_path / 'beautified.js'
    beautify(in_path, out_path)
    with out_path.open('rt') as f:
        assert f.read() == '''
const f = () => {
    const a = 42;
    return a;
};
const b = f();
        '''.strip()
