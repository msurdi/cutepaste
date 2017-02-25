from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpRequest


class ExceptionMapperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        return self.get_response(request)

    @staticmethod
    def process_exception(request: HttpRequest, exception: Exception):
        if not settings.EXCEPTION_MAPPER_ENABLED:
            return
        if isinstance(exception, ObjectDoesNotExist):
            raise Http404
