from django.db import models

from core.utilities.models import Singleton, SEOModel


class MainPage(SEOModel, Singleton):
    is_active = models.BooleanField(default=True)
    first_phone = models.CharField()
    second_phone = models.CharField()
    seo_text_en = models.TextField()
    seo_text_uk = models.TextField()
    created_at = models.DateField(auto_now_add=True)
