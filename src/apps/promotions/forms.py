from django import forms
from django.forms import inlineformset_factory

from .models import PromotionsImage, Promotions


class PromotionsForm(forms.ModelForm):
    publication_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'data-mask': '',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd/mm/yyyy',
                   'inputmode': 'numeric'},
            format='%d/%m/%Y'))

    class Meta:
        model = Promotions
        fields = [
            "is_active",
            "publication_date",
            "name_uk",
            "name_en",
            "description_uk",
            "description_en",
            "image",
            "video_url",
            "seo_url",
            "seo_title",
            "seo_keywords",
            "seo_description"
        ]
        widgets = {
            "is_active": forms.CheckboxInput(attrs={'class': 'form-control custom-control-input'}),
            "name_uk": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter promotion name in Ukrainian",
            }),
            "name_en": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter promotion name in English",
            }),
            "description_uk": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description in Ukrainian"
            }),
            "description_en": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description in English"
            }),
            "image": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
            "video_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Enter video URL",
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


class PromotionsImageForm(forms.ModelForm):
    class Meta:
        model = PromotionsImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
        }


PromotionsImageFormSet = inlineformset_factory(
    parent_model=Promotions,
    model=PromotionsImage,
    form=PromotionsImageForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1)
