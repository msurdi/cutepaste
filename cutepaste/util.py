from functools import wraps

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.safestring import mark_safe


def render_response(response: HttpResponse) -> str:
    return mark_safe(response.content.decode("utf-8"))


def ajax_only(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax():
            return view(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

    return _wrapped_view


def ic_redirect(response:HttpResponse, url:str) -> HttpResponse:
    response["X-IC-PushURL"] = url
    return response