from os import path

from django.http import HttpResponse
from django.shortcuts import render

from . import service

_CLIPBOARD = "clipboard"
_OPERATION = "operation"


def ls(request, files_path: str = "") -> HttpResponse:
    parent_path = ""
    if files_path:
        parent_path = path.join(files_path, "..")

    return render(request, "files/index.html", {
        "entries": service.ls(files_path),
        "current_path": files_path,
        "parent_path": parent_path,
        "clipboard_files_count": len(request.session.get(_CLIPBOARD, [])),
    })


def clipboard(request, operation: str) -> HttpResponse:
    if request.POST:
        request.session[_CLIPBOARD] = request.POST.getlist("selected", [])
        request.session[_OPERATION] = operation

    return render(request, "files/_clipboard_button.html", {
        "clipboard_files_count": len(request.session[_CLIPBOARD]),
    })


def paste(request, files_path: str) -> HttpResponse:
    if request.POST:
        if request.session[_OPERATION] == "cut":
            service.move(request.session.get(_CLIPBOARD, []), files_path)
        if request.session[_OPERATION] == "copy":
            service.copy(request.session.get(_CLIPBOARD, []), files_path)
    return ls(request, files_path)


def trash(request, files_path: str) -> HttpResponse:
    if request.POST:
        service.remove(request.POST.getlist("selected", []))
    return ls(request, files_path)
