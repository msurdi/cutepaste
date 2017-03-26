from unittest.mock import call

from .. import service
from ..models import FSEntry


def test_stat():
    entry = service.stat("somefile")

    assert isinstance(entry, FSEntry)


def test_ls(mocker, settings):
    def list_of_files(path):
        assert path == "/data/subdir/somedir"
        return ["file1", "file2", "file3"]

    settings.CP_ROOT_DIR = "/data"
    listdir_mock = mocker.patch("cutepaste.files.service.os.listdir")
    listdir_mock.side_effect = list_of_files

    entries = service.ls("subdir/somedir")

    assert len(entries) == 3


def test_ls_with_absolute_dir(mocker, settings):
    def ensure_listdir_inside_data_dir(path):
        assert path == "/data/root"
        return []

    settings.CP_ROOT_DIR = "/data"
    listdir_mock = mocker.patch("cutepaste.files.service.os.listdir")
    listdir_mock.side_effect = ensure_listdir_inside_data_dir

    service.ls("/root")


def test_move(mocker, settings):
    settings.CP_ROOT_DIR = "/data"
    move_mock = mocker.patch("cutepaste.files.service.shutil.move")

    service.move(["file1", "file2"], "/some/other/dir")

    assert move_mock.mock_calls == [call("/data/file1", "/data/some/other/dir/"),
                                    call("/data/file2", "/data/some/other/dir/")]


def test_move_absolute_dir(mocker, settings):
    settings.CP_ROOT_DIR = "/data"
    move_mock = mocker.patch("cutepaste.files.service.shutil.move")

    service.move(["/file1"], "/some/dir")

    assert move_mock.mock_calls == [call("/data/file1", "/data/some/dir/")]


def test_rename(mocker, settings):
    settings.CP_ROOT_DIR = "/data"
    move_mock = mocker.patch("cutepaste.files.service.shutil.move")

    service.rename("file1", "file2")

    assert move_mock.mock_calls == [call("/data/file1", "/data/file2")]


def test_rename_absolute(mocker, settings):
    settings.CP_ROOT_DIR = "/data"
    move_mock = mocker.patch("cutepaste.files.service.shutil.move")

    service.rename("/etc/hosts", "/etc/resolv.conf")

    assert move_mock.mock_calls == [call("/data/etc/hosts", "/data/etc/resolv.conf")]


def test_copy(mocker, settings):
    settings.CP_ROOT_DIR = "/data"
    copy_mock = mocker.patch("cutepaste.files.service.shutil.copy")

    service.copy(["file1", "file2"], "/some/dir")

    assert copy_mock.mock_calls == [call("/data/file1", "/data/some/dir/"),
                                    call("/data/file2", "/data/some/dir/")]


def test_copy_absolute(mocker, settings):
    settings.CP_ROOT_DIR = "/data"
    copy_mock = mocker.patch("cutepaste.files.service.shutil.copy")

    service.copy(["/etc/passwd"], "/tmp")

    assert copy_mock.mock_calls == [call("/data/etc/passwd", "/data/tmp/")]


def test_remove_files(mocker, settings):
    def is_file_results(path):
        return path in ["/data/file1", "/data/file2"]

    def is_dir_results(path):
        return path in ["/data/dir1"]

    settings.CP_ROOT_DIR = "/data"
    remove_mock = mocker.patch("cutepaste.files.service.os.remove")
    rmtree_mock = mocker.patch("cutepaste.files.service.shutil.rmtree")
    isfile_mock = mocker.patch("cutepaste.files.service.path.isfile")
    isfile_mock.side_effect = is_file_results
    isdir_mock = mocker.patch("cutepaste.files.service.path.isdir")
    isdir_mock.side_effect = is_dir_results

    service.remove(["file1", "file2", "dir1"])

    assert remove_mock.mock_calls == [call("/data/file1"), call("/data/file2")]
    assert rmtree_mock.mock_calls == [call("/data/dir1")]


def test_remove_absolute(mocker, settings):
    settings.CP_ROOT_DIR = "/data"
    remove_mock = mocker.patch("cutepaste.files.service.os.remove")
    isfile_mock = mocker.patch("cutepaste.files.service.path.isfile")
    isfile_mock.return_value = True

    service.remove(["/etc/hosts"])

    assert remove_mock.mock_calls == [call("/data/etc/hosts")]
