from django.db import models


class SEOModel(models.Model):
    seo_url = models.URLField()
    seo_title = models.CharField()
    seo_keywords = models.CharField()
    seo_description = models.TextField()

    class Meta:
        abstract = True

