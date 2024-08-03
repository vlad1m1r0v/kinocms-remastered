import urllib.parse

from django.db import models

from core.utilities.models import SEOModel, get_upload_path


class Film(SEOModel):
    name_uk = models.CharField()
    name_en = models.CharField()
    description_uk = models.TextField()
    description_en = models.TextField()
    image = models.ImageField(upload_to=get_upload_path)
    trailer_url = models.URLField()
    is_3d = models.BooleanField(default=False)
    is_2d = models.BooleanField(default=False)
    is_imax = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def video_id(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.trailer_url).query)
        return params['v'][0]


class FilmImage(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="images")
