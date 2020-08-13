from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import SignUpForm, SettingsForm, AccountLoginForm
from django.contrib.auth.views import (
    LoginView, LogoutView, FormView,
)

from questions.views import TredingMixin
from .mixins import AnonimousRequired, UserRequired


class SignUpView(TredingMixin, AnonimousRequired, CreateView):
    form_class = SignUpForm
    model = get_user_model()
    success_url = reverse_lazy('users:settings')
    template_name = 'users/registrations.html'
    page_url = reverse_lazy('question:index')


    def post(self, *args, **kwargs):
        response = super(SignUpView, self).post(*args, **kwargs)
        obj = self.object
        if obj and obj.is_active:
            login(self.request, obj)
        return response


class AccountLogoutView(TredingMixin, UserRequired, LogoutView):
    template_name = 'users/logout.html'
    page_url = reverse_lazy("question:index")


class AccountLoginView(TredingMixin, AnonimousRequired, LoginView):
    template_name = 'users/login.html'
    form_class = AccountLoginForm
    page_url = reverse_lazy('users:settings')


class Settings(TredingMixin, UserRequired,  UpdateView):
    form_class = SettingsForm
    success_url = reverse_lazy("users:settings")
    template_name = "users/setting.html"
    page_url = reverse_lazy("users:login")

    def form_invalid(self, *args, **kwargs):
        self.object.refresh_from_db()
        return super().form_invalid(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user
