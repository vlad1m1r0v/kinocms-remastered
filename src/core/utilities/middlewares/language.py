from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import activate


class LanguageMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request: HttpRequest):
        if request.user.is_authenticated:
            language = request.user.language
        else:
            language = request.COOKIES.get('language')

        if language:
            activate(language.lower())
