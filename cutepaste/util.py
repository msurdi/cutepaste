from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe


def render_response(response: HttpResponse) -> str:
    return mark_safe(response.content.decode("utf-8"))


def ajax_redirect(url: str) -> JsonResponse:
    return JsonResponse({
        "script": f"Turbolinks.visit('{url}')"
    })
