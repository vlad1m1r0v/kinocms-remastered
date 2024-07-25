from os.path import join
from os import listdir

from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import UploadedFile

from apps.banners.models import TopBanner, AdvertisementBanner, BannerSettings
from django.conf import settings


class Command(BaseCommand):
    help = "Create Banners for Website"

    def handle(self, *args, **options):
        # clear tables
        TopBanner.objects.all().delete()
        AdvertisementBanner.objects.all().delete()
        BannerSettings.load().delete()
        # background setting
        background_settings = BannerSettings.load()
        background_settings.is_background_image = True
        background_settings.are_banners_active = True
        background_settings.are_advertisements_active = True
        background_settings.banner_rotation = 5
        background_settings.advertisement_rotation = 5
        background_dir = join(settings.BASE_DIR, "images", "background")
        for file_name in listdir(background_dir):
            background_settings.background_image = UploadedFile(
                file=open(join(background_dir, file_name), 'rb')
            )
            break
        background_settings.save()
        # top banners
        top_banners_dir = join(settings.BASE_DIR, "images", "top_banners")
        top_banners: list[TopBanner] = []
        for index, file_name in enumerate(listdir(top_banners_dir)):
            top_banners += TopBanner(
                description=f"Description for Top Banner № {index + 1}",
                image=UploadedFile(file=open(join(top_banners_dir, file_name), 'rb')),
                url="https://www.imdb.com/"
            ),
        TopBanner.objects.bulk_create(objs=top_banners)
        # advertisement banners
        advertisement_banners_dir = join(settings.BASE_DIR, "images", "advertisement_banners")
        advertisement_banners: list[AdvertisementBanner] = []
        for index, file_name in enumerate(listdir(advertisement_banners_dir)):
            advertisement_banners += AdvertisementBanner(
                image=UploadedFile(file=open(join(advertisement_banners_dir, file_name), 'rb')),
                url="https://www.imdb.com/"
            ),
        AdvertisementBanner.objects.bulk_create(objs=advertisement_banners)

        self.stdout.write(
            self.style.SUCCESS("Banners and Background image were created successfully")
        )
