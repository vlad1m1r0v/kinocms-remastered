from django import forms
from django.forms import inlineformset_factory
from .models import Hall, HallImage


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = [
            "name_uk",
            "name_en",
            "description_uk",
            "description_en",
            "scheme",
            "upper_banner",
            "seo_url",
            "seo_title",
            "seo_keywords",
            "seo_description",
        ]
        widgets = {
            "name_uk": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter hall name in Ukrainian",
            }),
            "name_en": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter hall name in English",
            }),
            "description_uk": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description in Ukrainian",
            }),
            "description_en": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description in English",
            }),
            "scheme": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
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


class HallImageForm(forms.ModelForm):
    class Meta:
        model = HallImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
        }


HallImageFormSet = inlineformset_factory(
    parent_model=Hall,
    model=HallImage,
    form=HallImageForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1,
)
