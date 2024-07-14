from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileInput, URLInput, Textarea, modelformset_factory, Select, CheckboxInput, \
    RadioSelect

from apps.banners.models import TopBanner, BannerSettings, AdvertisementBanner


class TopBannerForm(ModelForm):
    class Meta:
        model = TopBanner
        fields = ["image", "url", "description"]
        widgets = {
            "image": FileInput(attrs={"class": "form-control custom-file-input",
                                      "type": "file"}),
            "url": URLInput(attrs={"class": "form-control custom",
                                   "aria-label": "Enter URL",
                                   "placeholder": "Enter URL"}),
            "description": Textarea(attrs={"class": "form-control",
                                           "aria-label": "Enter description",
                                           "placeholder": "Enter description",
                                           "rows": 3})
        }


TopBannerFormSet = modelformset_factory(model=TopBanner,
                                        form=TopBannerForm,
                                        can_delete=True,
                                        can_delete_extra=True,
                                        extra=1)


class TopBannerSettingsForm(ModelForm):
    class Meta:
        model = BannerSettings
        fields = ("banner_rotation", "are_banners_active")
        widgets = {
            'banner_rotation': Select(choices=((num, str(num)) for num in range(1, 11)),
                                      attrs={'class': 'form-control custom-select w-auto', }),
            'are_banners_active': CheckboxInput(attrs={'class': 'form-control custom-control-input'})
        }

    def save(self, commit=True):
        banner_settings = BannerSettings.load()
        banner_settings.banner_rotation = self.cleaned_data.get('banner_rotation')
        banner_settings.are_banners_active = self.cleaned_data.get('are_banners_active')
        banner_settings.save()


class BannerSettingsForm(ModelForm):
    class Meta:
        model = BannerSettings
        fields = ["background_image", "is_background_image"]
        widgets = {
            "is_background_image": RadioSelect(choices=[(True, 'Image on background'),
                                                        (False, 'Just background')],
                                               ),
            "background_image": FileInput(attrs={"class": "form-control custom-file-input",
                                                 "type": "file"})
        }

    def clean(self):
        is_background_image = self.cleaned_data.get('is_background_image')
        background_image = self.cleaned_data.get('background_image')

        if not is_background_image:
            return

        banner_settings = BannerSettings.load()

        if not background_image and not banner_settings.background_image:
            raise ValidationError("Background image not provided")

    def save(self, commit=True):
        banner_settings = BannerSettings.load()

        if self.cleaned_data['is_background_image'] is not None:
            banner_settings.is_background_image = self.cleaned_data['is_background_image']

        if self.cleaned_data['background_image']:
            banner_settings.background_image = self.cleaned_data['background_image']

        banner_settings.save()


class AdvertisementBannerForm(ModelForm):
    class Meta:
        model = AdvertisementBanner
        fields = ["image", "url"]
        widgets = {
            "image": FileInput(attrs={"class": "form-control custom-file-input",
                                      "type": "file"}),
            "url": URLInput(attrs={"class": "form-control custom",
                                   "aria-label": "Enter URL",
                                   "placeholder": "Enter URL"}),
        }


AdvertisementBannerFormset = modelformset_factory(model=AdvertisementBanner,
                                                  form=AdvertisementBannerForm,
                                                  can_delete=True,
                                                  can_delete_extra=True,
                                                  extra=1)


class AdvertisementBannerSettingsForm(ModelForm):
    class Meta:
        model = BannerSettings
        fields = ("advertisement_rotation", "are_advertisements_active")
        widgets = {
            'advertisement_rotation': Select(choices=((num, str(num)) for num in range(1, 11)),
                                             attrs={'class': 'form-control custom-select w-auto', }),
            'are_advertisements_active': CheckboxInput(attrs={'class': 'form-control custom-control-input'})
        }

    def save(self, commit=True):
        banner_settings = BannerSettings.load()
        banner_settings.advertisement_rotation = self.cleaned_data.get('advertisement_rotation')
        banner_settings.are_advertisements_active = self.cleaned_data.get('are_advertisements_active')
        banner_settings.save()
