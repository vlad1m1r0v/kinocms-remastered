from django.http import HttpRequest

from apps.banners.models import BannerSettings, TopBanner, AdvertisementBanner
from apps.pages.models import MainPage, Page


def main_page_context(_: HttpRequest):
    banner_settings = BannerSettings.load()
    main_page = MainPage.load()
    pages = Page.objects.filter(is_active=True)

    return {"banner_settings": banner_settings,
            "main_page": main_page,
            "pages": pages}
