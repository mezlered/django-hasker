from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AuthenticationForm
)


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'photo',)


class AccountLoginForm(AuthenticationForm):
    '''Logout'''


class SettingsForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "photo")
