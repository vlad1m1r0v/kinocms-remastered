from django.db import models

from core.utilities.models import SEOModel, get_upload_path


class Promotions(SEOModel):
    is_active = models.BooleanField(default=True)
    publication_date = models.DateField()
    name_uk = models.CharField()
    name_en = models.CharField()
    description_uk = models.TextField()
    description_en = models.TextField()
    image = models.ImageField(upload_to=get_upload_path)
    video_url = models.URLField()


class PromotionsImage(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    promotion = models.ForeignKey(Promotions, on_delete=models.CASCADE)
