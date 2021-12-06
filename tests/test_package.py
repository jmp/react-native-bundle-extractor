import pytest

from extractor.package import is_valid_package_name

valid_names = [
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
]

invalid_names = [
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
]

parameters = [(name, True) for name in valid_names] + [
    (name, False) for name in invalid_names
]


@pytest.mark.parametrize("test_input,expected", parameters)
def test_is_valid_package_name(test_input, expected):
    assert is_valid_package_name(test_input) == expected
