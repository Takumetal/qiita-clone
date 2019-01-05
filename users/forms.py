from django.contrib.auth import forms as UserForms
from django.utils.translation import gettext_lazy as _

from django import forms



class LoginForm(UserForms.AuthenticationForm):
    email = forms.EmailField(_('Email address'),)