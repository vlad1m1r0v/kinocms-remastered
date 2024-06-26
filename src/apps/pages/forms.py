from django import forms
from .models import MainPage


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = [
            "is_active",
            "first_phone",
            "second_phone",
            "seo_text_uk",
            "seo_text_en",
            "seo_url",
            "seo_title",
            "seo_keywords",
            "seo_description",
        ]
        widgets = {
            "is_active": forms.CheckboxInput(attrs={'class': 'form-control custom-control-input'}),
            "first_phone": forms.TextInput(attrs={
                "class": "form-control phone",
                "placeholder": "Enter first phone number"
            }),
            "second_phone": forms.TextInput(attrs={
                "class": "form-control phone",
                "placeholder": "Enter second phone number"
            }),
            "seo_text_uk": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO text in Ukrainian"
            }),
            "seo_text_en": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO text in English"
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
