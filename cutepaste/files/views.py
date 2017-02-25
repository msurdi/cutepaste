from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from os import path
from . import service


def ls(request: WSGIRequest, files_path: str = "") -> HttpResponse:
    parent_path = ""
    if files_path:
        parent_path = path.join(files_path, "..")

    return render(request, "files/index.html", {
        "entries": service.ls(files_path),
        "parent_path": parent_path,
    })
