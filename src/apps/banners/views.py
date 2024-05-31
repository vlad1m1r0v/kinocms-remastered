from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from apps.banners.forms import TopBannerSettingsForm, TopBannerFormSet, BannerSettingsForm, \
    AdvertisementBannerSettingsForm, AdvertisementBannerFormset
from apps.banners.models import BannerSettings, TopBanner, AdvertisementBanner
from core.utilities.guards import admin_only


@admin_only
class AdminBannersView(TemplateView):
    template_name = "adminlte/panel/banners.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        initial_settings = BannerSettings.load()
        # top banner settings
        context["top_banner_settings_form"] = TopBannerSettingsForm(
            instance=initial_settings,
            prefix="top_banner_settings")

        context["top_banner_formset"] = TopBannerFormSet(queryset=TopBanner.objects.all(),
                                                         prefix="top_banners")
        # background settings
        context["banner_settings_form"] = BannerSettingsForm(
            instance=initial_settings
        )
        # advertisement banner settings
        context["advertisement_banner_settings_form"] = AdvertisementBannerSettingsForm(
            instance=initial_settings,
            prefix="advertisement_banner_settings")

        context["advertisement_banner_formset"] = AdvertisementBannerFormset(
            queryset=AdvertisementBanner.objects.all(),
            prefix="advertisement_banners")

        return context


@admin_only
class AdminBackgroundSettingsView(View):
    @staticmethod
    def post(request, *args, **kwargs):
        form = BannerSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Background settings changed successfully")
        else:
            messages.error(request, "Some errors occurred while updating background settings")
        return redirect("adminlte_banners")


@admin_only
class AdminTopBannersView(View):
    @staticmethod
    def post(request, *args, **kwargs):
        top_banner_settings_form = TopBannerSettingsForm(request.POST, prefix="top_banner_settings")

        if top_banner_settings_form.is_valid():
            top_banner_settings_form.save()

        top_banner_formset = TopBannerFormSet(request.POST, request.FILES, prefix="top_banners")

        if top_banner_formset.is_valid():
            top_banner_formset.save()
            messages.success(request, "Top banners updated successfully")
        else:
            messages.error(request, "Some errors occurred while updating top banners")

        return redirect("adminlte_banners")


@admin_only
class AdminAdvertisementBannersView(View):
    @staticmethod
    def post(request, *args, **kwargs):
        advertisement_banner_settings_form = AdvertisementBannerSettingsForm(request.POST,
                                                                             prefix="advertisement_banner_settings")

        if advertisement_banner_settings_form.is_valid():
            advertisement_banner_settings_form.save()

        advertisement_banner_formset = AdvertisementBannerFormset(request.POST,
                                                                  request.FILES,
                                                                  prefix="advertisement_banners")

        if advertisement_banner_formset.is_valid():
            advertisement_banner_formset.save()
            messages.success(request, "Advertisement banners updated successfully")
        else:
            messages.error(request, "Some errors occurred while updating advertisement banners")

        return redirect("adminlte_banners")


@method_decorator(csrf_exempt, name='dispatch')
@admin_only
class AdminDeleteBackgroundView(View):
    @staticmethod
    def delete(request):
        banner_settings = BannerSettings.load()
        if banner_settings.background_image:
            banner_settings.background_image.delete()
            return JsonResponse({"status": 202})
        else:
            return JsonResponse({"status": 409})
