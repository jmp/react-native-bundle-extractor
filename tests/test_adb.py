from contextlib import contextmanager
from os import environ
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from extractor.adb import (
    check_adb,
    find_package_path,
    get_packages,
    pull_path,
    verify_package_exists,
)
from extractor.exceptions import (
    ExecutableNotFoundError,
    ExecuteError,
    PackageNotFoundError,
)


@contextmanager
def does_not_raise():
    yield


@patch.dict(environ, {"PATH": ""})
def test_check_adb_raises_exception_if_adb_not_in_path():
    with pytest.raises(ExecutableNotFoundError):
        check_adb()


@patch.dict(environ, {"PATH": str(Path(__file__).parent / "bin")})
def test_check_adb_does_not_raise_exception_if_adb_is_in_path():
    with does_not_raise():
        check_adb()


@patch("subprocess.run")
def test_get_packages_adb_success(mock_run):
    mock_run.return_value = Mock(
        stdout=b"""
package:com.android.cts.priv.ctsshim
package:com.android.internal.display.cutout.emulation.corner
package:com.android.providers.telephony
""".lstrip(),
        stderr=None,
    )
    assert get_packages() == [
        "com.android.cts.priv.ctsshim",
        "com.android.internal.display.cutout.emulation.corner",
        "com.android.providers.telephony",
    ]


@patch("subprocess.run")
def test_get_packages_adb_no_devices(mock_run):
    mock_run.return_value = Mock(
        stdout=None,
        stderr=b"error: no devices/emulators found",
    )
    with pytest.raises(ExecuteError):
        get_packages()


@patch("subprocess.run")
def test_find_package_path_success(mock_run):
    adb_stdout = (
        "package:/data/app/com.example.app-RGW6eku5yrzZ062ftW4_7Q" "==/base.apk\n"
    )
    mock_run.return_value = Mock(
        stdout=adb_stdout.encode(),
        stderr=None,
    )
    package = "com.example.app"
    expected = "/data/app/com.example.app-RGW6eku5yrzZ062ftW4_7Q==/base.apk"
    assert find_package_path(package) == expected


@patch("subprocess.run")
def test_find_package_path_does_not_exist(mock_run):
    mock_run.return_value = Mock(
        stdout=None,
        stderr=b"\n",
    )
    with pytest.raises(ExecuteError):
        assert find_package_path("this.does.not.exist")


@patch("subprocess.run")
def test_pull_path_success(mock_run):
    adb_stdout = "/foo: 1 file pulled. 144.3 MB/s (23917112 bytes in 0.158s)\n"
    mock_run.return_value = Mock(
        stdout=adb_stdout.encode(),
        stderr=None,
    )
    assert pull_path("/foo", "./foo") == adb_stdout.strip()


@patch("subprocess.run")
def test_pull_path_does_not_exist(mock_run):
    mock_run.return_value = Mock(
        stdout=None,
        stderr=b"adb: error: failed to stat remote object '/bar': No such "
        b"file or directory",
    )
    with pytest.raises(ExecuteError):
        pull_path("/bar", "./bar")


def test_verify_package_exists_success():
    with does_not_raise():
        verify_package_exists("com.example.app", ["com.example.app"])


def test_verify_package_exists_failure():
    with pytest.raises(PackageNotFoundError):
        verify_package_exists("com.example.app", [])
