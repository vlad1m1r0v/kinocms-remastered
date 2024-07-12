from django.http import HttpRequest, JsonResponse
from django.utils.translation import activate
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "site/main.html"


def change_language_view(request):
    language = request.POST.get('language')

    if request.user.is_authenticated:
        user = request.user
        user.language = language
        user.save()

    response = JsonResponse({'status': 'success'})
    response.set_cookie('language', language, max_age=365 * 24 * 60 * 60)
    return response
