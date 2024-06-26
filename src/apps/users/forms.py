import django.forms
from django import forms
from django.forms import widgets
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password

from apps.users.models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=widgets.Input(attrs={"class": "form-control", "placeholder": "Enter email", "type": "email"}),
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=widgets.Input(attrs={"class": "form-control", "placeholder": "Enter password", "type": "password"}),
        min_length=6,
        max_length=30,
    )


class UserForm(forms.ModelForm):
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'data-mask': '',
                   'data-inputmask-alias': 'datetime',
                   'data-inputmask-inputformat': 'dd/mm/yyyy',
                   'inputmode': 'numeric'},
            format='%d/%m/%Y'))

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "nick_name",
            "email",
            "address",
            "card_number",
            "language",
            "sex",
            "phone",
            "birth_date",
            "city",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter last name"}),
            "nick_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter nickname"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}),
            "address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter address", "rows": 2}),
            "card_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter credit card number"}),
            "language": forms.Select(attrs={"class": "form-control", "placeholder": "Select language"}),
            "sex": forms.Select(attrs={"class": "form-control", "placeholder": "Select sex"}),
            "phone": forms.TextInput(attrs={"class": "form-control phone", "placeholder": "Enter phone number"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control datepicker", "placeholder": "Select date of birth"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter city"}),
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": 'form-control', "placeholder": "Enter old password"}),
        required=False
    )
    new_password1 = forms.CharField(
        label="New password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": 'form-control', "placeholder": "Enter new password"}),
        required=False
    )

    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": 'form-control', "placeholder": "Confirm new password"}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if not new_password1 and not new_password2:
            return cleaned_data

        if not new_password1 or not new_password2:
            raise forms.ValidationError(
                "You must enter both old and new password fields",
                code='password_mismatch'
            )

        if new_password1 and new_password2:
            if not check_password(old_password, self.user.password):
                raise forms.ValidationError("Old password is incorrect", code='invalid_old_password')

            if new_password1 != new_password2:
                raise forms.ValidationError(
                    "The two password fields didn't match",
                    code='password_mismatch'
                )

            try:
                validate_password(new_password1)
            except forms.ValidationError as error:
                self.add_error('new_password1', error)

        return cleaned_data

    def save(self):
        if self.user and self.cleaned_data.get('new_password1'):
            new_password = self.cleaned_data['new_password1']
            self.user.password = make_password(new_password)
            self.user.save()
            return self.user
