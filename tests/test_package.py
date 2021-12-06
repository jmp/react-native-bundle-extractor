import pytest

from extractor.package import is_valid_package_name


@pytest.mark.parametrize(
    "valid_name",
    [
        "com.example",
        "com1.example",
        "com.example1",
        "com_.example",
        "com.example_",
        "com.example.app",
        "com1.example.app",
        "com.example1.app",
        "com.example.app1",
        "com_.example.app",
        "com.example_.app",
        "com.example.app_",
        "Com.Example.App",
    ],
)
def test_is_valid_package_name_returns_true_if_name_is_valid(valid_name):
    assert is_valid_package_name(valid_name) is True


@pytest.mark.parametrize(
    "invalid_name",
    [
        "com",
        "com.",
        ".com",
        "1com.example",
        "com.1example",
        "1com.example.app",
        "com.1example.app",
        "com.example.1app",
        "_com.example.app",
        "com._example.app",
        "com.example._app",
        "com.example.app/",
        ":com.example.app",
        "com.:example.app",
        "com.example.:app",
        "com:.example.app",
        "com.example:.app",
        "com.example.app:",
        "com..example.app",
        "com.example..app",
        "com.example.app.",
    ],
)
def test_is_valid_package_name_returns_false_if_name_is_invalid(invalid_name):
    assert is_valid_package_name(invalid_name) is False
