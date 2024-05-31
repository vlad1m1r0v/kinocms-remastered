from django.forms import Form, EmailField, CharField
from django.forms import widgets


class LoginForm(Form):
    email = EmailField(
        label="Email",
        required=True,
        widget=widgets.Input(attrs={"class": "form-control", "placeholder": "Enter email", "type": "email"}),
    )
    password = CharField(
        label="Password",
        required=True,
        widget=widgets.Input(attrs={"class": "form-control", "placeholder": "Enter password", "type": "password"}),
        min_length=6,
        max_length=30,
    )
