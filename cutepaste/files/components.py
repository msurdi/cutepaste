from django.template.loader import render_to_string
from typing import Iterator, List, Tuple

from cutepaste.files.forms import FilesEditForm
from cutepaste.files.models import File


def confirm_trash() -> str:
    return render_to_string(
        "files/components/confirm_trash.html",
        context={}
    )


def browser(files: List[File], directory: str, clipboard_files: List[str], selection_status: str) -> str:
    return render_to_string(
        "files/components/browser.html",
        context={
            "buttons": buttons(directory=directory,
                               clipboard_files=clipboard_files,
                               selection_status=selection_status),
            "filelist": filelist(files=files,
                                 directory=directory,
                                 clipboard_files=clipboard_files)
        }
    )


def _get_all_parent_paths(start_path: str) -> Iterator[Tuple[str, str]]:
    parent_paths = []
    directories = start_path.split("/")
    while directories:
        directory_name = directories[-1]
        directory_path = "/".join(directories)
        parent_paths.append((directory_name, directory_path))
        directories = directories[:-1]
    return reversed(parent_paths)


def filelist(files: List[File], directory: str, clipboard_files: List[str]) -> str:
    parent_paths = _get_all_parent_paths(directory)

    return render_to_string(
        "files/components/filelist.html",
        context={
            "files": files,
            "total_files": len(files),
            "parent_paths": parent_paths,
            "directory": directory,
            "clipboard_files": clipboard_files,
            "total_clipboard_files": len(clipboard_files),
        })


def buttons(directory: str, clipboard_files: List[str], selection_status: str) -> str:
    return render_to_string(
        "files/components/buttons.html",
        context={
            "directory": directory,
            "clipboard_files": clipboard_files,
            "selection_status": selection_status,
        })


def edit_form(form: FilesEditForm, directory: str) -> str:
    return render_to_string(
        "files/components/edit_form.html",
        context={
            "edit_form": form,
            "directory": directory,
        }
    )
