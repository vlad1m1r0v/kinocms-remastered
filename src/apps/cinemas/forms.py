from django import forms
from django.forms import inlineformset_factory

from .models import Cinema, CinemaImage


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = [
            "id",
            "name_uk",
            "name_en",
            "description_uk",
            "description_en",
            "features_uk",
            "features_en",
            "logo",
            "upper_banner",
            "seo_url",
            "seo_title",
            "seo_keywords",
            "seo_description",
        ]
        widgets = {
            "name_uk": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter cinema name in Ukrainian",
            }),
            "name_en": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter cinema name in English",
            }),
            "description_uk": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description in Ukrainian",
            }),
            "description_en": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description in English"
            }),
            "features_uk": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter features in Ukrainian"
            }),
            "features_en": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter features in English"
            }),
            "logo": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
            "upper_banner": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
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


class CinemaImageForm(forms.ModelForm):
    class Meta:
        model = CinemaImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
        }


CinemaImageFormSet = inlineformset_factory(
    parent_model=Cinema,
    model=CinemaImage,
    form=CinemaImageForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1,
)
