from uuid import uuid4

from django.db import models

from core.utilities.models import get_upload_path, Singleton


class BaseBanner(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    url = models.URLField()

    class Meta:
        abstract = True


class AdvertisementBanner(BaseBanner):
    pass


class TopBanner(BaseBanner):
    description = models.TextField()


def get_background_image_path(_: models.Model, filename: str) -> str:
    extension = filename.split('.')[-1]
    uuid = uuid4()
    return f'background/{uuid}.{extension}'


class BannerSettings(Singleton):
    banner_rotation = models.PositiveSmallIntegerField(default=5)
    are_banners_active = models.BooleanField(default=True)
    advertisement_rotation = models.PositiveSmallIntegerField(default=5)
    are_advertisements_active = models.BooleanField(default=True)
    background_image = models.ImageField(upload_to=get_background_image_path, null=True, blank=True)
    is_background_image = models.BooleanField(default=True)
