import os
from os import path
from typing import List

from django.conf import settings

from cutepaste.files.models import FSEntry


def ls(files_path: str) -> List[FSEntry]:
    root_path = getattr(settings, "CP_ROOT_DIRS", "/data")
    while files_path.startswith("/"):
        files_path = files_path[1:]
    root_absolute_path = os.path.join(root_path, files_path)
    entries = []
    for filename in os.listdir(root_absolute_path):
        file_relative_path = path.join(files_path, filename)
        file_absolute_path = path.join(root_absolute_path, filename)
        entries.append(FSEntry(file_absolute_path, file_relative_path))
    return entries
