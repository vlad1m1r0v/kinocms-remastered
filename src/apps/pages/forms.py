from django import forms
from django.forms import inlineformset_factory

from .models import MainPage, Page, PageImage, Contact, Contacts


class MainPageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MainPageForm, self).__init__(*args, **kwargs)
        self.fields['is_active'] = forms.BooleanField(
            initial=self.instance.is_active,
            widget=forms.CheckboxInput(attrs={'class': 'form-check custom-control-input', 'disabled': 'disabled'}),
            required=False,
        )

    class Meta:
        model = MainPage
        fields = [
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


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            "is_active",
            "name_uk",
            "name_en",
            "description_uk",
            "description_en",
            "image",
            "seo_url",
            "seo_title",
            "seo_keywords",
            "seo_description"
        ]
        widgets = {
            "is_active": forms.CheckboxInput(attrs={'class': 'form-control custom-control-input'}),
            "name_uk": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter page name in Ukrainian",
            }),
            "name_en": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter page name in English",
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


class PageImageForm(forms.ModelForm):
    class Meta:
        model = PageImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
        }


PageImageFormSet = inlineformset_factory(
    parent_model=Page,
    model=PageImage,
    form=PageImageForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1)


class ContactsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactsForm, self).__init__(*args, **kwargs)
        self.fields['is_active'] = forms.BooleanField(
            initial=self.instance.is_active,
            widget=forms.CheckboxInput(attrs={'class': 'form-check custom-control-input', 'disabled': 'disabled'}),
            required=False,
        )

    class Meta:
        model = Contacts
        fields = [
            "seo_url",
            "seo_title",
            "seo_keywords",
            "seo_description"
        ]
        widgets = {
            "seo_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO URL"
            }),
            "seo_title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO title"
            }),
            "seo_keywords": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO keywords"
            }),
            "seo_description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO description",
                "rows": 2
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['is_active',
                  'name_uk',
                  'name_en',
                  'address_uk',
                  'address_en',
                  'lat',
                  'lon',
                  'logo']
        widgets = {
            "is_active": forms.CheckboxInput(attrs={'class': 'form-control custom-control-input'}),
            "name_uk": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter contact name in Ukrainian"
            }),
            "name_en": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter contact name in English"
            }),
            "address_uk": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter address in Ukrainian"
            }),
            "address_en": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter address in English"
            }),
            "lon": forms.TextInput(attrs={
                "class": "form-control lon",
                "placeholder": "Enter longitude"
            }),
            "lat": forms.TextInput(attrs={
                "class": "form-control lat",
                "placeholder": "Enter latitude"
            }),
            "logo": forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
        }


ContactFormSet = inlineformset_factory(
    parent_model=Contacts,
    model=Contact,
    form=ContactForm,
    can_delete=True,
    can_delete_extra=True,
    extra=1)
