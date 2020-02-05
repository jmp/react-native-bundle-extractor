from unittest import mock

import pytest

from extractor.adb import check_adb, ExecutableNotFoundError


@mock.patch('shutil.which')
def test_check_adb_raises_exception_if_adb_not_in_path(mock_which):
    mock_which.return_value = None
    with pytest.raises(ExecutableNotFoundError):
        check_adb()


@mock.patch('shutil.which')
def test_check_adb_does_not_raise_exception_if_adb_is_in_path(mock_which):
    mock_which.return_value = '/usr/bin/adb'
    try:
        check_adb()
    except ExecutableNotFoundError:
        pytest.fail('Unexpected ExecutableNotFoundError')
