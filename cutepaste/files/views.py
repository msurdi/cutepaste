from os import path

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from cutepaste.files.forms import FilesEditForm
from cutepaste.util import ic_redirect
from . import service

CLIPBOARD_SESSION_KEY = "clipboard"
OPERATION_SESSION_KEY = "operation"
CUT_OPERATION = "cut"
COPY_OPERATION = "copy"


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
        if operation not in [CUT_OPERATION, COPY_OPERATION]:
            return HttpResponseBadRequest(f"Operation should be one of [{CUT_OPERATION}, {COPY_OPERATION}]")
        request.session[CLIPBOARD_SESSION_KEY] = request.POST.getlist("selected", [])
        request.session[OPERATION_SESSION_KEY] = operation

    return HttpResponse(_render_clipboard_button(request))


def _render_clipboard_button(request) -> str:
    return render_to_string("files/_clipboard_button.html", request=request, context={
        "clipboard_has_files": len(request.session.get(CLIPBOARD_SESSION_KEY, [])) > 0,
    })


def paste(request, files_path: str = "") -> HttpResponse:
    if request.POST:
        if request.session[OPERATION_SESSION_KEY] == CUT_OPERATION:
            service.move(request.session.get(CLIPBOARD_SESSION_KEY, []), files_path)
        elif request.session[OPERATION_SESSION_KEY] == COPY_OPERATION:
            service.copy(request.session.get(CLIPBOARD_SESSION_KEY, []), files_path)
        else:
            return HttpResponseBadRequest("Cannot paste from selected operation")

        request.session[CLIPBOARD_SESSION_KEY] = []
        request.session[OPERATION_SESSION_KEY] = None

    return ls(request, files_path)


def trash(request, files_path: str = "") -> HttpResponse:
    if not request.POST:
        return HttpResponseBadRequest()

    service.remove(request.POST.getlist("selected", []))
    return ls(request, files_path)


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
