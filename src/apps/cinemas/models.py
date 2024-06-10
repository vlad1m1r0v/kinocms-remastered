from uuid import uuid4

from django.db import models
from core.utilities.models import SEOModel, get_upload_path


def get_cinema_logo_path(_: models.Model, filename: str) -> str:
    extension = filename.split('.')[-1]
    uuid = uuid4()
    return f'cinema_logo/{uuid}.{extension}'


def get_cinema_upper_banner_path(_: models.Model, filename: str) -> str:
    extension = filename.split('.')[-1]
    uuid = uuid4()
    return f'cinema_upper_banner/{uuid}.{extension}'


class Cinema(SEOModel):
    name_uk = models.CharField()
    name_en = models.CharField()
    description_uk = models.TextField()
    description_en = models.TextField()
    features_uk = models.TextField()
    features_en = models.TextField()
    logo = models.ImageField(upload_to=get_cinema_logo_path)
    upper_banner = models.ImageField(upload_to=get_cinema_upper_banner_path)


class CinemaImage(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
