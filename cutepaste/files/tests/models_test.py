from unittest.mock import call

import pytest

from ..models import FSEntry


@pytest.fixture(name="entry")
def fixture_entry():
    return FSEntry("/data/somefile", "/somefile")


def test_entry_paths(entry):
    assert entry.relative_path == "/somefile"
    assert entry.absolute_path == "/data/somefile"
    assert entry.name == "somefile"


def test_entry_file(entry, mocker):
    isfile_mock = mocker.patch("os.path.isfile", autospec=True)
    isfile_mock.return_value = True

    isdir_mock = mocker.patch("os.path.isdir", autospec=True)
    isdir_mock.return_value = False

    assert entry.is_file
    assert not entry.is_dir
    assert isfile_mock.mock_calls == [call("/data/somefile")]
    assert isdir_mock.mock_calls == [call("/data/somefile")]
