from django.db import models

from core.utilities.models import Singleton, SEOModel, get_upload_path


class MainPage(SEOModel, Singleton):
    is_active = models.BooleanField(default=True)
    first_phone = models.CharField()
    second_phone = models.CharField()
    seo_text_en = models.TextField()
    seo_text_uk = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class Page(SEOModel):
    is_active = models.BooleanField(default=True)
    can_be_deleted = models.BooleanField(default=True)
    name_uk = models.CharField()
    name_en = models.CharField()
    description_uk = models.TextField()
    description_en = models.TextField()
    image = models.ImageField(upload_to=get_upload_path)
    created_at = models.DateField(auto_now_add=True)


class PageImage(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
