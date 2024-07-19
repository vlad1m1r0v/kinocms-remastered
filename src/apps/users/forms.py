import django.forms
from django import forms
from django.forms import widgets
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from apps.users.models import CustomUser


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=widgets.Input(attrs={"class": "form-control", "placeholder": _("Enter Password"), "type": "password"}),
        min_length=6,
        max_length=30,
    )

    password2 = forms.CharField(
        label=_("Repeat Password"),
        required=True,
        widget=widgets.Input(attrs={"class": "form-control", "placeholder": _("Repeat Password"), "type": "password"}),
        min_length=6,
        max_length=30,
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "password2"
        ]

        labels = {
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "email": _("E-Mail"),
            "password": _("Password"),
            "password2": _("Repeat Password")
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter first name"), "minlength": 2,
                       "required": True}),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter last name"), "minlength": 2, "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Enter email address")}),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": _("Enter Password"), "type": "password"}, ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password != password2:
                raise forms.ValidationError(_("Passwords don't match"))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=widgets.Input(attrs={"class": "form-control", "placeholder": _("Enter email"), "type": "email"}),
    )
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=widgets.Input(attrs={"class": "form-control", "placeholder": _("Enter password"), "type": "password"}),
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

        labels = {
            "first_name": _('First Name'),
            "last_name": _('Last Name'),
            "nick_name": _('Nick Name'),
            "email": _('E-Mail'),
            "address": _('Address'),
            "card_number": _('Card Number'),
            "language": _('Language'),
            "sex": _('Sex'),
            "phone": _('Phone'),
            "birth_date": _('Birth date'),
            "city": _('City'),
        }

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Enter first name")}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Enter last name")}),
            "nick_name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Enter nickname")}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Enter email address")}),
            "address": forms.Textarea(attrs={"class": "form-control", "placeholder": _("Enter address"), "rows": 2}),
            "card_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter credit card number")}),
            "language": forms.Select(attrs={"class": "form-control", "placeholder": _("Select language")}),
            "sex": forms.Select(attrs={"class": "form-control", "placeholder": _("Select sex")}),
            "phone": forms.TextInput(attrs={"class": "form-control phone", "placeholder": _("Enter phone number")}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control datepicker", "placeholder": _("Select date of birth")}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Enter city")}),
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": 'form-control', "placeholder": _("Enter old password")}),
        required=False
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": 'form-control', "placeholder": _("Enter new password")}),
        required=False
    )

    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": 'form-control', "placeholder": _("Confirm new password")}),
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
                _("You must enter both old and new password fields"),
                code='password_mismatch'
            )

        if new_password1 and new_password2:
            if not check_password(old_password, self.user.password):
                raise forms.ValidationError(_("Old password is incorrect"), code='invalid_old_password')

            if new_password1 != new_password2:
                raise forms.ValidationError(
                    _("The two password fields didn't match"),
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
