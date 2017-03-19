from unittest.mock import call

from .. import service
from ..models import FSEntry


def test_stat():
    entry = service.stat("somefile")
    assert isinstance(entry, FSEntry)


def test_ls(mocker):
    def list_of_files(path):
        assert path == "/data/subdir/somedir"
        return ["file1", "file2", "file3"]

    listdir_mock = mocker.patch("os.listdir")
    listdir_mock.side_effect = list_of_files

    entries = service.ls("subdir/somedir")
    assert len(entries) == 3


def test_ls_with_absolute_dir(mocker):
    def ensure_listdir_inside_data_dir(path):
        assert path == "/data/root"
        return []

    listdir_mock = mocker.patch("os.listdir")
    listdir_mock.side_effect = ensure_listdir_inside_data_dir
    service.ls("/root")


def test_move(mocker):
    move_mock = mocker.patch("shutil.move")
    service.move(["file1", "file2"], "/some/other/dir")

    assert move_mock.mock_calls == [call("/data/file1", "/data/some/other/dir/"),
                                    call("/data/file2", "/data/some/other/dir/")]


def test_move_absolute_dir(mocker):
    move_mock = mocker.patch("shutil.move")
    service.move(["/file1"], "/some/dir")

    assert move_mock.mock_calls == [call("/data/file1", "/data/some/dir/")]
