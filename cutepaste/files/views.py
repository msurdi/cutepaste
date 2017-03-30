from os import path

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from cutepaste.files.forms import FilesEditForm
from cutepaste.util import ic_redirect
from . import service

CLIPBOARD_SESSION_KEY = "clipboard"
OPERATION_SESSION_KEY = "operation"
OPERATION_SELECTED_KEY = "selected"
CUT_OPERATION = "cut"
COPY_OPERATION = "copy"


def ls(request, files_path: str = "") -> HttpResponse:
    entry = service.stat(files_path)
    if entry.is_file:
        response = HttpResponse()
        response["X-Sendfile"] = entry.absolute_path
        return response

    entries = service.ls(files_path)
    clipboard_files = request.session.get(CLIPBOARD_SESSION_KEY, [])
    parent_path = ""
    if files_path:
        parent_path = path.join(files_path, "..")

    return render(request, "files/index.html", {
        "entries": entries,
        "total_files": len(entries),
        "parent_path": parent_path,
        "current_path": files_path,
        "selected_files": [],
        "total_selected_files": 0,
        "clipboard_files": clipboard_files,
        "total_clipboard_files": len(clipboard_files),

    })


def buttons(request) -> HttpResponse:
    selected_files = request.GET.getlist("selected", [])
    clipboard_files = request.session.get(CLIPBOARD_SESSION_KEY, [])

    return render(request, "files/_buttons.html", {
        "total_files": int(request.GET.get("total_files", 0)),
        "current_path": request.GET["current_path"],
        "selected_files": selected_files,
        "total_selected_files": len(selected_files),
        "clipboard_files": clipboard_files,
        "total_clipboard_files": len(clipboard_files),
    })


def copy(request) -> HttpResponse:
    if not request.POST:
        return HttpResponseBadRequest()

    request.session[OPERATION_SESSION_KEY] = COPY_OPERATION
    request.session[CLIPBOARD_SESSION_KEY] = request.POST.getlist("selected", [])

    return HttpResponse(status=200)


def cut(request) -> HttpResponse:
    if not request.POST:
        return HttpResponseBadRequest()

    request.session[OPERATION_SESSION_KEY] = CUT_OPERATION
    request.session[CLIPBOARD_SESSION_KEY] = request.POST.getlist("selected", [])
    return HttpResponse(status=200)


def paste(request) -> HttpResponse:
    if not request.POST or "current_path" not in request.POST:
        return HttpResponseBadRequest()

    current_path = request.POST["current_path"]
    if request.session[OPERATION_SESSION_KEY] == CUT_OPERATION:
        service.move(request.session.get(CLIPBOARD_SESSION_KEY, []), current_path)
    elif request.session[OPERATION_SESSION_KEY] == COPY_OPERATION:
        service.copy(request.session.get(CLIPBOARD_SESSION_KEY, []), current_path)
    else:
        return HttpResponseBadRequest("Cannot paste from selected operation")

    request.session[CLIPBOARD_SESSION_KEY] = []
    request.session[OPERATION_SESSION_KEY] = None

    return ls(request, current_path)


def trash(request) -> HttpResponse:
    if not request.POST or "selected" not in request.POST:
        return HttpResponseBadRequest()
    current_path = request.POST["current_path"]

    service.remove(request.POST.getlist("selected", []))
    return ls(request, current_path)


def edit(request, files_path: str = "") -> HttpResponse:
    files = service.ls(files_path)
    edit_form = FilesEditForm(request.POST or None, files=files)

    if edit_form.is_valid():
        for relative_path, new_name in edit_form.cleaned_data.items():
            new_relative_path = path.join(files_path, new_name)
            if relative_path != new_relative_path:
                service.rename(relative_path, new_relative_path)
        redirect_url = reverse("files:ls", args=[files_path])
        return ic_redirect(ls(request, files_path), redirect_url)

    return render(request, "files/edit.html", {
        "current_path": files_path,
        "edit_form": edit_form,
    })
