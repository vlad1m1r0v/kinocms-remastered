from uuid import uuid4

from django.db import models

from apps.cinemas.models import Cinema
from core.utilities.models import SEOModel, get_upload_path


def get_hall_scheme_path(_: models.Model, filename: str) -> str:
    extension = filename.split('.')[-1]
    uuid = uuid4()
    return f'hall_scheme/{uuid}.{extension}'


def get_hall_upper_banner_path(_: models.Model, filename: str) -> str:
    extension = filename.split('.')[-1]
    uuid = uuid4()
    return f'hall_upper_banner/{uuid}.{extension}'


class Hall(SEOModel):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='halls')
    name_uk = models.CharField()
    name_en = models.CharField()
    description_uk = models.TextField()
    description_en = models.TextField()
    scheme = models.ImageField(upload_to=get_hall_scheme_path)
    upper_banner = models.ImageField(upload_to=get_hall_upper_banner_path)
    capacity = models.SmallIntegerField(default=200)


class HallImage(models.Model):
    cinema = models.ForeignKey(Hall, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
