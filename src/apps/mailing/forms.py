from django import forms
from .models import Template


class SendingOptionForm(forms.Form):
    CHOICES = [
        ('Everyone', 'Everyone'),
        ('Selectively', 'Selectively'),
    ]

    choice_field = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label='Choose sending option'
    )


class UploadTemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['file', ]
        widgets = {
            'file': forms.FileInput(attrs={"class": "form-control custom-file-input", "type": "file"}),
        }
