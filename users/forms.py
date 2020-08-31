from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'photo',)


class SettingsForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "photo")
