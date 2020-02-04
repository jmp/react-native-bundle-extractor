import os
import tempfile
import pytest


@pytest.fixture
def temporary_path():
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.close()
    assert os.path.exists(tmp_file.name)
    yield tmp_file.name
    os.unlink(tmp_file.name)
