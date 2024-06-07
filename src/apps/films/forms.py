from django import forms
from django.forms import inlineformset_factory

from apps.films.models import Film, FilmImage


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ["name_uk",
                  "name_en",
                  "description_uk",
                  "description_en",
                  "image",
                  "trailer_url",
                  "is_3d",
                  "is_2d",
                  "is_imax",
                  "seo_url",
                  "seo_title",
                  "seo_keywords",
                  "seo_description"
                  ]
        widgets = {
            "name_uk": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter film name in Ukrainian",
            }),
            "name_en": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter film name in English",
            }),
            "description_uk": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter film description in Ukrainian",
            }),
            "description_en": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter film description in English",
            }),
            "image": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
            "trailer_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Enter trailer URL",
            }),
            "is_3d": forms.CheckboxInput(attrs={
                "class": "form-control form-check-input"
            }),
            "is_2d": forms.CheckboxInput(attrs={
                "class": "form-control form-check-input"
            }),
            "is_imax": forms.CheckboxInput(attrs={
                "class": "form-control form-check-input"
            }),
            "seo_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO URL",
            }),
            "seo_title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO title",
            }),
            "seo_keywords": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO keywords",
            }),
            "seo_description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO description",
                "rows": 2,
            }),
        }


class FilmImageForm(forms.ModelForm):
    class Meta:
        model = FilmImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
        }


FilmImageFormSet = inlineformset_factory(
    parent_model=Film,
    model=FilmImage,
    form=FilmImageForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1)
