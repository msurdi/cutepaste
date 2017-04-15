from os import path

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cutepaste.files import components
from cutepaste.files.forms import FilesEditForm
from cutepaste.util import ajax_redirect
from . import service

CLIPBOARD_SESSION_KEY = "clipboard"
OPERATION_SESSION_KEY = "operation"
OPERATION_SELECTED_KEY = "selected"
CUT_OPERATION = "cut"
COPY_OPERATION = "copy"


def ls(request, directory: str = "") -> HttpResponse:
    file = service.stat(directory)

    if file.is_file:
        response = HttpResponse()
        response["Content-Type"] = ""  # Let webserver decide this
        response["X-Accel-Redirect"] = file.absolute_path
        return response

    files = service.ls(directory)
    clipboard_files = request.session.get(CLIPBOARD_SESSION_KEY, [])
    return render(request, "files/index.html", {
        "browser": components.browser(
            files=files,
            directory=directory,
            clipboard_files=clipboard_files,
            selection_status="none"),
    })


def edit(request, directory: str = "") -> HttpResponse:
    files = service.ls(directory)
    edit_form = FilesEditForm(request.POST or None, files=files)

    return render(request, "files/edit.html", {
        "directory": directory,
        "edit_form": components.edit_form(
            form=edit_form,
            directory=directory,
        ),
    })


@api_view(["post"])
def rename(request):
    directory = request.POST.get("directory")
    files = service.ls(directory)
    edit_form = FilesEditForm(request.POST, files=files)

    if edit_form.is_valid():
        for relative_path, new_name in edit_form.cleaned_data.items():
            new_relative_path = path.join(directory, new_name)
            if relative_path != new_relative_path:
                service.rename(relative_path, new_relative_path)
        redirect_url = reverse("files:ls", args=[directory])
        return ajax_redirect(redirect_url)

    return JsonResponse({
        "components": {
            "#edit-form": components.edit_form(
                form=edit_form,
                directory=directory,
            ),
        }
    })


@api_view(["post"])
def copy(request) -> HttpResponse:
    clipboard_files = request.POST.getlist("selected", [])
    directory = request.POST.get("directory", "")
    selection_status = request.POST.get("selection_status", "none")

    request.session[OPERATION_SESSION_KEY] = COPY_OPERATION
    request.session[CLIPBOARD_SESSION_KEY] = request.POST.getlist("selected", [])

    return Response({
        "components": {
            "#buttons": components.buttons(
                directory=directory,
                clipboard_files=clipboard_files,
                selection_status=selection_status,
            )
        }
    })


@api_view(["post"])
def cut(request) -> Response:
    clipboard_files = request.POST.getlist("selected", [])
    directory = request.POST.get("directory", "")
    selection_status = request.POST.get("selection_status", "none")

    request.session[OPERATION_SESSION_KEY] = CUT_OPERATION
    request.session[CLIPBOARD_SESSION_KEY] = clipboard_files

    return Response({
        "components": {
            "#buttons": components.buttons(
                directory=directory,
                clipboard_files=clipboard_files,
                selection_status=selection_status,
            )
        }
    })


@cache_page(60 * 60 * 24)
@api_view(["get"])
def select(request) -> Response:
    clipboard_files = request.session.get(CLIPBOARD_SESSION_KEY, [])
    directory = request.GET.get("directory", "")
    selection_status = request.GET.get("selection_status", "none")

    return Response({
        "components": {
            "#buttons": components.buttons(
                directory=directory,
                clipboard_files=clipboard_files,
                selection_status=selection_status,
            )
        }
    })


@api_view(["get"])
def confirm_trash(request) -> Response:
    return Response({
        "components-inner": {
            "#messages": components.confirm_trash(),
        }
    })


@api_view(["post"])
def paste(request) -> HttpResponse:
    if not request.POST or "directory" not in request.POST:
        return HttpResponseBadRequest()

    directory = request.POST["directory"]
    if request.session[OPERATION_SESSION_KEY] == CUT_OPERATION:
        service.move(request.session.get(CLIPBOARD_SESSION_KEY, []), directory)
    elif request.session[OPERATION_SESSION_KEY] == COPY_OPERATION:
        service.copy(request.session.get(CLIPBOARD_SESSION_KEY, []), directory)
    else:
        return HttpResponseBadRequest("Cannot paste from selected operation")

    request.session[CLIPBOARD_SESSION_KEY] = []
    request.session[OPERATION_SESSION_KEY] = None
    return ajax_redirect(reverse("files:ls", args=[directory]))


@api_view(["post"])
def trash(request) -> HttpResponse:
    if "selected" not in request.POST:
        return HttpResponseBadRequest()

    directory = request.POST["directory"]
    service.remove(request.POST.getlist("selected", []))
    return ajax_redirect(reverse("files:ls", args=[directory]))
