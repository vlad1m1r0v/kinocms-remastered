from django.db import models
from core.utilities.models import get_upload_path


class Template(models.Model):
    name = models.CharField(null=True, blank=True)
    file = models.FileField(upload_to=get_upload_path)

    def save(self, *args, **kwargs):
        self.name = self.file.name
        super().save(*args, **kwargs)
