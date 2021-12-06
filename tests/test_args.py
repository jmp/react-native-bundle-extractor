import pytest

from extractor.args import parse_args


def test_parse_args_exits_with_usage_if_invalid_arguments(capsys):
    with pytest.raises(SystemExit):
        parse_args([])
    captured = capsys.readouterr()
    assert captured.err.startswith("usage:")


def test_parse_args_takes_apk_or_package_as_first_argument():
    source = "app.apk"
    args = parse_args([source])
    assert args.source == source


def test_parse_args_takes_bundle_filename_as_optional_argument():
    bundle = "test.bundle"
    args = parse_args(["app.apk", "--bundle", bundle])
    assert args.bundle == bundle


def test_parse_args_has_default_bundle_filename():
    args = parse_args(["app.apk"])
    assert isinstance(args.bundle, str)
    assert len(args.bundle) > 0


def test_parse_args_takes_output_path_as_optional_argument():
    out_path = "out.bundle"
    args = parse_args(["app.apk", "--out", out_path])
    assert args.out == out_path


def test_parse_args_has_default_output_path():
    args = parse_args(["app.apk"])
    assert isinstance(args.bundle, str)
    assert len(args.bundle) > 0
