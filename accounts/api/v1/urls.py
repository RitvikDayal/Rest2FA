from django.urls import path
from .views import (
    UserLoginView,
    TOTPClientCreateView,
    TOTPVerifyView,
    ProtectView,
    UserRegistrationView,
    LogoutHandlerView,
)


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("log-out/", LogoutHandlerView.as_view(), name="user_logout"),
    path(
        "2fa/registration/", TOTPClientCreateView.as_view(), name="totp-client-register"
    ),
    path("2fa/verify/<int:token>/", TOTPVerifyView.as_view(), name="totp-verify"),
    path("2fa/protected/", ProtectView.as_view(), name="totp-protect"),
]
