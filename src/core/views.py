from django.http import JsonResponse
from django.views.generic import TemplateView
from apps.banners.models import BannerSettings, TopBanner, AdvertisementBanner


class MainPageView(TemplateView):
    template_name = "site/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["background_settings"] = BannerSettings.load()
        context["top_banners"] = TopBanner.objects.all()
        context["advertisement_banners"] = AdvertisementBanner.objects.all()
        return context


def change_language_view(request):
    language = request.POST.get('language')

    if request.user.is_authenticated:
        user = request.user
        user.language = language
        user.save()

    response = JsonResponse({'status': 'success'})
    response.set_cookie('language', language, max_age=365 * 24 * 60 * 60)
    return response
