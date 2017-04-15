import locale
import os
import shutil
from os import path
from typing import Any, Callable, List

from PyICU import Collator, Locale
from django.conf import settings

from cutepaste.files.models import FSEntry

_collator = Collator.createInstance(Locale(locale.getdefaultlocale()[0]))


def _relative_path(file_path: str) -> str:
    while file_path.startswith("/"):
        file_path = file_path[1:]
    return file_path


def _absolute_path(file_path: str) -> str:
    root_path = getattr(settings, "CP_ROOT_DIR", "/data")
    return path.join(root_path, _relative_path(file_path))


def _sort_files(files: List[FSEntry]) -> List[FSEntry]:
    return sorted(files, key=lambda f: (f.is_file, _collator.getSortKey(f.name)))


def ls(files_path: str) -> List[FSEntry]:
    root_path = getattr(settings, "CP_ROOT_DIR", "/data")
    relative_files_path = _relative_path(files_path)
    root_absolute_path = os.path.join(root_path, relative_files_path)
    entries = []
    for filename in os.listdir(root_absolute_path):
        if settings.CP_SHOW_HIDDEN_FILES or not filename.startswith("."):
            file_relative_path = path.join(relative_files_path, filename)
            file_absolute_path = path.join(root_absolute_path, filename)
            entries.append(FSEntry(file_absolute_path, file_relative_path))
    return _sort_files(entries)


def stat(file_path) -> FSEntry:
    absolute_path = _absolute_path(file_path)
    return FSEntry(absolute_path, file_path)


def _perfom_fs_operation(operation: Callable[[str, str], Any], source_files: List[str], destination_path: str) -> None:
    root_path = getattr(settings, "CP_ROOT_DIR", "/data")
    relative_destination_path = _relative_path(destination_path)
    for source_file in source_files:
        relative_source_file = _relative_path(source_file)
        absolute_source_path = path.join(root_path, relative_source_file)
        absolute_target_dir = path.join(root_path, relative_destination_path) + "/"
        operation(absolute_source_path, absolute_target_dir)


def move(source_files: List[str], destination_path: str) -> None:
    _perfom_fs_operation(shutil.move, source_files, destination_path)


def rename(source_file: str, destination_file: str) -> None:
    absolute_source_path = _absolute_path(source_file)
    absolute_destination_path = _absolute_path(destination_file)
    shutil.move(absolute_source_path, absolute_destination_path)


def copy(source_files: List[str], destination_path: str) -> None:
    _perfom_fs_operation(shutil.copy, source_files, destination_path)


def remove(source_files: List[str]) -> None:
    root_path = getattr(settings, "CP_ROOT_DIR", "/data")
    for source_file in source_files:
        relative_source_file = _relative_path(source_file)
        absolute_source_path = path.join(root_path, relative_source_file)
        if path.isfile(absolute_source_path):
            os.remove(absolute_source_path)
        if path.isdir(absolute_source_path):
            shutil.rmtree(absolute_source_path)
