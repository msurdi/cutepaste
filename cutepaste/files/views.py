from os import path

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from cutepaste.files.forms import FilesEditForm
from cutepaste.util import ic_redirect
from . import service

_CLIPBOARD = "clipboard"
_OPERATION = "operation"


def ls(request, files_path: str = "") -> HttpResponse:
    entry = service.stat(files_path)
    if entry.is_file:
        response = HttpResponse()
        response["X-Sendfile"] = entry.absolute_path
        return response

    parent_path = ""
    if files_path:
        parent_path = path.join(files_path, "..")

    return render(request, "files/index.html", {
        "entries": service.ls(files_path),
        "current_path": files_path,
        "parent_path": parent_path,
        "clipboard_button": _render_clipboard_button(request),
    })


def clipboard(request, operation: str) -> HttpResponse:
    if request.POST:
        request.session[_CLIPBOARD] = request.POST.getlist("selected", [])
        request.session[_OPERATION] = operation
    return HttpResponse(_render_clipboard_button(request))


def _render_clipboard_button(request) -> str:
    return render_to_string("files/_clipboard_button.html", request=request, context={
        "clipboard_has_files": len(request.session.get(_CLIPBOARD, [])) > 0,
    })


def paste(request, files_path: str = "") -> HttpResponse:
    if request.POST:
        if request.session[_OPERATION] == "cut":
            service.move(request.session.get(_CLIPBOARD, []), files_path)
        if request.session[_OPERATION] == "copy":
            service.copy(request.session.get(_CLIPBOARD, []), files_path)
        request.session[_CLIPBOARD] = []
    return ls(request, files_path)


def trash(request, files_path: str = "") -> HttpResponse:
    if request.POST:
        service.remove(request.POST.getlist("selected", []))
    return ls(request, files_path)


def edit(request, files_path: str = "") -> HttpResponse:
    files = service.ls(files_path)
    edit_form = FilesEditForm(request.POST or None, files=files)
    if edit_form.is_valid():
        for relative_path, new_name in edit_form.cleaned_data.items():
            new_relative_path = path.join(files_path, new_name)
            if new_name != new_relative_path:
                service.rename(relative_path, new_relative_path)
        redirect_url = reverse("files:ls", args=[files_path])
        return ic_redirect(ls(request, files_path), redirect_url)
    return render(request, "files/edit.html", {
        "current_path": files_path,
        "edit_form": edit_form,
    })
