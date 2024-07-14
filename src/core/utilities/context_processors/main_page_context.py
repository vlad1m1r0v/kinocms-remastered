from django.http import HttpRequest

from apps.banners.models import BannerSettings, TopBanner, AdvertisementBanner
from apps.pages.models import MainPage


def main_page_context(_: HttpRequest):
    banner_settings = BannerSettings.load()
    top_banners = TopBanner.objects.all()
    advertisement_banners = AdvertisementBanner.objects.all()
    main_page_info = MainPage.load()
    return {"banner_settings": banner_settings,
            "top_banners": top_banners,
            "advertisement_banners": advertisement_banners,
            "main_page_info": main_page_info}
