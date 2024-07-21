from django.db import models
import urllib.parse
from core.utilities.models import SEOModel, get_upload_path


class News(SEOModel):
    is_active = models.BooleanField(default=True)
    publication_date = models.DateField()
    name_uk = models.CharField()
    name_en = models.CharField()
    description_uk = models.TextField()
    description_en = models.TextField()
    image = models.ImageField(upload_to=get_upload_path)
    video_url = models.URLField()

    @property
    def video_id(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.video_url).query)
        return params['v'][0]


class NewsImage(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
