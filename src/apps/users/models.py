from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    nick_name = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    card_number = models.CharField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    language_choices = [
        ("UK", _("Ukrainian")),
        ("EN", _("English"))
    ]
    language = models.CharField(choices=language_choices, default='EN')

    sex_choices = [
        ("MALE", _("Male")),
        ("FEMALE", _("Female"))
    ]
    sex = models.CharField(choices=sex_choices, default='MALE')
    created_at = models.DateField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
