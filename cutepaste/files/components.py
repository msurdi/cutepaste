from os import path

from django.template.loader import render_to_string
from typing import List

from cutepaste.files.forms import FilesEditForm
from cutepaste.files.models import FSEntry


def confirm_trash() -> str:
    return render_to_string(
        "files/components/confirm_trash.html",
        context={}
    )

def browser(files: List[FSEntry], current_path: str, clipboard_files: str, selection_status: str) -> str:
    return render_to_string(
        "files/components/browser.html",
        context={
            "buttons": buttons(current_path=current_path,
                               clipboard_files=clipboard_files,
                               selection_status=selection_status),
            "filelist": filelist(files=files,
                                 current_path=current_path,
                                 clipboard_files=clipboard_files)
        }
    )


def filelist(files: List[FSEntry], current_path: str, clipboard_files: str) -> str:
    parent_path = ""
    if current_path:
        parent_path = path.join(current_path, "..")

    return render_to_string(
        "files/components/filelist.html",
        context={
            "files": files,
            "total_files": len(files),
            "parent_path": parent_path,
            "current_path": current_path,
            "clipboard_files": clipboard_files,
            "total_clipboard_files": len(clipboard_files),
        })


def buttons(current_path: str, clipboard_files: str, selection_status: str) -> str:
    return render_to_string(
        "files/components/buttons.html",
        context={
            "current_path": current_path,
            "clipboard_files": clipboard_files,
            "selection_status": selection_status,
        })


def edit_form(form: FilesEditForm, current_path: str) -> str:
    return render_to_string(
        "files/components/edit_form.html",
        context={
            "edit_form": form,
            "current_path": current_path,
        }
    )
