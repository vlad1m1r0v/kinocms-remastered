from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _


def change_language_view(request):
    language = request.POST.get('language')

    if request.user.is_authenticated:
        user = request.user
        user.language = language
        user.save()

    response = JsonResponse({'status': 'success'})
    response.set_cookie('language', language, max_age=365 * 24 * 60 * 60)

    activate(language.lower())

    messages.success(request, _('Language was changed successfully'))

    return response
