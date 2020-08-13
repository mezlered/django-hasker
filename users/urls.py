from django.urls import path

from .views import SignUpView, Settings, AccountLogoutView, AccountLoginView

app_name = 'users'


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("settings/", Settings.as_view(), name="settings"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("login/", AccountLoginView.as_view(), name="login"),
]