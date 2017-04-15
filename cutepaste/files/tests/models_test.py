from unittest.mock import call

import pytest

from ..models import File


@pytest.fixture(name="file")
def fixture_file():
    return File("/data/somefile", "/somefile")


def test_file_paths(file):
    assert file.relative_path == "/somefile"
    assert file.absolute_path == "/data/somefile"
    assert file.name == "somefile"


def test_file(file, mocker):
    isfile_mock = mocker.patch("cutepaste.files.models.path.isfile", autospec=True)
    isfile_mock.return_value = True

    isdir_mock = mocker.patch("cutepaste.files.models.path.isdir", autospec=True)
    isdir_mock.return_value = False

    assert file.is_file
    assert not file.is_dir
    assert isfile_mock.mock_calls == [call("/data/somefile")]
    assert isdir_mock.mock_calls == [call("/data/somefile")]
