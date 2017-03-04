import os
import shutil
import locale
from os import path
from typing import Callable, List
from PyICU import Collator, Locale
from django.conf import settings

from cutepaste.files.models import FSEntry

_collator = Collator.createInstance(Locale(locale.getdefaultlocale()[0]))


def _relative_path(file_path: str) -> str:
    while file_path.startswith("/"):
        file_path = file_path[1:]
    return file_path


def ls(files_path: str) -> List[FSEntry]:
    root_path = getattr(settings, "CP_ROOT_DIRS", "/data")
    relative_files_path = _relative_path(files_path)
    root_absolute_path = os.path.join(root_path, files_path)
    entries = []
    for filename in os.listdir(root_absolute_path):
        if settings.CP_SHOW_HIDDEN_FILES or not filename.startswith("."):
            file_relative_path = path.join(relative_files_path, filename)
            file_absolute_path = path.join(root_absolute_path, filename)
            entries.append(FSEntry(file_absolute_path, file_relative_path))
    return sorted(entries, key=lambda e: _collator.getSortKey(e.name))


def _perfom_fs_operation(operation: Callable[[str, str], str], source_files: List[str], destination_path: str) -> None:
    root_path = getattr(settings, "CP_ROOT_DIRS", "/data")
    relative_destination_path = _relative_path(destination_path)
    for source_file in source_files:
        absolute_source_path = path.join(root_path, source_file)
        absolute_target_dir = path.join(root_path, relative_destination_path) + "/"
        operation(absolute_source_path, absolute_target_dir)


def move(source_files: List[str], destination_path: str) -> None:
    _perfom_fs_operation(shutil.move, source_files, destination_path)


def copy(source_files: List[str], destination_path: str) -> None:
    _perfom_fs_operation(shutil.copy, source_files, destination_path)


def remove(source_files: List[str]) -> None:
    root_path = getattr(settings, "CP_ROOT_DIRS", "/data")
    for source_file in source_files:
        relative_source_file = _relative_path(source_file)
        absolute_source_path = path.join(root_path, relative_source_file)
        if path.isfile(absolute_source_path):
            os.remove(absolute_source_path)
        if path.isdir(absolute_source_path):
            shutil.rmtree(absolute_source_path)
