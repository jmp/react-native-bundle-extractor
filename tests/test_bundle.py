from extractor.bundle import beautify


def test_beautify(tmp_path):
    in_path = tmp_path / 'ugly.js'
    in_path.write_text('const f=()=>{const a=42;return a;};const b=f();')
    out_path = tmp_path / 'beautified.js'
    beautify(in_path, out_path)
    assert out_path.read_text() == '''
const f = () => {
    const a = 42;
    return a;
};
const b = f();
        '''.strip()
