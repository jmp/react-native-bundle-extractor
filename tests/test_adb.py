from unittest.mock import patch, Mock

import pytest

from extractor.adb import check_adb, ExecutableNotFoundError, get_packages, \
    AdbError


@patch('shutil.which')
def test_check_adb_raises_exception_if_adb_not_in_path(mock_which):
    mock_which.return_value = None
    with pytest.raises(ExecutableNotFoundError):
        check_adb()


@patch('shutil.which')
def test_check_adb_does_not_raise_exception_if_adb_is_in_path(mock_which):
    mock_which.return_value = '/usr/bin/adb'
    try:
        check_adb()
    except ExecutableNotFoundError:
        pytest.fail('Unexpected ExecutableNotFoundError')


@patch('subprocess.run')
def test_get_packages_adb_returns_packages(mock_run):
    mock_run.return_value = Mock(stdout=b'''
package:com.android.cts.priv.ctsshim
package:com.google.android.youtube
package:com.android.internal.display.cutout.emulation.corner
package:com.google.android.ext.services
package:com.android.internal.display.cutout.emulation.double
package:com.android.providers.telephony
'''.strip(), stderr=None)
    try:
        get_packages()
    except AdbError:
        pytest.fail('Unexpected AdbError')


@patch('subprocess.run')
def test_get_packages_adb_returns_error(mock_run):
    mock_run.return_value = Mock(
        stdout=None,
        stderr=b'error: no devices/emulators found',
    )
    with pytest.raises(AdbError):
        get_packages()
